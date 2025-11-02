import numpy as np
import matplotlib.pyplot
from scipy.signal import welch

#-------------------------
#Params
#-------------------------
fs       = 2.4e6  #Sample Rate
f_tone   = 100e3  #Sample Tone
N        = 65536  #samples
Vref     = 1.0    # ADC full-scale voltage is -1 <= V <= 1
FE_gain  = 0.95   # front - end gain (AGC)
A_in     = 0.9 * Vref #Analog input before FE Gain
sigma_an = 1e-4   # analog pre-adc noise (volts rms)

t = np.arange(N)/fs
xin = A_in * np.sin(2*np.pi*f_tone*t) + np.random.default_rng(0).normal(0,sigma_an, N)
x_fe = FE_gain * xin #front end applied

#-------------------------
#Ideal mid-rise ADC quantizer
#-------------------------
def adc_quantize(x, bits, vref):
    """
    Mid-rise uniform quantizer for + / - vref input.
    returns (x_quantized_volts, integer_codes)
    """
    L = 2**bits
    delta = 2*vref / L
    #clip input to +/- vref
    x_clipped = np.clip(x,-vref,vref -1e-12) #right edge for bins
    
    #map to 0 to L-1
    codes = np.floor((x_clipped + vref)/delta).astype(int)
    #mid-rise reconstruction level (center of bins)
    xq = (codes + 0.5) * delta - vref
    return xq, codes


#fix constant enob
def total_snr(x, x_ref):
    noise = x - x_ref
    return 10*np.log10(np.mean(x_ref**2)/np.mean(noise**2))


#-------------------------
#Welch SNR Estimate
#-------------------------
def psd_snr(x, fs, f0, band_hz=10e3, nperseg=4096, noverlap=2048, search_hz=30e3):
    from scipy.signal import welch
    f, Pxx = welch(x, fs=fs, window='hann', nperseg=nperseg,
                   noverlap=noverlap, scaling='density', return_onesided=False)
    f = np.fft.fftshift(f)
    Pxx = np.fft.fftshift(Pxx)

    # --- find actual tone peak within a small search window around f0 ---
    search = (f > (f0 - search_hz)) & (f < (f0 + search_hz))
    if not np.any(search):
        # fallback: use f0 directly
        f_peak = f0
    else:
        idx_peak = np.argmax(Pxx[search])
        f_peak = f[search][idx_peak]

    # integrate ±band_hz around the detected peak
    sig_band   = (f > (f_peak - band_hz)) & (f < (f_peak + band_hz))
    noise_band = ~sig_band

    P_sig   = np.sum(Pxx[sig_band])
    P_noise = np.sum(Pxx[noise_band]) / np.sum(noise_band) * np.sum(sig_band)
    SNRdB   = 10*np.log10(P_sig/(P_noise + 1e-30))
    return SNRdB, f, Pxx, f_peak

#-------------------------
#Run for multiple bit depths
#-------------------------
bit_depts = [4, 6, 8, 12]
results = []

plt.figure(figsize=(10,5))
for i, B in enumerate(bit_depts):
    xq, _ = adc_quantize(x_fe, B, Vref)
    __, f_psd, Pxx, f_peak = psd_snr(xq, fs, f_tone)
    SNRdB = total_snr(xq, x_fe)## fix constant enob
    # Ideal quantization SNR adjusted for back-off from full-scale peak
    # Full-scale peak = Vref. Our sine peak after FE = FE_gain*A_in.
    A_peak_after = FE_gain * A_in
    backoff_dB = 20*np.log10((A_peak_after + 1e-30)/(Vref + 1e-30))  # negative for backoff
    SNR_ideal_adj = 6.02*B + 1.76 + backoff_dB

    ENOB_meas = (SNRdB - 1.76 - backoff_dB)/6.02

    results.append((B, SNRdB, SNR_ideal_adj, ENOB_meas))

    # Plot PSD (in dB/Hz)
    Pxx_db = 10*np.log10(Pxx + 1e-20)
    plt.plot(f_psd/1e3, Pxx_db, lw=1.0, label=f"{B}-bit (SNR={SNRdB:.1f} dB)")


plt.axvspan((f_tone-5e3)/1e3, (f_tone+5e3)/1e3, color='orange', alpha=0.25, zorder=3, label='Signal Band')
plt.title("Quantization Noise vs Bit Depth — Welch PSD (realistic ADC chain)")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Power Spectral Density (dB/Hz)")
plt.grid(True, ls=':', alpha=0.7)
plt.xlim(-fs/(2*1e3), fs/(2*1e3))
plt.axvline(0, color='gray', lw=0.8, ls='--', alpha=0.6)

plt.legend(ncol=2, fontsize=9)
plt.show()

# -----------------------------
# Print summary table
# -----------------------------
print("ADC Quantization: Measured vs Theoretical SNR and ENOB")
print(f"(fs={fs/1e6:.1f} MHz, tone={f_tone/1e3:.0f} kHz, FE gain={FE_gain:.2f}, A_in={A_in/Vref:.2f}·Vref peak)")
print("Bits  MeasSNR(dB)  IdealSNR_adj(dB)   ENOB_meas")
for B, snr_meas, snr_id, enob in results:
    print(f"{B:>4}  {snr_meas:11.2f}      {snr_id:12.2f}      {enob:8.2f}") 
    
# -----------------------------
# Visualization: SNR and ENOB vs Bit Depth
# -----------------------------
import matplotlib.pyplot as plt
import numpy as np

# Extract data
bits = np.array([r[0] for r in results])
snr_meas = np.array([r[1] for r in results])
snr_ideal = np.array([r[2] for r in results])
enob_meas = np.array([r[3] for r in results])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

# --- SNR vs Bits ---
ax1.plot(bits, snr_meas, 'o-', lw=2, label='Measured SNR')
ax1.plot(bits, snr_ideal, 's--', lw=2, label='Ideal SNR (Adjusted)')
ax1.set_xlabel("Bit Depth (bits)")
ax1.set_ylabel("SNR (dB)")
ax1.set_title("SNR vs Bit Depth")
ax1.grid(True, ls=':')
ax1.legend()
ax1.text(bits[-1]-1, snr_meas[-1]-10, "≈6 dB/bit", fontsize=9, color='gray')

# --- ENOB vs Bits ---
ax2.plot(bits, enob_meas, 'o-', lw=2, color='tab:green', label='Measured ENOB')
ax2.plot(bits, bits, 's--', lw=2, color='tab:orange', label='Ideal ENOB = N bits')
ax2.set_xlabel("Bit Depth (bits)")
ax2.set_ylabel("ENOB (bits)")
ax2.set_title("Effective Number of Bits (ENOB)")
ax2.grid(True, ls=':')
ax2.legend()

plt.suptitle("ADC Performance Summary — SNR and ENOB Scaling", fontsize=13)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
