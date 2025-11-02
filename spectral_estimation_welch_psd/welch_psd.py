import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, get_window

#-------------------------
#Params
#-------------------------
fs = 2.4e6     # Sample Rate (2.4MHz )
f_tone = 100e3 # 100 kHz  tone
N = 16384      # samples
t = np.arange(N) / fs 

#tone + noise
rng = np.random.default_rng(0)
noise_power = 0.001
signal = np.exp(2j *np.pi *f_tone *t) 
rx_signal = signal + np.sqrt(noise_power/2)*(rng.standard_normal(N) + 1j * rng.standard_normal(N))

#-------------------------
#Single FFT with no Averaging
#-------------------------\
window = get_window('hann', N)
fft_vals = np.fft.fftshift(np.fft.fft(rx_signal * window))
freqs = np.fft.fftshift(np.fft.fftfreq(N,1/fs))
mag_db = 20*np.log10(np.abs(fft_vals)/np.max(np.abs(fft_vals))+1e-12)

#-------------------------
#Welch PSD Averaging
#-------------------------
f_psd, Pxx = welch(rx_signal, fs=fs, window ='hann', nperseg=1024, noverlap=512, scaling='density')
Pxx_db = 10*np.log10(Pxx + 1e-15)

#-------------------------
#Plot comparison
#-------------------------
plt.figure(figsize=(10,5))
plt.plot(freqs/1e3, mag_db, label='Single FFT Snapshot', color='gray', alpha=0.6)
plt.plot(np.fft.fftshift(f_psd)/1e3, np.fft.fftshift(Pxx_db), label='Welch PSD (Averaged)', color='orange', linewidth=1.8)
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude / Power (dB)")
plt.title("Welch Power Spectral Density (PSD) vs. Single FFT Snapshot")
plt.legend()
plt.grid(True)
plt.xlim(-fs/(2*1e3), fs/(2*1e3))
plt.show()