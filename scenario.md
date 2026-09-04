[scenario.md](https://github.com/user-attachments/files/31845370/scenario.md)
# Scenario

**Organization:** CloudNative (fictional) — a cloud-native SaaS company
**Infrastructure:** Fully hosted on AWS. No owned or leased office premises.
**Workforce:** Fully remote.
**Development:** All software development performed in-house.
**Objective:** Build a complete ISO/IEC 27001:2022 Statement of Applicability (SoA)
ahead of a certification audit.

## The starting point

CloudNative already has an internal **Evidence Index** — 32 artifacts (policies,
standards, procedures, registers, records) that its security team produced over the
past year, each mapped to the Annex A controls it supports. What it does not have is
a formal SoA: the mandatory document that takes a position — Applicable or Not
Applicable, with justification — on all 93 Annex A controls, not just the ones
evidence already exists for.

That gap is the actual exercise: the Evidence Index tells you what's already been
*done*. It doesn't tell you what's been *decided*. An SoA requires a decision and a
justification for every one of the 93 controls, including the ones nobody has
gotten around to yet.

## What had to be figured out

Cross-referencing the Evidence Index against the full Annex A list showed 77
controls already covered by existing evidence. The remaining 16 had no artifact
behind them at all, and each needed an actual applicability decision:

- **Most Physical (A.7) controls** — CloudNative owns no physical premises. The
  question wasn't "do we have evidence for this," it was "does this control even
  apply to a company with no office, no data center, and no physical equipment of
  its own?" For most of them, the answer is no — and the justification has to say
  *why*, not just assert it (AWS carries physical security under the shared-
  responsibility model, referenced back to the supplier-management controls that
  already exist).
- **A.8.30 (Outsourced development)** — CloudNative doesn't currently outsource any
  development. Marking this Not Applicable is a real, defensible risk-based
  exclusion — the kind of call an SoA is actually supposed to contain — but it's
  also a call that needs revisiting the moment that fact changes.
- **The remaining gaps** (segregation of duties, contact with authorities, storage
  media, equipment maintenance, web filtering, environment separation, test data) —
  these are Applicable, but genuinely not yet fully implemented or documented. The
  honest move was to say so, with a specific note on what exists informally versus
  what's missing, rather than either hiding the gap or forcing a false "Yes,
  Implemented."

## What would happen next in a real engagement

Every row marked Partial/Gap becomes a line in a remediation tracker with an owner
and a target date. The Not Applicable rows get revisited at the next annual SoA
review, since applicability can change as the business does (e.g., if CloudNative
ever brings on an outsourced dev team, A.8.30 flips back to Applicable).
