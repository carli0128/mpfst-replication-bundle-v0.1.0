We do not redistribute third-party datasets.

Use these helpers to fetch open-access data reproducibly (downloads are cached under `data/cache/`):

- `fetch_openneuro.py`  – EEG helper
	- Provider `physionet` (default): use MNE to fetch EEG Motor Movement/Imagery (EEGMMI) and optionally export a single-channel CSV.
		- Example: `python data/fetch_openneuro.py --provider physionet --channel Cz --export-csv`
	- Provider `openneuro`: download a specific file by URL.
		- Example: `python data/fetch_openneuro.py --provider openneuro --url https://openneuro.org/crn/datasets/ds004283/snapshots/1.0.0/files/README`

- `fetch_iris.py`       – Seismology (IRIS/USGS via ObsPy)
	- Example: `python data/fetch_iris.py --network IU --station ANMO --channel BHZ --start 2020-01-01T00:00:00 --duration 600 --csv`

- `fetch_gwosc.py`      – GW ringdowns (GWOSC event catalog JSON)
	- Example: `python data/fetch_gwosc.py --event GW150914 --catalog GWTC-1-confident`

Notes
-----
- Only `obspy` is required by default (see `requirements.txt`). `mne` is optional and only needed for the PhysioNet EEG helper.
- Large strain files from GWOSC are not downloaded by default; the script fetches compact JSON metadata.
