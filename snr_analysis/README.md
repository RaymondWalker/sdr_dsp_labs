## Signal-to-Noise Ratio (SNR) & Noise Analysis ( Explanation)

While covered before in passing, I felt it worth pausing to go more in depth on what noise and **SNR** meant and why it was important to our filtering sections. 


### Theory

In any signal acquisition system, from SDR to radar or microphones, noise is inevitable. The **Signal-to-Noise Ratio (SNR)** identifies how strong a signal is compared to the noise around: 
$$ 
SNR_{linear} = \frac{P_{signal}}{P_{noise}}
$$
$$
SNR_{dB} = 10\log_{10}(\frac{P_{signal}}{P_{noise}})
$$

Where:

- $P_{signal}$ is the power of the signal we want to measure
- $P_{noise}$ is the power of the noise of the environment

When the digital filters were applied, $h(n)$ / $h(\omega)$ was designed to remove as much noise power as possible without distorting the main signal. Contrasting both **IIR** and **FIR** in this role:

- **FIR** filters provided a stable, linear-phase filter but require more coefficients
- **IIR** filters offered sharper roll-off with less coefficients, but at the cost of phase distortion

A common way to estimate SNR Numerically:



$$
SNR = 10\log_{10}(\frac{mean(x_{signal}^2)}{mean(x_{noise}^2)})
$$