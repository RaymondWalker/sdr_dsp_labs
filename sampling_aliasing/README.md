## Sampling & Aliasing 

### Theory
When we digitize a signal, we take **samples** at a certain rate $f_{s}$. 
If the signal contains frequency higher than half of $f_{s}$, the components **fold back** into the lower band, this is known as **aliasing**.
$$
f_{alias} = | f_{signal} -kf_{s}| \space for \space some \space integer \space k
$$
The **Nyquist Frequency** is:

$$
f_N=\frac{f_s}{2} 
$$
And the nyquist frequency is the maximum frequency that can be uniquely represented without aliasing, which means the sample frequency should be twice as much as the frequency of the actual signal:
$$
f_s \geq 2f_{max}
$$


