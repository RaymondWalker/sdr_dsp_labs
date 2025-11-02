## Complex Mixing (IQ), and Baseband Conversion

### Theory

When an SDR recieves a signal, the radio signal is at a very high frequency. To process it efficiently at a digital form, it must be shifted to a much lower frequency - close to **baseband** (centered at 0 Hz).
This is called **Mixing Down / Frequency Translation**.

To do so , we use a **complex explonential** (like what we've seen for fft's) as the local oscillator (LO):
$$
x_{mix}(t)=x_{RF}(t)\cdot e^{-j2\pi f_{LO} t}
$$
This process shifts the RF Frequency down, such that:
$$
f_{new}=f_{RF} - f_{LO}
$$

Choosing $f_{LO}$ to be the same as $f_{RF}$ (ie. Local oscillator = 2.4GHz, RF = 2.4GHz) the signal moves to **0 Hz** (baseband)

$$
x_{mixed}(t) = A\cdot e^{j2\pi (f_{RF}-f_{LO} t)}
$$
$$
f_{RF} =f_{LO} ,\space x_{mixed}(t) = A\cdot e^{j\cdot 0} = A \cdot 1 = A
$$

In laymans terms, we are turning our signal into an easy to measure DC**(Baseband)** Signal that can be further processed.

## Low-Pass Filtering and Decimation

### Theory
Once at baseband frequency, we only need to keep the signal around 0 Hz - the desired **bandwidth B**.
We will apply a **low-pass filter (LPF)** to remove anything outside this bandwidth.

Then, since the signal's new bandwidth will be much smaller, we can **decimate** the sample rate (reduce sample rate) by a factor of **R** -
*this can only be done after filtering, or else aliasing will occur*
$$
f_{s,new} = \frac {f_s}{R}
$$

This process is what SDR front-ends do when tunned into a station / frequency while avoiding aliasing.

### Code :