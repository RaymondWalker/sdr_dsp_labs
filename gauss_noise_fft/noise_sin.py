import numpy as np
import matplotlib.pyplot as plt

fs = 2.4e6 #sample rate ( 2.4 MHz)
f_tone = 100e3 #100 kHz tone
N = 2048 # Fundamental period

t = np.arange(N) / fs
signal = np.exp(2j * np.pi * f_tone * t)

#gauss white noise
noise_power = 0.01
noise = np.sqrt(noise_power/2) * (np.random.randn(N) + 1j *np.random.randn(N))

#combine signals
rx_signal = signal + noise

fft_rx = np.fft.fftshift(np.fft.fft(rx_signal))

#fk = k / N * fs
freqs = np.fft.fftshift(np.fft.fftfreq(N, 1/fs))

#Unwrap phase to prevent sudden jumps (degs)
phase = np.unwrap( (180 / np.pi) * (np.angle(fft_rx)))

magnitude = 20*np.log10(np.abs(fft_rx) / np.max(np.abs(fft_rx)))

#fig and axisw
fig, ax1 = plt.subplots(figsize=(8,4))

#plot as dB in relation to kHz
ax1.plot(freqs/1e3, magnitude, color = 'b', label = 'Magnitude(dB)' )
ax1.set_xlabel('Frequency (kHz)')
ax1.set_ylabel('Magnitude (dB)', color = 'b')
ax1.tick_params(axis = 'y', labelcolor='b')

#center plot
ax1.set_xlim(-fs/(2*1e3), fs/(2*(1e3)))

#plot phase in relation to kHz
ax2 = ax1.twinx()
ax2.plot(freqs/1e3, phase, color = 'r', linestyle='--', label='Phase (rad)')
ax2.set_ylabel('Phase (degrees)', color ='r')
ax2.tick_params(axis='y', labelcolor='r')


plt.title("SDR Synthetic 100kHz tone (with noise) and analysis + Phase vs Freq")
ax1.grid(True)
ax2.grid(True)
plt.show()
