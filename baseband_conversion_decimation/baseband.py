import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin

# -------------------------
# Params
# -------------------------
fs  = 2.4e6  #sample rate
fRF = 1.20e6 # RF Tone
BW  = 100e3  # Desired channel bandwidth
N   = 2**18  # Samples
rng = np.random.default_rng(0) 

#Simulate input: main tone + out-of-band interference + Noise
t = np.arange(N)/fs
x = (0.8*np.exp(1j*2*np.pi*fRF*t)+  #main RF tone
     0.2*np.exp(1j*2*np.pi*(fRF+180e3)*t) + #out of band tone
     0.1 *np.exp(1j*2*np.pi*(fRF-300e3)*t))
x += (rng.normal(0, 0.02, N) + 1j*rng.normal(0, 0.02, N)) #noise + signal(RF + out of band)

# -------------------------
# Mix-Down ( freq translation)
# -------------------------

"""
You will see two signals, One that is a straight line, and one that looks like 
a proper 'oscillating signal'. 

This was confusing to me at first, but understand that we mixed our initial
signal to DC, which is why it is a straight line.

We can play with it by detuning the LO by adding / subtracting to fRF

TL;DR:

Our straight line (0Hz) is intended, the oscillating signal is out of band.



"""
fLO = fRF# sets to 0 Hz, see theory
lo = np.exp(-1j*2*np.pi*fLO*t) # local oscillator
x_mixed = x * lo # shift RF to baseband

# -------------------------
# Low pass filter
# -------------------------
cutoff = 0.6 * BW
h = firwin(321, cutoff = cutoff, fs=fs)
x_filt = np.convolve(x_mixed, h, mode='same')

# -------------------------
# Decimation
# -------------------------
R = 6 #decimation factor
fs_new = fs/R
x_dec = x_filt[::R]

# -------------------------
# Plot Frequency Spectra
# -------------------------
def psd(x, fs, nfft = 8192):
    X = np.fft.fftshift(np.fft.fft(x,nfft))
    f = np.fft.fftshift(np.fft.fftfreq(nfft, 1/fs))
    return f/1e6, 10*np.log10(np.abs(X)**2 / np.max(np.abs(X)**2))

fix, axs = plt.subplots(3, 1, figsize=(9,9))
plt.subplots_adjust(hspace=0.6)

f1, P1 = psd(x, fs)
f2, P2 = psd(x_mixed, fs)
f3, P3 = psd(x_dec, fs_new)

#input
axs[0].plot(f1, P1)
axs[0].set_title("RF Input (2.4 MS/s)") #mega-samples per sec
axs[0].set_ylabel("Power (dB)")

#input mixed
axs[1].plot(f2, P2, color='tab:orange')
axs[1].set_title("After Complex Mix-Down (shifted to 0 Hz)")
axs[1].set_ylabel("Power (dB)")
axs[1].axvspan(-BW/2/1e6, BW/2/1e6, color='orange', alpha = 0.15, label ='Target Band')
axs[1].legend()

axs[2].plot(f3, P3, color='tab:green')
axs[2].set_title(f"After LPF + Decimation by {R} (fs = {fs_new/1e3:.0f} kS/s)") #kiloSamples per second
axs[2].set_xlabel("Frequency (MHz)")
axs[2].set_ylabel("Power (dB)")
axs[2].set_xlim(-BW/1e6, BW/1e6)
axs[2].grid(True, ls=':')

plt.tight_layout()
plt.show()
