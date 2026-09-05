# Scenario

**Organization:** CloudNative (fictional) — same company as Projects 02 and 05.
**Objective:** Reduce manual evidence-collection effort for two Annex A controls
by automating the check, without losing the judgment a human reviewer would
apply.

## The starting point

CloudNative's security team was collecting evidence for two controls the same
way most teams do it manually: log into the AWS Console, check each IAM user
for an MFA device, screenshot the list; log into S3, click into each bucket,
check the encryption and public-access settings, screenshot those too. It works,
but it's slow, it goes stale immediately, and it's easy to miss a bucket or user
that got added since the last review.

## What got automated, and why these two controls specifically

**A.8.5 (Secure authentication)** and **A.8.9 (Configuration management)** were
chosen because they're both genuinely check-able against an API — "does this
user have MFA" and "is this bucket encrypted" are factual, queryable states, not
judgment calls in themselves. That's the actual criterion for whether a control
is a good automation candidate: can the answer be pulled from a system directly,
or does it require interpreting context a script can't see.

## Where the automation still needed judgment built in

Neither script is a naive "check the box" query — both had to encode a rule a
human GRC reviewer would apply, not just an API response:

- **MFA script:** service accounts (like a CI/CD deploy user) can't complete an
  interactive MFA challenge. A naive script would flag them as non-compliant
  right alongside a human user who genuinely has no MFA set up — which would
  bury the real finding in noise and train reviewers to ignore the report.
  The script separates service accounts into their own category with a
  different expected control (key rotation) instead.
- **S3 script:** a bucket correctly classified as "Public" is *supposed* to be
  unencrypted and publicly readable — flagging it as a finding would be wrong,
  not just noisy. More importantly, a bucket with **no classification at all**
  isn't a configuration failure, it's a *prerequisite* failure: you can't decide
  whether encryption is required until someone classifies the data. The script
  reports that as its own category (tied back to A.5.9/A.5.12, the same asset-
  classification controls from the Project 02 SoA) rather than guessing.

## What this doesn't solve

Automation only checks what it's told to check. It won't catch a bucket that
should exist but doesn't (an asset inventory gap, not a configuration gap), and
it can't decide whether a NON-COMPLIANT finding is worth an exception — that's
still a human risk-acceptance decision (see Project 05). What it does is turn a
half-day of manual screenshotting into a two-minute script run with a
timestamped, reproducible file — freeing that half-day for the judgment calls
that actually need a person.

## Why these scripts have a --demo mode

A real version of these scripts needs live AWS credentials to run against a
real account. Those credentials obviously can't go in a public portfolio repo.
Both scripts default to a `--demo` mode that runs against a local synthetic
data file instead — the logic being demonstrated is identical, but nothing here
requires or exposes real infrastructure access. The `--live` code path is
included so the production shape of each script is visible, even though it
isn't executable from this repo.
