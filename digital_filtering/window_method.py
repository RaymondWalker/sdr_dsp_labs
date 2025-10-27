"""
easiest way to design h[k] : 
Window Method (hann)

Generates band-pass FIR centered around 100 kHz
"""

from scipy.signal import firwin

numtaps = 101     #number of coefficients ( filter length)
lowcut  = 80e3    #lower cut off frequency (80kHz)
highcut = 120e3   #Uppoer cut off frequency (120kHZ)
fs      = 2.4e6   #sample rate (2.4MHz)


taps = firwin (
    numtaps,
    [lowcut, highcut],
    pass_zero=False,
    fs=fs,
    window='hann')