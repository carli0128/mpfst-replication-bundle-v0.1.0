import numpy as np
from scipy.stats import gaussian_kde

def dip_proxy_kde(x, bw='scott', grid=1024):
    """Crude bimodality proxy: count local maxima of KDE."""
    x = np.asarray(x, dtype=float)
    if len(np.unique(x))<5: return {"n_peaks": 0}
    kde = gaussian_kde(x, bw_method=bw)
    t = np.linspace(x.min(), x.max(), grid)
    y = kde(t)
    # count peaks
    peaks = np.where((y[1:-1]>y[:-2]) & (y[1:-1]>y[2:]))[0]
    return {"n_peaks": int(len(peaks))}
