#!/usr/bin/env python3
"""C23 v2.8 non-author final entrypoint and replay-boundary attacks."""
from __future__ import annotations

import argparse
import ast
import copy
import functools
import hashlib
import importlib.util
import inspect
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def file_sha(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--authority-root", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--runner", required=True)
    p.add_argument("--verifier", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()

    runner_path = Path(a.runner)
    r = load(runner_path, "c23_v28_independent_final")
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

    def attack(test_id: str, family: str, fn, expected_reject=True) -> None:
        observed, message = "ACCEPTED", ""
        try:
            fn()
        except Exception as exc:
            observed, message = "REJECT", f"{type(exc).__name__}: {exc}"
        secure = observed == "REJECT" if expected_reject else observed == "ACCEPTED"
        attacks.append({
            "test_id": test_id,
            "family": family,
            "observed": observed,
            "secure_expected": "REJECT" if expected_reject else "ACCEPTED",
            "secure_contract_passed": secure,
            "escape": not secure,
            "message": message,
        })

    # Old envelope verifier must be absent from every fresh module view.
    attack("I01_OLD_PRIVATE_GETATTR", "removed-entrypoint", lambda: getattr(r, "_verify_result_envelope")(forged_fail, root))
    attack("I02_OLD_PRIVATE_MODULE_DICT", "removed-entrypoint", lambda: r.__dict__["_verify_result_envelope"](forged_rr, root))

    def reflected_old_name():
        matches = [name for name in vars(r) if "verify_result_envelope" in name]
        if not matches:
            raise AttributeError("old envelope verifier absent")
        vars(r)[matches[0]](forged_fail, root)

    attack("I03_OLD_PRIVATE_REFLECTION", "removed-entrypoint", reflected_old_name)

    def ast_old_function():
        tree = ast.parse(runner_path.read_text())
        names = [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        if "_verify_result_envelope" not in names:
            raise AttributeError("old envelope function absent from source AST")
        raise RuntimeError("old envelope function still declared")

    attack("I04_OLD_PRIVATE_SOURCE_AST", "removed-entrypoint", ast_old_function)

    def code_object_old_reference():
        functions = [obj for obj in vars(r).values() if inspect.isfunction(obj)]
        found = [obj.__name__ for obj in functions if "_verify_result_envelope" in obj.__code__.co_names]
        if not found:
            raise AttributeError("old envelope name absent from live code objects")
        raise RuntimeError("old envelope name retained by " + ",".join(found))

    attack("I05_OLD_PRIVATE_CODE_OBJECT", "removed-entrypoint", code_object_old_reference)

    def fresh_import_old_entry():
        fresh = load(runner_path, "c23_v28_independent_second_import")
        getattr(fresh, "_verify_result_envelope")(forged_fail, root)

    attack("I06_OLD_PRIVATE_FRESH_IMPORT", "removed-entrypoint", fresh_import_old_entry)

    # Enumerate every module-level callable whose name could imply acceptance.
    def low_arity_acceptor():
        for name, obj in vars(r).items():
            if not callable(obj) or not any(token in name.lower() for token in ("verify", "accept", "envelope")):
                continue
            try:
                inspect.signature(obj).bind(forged_fail, root)
            except (TypeError, ValueError):
                continue
            obj(forged_fail, root)
            return
        raise AttributeError("no result+root acceptance callable")

    attack("I07_REFLECTED_LOW_ARITY_ACCEPTOR", "callable-inventory", low_arity_acceptor)

    def only_strong_acceptor():
        candidates = [name for name, obj in vars(r).items() if callable(obj) and any(t in name.lower() for t in ("verify", "accept", "envelope"))]
        if candidates != ["verify_result"]:
            raise RuntimeError("unexpected acceptance callables: " + repr(candidates))
        raise AttributeError("only verify_result is present and it requires three arguments")

    attack("I08_CALLABLE_INVENTORY_EXACT", "callable-inventory", only_strong_acceptor)

    # Alias, getattr, module-dict, partial and signature-default attacks.
    attack("I09_ALIAS_FORGED_FAIL", "alias-partial", lambda: r.verify_result(forged_fail, root, source))
    attack("I10_GETATTR_FORGED_RR", "alias-partial", lambda: getattr(r, "verify_result")(forged_rr, root, source))
    attack("I11_MODULE_DICT_FORGED_FAIL", "alias-partial", lambda: vars(r)["verify_result"](forged_fail, root, source))
    attack("I12_PARTIAL_MISSING_SOURCE", "alias-partial", lambda: functools.partial(r.verify_result, forged_fail, root)())
    attack("I13_PARTIAL_KEYWORD_MISSING_ROOT", "alias-partial", lambda: functools.partial(r.verify_result, result=forged_fail, source=source)())
    attack("I14_COMPLETE_PARTIAL_FORGED", "alias-partial", lambda: functools.partial(r.verify_result, forged_rr, root, source)())

    def default_values_absent():
        if r.verify_result.__defaults__ is None and r.verify_result.__kwdefaults__ is None:
            raise AttributeError("verify_result has no default arguments")
        r.verify_result(forged_fail, root)

    attack("I15_SIGNATURE_DEFAULTS_ABSENT", "signature-boundary", default_values_absent)
    attack("I16_ROOT_NONE", "signature-boundary", lambda: r.verify_result(forged_fail, None, source))
    attack("I17_SOURCE_NONE", "signature-boundary", lambda: r.verify_result(forged_fail, root, None))
    attack("I18_ROOT_SOURCE_SWAPPED", "signature-boundary", lambda: r.verify_result(forged_fail, source, root))

    # Result/source/case transplant and coherent digest resealing.
    def result_identity_transplant():
        candidate = copy.deepcopy(persisted)
        candidate["trials"][0].update({k: candidate["trials"][1][k] for k in ("case_record_id", "task_id", "trial_id", "run_id", "evidence_id")})
        resign(candidate)
        r.verify_result(candidate, root, source)

    attack("I19_CROSS_CASE_RESULT_TRANSPLANT", "cross-case-source-root", result_identity_transplant)

    def source_case_transplant():
        candidate = copy.deepcopy(source)
        candidate["scenarios"][0]["raw_state"] = copy.deepcopy(candidate["scenarios"][1]["raw_state"])
        r.verify_result(persisted, root, candidate)

    attack("I20_CROSS_CASE_SOURCE_TRANSPLANT", "cross-case-source-root", source_case_transplant)

    def source_registry_reseal():
        candidate = copy.deepcopy(source)
        record = candidate["registries"]["source_registry"][0]
        record["private_content"] = {"private_case": "FORGED.INDEPENDENT.V28"}
        record["private_content_digest"] = r.digest(record["private_content"])
        record["record_digest"] = r.digest({k: v for k, v in record.items() if k != "record_digest"})
        r.verify_result(persisted, root, candidate)

    attack("I21_SOURCE_CONTENT_RESEALED_OLD_ROOT", "cross-case-source-root", source_registry_reseal)

    def result_full_reseal():
        candidate = changed(fail_row["scenario_id"], verdict="PASS", reasons=[], accepted_real_claim_count=0, external_effect_count=0)
        r.verify_result(candidate, root, source)

    attack("I22_RESULT_FULL_DIGEST_RESEAL", "cross-case-source-root", result_full_reseal)

    def make_equivalent_new_trio():
        doc = copy.deepcopy(source)
        new_root = copy.deepcopy(root)
        # Reversing a registry list changes the pinned root bytes while keeping
        # the closed-world record set and semantics equivalent.
        doc["registries"]["source_registry"].reverse()
        new_root["registries"] = copy.deepcopy(doc["registries"])
        new_root["suite_manifest"] = r.suite_manifest(doc["suite"], doc["scenarios"])
        new_root["root_digest"] = r.digest(r.root_payload(new_root))
        old_pin = r.PINNED_AUTHORITY_ROOT_DIGEST
        try:
            r.PINNED_AUTHORITY_ROOT_DIGEST = new_root["root_digest"]
            new_result = r.evaluate(doc, new_root)
        finally:
            r.PINNED_AUTHORITY_ROOT_DIGEST = old_pin
        return doc, new_root, new_result

    def coherent_new_trio_without_pin():
        doc, new_root, new_result = make_equivalent_new_trio()
        r.verify_result(new_result, new_root, doc)

    attack("I23_COHERENT_NEW_TRIO_WITHOUT_PIN", "cross-case-source-root", coherent_new_trio_without_pin)

    def root_only_transplant():
        _, new_root, _ = make_equivalent_new_trio()
        r.verify_result(persisted, new_root, source)

    attack("I24_ROOT_ONLY_TRANSPLANT", "cross-case-source-root", root_only_transplant)

    # CLI must use the same source+root replay contract.
    def cli_forged():
        with tempfile.TemporaryDirectory(prefix="c23-v28-independent-cli-") as td:
            path = Path(td) / "forged.json"
            path.write_text(json.dumps(forged_fail, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            proc = subprocess.run(["python3", a.verifier, "--result", str(path), "--authority-root", a.authority_root, "--input", a.input], capture_output=True, text=True)
            if proc.returncode:
                raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    attack("I25_CLI_FORGED_RESULT", "cli-boundary", cli_forged)

    def cli_missing_input():
        proc = subprocess.run(["python3", a.verifier, "--result", a.result, "--authority-root", a.authority_root], capture_output=True, text=True)
        if proc.returncode:
            raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    attack("I26_CLI_MISSING_SOURCE", "cli-boundary", cli_missing_input)

    # Strict parser boundary.
    def strict_duplicate(text: str, needle: str, replacement: str, kind: str):
        parsed = r.strict_json_loads(text.replace(needle, replacement, 1))
        if kind == "result":
            r.verify_result(parsed, root, source)
        elif kind == "source":
            r.verify_result(persisted, root, parsed)
        else:
            r.verify_result(persisted, parsed, source)

    attack("I27_STRICT_RESULT_DUPLICATE", "duplicate-json", lambda: strict_duplicate(result_text, '"verdict": "FAIL"', '"verdict": "PASS",\n        "verdict": "FAIL"', "result"))
    attack("I28_STRICT_SOURCE_DUPLICATE", "duplicate-json", lambda: strict_duplicate(source_text, '"schema_version": "c23.case.input.v2.7"', '"schema_version": "FORGED",\n  "schema_version": "c23.case.input.v2.7"', "source"))
    attack("I29_STRICT_ROOT_DUPLICATE", "duplicate-json", lambda: strict_duplicate(root_text, '"root_digest":', '"root_digest": "' + "0" * 64 + '",\n  "root_digest":', "root"))

    # Boundary attacks deliberately use module-level mutable/private objects.
    # If these accept ambiguous or forged inputs, the review records the escape
    # rather than treating a leading underscore or mutable global as authority.
    def permissive_result_parser_bypass():
        hostile = result_text.replace('"verdict": "FAIL"', '"verdict": "PASS",\n        "verdict": "FAIL"', 1)
        parsed = r._ORIGINAL_JSON_LOADS(hostile)
        r.verify_result(parsed, root, source)

    attack("I30_PRIVATE_PERMISSIVE_RESULT_PARSER", "private-parser-bypass", permissive_result_parser_bypass)

    def permissive_source_parser_bypass():
        hostile = source_text.replace('"schema_version": "c23.case.input.v2.7"', '"schema_version": "FORGED",\n  "schema_version": "c23.case.input.v2.7"', 1)
        parsed = r._ORIGINAL_JSON_LOADS(hostile)
        r.verify_result(persisted, root, parsed)

    attack("I31_PRIVATE_PERMISSIVE_SOURCE_PARSER", "private-parser-bypass", permissive_source_parser_bypass)

    def permissive_root_parser_bypass():
        hostile = root_text.replace('"root_digest":', '"root_digest": "' + "0" * 64 + '",\n  "root_digest":', 1)
        parsed = r._ORIGINAL_JSON_LOADS(hostile)
        r.verify_result(persisted, parsed, source)

    attack("I32_PRIVATE_PERMISSIVE_ROOT_PARSER", "private-parser-bypass", permissive_root_parser_bypass)

    def monkeypatch_evaluator():
        original = r.evaluate
        try:
            r.evaluate = lambda supplied_source, supplied_root: copy.deepcopy(forged_fail)
            r.verify_result(forged_fail, root, source)
        finally:
            r.evaluate = original

    attack("I33_MONKEYPATCH_EVALUATOR", "monkeypatch-boundary", monkeypatch_evaluator)

    def unauthorized_pin_monkeypatch():
        doc, new_root, new_result = make_equivalent_new_trio()
        old_pin = r.PINNED_AUTHORITY_ROOT_DIGEST
        try:
            r.PINNED_AUTHORITY_ROOT_DIGEST = "PENDING"
            r.verify_result(new_result, new_root, doc)
        finally:
            r.PINNED_AUTHORITY_ROOT_DIGEST = old_pin

    attack("I34_MONKEYPATCH_PIN_TO_PENDING", "monkeypatch-boundary", unauthorized_pin_monkeypatch)

    # Positive controls prove the oracle is not an all-reject policy.
    def control(test_id: str, family: str, fn) -> None:
        observed, message = "PASS", ""
        try:
            fn()
        except Exception as exc:
            observed, message = "REJECT", f"{type(exc).__name__}: {exc}"
        controls.append({"test_id": test_id, "family": family, "observed": observed, "expected": "PASS", "passed": observed == "PASS", "message": message})

    control("C01_PERSISTED_STRONG_VERIFY", "strong-verifier", lambda: r.verify_result(copy.deepcopy(persisted), copy.deepcopy(root), copy.deepcopy(source)))
    control("C02_ALIAS_STRONG_VERIFY", "strong-verifier", lambda: getattr(r, "verify_result")(copy.deepcopy(persisted), copy.deepcopy(root), copy.deepcopy(source)))
    control("C03_COMPLETE_PARTIAL", "strong-verifier", lambda: functools.partial(r.verify_result, copy.deepcopy(persisted), copy.deepcopy(root), copy.deepcopy(source))())
    control("C04_DETERMINISTIC_REPLAY", "strong-verifier", lambda: r.verify_result(r.evaluate(copy.deepcopy(source), copy.deepcopy(root)), copy.deepcopy(root), copy.deepcopy(source)))
    control("C05_EQUIVALENT_JSON", "normalization", lambda: r.verify_result(r.strict_json_loads(json.dumps(persisted, ensure_ascii=True, indent=7)), copy.deepcopy(root), r.strict_json_loads(json.dumps(source, ensure_ascii=True, indent=5))))

    def legal_repin():
        doc, new_root, new_result = make_equivalent_new_trio()
        old_pin = r.PINNED_AUTHORITY_ROOT_DIGEST
        try:
            r.PINNED_AUTHORITY_ROOT_DIGEST = new_root["root_digest"]
            r.verify_result(new_result, new_root, doc)
        finally:
            r.PINNED_AUTHORITY_ROOT_DIGEST = old_pin

    control("C06_LEGAL_NEW_ROOT_REPIN", "authorized-repin", legal_repin)

    def cli_control():
        proc = subprocess.run(["python3", a.verifier, "--result", a.result, "--authority-root", a.authority_root, "--input", a.input], capture_output=True, text=True)
        if proc.returncode:
            raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    control("C07_CLI_STRONG_VERIFY", "strong-verifier", cli_control)

    escapes = [x for x in attacks if x["escape"]]
    payload = {
        "schema_version": "c23.v2.8-independent-final-negative.v1",
        "review_role": "non_author",
        "oracle": "all module-level result acceptance paths require source+root semantic replay; raw duplicate JSON is rejected before normalization",
        "input_sha256": file_sha(a.input),
        "authority_root_sha256": file_sha(a.authority_root),
        "result_sha256": file_sha(a.result),
        "runner_sha256": file_sha(a.runner),
        "verifier_sha256": file_sha(a.verifier),
        "baseline_distribution": persisted["distribution"],
        "baseline_decision_digest": persisted["decision_digest"],
        "attack_count": len(attacks),
        "secure_attack_count": len(attacks) - len(escapes),
        "escape_count": len(escapes),
        "escape_ids": [x["test_id"] for x in escapes],
        "positive_control_count": len(controls),
        "positive_control_pass_count": sum(x["passed"] for x in controls),
        "attacks": attacks,
        "positive_controls": controls,
        "limits": {
            "real_case_executed": False,
            "real_runtime_migration_executed": False,
            "external_effect_executed": False,
            "practice_gate": "REVIEW_REQUIRED",
            "chief_editor_rc": "NOT_AUTHORIZED",
        },
    }
    payload["suite_digest"] = r.digest(
        [(x["test_id"], x["observed"], x["message"], x["secure_contract_passed"]) for x in attacks]
        + [(x["test_id"], x["observed"], x["message"], x["passed"]) for x in controls]
    )
    Path(a.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: payload[k] for k in ("attack_count", "secure_attack_count", "escape_count", "escape_ids", "positive_control_count", "positive_control_pass_count", "suite_digest")}, ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"] == len(controls) else 1


if __name__ == "__main__":
    raise SystemExit(main())
