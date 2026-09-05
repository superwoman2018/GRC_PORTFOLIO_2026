[README 05.md](https://github.com/user-attachments/files/31868263/README.05.md)
# 01 — PCI DSS Network Segmentation Review

**Framework:** PCI DSS
**Core skill demonstrated:** Defending risk claims under audit scrutiny — not
just documenting segmentation, but being ready for the assessor's follow-up
question.

## What's in this folder

| File | What it is |
|---|---|
| `scenario.md` | The scope call that mattered, and why the SEG-07 finding is treated as a real finding, not explained away |
| `deliverables/CloudNative_PCI_Segmentation_Test_Results.xlsx` | 7 segmentation tests between network zones, including one genuine finding |
| `deliverables/CloudNative_PCI_Segmentation_Review.docx` | Full report — cardholder data flow, scope determination, test summary, and a dedicated section anticipating and answering the hardest assessor questions |

## How to read this

Start with the report's Section 3 (Scope Determination) to see the actual
judgment call — why Support Tooling isn't in the CDE despite touching the
payment flow. Then read Section 5 (Anticipating Assessor Questions) closely;
that section is the actual point of this project, more than the segmentation
diagram itself. The test results spreadsheet backs up every claim in the
report with a specific, individually tested network path — including the one
that failed.

## Disclaimer

This is a portfolio exercise for a fictional company, not a real PCI DSS
assessment. It does not replace a Qualified Security Assessor's formal
validation, and specific PCI DSS requirements should be verified against the
current official standard before being relied on for a real compliance
decision.
