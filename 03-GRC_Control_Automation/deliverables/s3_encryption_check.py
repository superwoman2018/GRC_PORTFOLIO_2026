#!/usr/bin/env python3
"""
s3_encryption_check.py

Automates evidence collection for ISO 27001:2022 Annex A control A.8.9
(Configuration management) as applied to S3 bucket encryption and public
access settings.

Why this is more than a yes/no check
-------------------------------------
The naive version of this script would flag every unencrypted or publicly
readable bucket as a finding. That's wrong often enough to be actively
misleading:

  - A bucket correctly classified as "Public" (e.g. static assets served to
    a CDN) is SUPPOSED to be publicly readable and doesn't need encryption
    at rest to protect confidentiality — there's no confidentiality
    requirement for data that's intentionally public.
  - A bucket with NO classification at all is a different, arguably more
    urgent problem than a misconfigured one: you can't make an encryption
    or access decision for data you haven't classified yet. This script
    reports that as its own finding category (tied to A.5.9 / A.5.12 —
    asset inventory and classification), not as an encryption failure.

So the script's judgment isn't "is this encrypted" — it's "does this
bucket's configuration match what its declared classification requires."
That distinction is the actual point of this exercise: automation is good
at checking configuration against a rule, but the rule still has to be
written by someone who understands the classification scheme, not just
the API.

Modes
-----
--demo   Uses sample_data/s3_buckets_demo.json. No AWS access required.
--live   Queries real AWS S3 via boto3 (bucket encryption + public access
         block configuration). Requires credentials; not runnable in this
         portfolio context.
"""

import json
import csv
import argparse
from datetime import datetime, timezone
from pathlib import Path

CONTROL_ID = "A.8.9"
CONTROL_NAME = "Configuration management"


def load_demo_buckets(fixture_path: Path):
    with open(fixture_path, "r") as f:
        return json.load(f)["s3_buckets"]


def load_live_buckets():
    """Production path — queries real AWS S3. Not executed in this portfolio context."""
    import boto3

    s3 = boto3.client("s3")
    buckets = []
    for b in s3.list_buckets()["Buckets"]:
        name = b["Name"]
        try:
            enc = s3.get_bucket_encryption(Bucket=name)
            encryption_enabled = True
            encryption_type = enc["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]
        except s3.exceptions.ClientError:
            encryption_enabled = False
            encryption_type = None
        try:
            pab = s3.get_public_access_block(Bucket=name)["PublicAccessBlockConfiguration"]
            public_access_blocked = all(pab.values())
        except s3.exceptions.ClientError:
            public_access_blocked = False
        buckets.append({
            "name": name,
            "encryption_enabled": encryption_enabled,
            "encryption_type": encryption_type,
            "public_access_blocked": public_access_blocked,
            "data_classification": "unknown",  # would come from a tagging standard, not the S3 API itself
        })
    return buckets


def assess(buckets):
    rows = []
    for b in buckets:
        classification = b["data_classification"]

        if classification in (None, "Unclassified", "unknown"):
            status = "NEEDS CLASSIFICATION"
            note = "Bucket has no data classification on record. Cannot assess encryption/access requirements until classified (see A.5.9, A.5.12). Escalate to data owner."
        elif classification == "Public":
            status = "Compliant"
            note = "Classified Public — encryption and access-blocking are not required for intentionally public data."
        elif classification in ("Internal", "Confidential"):
            issues = []
            if not b["encryption_enabled"]:
                issues.append("encryption not enabled")
            if not b["public_access_blocked"]:
                issues.append("public access not blocked")
            if classification == "Confidential" and b["encryption_type"] not in ("SSE-KMS",):
                issues.append("Confidential data should use SSE-KMS, not default S3 encryption")
            if issues:
                status = "NON-COMPLIANT"
                note = "; ".join(issues)
            else:
                status = "Compliant"
                note = ""
        else:
            status = "NEEDS CLASSIFICATION"
            note = f"Unrecognized classification value '{classification}'."

        rows.append({
            "bucket": b["name"],
            "classification": classification,
            "encryption_enabled": b["encryption_enabled"],
            "encryption_type": b["encryption_type"] or "none",
            "public_access_blocked": b["public_access_blocked"],
            "control": CONTROL_ID,
            "status": status,
            "note": note,
        })
    return rows


def write_report(rows, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = output_dir / f"s3_config_evidence_report_{timestamp}.csv"
    fieldnames = ["bucket", "classification", "encryption_enabled", "encryption_type",
                  "public_access_blocked", "control", "status", "note"]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return out_path


def print_summary(rows):
    total = len(rows)
    compliant = sum(1 for r in rows if r["status"] == "Compliant")
    non_compliant = sum(1 for r in rows if r["status"] == "NON-COMPLIANT")
    needs_class = sum(1 for r in rows if r["status"] == "NEEDS CLASSIFICATION")
    print(f"\n{CONTROL_ID} — {CONTROL_NAME}: evidence summary")
    print(f"  Total buckets reviewed      : {total}")
    print(f"  Compliant                   : {compliant}")
    print(f"  NON-COMPLIANT               : {non_compliant}")
    print(f"  Needs classification first  : {needs_class}")
    if non_compliant or needs_class:
        print("\n  Findings:")
        for r in rows:
            if r["status"] != "Compliant":
                print(f"    - {r['bucket']}: {r['status']} — {r['note']}")


def main():
    parser = argparse.ArgumentParser(description="Automate S3 configuration evidence collection for A.8.9.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true", help="Use local synthetic fixture, no AWS access required.")
    mode.add_argument("--live", action="store_true", help="Query real AWS S3 (requires boto3 + credentials).")
    args = parser.parse_args()

    if args.demo:
        fixture = Path(__file__).parent / "sample_data" / "s3_buckets_demo.json"
        buckets = load_demo_buckets(fixture)
    else:
        buckets = load_live_buckets()

    rows = assess(buckets)
    out_path = write_report(rows, Path(__file__).parent / "sample_output")
    print_summary(rows)
    print(f"\nEvidence report written to: {out_path}")


if __name__ == "__main__":
    main()
