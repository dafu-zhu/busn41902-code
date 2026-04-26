# Datasets

Raw data files used by the demos, copied from the lecturer's MATLAB
materials. Committed to git for reproducibility.

| File | Size | Used in | Description |
|------|-----:|---------|-------------|
| `big2.mat` | 21 MB | L1, L3 | (TBD — populate during L1 port) |
| `mishkin.txt` | 24 KB | L3 | Mishkin (1981) real interest rate series — used by `MishkinExample.m` |
| `MROZ.xlsx` | 104 KB | L6 | Mroz (1987) female labor supply — used by `MrozExample.m` and `ml_probit_LARGE.m` |
| `pricing.dat` | 45 KB | L6 | (TBD — populate during L6 port) |

`big2.mat` is the only large file; if its size becomes a clone-time concern,
consider converting to a compressed `.npz` (numpy native) during the L1 port,
or moving to Git LFS. Total uncompressed: ~21 MB.

Original MATLAB sources live under
`good-student-note:inputs/busn41902/code/L?/` — they are NOT mirrored here
(this repo is Python-only by design).
