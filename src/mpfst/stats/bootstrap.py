import numpy as np

def ci_mean(x, alpha=0.05, n_boot=2000, seed=None):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    bs = [rng.choice(x, size=len(x), replace=True).mean() for _ in range(n_boot)]
    lo, hi = np.quantile(bs, [alpha/2, 1-alpha/2])
    return float(lo), float(hi)
