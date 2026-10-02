#!/usr/bin/env python3
"""Independent C18 v2 reproduction and adversarial state-boundary checks.

This script never writes the author fixture. It rebuilds/runs two fresh copies,
then evaluates independent mutations against the current state-derived control.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import py_compile
import shutil
import subprocess
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("c18_current_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load current runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def resign_card(module, raw: dict, source: dict) -> None:
    card = raw["card"]
    payload = {key: value for key, value in card.items() if key != "signature"}
    card["signature"] = module.sign(payload, card["signer_ref"], source["synthetic_key_material"])
    raw["cache"]["card_digest"] = module.digest(card)


def resign_artifact(module, raw: dict, source: dict, signer: str = "issuer-good") -> None:
    artifact = raw["artifact"]
    artifact["content_digest"] = module.digest(artifact["content"])
    payload = {key: artifact[key] for key in artifact["signed_fields"] if key in artifact}
    artifact["signature"] = {
        "signer_ref": signer,
        "value": module.sign(payload, signer, source["synthetic_key_material"]),
    }


def run_fresh_copy(package: Path, label: str) -> dict:
    runs = package / "review" / "runs"
    with tempfile.TemporaryDirectory(prefix=f"c18-v2-independent-{label}-") as raw_dir:
        temp = Path(raw_dir)
        builder = temp / "build-synthetic-a2a-input.py"
        runner = temp / "run-a2a-harness.py"
        shutil.copy2(runs / builder.name, builder)
        shutil.copy2(runs / runner.name, runner)
        py_compile.compile(str(builder), doraise=True)
        py_compile.compile(str(runner), doraise=True)
        subprocess.run(["python3", str(builder)], cwd=temp, check=True, capture_output=True, text=True)
        completed = subprocess.run(
            ["python3", str(runner), "--input", str(temp / "synthetic-a2a-input.yaml"), "--output", str(temp / "synthetic-a2a-results.yaml")],
            cwd=temp,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads((temp / "synthetic-a2a-results.yaml").read_text(encoding="utf-8"))
        return {
            "label": label,
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "input_sha256": sha256(temp / "synthetic-a2a-input.yaml"),
            "results_sha256": sha256(temp / "synthetic-a2a-results.yaml"),
            "summary_sha256": sha256(temp / "synthetic-a2a-summary.md"),
            "input_bytes": (temp / "synthetic-a2a-input.yaml").stat().st_size,
            "results_bytes": (temp / "synthetic-a2a-results.yaml").stat().st_size,
            "summary_bytes": (temp / "synthetic-a2a-summary.md").stat().st_size,
            "trial_count": result["trial_count"],
            "distribution": result["distribution"],
            "by_layer": result["by_layer"],
            "decision_digest": result["decision_digest"],
            "representative_real_world_evidence_count": result["representative_real_world_evidence_count"],
            "synthetic_shadow_trial_count": result["synthetic_shadow_trial_count"],
            "external_side_effect_count": result["external_side_effect_count"],
        }


def verdict_attack(module, source: dict, scenario: dict, attack_id: str, target: str, expected: list[str], mutate) -> dict:
    local_source = copy.deepcopy(source)
    local_scenario = copy.deepcopy(scenario)
    raw = module.materialize(local_source, local_scenario)
    mutate(raw, local_source)
    try:
        decision, reasons, states, effects = module.evaluate(raw, local_source)
        actual = decision
        error = None
    except Exception as exc:  # fail-closed schema rejection is a valid outcome for selected tests
        actual = "SCHEMA_REJECT"
        reasons = []
        states = {}
        effects = None
        error = f"{type(exc).__name__}: {exc}"
    return {
        "attack_id": attack_id,
        "target": target,
        "boundary": "materialized_state",
        "expected_allowed_outcomes": expected,
        "actual_outcome": actual,
        "control_passed": actual in expected,
        "reasons": reasons,
        "states": states,
        "external_effects": effects,
        "error": error,
    }


def source_attack(module, source: dict, attack_id: str, target: str, expected: list[str], mutate) -> dict:
    local_source = copy.deepcopy(source)
    mutate(local_source)
    try:
        checked = module.validate_source(local_source)
        scenario = checked["scenarios"][0]
        raw = module.materialize(checked, scenario)
        decision, reasons, states, effects = module.evaluate(raw, checked)
        actual = decision
        error = None
    except Exception as exc:
        actual = "SCHEMA_REJECT"
        reasons = []
        states = {}
        effects = None
        error = f"{type(exc).__name__}: {exc}"
    return {
        "attack_id": attack_id,
        "target": target,
        "boundary": "source_contract",
        "expected_allowed_outcomes": expected,
        "actual_outcome": actual,
        "control_passed": actual in expected,
        "reasons": reasons,
        "states": states,
        "external_effects": effects,
        "error": error,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = Path(args.package).resolve()
    output_path = Path(args.output).resolve()
    runs = package / "review" / "runs"
    module = load_module(runs / "run-a2a-harness.py")
    source = json.loads((runs / "synthetic-a2a-input.yaml").read_text(encoding="utf-8"))
    source = module.validate_source(source)
    baseline_scenario = copy.deepcopy(source["scenarios"][0])

    fresh = [run_fresh_copy(package, "A"), run_fresh_copy(package, "B")]
    saved = {
        "input_sha256": sha256(runs / "synthetic-a2a-input.yaml"),
        "results_sha256": sha256(runs / "synthetic-a2a-results.yaml"),
        "summary_sha256": sha256(runs / "synthetic-a2a-summary.md"),
    }
    fresh_equal = fresh[0]["input_sha256"] == fresh[1]["input_sha256"] == saved["input_sha256"]
    results_equal = fresh[0]["results_sha256"] == fresh[1]["results_sha256"] == saved["results_sha256"]
    summary_equal = fresh[0]["summary_sha256"] == fresh[1]["summary_sha256"] == saved["summary_sha256"]

    attacks: list[dict] = []
    add_v = lambda aid, target, expected, fn: attacks.append(verdict_attack(module, source, baseline_scenario, aid, target, expected, fn))
    add_s = lambda aid, target, expected, fn: attacks.append(source_attack(module, source, aid, target, expected, fn))

    add_v("AT-CARD-01", "forged Card signature", ["FAIL"], lambda raw, src: raw["card"].__setitem__("signature", "forged"))
    def card_actor(raw, src):
        raw["card"]["agent_id"] = "agent-evil"
        resign_card(module, raw, src)
    add_v("AT-CARD-02", "validly signed Card actor mismatches delegation/authority", ["FAIL"], card_actor)
    def unsafe_endpoint(raw, src):
        raw["card"]["endpoint"] = "https://127.0.0.1/a2a"
        resign_card(module, raw, src)
    add_v("AT-CARD-03", "validly signed unsafe Card endpoint", ["FAIL"], unsafe_endpoint)
    add_v("AT-CARD-04", "Card cache digest mismatch", ["FAIL"], lambda raw, src: raw["cache"].__setitem__("card_digest", "0" * 64))

    add_v("AT-AUTH-01", "expired authority", ["FAIL"], lambda raw, src: src["authority_store"]["auth-produce"].__setitem__("expires", "2026-09-29T00:00:00Z"))
    add_v("AT-AUTH-02", "wrong authority actor", ["FAIL"], lambda raw, src: src["authority_store"]["auth-produce"].__setitem__("actor", "agent-evil"))
    add_v("AT-AUTH-03", "wrong authority action", ["FAIL"], lambda raw, src: src["authority_store"]["auth-produce"].__setitem__("action", "delete"))
    add_v("AT-AUTH-04", "wrong authority object", ["FAIL"], lambda raw, src: src["authority_store"]["auth-produce"].__setitem__("object", "payment"))
    add_v("AT-AUTH-05", "revoked authority", ["FAIL"], lambda raw, src: src["authority_store"]["auth-produce"].__setitem__("status", "REVOKED"))
    add_v("AT-AUTH-06", "untrusted approver", ["FAIL"], lambda raw, src: src["authority_store"]["auth-produce"].__setitem__("approver", "agent-good"))

    add_v("AT-ART-01", "artifact content changes after digest/signature", ["FAIL"], lambda raw, src: raw["artifact"]["content"].__setitem__("amount", 101))
    def signed_wrong_content(raw, src):
        raw["artifact"]["content"]["unit"] = "USD"
        resign_artifact(module, raw, src)
    add_v("AT-ART-02", "valid signature over business-wrong content", ["FAIL"], signed_wrong_content)
    def revoked_artifact_signer(raw, src):
        resign_artifact(module, raw, src, signer="issuer-colluder")
    add_v("AT-ART-03", "valid signature from revoked artifact signer", ["FAIL"], revoked_artifact_signer)
    def narrow_signed_fields(raw, src):
        raw["artifact"]["signed_fields"] = ["artifact_id"]
        resign_artifact(module, raw, src)
    add_v("AT-ART-04", "narrow Artifact signed_fields", ["FAIL"], narrow_signed_fields)
    def wrong_task(raw, src):
        raw["artifact"]["task_id"] = "task-other"
        resign_artifact(module, raw, src)
    add_v("AT-ART-05", "Artifact bound to another Task", ["FAIL"], wrong_task)
    def missing_provenance(raw, src):
        raw["artifact"]["provenance"] = []
        resign_artifact(module, raw, src)
    add_v("AT-ART-06", "Artifact provenance removed", ["FAIL"], missing_provenance)

    def terminal_regression(raw, src):
        raw["events"].append({"event_id":"e4","sequence":4,"task_id":"task-001","state_version":4,"protocol_state":"WORKING"})
        raw["task_snapshot"].update(current_state="WORKING", state_version=4)
    add_v("AT-STATE-01", "terminal COMPLETED regresses to WORKING", ["FAIL"], terminal_regression)
    add_v("AT-STATE-02", "unknown protocol enum", ["SCHEMA_REJECT"], lambda raw, src: raw["events"][-1].__setitem__("protocol_state", "ALIEN"))
    add_v("AT-STATE-03", "Task snapshot differs from terminal Event", ["FAIL"], lambda raw, src: raw["task_snapshot"].__setitem__("current_state", "FAILED"))
    def working_but_stopped(raw, src):
        raw["events"] = raw["events"][:2]
        raw["task_snapshot"].update(current_state="WORKING", state_version=2)
    add_v("AT-D21-01", "nonterminal protocol but stopped and accepted", ["REVIEW_REQUIRED", "FAIL"], working_but_stopped)
    add_v("AT-D21-02", "delivery not visible", ["FAIL"], lambda raw, src: raw["acceptance_evidence"].__setitem__("delivery_visibility", "NOT_VISIBLE"))
    add_v("AT-STOP-01", "missing stop receipt", ["REVIEW_REQUIRED", "FAIL"], lambda raw, src: raw["execution"]["stop_receipt"].update(status="MISSING", receipt_id="NONE"))
    add_v("AT-STOP-02", "UNKNOWN authoritative readback", ["REVIEW_REQUIRED", "FAIL"], lambda raw, src: raw["execution"]["authoritative_readback"].__setitem__("worker", "UNKNOWN"))
    add_v("AT-STOP-03", "dummy receipt claims VERIFIED", ["REVIEW_REQUIRED", "FAIL"], lambda raw, src: raw["execution"]["stop_receipt"].update(status="VERIFIED", receipt_id="NONE"))

    add_s("AT-SCHEMA-01", "unknown root field", ["SCHEMA_REJECT"], lambda src: src.__setitem__("is_valid", True))
    add_s("AT-SCHEMA-02", "unknown schema version", ["SCHEMA_REJECT"], lambda src: src.__setitem__("schema_version", "c18.synthetic.v999"))
    add_s("AT-SCHEMA-03", "unknown mutation", ["SCHEMA_REJECT"], lambda src: src["scenarios"][0]["mutations"].append("mystery_attack"))
    def unknown_effect(src):
        src["base_execution"]["effect_ledger"] = [{"effect_id":"effect-x","status":"ALIEN","confirmed_external_write":False}]
    add_s("AT-SCHEMA-04", "unknown effect enum", ["SCHEMA_REJECT"], unknown_effect)
    def duplicate_scenario(src):
        src["scenarios"] = [copy.deepcopy(src["scenarios"][0]), copy.deepcopy(src["scenarios"][0])]
    add_s("AT-ID-01", "duplicate scenario/task/trial identity", ["SCHEMA_REJECT"], duplicate_scenario)
    def duplicate_same_event(raw, src):
        raw["events"].append(copy.deepcopy(raw["events"][-1]))
    add_v("AT-ID-02", "same event ID and same payload is idempotent", ["PASS"], duplicate_same_event)
    def duplicate_conflict(raw, src):
        raw["events"].append({"event_id":"e3","sequence":4,"task_id":"task-001","state_version":4,"protocol_state":"FAILED"})
    add_v("AT-ID-03", "same event ID with different payload", ["FAIL"], duplicate_conflict)

    def no_authority_high_trust(raw, src):
        raw["authority_evidence_ref"] = "missing-auth"
        raw["artifact"]["authority_evidence_ref"] = "missing-auth"
        raw["trust_evidence"]["score"] = 100
        resign_artifact(module, raw, src)
    add_v("AT-HARD-01", "maximum trust cannot compensate missing authority", ["FAIL"], no_authority_high_trust)
    def hard_plus_unknown(raw, src):
        raw["authority_evidence_ref"] = "missing-auth"
        raw["artifact"]["authority_evidence_ref"] = "missing-auth"
        raw["execution"]["authoritative_readback"]["worker"] = "UNKNOWN"
        resign_artifact(module, raw, src)
    add_v("AT-HARD-02", "authority hard failure is not averaged with UNKNOWN", ["FAIL"], hard_plus_unknown)

    def d22_self_asserted(src):
        src["scenarios"] = [copy.deepcopy(src["scenarios"][0])]
        sc = src["scenarios"][0]
        sc["layer"] = "representative_real_world"
        sc["real_world_evidence_id"] = "rw-self"
        sc["real_world_source_id"] = "self-asserted-source"
        src["data_origin"] = "representative_real_world"
        src["representative_real_world_executed"] = True
        src["real_world_evidence_manifest"] = {
            "rw-self": {
                "verified": True,
                "origin": "representative_real_world",
                "source_id": "self-asserted-source",
                "run_id": "C18-S01-T1",
            }
        }
    add_s("AT-D22-01", "synthetic fixture relabeled with self-asserted real-world manifest", ["SCHEMA_REJECT", "REVIEW_REQUIRED", "FAIL"], d22_self_asserted)

    failures = [item["attack_id"] for item in attacks if not item["control_passed"]]
    output = {
        "review_id": "C18-v2-independent-reproduction-20260930",
        "chapter_id": "C18",
        "reviewer_role": "non_author_independent_reviewer",
        "executed_on": "2026-09-30",
        "scope": "offline synthetic fresh-temp rebuild plus independent state-boundary attacks",
        "author_files_modified": False,
        "network_used_by_harness": False,
        "real_credentials_used": False,
        "external_side_effects": 0,
        "fresh_temp_runs": fresh,
        "saved_artifact_hashes": saved,
        "fresh_temp_input_equals_each_other_and_saved": fresh_equal,
        "fresh_temp_results_equals_each_other_and_saved": results_equal,
        "fresh_temp_summary_equals_each_other_and_saved": summary_equal,
        "attack_count": len(attacks),
        "attack_control_pass_count": len(attacks) - len(failures),
        "attack_control_fail_count": len(failures),
        "failed_attack_ids": failures,
        "attacks": attacks,
        "gate_implication": {
            "synthetic_machine_control": "FAIL" if failures else "PASS_IN_SYNTHETIC_SCOPE",
            "real_a2a_openclaw_hermes_practice": "REVIEW_REQUIRED",
            "muse_internal_implementation": "NOT_CLAIMED",
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "fresh_equal": fresh_equal and results_equal and summary_equal,
        "attack_count": len(attacks),
        "failed_attack_ids": failures,
        "output": str(output_path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
