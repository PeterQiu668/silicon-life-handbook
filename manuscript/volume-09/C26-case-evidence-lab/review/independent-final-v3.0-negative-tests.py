#!/usr/bin/env python3
"""Non-author final attacks for the C23 v3.0 raw verifier boundary."""
from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import importlib.util
import inspect
import json
import math
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def fsha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    for flag in ("input", "authority-root", "result", "runner", "verifier", "output"):
        parser.add_argument("--" + flag, required=True)
    args = parser.parse_args()
    runner = Path(args.runner)
    verifier = Path(args.verifier)
    r = load(runner, "c23_v30_independent_final")
    source_text = Path(args.input).read_text()
    root_text = Path(args.authority_root).read_text()
    result_text = Path(args.result).read_text()
    source = r.strict_json_loads(source_text)
    root = r.strict_json_loads(root_text)
    result = r.strict_json_loads(result_text)
    r.verify_raw_documents(result_text, root_text, source_text)

    attacks, controls, boundaries = [], [], []

    def resign(candidate):
        candidate["distribution"] = dict(sorted(Counter(x["derived"]["verdict"] for x in candidate["trials"]).items()))
        candidate["accepted_real_claim_count"] = sum(x["derived"]["accepted_real_claim_count"] for x in candidate["trials"])
        candidate["external_effect_count"] = sum(x["derived"]["external_effect_count"] for x in candidate["trials"])
        candidate["decision_digest"] = r.digest({k: v for k, v in candidate.items() if k != "decision_digest"})

    forged = copy.deepcopy(result)
    fail_row = next(x for x in forged["trials"] if x["derived"]["verdict"] == "FAIL")
    fail_row["derived"].update(verdict="PASS", reasons=[])
    resign(forged)
    forged_text = json.dumps(forged, ensure_ascii=False, sort_keys=True)
    forged_rr = copy.deepcopy(result)
    rr_row = next(x for x in forged_rr["trials"] if x["derived"]["verdict"] == "REVIEW_REQUIRED")
    rr_row["derived"].update(verdict="PASS", reasons=[])
    resign(forged_rr)
    rr_text = json.dumps(forged_rr, ensure_ascii=False, sort_keys=True)

    def trio(build_id):
        src = copy.deepcopy(source)
        src["suite"]["build_id"] = build_id
        authority = copy.deepcopy(root)
        authority["suite_manifest"]["build_id"] = build_id
        authority["root_digest"] = r.digest(r.root_payload(authority))
        outcome = r.evaluate(copy.deepcopy(src), copy.deepcopy(authority))
        return tuple(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in (src, authority, outcome))

    unauthorized = trio("BUILD.C23.20261001.V30.INDEPENDENT.UNAUTHORIZED")
    repin = trio("BUILD.C23.20261001.V29.REPIN")
    invalid_environment = copy.deepcopy(source)
    invalid_environment["environment"]["network_accessed"] = True
    invalid_environment_text = json.dumps(invalid_environment, ensure_ascii=False, sort_keys=True)
    extra_source = copy.deepcopy(source)
    extra_source["unexpected_parallel_truth"] = {"status": "ACTIVE"}
    extra_source_text = json.dumps(extra_source, ensure_ascii=False, sort_keys=True)
    wrong_schema_source = copy.deepcopy(source)
    wrong_schema_source["schema_version"] = "FORGED.SCHEMA"
    wrong_schema_text = json.dumps(wrong_schema_source, ensure_ascii=False, sort_keys=True)

    def patch(name, value, fn):
        marker = object()
        old = getattr(r, name, marker)
        setattr(r, name, value)
        try:
            return fn()
        finally:
            if old is marker:
                delattr(r, name)
            else:
                setattr(r, name, old)

    def patch_attr(obj, name, value, fn):
        old = getattr(obj, name)
        setattr(obj, name, value)
        try:
            return fn()
        finally:
            setattr(obj, name, old)

    def patch_many(bindings, fn):
        old = []
        marker = object()
        for name, value in bindings:
            previous = getattr(r, name, marker)
            old.append((name, previous))
            setattr(r, name, value)
        try:
            return fn()
        finally:
            for name, previous in reversed(old):
                if previous is marker:
                    delattr(r, name)
                else:
                    setattr(r, name, previous)

    def attack(test_id, family, fn):
        observed, message = "ACCEPTED", ""
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - the rejection is the observation
            observed, message = "REJECT", f"{type(exc).__name__}: {exc}"
        attacks.append({"test_id": test_id, "family": family, "observed": observed, "expected": "REJECT", "secure": observed == "REJECT", "escape": observed != "REJECT", "message": message})

    def control(test_id, family, fn):
        observed, message = "PASS", ""
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            observed, message = "REJECT", f"{type(exc).__name__}: {exc}"
        controls.append({"test_id": test_id, "family": family, "observed": observed, "expected": "PASS", "passed": observed == "PASS", "message": message})

    def boundary(test_id, fn):
        observed, message = "ACCEPTED", ""
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            observed, message = "REJECT", f"{type(exc).__name__}: {exc}"
        boundaries.append({"test_id": test_id, "scope": "out_of_scope_arbitrary_same_process", "observed": observed, "message": message})

    def cli(result_path=args.result, root_path=args.authority_root, source_path=args.input, pin_id="PIN.C23.CURRENT", program=verifier):
        proc = subprocess.run(
            ["python3", str(program), "--result", str(result_path), "--authority-root", str(root_path), "--input", str(source_path), "--pin-id", pin_id],
            capture_output=True,
            text=True,
        )
        if proc.returncode:
            raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    original_canonical = r.canonical

    def result_only_constant(value):
        if isinstance(value, dict) and value.get("schema_version") == r.RESULT_SCHEMA and "trials" in value:
            return "INDEPENDENT.FORGED.RESULT.EQUALITY"
        return original_canonical(value)

    # Raw-document provenance and retired object-level acceptance APIs.
    attack("I30-001_RESULT_DICT", "raw-boundary", lambda: r.verify_raw_documents(result, root_text, source_text))
    attack("I30-002_ROOT_DICT", "raw-boundary", lambda: r.verify_raw_documents(result_text, root, source_text))
    attack("I30-003_SOURCE_DICT", "raw-boundary", lambda: r.verify_raw_documents(result_text, root_text, source))
    attack("I30-004_ALL_DICT", "raw-boundary", lambda: r.verify_raw_documents(result, root, source))
    attack("I30-005_BYTEARRAY", "raw-boundary", lambda: r.verify_raw_documents(bytearray(result_text.encode()), root_text, source_text))
    attack("I30-006_OLD_VERIFY_RESULT", "retired-object-api", lambda: getattr(r, "verify_result")(result, root, source))
    attack("I30-007_OLD_PRIVATE_JSON_ALIAS", "retired-object-api", lambda: getattr(r, "_ORIGINAL_JSON_LOADS")(result_text))
    attack("I30-008_EVALUATE_THREE_OBJECTS", "retired-object-api", lambda: r.evaluate(result, root, source))

    # Strict parser: duplicate keys, trailing documents, invalid UTF-8 and non-finite numbers.
    duplicate_result = result_text.replace('"verdict": "FAIL"', '"verdict": "PASS",\n        "verdict": "FAIL"', 1)
    duplicate_source = source_text.replace('"case_version": 1', '"case_version": 2, "case_version": 1', 1)
    duplicate_root = root_text.replace('"suite_id":', '"suite_id": "FORGED", "suite_id":', 1)
    attack("I30-009_DUP_RESULT", "strict-parser", lambda: r.verify_raw_documents(duplicate_result, root_text, source_text))
    attack("I30-010_DUP_SOURCE", "strict-parser", lambda: r.verify_raw_documents(result_text, root_text, duplicate_source))
    attack("I30-011_DUP_ROOT", "strict-parser", lambda: r.verify_raw_documents(result_text, duplicate_root, source_text))
    attack("I30-012_TRAILING_RESULT", "strict-parser", lambda: r.verify_raw_documents(result_text + "{}", root_text, source_text))
    attack("I30-013_TRAILING_ROOT", "strict-parser", lambda: r.verify_raw_documents(result_text, root_text + "[]", source_text))
    attack("I30-014_TRAILING_SOURCE", "strict-parser", lambda: r.verify_raw_documents(result_text, root_text, source_text + "{}"))
    attack("I30-015_NAN_RESULT", "strict-parser", lambda: r.verify_raw_documents(result_text.replace('"trial_count": 32', '"trial_count": NaN', 1), root_text, source_text))
    attack("I30-016_INFINITY_SOURCE", "strict-parser", lambda: r.verify_raw_documents(result_text, root_text, source_text.replace('"trial_count": 3', '"trial_count": Infinity', 1)))
    attack("I30-017_NAN_ROOT", "strict-parser", lambda: r.verify_raw_documents(result_text, root_text.replace('"case_version": 1', '"case_version": NaN', 1), source_text))
    attack("I30-018_INVALID_UTF8", "strict-parser", lambda: r.verify_raw_documents(b"\xff", root_text, source_text))
    attack("I30-019_STRING_PATH_NOT_PATH", "strict-parser", lambda: r.verify_raw_documents(str(Path(args.result)), root_text, source_text))

    # Pin, root and full semantic replay.
    attack("I30-020_EMPTY_PIN", "pin-root", lambda: r.verify_raw_documents(result_text, root_text, source_text, pin_id=""))
    attack("I30-021_PENDING_PIN", "pin-root", lambda: r.verify_raw_documents(result_text, root_text, source_text, pin_id="PENDING"))
    attack("I30-022_UNKNOWN_PIN", "pin-root", lambda: r.verify_raw_documents(result_text, root_text, source_text, pin_id="PIN.C23.UNKNOWN"))
    attack("I30-023_CURRENT_WITH_REPIN_ROOT", "pin-root", lambda: r.verify_raw_documents(repin[2], repin[1], repin[0], pin_id="PIN.C23.CURRENT"))
    attack("I30-024_REPIN_WITH_CURRENT_ROOT", "pin-root", lambda: r.verify_raw_documents(result_text, root_text, source_text, pin_id="PIN.C23.V29.REPIN"))
    attack("I30-025_UNAUTHORIZED_SELF_CONSISTENT_TRIO", "pin-root", lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0]))
    attack("I30-026_FORGED_FAIL_RESULT", "semantic-replay", lambda: r.verify_raw_documents(forged_text, root_text, source_text))
    attack("I30-027_FORGED_RR_RESULT", "semantic-replay", lambda: r.verify_raw_documents(rr_text, root_text, source_text))

    # Ordinary module-global and shared-module attribute rebinding.  Every call
    # attempts a concrete forged result, malformed source or unauthorized trio.
    attack("I30-028_PATCH_CANONICAL", "module-global", lambda: patch("canonical", result_only_constant, lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-029_PATCH_DIGEST", "module-global", lambda: patch("digest", lambda *_: "0" * 64, lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-030_PATCH_STRICT_PARSER", "module-global", lambda: patch("strict_json_loads", json.loads, lambda: r.verify_raw_documents(duplicate_result, root_text, source_text)))
    attack("I30-031_PATCH_AUTHORITY_VALIDATOR", "module-global", lambda: patch("validate_authority_root", lambda *_: None, lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    baseline_index = r.validate_document(copy.deepcopy(source), copy.deepcopy(root))
    attack("I30-032_PATCH_DOCUMENT_VALIDATOR", "module-global", lambda: patch("validate_document", lambda *_: baseline_index, lambda: r.verify_raw_documents(result_text, root_text, invalid_environment_text)))
    attack("I30-033_PATCH_PUBLIC_EVALUATOR", "module-global", lambda: patch("evaluate", lambda *_: copy.deepcopy(forged), lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-034_PATCH_PRIVATE_EVALUATOR", "module-global", lambda: patch("_evaluate_with_pin", lambda *_: copy.deepcopy(forged), lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-035_PATCH_ROOT_PAYLOAD", "module-global", lambda: patch("root_payload", lambda *_: {}, lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-036_PATCH_EXACT", "module-global", lambda: patch("exact", lambda *_: None, lambda: r.verify_raw_documents(result_text, root_text, extra_source_text)))
    attack("I30-037_PATCH_SHA", "module-global", lambda: patch("sha", lambda *_: None, lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-038_PATCH_VALIDATE_RECORD", "module-global", lambda: patch("validate_record", lambda *_: None, lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-039_PATCH_INDEX_RECORDS", "module-global", lambda: patch("index_records", lambda *_: baseline_index, lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-040_PATCH_DT", "module-global", lambda: patch("dt", lambda *_: r.datetime.max.replace(tzinfo=r.datetime.now().astimezone().tzinfo), lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-041_PATCH_SCHEMA_CONSTANT", "module-global", lambda: patch("SCHEMA", "FORGED.SCHEMA", lambda: r.verify_raw_documents(result_text, root_text, wrong_schema_text)))
    attack("I30-042_PATCH_RESULT_SCHEMA", "module-global", lambda: patch("RESULT_SCHEMA", forged["schema_version"], lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-043_PATCH_PIN_READER", "module-global", lambda: patch("_read_pin_registry", lambda: (("PIN.C23.CURRENT", r.strict_json_loads(unauthorized[1])["root_digest"]),), lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-044_PATCH_PIN_DIGEST", "module-global", lambda: patch("PIN_REGISTRY_SHA256", "0" * 64, lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-045_PATCH_RETIRED_PIN", "module-global", lambda: patch("PINNED_AUTHORITY_ROOT_DIGEST", r.strict_json_loads(unauthorized[1])["root_digest"], lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-046_INJECT_CAPTURED_PIN_NAME", "module-dict", lambda: patch("_CAPTURED_PIN_ROWS", (("PIN.C23.CURRENT", r.strict_json_loads(unauthorized[1])["root_digest"]),), lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-047_PATCH_JSON_DUMPS", "shared-module", lambda: patch_attr(r.json, "dumps", lambda *_a, **_k: "INDEPENDENT.FORGED.RESULT.EQUALITY", lambda: r.verify_raw_documents(forged_text, root_text, source_text)))
    attack("I30-048_PATCH_HASHLIB_SHA256", "shared-module", lambda: patch_attr(r.hashlib, "sha256", lambda *_: type("H", (), {"hexdigest": lambda _s: "0" * 64})(), lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-049_PATCH_UNIQUE_PAIRS", "module-global", lambda: patch("_unique_object_pairs", dict, lambda: r.verify_raw_documents(duplicate_result, root_text, source_text)))
    attack("I30-050_PATCH_MATH_ISFINITE", "shared-module", lambda: patch_attr(r.math, "isfinite", lambda *_: True, lambda: r.verify_raw_documents(result_text, root_text, source_text.replace('"trial_count": 3', '"trial_count": Infinity', 1))))
    attack("I30-051_PATCH_PATH_TYPE", "module-global", lambda: patch("Path", str, lambda: r.verify_raw_documents(str(Path(args.result)), root_text, source_text)))

    # Combinations must not reconstruct an acceptance path.
    attack("I30-052_CANONICAL_PLUS_ROOT_VALIDATOR", "combined-global", lambda: patch_many([("canonical", result_only_constant), ("validate_authority_root", lambda *_: None)], lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-053_PARSER_PLUS_EVALUATOR", "combined-global", lambda: patch_many([("strict_json_loads", json.loads), ("_evaluate_with_pin", lambda *_: copy.deepcopy(forged))], lambda: r.verify_raw_documents(duplicate_result, root_text, source_text)))
    attack("I30-054_AUTHORITY_PLUS_DOCUMENT", "combined-global", lambda: patch_many([("validate_authority_root", lambda *_: None), ("validate_document", lambda *_: baseline_index)], lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))
    attack("I30-055_DIGEST_EXACT_SHA", "combined-global", lambda: patch_many([("digest", lambda *_: "0" * 64), ("exact", lambda *_: None), ("sha", lambda *_: None)], lambda: r.verify_raw_documents(forged_text, root_text, extra_source_text)))
    attack("I30-056_ALL_PUBLIC_SEMANTICS", "combined-global", lambda: patch_many([("canonical", lambda *_: "X"), ("digest", lambda *_: "0" * 64), ("validate_authority_root", lambda *_: None), ("validate_document", lambda *_: baseline_index), ("_evaluate_with_pin", lambda *_: copy.deepcopy(forged)), ("strict_json_loads", json.loads)], lambda: r.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0])))

    # Saved aliases, partials, getattr/module-dict paths, reload and defaults.
    saved = r.verify_raw_documents
    alias = getattr(r, "verify_raw_documents")
    partial = functools.partial(saved, forged_text, root_text)
    def module_dict_canonical_attack():
        namespace = vars(r)
        old = namespace["canonical"]
        namespace["canonical"] = result_only_constant
        try:
            return saved(forged_text, root_text, source_text)
        finally:
            namespace["canonical"] = old
    attack("I30-057_SAVED_CORE_AFTER_PUBLIC_REBIND", "alias-reflection", lambda: patch("verify_raw_documents", lambda *_a, **_k: True, lambda: saved(forged_text, root_text, source_text)))
    attack("I30-058_GETATTR_ALIAS_FORGED", "alias-reflection", lambda: alias(forged_text, root_text, source_text))
    attack("I30-059_PARTIAL_FORGED", "alias-reflection", lambda: partial(source_text))
    attack("I30-060_MODULE_DICT_CANONICAL_REBIND", "alias-reflection", module_dict_canonical_attack)
    fresh = load(runner, "c23_v30_independent_reload")
    attack("I30-061_FRESH_IMPORT_FORGED", "import-reload", lambda: fresh.verify_raw_documents(forged_text, root_text, source_text))
    attack("I30-062_FRESH_IMPORT_UNAUTHORIZED", "import-reload", lambda: fresh.verify_raw_documents(unauthorized[2], unauthorized[1], unauthorized[0]))

    original_kwdefaults = dict(saved.__kwdefaults__ or {})
    def mutate_default():
        saved.__kwdefaults__["pin_id"] = "PIN.C23.V29.REPIN"
        try:
            return saved(result_text, root_text, source_text)
        finally:
            saved.__kwdefaults__.clear()
            saved.__kwdefaults__.update(original_kwdefaults)
    attack("I30-063_SIGNATURE_DEFAULT_REBIND", "signature-default", mutate_default)

    with tempfile.TemporaryDirectory(prefix="c23-v30-independent-") as temp_name:
        temp = Path(temp_name)
        forged_path = temp / "forged.json"
        duplicate_path = temp / "duplicate.json"
        unauthorized_source = temp / "unauthorized-source.json"
        unauthorized_root = temp / "unauthorized-root.json"
        unauthorized_result = temp / "unauthorized-result.json"
        repin_source = temp / "repin-source.json"
        repin_root = temp / "repin-root.json"
        repin_result = temp / "repin-result.json"
        forged_path.write_text(forged_text)
        duplicate_path.write_text(duplicate_result)
        for path, value in ((unauthorized_source, unauthorized[0]), (unauthorized_root, unauthorized[1]), (unauthorized_result, unauthorized[2]), (repin_source, repin[0]), (repin_root, repin[1]), (repin_result, repin[2])):
            path.write_text(value)

        attack("I30-064_CLI_FORGED_RESULT", "fresh-cli", lambda: cli(forged_path))
        attack("I30-065_CLI_DUPLICATE_RESULT", "fresh-cli", lambda: cli(duplicate_path))
        attack("I30-066_CLI_UNAUTHORIZED_TRIO", "fresh-cli", lambda: cli(unauthorized_result, unauthorized_root, unauthorized_source))

        def cli_missing_source():
            proc = subprocess.run(["python3", str(verifier), "--result", args.result, "--authority-root", args.authority_root], capture_output=True, text=True)
            if proc.returncode:
                raise ValueError("CLI missing source rejected")
        attack("I30-067_CLI_MISSING_SOURCE", "fresh-cli", cli_missing_source)

        def tamper_runner():
            for name in ("verify-case-result.py", "run-case-harness.py", "frozen-pin-registry.json"):
                shutil.copy(verifier.parent / name, temp / name)
            with (temp / "run-case-harness.py").open("a") as handle:
                handle.write("\n# independent runner tamper\n")
            cli(program=temp / "verify-case-result.py")
        attack("I30-068_CLI_RUNNER_DIGEST", "fresh-cli", tamper_runner)

        def tamper_registry():
            for name in ("verify-case-result.py", "run-case-harness.py", "frozen-pin-registry.json"):
                shutil.copy(verifier.parent / name, temp / name)
            registry = json.loads((temp / "frozen-pin-registry.json").read_text())
            registry["pins"][0]["authority_root_digest"] = r.strict_json_loads(unauthorized[1])["root_digest"]
            (temp / "frozen-pin-registry.json").write_text(json.dumps(registry))
            cli(program=temp / "verify-case-result.py")
        attack("I30-069_CLI_PIN_REGISTRY_DIGEST", "fresh-cli", tamper_registry)

        # Legal controls prove that the suite is not an all-reject oracle.
        control("I30-C01_RAW_TEXT", "positive", lambda: r.verify_raw_documents(result_text, root_text, source_text))
        control("I30-C02_RAW_BYTES", "positive", lambda: r.verify_raw_documents(result_text.encode(), root_text.encode(), source_text.encode()))
        control("I30-C03_RAW_PATH", "positive", lambda: r.verify_raw_documents(Path(args.result), Path(args.authority_root), Path(args.input)))
        control("I30-C04_FRESH_CLI", "positive", lambda: cli())
        control("I30-C05_AUTHORIZED_REPIN_RAW", "authorized-repin", lambda: r.verify_raw_documents(repin[2], repin[1], repin[0], pin_id="PIN.C23.V29.REPIN"))
        control("I30-C06_AUTHORIZED_REPIN_CLI", "authorized-repin", lambda: cli(repin_result, repin_root, repin_source, "PIN.C23.V29.REPIN"))
        control("I30-C07_SAVED_ALIAS_LEGAL", "positive", lambda: saved(result_text, root_text, source_text))
        control("I30-C08_FRESH_IMPORT_LEGAL", "positive", lambda: fresh.verify_raw_documents(result_text, root_text, source_text))
        control("I30-C09_GLOBALS_BROKEN_LEGAL", "positive", lambda: patch_many([("canonical", lambda *_: "BROKEN"), ("validate_authority_root", lambda *_: None), ("strict_json_loads", json.loads)], lambda: r.verify_raw_documents(result_text, root_text, source_text)))

    # Direct cell writes require arbitrary same-process object mutation.  They
    # are reported as the declared non-goal and excluded from in-scope counts.
    freevars = dict(zip(saved.__code__.co_freevars, saved.__closure__ or ()))
    def mutate_cell(name, value, fn):
        cell = freevars[name]
        old = cell.cell_contents
        cell.cell_contents = value
        try:
            return fn()
        finally:
            cell.cell_contents = old
    boundary("I30-B01_DIRECT_CANONICAL_CELL", lambda: mutate_cell("canonical_fn", lambda *_: "EQUAL", lambda: saved(forged_text, root_text, source_text)))
    boundary("I30-B02_DIRECT_EVALUATOR_CELL", lambda: mutate_cell("evaluator_fn", lambda *_: copy.deepcopy(forged), lambda: saved(forged_text, root_text, source_text)))

    escapes = [row for row in attacks if row["escape"]]
    payload = {
        "schema_version": "c23.v3.0-independent-final.v1",
        "role": "non_author_final_reviewer",
        "attack_count": len(attacks),
        "secure_attack_count": len(attacks) - len(escapes),
        "escape_count": len(escapes),
        "escape_ids": [row["test_id"] for row in escapes],
        "positive_control_count": len(controls),
        "positive_control_pass_count": sum(row["passed"] for row in controls),
        "boundary_demonstration_count": len(boundaries),
        "boundary_accept_count": sum(row["observed"] == "ACCEPTED" for row in boundaries),
        "baseline_distribution": result["distribution"],
        "baseline_decision_digest": result["decision_digest"],
        "input_sha256": fsha(args.input),
        "root_sha256": fsha(args.authority_root),
        "result_sha256": fsha(args.result),
        "runner_sha256": fsha(args.runner),
        "verifier_sha256": fsha(args.verifier),
        "pin_registry_sha256": fsha(runner.parent / "frozen-pin-registry.json"),
        "attacks": attacks,
        "positive_controls": controls,
        "boundary_demonstrations": boundaries,
        "limits": {
            "real_case_executed": False,
            "real_authorization_and_copyright_reviewed": False,
            "real_runtime_migration_executed": False,
            "real_external_effect_executed": False,
            "direct_closure_cell_mutation": "OUT_OF_SCOPE_DEMONSTRATED",
            "practice_gate": "REVIEW_REQUIRED",
            "chief_editor_rc": "NOT_AUTHORIZED",
        },
    }
    payload["suite_digest"] = r.digest([(x["test_id"], x["observed"], x["message"], x.get("secure", x.get("passed"))) for x in attacks + controls + boundaries])
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in ("attack_count", "secure_attack_count", "escape_count", "escape_ids", "positive_control_count", "positive_control_pass_count", "boundary_accept_count", "suite_digest")}, ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"] == len(controls) else 1


if __name__ == "__main__":
    raise SystemExit(main())
