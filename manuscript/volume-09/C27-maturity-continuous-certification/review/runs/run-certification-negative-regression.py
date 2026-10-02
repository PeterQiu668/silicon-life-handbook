#!/usr/bin/env python3
"""Preserved 25-case negative regression for the pinned C24 v2.4 controller."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha(value):
    return "sha256:" + hashlib.sha256(canon(value).encode()).hexdigest()


def reseal(record, field="record_digest"):
    record[field] = sha({key: value for key, value in record.items() if key != field})


def run_case(source, authority, runner, mutate_source=None, mutate_authority=None):
    candidate = copy.deepcopy(source)
    candidate["scenarios"] = [copy.deepcopy(source["scenarios"][0])]
    root = copy.deepcopy(authority)
    if mutate_source:
        mutate_source(candidate)
    if mutate_authority:
        mutate_authority(root)
    with tempfile.TemporaryDirectory(prefix="c24-v21-negative-") as tmp:
        inp = Path(tmp) / "input.json"
        auth = Path(tmp) / "authority.json"
        out = Path(tmp) / "result.json"
        inp.write_text(json.dumps(candidate, ensure_ascii=False, sort_keys=True, allow_nan=True) + "\n")
        auth.write_text(json.dumps(root, ensure_ascii=False, sort_keys=True) + "\n")
        proc = subprocess.run(
            ["python3", str(runner), "--input", str(inp), "--authority", str(auth), "--output", str(out)],
            capture_output=True,
            text=True,
        )
        if proc.returncode:
            return "SCHEMA_REJECT", proc.stderr.strip().splitlines()[-1]
        result = json.loads(out.read_text())
        trial = result["trials"][0]
        return trial["decision"], trial["reasons"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--authority", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = json.loads(Path(args.input).read_text())
    authority = json.loads(Path(args.authority).read_text())
    runner = Path(args.runner)
    cases = []

    def add(name, mutate, expected=("FAIL", "SCHEMA_REJECT")):
        cases.append((name, set(expected), mutate, None))

    def add_root(name, mutate, expected=("SCHEMA_REJECT",)):
        cases.append((name, set(expected), None, mutate))

    def cert_state(candidate):
        state = candidate["scenarios"][0]["state"]
        return state, state["certificate_registry"][state["certificate_ref"]]

    def expired_limited(candidate):
        _, cert = cert_state(candidate)
        cert["expires_at"] = "2026-09-29T00:00:00Z"
        reseal(cert)

    def lifecycle_kind_mismatch(candidate):
        state, _ = cert_state(candidate)
        state["lifecycle"]["kind"] = "REVOKE"
        reseal(state["lifecycle"])

    def future_lifecycle(candidate):
        state, _ = cert_state(candidate)
        state["lifecycle"]["occurred_at"] = "2026-10-02T00:00:00Z"
        reseal(state["lifecycle"])

    def material_missing_evidence(candidate):
        state, _ = cert_state(candidate)
        state["change"].update(material=True, kind="MODEL", impact_review="PASS", retest="PASS", evidence_ref="EV-MISSING")
        reseal(state["change"])

    def output_status(candidate, status):
        state, _ = cert_state(candidate)
        trial = next(iter(state["trial_registry"].values()))
        evidence = state["evidence_registry"][trial["output_ref"]]
        evidence["status"] = status
        reseal(evidence)

    def short_content(candidate, ref_key, value):
        state, _ = cert_state(candidate)
        ref = state["evidence_bundle"][ref_key]
        state["evidence_registry"][ref]["content_digest"] = value
        reseal(state["evidence_registry"][ref])

    # Exact seven attacks from the v2 independent review.
    add("expired_limited_certificate", expired_limited)
    add("lifecycle_kind_current_mismatch", lifecycle_kind_mismatch)
    add("future_lifecycle_event", future_lifecycle)
    add("material_change_missing_evidence", material_missing_evidence)
    add("trial_output_evidence_fail", lambda c: output_status(c, "FAIL"))
    add("artifact_short_unbound_content_digest", lambda c: short_content(c, "artifact_ref", "sha256:x"))
    add("signature_short_unbound_content_digest", lambda c: short_content(c, "signature_ref", "sha256:y"))

    # Near-neighbor semantic and digest attacks.
    add("trial_output_evidence_revoked", lambda c: output_status(c, "REVOKED"))
    add("artifact_well_formed_wrong_digest", lambda c: short_content(c, "artifact_ref", "sha256:" + "a" * 64))
    add("signature_well_formed_wrong_digest", lambda c: short_content(c, "signature_ref", "sha256:" + "b" * 64))
    add("manifest_short_content_digest", lambda c: short_content(c, "manifest_ref", "sha256:z"))
    add("holdout_short_content_digest", lambda c: short_content(c, "holdout_ref", "sha256:q"))
    add("grader_short_content_digest", lambda c: short_content(c, "grader_ref", "sha256:g"))
    add("failure_short_content_digest", lambda c: short_content(c, "failure_ref", "sha256:f"))
    add("cost_short_content_digest", lambda c: short_content(c, "cost_ref", "sha256:c"))

    def lifecycle_before_issue(candidate):
        state, cert = cert_state(candidate)
        state["lifecycle"]["occurred_at"] = "2026-09-01T00:00:00Z"
        cert["issued_at"] = "2026-09-30T11:50:00Z"
        reseal(state["lifecycle"]); reseal(cert)
    add("lifecycle_event_before_issue", lifecycle_before_issue)

    def expired_state_premature(candidate):
        state, cert = cert_state(candidate)
        cert["lifecycle"] = "EXPIRED"; reseal(cert)
        state["lifecycle"].update(current="EXPIRED", kind="EXPIRE"); reseal(state["lifecycle"])
    add("expired_state_before_expiry", expired_state_premature)

    def change_evidence_wrong_digest(candidate):
        state, _ = cert_state(candidate)
        ev = state["evidence_registry"][state["change"]["evidence_ref"]]
        ev["content_digest"] = "sha256:" + "d" * 64
        reseal(ev)
    add("material_change_evidence_wrong_content", change_evidence_wrong_digest)

    def lifecycle_evidence_wrong_digest(candidate):
        state, _ = cert_state(candidate)
        ev = state["evidence_registry"][state["lifecycle"]["evidence_ref"]]
        ev["content_digest"] = "sha256:" + "e" * 64
        reseal(ev)
    add("lifecycle_evidence_wrong_content", lifecycle_evidence_wrong_digest)

    def trial_output_wrong_trial(candidate):
        state, _ = cert_state(candidate)
        trial = next(iter(state["trial_registry"].values()))
        ev = state["evidence_registry"][trial["output_ref"]]
        ev["object_id"] = "TRIAL-WRONG"
        reseal(ev)
    add("trial_output_wrong_trial_binding", trial_output_wrong_trial)

    def trial_output_wrong_release(candidate):
        state, _ = cert_state(candidate)
        trial = next(iter(state["trial_registry"].values()))
        ev = state["evidence_registry"][trial["output_ref"]]
        ev["object_version"] = "openclaw@wrong"
        reseal(ev)
    add("trial_output_wrong_release_binding", trial_output_wrong_release)

    def state_self_reseal(candidate):
        state, cert = cert_state(candidate)
        cert["expires_at"] = "2036-09-30T00:00:00Z"
        reseal(cert)
    add("state_self_reseal_cannot_change_frozen_fact", state_self_reseal)

    add("source_trusted_clock_tamper", lambda c: c.update(now="2026-09-01T00:00:00Z"), expected=("SCHEMA_REJECT",))
    add_root("authority_root_literal_tamper", lambda r: r.update(root_digest="sha256:" + "f" * 64))

    def root_reseal(root):
        first = next(iter(root["scenario_registry"].values()))
        first["state_digest"] = "sha256:" + "1" * 64
        root["root_digest"] = sha({key: value for key, value in root.items() if key != "root_digest"})
    add_root("authority_registry_tamper_and_reseal", root_reseal)

    rows = []
    for attack_id, expected, mutate_source, mutate_authority in cases:
        actual, detail = run_case(source, authority, runner, mutate_source, mutate_authority)
        rows.append({"attack_id": attack_id, "secure_expected": sorted(expected), "actual": actual, "matched": actual in expected, "detail": detail})
    payload = {
        "schema": "c24.cert.negative-regression.v2.4-compat",
        "authority_root_digest": authority["root_digest"],
        "attack_count": len(rows),
        "matched_count": sum(row["matched"] for row in rows),
        "fail_open_count": sum(not row["matched"] for row in rows),
        "attacks": rows,
    }
    payload["suite_digest"] = sha(rows)
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in ("attack_count", "matched_count", "fail_open_count", "suite_digest")}, ensure_ascii=False))
    return 0 if payload["fail_open_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
