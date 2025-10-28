"""GW superradiance (VBK) evaluator for MPFST.
All quantities assumed in geometric units (G = c = 1).

This module implements a *specialization* of the MPFST linear-response gate
to the Kerr/Kerr–Newman case using the analytic conditions highlighted in the
VBK analysis: (i) quasibound condition μ > μ0 = q Q / M; (ii) superradiance
condition μ < ω_c = (m a + q Q r_+) / (r_+^2 + a^2).  In the astrophysical limit
Q≈0, these reduce to μ > 0 and μ < Ω_H, where Ω_H = a / (r_+^2 + a^2).

The functions below are lightweight and pure-python; they do not depend on
external packages. They are intended to *evaluate* MPFST's domain-agnostic
linear-response gate in the GR ringdown case without altering MPFST's core API.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass
class BHParams:
    M: float         # remnant mass (geometric units)
    a: float         # specific angular momentum (J/M), 0 <= a < M
    Q: float = 0.0   # charge (astrophysical: ~0)
    m: int = 1       # azimuthal number of the mode
    q: float = 0.0   # field charge (test value; often 0 or 1)
    mu: float = 0.0  # test field mass (Compton frequency)

def r_plus(params: BHParams) -> float:
    """Horizon radius r_+ = M + sqrt(M^2 - a^2 - Q^2)."""
    M,a,Q = params.M, params.a, params.Q
    disc = M*M - a*a - Q*Q
    if disc < 0:
        raise ValueError("Extremality violated: M^2 < a^2 + Q^2")
    return M + math.sqrt(disc)

def mu0(params: BHParams) -> float:
    """Quasibound threshold μ0 = q Q / M."""
    return (params.q * params.Q) / params.M if params.M!=0 else math.inf

def omega_c(params: BHParams) -> float:
    """Superradiant critical frequency ω_c = (m a + q Q r_+) / (r_+^2 + a^2)."""
    rp = r_plus(params)
    num = params.m * params.a + params.q * params.Q * rp
    den = rp*rp + params.a*params.a
    return num / den

def superradiance_overlap(params: BHParams) -> bool:
    """Return True iff μ > μ0 and μ < ω_c."""
    mu_val = params.mu
    return (mu_val > mu0(params)) and (mu_val < omega_c(params))

def imomega_quadratic_weight(params: BHParams, C: float = 1.0) -> float:
    """Quadratic-onset proxy near μ0: Im ω ∝ (μ - μ0)^2 inside overlap, else 0.
    This is a *weight* (not a calibrated growth rate)."""
    mu_val = params.mu
    mu0_val = mu0(params)
    if superradiance_overlap(params):
        d = mu_val - mu0_val
        return C * (d*d)
    return 0.0

# Simple convenience wrapper returning both gate and weight
def evaluate_gate_and_weight(params: BHParams, C: float = 1.0):
    return superradiance_overlap(params), imomega_quadratic_weight(params, C)

# CLI helper
def cli():
    import argparse, json
    ap = argparse.ArgumentParser(description="Evaluate VBK superradiance gate for given BH parameters.")
    ap.add_argument("--M", type=float, required=True)
    ap.add_argument("--a", type=float, required=True)
    ap.add_argument("--Q", type=float, default=0.0)
    ap.add_argument("--m", type=int, default=1)
    ap.add_argument("--q", type=float, default=0.0)
    ap.add_argument("--mu", type=float, required=True)
    ap.add_argument("--C", type=float, default=1.0)
    args = ap.parse_args()
    params = BHParams(M=args.M, a=args.a, Q=args.Q, m=args.m, q=args.q, mu=args.mu)
    gate, w = evaluate_gate_and_weight(params, C=args.C)
    print(json.dumps({"gate": gate, "weight": w, "omega_c": omega_c(params), "mu0": mu0(params)}))
