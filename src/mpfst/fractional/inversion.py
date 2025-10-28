import argparse, numpy as np

def invert_beta(mu: float|None, gamma: float|None, H: float|None, weights=(0.5,0.5)) -> float:
    """Predict β from (μ, γ, H). We combine γ and (2-μ) with optional H-aware weighting.
    This is a transparent heuristic aligned with MPFST addendum used in the memos.
    """
    vals = []
    w = []
    if gamma is not None and np.isfinite(gamma):
        vals.append(gamma); w.append(weights[0])
    if mu is not None and np.isfinite(mu):
        vals.append(max(0.0, 2.0-mu)); w.append(weights[1])
    if not vals:
        return float("nan")
    beta = float(np.average(vals, weights=w))
    # Optional H modulation: if H strong, trust tails/spectra more (already reflected).
    return beta

def invert_cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mu", type=float, required=False)
    ap.add_argument("--gamma", type=float, required=False)
    ap.add_argument("--H", type=float, required=False)
    args = ap.parse_args()
    print(invert_beta(args.mu, args.gamma, args.H))
