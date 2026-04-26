# Inconsistencies — BUSN 41902 code vs. lecture notes

Audit log of discrepancies discovered during the MATLAB → Python port.
See the design spec at
`good-student-note:docs/superpowers/specs/2026-04-25-busn41902-code-integration-design.md`
§7 for the full schema and resolution workflow.

## Severity tags

- `cosmetic` — variable names, formatting, no numeric impact.
- `numeric` — changes computed values.
- `pedagogical` — conceptual mismatch between code and lecture's exposition.
- `blocking` — actively wrong (in code or lecture).

## Status legend

- `open` — discovered, awaiting decision.
- `decided` — user has chosen a resolution.
- `resolved` — fix applied to the offender (notes or code).

## Entry template

Use the following block for each new entry. Replace `INC-NNN` with a
running 3-digit counter (INC-001, INC-002, …):

```markdown
## INC-NNN: <one-line title>

- **Lecture**: `lecNN.tex` §X.Y, eq. (N.NN)
- **MATLAB source**: `inputs/busn41902/code/L?/...m:LINE`
- **Existing port** (if any): `inputs/busn41902/code/L?/...py:LINE`
- **Severity**: cosmetic | numeric | pedagogical | blocking
- **Description**: <what the mismatch is and why it matters>
- **Proposed resolutions**:
  - (a) <option>
  - (b) <option>
- **Status**: open
- **Resolution**: _(filled in after decision)_
```

## Entries

## INC-001: `solve` vs. `inv` for OLS normal equations

- **Lecture**: `lec01.tex` §3 (Slide L1.15) — `(X'X)^{-1}(X'Y)`
- **MATLAB source**: `inputs/busn41902/code/L1/AKMeanExample.m:18, :25, :33` — `inv(X'*X)*(X'*y)`
- **Existing port**: `inputs/busn41902/code/L1/lecture1.ipynb` cell 3 — `np.linalg.inv(X.T @ X) @ (X.T @ y)`
- **Severity**: cosmetic
- **Description**: Computing the explicit inverse is numerically less stable than solving the normal equations directly via LU factorization, and ~2× slower. The Python port standardizes on `np.linalg.solve(X.T @ X, X.T @ y)` everywhere (`busn41902.regression.ols` and the inline solver in `demo_conditional_mean.py`).
- **Resolution**: Standardize on `solve`; logged once for the first occurrence (in `demo_conditional_mean.py`, then reaffirmed in `busn41902.regression.ols`'s docstring). The textbook expression $\beta = (X'X)^{-1}X'Y$ remains the *mathematical* statement; the implementation chooses a different numerical realization.
- **Status**: resolved

## INC-002: Spline basis truncation direction

- **Lecture**: `lec01.tex` §3 (Slide L1.13 answer 3) — basis form not specified explicitly
- **MATLAB source**: `inputs/busn41902/code/L1/AKMeanExample.m:32` — `((d-12).*(d<=12)).^3` and `((d-16).*(d<=16)).^3`
- **Existing port**: `inputs/busn41902/code/L1/lecture1.ipynb` cell 3 — same as MATLAB
- **Severity**: cosmetic
- **Description**: The MATLAB basis truncates *below* the knot (non-zero for $d \le k$). The standard textbook truncated-power basis $(d-k)_+^3$ truncates *above* the knot (non-zero for $d > k$). Both span the same $C^2$ cubic-spline space with breakpoints at $\{12, 16\}$ — fitted curve identical, coefficients differ.
- **Resolution**: Keep MATLAB form so β-by-β comparison against the MATLAB reference is exact in the verification test. `demo_spline.py` §2 walkthrough explains the parametrization choice and shows that both forms yield the same fit.
- **Status**: resolved
