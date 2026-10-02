#!/usr/bin/env python3
"""C23 v2.8 regression for a non-bypassable semantic-replay verifier.

This suite treats every importable result-acceptance path as public attack
surface.  A callable may accept a persisted result only when it also consumes
the frozen source and authority root and deterministically replays semantics.
"""
from __future__ import annotations

import argparse
import copy
import functools
import importlib.util
import inspect
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location("c23_v28_runner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--authority-root", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--runner", required=True)
    p.add_argument("--verifier", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()

    r = load(Path(a.runner))
    source_text = Path(a.input).read_text()
    root_text = Path(a.authority_root).read_text()
    result_text = Path(a.result).read_text()
    source = r.strict_json_loads(source_text)
    root = r.strict_json_loads(root_text)
    persisted = r.strict_json_loads(result_text)
    r.verify_result(copy.deepcopy(persisted), copy.deepcopy(root), copy.deepcopy(source))

    fail_row = next(x for x in persisted["trials"] if x["derived"]["verdict"] == "FAIL")
    rr_row = next(x for x in persisted["trials"] if x["derived"]["verdict"] == "REVIEW_REQUIRED")
    pass_row = next(x for x in persisted["trials"] if x["derived"]["verdict"] == "PASS")
    attacks: list[dict] = []
    controls: list[dict] = []

    def resign(result: dict) -> None:
        result["distribution"] = dict(sorted(Counter(x["derived"]["verdict"] for x in result["trials"]).items()))
        result["accepted_real_claim_count"] = sum(x["derived"]["accepted_real_claim_count"] for x in result["trials"])
        result["external_effect_count"] = sum(x["derived"]["external_effect_count"] for x in result["trials"])
        result["decision_digest"] = r.digest({k: v for k, v in result.items() if k != "decision_digest"})

    def changed(scenario_id: str, **values) -> dict:
        candidate = copy.deepcopy(persisted)
        row = next(x for x in candidate["trials"] if x["scenario_id"] == scenario_id)
        row["derived"].update(values)
        resign(candidate)
        return candidate

    forged_fail = changed(fail_row["scenario_id"], verdict="PASS", reasons=[])
    forged_rr = changed(rr_row["scenario_id"], verdict="PASS", reasons=[])

    def reject(test_id: str, family: str, fn) -> None:
        observed, message = "ACCEPTED", ""
        try:
            fn()
        except Exception as exc:
            observed, message = "REJECT", f"{type(exc).__name__}: {exc}"
        attacks.append({
            "test_id": test_id,
            "family": family,
            "observed": observed,
            "secure_expected_outcomes": ["REJECT"],
            "secure_contract_passed": observed == "REJECT",
            "escape": observed != "REJECT",
            "message": message,
        })

    # Exact v2.7 blockers: direct import and direct call must be impossible.
    reject("V28-U01_DIRECT_OLD_ENVELOPE_FAIL_TO_PASS", "module-entrypoint-bypass", lambda: getattr(r, "_verify_result_envelope")(forged_fail, root))
    reject("V28-U02_DIRECT_OLD_ENVELOPE_RR_TO_PASS", "module-entrypoint-bypass", lambda: getattr(r, "_verify_result_envelope")(forged_rr, root))

    def reflected_low_arity(candidate: dict) -> None:
        for name, obj in vars(r).items():
            if not callable(obj) or not any(token in name.lower() for token in ("verify", "envelope", "accept")):
                continue
            try:
                inspect.signature(obj).bind(candidate, root)
            except (TypeError, ValueError):
                continue
            obj(candidate, root)
            return
        raise AttributeError("no importable result acceptance callable binds result+root without source")

    reject("V28-03_REFLECTION_LOW_ARITY_FAIL", "reflection-bypass", lambda: reflected_low_arity(forged_fail))
    reject("V28-04_REFLECTION_LOW_ARITY_RR", "reflection-bypass", lambda: reflected_low_arity(forged_rr))
    reject("V28-05_ALIAS_FAIL_TO_PASS", "alias-bypass", lambda: r.verify_result(forged_fail, root, source))
    reject("V28-06_MODULE_DICT_ALIAS_RR_TO_PASS", "alias-bypass", lambda: r.__dict__["verify_result"](forged_rr, root, source))
    reject("V28-07_PARTIAL_MISSING_SOURCE", "partial-argument-bypass", lambda: functools.partial(r.verify_result, forged_fail, root)())
    reject("V28-08_PARTIAL_COMPLETE_BUT_FORGED", "partial-argument-bypass", lambda: functools.partial(r.verify_result, forged_fail, root, source)())
    reject("V28-09_POSITIONAL_SOURCE_OMITTED", "argument-bypass", lambda: r.verify_result(forged_fail, root))
    reject("V28-10_SOURCE_NONE", "argument-bypass", lambda: r.verify_result(forged_fail, root, None))
    reject("V28-11_ROOT_NONE", "argument-bypass", lambda: r.verify_result(forged_fail, None, source))
    reject("V28-12_ROOT_SOURCE_SWAPPED", "argument-bypass", lambda: r.verify_result(forged_fail, source, root))
    reject("V28-13_FAIL_REASON_AND_DIGEST_REWRITE", "coherent-result-rewrite", lambda: r.verify_result(changed(fail_row["scenario_id"], reasons=["FORGED.V28"]), root, source))
    reject("V28-14_PASS_COUNT_AND_DIGEST_REWRITE", "coherent-result-rewrite", lambda: r.verify_result(changed(pass_row["scenario_id"], external_effect_count=1), root, source))

    def cross_case_result() -> None:
        candidate = copy.deepcopy(persisted)
        candidate["trials"][0].update({k: candidate["trials"][1][k] for k in ("case_record_id", "task_id", "trial_id", "run_id", "evidence_id")})
        resign(candidate)
        r.verify_result(candidate, root, source)

    reject("V28-15_CROSS_CASE_RESULT_TRANSPLANT", "cross-case", cross_case_result)

    def cross_case_source() -> None:
        candidate = copy.deepcopy(source)
        candidate["scenarios"][0]["raw_state"]["source_ref"] = candidate["scenarios"][1]["raw_state"]["source_ref"]
        r.verify_result(persisted, root, candidate)

    reject("V28-16_CROSS_CASE_SOURCE_TRANSPLANT", "cross-case", cross_case_source)

    def source_content_resealed() -> None:
        candidate = copy.deepcopy(source)
        record = candidate["registries"]["source_registry"][0]
        record["private_content"] = {"private_case": "FORGED.V28"}
        record["private_content_digest"] = r.digest(record["private_content"])
        record["record_digest"] = r.digest({k: v for k, v in record.items() if k != "record_digest"})
        r.verify_result(persisted, root, candidate)

    reject("V28-17_SOURCE_RESEALED_ROOT_STALE", "source-root-binding", source_content_resealed)

    def duplicate_result_key() -> None:
        hostile = result_text.replace('"verdict": "PASS"', '"verdict": "FAIL",\n        "verdict": "PASS"', 1)
        parsed = r.strict_json_loads(hostile)
        r.verify_result(parsed, root, source)

    reject("V28-18_RESULT_DUPLICATE_KEY", "parser-boundary", duplicate_result_key)

    def cli_forged() -> None:
        with tempfile.TemporaryDirectory(prefix="c23-v28-cli-") as td:
            path = Path(td) / "forged-result.json"
            path.write_text(json.dumps(forged_fail, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            proc = subprocess.run([
                "python3", a.verifier,
                "--result", str(path),
                "--authority-root", a.authority_root,
                "--input", a.input,
            ], capture_output=True, text=True)
            if proc.returncode:
                raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    reject("V28-19_CLI_FAIL_TO_PASS", "cli-semantic-replay", cli_forged)

    def callable_copy_bypass() -> None:
        alias = getattr(r, "verify_result")
        copied = functools.partial(alias, result=forged_rr, authority_root=root)
        copied(source=source)

    reject("V28-20_KEYWORD_PARTIAL_RR_TO_PASS", "partial-argument-bypass", callable_copy_bypass)

    def control(test_id: str, fn) -> None:
        observed, message = "PASS", ""
        try:
            fn()
        except Exception as exc:
            observed, message = "REJECT", f"{type(exc).__name__}: {exc}"
        controls.append({"test_id": test_id, "observed": observed, "expected": "PASS", "passed": observed == "PASS", "message": message})

    control("V28-C01_PERSISTED_STRONG_VERIFY", lambda: r.verify_result(copy.deepcopy(persisted), copy.deepcopy(root), copy.deepcopy(source)))
    control("V28-C02_ALIAS_STRONG_VERIFY", lambda: getattr(r, "verify_result")(copy.deepcopy(persisted), copy.deepcopy(root), copy.deepcopy(source)))
    control("V28-C03_PARTIAL_WITH_SOURCE_ROOT", lambda: functools.partial(r.verify_result, copy.deepcopy(persisted), copy.deepcopy(root), copy.deepcopy(source))())
    control("V28-C04_DETERMINISTIC_REPLAY", lambda: r.verify_result(r.evaluate(copy.deepcopy(source), copy.deepcopy(root)), copy.deepcopy(root), copy.deepcopy(source)))

    def cli_control() -> None:
        proc = subprocess.run([
            "python3", a.verifier,
            "--result", a.result,
            "--authority-root", a.authority_root,
            "--input", a.input,
        ], capture_output=True, text=True)
        if proc.returncode:
            raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    control("V28-C05_CLI_STRONG_VERIFY", cli_control)

    escapes = [x for x in attacks if x["escape"]]
    payload = {
        "schema_version": "c23.v2.8.author-remediation-regression.v1",
        "baseline_distribution": persisted["distribution"],
        "baseline_decision_digest": persisted["decision_digest"],
        "attack_count": len(attacks),
        "secure_attack_count": len(attacks) - len(escapes),
        "escape_count": len(escapes),
        "escape_ids": [x["test_id"] for x in escapes],
        "positive_control_count": len(controls),
        "positive_control_pass_count": sum(x["passed"] for x in controls),
        "tests": attacks,
        "positive_controls": controls,
    }
    payload["suite_digest"] = r.digest(
        [(x["test_id"], x["observed"], x["message"], x["secure_contract_passed"]) for x in attacks]
        + [(x["test_id"], x["observed"], x["message"], x["passed"]) for x in controls]
    )
    Path(a.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: payload[k] for k in ("attack_count", "secure_attack_count", "escape_count", "positive_control_count", "positive_control_pass_count", "suite_digest")}, ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"] == len(controls) else 1


if __name__ == "__main__":
    raise SystemExit(main())
