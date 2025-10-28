"""MPFST linear-response gate wrappers.

The *principle* is unified: a mode activates when coherence clears the gate
(mℓ > m1) AND the linear-response operator admits a localized growing solution.
This module provides a tiny adapter for the GW ringdown case via the VBK
evaluator (gw_superradiance). Other domains can register their own adapters.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, Any, Tuple

# Registry pattern so we don't hard-wire domains
_REGISTRY: Dict[str, Callable[..., Tuple[bool, float]]] = {}

def register(domain: str, fn: Callable[..., Tuple[bool, float]]):
    _REGISTRY[domain] = fn

def evaluate(domain: str, **kwargs) -> Tuple[bool, float]:
    if domain not in _REGISTRY:
        raise KeyError(f"No linear-response evaluator registered for domain '{domain}'")
    return _REGISTRY[domain](**kwargs)

# --- GW VBK specialization ---
def _gw_vbk_adapter(**kwargs):
    from mpfst.domains.gw_superradiance import BHParams, evaluate_gate_and_weight
    # kwargs expected: M, a, Q, m, q, mu, C (optional)
    p = BHParams(M=kwargs.get('M'), a=kwargs.get('a'),
                 Q=kwargs.get('Q', 0.0), m=kwargs.get('m', 1),
                 q=kwargs.get('q', 0.0), mu=kwargs.get('mu', 0.0))
    C = kwargs.get('C', 1.0)
    return evaluate_gate_and_weight(p, C=C)

register('gw_vbk', _gw_vbk_adapter)

# Simple CLI for scripting
def gw_vbk_cli():
    import argparse, json
    ap = argparse.ArgumentParser(description="Linear-response gate (GW VBK specialization)")
    ap.add_argument("--M", type=float, required=True)
    ap.add_argument("--a", type=float, required=True)
    ap.add_argument("--Q", type=float, default=0.0)
    ap.add_argument("--m", type=int, default=1)
    ap.add_argument("--q", type=float, default=0.0)
    ap.add_argument("--mu", type=float, required=True)
    ap.add_argument("--C", type=float, default=1.0)
    args = ap.parse_args()
    gate, weight = evaluate('gw_vbk', M=args.M, a=args.a, Q=args.Q, m=args.m, q=args.q, mu=args.mu, C=args.C)
    print(json.dumps({"gate": gate, "weight": weight}))
