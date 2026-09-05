# 04 — GRC Control Automation

**Framework:** GRC Engineering
**Core skill demonstrated:** Bridging governance and engineering — writing
automation that encodes the same judgment a manual reviewer would apply, not
just a raw API query.

## What's in this folder

| File | What it is |
|---|---|
| `scenario.md` | Why these two controls, and the judgment built into each script |
| `deliverables/mfa_enforcement_check.py` | Automates evidence collection for A.8.5 (Secure authentication) |
| `deliverables/s3_encryption_check.py` | Automates evidence collection for A.8.9 (Configuration management) |
| `deliverables/sample_data/` | Synthetic fixtures used in `--demo` mode (no real AWS data) |
| `deliverables/sample_output/` | Actual evidence reports produced by running both scripts |

## Running it yourself

Both scripts run with the Python standard library only in demo mode — no
AWS credentials or `boto3` install required:

```
cd deliverables
python3 mfa_enforcement_check.py --demo
python3 s3_encryption_check.py --demo
```

Each run prints a summary to the terminal and writes a timestamped CSV to
`sample_output/`. The `--live` code path (reading from a real AWS account via
`boto3`) is included in both scripts to show the production version, but isn't
runnable from this repo — see `scenario.md` for why.

## The actual finding worth reading

Both scripts surfaced something more interesting than a plain pass/fail:

- The MFA check separates **service accounts** from human users instead of
  flagging both as the same kind of failure.
- The S3 check treats an **unclassified bucket** as a different, arguably more
  urgent problem than a misconfigured one — you can't assess a control against
  data nobody's classified yet.

That distinction — what the automation should flag as a real finding versus
what it should route to a different process entirely — is the actual skill
this project is meant to demonstrate, not the Python itself.
