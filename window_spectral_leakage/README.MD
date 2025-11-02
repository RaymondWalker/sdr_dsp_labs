## Window & Spectral Leakage

### Theory

We can recall from the from the theory section of FIR that the relationship between our intput $x(\omega)$ and our output $y(\omega)$ was the transfer fuction  $h(\omega)$. When windowing, this operation becomes 'flipped', where we are only permitted to multiply h and x in the time domain;  rather than when filtering happens  in the frequency domain. 

When we observe a finite-lenght signal, x[n], this operation is equivalent to multiplying by a continuous signal by a rectangular window $w[n]$. In frequency domain, this is a convolution between the ideal spectrum and the Fourier transform of the window itself. This can be confusing, 

This convolution, however, introduces spectral leakage, where energy from one frequency 'leaks' into other frequencies, forming side lobes around the main tone. By applying different windowing techniques  ( Han, Hamming, Blackman, etc...) we can reduce the amplitude of the side lobes at the cost of widening the main lobe. The choice of the window represents teh trade-off between frequency resolution ( narrowing the main lobe) and leakage suppression (low side lobes).


### Analysis
Different windowing functions offer trade-offs between frequency resolution and leakage suppression.
A rectangular window provides the narrowest main lobe, allowing fine frequency resolution, but produces large side lobes that cause severe spectral leakage ( -26.50 dB).
The Hann and Hamming windows taper smoothly to zero at the edges, which reduces the side-lobe level and leakage at the cost of slightly widening the main lobe.
Finally, the Blackman window offers excellent leakage suppression—with side lobes over 70 dB below the main tone—but its main lobe is the widest, making it less effective at resolving closely spaced frequencies.
In short, each window balances clarity and precision differently: sharper windows reveal detail, while smoother ones suppress interference.