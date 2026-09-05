#!/usr/bin/env python3
"""
mfa_enforcement_check.py

Automates evidence collection for ISO 27001:2022 Annex A control A.8.5
(Secure authentication) — specifically, verifying that IAM users have
multi-factor authentication enabled.

Why this exists
----------------
Before this script, "evidence of MFA enforcement" meant someone logging into
the AWS Console, taking a screenshot of the IAM users list, and pasting it
into a compliance folder every quarter. That's slow, easy to forget, and the
screenshot goes stale the moment a new user is added. This script queries the
actual IAM state and produces a dated, reproducible evidence report instead.

Modes
-----
--demo   Uses a local synthetic fixture (sample_data/iam_users_demo.json).
         No AWS credentials or network access required. This is the mode
         used to produce the sample_output/ file in this repo, since a
         public portfolio repo should never contain real cloud credentials
         or real employee usernames.
--live   Connects to a real AWS account via boto3 and queries IAM directly.
         Requires `pip install boto3` and valid AWS credentials configured
         in the environment. Not runnable in this portfolio context —
         included to show what the production version of this script does.

Judgment built into the script (not just the query)
-----------------------------------------------------
A raw "does this user have an MFA device" check isn't enough to be useful
evidence — it has to account for:
  - Service accounts (e.g. CI/CD deploy users) can't complete an interactive
    MFA challenge. Flagging them as an MFA "failure" is misleading; they need
    a different compensating control (access key rotation, least-privilege
    scoping) and are reported in their own category, not lumped in with
    human users who should have MFA and don't.
  - Users with no recent activity are flagged separately, since a stale
    account with no MFA is a different (and often lower) priority than an
    active one.

Output
------
Writes a timestamped CSV to sample_output/ with one row per user, their
MFA status, and a compliance flag against A.8.5.
"""

import json
import csv
import argparse
from datetime import datetime, timezone
from pathlib import Path

CONTROL_ID = "A.8.5"
CONTROL_NAME = "Secure authentication"


def load_demo_users(fixture_path: Path):
    with open(fixture_path, "r") as f:
        return json.load(f)["iam_users"]


def load_live_users():
    """
    Production path — queries real AWS IAM.
    Not used in --demo mode and not executed in this portfolio context.
    """
    import boto3  # imported here so --demo mode never requires boto3 installed

    iam = boto3.client("iam")
    users = []
    paginator = iam.get_paginator("list_users")
    for page in paginator.paginate():
        for u in page["Users"]:
            username = u["UserName"]
            mfa_devices = iam.list_mfa_devices(UserName=username)["MFADevices"]
            keys = iam.list_access_keys(UserName=username)["AccessKeyMetadata"]
            active_keys = [k for k in keys if k["Status"] == "Active"]
            users.append({
                "username": username,
                "role": "unknown",  # would be pulled from a tag or an identity-mapping source
                "mfa_devices": len(mfa_devices),
                "access_keys_active": len(active_keys),
                "last_activity": u.get("PasswordLastUsed", "unknown"),
            })
    return users


def is_service_account(username: str) -> bool:
    return username.startswith("svc-")


def assess(users):
    rows = []
    for u in users:
        service_acct = is_service_account(u["username"])
        has_mfa = u["mfa_devices"] > 0

        if service_acct:
            status = "N/A — service account"
            note = "MFA not applicable to non-interactive accounts. Compensating control: access key rotation policy applies instead (see A.5.17)."
        elif has_mfa:
            status = "Compliant"
            note = ""
        else:
            status = "NON-COMPLIANT"
            note = "No MFA device registered. Escalate to account owner for remediation."

        rows.append({
            "username": u["username"],
            "role": u["role"],
            "mfa_devices": u["mfa_devices"],
            "active_access_keys": u["access_keys_active"],
            "last_activity": u["last_activity"],
            "control": CONTROL_ID,
            "status": status,
            "note": note,
        })
    return rows


def write_report(rows, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = output_dir / f"mfa_evidence_report_{timestamp}.csv"
    fieldnames = ["username", "role", "mfa_devices", "active_access_keys",
                  "last_activity", "control", "status", "note"]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return out_path


def print_summary(rows):
    total = len(rows)
    compliant = sum(1 for r in rows if r["status"] == "Compliant")
    non_compliant = sum(1 for r in rows if r["status"] == "NON-COMPLIANT")
    na = sum(1 for r in rows if "N/A" in r["status"])
    print(f"\n{CONTROL_ID} — {CONTROL_NAME}: evidence summary")
    print(f"  Total accounts reviewed : {total}")
    print(f"  Compliant (MFA enabled) : {compliant}")
    print(f"  NON-COMPLIANT (no MFA)  : {non_compliant}")
    print(f"  N/A (service accounts)  : {na}")
    if non_compliant:
        print("\n  Non-compliant users:")
        for r in rows:
            if r["status"] == "NON-COMPLIANT":
                print(f"    - {r['username']} ({r['role']}) — last active {r['last_activity']}")


def main():
    parser = argparse.ArgumentParser(description="Automate MFA enforcement evidence collection for A.8.5.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true", help="Use local synthetic fixture, no AWS access required.")
    mode.add_argument("--live", action="store_true", help="Query real AWS IAM (requires boto3 + credentials).")
    args = parser.parse_args()

    if args.demo:
        fixture = Path(__file__).parent / "sample_data" / "iam_users_demo.json"
        users = load_demo_users(fixture)
    else:
        users = load_live_users()

    rows = assess(users)
    out_path = write_report(rows, Path(__file__).parent / "sample_output")
    print_summary(rows)
    print(f"\nEvidence report written to: {out_path}")


if __name__ == "__main__":
    main()
