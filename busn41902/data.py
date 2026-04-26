"""Dataset loaders for BUSN 41902 demos."""

from pathlib import Path

import numpy as np
from scipy.io import loadmat

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_big2() -> tuple[np.ndarray, np.ndarray]:
    """Load the AK census wage/education dataset.

    The .mat file stores ``y`` (log-wage) and ``d`` (years of education)
    as sparse matrices. We extract them via ``.toarray().flatten()`` and
    drop observations with ``d < 0`` (matching the lecturer's MATLAB
    preprocessing in ``AKMeanExample.m``).

    Returns
    -------
    y : ndarray, shape (n,)
        Log-wage.
    d : ndarray, shape (n,)
        Years of education (integer-valued, ``>= 0``).

    Notes
    -----
    MATLAB origin: ``load big2; I = find(d >= 0); y = y(I,:); d = d(I,:);``
    """
    raw = loadmat(_DATA_DIR / "big2.mat")
    y = np.asarray(raw["y"].toarray()).flatten()
    d = np.asarray(raw["d"].toarray()).flatten()
    mask = d >= 0
    return y[mask], d[mask]
