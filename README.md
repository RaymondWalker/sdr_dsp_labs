#  SDR DSP Labs  
*A practical lab notebook for exploring digital signal processing through simulation and SDR principles.*

---

## 📘 Overview
**SDR DSP Labs** is a growing collection of Python notebooks focused on the **fundamentals of digital signal processing (DSP)** and how they apply to **software-defined radio (SDR)**.  
Each section introduces theory, walks through a simulation, and visualizes results — making complex concepts intuitive and hands-on.

**Goal:** Build a working understanding of how SDR systems analyze, filter, and fine-tune signals in the digital domain.

---

##  Key Concepts Covered
- Fast Fourier Transform (FFT) & Frequency Analysis  
- Gaussian Noise Modeling & SNR Measurement  
- Windowing, Spectral Leakage, and PSD (Welch Averaging)  
- FIR and IIR Digital Filtering  
- Quantization & ADC Bit-Depth Effects  
- Sampling and Aliasing Behavior  
- Complex Mixing (IQ) and Baseband Conversion  
- Digital Fine-Tuning (Residual LO Error Correction)

---

##  Notebook Directory

| Section | Title | Concepts |
|----------|-------|-----------|
| **1.1** | FFT Foundations | Manual vs NumPy FFT, frequency bins |
| **1.3** | Gaussian Noise Modeling | AWGN generation, FFT visualization |
| **1.4** | SNR Estimation | Theoretical vs measured SNR, Welch PSD |
| **1.5** | FIR Filtering | Band-pass design, SNR improvement |
| **1.6** | IIR Filtering | Butterworth filter, stability comparison |
| **1.7** | Spectral Leakage | Window types, sidelobe level (PSL) |
| **1.8** | Welch PSD | Averaging, noise variance reduction |
| **1.9** | Resolution Bandwidth | Trade-offs between time and frequency resolution |
| **1.12** | Quantization & ENOB | ADC behavior, bit-depth scaling |
| **1.13** | Sampling & Aliasing | Nyquist theorem, aliasing visualization |
| **1.14** | Complex Mixing | Frequency translation to baseband |
| **1.15** | LPF & Decimation | Bandwidth reduction and resampling |
| **1.16** | Digital Fine-Tuning | NCO-based derotation for residual LO offsets |

---

##  Environment Setup
Install dependencies (Python 3.9+ recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy scipy matplotlib pandas jupyter

## Runinning the main Noteook:
    ```bash
    jupyter lab notebooks/SDR_DSP_notebook.ipynb

## Learning Outcome

Interpret FFT magnitude and phase results correctly

Measure and verify SNR in noisy environments

Design FIR and IIR filters and observe frequency response

Understand windowing and its impact on spectral shape

Simulate and correct residual frequency offsets digitally

