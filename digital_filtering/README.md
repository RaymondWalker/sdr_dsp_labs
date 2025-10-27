# Finite Impulse 

### Theory

\[
y[n]=\sum_k{k=0}^{N-1} x[k] \cdot h[n-k]
\]

where in frequency (much more simple operation)

\[
Y(f) = X(f) \cdot H(f)
\]

The goal is to design H(f) as to remove all unwanted noise and keep our main signal.

### Objective

Demonstrate FIR Filtering by removing out-of-band noise (~100kHz tone)

### Concepts
- Fir Design with 'scipy.signal.firwin'
- Frequency-domain interpretation of filtering
- SNR improvement and bandwidth tradeoffs

### Results
| Metric    | Before | After|
|:-----------:|:-----------:|:----------:|
| Estimated SNR | 20.0 dB | 27.3 dB |
