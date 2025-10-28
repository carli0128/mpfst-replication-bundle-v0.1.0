import numpy as np
from scipy.signal import butter, filtfilt, hilbert

def octave_band_edges(fmin, fmax, n_bands):
    edges = [fmin*(2**i) for i in range(n_bands+1)]
    edges = [e for e in edges if e<=fmax*(1+1e-9)]
    return np.array(edges)

def band_envelope(x, fs, f_lo, f_hi, order=4):
    ny = fs/2
    f_lo = max(1e-6, min(f_lo, ny*0.99))
    f_hi = max(f_lo*1.01, min(f_hi, ny*0.999))
    b,a = butter(order, [f_lo/ny, f_hi/ny], btype="band")
    y = filtfilt(b,a,x)
    env = np.abs(hilbert(y))
    return env

def filterbank_energy(x, fs, edges):
    E = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        env = band_envelope(x, fs, lo, hi)
        E.append(env**2)
    return np.array(E)  # shape: (bands, time)
