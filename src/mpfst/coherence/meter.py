import numpy as np

def compute_m_l(mu: float|None, gamma: float|None, H: float|None,
                weights=(0.33,0.33,0.34)) -> float:
    """Combine (μ, γ, H) into a coherence meter mℓ ∈ [0,1].
    Heavier tails (smaller μ), steeper spectra (larger γ), and stronger memory (H>0.5)
    increase mℓ. Thresholds: m1≈0.33, m2≈0.66.
    """
    w1,w2,w3 = weights
    terms = []
    if mu is not None and np.isfinite(mu):
        # normalize: μ∈[1,3+] → score in [0,1]
        t = np.clip((2.0 - (mu-1.0)) / 2.0, 0, 1)  # heuristic
        terms.append(w1*t)
    if gamma is not None and np.isfinite(gamma):
        t = np.clip(gamma/2.0, 0, 1)  # 0..2 mapped to 0..1
        terms.append(w2*t)
    if H is not None and np.isfinite(H):
        t = np.clip((H-0.5)/0.5, 0, 1)
        terms.append(w3*t)
    score = sum(terms) / (w1+w2+w3)
    return float(np.clip(score, 0, 1))
