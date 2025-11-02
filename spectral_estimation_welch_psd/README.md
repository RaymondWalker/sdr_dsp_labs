## Spectral Estimation & Welch Power Spectral Density
### Theory
If we take a single FFT, it will show the frequency of one single time segment. This reading can be **noisy and unstable** . 
This happens because each FFT grame captures a small random snapshot of noise -so the spectral power will vary wildly from frame to frame. 

The **Welch Method** solves this by splitting the signal into overlapping segments, applying a window to each, taking the FFT, and then **averaging the power spectra** of all segments. This averaging reduces noise variance roughly by 1/N, where N is the number of averaged segments. 

The trade offs: 
- Longer segments results in higher frequency resolution but fewer averages ( noisier estimates).
- Shorter segments have a lower, smoother resolution with a more stable estimate.

Applying Welch averaging to an SDR spectrum display will make it smooth rather than flickering frame to frame

