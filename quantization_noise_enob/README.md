## Quantization Noise & Effective Number of Bits (ENOB)

### Theory
When an analog signal passes through an **Analog-to-Digital Converter (ADC)**, its continuous amplitude range is divided into discrete **quantization levels.** This introduces quantization error, which behaves like an additive white noise (assuming the signal isn't correlated with the quantization).

For an *ideal* ADC with N bits:
$$
SNR_{quantization} = 6.02N + 1.76dB
$$
This defines the **theoretical signal-to-noise ratio** due to solely to quantization - meaning that even in a perfectly noiseless system, a 12-bit converter will cap the best possible SNR at 74 dB

### Quick rundown

- ADC maps analog input to $\pm\space Vref$ to $2^n$ codes => step $\Delta = \frac{2V_{ref}}{2^N}$
- Quantization error acks like white noise
- Ideal SNR = $SNR_{quantization}$ (look above)
- If the Sines peak is **A**(relative to full scale peak **$V_{ref}$**) subtract back-off:
  $$
  SNR_{ideal,A} \approx \space 6.02N + 1.76 + 20\log_{10}(\frac{A}{V_{ref}})
  $$
  (e.g, with -6dBFS you lose ~-6dB)

### Concepts
|Concept    | Description | 
|:-----------:|:-----------:|
| Quantization Step($\Delta$) | Smallest change in amplitude represented by 1 Least sig Bit| 
| Quantization Noise Power| Uniformly distributed between $\pm \Delta / 2  => \space variance = \Delta ^2 / 12$ |
| Dynamic Range (DR)| Max signal level before clipping vs quantization floor |
|ENOB|Effective Number of Bits - Real world resolution including distortion|
|Trade-Off|More bits => higher SNR and SR, but slower sampling and larger data throughput|

