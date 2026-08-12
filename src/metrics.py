import numpy as np

def transparency_index(ec, fc, dt):
    """TI = (EC + FC + DT) / 3.

    EC, FC, and DT must be supplied on the same scale as the desired TI.
    For the manuscript's TI (0-10), pass EC, FC, and DT on a 0-10 scale.
    """
    return float(np.mean([ec, fc, dt]))

def decision_traceability_score(tp, td):
    if td <= 0:
        raise ValueError("TD must be > 0")
    return float(tp / td)

def ambiguity_reduction(ab, ax):
    if ab <= 0:
        raise ValueError("A_b must be > 0")
    return float((ab - ax) / ab * 100.0)

def computational_overhead_ms(tx, tb):
    return float(tx - tb)

def computational_overhead_pct(tx, tb):
    if tb <= 0:
        raise ValueError("T_b must be > 0")
    return float((tx - tb) / tb * 100.0)
