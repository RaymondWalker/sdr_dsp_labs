## Noise Characterization in Frequency Domain

### Theory

In the SNR Analysis section, SNR was measured in the time domain, and we analyzed how filters impact the SNR in the same domain. 

In most real world systems, SNR is measured in the frequency domain instead, because there is more meaningful data to be pulled from a FFT. This is because the signal can be separate into different spectral components. 

When we take a FFT of a noisy signal, each bin represents energy over a small bandwidth, which is equal to the Resolution bandwidth: 

$$
RBW = \frac{f_s}{N_{FFT}}
$$

To measure SNR in the frequency domain, we first need to find the power of both the signal and the noise. We do this by **summing the power spectral density (PSD) across the signal band ($f \in signal\space band$)** and compare it to the **noise floor accross the rest of the spectrum ($f \notin signal \space band$)**:

$$
P_{signal} = \sum_{f\in signal\space band}|X(f)|^2 ,\space \space P_{noise}=\sum_{f\notin signal\space band}|X(f)|^2
$$
$$
SNR_{dB} = 10\log_{10}(\frac{P_{signal}}{P_{noise}})
$$

This is the same concept used within spectrum analyzers and SDR Software, where the noise floor is typicall expressed as **dB/Hz**.
In this approach, both total noise power and SNR depend on:

- The **window type**
- The **FFT Length** (RBW)
- The **averaging** method (Welch)

