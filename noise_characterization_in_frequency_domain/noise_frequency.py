import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch



#-------------------------
#Params
#-------------------------
fs     = 2.4e6
f_tone = 100e3 
N      = 65536
t      = np.arange(N) / fs



#-------------------------
#Signal + Noise Generation
#-------------------------
rng = np.random.default_rng(0)
noise_power = 0.01
signal = np.exp(2j * np.pi * f_tone * t)
rx_signal = signal + np.sqrt(noise_power / 2) * (rng.standard_normal(N) + 1j*rng.standard_normal(N))


#-------------------------
#Welch PSD
#-------------------------
f_psd, Pxx = welch(rx_signal, fs = fs, window = 'hann', nperseg = 2048, noverlap = 1024, scaling = 'density')
Pxx_db = 10* np.log10(Pxx + 1e-20)


#-----------------------------------
#Estimate Signal Band + Noise Floor (See theory)
#-----------------------------------
#define + / - 5 kHz around tone as "signal band"
band_mask = (f_psd > f_tone - 5e3) & (f_psd < f_tone + 5e3)
noise_mask = ~band_mask

P_sig = np.sum(Pxx[band_mask])
P_noise = np.sum(Pxx[noise_mask])
SNR_est_db = 10*np.log10(P_sig/P_noise + 1e-20)

#-------------------------
#Plot
#-------------------------
plt.figure(figsize=(10,5))
plt.plot(f_psd/1e3, Pxx_db, color='royalblue', lw=1.1, zorder=1, label="Welch PSD")
plt.axvspan((f_tone-5e3)/1e3, (f_tone+5e3)/1e3,
            color='orange', alpha=0.35, zorder=3, label='Signal Band')

plt.axhline(np.median(Pxx_db), color='gray', ls='--', lw=0.8, alpha=0.6, label='Noise Floor')
plt.title(f"Frequency-Domain Noise Characterization\nEstimated SNR = {SNR_est_db:.2f} dB")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Power Spectral Density (dB/Hz)")
plt.grid(True, which='both', ls=':', alpha=0.7)
plt.legend(frameon=True)
plt.show()