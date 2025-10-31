"""
Butterworth band-pass filter

Great for maximally flat frequency response, no ripple
"""

from scipy.signal import butter, sosfilt, sosfreqz
import matplotlib.pyplot as plt
import numpy as np

#-----------------------------
#Params
#-----------------------------
fs = 2.4e6 # 2.4 MHz Sampling rate
lowcut = 80e3 # 80 kHz Lower cut-off frequency
highcut = 120e3 # 120kHz Upper cutoff frequency
order = 4 # Filter order controlling steepness

#-----------------------------
#Filter
#-----------------------------
sos = butter(order, [lowcut,highcut], btype='bandpass', fs=fs, output='sos')

#-----------------------------
#Plot
#-----------------------------

w, h = sosfreqz(sos, worN=2048, fs=fs)

plt.figure(figsize=(8, 4))
plt.plot(w/1e3, 20 * np.log10(np.abs(h) + 1e-20)) #prevent divide by zero error
plt.title(f"Butterworth IIR Band-Pass Filter (Order = {order})")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude (dB)")
plt.grid(True)
plt.show()