import numpy as np
from scipy.signal import welch
from numpy.typing import ArrayLike

def spectral_slope_gamma(x: ArrayLike, fs: float, fmin: float=0.5, fmax: float|None=None) -> float:
    """Estimate 1/f^γ slope via log–log fit of Welch PSD between fmin..fmax."""
    x = np.asarray(x, dtype=float)
    if fmax is None: fmax = fs/2*0.95
    f, Pxx = welch(x, fs=fs, nperseg=min(4096, max(256, int(fs*2))))
    m = (f>=fmin) & (f<=fmax) & (Pxx>0)
    F = np.log10(f[m]); S = np.log10(Pxx[m])
    A = np.vstack([np.ones_like(F), -F]).T  # P ~ f^{-γ} => logP = c - γ log f
    coef, *_ = np.linalg.lstsq(A, S, rcond=None)
    gamma = coef[1]
    return float(gamma)

def hurst_dfa(x: ArrayLike, min_scale: int=8, max_scale: int=512, num_scales: int=12) -> float:
    """Simple DFA (order-1) estimate of Hurst exponent."""
    x = np.asarray(x, dtype=float)
    y = np.cumsum(x - np.mean(x))
    scales = np.unique(np.logspace(np.log10(min_scale), np.log10(max_scale), num_scales).astype(int))
    F = []
    for s in scales:
        if s<4 or s>=len(y): continue
        nseg = len(y)//s
        z = y[:nseg*s].reshape(nseg, s)
        t = np.arange(s)
        # detrend each segment
        res = []
        for seg in z:
            A = np.vstack([np.ones_like(t), t]).T
            coef, *_ = np.linalg.lstsq(A, seg, rcond=None)
            res.append(seg - (coef[0]+coef[1]*t))
        res = np.concatenate(res)
        F.append(np.sqrt(np.mean(res**2)))
    F = np.array(F); S = scales[:len(F)]
    A = np.vstack([np.ones_like(np.log10(S)), np.log10(S)]).T
    coef, *_ = np.linalg.lstsq(A, np.log10(F), rcond=None)
    H = coef[1]
    return float(H)

def heavy_tail_mu_hill(x: ArrayLike, q: float=0.95) -> float:
    """Hill estimator on absolute increments; returns tail index μ (Pareto-like)."""
    x = np.asarray(x, dtype=float)
    dx = np.diff(x)
    a = np.abs(dx)
    a = a[a>0]
    if len(a)<10: return float("nan")
    k = max(5, int(len(a)*(1-q)))
    a_sorted = np.sort(a)[::-1]
    top = a_sorted[:k]
    xmin = a_sorted[k] if k<len(a_sorted) else a_sorted[-1]
    if np.any(top<=0) or xmin<=0: return float("nan")
    hill = 1.0 / (np.mean(np.log(top/xmin)) + 1e-12)
    # map Hill alpha→ μ; here we use μ≈alpha (tail exponent), consistent for Pareto tails
    return float(hill)
