import numpy as np

def predict_tail_exponent(beta: float) -> float:
    """In the fractional-relaxation picture, the late-time envelope ~ t^{-p} with p≈β."""
    return float(beta)

def predict_group_delay_power(alpha: float) -> float:
    """For dispersion with fractional Laplacian order α, group delay ~ f^{α-2}."""
    return float(alpha-2.0)
