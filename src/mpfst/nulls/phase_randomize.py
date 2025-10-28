import numpy as np

def phase_randomize(x: np.ndarray, seed: int|None=None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    X = np.fft.rfft(x)
    phases = rng.uniform(0, 2*np.pi, size=X.shape)
    phases[0] = 0.0
    if X.shape[0]>1 and (len(x)%2==0):
        phases[-1] = 0.0
    Y = np.abs(X) * np.exp(1j*phases)
    y = np.fft.irfft(Y, n=len(x))
    return np.asarray(y, dtype=float)
