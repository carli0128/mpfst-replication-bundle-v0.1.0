import numpy as np
from mpfst.spectral.utils import octave_band_edges, filterbank_energy
from mpfst.spectral.ssm import dominant_shell_indices, detect_shell_jumps

def test_ssm_detects_jump():
    fs = 1000.0
    t = np.arange(0, 2.0, 1/fs)
    # 20 Hz for first second, 40 Hz for second second => ~+1 octave
    x = np.sin(2*np.pi*20*t*(t<1.0)) + np.sin(2*np.pi*40*t*(t>=1.0))
    edges = octave_band_edges(8, 128, 5)
    E = filterbank_energy(x, fs, edges)
    dom = dominant_shell_indices(E, energy_min=np.percentile(E, 80))
    jumps = detect_shell_jumps(dom, edges, min_gap=10)
    assert any(abs(d[-1]-1.0)<0.2 for d in jumps), f"No octave jump found: {jumps}"
