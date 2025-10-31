import numpy as np
import matplotlib.pyplot as plt

def compute_fft(signal, fs, window='hann'):
    """
    Compute windowed FFT and return frequency/magnitude arrays.
    """
    N = len(signal)
    w = np.hanning(N) if window == 'hann' else np.ones(N)
    fft_out = np.fft.fftshift(np.fft.fft(signal * w))
    freqs = np.fft.fftshift(np.fft.fftfreq(N, 1/fs))
    mag_dbfs = 20 * np.log10(np.abs(fft_out) + 1e-15)
    return freqs, mag_dbfs

def plot_spectrum(freqs, mag_dbfs, label=None, color='b'):
    plt.plot(freqs/1e3, mag_dbfs, color=color, label=label)
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True)
    if label: plt.legend()