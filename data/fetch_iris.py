#!/usr/bin/env python
"""
Fetch a short seismic waveform from IRIS FDSN and cache it locally.

Examples
--------
  # 10 minutes of IU.ANMO.BHZ starting at 2020-01-01T00:00:00
  python data/fetch_iris.py --network IU --station ANMO --channel BHZ \
	--start 2020-01-01T00:00:00 --duration 600

Outputs
-------
  - MiniSEED file under data/cache/iris/
  - Optional CSV with two columns: t,x (time seconds, displacement)

Notes
-----
Requires obspy (listed in requirements.txt). Network access is needed on first run.
"""

import argparse
import os
from datetime import datetime, timedelta

import numpy as np

try:
	from obspy.clients.fdsn import Client
	from obspy import UTCDateTime
except Exception as e:  # pragma: no cover - helpful error for users
	raise SystemExit(
		"This script requires ObsPy. Install with: python -m pip install obspy"
	) from e


def parse_args():
	p = argparse.ArgumentParser(description="Fetch seismic waveform from IRIS FDSN")
	p.add_argument("--network", default="IU")
	p.add_argument("--station", default="ANMO")
	p.add_argument("--location", default="*")
	p.add_argument("--channel", default="BHZ")
	p.add_argument("--start", default="2020-01-01T00:00:00",
				   help="ISO start time UTC, e.g., 2020-01-01T00:00:00")
	p.add_argument("--duration", type=int, default=600, help="Seconds to fetch")
	p.add_argument("--outdir", default="data/cache/iris", help="Output directory")
	p.add_argument("--csv", action="store_true", help="Also write CSV t,x")
	return p.parse_args()


def main():
	args = parse_args()
	os.makedirs(args.outdir, exist_ok=True)

	client = Client("IRIS")
	t0 = UTCDateTime(args.start)
	t1 = t0 + float(args.duration)
	st = client.get_waveforms(args.network, args.station, args.location, args.channel, t0, t1)
	st.merge(method=1, fill_value="interpolate")
	tr = st[0]

	# Build filenames
	start_str = datetime.utcfromtimestamp(float(tr.stats.starttime)).isoformat(timespec="seconds")
	base = f"{args.network}.{args.station}.{args.location}.{args.channel}__{start_str}__{args.duration}s"
	mseed_path = os.path.join(args.outdir, base + ".mseed")
	st.write(mseed_path, format="MSEED")

	print(f"Saved MiniSEED: {mseed_path}")

	if args.csv:
		fs = float(tr.stats.sampling_rate)
		x = tr.data.astype(float)
		t = np.arange(len(x)) / fs
		csv_path = os.path.join(args.outdir, base + ".csv")
		# Write with header
		with open(csv_path, "w") as f:
			f.write("t,x\n")
			for ti, xi in zip(t, x):
				f.write(f"{ti},{xi}\n")
		print(f"Saved CSV: {csv_path} (fs={fs} Hz)")


if __name__ == "__main__":
	main()
