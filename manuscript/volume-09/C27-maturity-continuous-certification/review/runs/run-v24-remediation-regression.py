#!/usr/bin/env python3
"""C24 v2.4 author-side security regression.

The suite exercises the six v2.4 closure contracts without trusting fixture
names or author-supplied expected decisions.  It is offline and synthetic: a
PASS proves only the deterministic controller invariant, never a real-world
certificate, deployment, or external effect.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location("c24_v24_runner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def seal(runner, row, field="record_digest"):
    row[field] = runner.sha({k: v for k, v in row.items() if k != field})


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--authority", required=True)
    p.add_argument("--runner", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--output", required=True)
    z = p.parse_args()
    input_path, authority_path = Path(z.input), Path(z.authority)
    runner_path, result_path = Path(z.runner), Path(z.result)
    r = load(runner_path)
    raw_source = r.strict_json_loads(input_path.read_text())
    raw_authority = r.strict_json_loads(authority_path.read_text())
    authority = r.validate_authority(copy.deepcopy(raw_authority))
    source = r.validate(copy.deepcopy(raw_source), authority)
    saved = r.strict_json_loads(result_path.read_text())
    r.verify_result(copy.deepcopy(saved), authority, source)
    by_id = {x["scenario_id"]: x for x in source["scenarios"]}
    active_id = next(x["scenario_id"] for x in saved["trials"] if x["decision"] == "PASS" and x["lifecycle"] == "ACTIVE")
    active = by_id[active_id]
    rows = []

    def semantic(test_id, family, mutate, secure=None):
        scenario = copy.deepcopy(active)
        state = scenario["state"]
        decision, lifecycle, reasons = "ERROR", "REVOKED", []
        message = ""
        try:
            mutate(state)
            checked = r.validate_state(state, "v24." + test_id)
            decision, lifecycle, reasons, *_ = r.evaluate(source, checked, scenario["layer"], authority)
        except (ValueError, TypeError, KeyError) as exc:
            decision, lifecycle, reasons, message = "SCHEMA_REJECT", "REVOKED", [str(exc)], str(exc)
        ok = secure(decision, lifecycle, reasons) if secure else decision != "PASS"
        rows.append({"test_id": test_id, "family": family, "layer": "semantic_legal_reseal", "actual_decision": decision, "actual_lifecycle": lifecycle, "actual_reasons": reasons, "secure_contract_passed": bool(ok), "escape": not bool(ok), "message": message})

    def cert_window(state, issued, expires, lifecycle=None):
        cert = state["certificate_registry"][state["certificate_ref"]]
        cert["issued_at"], cert["expires_at"] = issued, expires
        if lifecycle:
            cert["lifecycle"] = lifecycle
            cert["public_claim"] = {
                "ACTIVE": "synthetic active assessment",
                "EXPIRED": "synthetic assessment expired",
            }[lifecycle]
            claim = state["evidence_registry"][cert["public_claim_ref"]]
            claim["content_digest"] = r.sha(cert["public_claim"])
            seal(r, claim)
            life = state["lifecycle"]
            life.update(current=lifecycle, kind="EXPIRE" if lifecycle == "EXPIRED" else "ACTIVATE", occurred_at=issued)
            seal(r, life)
            lev = state["evidence_registry"][life["evidence_ref"]]
            lev["content_digest"] = r.sha(r.lifecycle_payload(life))
            seal(r, lev)
        seal(r, cert)

    semantic("V24-01-ZERO-DURATION-ACTIVE", "certificate-window", lambda s: cert_window(s, "2026-09-30T11:50:00Z", "2026-09-30T11:50:00Z"))
    semantic("V24-02-ZERO-DURATION-EXPIRED", "certificate-window", lambda s: cert_window(s, "2026-09-30T11:50:00Z", "2026-09-30T11:50:00Z", "EXPIRED"))
    semantic("V24-03-NEGATIVE-WINDOW", "certificate-window", lambda s: cert_window(s, "2026-09-30T11:50:00Z", "2026-09-30T11:49:59Z"))
    semantic("V24-04-INVALID-ISSUED-STAMP", "certificate-window", lambda s: cert_window(s, "not-a-time", "2026-10-01T00:00:00Z"))

    def full_recert(state):
        app, ch = state["application"], state["change"]
        change_at = "2026-09-30T11:05:00Z"
        trial_times = ["2026-09-30T11:20:00Z", "2026-09-30T11:21:00Z", "2026-09-30T11:22:00Z"]
        evidence_times = ["2026-09-30T11:23:00Z", "2026-09-30T11:24:00Z", "2026-09-30T11:25:00Z"]
        entries = []
        trials = sorted(state["trial_registry"].values(), key=lambda x: x["layer"])
        # Keep the layer set explicit even if lexical order changes.
        trials = sorted(trials, key=lambda x: {"training": 0, "regression": 1, "holdout": 2}[x["layer"]])
        for t, completed, issued in zip(trials, trial_times, evidence_times):
            t["completed_at"] = completed
            seal(r, t)
            ev = state["evidence_registry"][t["output_ref"]]
            ev["issued_at"] = issued
            seal(r, ev)
            entries.append({"trial_ref": t["trial_id"], "evidence_ref": ev["evidence_id"], "layer": t["layer"], "security_slices": ["certification-redteam"], "affected_scopes": ["MODEL"]})
        manifest = {"manifest_id": "RETEST-MANIFEST-V24", "change_id": ch["change_id"], "pre_change_release": "openclaw@prechange-2026.9.5", "post_change_release": app["release"], "affected_scopes": ["MODEL"], "required_layers": ["training", "regression", "holdout"], "required_security_slices": ["certification-redteam"], "entries": entries}
        manifest["manifest_digest"] = r.sha(manifest)
        ch.update(material=True, kind="MODEL", impact_review="PASS", retest="PASS", issued_at=change_at, affected_scopes=["MODEL"], post_change_release=app["release"], retest_trial_refs=[x["trial_ref"] for x in entries], retest_evidence_refs=[x["evidence_ref"] for x in entries], retest_review_ref=next(iter(state["review_registry"])), retest_manifest=manifest)
        seal(r, ch)
        change_ev = state["evidence_registry"][ch["evidence_ref"]]
        change_ev["content_digest"] = r.sha(r.change_payload(app, ch))
        seal(r, change_ev)

    def recert_mutator(mutate):
        def apply(state):
            full_recert(state)
            mutate(state)
            ch = state["change"]
            rm = ch["retest_manifest"]
            rm["manifest_digest"] = r.sha({k: v for k, v in rm.items() if k != "manifest_digest"})
            seal(r, ch)
            ev = state["evidence_registry"][ch["evidence_ref"]]
            ev["content_digest"] = r.sha(r.change_payload(state["application"], ch))
            seal(r, ev)
        return apply

    semantic("V24-05-RECERT-MISSING-HOLDOUT", "post-change-lineage", recert_mutator(lambda s: (s["change"]["retest_trial_refs"].pop(), s["change"]["retest_evidence_refs"].pop(), s["change"]["retest_manifest"]["entries"].pop())))
    semantic("V24-06-RECERT-CROSS-TRIAL-OUTPUT", "post-change-lineage", recert_mutator(lambda s: s["change"]["retest_manifest"]["entries"][0].update(evidence_ref=s["change"]["retest_manifest"]["entries"][1]["evidence_ref"])))
    semantic("V24-07-RECERT-PUBLIC-CLAIM-EVIDENCE", "post-change-lineage", recert_mutator(lambda s: s["change"]["retest_manifest"]["entries"][0].update(evidence_ref=s["certificate_registry"][s["certificate_ref"]]["public_claim_ref"])))
    semantic("V24-08-RECERT-WRONG-AFFECTED-SCOPE", "post-change-lineage", recert_mutator(lambda s: s["change"]["retest_manifest"].update(affected_scopes=["TOOL"])))
    semantic("V24-09-RECERT-MISSING-SECURITY-SLICE", "post-change-lineage", recert_mutator(lambda s: s["change"]["retest_manifest"].update(required_security_slices=[])))
    semantic("V24-10-RECERT-SAME-PRE-POST-RELEASE", "post-change-lineage", recert_mutator(lambda s: s["change"]["retest_manifest"].update(pre_change_release=s["application"]["release"])))
    semantic("V24-11-RECERT-PRECHANGE-TRIAL", "post-change-lineage", recert_mutator(lambda s: (s["trial_registry"][s["change"]["retest_trial_refs"][0]].update(completed_at="2026-09-30T11:04:59Z"), seal(r, s["trial_registry"][s["change"]["retest_trial_refs"][0]]))))
    semantic("V24-12-RECERT-REVIEW-BEFORE-EVIDENCE", "post-change-lineage", recert_mutator(lambda s: (next(iter(s["review_registry"].values())).update(issued_at="2026-09-30T11:24:30Z"), seal(r, next(iter(s["review_registry"].values()))))))

    def effect(state, top_status, top_external, observed_status="APPLIED"):
        app = state["application"]
        obs = {"effect_id": "EFFECT-V24", "status": observed_status, "external": True, "environment": "external"}
        row = {"effect_id": "EFFECT-V24", "application_id": app["application_id"], "external": top_external, "status": top_status, "environment": "external", "receipt": copy.deepcopy(obs), "receipt_digest": r.sha(obs), "readback": copy.deepcopy(obs), "readback_digest": r.sha(obs)}
        seal(r, row)
        state["effect_ledger"] = [row]

    semantic("V24-13-EFFECT-NONE-HIDES-APPLIED", "effect-derivation", lambda s: effect(s, "NONE", False))
    semantic("V24-14-EFFECT-FAILED-HIDES-APPLIED", "effect-derivation", lambda s: effect(s, "FAILED", True))
    semantic("V24-15-EFFECT-UNKNOWN-HIDES-APPLIED", "effect-derivation", lambda s: effect(s, "UNKNOWN", True))
    semantic("V24-16-EFFECT-APPLIED-TOP-FALSE", "effect-derivation", lambda s: effect(s, "APPLIED", False))

    def reject_result(test_id, family, mutate, *, source_replay=False):
        candidate = copy.deepcopy(saved)
        mutate(candidate)
        candidate["decision_digest"] = r.sha(r.result_payload(candidate))
        actual, message = "ACCEPTED", ""
        try:
            r.verify_result(candidate, authority, source if source_replay else None)
        except (ValueError, TypeError, KeyError) as exc:
            actual, message = "REJECT", str(exc)
        ok = actual == "REJECT"
        rows.append({"test_id": test_id, "family": family, "layer": "persisted-result-verifier", "actual": actual, "secure_contract_passed": ok, "escape": not ok, "message": message})

    reject_result("V24-17-COHERENT-REAL-SUCCESS-REHASH", "independent-measurement-root", lambda x: (x["trials"][0].update(successful_real_certificates=1), x.update(successful_real_certificates=1)))
    reject_result("V24-18-COHERENT-EXTERNAL-SUCCESS-REHASH", "independent-measurement-root", lambda x: (x["trials"][0].update(successful_external_effects=1), x.update(successful_external_effects=1)))

    def rewrite_fail_to_pass(result):
        row = next(x for x in result["trials"] if x["decision"] == "FAIL")
        row.update(decision="PASS", lifecycle="ACTIVE", reasons=[])
        result["distribution"] = dict(sorted(Counter(x["decision"] for x in result["trials"]).items()))
        result["lifecycle_distribution"] = dict(sorted(Counter(x["lifecycle"] for x in result["trials"]).items()))

    reject_result("V24-19-FAIL-TO-PASS-REHASH", "semantic-replay", rewrite_fail_to_pass)
    reject_result("V24-20-FAIL-TO-PASS-REHASH-WITH-REPLAY", "semantic-replay", rewrite_fail_to_pass, source_replay=True)
    reject_result("V24-21-STATE-DIGEST-REWRITE", "semantic-replay", lambda x: x["trials"][0].update(state_digest="sha256:" + "0" * 64))

    def parse_attack(test_id, family, raw, kind):
        actual, message = "ACCEPTED", ""
        try:
            parsed = r.strict_json_loads(raw)
            if kind == "input": r.validate(parsed, authority)
            elif kind == "authority": r.validate_authority(parsed)
            else: r.verify_result(parsed, authority)
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            actual, message = "REJECT", str(exc)
        ok = actual == "REJECT"
        rows.append({"test_id": test_id, "family": family, "layer": "serialized-json-boundary", "actual": actual, "secure_contract_passed": ok, "escape": not ok, "message": message})

    input_text, authority_text, result_text = input_path.read_text(), authority_path.read_text(), result_path.read_text()
    parse_attack("V24-22-DUPLICATE-INPUT-TOP", "duplicate-json-key", input_text.replace("{", '{\n  "now":"1900-01-01T00:00:00Z",', 1), "input")
    parse_attack("V24-23-DUPLICATE-INPUT-NESTED", "duplicate-json-key", input_text.replace('"budget": 100.0', '"budget": -1,\n          "budget": 100.0', 1), "input")
    parse_attack("V24-24-DUPLICATE-AUTHORITY-TOP", "duplicate-json-key", authority_text.replace("{", '{\n  "issuer":"attacker",', 1), "authority")
    parse_attack("V24-25-DUPLICATE-AUTHORITY-NESTED", "duplicate-json-key", authority_text.replace('"status": "ACTIVE"', '"status": "REVOKED",\n      "status": "ACTIVE"', 1), "authority")
    parse_attack("V24-26-DUPLICATE-RESULT-TOP", "duplicate-json-key", result_text.replace("{", '{\n  "trial_count":999,', 1), "result")
    parse_attack("V24-27-DUPLICATE-RESULT-NESTED", "duplicate-json-key", result_text.replace('"decision": "PASS"', '"decision": "FAIL",\n      "decision": "PASS"', 1), "result")

    # Independent authority documents are pinned, so a submitted result cannot
    # rewrite both the counters and the measuring authority and then self-seal.
    def forged_authority(which):
        forged = copy.deepcopy(raw_authority)
        if which == "measurement":
            sid = active_id
            m = forged["measurement_registry"][sid]
            m["successful_real_certificates"] += 1
            m["record_digest"] = r.sha({k: v for k, v in m.items() if k != "record_digest"})
        else:
            sid = next(k for k, v in forged["semantic_registry"].items() if v["decision"] == "FAIL")
            s = forged["semantic_registry"][sid]
            s.update(decision="PASS", lifecycle="ACTIVE", reasons=[])
            s["semantic_digest"] = r.sha({k: v for k, v in s.items() if k != "semantic_digest"})
        forged["root_digest"] = r.sha({k: v for k, v in forged.items() if k != "root_digest"})
        return forged

    for test_id, kind in (("V24-28-FORGED-MEASUREMENT-ROOT", "measurement"), ("V24-29-FORGED-SEMANTIC-ROOT", "semantic")):
        actual, message = "ACCEPTED", ""
        try: r.validate_authority(forged_authority(kind))
        except (ValueError, TypeError, KeyError) as exc: actual, message = "REJECT", str(exc)
        ok = actual == "REJECT"
        rows.append({"test_id": test_id, "family": "pinned-independent-authority", "layer": "authority-root", "actual": actual, "secure_contract_passed": ok, "escape": not ok, "message": message})

    positives = []
    def positive(test_id, mutate):
        scenario = copy.deepcopy(active)
        decision, lifecycle, reasons = "ERROR", "REVOKED", []
        try:
            mutate(scenario["state"])
            checked = r.validate_state(scenario["state"], "v24.positive." + test_id)
            decision, lifecycle, reasons, *_ = r.evaluate(source, checked, scenario["layer"], authority)
        except (ValueError, TypeError, KeyError) as exc:
            reasons = [str(exc)]
        positives.append({"test_id": test_id, "decision": decision, "lifecycle": lifecycle, "reasons": reasons, "passed": decision == "PASS"})

    positive("V24-P01-UNCHANGED-ACTIVE", lambda s: None)
    positive("V24-P02-LEGAL-RECERTIFICATION", full_recert)
    payload = {
        "schema": "c24.cert.v2.4-remediation-regression.v1",
        "scope": "offline_synthetic_author_remediation",
        "input_sha256": "sha256:" + hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "authority_sha256": "sha256:" + hashlib.sha256(authority_path.read_bytes()).hexdigest(),
        "runner_sha256": "sha256:" + hashlib.sha256(runner_path.read_bytes()).hexdigest(),
        "result_sha256": "sha256:" + hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "attack_count": len(rows),
        "secure_count": sum(x["secure_contract_passed"] for x in rows),
        "escape_count": sum(x["escape"] for x in rows),
        "positive_count": len(positives),
        "positive_pass_count": sum(x["passed"] for x in positives),
        "attacks": rows,
        "positive_controls": positives,
        "limits": {"real_runtime_executed": False, "real_certificate_issued": False, "real_external_effect_executed": False, "practice_gate": "REVIEW_REQUIRED", "fact_cross_editor_chief_rc": "NOT_AUTHORIZED"},
    }
    payload["suite_digest"] = r.sha({"attacks": rows, "positive_controls": positives})
    Path(z.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: payload[k] for k in ("attack_count", "secure_count", "escape_count", "positive_count", "positive_pass_count", "suite_digest")}, ensure_ascii=False))
    return 0 if payload["escape_count"] == 0 and payload["positive_pass_count"] == payload["positive_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
