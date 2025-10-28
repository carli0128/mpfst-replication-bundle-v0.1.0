#!/usr/bin/env python
import argparse, pandas as pd
from mpfst.coherence.metrics import spectral_slope_gamma, hurst_dfa, heavy_tail_mu_hill
from mpfst.coherence.meter import compute_m_l

ap = argparse.ArgumentParser()
ap.add_argument("--csv", required=True, help="CSV with column x and fs header value")
ap.add_argument("--fs", type=float, required=True)
args = ap.parse_args()

df = pd.read_csv(args.csv)
x = df['x'].values
mu = heavy_tail_mu_hill(x)
gamma = spectral_slope_gamma(x, fs=args.fs)
H = hurst_dfa(x)
m_l = compute_m_l(mu, gamma, H)
print(f"mu={mu:.3f}, gamma={gamma:.3f}, H={H:.3f}, m_l={m_l:.3f}")
