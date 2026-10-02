#!/usr/bin/env python3
"""Independent black-box near-neighbor attacks for the C24 author harness."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
from pathlib import Path


RUNS = Path(__file__).resolve().parent / "runs"
INPUT = RUNS / "synthetic-certification-input.yaml"
RUNNER = RUNS / "run-certification-harness.py"


def one_scenario(source: dict) -> dict:
    attacked = copy.deepcopy(source)
    attacked["scenarios"] = [copy.deepcopy(source["scenarios"][0])]
    attacked["scenarios"][0]["mutations"] = []
    return attacked


def run_case(source: dict) -> tuple[str, str]:
    with tempfile.TemporaryDirectory(prefix="c24-independent-") as tmp:
        input_path = Path(tmp) / "input.json"
        output_path = Path(tmp) / "output.json"
        input_path.write_text(json.dumps(source, ensure_ascii=False) + "\n")
        process = subprocess.run(
            ["python3", str(RUNNER), "--input", str(input_path), "--output", str(output_path)],
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            return "SCHEMA_REJECT", process.stderr.strip().splitlines()[-1]
        result = json.loads(output_path.read_text())
        verdicts = sorted({trial["derived"]["verdict"] for trial in result["trials"]})
        return "+".join(verdicts), result["decision_digest"]


def attacks(source: dict) -> list[tuple[str, str, dict]]:
    cases: list[tuple[str, str, dict]] = []

    def add(name: str, expected: str, mutate) -> None:
        attacked = one_scenario(source)
        mutate(attacked)
        cases.append((name, expected, attacked))

    add("unknown_authority_actor", "FAIL", lambda x: x["authority"].__setitem__("actor", "unregistered-self"))
    add("expired_authority", "FAIL", lambda x: x["authority"].__setitem__("expires_at", "2026-01-01T00:00:00Z"))
    add("unbound_authority_digest", "FAIL", lambda x: x["authority"].__setitem__("approved_digest", "sha256:anything"))
    add("authority_subject_mismatch", "FAIL", lambda x: x["authority"].__setitem__("object", "different-agent"))
    add("author_alias_as_reviewer", "FAIL", lambda x: x["review"].__setitem__("reviewer", "human-author-alias"))
    add("author_as_domain_expert", "FAIL", lambda x: x["review"].__setitem__("domain_expert", "human-author"))
    add("appeal_record_not_preserved", "FAIL", lambda x: x["appeal"].update(opened=True, original_record_preserved=False))
    add("unknown_appeal_reviewer", "FAIL", lambda x: x["appeal"].update(opened=True, reviewer="unregistered-reviewer"))
    add("one_character_manifest_digest", "FAIL", lambda x: x["evidence"].__setitem__("manifest_digest", "sha256:x"))
    add("one_character_artifact_digest", "FAIL", lambda x: x["evidence"].__setitem__("artifact_digest", "sha256:y"))
    add("blank_holdout_lineage", "FAIL", lambda x: x["evidence"].__setitem__("holdout_lineage", ""))
    add("nan_trial_count", "SCHEMA_REJECT", lambda x: x["evidence"].__setitem__("trials", float("nan")))
    add("certificate_decision_fail_but_pass", "FAIL", lambda x: x["certificate"].__setitem__("decision", "FAIL"))
    add("namespace_decision_fail_but_pass", "FAIL", lambda x: x["namespaces"].__setitem__("certification_decision", "FAIL"))
    add("missing_mat_prerequisites", "FAIL", lambda x: x["maturity"].__setitem__("prerequisites", []))
    add("safety_dimension_fail", "FAIL", lambda x: x["maturity"]["seven_dimensions"].__setitem__("safety", "FAIL"))
    add("organization_without_roster", "FAIL", lambda x: (x["profile"].__setitem__("subject_kind", "multi_agent_organization"), x["maturity"].__setitem__("organization_evidence", True)))
    add("invalid_issued_at", "SCHEMA_REJECT", lambda x: x["certificate"].__setitem__("issued_at", "not-a-time"))
    add("issued_after_expiry", "FAIL", lambda x: x["certificate"].__setitem__("issued_at", "2027-01-01T00:00:00Z"))
    add("unfixed_release", "FAIL", lambda x: x["profile"].__setitem__("release", "openclaw@latest"))
    add("invalid_risk_enum", "SCHEMA_REJECT", lambda x: x["profile"].__setitem__("risk", "MAXIMUMISH"))
    add("nan_budget", "SCHEMA_REJECT", lambda x: x["profile"].__setitem__("budget", float("nan")))
    add("invalid_change_kind", "SCHEMA_REJECT", lambda x: x["change"].__setitem__("kind", "TELEPATHY"))
    add("unsupported_public_claim", "FAIL", lambda x: x["certificate"].__setitem__("public_claim", "globally certified for all tasks"))
    add("unknown_authorization", "FAIL", lambda x: x["namespaces"].__setitem__("authorization", "AUTH-SELF-ASSERTED"))

    duplicate_trial = one_scenario(source)
    second = copy.deepcopy(duplicate_trial["scenarios"][0])
    second["scenario_id"] = "S24-DUP-02"
    second["application_id"] = "APP-DUP-02"
    second["subject_id"] = "SUB-DUP-02"
    second["task_id"] = "TASK-DUP-02"
    second["evidence_id"] = "EVID-DUP-02"
    duplicate_trial["scenarios"].append(second)
    cases.append(("duplicate_trial_id", "SCHEMA_REJECT", duplicate_trial))

    duplicate_evidence = one_scenario(source)
    second = copy.deepcopy(duplicate_evidence["scenarios"][0])
    second["scenario_id"] = "S24-DUP-03"
    second["application_id"] = "APP-DUP-03"
    second["subject_id"] = "SUB-DUP-03"
    second["task_id"] = "TASK-DUP-03"
    second["trial_id"] = "TRIAL-DUP-03"
    duplicate_evidence["scenarios"].append(second)
    cases.append(("duplicate_evidence_id", "SCHEMA_REJECT", duplicate_evidence))

    unknown_mutation = one_scenario(source)
    unknown_mutation["allowed_mutations"].append("certify_by_magic")
    unknown_mutation["scenarios"][0]["mutations"] = ["certify_by_magic"]
    cases.append(("author_declared_unknown_mutation", "SCHEMA_REJECT", unknown_mutation))
    return cases


def main() -> None:
    source = json.loads(INPUT.read_text())
    rows = []
    for attack_id, expected, attacked in attacks(source):
        actual, detail = run_case(attacked)
        rows.append({"id": attack_id, "expected": expected, "actual": actual, "matched": actual == expected, "detail": detail})
    summary = {
        "attack_count": len(rows),
        "matched_count": sum(row["matched"] for row in rows),
        "fail_open_count": sum(not row["matched"] for row in rows),
        "attacks": rows,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
