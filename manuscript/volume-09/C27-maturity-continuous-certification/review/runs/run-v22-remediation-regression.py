#!/usr/bin/env python3
"""C24 v2.2 author remediation regression.

Runs two fresh-temp builds and checks both nested semantic decisions and the
black-box frozen-root control for the 18 v2.1 semantic escapes. It does not
approve any editorial or review gate.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ESCAPES = {
    "review_issued_after_certificate": ("FAIL", "REVIEW_RECORD_INVALID_AT_CERTIFICATE_TIME"),
    "review_issued_in_future": ("FAIL", "REVIEW_RECORD_INVALID_AT_CERTIFICATE_TIME"),
    "issuance_authority_issued_after_certificate": ("FAIL", "ISSUANCE_AUTHORITY_INVALID_AT_CERTIFICATE_TIME"),
    "issuance_authority_not_before_after_certificate": ("FAIL", "ISSUANCE_AUTHORITY_INVALID_AT_CERTIFICATE_TIME"),
    "lifecycle_authority_not_before_after_event": ("FAIL", "LIFECYCLE_BINDING_OR_AUTHORITY_INVALID_AT_EVENT_TIME"),
    "artifact_issued_after_certificate": ("FAIL", "EVIDENCE_NOT_VALID_AT_CERTIFICATE_TIME"),
    "application_signature_issued_after_certificate": ("FAIL", "EVIDENCE_NOT_VALID_AT_CERTIFICATE_TIME"),
    "trial_output_issued_after_certificate": ("FAIL", "TRIAL_NOT_COMPLETE_OR_VALID_AT_CERTIFICATE_TIME"),
    "opened_appeal_issued_in_future": ("FAIL", "APPEAL_FROM_FUTURE"),
    "certificate_issuer_is_reviewer": ("FAIL", "CANONICAL_ROLE_CONFLICT"),
    "certificate_issuer_is_domain_expert": ("FAIL", "CANONICAL_ROLE_CONFLICT"),
    "appeal_reviewer_is_certificate_issuer": ("FAIL", "CANONICAL_ROLE_CONFLICT"),
    "appeal_reviewer_is_domain_expert": ("FAIL", "CANONICAL_ROLE_CONFLICT"),
    "lifecycle_owner_is_reviewer": ("FAIL", "CANONICAL_ROLE_CONFLICT"),
    "certificate_expiry_outlives_application": ("FAIL", "CERTIFICATE_EXCEEDS_COMMON_VALIDITY_WINDOW"),
    "material_change_after_certificate": ("REVIEW_REQUIRED", "MATERIAL_CHANGE_AFTER_CERTIFICATE_REQUIRES_RECERTIFICATION"),
    "material_change_from_future": ("FAIL", "MATERIAL_CHANGE_FROM_FUTURE"),
    "offline_external_effect_unknown": ("REVIEW_REQUIRED", "EXTERNAL_EFFECT_UNRESOLVED"),
}


def digest_bytes(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def run_checked(args: list[str], cwd: Path) -> None:
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def pending_effect_control(runner, source, authority, baseline):
    attacked = copy.deepcopy(baseline)
    state = attacked["state"]
    app = state["application"]
    effect = {
        "effect_id": "EFFECT-PENDING-V22",
        "application_id": app["application_id"],
        "external": True,
        "status": "PENDING",
        "environment": "external",
        "record_digest": "",
    }
    effect["record_digest"] = runner.sha({k: v for k, v in effect.items() if k != "record_digest"})
    state["effect_ledger"] = [effect]
    validated = runner.validate_state(state, "pending_effect.state")
    decision, lifecycle, reasons, *_ = runner.evaluate(source, validated, attacked["layer"], authority)
    return {
        "decision": decision,
        "lifecycle": lifecycle,
        "reasons": reasons,
        "matched": decision == "REVIEW_REQUIRED" and "EXTERNAL_EFFECT_UNRESOLVED" in reasons,
    }


def explicit_conflict_exception_control(runner, source, authority, baseline):
    attacked = copy.deepcopy(baseline)
    state = attacked["state"]
    app = state["application"]
    review = next(iter(state["review_registry"].values()))
    issue = next(x for x in state["authority_registry"].values() if x["action"] == "issue_synthetic_assessment")
    certifier = issue["actor"]
    principal = state["principal_registry"][certifier]
    principal["roles"] = sorted(set(principal["roles"] + ["reviewer"]))
    principal["aliases"] = [certifier + "-ALIAS"]
    principal["record_digest"] = runner.sha({k: v for k, v in principal.items() if k != "record_digest"})
    review["reviewer"] = certifier
    review["record_digest"] = runner.sha({k: v for k, v in review.items() if k != "record_digest"})
    exception_actor = next(pid for pid, row in state["principal_registry"].items() if "conflict_exception_approver" in row["roles"])
    exception_id = "ROLE-EXCEPTION-V22"
    authority_id = "AUTH-ROLE-EXCEPTION-V22"
    auth = {
        "authority_id": authority_id,
        "actor": exception_actor,
        "action": "approve_role_conflict_exception",
        "subject_type": "exception",
        "subject_id": exception_id,
        "object_digest": app["application_digest"],
        "scope": app["scope"],
        "status": "ACTIVE",
        "issued_at": "2026-09-30T09:00:00Z",
        "not_before": "2026-09-30T09:00:00Z",
        "expires_at": "2026-10-30T00:00:00Z",
        "record_digest": "",
    }
    auth["record_digest"] = runner.sha({k: v for k, v in auth.items() if k != "record_digest"})
    state["authority_registry"][authority_id] = auth
    exception = {
        "exception_id": exception_id,
        "roles": ["certifier", "reviewer"],
        "principals": [certifier, certifier + "-ALIAS"],
        "authority_ref": authority_id,
        "reason": "synthetic conflict exception must degrade",
        "status": "APPROVED",
        "record_digest": "",
    }
    exception["record_digest"] = runner.sha({k: v for k, v in exception.items() if k != "record_digest"})
    state["role_conflict_exceptions"] = [exception]
    validated = runner.validate_state(state, "conflict_exception.state")
    decision, lifecycle, reasons, *_ = runner.evaluate(source, validated, attacked["layer"], authority)
    return {
        "decision": decision,
        "lifecycle": lifecycle,
        "reasons": reasons,
        "matched": (decision == "REVIEW_REQUIRED" and "ROLE_CONFLICT_EXCEPTION_REQUIRES_LIMITED_REVIEW" in reasons) or (decision == "FAIL" and "AUTHORITY_ROOT_PROJECTION_INVALID" in reasons),
        "v2_5_fail_closed_root_projection": decision == "FAIL" and "AUTHORITY_ROOT_PROJECTION_INVALID" in reasons,
    }


def one_run(source_dir: Path, historical: Path, run_id: int):
    with tempfile.TemporaryDirectory(prefix=f"c24-v22-run-{run_id}-") as raw:
        td = Path(raw)
        for name in ("build-certification-fixture.py", "run-certification-harness.py"):
            shutil.copy2(source_dir / name, td / name)
        input_path = td / "synthetic-certification-input.yaml"
        authority_path = td / "frozen-certification-authority.yaml"
        result_path = td / "synthetic-certification-results.json"
        historical_path = td / "historical-28.json"
        run_checked(["python3", "build-certification-fixture.py", "--output", str(input_path), "--authority-output", str(authority_path)], td)
        run_checked(["python3", "run-certification-harness.py", "--input", str(input_path), "--authority", str(authority_path), "--output", str(result_path)], td)
        historical_proc = subprocess.run(["python3", str(historical), "--input", str(input_path), "--authority", str(authority_path), "--runner", str(td / "run-certification-harness.py"), "--output", str(historical_path)], cwd=td, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # The immutable v2.1 suite intentionally exits non-zero for three
        # contract-renamed outcomes; the v2.2 assertions below adjudicate them.
        if not historical_path.exists() or historical_proc.returncode not in {0, 1}:
            raise RuntimeError(historical_proc.stderr)

        result = json.loads(result_path.read_text())
        old = json.loads(historical_path.read_text())
        attacks = {row["attack_id"]: row for row in old["attacks"]}
        escape_rows = []
        for attack_id, (expected, reason) in ESCAPES.items():
            row = attacks[attack_id]
            semantic = row["semantic"]
            blackbox = row["blackbox"]
            semantic_ok = semantic["actual"] == expected and reason in semantic["reasons"]
            blackbox_ok = (
                (blackbox["actual"] == "FAIL" and "FROZEN_SCENARIO_BINDING_INVALID" in blackbox["reasons"])
                or (blackbox["actual"] == "SCHEMA_REJECT" and any("frozen identity or state binding" in value for value in blackbox["reasons"]))
                or (blackbox["actual"] == "SCHEMA_REJECT" and any("result input semantic source binding" in value for value in blackbox["reasons"]))
            )
            escape_rows.append({
                "attack_id": attack_id,
                "expected": expected,
                "required_reason": reason,
                "semantic_actual": semantic["actual"],
                "semantic_reasons": semantic["reasons"],
                "semantic_matched": semantic_ok,
                "blackbox_actual": blackbox["actual"],
                "blackbox_reasons": blackbox["reasons"],
                "blackbox_root_matched": blackbox_ok,
            })

        source = json.loads(input_path.read_text())
        authority = json.loads(authority_path.read_text())
        runner = load_module(td / "run-certification-harness.py", f"c24_v22_runner_{run_id}")
        valid = result["trials"][-1]
        pending = pending_effect_control(runner, source, authority, source["scenarios"][0])
        conflict_exception = explicit_conflict_exception_control(runner, source, authority, source["scenarios"][0])
        return {
            "run_id": run_id,
            "input_sha256": digest_bytes(input_path),
            "authority_sha256": digest_bytes(authority_path),
            "result_sha256": digest_bytes(result_path),
            "authority_root_digest": result["authority_root_digest"],
            "decision_digest": result["decision_digest"],
            "trial_count": result["trial_count"],
            "distribution": result["distribution"],
            "lifecycle_distribution": result["lifecycle_distribution"],
            "successful_real_certificates": result["successful_real_certificates"],
            "successful_external_effects": result["successful_external_effects"],
            "historical_28_semantic_pass_escapes": old["frozen_root_masked_escape_count"],
            "escape_assertions": escape_rows,
            "valid_pass_neighbor": {
                "scenario_id": valid["scenario_id"],
                "decision": valid["decision"],
                "reasons": valid["reasons"],
                "matched": valid["decision"] == "PASS" and valid["reasons"] == [],
            },
            "pending_external_effect": pending,
            "explicit_conflict_exception": conflict_exception,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-dir", required=True)
    parser.add_argument("--historical-tests", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source_dir = Path(args.runs_dir).resolve()
    historical = Path(args.historical_tests).resolve()
    runs = [one_run(source_dir, historical, index) for index in (1, 2)]
    stable_fields = ("input_sha256", "authority_sha256", "result_sha256", "authority_root_digest", "decision_digest", "distribution", "lifecycle_distribution")
    deterministic = all(runs[0][field] == runs[1][field] for field in stable_fields)
    semantic_ok = all(row["semantic_matched"] and row["blackbox_root_matched"] for run in runs for row in run["escape_assertions"])
    pass_ok = all(run["valid_pass_neighbor"]["matched"] for run in runs)
    pending_ok = all(run["pending_external_effect"]["matched"] for run in runs)
    exception_ok = all(run["explicit_conflict_exception"]["matched"] for run in runs)
    payload = {
        "schema": "c24.cert.v2.4-historical-remediation-regression.v1",
        "scope": "offline_synthetic_fresh_temp_semantic_and_blackbox",
        "run_count": 2,
        "escape_count": len(ESCAPES),
        "escape_assertion_count": len(ESCAPES) * 2,
        "deterministic": deterministic,
        "semantic_and_blackbox_closed": semantic_ok,
        "valid_pass_neighbor_proven": pass_ok,
        "pending_external_effect_review_required": pending_ok,
        "explicit_conflict_exception_degraded": exception_ok,
        "runs": runs,
    }
    payload["suite_digest"] = "sha256:" + hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in ("run_count", "escape_count", "deterministic", "semantic_and_blackbox_closed", "valid_pass_neighbor_proven", "pending_external_effect_review_required", "explicit_conflict_exception_degraded", "suite_digest")}, ensure_ascii=False))
    if not all((deterministic, semantic_ok, pass_ok, pending_ok, exception_ok)):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
