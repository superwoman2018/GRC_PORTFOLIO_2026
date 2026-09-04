# 02 — ISO 27001 Statement of Applicability

**Framework:** ISO/IEC 27001:2022, Annex A (93 controls)
**Core skill demonstrated:** Risk-driven control exclusions — deciding, and
justifying, which controls do and don't apply.

## What's in this folder

| File | What it is |
|---|---|
| `scenario.md` | The situation this project starts from, and what had to be figured out |
| `deliverables/CloudNative_ISO27001_Evidence_Index.xlsx` | The starting point — 32 existing artifacts mapped to the controls they support |
| `deliverables/CloudNative_ISO27001_SoA.xlsx` | The finished Statement of Applicability — all 93 controls, Applicable Yes/No, justification, evidence reference, and implementation status |

## How to read the SoA file

- **77 controls** are marked Applicable = Yes, Implemented, referencing the
  specific evidence artifact (EV-XXX) that supports them.
- **16 controls** had no existing evidence and required an individual applicability
  decision — these are the rows worth reading closely, since the reasoning behind
  each Yes/No *is* the SoA. See `scenario.md` for the walkthrough of that reasoning.
- The **Summary** tab auto-totals applicability and implementation status across all
  93 rows.

## What I'd flag if this were a real audit

An assessor would likely push hardest on the Not Applicable physical controls and
on A.8.30 — those are the rows where "we don't have evidence" could be mistaken for
"we didn't think about it," when the actual position is a considered exclusion.
Being able to explain *why* each exclusion holds, not just that it's marked No, is
the point of this exercise.
