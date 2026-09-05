[scenario.md](https://github.com/user-attachments/files/31868268/scenario.md)
# Scenario

**Organization:** CloudNative (fictional) — same company as Projects 02, 03, 04, 05.
**Objective:** Confirm that CloudNative's network segmentation actually reduces
PCI DSS scope the way the architecture diagram claims — and be ready to defend
that claim when an assessor pushes on it.

## Why this is a "defend it" project, not a "document it" project

Anyone can draw a network diagram with a box labeled "Cardholder Data
Environment" and arrows showing what's supposedly isolated from it. A
Qualified Security Assessor doesn't accept the diagram — they test whether the
isolation actually holds, and then they ask the person defending it *how they
know*. That's the actual skill this project is built around: not producing
the diagram, but being ready for the follow-up question after it.

## The clean part of the scope call

CloudNative uses Stripe for all card capture — customers enter card details
into a Stripe-hosted iframe that CloudNative's own code never has access to.
That means no system CloudNative operates ever touches a full card number,
which is most of the scope-reduction argument. This part isn't controversial;
it's a well-established pattern (SAQ A-eligible integrations work this way by
design).

## The part that actually needed judgment

The harder call is **Support Tooling** — the internal system that receives
Stripe's webhook notifications, which include the last 4 digits of the card
and a billing status, but never the full number. Two wrong answers were
available here: treating it as fully in-scope (wasting compliance effort on
truncated data that PCI DSS doesn't require CDE-level protection for), or
treating it as a normal internal system with no special scrutiny (wrong in the
other direction, since it does sit in the payment flow). The right call — test
its segmentation explicitly rather than assuming either extreme — is what
SEG-05 and SEG-07 in the test results are actually for.

## The finding, and why it matters more than a clean pass would

SEG-07 found a real gap: a maintenance SSH rule was left open longer than
intended, creating a reachable path that shouldn't have existed. It didn't
expose cardholder data — Support Tooling never held PAN in the first place —
but a "this technically didn't cause harm" answer isn't good enough for an
assessor, and it isn't the honest framing either. The report treats it as
what it is: a segmentation-accuracy failure that happened not to coincide with
actual exposure, not a non-issue. The remediation (removing the rule, adding a
quarterly re-test) is the part that actually demonstrates the finding was
taken seriously rather than explained away.

## What I'd want feedback on

Section 5 (Anticipating Assessor Questions) is the part I'd most want a real
QSA or senior GRC person to push on — those are the questions I predicted
would come up, not questions I know for certain a real assessor would ask.
