# GRC Portfolio 2026 — Judgment Under Real Constraints

## Why I built this

Most GRC portfolios show the same thing: a control mapping, a policy template,
a list of frameworks someone has "worked with." That proves familiarity with
vocabulary. It doesn't prove someone can do the job.

The actual work of GRC isn't knowing what ISO 27001 or PCI DSS says — it's
deciding how a specific organization, with specific limitations and specific
business pressure, should respond to what the standard asks for. That means
making a call, writing down why, and being ready to defend it when someone
pushes back.

This repository is five scenarios where I did exactly that: took a
realistic constraint, made a documented decision, and wrote down the
reasoning — including where that reasoning has limits.

## What I'm optimizing for

| | Just doing the task | Showing judgment |
|---|---|---|
| **Looks like** | A control mapped to a requirement | A decision on how to meet (or not meet) that requirement, and why |
| **Explains** | *What* the framework says | *Why* it matters here, and when it wouldn't |
| **Survives** | A checklist review | A follow-up question from someone who disagrees |

Anyone can produce the left column with a template. The right column is
the actual skill.

## Projects

| # | Project | Framework / Domain | What it's testing |
|---|---|---|---|
| 01 | PCI DSS Network Segmentation Review | PCI DSS | Whether a segmentation claim would hold up under an assessor's questions |
| 02 | ISO 27001 Statement of Applicability | ISO 27001 | Justifying control exclusions with a real risk rationale, not a shortcut |
| 03 | EU AI Act High-Risk Assessment | EU AI Act | Turning a regulation's wording into an actual operational classification |
| 04 | GRC Control Automation | GRC Engineering | Where automation genuinely reduces manual compliance effort, and where it can't |
| 05 | Risk Acceptance Documentation | Enterprise Risk | Writing a risk decision a business leader — not a security person — would actually understand |

Each folder contains the scenario I worked from, the deliverable I produced,
and a short write-up of the trade-offs and assumptions behind it.

## How to use this

```
git clone https://github.com/YOUR-USERNAME/grc-portfolio-2026.git
cd grc-portfolio-2026/01-pci-dss-network-segmentation
```

Each project folder has its own README with the scenario and the finished
deliverable. Start with whichever domain is closest to the roles you're
targeting.

## Disclaimer

Every project in this repository is built for a single fictional company
(CloudNative) as a portfolio exercise — none of this reflects a real client
engagement, and none of it is legal, audit, or compliance advice. Framework
citations, control numbers, and regulatory obligations are represented as
accurately as I could make them, but should be verified against the current
official standard or regulation before being relied on for a real decision.

## About me

Maimoona Iqbal — GRC professional, CISA certified. Connect on
[LinkedIn](https://www.linkedin.com/in/maimoonaiqbal/) · More write-ups on
[Medium](https://medium.com/@maimoona2018).
