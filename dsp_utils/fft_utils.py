import numpy as np
import matplotlib.pyplot as plt


def compute_fft(signal, fs, window='hann'):
    """
    Compute the FFT of a signal with optional windowing.

    Args:
        signal : np.ndarray
            Input time-domain signal
        fs : float
            Sampling frequency (Hz)
        window : str or np.ndarray
            Window type ('hann', 'hamming', etc.) or explicit array

    Returns:
        freqs : np.ndarray
            Frequency axis (Hz)
        mag_db : np.ndarray
            Normalized magnitude in decibels (dB)
    """
    N = len(signal)

    # --- handle window flexibly ---
    if isinstance(window, str):
        try:
            w = getattr(np, window)(N)
        except AttributeError:
            raise ValueError(f"Unknown window type: {window}")
    elif isinstance(window, np.ndarray):
        if len(window) != N:
            raise ValueError("Window length must match signal length")
        w = window
    else:
        raise TypeError("window must be a string or NumPy array")

    # --- apply window and FFT ---
    sig_win = signal * w
    X = np.fft.fftshift(np.fft.fft(sig_win))
    freqs = np.fft.fftshift(np.fft.fftfreq(N, 1/fs))

    # --- normalize magnitude ---
    mag_db = 20 * np.log10(np.abs(X) / np.max(np.abs(X)) + 1e-15)
    return freqs, mag_db 

def plot_spectrum(freqs, mag_dbfs, label=None, color='b'):
    plt.plot(freqs/1e3, mag_dbfs, color=color, label=label)
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True)
    if label: plt.legend()

def measure_psl(signal, fs, window, guard_bins=10):
    """
    Measure Peak Sidelobe Level (PSL) relative to main lobe.
    
    Parameters:
        signal: array-like, time-domain signal
        fs: float, sampling rate
        window: array-like, window function
        guard_bins: int, number of bins around the main tone to ignore

    Returns:
        psl_db: float, PSL in dB
    """
    N = len(signal)
    # RMS-normalize the window to keep comparisons fair
    w_norm = window / np.sqrt(np.mean(window**2))
    sig_win = signal * w_norm

    X = np.fft.fft(sig_win)
    mag = np.abs(X)

    # Find main peaks (for real signal, two symmetric peaks)
    main_bin = np.argmax(mag)
    sym_bin = (N - main_bin) % N

    # Exclude ±guard_bins around both peaks
    mask = np.ones_like(mag, dtype=bool)
    for center in [main_bin, sym_bin]:
        a = max(center - guard_bins, 0)
        b = min(center + guard_bins + 1, N)
        mask[a:b] = False

    peak_side = np.max(mag[mask])
    peak_main = np.max(mag[~mask])
    psl_db = 20 * np.log10(peak_side / (peak_main + 1e-20))
    return psl_db


def plot_window_spectra(signal, fs, windows_dict):
    """
    Plot spectra for multiple windows for visual comparison.

    Parameters:
        signal: array-like, time-domain signal
        fs: sampling rate (Hz)
        windows_dict: dict {name: window_array}
    """
    plt.figure(figsize=(9, 5))
    N = len(signal)
    for name, w in windows_dict.items():
        freqs = np.fft.fftshift(np.fft.fftfreq(N, 1/fs))
        fft_vals = np.fft.fftshift(np.fft.fft(signal * w))
        mag_db = 20 * np.log10(np.abs(fft_vals)/np.max(np.abs(fft_vals)) + 1e-15)
        plt.plot(freqs, mag_db, label=name)
    plt.title("Spectral Leakage - Effect of Windowing")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized Magnitude (dB)")
    plt.legend()
    plt.grid(True)
    plt.xlim(0, fs/2)
    plt.show()