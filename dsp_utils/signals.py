import numpy as np

def generate_tone(f_tone = 100e3, fs = 2.4e6, N = 2048, snr_db = 20):
    """
    Generate complex exponential tone with additive white gaussian noise

    Params
    ---------
    f_tone : float
        Tone frequency in Hz
    fs : float
        Sampling rate in Hz
    N : int
        Number of samples
    snr_db : float
        Desired signal - to - noise ratio in db

    Returns
    ------
    Signal : np.ndarray
        clean tone signal
    noiy_signal: np.ndarray
        tone wiht AWGN applied

    """

    t  = np.arange (N) / fs
    signal = np.exp(2j * np.pi *f_tone * t)

    #compute noise power from desired snr
    signal_power = np.mean(np.abs(signal)**2)
    noise_power = signal_power / (10**(snr_db / 10))
    noise = np.sqrt(noise_power/2) * (np.random.randn(N) + 1j*np.random.randn(N))


    return signal, signal + noise

