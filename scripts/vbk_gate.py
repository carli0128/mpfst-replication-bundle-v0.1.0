#!/usr/bin/env python
import argparse, json
from mpfst.gating.linear_response import evaluate

ap = argparse.ArgumentParser(description='Evaluate VBK gate (GW) for MPFST.')
ap.add_argument('--M', type=float, required=True)
ap.add_argument('--a', type=float, required=True)
ap.add_argument('--Q', type=float, default=0.0)
ap.add_argument('--m', type=int, default=1)
ap.add_argument('--q', type=float, default=0.0)
ap.add_argument('--mu', type=float, required=True)
ap.add_argument('--C', type=float, default=1.0)
args = ap.parse_args()

gate, w = evaluate('gw_vbk', M=args.M, a=args.a, Q=args.Q, m=args.m, q=args.q, mu=args.mu, C=args.C)
print(json.dumps({'gate': gate, 'weight': w}))
