import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, get_window
import time
import pandas as pd


#Timing function for comparison
def time_function(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

#-------------------------
#Params
#-------------------------
fs     = 2.4e6   #2.4 MHz sample rate
f_tone = 100e3   #100kHz Tone
N      = 65536   # Very large length
t = np.arange(N) / fs

#AWGN
rng = np.random.default_rng(0)
noise_power = 0.001
signal = np.exp(2j * np.pi * f_tone * t)
rx_signal = signal + np.sqrt(noise_power / 2) * (rng.standard_normal(N) + 1j* rng.standard_normal(N))

#-------------------------
#Welch PSD 
#-------------------------
segment_lengths = [256, 1024, 4096, 16384]
plt.figure(figsize=(10,5))

timing_results = []

for seg in segment_lengths:
    # Time the Welch PSD call
    (f_psd, Pxx), elapsed = time_function(
        welch, rx_signal, fs, 'hann', seg, seg//2, scaling='density'
    )
    
    Pxx_db = 10*np.log10(Pxx + 1e-15)
    plt.plot(np.fft.fftshift(f_psd)/1e3, np.fft.fftshift(Pxx_db),
             label=f"nperseg={seg} (RBW={fs/seg/1e3:.1f} kHz, {elapsed*1e3:.1f} ms)")
    
    timing_results.append((seg, fs/seg, elapsed))

plt.xlabel("Frequency (kHz)")
plt.ylabel("Power (dB/Hz)")
plt.title("Resolution Bandwidth & Segment Length Trade-Off")
plt.grid(True)
plt.legend()
plt.xlim(-300, 300)
plt.show()

#-------------------------
#Time comparison
#-------------------------

print("Segment Length Timing Comparison:")
print("nperseg\tRBW (Hz)\tTime (ms)")
for seg, rbw, elapsed in timing_results:
    print(f"{seg}\t{rbw:10.1f}\t{elapsed*1e3:8.2f}")

# Convert timing results to DataFrame for plotting
df = pd.DataFrame(timing_results, columns=["nperseg", "RBW_Hz", "Time_s"])
df["RBW_kHz"] = df["RBW_Hz"] / 1e3
df["Time_ms"] = df["Time_s"] * 1e3

# Plot RBW vs. Time
plt.figure(figsize=(7,4))
plt.plot(df["RBW_kHz"], df["Time_ms"], 'o-', lw=2)
plt.xscale('log')
plt.xlabel("Resolution Bandwidth (kHz, log scale)")
plt.ylabel("Computation Time (ms)")
plt.title("Computation Time vs. Resolution Bandwidth")
plt.grid(True, which='both', ls='--')
plt.show()





