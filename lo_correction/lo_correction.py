import numpy as np
import matplotlib.pyplot as plt

#------------------------------------
# Parameters
#------------------------------------
fs = 2.4e6        # Sample rate (Hz)
N = 2**15         # Samples
delta_f = 6e3     # Residual LO offset (Hz)
A = 1.0           # Tone amplitude
SNR_dB = 20       # Additive noise
np.random.seed(0)

#------------------------------------
# Simulated received signal
#------------------------------------
n = np.arange(N)
x_clean = A * np.exp(1j * 2*np.pi * delta_f * n / fs)
noise_power = (A**2) / (2 * 10**(SNR_dB/10))
noise = np.sqrt(noise_power) * (np.random.randn(N) + 1j*np.random.randn(N))
x = x_clean + noise

#------------------------------------
# Frequency estimation (phase difference method)
#------------------------------------
def estimate_freq(x, fs):
    x1 = x[1:]
    x0 = x[:-1]
    return np.angle(np.mean(x1 * np.conj(x0))) * fs / (2*np.pi)

f_hat = estimate_freq(x, fs)

#------------------------------------
# Apply digital correction (NCO derotation)
#------------------------------------
phi = -2*np.pi * f_hat * n / fs
y = x * np.exp(1j * phi)

#------------------------------------
# Plot: Spectrum before and after correction
#------------------------------------
def plot_fft(signal, fs, title):
    N = len(signal)
    X = np.fft.fftshift(np.fft.fft(signal * np.hanning(N)))
    f = np.fft.fftshift(np.fft.fftfreq(N, 1/fs))
    plt.figure(figsize=(8,4))
    plt.plot(f/1e3, 20*np.log10(np.abs(X)+1e-15))
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude (dB)")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()

plot_fft(x, fs, "Before Correction — Residual LO Offset")
plot_fft(y, fs, "After Correction — Tone Recentered at DC")

#------------------------------------
# Plot: Phase vs Time (first few ms)
#------------------------------------
plt.figure(figsize=(8,4))
plt.plot(np.unwrap(np.angle(x[:4096])), label="Before")
plt.plot(np.unwrap(np.angle(y[:4096])), label="After")
plt.title("Phase Evolution Before vs After Correction")
plt.xlabel("Sample Index")
plt.ylabel("Unwrapped Phase (radians)")
plt.legend()
plt.grid(True)
plt.tight_layout()

#------------------------------------
# Plot: Constellation
#------------------------------------
plt.figure(figsize=(5,5))
plt.scatter(np.real(x[:2000]), np.imag(x[:2000]), s=3, alpha=0.6, label="Before")
plt.scatter(np.real(y[:2000]), np.imag(y[:2000]), s=3, alpha=0.6, label="After")
plt.title("IQ Constellation — Before vs After Digital Fine-Tuning")
plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.axis('equal')
plt.legend()
plt.grid(True)
plt.tight_layout()

print(f"True Δf = {delta_f:.1f} Hz")
print(f"Estimated Δf = {f_hat:.2f} Hz")
