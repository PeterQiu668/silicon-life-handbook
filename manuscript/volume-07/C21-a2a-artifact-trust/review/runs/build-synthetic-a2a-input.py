#!/usr/bin/env python3
"""Build the frozen C18 v3 stateful synthetic fixture."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "synthetic-a2a-input.yaml"


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def scenario(scenario_id: str, layer: str, mutations: list[str], expected: str, *, shadow: bool = False) -> dict:
    record = {
        "id": scenario_id,
        "kind": "normal" if not mutations else "adversarial",
        "layer": layer,
        "security_red_team": bool(mutations),
        "mutations": mutations,
        "expected": expected,
    }
    if shadow:
        record["synthetic_shadow"] = True
        record["intended_target_layer"] = "representative_real_world"
    return record


def main() -> None:
    fixture = {
        "schema_version": "c18.synthetic.v3",
        "seed": "C18-2026-09-30-v3",
        "now": "2026-09-30T12:00:00Z",
        "environment": {"mode":"offline_synthetic","real_credentials":False,"network":False,"external_side_effects_allowed":False},
        "data_origin": "synthetic",
        "representative_real_world_executed": False,
        "synthetic_key_material": {"issuer-good":"SYNTHETIC-KEY-A","issuer-colluder":"SYNTHETIC-KEY-B"},
        "trust_roots": {"issuer-good":{"status":"ACTIVE","provider_org":"org-test"},"issuer-colluder":{"status":"REVOKED","provider_org":"org-colluder"}},
        "authority_store": {
            "auth-produce": {"actor":"agent-good","action":"produce","object":"report","scope":"local","not_before":"2026-09-30T00:00:00Z","expires":"2026-10-01T00:00:00Z","status":"ACTIVE","approver":"human-approver","policy_version":"policy-v2"}
        },
        "trusted_approvers": ["human-approver"],
        "delegation_store": {
            "delegation-good": {"parent_actor":"org-dispatch","child_actor":"agent-good","actions":["produce"],"objects":["report"],"scopes":["local"],"not_before":"2026-09-30T00:00:00Z","expires":"2026-10-01T00:00:00Z","status":"ACTIVE"}
        },
        "schema_registry": {
            "schema:report:v1": {"required_content_fields":["amount","unit","finding"],"allowed_units":["CNY"]}
        },
        "capability_probe_store": {
            "research":{"status":"VERIFIED","task_class":"research","risk":"high"},
            "draft":{"status":"VERIFIED","task_class":"draft","risk":"high"}
        },
        "stop_receipt_registry": {
            "stop-001": {
                "task_id":"task-001","worker":"agent-good","status":"VERIFIED",
                "issued_at":"2026-09-30T11:59:00Z","source":"control-plane",
                "object_digest": digest({"task_id":"task-001","worker":"agent-good","status":"VERIFIED","issued_at":"2026-09-30T11:59:00Z","source":"control-plane"})
            }
        },
        "base_card": {
            "agent_id":"agent-good","provider_org":"org-test","protocol":"1.0","supported_interfaces":["json-rpc"],
            "endpoint":"https://synthetic.invalid/a2a","skills":["research","draft"],"security_schemes":["bearer"],
            "issued_at":"2026-09-30T00:00:00Z","expires_at":"2026-10-01T00:00:00Z","signer_ref":"issuer-good","revocation_status":"ACTIVE"
        },
        "base_task": {"task_id":"task-001","owner":"agent-good","state_version":3,"current_state":"COMPLETED","delegation_ref":"delegation-good"},
        "base_artifact": {
            "artifact_id":"art-001","task_id":"task-001","object_type":"report","version":1,
            "schema_ref":"schema:report:v1","content":{"amount":100,"unit":"CNY","finding":"synthetic"},
            "producer":"agent-good","owner":"org-test","accountable_human":"human-owner",
            "authority_evidence_ref":"auth-produce","provenance":["input:synthetic-case-c","source:public"],
            "tool_receipts":["receipt:synthetic-tool-read"],"transformation_chain":["normalize","analyze","render"],
            "retention":{"class":"training-synthetic","expires_at":"2027-09-30T00:00:00Z"},
            "acceptance_evidence_ref":"accept-art-001",
            "signed_fields":["artifact_id","task_id","object_type","version","schema_ref","content","producer","owner","accountable_human","authority_evidence_ref","provenance","tool_receipts","transformation_chain","retention","acceptance_evidence_ref","content_digest"]
        },
        "base_events": [
            {"event_id":"e1","sequence":1,"task_id":"task-001","state_version":1,"protocol_state":"SUBMITTED"},
            {"event_id":"e2","sequence":2,"task_id":"task-001","state_version":2,"protocol_state":"WORKING"},
            {"event_id":"e3","sequence":3,"task_id":"task-001","state_version":3,"protocol_state":"COMPLETED","artifact_ref":"art-001"}
        ],
        "base_execution": {
            "worker_state":"STOPPED","descendants":[{"id":"child-1","state":"COMPLETED"}],"locks_released":True,
            "cancel":{"requested":False,"ack":"NONE"},"effect_ledger":[],"stop_receipt":{"status":"VERIFIED","receipt_id":"stop-001"},
            "authoritative_readback":{"worker":"STOPPED","queue":"CLEAR","inflight":"CLEAR"}
        },
        "real_world_evidence_manifest": {},
        "allowed_mutations": [
            "forged_card_signature","expired_card_cache","inflated_skill","duplicate_event","event_gap",
            "timeout_remote_running","cancel_ack_effect_pending","artifact_digest_mismatch","signed_content_wrong",
            "high_trust_no_authority","collusive_scoring","duplicate_id_different_payload"
        ],
    }
    fixture["scenarios"] = [
        scenario("S01","training",[],"PASS"),
        scenario("S02","regression",["forged_card_signature"],"FAIL"),
        scenario("S03","regression",["expired_card_cache"],"REVIEW_REQUIRED"),
        scenario("S04","holdout",["inflated_skill"],"REVIEW_REQUIRED"),
        scenario("S05","training",["duplicate_event"],"PASS"),
        scenario("S06","regression",["event_gap"],"REVIEW_REQUIRED"),
        scenario("S07","holdout",["timeout_remote_running"],"REVIEW_REQUIRED",shadow=True),
        scenario("S08","holdout",["cancel_ack_effect_pending"],"REVIEW_REQUIRED",shadow=True),
        scenario("S09","training",["artifact_digest_mismatch"],"FAIL"),
        scenario("S10","regression",["signed_content_wrong"],"FAIL"),
        scenario("S11","holdout",["high_trust_no_authority"],"FAIL"),
        scenario("S12","holdout",["collusive_scoring"],"FAIL"),
        scenario("S13","holdout",["duplicate_id_different_payload"],"FAIL"),
        scenario("S14","training",["duplicate_event"],"PASS"),
        scenario("S15","holdout",["expired_card_cache","high_trust_no_authority"],"FAIL"),
        scenario("S16","holdout",["signed_content_wrong","collusive_scoring"],"FAIL"),
        scenario("S17","holdout",["event_gap","cancel_ack_effect_pending"],"REVIEW_REQUIRED",shadow=True),
        scenario("S18","holdout",["artifact_digest_mismatch","duplicate_event","high_trust_no_authority"],"FAIL")
    ]
    OUTPUT.write_text(json.dumps(fixture, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
