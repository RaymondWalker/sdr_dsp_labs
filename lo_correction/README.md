## Digital Fine-Tuning and Residual LO Error Correction

### Theory

#### Error caused by mismatch

In a perfect world, aka our simulations, the **local oscillator** will mix perfectly with the RF signal so that the signal sits at DC in baseband. 
However, this is never perfect. This error shows up as a **residual frequency error**, which causes the baseband signal to **slowly rotate** in the complex(I/Q) Plane.

Lets start with the original equation:
$$
x_{mixed}(t) = A\cdot e^{j2\pi (f_{RF}-f_{LO} t)}
$$

Assuming $f_{RF} \neq f_{LO}$, we can say that $\Delta f = f_{RF} - f_{LO}$:
$$
X_{mixed}(n) = A\cdot e^{j2\pi \frac{\Delta f n}{f_s} }
$$

This means that $A\cdot e^{j2\pi \frac{\Delta f}{f_s} }$ term means the phasor will keep rotating, rather than be at 0 Hz it will be $ \pm \Delta f$. This can cause failures in decoding and demodulating certain techniques such as QPSK. 

#### Fixing it Digitally

We can fix the residual frequency using a **Numerically Controlled Oscillator (NCO)**, Which acts as a digital sine-wave generator we multiply with the signal to "derotate" it. 

But to do so, we need to estimate the offset. 
There are two simple ways:

##### a.) FFT-Peak Estimate

Take a FFT of the baseband and find where the largest magnitude peak sits. 
This will give a course estimate of $\Delta f$, which is good for small data sets or when expecting a single tone.

##### b.) Phase- Difference Estimate

A faster and cleaner trick for narrowband or high-SNR sigals:
$$
\hat \omega = \angle(mean(x[n]x^*[n-1]))
$$
$$
\hat f = \frac{\hat \omega f_s} {2 \pi}
$$

This measures the *average phase advance per sample*.
If you phase increases by 0.0157 rad per sample at 16 kHz, that's roughly a 40 Hz offset. 

Once you have $\hat f$, you can apply the correction to the original formula:
$$
X_{mixed}(n) = x[n]\cdot e^{j2\pi \frac{\hat f n}{f_s} }
$$

This will allow the tone / carrier to move back to DC. 

### code :
