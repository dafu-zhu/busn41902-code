# busn41902-code

Python companion code and worked demos for **BUSN 41902: Statistical Inference I** (Booth PhD core econometrics).

This repo is the implementation companion to the LaTeX lecture notes that live at
[good-student-note](https://github.com/dafu-zhu/good-student-note) under `notes/busn41902/`.
The notes derive the math; this repo shows the math becoming computation.

**Live docs site:** https://dafu-zhu.github.io/busn41902-code/

## Install (local)

Requires Python ≥ 3.11 and [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/dafu-zhu/busn41902-code.git
cd busn41902-code
uv sync --all-extras
```

## Run a demo

```bash
uv run python L1/demo_ak_mean.py    # generates L1/figures/*.pdf
```

## Render the docs site locally

```bash
uv run quarto preview
```

Opens a local server at http://localhost:4444 with hot-reload.

## Algorithm fidelity

All algorithms are implemented from numpy/scipy primitives, mirroring the lecturer's MATLAB. We do **not** delegate the taught algorithm to a higher-level library (statsmodels, sklearn). See `INCONSISTENCIES.md` for any discrepancies surfaced during the port.
