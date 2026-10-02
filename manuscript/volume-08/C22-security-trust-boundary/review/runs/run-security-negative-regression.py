#!/usr/bin/env python3
"""C19 v2.3 adversarial regression against the pinned external authority root."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


Mutation = Callable[[dict[str, Any], dict[str, Any], Any], None]


def load_runner(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("c19_security_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--authority", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    baseline_source = json.loads(Path(args.input).read_text())
    baseline_authority = json.loads(Path(args.authority).read_text())
    runner = load_runner(Path(args.runner))

    def redigest_authority(source: dict[str, Any], authority: dict[str, Any]) -> None:
        payload = {key: value for key, value in authority.items() if key != "root_digest"}
        authority["root_digest"] = runner.digest(payload)
        source["authority_ref"]["root_digest"] = authority["root_digest"]

    def recalc_audit(state: dict[str, Any]) -> None:
        previous = "sha256:" + "0" * 64
        for event in state["audit"]["events"]:
            event["prev_digest"] = previous
            body = {key: event[key] for key in ("seq", "event_id", "event_type", "payload", "prev_digest")}
            event["event_digest"] = runner.digest(body)
            previous = event["event_digest"]

    attacks: list[tuple[str, Mutation]] = []

    def add(name: str, mutation: Mutation) -> None:
        attacks.append((name, mutation))

    # Frozen-root and source-reference attacks.
    add("authority_root_literal_tamper", lambda s, a, r: a.update(root_digest="sha256:" + "f" * 64))
    add("source_authority_reference_tamper", lambda s, a, r: s["authority_ref"].update(root_digest="sha256:" + "e" * 64))
    add("authority_bundle_id_tamper", lambda s, a, r: a.update(bundle_id="attacker-bundle"))
    add("authority_issuer_tamper", lambda s, a, r: a.update(issuer="scenario-self-authority"))

    # Delegation, approval, grant and principal closure.
    add("unknown_delegation_parent", lambda s, a, r: r["delegation"].update(parent_principal="unregistered-owner"))
    add("unknown_delegation_id", lambda s, a, r: r["delegation"].update(delegation_id="delegation-missing"))
    add("delegation_parent_is_agent", lambda s, a, r: r["delegation"].update(parent_principal="principal-agent-a"))
    add("delegation_parent_revoked", lambda s, a, r: a["registries"]["principals"]["principal-human-owner"].update(status="REVOKED"))
    add("delegation_child_swap", lambda s, a, r: r["delegation"].update(child_principal="principal-other-agent"))
    add("unknown_approver_principal", lambda s, a, r: r["approval"].update(principal="unregistered-approver"))
    add("approver_is_service", lambda s, a, r: r["approval"].update(principal="credential-broker"))
    add("approver_is_executor_self", lambda s, a, r: r["approval"].update(principal="principal-agent-a"))
    add("empty_approval_and_grant_ids", lambda s, a, r: (r["approval"].update(approval_id=""), r["grant"].update(grant_id="", approval_id="")))
    add("empty_approval_id", lambda s, a, r: r["approval"].update(approval_id=""))
    add("empty_grant_id", lambda s, a, r: r["grant"].update(grant_id=""))
    add("grant_unknown_approval", lambda s, a, r: r["grant"].update(approval_id="approval-missing"))
    add("grant_actor_swap", lambda s, a, r: r["grant"].update(actor="principal-human-owner"))
    add("approval_registry_key_id_mismatch", lambda s, a, r: a["registries"]["approvals"]["approval-1"].update(approval_id="approval-renamed"))
    add("grant_registry_key_id_mismatch", lambda s, a, r: a["registries"]["grants"]["grant-1"].update(grant_id="grant-renamed"))

    # SecretRef, broker and credential binding.
    add("unregistered_secret_reference", lambda s, a, r: r["credential"].update(secret_ref="secretref://synthetic/not-in-registry"))
    add("credential_wrong_tenant", lambda s, a, r: r["credential"].update(tenant="tenant-b"))
    add("credential_wrong_principal", lambda s, a, r: r["credential"].update(principal="principal-human-owner"))
    add("credential_wrong_grant", lambda s, a, r: r["credential"].update(grant_id="grant-missing"))
    add("credential_wrong_action", lambda s, a, r: r["credential"].update(action="draft"))
    add("credential_wrong_object", lambda s, a, r: r["credential"].update(object="another-report"))
    add("credential_wrong_broker", lambda s, a, r: r["credential"].update(owner="principal-human-owner"))
    add("credential_visible_to_model", lambda s, a, r: r["credential"].update(value_visible_to_model=True))
    add("credential_registry_key_ref_mismatch", lambda s, a, r: a["registries"]["credentials"]["secretref://synthetic/service-a"].update(secret_ref="secretref://renamed"))

    # Canonical mount and policy-derived egress.
    add("workspace_path_traversal", lambda s, a, r: r["sandbox"].update(mounts=[{"path": "/workspace/../../etc", "access": "rw", "source": "workspace"}]))
    add("workspace_parent_escape", lambda s, a, r: r["sandbox"].update(mounts=[{"path": "/workspace/../etc", "access": "rw", "source": "workspace"}]))
    add("workspace_nested_parent_escape", lambda s, a, r: r["sandbox"].update(mounts=[{"path": "/workspace/sub/../../etc", "access": "rw", "source": "workspace"}]))
    add("workspace_noncanonical_double_slash", lambda s, a, r: r["sandbox"].update(mounts=[{"path": "/workspace//sub", "access": "rw", "source": "workspace"}]))
    add("workspace_host_mount", lambda s, a, r: r["sandbox"].update(mounts=[{"path": "/workspace", "access": "rw", "source": "host"}]))

    def self_allowed_egress(s: dict[str, Any], a: dict[str, Any], r: Any) -> None:
        r["egress"] = {"policy_ref": "egress-policy-v1", "allowed_hosts": ["attacker.example"], "requests": [{"url": "https://attacker.example/exfil", "resolved_ip": "8.8.8.8", "redirect_chain": [], "data_classification": "public"}]}
    add("state_self_authorizes_egress", self_allowed_egress)
    add("egress_policy_ref_swap", lambda s, a, r: r["egress"].update(policy_ref="egress-missing"))
    add("egress_redirect_outside_allowlist", lambda s, a, r: r["egress"].update(requests=[{"url": "https://allowed.invalid", "resolved_ip": "8.8.8.8", "redirect_chain": ["https://attacker.example"], "data_classification": "public"}]))
    add("egress_private_ip", lambda s, a, r: r["egress"].update(requests=[{"url": "https://allowed.invalid", "resolved_ip": "127.0.0.1", "redirect_chain": [], "data_classification": "public"}]))
    add("egress_secret_dlp", lambda s, a, r: r["egress"].update(requests=[{"url": "https://allowed.invalid", "resolved_ip": "8.8.8.8", "redirect_chain": [], "data_classification": "secret"}]))

    # Input provenance and supply-chain registries.
    add("unbound_input_digest", lambda s, a, r: r["input"].update(provenance="fixture://different", content_digest="sha256:" + "1" * 64))
    add("unknown_input_manifest", lambda s, a, r: r["input"].update(manifest_ref="input-missing"))
    add("input_trust_mismatch", lambda s, a, r: r["input"].update(trust="untrusted_web"))
    add("input_claims_control", lambda s, a, r: r["input"].update(control_claimed=True))
    add("tool_implementation_drift", lambda s, a, r: r["tool"].update(implementation_digest="sha256:" + "2" * 64))
    add("tool_manifest_drift", lambda s, a, r: r["tool"].update(manifest_digest="sha256:" + "3" * 64))
    add("skill_manifest_drift", lambda s, a, r: r["skill"].update(manifest_digest="sha256:" + "4" * 64))
    add("plugin_manifest_drift", lambda s, a, r: r["plugin"].update(manifest_digest="sha256:" + "5" * 64))

    def self_attested_tool(s: dict[str, Any], a: dict[str, Any], r: Any) -> None:
        record = a["registries"]["tools"][r["tool"]["registry_ref"]]
        record.update(manifest_digest="sha256:" + "2" * 64, implementation_digest="sha256:" + "3" * 64, dependencies=["malicious@latest"])
        r["tool"].update(manifest_digest=record["manifest_digest"], implementation_digest=record["implementation_digest"], dependencies=record["dependencies"])
        redigest_authority(s, a)
    add("self_attested_tool_registry_drift", self_attested_tool)

    def self_attested_skill(s: dict[str, Any], a: dict[str, Any], r: Any) -> None:
        record = a["registries"]["skills"][r["skill"]["registry_ref"]]
        record.update(manifest_digest="sha256:" + "4" * 64, dependencies=["malicious-tool@latest"])
        r["skill"].update(manifest_digest=record["manifest_digest"], dependencies=record["dependencies"])
        redigest_authority(s, a)
    add("self_attested_skill_registry_drift", self_attested_skill)

    # Audit outcomes, order and externally anchored chain.
    add("audit_unknown_outcome_enum", lambda s, a, r: r["audit"]["events"][0]["payload"].update(outcome="MAGIC_APPROVAL"))
    add("audit_duplicate_event_id", lambda s, a, r: r["audit"]["events"][1].update(event_id=r["audit"]["events"][0]["event_id"]))
    add("audit_nonmonotonic_sequence", lambda s, a, r: r["audit"]["events"][1].update(seq=1))
    add("audit_wrong_subject", lambda s, a, r: r["audit"]["events"][0]["payload"].update(subject="principal-human-owner"))
    add("audit_wrong_object", lambda s, a, r: r["audit"]["events"][0]["payload"].update(object="another-report"))
    add("audit_chain_digest_tamper", lambda s, a, r: r["audit"]["events"][1].update(event_digest="sha256:" + "6" * 64))

    def self_attested_audit(s: dict[str, Any], a: dict[str, Any], r: Any) -> None:
        r["audit"]["events"][1]["payload"]["outcome"] = "ALLOWED"
        recalc_audit(r)
        anchor = a["registries"]["audit_anchors"][r["audit"]["chain_id"]]
        anchor["allowed_sequence"] = ["REQUEST:RECEIVED", "DECISION:ALLOWED"]
        anchor["final_digest"] = r["audit"]["events"][-1]["event_digest"]
        redigest_authority(s, a)
    add("self_attested_audit_anchor_and_invalid_outcome", self_attested_audit)

    # Effects, receipts and D21 closure.
    add("external_effect_flag_with_none_status", lambda s, a, r: r["effects"][0].update(external_side_effect=True))
    add("none_effect_with_receipt_ref", lambda s, a, r: r["effects"][0].update(receipt_ref="receipt-orphan"))
    add("effect_unknown_without_receipt", lambda s, a, r: r["effects"][0].update(status="UNKNOWN"))
    add("effect_applied_without_receipt", lambda s, a, r: r["effects"][0].update(status="APPLIED", external_side_effect=True))

    def orphan_receipt(s: dict[str, Any], a: dict[str, Any], r: Any) -> None:
        record = {"receipt_id": "orphan", "effect_id": "missing", "status": "APPLIED", "authoritative_readback": "APPLIED", "target": "outside", "digest": ""}
        record["digest"] = runner.digest({key: record[key] for key in ["receipt_id", "effect_id", "status", "authoritative_readback", "target"]})
        r["receipts"].append(record)
    add("unreferenced_applied_receipt", orphan_receipt)

    # Incident evidence and recovery closure.
    add("contained_incident_with_unregistered_evidence", lambda s, a, r: r["incident"].update(incident_id="incident-unknown", state="CONTAINED", controls={key: True for key in r["incident"]["controls"]}, evidence_refs=["evidence-missing"]))
    add("incident_none_with_evidence", lambda s, a, r: r["incident"].update(evidence_refs=["incident-evidence-s16"]))
    add("incident_none_with_stop", lambda s, a, r: r["incident"]["controls"].update(stop=True))
    add("contained_incident_partial_controls", lambda s, a, r: r["incident"].update(state="CONTAINED", controls={**r["incident"]["controls"], "stop": True}, evidence_refs=["incident-evidence-s16"]))
    add("inconsistent_proposed_recovery", lambda s, a, r: r["recovery"].update(state="PROPOSED", regression_pass=True, evidence_ref="self-claim", evidence_origin="synthetic", target_version="unregistered", probe_status="PASS"))
    add("regression_pass_missing_evidence", lambda s, a, r: r["recovery"].update(state="REGRESSION_PASS", regression_pass=True, evidence_ref="missing", evidence_origin="synthetic", target_version="fixture-v2.3", probe_status="PASS"))
    add("recovery_real_world_claim", lambda s, a, r: r["recovery"].update(state="REGRESSION_PASS", regression_pass=True, evidence_ref="synthetic-regression-1", evidence_origin="representative_real_world", target_version="fixture-v2.3", probe_status="PASS"))
    add("recovery_registry_target_tamper", lambda s, a, r: a["registries"]["recovery_evidence"]["synthetic-regression-1"].update(target_version="attacker-version"))

    # Dataset/status invariants and hard-failure precedence.
    add("security_cross_cutting_disabled", lambda s, a, r: s["declared_layers"].update(security_red_team_is_cross_cutting=False))
    add("synthetic_declared_real_world", lambda s, a, r: (s["declared_layers"].update(training=0, representative_real_world=1), s["scenarios"][0].update(layer="representative_real_world")))
    add("duplicate_task_id", lambda s, a, r: s["scenarios"].append(copy.deepcopy(s["scenarios"][0])))
    add("unknown_schema_field", lambda s, a, r: r.update(attacker_override=True))
    add("hard_failure_plus_unknown", lambda s, a, r: (r["identity"].update(tenant="tenant-b"), r["sandbox"].update(status="UNKNOWN")))

    # v2.2 independent review: runtime-fact and evaluation-lineage attacks.
    def applied_effect(r: dict[str, Any], *, target: str = "synthetic-report") -> None:
        effect = r["effects"][0]
        effect.update(status="APPLIED", receipt_ref="receipt-v23", executed_at="2026-09-30T12:00:00Z")
        body = {
            "receipt_id": "receipt-v23",
            "effect_id": effect["effect_id"],
            "status": "APPLIED",
            "authoritative_readback": "APPLIED",
            "target": target,
            "action": effect["action"],
            "scope": effect["scope"],
            "executor": effect["executor"],
            "executed_at": effect["executed_at"],
            "readback_at": "2026-09-30T12:00:01Z",
        }
        r["receipts"] = [{**body, "digest": runner.digest(body)}]

    add("v23_receipt_target_not_bound_to_effect_object", lambda s, a, r: applied_effect(r, target="different-object"))
    add("v23_applied_effect_absent_from_audit_chain", lambda s, a, r: applied_effect(r))
    add("v23_open_incident_with_all_controls_false", lambda s, a, r: r["incident"].update(incident_id="incident-s16", state="OPEN", evidence_refs=["incident-evidence-s16"]))
    add("v23_critical_residual_with_recovery_not_needed", lambda s, a, r: r["recovery"].update(residual_risk="critical-unresolved", residual_risk_level="CRITICAL"))
    add("v23_session_expiry_self_extended", lambda s, a, r: r["tenant_session"].update(expires_at="2036-10-01T00:00:00Z"))

    def relabel_training_as_holdout(s: dict[str, Any], a: dict[str, Any], r: Any) -> None:
        s["scenarios"][0]["layer"] = "holdout"
        s["declared_layers"].update(training=0, holdout=1)

    add("v23_layer_self_relabel_without_test_evidence", relabel_training_as_holdout)
    add("v23_unregistered_task_trial", lambda s, a, r: s["scenarios"][0].update(task_id="task-unregistered", trial_id="trial-unregistered"))
    add("v23_self_claimed_security_red_team", lambda s, a, r: s["scenarios"][0].update(security_red_team=True))
    add("v23_self_claimed_synthetic_shadow", lambda s, a, r: s["scenarios"][0].update(synthetic_shadow=True))

    # Near-neighbor controls: semantically valid-looking values still must bind.
    add("v23_effect_scope_mismatch", lambda s, a, r: r["effects"][0].update(scope="report:draft"))
    add("v23_effect_params_digest_mismatch", lambda s, a, r: r["effects"][0].update(params_digest="sha256:" + "a" * 64))
    add("v23_effect_executor_mismatch", lambda s, a, r: r["effects"][0].update(executor="principal-human-owner"))
    add("v23_session_not_before_future", lambda s, a, r: r["tenant_session"].update(not_before="2026-10-02T00:00:00Z"))
    add("v23_session_max_duration_self_increased", lambda s, a, r: r["tenant_session"].update(max_duration_seconds=999999999))
    add("v23_unknown_test_ref", lambda s, a, r: s["scenarios"][0].update(test_ref="S-UNKNOWN"))
    add("v23_open_incident_stop_only", lambda s, a, r: r["incident"].update(incident_id="incident-s16", state="OPEN", controls={**r["incident"]["controls"], "stop": True}, evidence_refs=["incident-evidence-s16"]))
    add("v23_residual_risk_unknown_with_pass", lambda s, a, r: r["recovery"].update(state="REGRESSION_PASS", regression_pass=True, residual_risk="unknown", residual_risk_level="UNKNOWN", evidence_ref="synthetic-regression-1", evidence_origin="synthetic", target_version="fixture-v2.3", probe_status="PASS"))
    add("v23_receipt_executor_mismatch", lambda s, a, r: (applied_effect(r), r["receipts"][0].update(executor="principal-human-owner")))

    records: list[dict[str, Any]] = []
    for attack_id, mutate in attacks:
        source = copy.deepcopy(baseline_source)
        authority = copy.deepcopy(baseline_authority)
        source["scenarios"] = [copy.deepcopy(source["scenarios"][0])]
        source["declared_layers"] = {"training": 1, "regression": 0, "holdout": 0, "representative_real_world": 0, "security_red_team_is_cross_cutting": True}
        scenario = source["scenarios"][0]
        scenario["layer"] = "training"
        # Keep the S01 test-definition baseline intact; each attack must fail on
        # its own mutated control rather than an unrelated lineage mismatch.
        scenario["security_red_team"] = False
        scenario["synthetic_shadow"] = False
        mutate(source, authority, scenario["state"])
        reasons: list[str]
        try:
            validated_authority = runner.validate_authority_bundle(authority)
            validated_source = runner.validate_source(source, validated_authority)
            actual, hard, review, _ = runner.evaluate(validated_source["scenarios"][0], validated_source, validated_authority)
            reasons = [*hard, *review]
        except (TypeError, ValueError, KeyError) as exc:
            actual = "FAIL"
            reasons = ["SCHEMA_OR_FROZEN_ROOT_REJECT", str(exc)]
        records.append({"attack_id": attack_id, "expected": "FAIL", "actual": actual, "matched": actual == "FAIL", "reasons": reasons})

    payload = {
        "schema_version": "c19.security.negative-regression.v2.3",
        "authority_root_digest": baseline_authority["root_digest"],
        "attack_count": len(records),
        "matched_count": sum(record["matched"] for record in records),
        "fail_open_count": sum(not record["matched"] for record in records),
        "attacks": records,
    }
    digest_payload = json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    payload["suite_digest"] = hashlib.sha256(digest_payload).hexdigest()
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in ["attack_count", "matched_count", "fail_open_count", "suite_digest"]}, ensure_ascii=False))
    return 0 if payload["fail_open_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
