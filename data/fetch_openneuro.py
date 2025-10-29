#!/usr/bin/env python
"""
Fetch an example EEG dataset for the notebooks.

Two provider modes:
  - physionet (default): Uses MNE to fetch the EEG Motor Movement/Imagery dataset
	(open access) and exports a single-channel CSV for quick testing.
  - openneuro: Downloads a specific file URL from OpenNeuro if provided.

Examples
--------
  # Fetch PhysioNet EEGMMI and export a Cz channel CSV
  python data/fetch_openneuro.py --provider physionet --channel Cz --export-csv

  # Download a specific OpenNeuro file by URL (small file recommended)
  python data/fetch_openneuro.py --provider openneuro \
	--url https://openneuro.org/crn/datasets/ds004283/snapshots/1.0.0/files/README

Notes
-----
This script keeps dependencies light. The PhysioNet mode requires MNE-Python.
If MNE is not installed, a helpful message is shown.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

import requests


def parse_args():
	p = argparse.ArgumentParser(description="Fetch EEG data (PhysioNet or OpenNeuro)")
	p.add_argument("--provider", choices=["physionet", "openneuro"], default="physionet")
	p.add_argument("--outdir", default="data/cache/eeg")
	p.add_argument("--channel", default="Cz", help="Channel to export if --export-csv")
	p.add_argument("--export-csv", action="store_true", help="Export selected channel to CSV")
	p.add_argument("--url", help="Direct file URL for provider=openneuro")
	return p.parse_args()


def fetch_physionet(outdir: str, channel: str, export_csv: bool):
	try:
		import mne
		from mne.datasets import eegbci
	except Exception as e:  # pragma: no cover
		print("MNE is required for --provider physionet. Install with: pip install mne", file=sys.stderr)
		raise SystemExit(1)

	os.makedirs(outdir, exist_ok=True)
	# Subject 1, runs [3,7,11] commonly used in examples
	files = eegbci.load_data(1, runs=[3, 7, 11])
	# Export a short CSV from the first file for convenience
	if export_csv and files:
		raw = mne.io.read_raw_edf(files[0], preload=True, verbose=False)
		if channel not in raw.ch_names:
			# fallback to first available if requested channel missing
			channel_to_use = next((ch for ch in [channel, "C3", "C4", "Fz", "Pz"] if ch in raw.ch_names), raw.ch_names[0])
		else:
			channel_to_use = channel
		raw.pick([channel_to_use])
		raw.resample(128.0)
		x = raw.get_data()[0]
		fs = raw.info["sfreq"]
		csv_path = os.path.join(outdir, f"physionet_subject1_{channel_to_use}_128Hz.csv")
		with open(csv_path, "w") as f:
			f.write("x\n")
			for xi in x:
				f.write(f"{xi}\n")
		meta_path = os.path.join(outdir, "README_physionet.txt")
		with open(meta_path, "w") as f:
			f.write("EEGMMI fetched via MNE; CSV contains channel {ch} resampled to 128 Hz.\n".format(ch=channel_to_use))
		print(f"Exported CSV: {csv_path} (fs={fs:.1f} Hz), metadata: {meta_path}")
	print("PhysioNet EEGMMI files are cached under ~/mne_data; see MNE output for paths.")


def fetch_openneuro_file(outdir: str, url: str):
	if not url:
		raise SystemExit("--url is required for provider=openneuro")
	os.makedirs(outdir, exist_ok=True)
	fname = Path(url).name.replace(":", "_")
	dest = os.path.join(outdir, fname)
	with requests.get(url, stream=True, timeout=60) as r:
		r.raise_for_status()
		with open(dest, "wb") as f:
			for chunk in r.iter_content(chunk_size=1024 * 128):
				if chunk:
					f.write(chunk)
	print(f"Downloaded: {dest}")


def main():
	args = parse_args()
	if args.provider == "physionet":
		fetch_physionet(args.outdir, args.channel, args.export_csv)
	else:
		fetch_openneuro_file(args.outdir, args.url)


if __name__ == "__main__":
	main()
