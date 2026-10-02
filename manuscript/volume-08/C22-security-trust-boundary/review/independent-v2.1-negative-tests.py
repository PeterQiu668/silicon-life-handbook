#!/usr/bin/env python3
"""Non-author near-neighbor attacks beyond the C19 v2.1 author regression."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


RUNS = Path(__file__).resolve().parent / "runs"
INPUT = RUNS / "synthetic-security-input.yaml"
RUNNER = RUNS / "run-security-harness.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("c19_independent_runner", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    baseline = json.loads(INPUT.read_text())
    records = []

    def run(attack_id, mutate, expected="FAIL"):
        source = copy.deepcopy(baseline)
        source["scenarios"] = [copy.deepcopy(source["scenarios"][0])]
        source["declared_layers"] = {
            "training": 1,
            "regression": 0,
            "holdout": 0,
            "representative_real_world": 0,
            "security_red_team_is_cross_cutting": True,
        }
        mutate(source, source["scenarios"][0]["state"])
        try:
            runner.validate_source(source)
            actual, hard, review, _ = runner.evaluate(source["scenarios"][0], source)
        except (TypeError, ValueError) as exc:
            actual, hard, review = "SCHEMA_REJECT", [str(exc)], []
        records.append({"id": attack_id, "expected": expected, "actual": actual, "matched": actual == expected, "reasons": [*hard, *review]})

    run("unknown_delegation_parent", lambda x, s: s["delegation"].update(parent_principal="unregistered-owner"))
    run("unknown_approver_principal", lambda x, s: s["approval"].update(principal="unregistered-approver"))
    run("empty_approval_and_grant_ids", lambda x, s: (s["approval"].update(approval_id=""), s["grant"].update(grant_id="", approval_id="")))
    run("unregistered_secret_reference", lambda x, s: s["credential"].update(secret_ref="secretref://synthetic/not-in-registry"))
    run("workspace_path_traversal", lambda x, s: s["sandbox"].update(mounts=[{"path":"/workspace/../../etc","access":"rw","source":"workspace"}]))

    def self_allowed_egress(x, s):
        s["egress"] = {"allowed_hosts":["attacker.example"], "requests":[{"url":"https://attacker.example/exfil","resolved_ip":"8.8.8.8","redirect_chain":[],"data_classification":"public"}]}
    run("state_self_authorizes_egress", self_allowed_egress)

    run("unbound_input_digest", lambda x, s: s["input"].update(provenance="fixture://different", content_digest="sha256:" + "1" * 64))

    def self_attested_tool_registry(x, s):
        record = x["authorities"]["tool_registry"][s["tool"]["registry_ref"]]
        record.update(manifest_digest="sha256:" + "2" * 64, implementation_digest="sha256:" + "3" * 64, dependencies=["malicious@latest"])
        s["tool"].update(manifest_digest=record["manifest_digest"], implementation_digest=record["implementation_digest"], dependencies=record["dependencies"])
    run("self_attested_tool_registry_drift", self_attested_tool_registry)

    def self_attested_skill_registry(x, s):
        record = x["authorities"]["skill_registry"][s["skill"]["registry_ref"]]
        record.update(manifest_digest="sha256:" + "4" * 64, dependencies=["malicious-tool@latest"])
        s["skill"].update(manifest_digest=record["manifest_digest"], dependencies=record["dependencies"])
    run("self_attested_skill_registry_drift", self_attested_skill_registry)

    def self_attested_audit_anchor(x, s):
        previous = "sha256:" + "0" * 64
        for event in s["audit"]["events"]:
            event["payload"]["outcome"] = "MAGIC_APPROVAL"
            event["prev_digest"] = previous
            body = {key: event[key] for key in ("seq", "event_id", "event_type", "payload", "prev_digest")}
            event["event_digest"] = runner.digest(body)
            previous = event["event_digest"]
        x["authorities"]["audit_anchors"][s["audit"]["chain_id"]]["final_digest"] = previous
    run("self_attested_audit_anchor_and_invalid_outcome", self_attested_audit_anchor)

    run("contained_incident_with_unregistered_evidence", lambda x, s: s["incident"].update(state="CONTAINED", controls={key: True for key in s["incident"]["controls"]}, evidence_refs=["not-in-audit-registry"]))
    run("inconsistent_proposed_recovery", lambda x, s: s["recovery"].update(state="PROPOSED", regression_pass=True, evidence_ref="self-claim", evidence_origin="synthetic", target_version="unregistered", probe_status="PASS"))
    run("external_effect_flag_with_none_status", lambda x, s: s["effects"][0].update(external_side_effect=True))
    run("unreferenced_applied_receipt", lambda x, s: s["receipts"].append({"receipt_id":"orphan","effect_id":"missing","status":"APPLIED","authoritative_readback":"APPLIED","target":"outside","digest":runner.digest({"receipt_id":"orphan","effect_id":"missing","status":"APPLIED","authoritative_readback":"APPLIED","target":"outside"})}))
    run("security_cross_cutting_disabled", lambda x, s: x["declared_layers"].update(security_red_team_is_cross_cutting=False))

    print(json.dumps({
        "attack_count": len(records),
        "matched_count": sum(record["matched"] for record in records),
        "fail_open_count": sum(not record["matched"] for record in records),
        "attacks": records,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
