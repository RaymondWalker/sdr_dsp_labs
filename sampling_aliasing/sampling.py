import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Parameters
# -------------------------
f_signal = 3e3   # 3 kHz tone
dur = 2e-3       # 2 ms duration
fs_list = [12e3, 6e3, 4e3, 2e3]  # sample rates (above, equal, below Nyquist)

# -------------------------
# Generate continuous signal
# -------------------------
t_cont = np.linspace(0, dur, 10000)
x_cont = np.sin(2*np.pi*f_signal*t_cont)

# -------------------------
# Plot setup
# -------------------------
fig, axes = plt.subplots(len(fs_list), 2, figsize=(11, 10))  # Taller figure
plt.subplots_adjust(hspace=0.8, wspace=0.35)  # More vertical space between rows
fig.suptitle("Aliasing Demonstration — Effect of Sampling Rate", fontsize=16, weight='bold', y=0.95)

# -------------------------
# Loop through sampling rates
# -------------------------
for i, fs in enumerate(fs_list):
    # Sample signal
    t = np.arange(0, dur, 1/fs)
    x = np.sin(2*np.pi*f_signal*t)

    # Compute FFT
    N = 2048
    X = np.fft.fftshift(np.fft.fft(x, N))
    freqs = np.fft.fftshift(np.fft.fftfreq(N, 1/fs))
    mag_db = 20*np.log10(np.abs(X)/np.max(np.abs(X)) + 1e-12)

    # Compute alias frequency
    f_alias = abs(f_signal - round(f_signal/fs) * fs)

    # ---- Time-domain plot ----
    ax_t = axes[i, 0]
    ax_t.plot(t_cont * 1e3, x_cont, 'gray', lw=1.5, label='Original 3 kHz (continuous)')
    ax_t.stem(t * 1e3, x, linefmt='C0-', markerfmt='C0o', basefmt=" ", label=f'Sampled @ {fs/1e3:.1f} kHz')
    ax_t.set_title(f"Time Domain — fs = {fs/1e3:.1f} kHz", fontsize=12, weight='bold')
    ax_t.set_xlabel("Time (ms)")
    ax_t.set_ylabel("Amplitude")
    ax_t.set_xlim(0, dur*1e3)
    ax_t.legend(loc='upper right', fontsize=8)
    ax_t.grid(True, ls=':', alpha=0.7)

    # ---- Frequency-domain plot ----
    ax_f = axes[i, 1]
    ax_f.plot(freqs/1e3, mag_db, 'C1', lw=1.5)
    ax_f.axvline(f_signal/1e3, color='gray', ls='--', lw=0.8, alpha=0.8)
    ax_f.axvline(-f_signal/1e3, color='gray', ls='--', lw=0.8, alpha=0.8)
    ax_f.axvline(f_alias/1e3, color='r', ls='--', lw=1.0, alpha=0.8, label=f"Aliased @ {f_alias/1e3:.2f} kHz")
    ax_f.axvline(-f_alias/1e3, color='r', ls='--', lw=1.0, alpha=0.8)
    ax_f.set_xlim(-6, 6)
    ax_f.set_ylim(-60, 5)
    ax_f.set_title("Frequency Spectrum (FFT)", fontsize=12, weight='bold')
    ax_f.set_xlabel("Frequency (kHz)")
    ax_f.set_ylabel("Magnitude (dB)")
    ax_f.legend(loc='lower right', fontsize=8)
    ax_f.grid(True, ls=':', alpha=0.7)

plt.show()
