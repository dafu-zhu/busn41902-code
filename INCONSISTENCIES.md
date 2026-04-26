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

*(none yet — populated during lecture porting phases)*
