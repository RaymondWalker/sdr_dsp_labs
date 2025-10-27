import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, get_window

from scipy.signal import lfilter

#------------------------------------
#Signal
#------------------------------------

fs = 2.4e6 #sample rate ( 2.4 MHz)
f_tone = 100e3 #100 kHz tone
N = 2048 # Fundamental period

t = np.arange(N) / fs

signal = np.exp(2j * np.pi * f_tone * t)

#------------------------------------
#gauss white noise (AWGN)
#------------------------------------
rng = np.random.default_rng(0)
noise_power = 0.01
noise = np.sqrt(noise_power/2) * (rng.standard_normal(N) + 1j *rng.standard_normal(N))
rx_signal = signal + noise


#------------------------------------
#Filtered signal (FIR Band-pass) -- look at window_method.py
#------------------------------------
from scipy.signal import firwin

numtaps = 101     #number of coefficients ( filter length)
lowcut  = 80e3    #lower cut off frequency (80kHz)
highcut = 120e3   #Uppoer cut off frequency (120kHZ)
fs      = 2.4e6   #sample rate (2.4MHz)


taps = firwin (
    numtaps,
    [lowcut, highcut],
    pass_zero=False,
    fs=fs,
    window='hann')

filtered_signal = lfilter(taps, 1.0, rx_signal)



#------------------------------------
#combine signals
#------------------------------------

w = np.hanning(N)
fft_rx_w_filtered = np.fft.fftshift(np.fft.fft(filtered_signal * w))
freqs = np.fft.fftshift(np.fft.fftfreq(N,1/fs))
mag_dbfs= 20*np.log10(np.abs(fft_rx_w_filtered) + 1e-15) 

#------------------------------------
#unfiltered signal for comparison
#------------------------------------

fft_rx_w = np.fft.fftshift(np.fft.fft(rx_signal * w))
mag_dbfs_before = 20*np.log10(np.abs(fft_rx_w) + 1e-15)


#------------------------------------
#Power spectral density
#----------------------------------measure_snr/snr.py--
f_psd, Pxx = welch(rx_signal, fs=fs, window='hann', nperseg = 256, noverlap=128, return_onesided=False, scaling='density')
f_psd = np.fft.fftshift(f_psd); Pxx = np.fft.fftshift(Pxx)
psd_db_hz =10*np.log10(Pxx + 1e-20) 

#------------------------------------
#Unfiltered SNR
#------------------------------------

# tone index ( neares bin to +f_tone after shift)
k0 = np.argmin(np.abs(freqs - f_tone))
bw_bins = 3
sig_bins = np.arange(k0-bw_bins, k0+bw_bins+1)


fft_rx_w_unfiltered = np.fft.fftshift(np.fft.fft(rx_signal * w))
P_sig_before = np.sum(np.abs(fft_rx_w_unfiltered[sig_bins])**2)
mask_before = np.ones_like(fft_rx_w_unfiltered, dtype=bool); mask_before[sig_bins] = False
P_noise_before = np.sum(np.abs(fft_rx_w_unfiltered[mask_before])**2) / np.sum(mask_before) * len(sig_bins)
SNR_est_before_dB = 10*np.log10(P_sig_before / P_noise_before + 1e-30)




#------------------------------------
#Filtered SNR
#------------------------------------


#total power from fft-filtered
P_sig = np.sum(np.abs(fft_rx_w_filtered[sig_bins])**2)
mask = np.ones_like(fft_rx_w_filtered, dtype=bool); mask[sig_bins] = False
P_noise = np.sum(np.abs(fft_rx_w_filtered[mask])**2) / np.sum(mask) * len(sig_bins) # equalize to same bin amount

#snr theory - general
SNR_th_db = 10*np.log10(1/ noise_power)

#snr after filtering
SNR_est_after_dB = 10*np.log10(P_sig / P_noise + 1e-30)

print(f"Theoretical SNR = {SNR_th_db:.1f} dB")
print(f"Estimated SNR = {SNR_est_after_dB:.1f} dB")

#------------------------------------
# Bandwidth
#------------------------------------

bw = highcut - lowcut
print(f"Filter bandwidth: {bw/1e3:.1f} kHz")
print(f"Main lobe width: ~{bw/fs*N:.2f} FFT bins")



#------------------------------------
# filter shape Plot
#------------------------------------

from scipy.signal import freqz
bw = highcut - lowcut
print(f"Filter bandwidth: {bw/1e3:.1f} kHz")
print(f"Main lobe width: ~{bw/fs*N:.2f} FFT bins")
w_hz, h = freqz(taps, worN=8000, fs=fs)
plt.figure(figsize=(6,3))
plt.plot(w_hz/1e3, 20*np.log10(np.abs(h)))
plt.title('FIR Filter Frequency Response')
plt.xlabel('Frequency (kHz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.tight_layout()
plt.show()


#------------------------------------
# Plot
#------------------------------------
fig, ax1 = plt.subplots(figsize=(8,4))
ax1.plot(freqs/1e3, mag_dbfs_before, color='gray', alpha=0.4, label='Before Filtering')
ax1.plot(freqs/1e3, mag_dbfs, color='b', label='After FIR Filter')
ax1.plot(f_psd/1e3, psd_db_hz, color='orange', alpha=0.6, label='PSD (Welch)')
ax1.set_xlabel('Frequency (kHz)')
ax1.set_ylabel('Magnitude (dB)', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_xlim(-fs/(2*1e3), fs/(2*1e3))
plt.title("SDR Synthetic 100kHz Tone with Noise — FFT + PSD + SNR")
ax1.grid(True)
ax1.legend()

snr_text = (
    f"Theoretical SNR = {SNR_th_db:.1f} dB\n"
    f"Estimated SNR (Before) = {SNR_est_before_dB:.1f} dB\n"
    f"Estimated SNR (After)  = {SNR_est_after_dB:.1f} dB"
)
plt.subplots_adjust(bottom=0.3)
plt.figtext(
    0.13, 0.05, snr_text,
    fontsize=9, ha='left', va='bottom', family='monospace'
)

plt.savefig("snr_demo.png", dpi=200, bbox_inches='tight')
plt.show()