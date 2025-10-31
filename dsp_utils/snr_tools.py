import numpy as np

def estimate_snr(rx_signal, filtered_signal, fs, f_tone, bw_bins=3):
    """
    Estimate SNR before and after filtering using FFT bin integration.
    """
    N = len(rx_signal)
    freqs = np.fft.fftshift(np.fft.fftfreq(N, 1/fs))
    w = np.hanning(N)
    
    def power_components(sig):
        fft_sig = np.fft.fftshift(np.fft.fft(sig * w))
        k0 = np.argmin(np.abs(freqs - f_tone))
        sig_bins = np.arange(k0-bw_bins, k0+bw_bins+1)
        P_sig = np.sum(np.abs(fft_sig[sig_bins])**2)
        mask = np.ones_like(fft_sig, dtype=bool); mask[sig_bins] = False
        P_noise = np.sum(np.abs(fft_sig[mask])**2) / np.sum(mask) * len(sig_bins)
        return P_sig, P_noise
    
    P_sig_b, P_noise_b = power_components(rx_signal)
    P_sig_a, P_noise_a = power_components(filtered_signal)
    
    snr_before = 10*np.log10(P_sig_b / P_noise_b + 1e-30)
    snr_after  = 10*np.log10(P_sig_a / P_noise_a + 1e-30)
    
    return snr_before, snr_after