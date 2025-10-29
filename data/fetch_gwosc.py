#!/usr/bin/env python
"""
Fetch small, open-access artifacts from GWOSC (LIGO/Virgo/KAGRA Open Science Center).

By default this pulls the compact JSON event catalog entry instead of large strain files.
You can choose an event (e.g., GW150914) and a catalog (e.g., GWTC-1-confident).

Examples
--------
  # Fetch the GW150914 JSON entry from GWTC-1-confident
  python data/fetch_gwosc.py --event GW150914 --catalog GWTC-1-confident

  # Fetch the entire catalog JSON
  python data/fetch_gwosc.py --catalog GWTC-1-confident --all

Outputs
-------
  - JSON saved to data/cache/gwosc/
"""

import argparse
import os
from pathlib import Path

import requests


BASE = "https://www.gw-openscience.org/eventapi/json"


def parse_args():
	p = argparse.ArgumentParser(description="Fetch GWOSC event catalog JSON")
	p.add_argument("--catalog", default="GWTC-1-confident")
	p.add_argument("--event", default="GW150914")
	p.add_argument("--all", action="store_true", help="Fetch entire catalog JSON instead of single event")
	p.add_argument("--outdir", default="data/cache/gwosc")
	return p.parse_args()


def main():
	args = parse_args()
	os.makedirs(args.outdir, exist_ok=True)
	if args.all:
		url = f"{BASE}/{args.catalog}"
		fname = Path(args.outdir) / f"{args.catalog}.json"
	else:
		url = f"{BASE}/{args.catalog}/{args.event}"
		fname = Path(args.outdir) / f"{args.catalog}_{args.event}.json"

	r = requests.get(url, timeout=60)
	r.raise_for_status()
	with open(fname, "wb") as f:
		f.write(r.content)
	print(f"Downloaded: {fname}")


if __name__ == "__main__":
	main()
