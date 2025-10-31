from scipy.signal import butter, sosfilt, firwin, lfilter,sosfreqz
import numpy as np

def apply_bandpass(signal, fs, lowcut, highcut, order = 4, method = 'iir'):
    """
    Apply FIR or IIR bandpass filter to a signal
    """
    if method.lower() == 'iir':
        sos = butter(order, [lowcut, highcut], btype='bandpass', fs=fs, output='sos')
        return sosfilt(sos, signal)
    elif method.lower() == 'fir':
        numtaps = 128
        taps = firwin(numtaps, [lowcut, highcut], pass_zero=False, fs=fs)
        return lfilter(taps, 1.0, signal)
    else:
        raise ValueError("Must be 'iir' or 'fir'")

def get_filter_response(fs, lowcut, highcut, order=4, method='iir'):
    """
    Return frequency and magnitude response for plotting
    """
    if method.lower() == 'iir':
        sos = butter(order, [lowcut, highcut], btype='bandpass', fs=fs, output='sos')
        w, h = sosfreqz(sos, fs=fs)
    else:
        numtaps = 128
        taps = firwin(numtaps, [lowcut, highcut], pass_zero=False, fs=fs)
        w, h = np.fft.fftfreq(len(taps), 1/fs), np.fft.fft(taps)
    return w, 20*np.log10(np.abs(h) + 1e-12)