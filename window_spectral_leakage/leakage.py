import sys, os
sys.path.append(os.path.abspath("/home/ostrich/Dev/sdr_dsp_labs"))
from dsp_utils import compute_fft, plot_spectrum, measure_psl
import numpy as np
import matplotlib.pyplot as plt

#-------------------------
#Params
#-------------------------

fs = 1000 # 1kHz Sample rate
f_tone = 123.4 # Choose tone not aligned with fft bins
N = 256# Small sample to exaggerate leakage

t = np.arange(N) / fs
signal = np.sin(2*np.pi*f_tone*t)

#-------------------------
#Define Window Types
#-------------------------
windows = {
    "Rectangular": np.ones(N),
    "Hann": np.hanning(N),
    "Hamming": np.hamming(N),
    "Blackman": np.blackman(N),
}

#-------------------------
#Compute FFT For Each Kind of Window
#-------------------------
plt.figure(figsize=(9,5))
for name, w in windows.items():
    freqs, mag_db = compute_fft(signal,fs, window = w)

    plt.plot(freqs, mag_db, label=name)

#-------------------------
#Plot
#-------------------------

plt.title("Spectral Leakage - Effect of Windowing")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Normalized Magnitude (dB)")
plt.legend()
plt.grid(True)
plt.xlim(0, fs/2)
plt.show()

#-------------------------
#Measure Leakage for Each Window
#-------------------------

print("Peak Sidelobe Level (dB relative to main lobe):")
for name, w in windows.items():
    psl_db = measure_psl(signal, fs, w, guard_bins=10)
    print(f"{name:12s}: {psl_db:6.2f} dB")