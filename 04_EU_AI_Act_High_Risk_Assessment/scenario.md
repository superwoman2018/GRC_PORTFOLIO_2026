[scenario.md](https://github.com/user-attachments/files/31867784/scenario.md)
# Scenario

**Organization:** CloudNative (fictional) — same company as Projects 02, 04, 05.
**Objective:** Classify CloudNative's AI systems under the EU AI Act's risk
tiers, and work through one classification — a resume-screening feature — in
full, since it's the one with real legal consequences attached.

## Why an inventory first

The EU AI Act doesn't regulate a company — it regulates individual AI systems,
each classified on its own. So the first real step isn't assessing one system
in depth; it's listing every AI system in use and sorting them by tier, so
nothing gets missed and effort goes where the actual risk is. CloudNative has
four: two customer-facing product features, one internal security tool, and
one AI capability embedded in a vendor's product.

## The classification that actually matters: TalentMatch AI

TalentMatch AI — the resume-ranking feature in CloudNative's HR module — is a
clean match for Annex III(4)(a), the EU AI Act's explicit high-risk category
for recruitment and candidate-selection AI. This one wasn't a hard call to
classify; it's a hard problem to *remediate*, since it comes with a full
obligation set (risk management, bias testing, human oversight, EU database
registration) that a feature built without those requirements in mind wasn't
designed to meet. The full assessment walks through why it qualifies and what
closing the gap actually requires.

## The classification that took more judgment: what ISN'T high-risk

The more interesting test of "translating regulation to operational reality"
isn't spotting the obvious high-risk system — it's correctly clearing the ones
that look like they might be but aren't:

- **SupportBot** (the customer support chatbot) is the system most people would
  guess wrong on. It's AI-powered and customer-facing, which makes it feel like
  it should carry more obligations than it does. But it doesn't make or
  influence a decision about employment, credit, essential services, or any
  other Annex III category — it answers support questions. It only triggers
  Article 50's transparency requirement (tell users they're talking to AI),
  nothing more. Over-classifying this as high-risk would waste compliance
  effort on a system that doesn't need it.
- **Account Anomaly Detection Engine** is the harder judgment call in the other
  direction. It affects real people (flagging accounts for review), but a human
  security analyst makes every actual decision — the model surfaces a signal,
  it doesn't act. That keeps it out of Annex III today. The register explicitly
  notes this needs re-assessment if the design ever changes to auto-suspend
  accounts without human review — the classification is tied to *how the
  system is used*, not just what it technically could do.

## What this doesn't cover

This is a classification exercise, not a legal opinion — the actual assessment
document says so explicitly. A real deployment would need a qualified legal
review before relying on this classification in front of a regulator or a
client, and the AI Act's compliance deadlines are staggered and worth
reconfirming against the current schedule at the time any of this is acted on.
