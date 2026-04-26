"""busn41902: Python companion code for BUSN 41902 Statistical Inference I.

Modules will be added per-lecture during the porting phases:
    busn41902.acf       — autocorrelation utilities (L2)
    busn41902.hac       — heteroskedasticity- and autocorrelation-consistent SEs (L2/L3)
    busn41902.gmm       — generalized method of moments (L5)
    busn41902.ml        — maximum likelihood (L6)
    busn41902.bootstrap — bootstrap (L8)
    busn41902.data      — dataset loaders
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("busn41902")
except PackageNotFoundError:
    __version__ = "unknown"
