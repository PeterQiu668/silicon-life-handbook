#!/usr/bin/env python3
"""Independent C24 v2.7 final semantic, binding, and replay review.

This program intentionally does not trust scenario names, author expected values,
or the v2.7 author regression outcome.  It treats a candidate as accepted only
when the relevant closed-world contract *and* the pinned source/root/result
replay accept it.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import inspect
import json
import subprocess
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path


def load_runner(path: str):
    spec = importlib.util.spec_from_file_location("c24_v27_independent_runner", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def file_sha(path: str) -> str:
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def at(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--authority", required=True)
    p.add_argument("--runner", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--contracts", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    r = load_runner(args.runner)
    source_text = Path(args.input).read_text()
    authority_text = Path(args.authority).read_text()
    result_text = Path(args.result).read_text()
    contract_text = Path(args.contracts).read_text()
    source = r.validate(r.strict_json_loads(source_text), r.validate_authority(r.strict_json_loads(authority_text)))
    authority = r.validate_authority(r.strict_json_loads(authority_text))
    saved = r.strict_json_loads(result_text)
    contracts = r.strict_json_loads(contract_text)
    r.verify_result(copy.deepcopy(saved), authority, source)

    scenarios = {x["scenario_id"]: x for x in source["scenarios"]}
    trials = {x["scenario_id"]: x for x in saved["trials"]}
    controls = {x["kind"]: x for x in contracts["controls"]}
    renewal = controls["LEGAL_RENEWAL"]
    recert = controls["LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION"]
    renewal_state = scenarios["S24-059"]["state"]
    recert_state = scenarios["S24-060"]["state"]

    def record_ok(row, field="record_digest"):
        return row.get(field) == r.sha({k: v for k, v in row.items() if k != field})

    def reseal(row, field="record_digest"):
        row[field] = r.sha({k: v for k, v in row.items() if k != field})

    def plan_bound(state, control):
        matches = [
            x
            for x in state["evidence_registry"].values()
            if x["kind"] == "appeal_record"
            and x["source"] == "preregistered-positive-control-plan"
            and x["object_id"] == control["control_id"]
        ]
        if len(matches) != 1 or not record_ok(matches[0]) or matches[0]["content_digest"] != r.sha(control):
            raise ValueError("positive plan digest is not rooted in state")

    def current_issue_ok(state, ref, when):
        app = state["application"]
        if not r.auth_ok(
            state,
            authority,
            ref,
            at(when),
            action="issue_synthetic_assessment",
            subject_type="application",
            subject_id=app["application_id"],
            object_digest=app["application_digest"],
            scope=app["scope"],
        ):
            raise ValueError("current issuance authority is invalid")

    def disposition_ok(control, state):
        rw = control["representative_real_world"]
        if set(rw) != {"status", "policy_authority_ref", "approval_authority_ref", "reason"}:
            raise ValueError("real-world disposition schema")
        if rw["status"] != "NOT_APPLICABLE" or not rw["reason"].strip():
            raise ValueError("real-world disposition is not explicit N/A")
        policy = authority["d22_policy"]
        if rw["policy_authority_ref"] != policy["policy_id"] or "representative_real_world" not in policy["not_applicable_layers"]:
            raise ValueError("real-world N/A policy is not bound")
        cert = state["certificate_registry"][state["certificate_ref"]]
        current_issue_ok(state, rw["approval_authority_ref"], cert["issued_at"])

    def validate_renewal(control, state):
        if control["kind"] != "LEGAL_RENEWAL" or control["schema"] != "c24.cert.positive-control.v2.7":
            raise ValueError("renewal contract identity")
        app = state["application"]
        current = state["certificate_registry"][state["certificate_ref"]]
        review = next(iter(state["review_registry"].values()))
        old_app = control["original_application"]
        old_auth = control["original_authority"]
        old_review = control["original_review"]
        old_bundle = control["original_bundle"]
        old_maturity = control["original_maturity"]
        old_namespace = control["original_namespace"]
        old_claim = control["original_public_claim"]
        original = control["original_certificate"]
        request = control["renewal_request"]
        for row in (old_app, old_auth, old_review, old_bundle, old_maturity, old_namespace, old_claim, original):
            if not record_ok(row):
                raise ValueError("renewal historical chain digest")
        if (control["application_id"], control["subject_id"], control["scope"], control["release"]) != (
            app["application_id"], app["subject_id"], app["scope"], app["release"]
        ):
            raise ValueError("renewal current application binding")
        if original["certificate_id"] == current["certificate_id"]:
            raise ValueError("renewal reuses certificate id")
        if (original["subject_id"], original["scope"], original["release"]) != (
            current["subject_id"], current["scope"], current["release"]
        ):
            raise ValueError("renewal subject/scope/release mismatch")
        if original["decision"] != "PASS" or original["lifecycle"] != "ACTIVE" or original["real_certificate"]:
            raise ValueError("original certificate is not a valid synthetic PASS")
        if (original["application_id"], original["application_digest"]) != (old_app["application_id"], old_app["record_digest"]):
            raise ValueError("original application binding")
        if (old_app["subject_id"], old_app["scope"], old_app["release"]) != (app["subject_id"], app["scope"], app["release"]):
            raise ValueError("original application continuity")
        if original["authority_ref"] != old_auth["authority_id"] or old_auth["subject_id"] != old_app["application_id"] or old_auth["object_digest"] != old_app["record_digest"]:
            raise ValueError("original authority binding")
        if old_auth["action"] != "issue_synthetic_assessment" or old_auth["status"] != "ACTIVE":
            raise ValueError("original authority state")
        if not (at(old_auth["not_before"]) <= at(original["issued_at"]) <= at(old_auth["expires_at"])):
            raise ValueError("original authority validity window")
        if original["review_ref"] != old_review["review_id"] or old_review["application_id"] != old_app["application_id"] or old_review["application_digest"] != old_app["record_digest"]:
            raise ValueError("original review binding")
        if old_review["decision"] != "PASS" or old_review["reviewer"] in {old_review["author"], old_review["controller"], old_review["domain_expert"]} or old_review["domain_expert"] in {old_review["author"], old_review["controller"]}:
            raise ValueError("original review independence")
        if old_bundle["status"] != "PASS" or old_maturity["decision"] != "PASS" or old_namespace["certification_decision"] != "PASS" or old_claim["status"] != "PASS":
            raise ValueError("original supporting record failed")
        if original["bundle_digest"] != old_bundle["record_digest"] or original["maturity_digest"] != old_maturity["record_digest"] or original["namespace_digest"] != old_namespace["record_digest"]:
            raise ValueError("original evidence projection")
        if original["public_claim_ref"] != old_claim["evidence_id"] or old_claim["certificate_id"] != original["certificate_id"]:
            raise ValueError("original claim projection")
        if review["reviewer"] in {review["author"], review["controller"], review["domain_expert"]} or review["domain_expert"] in {review["author"], review["controller"]}:
            raise ValueError("renewal review independence")
        if request["previous_certificate_ref"] != original["certificate_id"] or request["current_certificate_ref"] != current["certificate_id"] or request["independent_review_ref"] != review["review_id"] or request["issuance_authority_ref"] != current["authority_ref"]:
            raise ValueError("renewal request binding")
        if not (at(original["issued_at"]) < at(request["requested_at"]) < at(review["issued_at"]) < at(current["issued_at"]) < at(original["expires_at"])):
            raise ValueError("renewal causal window")
        order = control["lifecycle_order"]
        expected = ["ORIGINAL_CERTIFICATE_ISSUED", "RENEWAL_REQUESTED", "INDEPENDENT_REVIEW_RECORDED", "RENEWED_CERTIFICATE_ISSUED", "RENEWED_CERTIFICATE_ACTIVATED", "ORIGINAL_CERTIFICATE_EXPIRES"]
        times = [at(x["occurred_at"]) for x in order]
        if [x["kind"] for x in order] != expected or times != sorted(times) or len(set(times)) != len(times):
            raise ValueError("renewal lifecycle order")
        projected = [original["issued_at"], request["requested_at"], review["issued_at"], current["issued_at"], state["lifecycle"]["occurred_at"], original["expires_at"]]
        if [x["occurred_at"] for x in order] != projected:
            raise ValueError("renewal lifecycle projection")
        current_issue_ok(state, request["issuance_authority_ref"], current["issued_at"])
        disposition_ok(control, state)
        plan_bound(state, control)
        if trials["S24-059"]["decision"] != "PASS" or trials["S24-059"]["lifecycle"] != "ACTIVE":
            raise ValueError("renewal scenario is not PASS/ACTIVE")
        return True

    def validate_recert(control, state):
        if control["kind"] != "LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION" or control["schema"] != "c24.cert.positive-control.v2.7":
            raise ValueError("recert contract identity")
        app = state["application"]
        change = state["change"]
        cert = state["certificate_registry"][state["certificate_ref"]]
        review = state["review_registry"].get(change["retest_review_ref"])
        entries = change["retest_manifest"]["entries"]
        if not change["material"] or change["impact_review"] != "PASS" or change["retest"] != "PASS":
            raise ValueError("material recert decision")
        if control["application_id"] != app["application_id"] or control["subject_id"] != app["subject_id"] or control["scope"] != app["scope"]:
            raise ValueError("recert application binding")
        if control["change_ref"] != change["change_id"] or control["post_change_release"] != app["release"] or change["post_change_release"] != app["release"]:
            raise ValueError("recert release/change binding")
        if set(control["required_layers"]) != {"training", "regression", "holdout"} or set(change["retest_manifest"]["required_layers"]) != set(control["required_layers"]):
            raise ValueError("recert three-layer contract")
        if set(control["required_security_slices"]) != {"certification-redteam"} or set(change["retest_manifest"]["required_security_slices"]) != set(control["required_security_slices"]):
            raise ValueError("recert security slice contract")
        if {x["layer"] for x in entries} != {"training", "regression", "holdout"} or {x["trial_ref"] for x in entries} != set(control["trial_refs"]) or {x["evidence_ref"] for x in entries} != set(control["output_refs"]):
            raise ValueError("recert exact entry projection")
        if len(entries) != 3 or len(set(control["trial_refs"])) != 3 or len(set(control["output_refs"])) != 3:
            raise ValueError("recert unique trial/output projection")
        changed_at = at(change["issued_at"])
        latest = changed_at
        for entry in entries:
            trial = state["trial_registry"].get(entry["trial_ref"])
            output = state["evidence_registry"].get(entry["evidence_ref"])
            if not trial or not output or not record_ok(trial) or not record_ok(output):
                raise ValueError("recert trial/output record")
            if trial["output_ref"] != entry["evidence_ref"] or trial["layer"] != entry["layer"] or trial["release"] != app["release"] or output["object_version"] != app["release"]:
                raise ValueError("recert trial/output/release binding")
            if output["status"] != "PASS" or output["kind"] != "trial_output":
                raise ValueError("recert output state")
            if not set(entry["security_slices"]) >= set(control["required_security_slices"]):
                raise ValueError("recert security slice missing")
            if not (changed_at < at(trial["completed_at"]) <= at(output["issued_at"])):
                raise ValueError("recert post-change time")
            latest = max(latest, at(output["issued_at"]))
        if not review or not record_ok(review) or review["review_id"] != control["independent_review_ref"] or review["decision"] != "PASS" or at(review["issued_at"]) <= latest:
            raise ValueError("recert independent review timing/state")
        if review["reviewer"] in {review["author"], review["controller"], review["domain_expert"], change["owner"]}:
            raise ValueError("recert review conflict")
        if not (at(review["issued_at"]) < at(cert["issued_at"]) <= at(state["lifecycle"]["occurred_at"])):
            raise ValueError("recert issuance/lifecycle time")
        current_issue_ok(state, control["issuance_authority_ref"], cert["issued_at"])
        disposition_ok(control, state)
        plan_bound(state, control)
        if trials["S24-060"]["decision"] != "PASS" or trials["S24-060"]["lifecycle"] != "ACTIVE":
            raise ValueError("recert scenario is not PASS/ACTIVE")
        return True

    attacks = []

    def record_attack(test_id, family, channel, fn, hard=True):
        actual = "ACCEPTED"
        message = ""
        try:
            value = fn()
            if isinstance(value, tuple):
                actual = value[0]
                message = value[1] if len(value) > 1 else ""
            elif isinstance(value, str):
                actual = value
        except (ValueError, TypeError, KeyError, AssertionError, AttributeError, subprocess.CalledProcessError) as exc:
            actual = "REJECT"
            message = f"{type(exc).__name__}: {exc}"
        secure = actual in {"REJECT", "FAIL", "SCHEMA_REJECT"} if hard else actual != "ACCEPTED" and actual != "PASS"
        attacks.append({"test_id": test_id, "family": family, "channel": channel, "actual": actual, "secure": secure, "escape": not secure, "message": message})

    def contract_attack(test_id, family, kind, mutate_control=None, mutate_state=None):
        control = copy.deepcopy(renewal if kind == "renewal" else recert)
        state = copy.deepcopy(renewal_state if kind == "renewal" else recert_state)
        if mutate_control:
            mutate_control(control)
        if mutate_state:
            mutate_state(state)
        return validate_renewal(control, state) if kind == "renewal" else validate_recert(control, state)

    def semantic_attack(sid, mutate):
        sc = scenarios[sid]
        state = copy.deepcopy(sc["state"])
        mutate(state)
        try:
            state = r.validate_state(state, "independent." + sid)
            decision, lifecycle, reasons, *_ = r.evaluate(source, state, sc["layer"], authority)
            return decision, ";".join(reasons)
        except (ValueError, TypeError, KeyError) as exc:
            return "SCHEMA_REJECT", f"{type(exc).__name__}: {exc}"

    def mutate_event(state, kind, fn):
        row = next(x for x in state["event_registry"].values() if x["kind"] == kind)
        fn(row, state)
        reseal(row)

    # Renewal contract, time, role, N/A, and rooted-plan attacks.
    record_attack("F01", "renewal-identity", "contract", lambda: contract_attack("", "", "renewal", lambda c: (c["original_certificate"].update(certificate_id=c["renewal_request"]["current_certificate_ref"]), reseal(c["original_certificate"]))))
    record_attack("F02", "renewal-window", "contract", lambda: contract_attack("", "", "renewal", lambda c: c["renewal_request"].update(requested_at="2026-10-01T00:00:00Z")))
    record_attack("F03", "renewal-window", "contract", lambda: contract_attack("", "", "renewal", lambda c: c["renewal_request"].update(requested_at="2026-09-30T10:55:00Z")))
    record_attack("F04", "renewal-window", "contract", lambda: contract_attack("", "", "renewal", lambda c: (c["original_authority"].update(expires_at="2026-09-02T23:59:00Z"), reseal(c["original_authority"]))))
    record_attack("F05", "renewal-review", "contract", lambda: contract_attack("", "", "renewal", lambda c: (c["original_review"].update(reviewer=c["original_review"]["author"]), reseal(c["original_review"]))))
    record_attack("F06", "renewal-support", "contract", lambda: contract_attack("", "", "renewal", lambda c: (c["original_bundle"].update(status="FAIL"), reseal(c["original_bundle"]))))
    record_attack("F07", "renewal-support", "contract", lambda: contract_attack("", "", "renewal", lambda c: (c["original_public_claim"].update(status="FAIL"), reseal(c["original_public_claim"]))))
    record_attack("F08", "renewal-request", "contract", lambda: contract_attack("", "", "renewal", lambda c: c["renewal_request"].update(independent_review_ref="REVIEW-UNKNOWN")))
    record_attack("F09", "renewal-dag", "contract", lambda: contract_attack("", "", "renewal", lambda c: c["lifecycle_order"].__setitem__(4, copy.deepcopy(c["lifecycle_order"][3]))))
    record_attack("F10", "renewal-na", "contract", lambda: contract_attack("", "", "renewal", lambda c: c["representative_real_world"].update(status="PASS")))
    record_attack("F11", "renewal-na", "contract", lambda: contract_attack("", "", "renewal", lambda c: c["representative_real_world"].update(approval_authority_ref="AUTH-UNKNOWN")))
    record_attack("F12", "renewal-plan-root", "contract", lambda: contract_attack("", "", "renewal", lambda c: c.update(control_id="C24-POS-RENEWAL-FORGED")))

    # Material-change D22, release, trial/output, review, and plan attacks.
    record_attack("F13", "recert-layer", "contract", lambda: contract_attack("", "", "recert", lambda c: c["required_layers"].remove("training")))
    record_attack("F14", "recert-layer", "contract", lambda: contract_attack("", "", "recert", lambda c: c["required_layers"].remove("regression")))
    record_attack("F15", "recert-layer", "contract", lambda: contract_attack("", "", "recert", lambda c: c["required_layers"].remove("holdout")))
    record_attack("F16", "recert-security", "contract", lambda: contract_attack("", "", "recert", lambda c: c.update(required_security_slices=[])))
    record_attack("F17", "recert-release", "contract", lambda: contract_attack("", "", "recert", lambda c: c.update(post_change_release="openclaw@forged")))
    record_attack("F18", "recert-output", "contract", lambda: contract_attack("", "", "recert", lambda c: c["output_refs"].__setitem__(2, c["output_refs"][0])))
    record_attack("F19", "recert-na", "contract", lambda: contract_attack("", "", "recert", lambda c: c["representative_real_world"].update(reason="")))
    record_attack("F20", "recert-na", "contract", lambda: contract_attack("", "", "recert", lambda c: c["representative_real_world"].update(policy_authority_ref="POLICY-UNKNOWN")))
    record_attack("F21", "recert-change", "semantic", lambda: semantic_attack("S24-060", lambda s: (s["change"].update(material=False), reseal(s["change"]))))
    record_attack("F22", "recert-security", "semantic", lambda: semantic_attack("S24-060", lambda s: (s["change"]["retest_manifest"]["entries"][0].update(security_slices=[]), reseal(s["change"]))))
    record_attack("F23", "recert-output", "semantic", lambda: semantic_attack("S24-060", lambda s: (s["change"]["retest_manifest"]["entries"][1].update(evidence_ref=s["change"]["retest_manifest"]["entries"][0]["evidence_ref"]), reseal(s["change"]))))
    def output_fail(state):
        ref = state["change"]["retest_evidence_refs"][0]
        state["evidence_registry"][ref]["status"] = "FAIL"
        reseal(state["evidence_registry"][ref])
    record_attack("F24", "recert-output", "semantic", lambda: semantic_attack("S24-060", output_fail))
    def trial_before_change(state):
        ref = state["change"]["retest_trial_refs"][0]
        state["trial_registry"][ref]["completed_at"] = "2026-09-30T09:34:00Z"
        reseal(state["trial_registry"][ref])
    record_attack("F25", "recert-time", "semantic", lambda: semantic_attack("S24-060", trial_before_change))
    def output_before_trial(state):
        ref = state["change"]["retest_trial_refs"][1]
        out = state["trial_registry"][ref]["output_ref"]
        state["evidence_registry"][out]["issued_at"] = "2026-09-30T10:14:00Z"
        reseal(state["evidence_registry"][out])
    record_attack("F26", "recert-time", "semantic", lambda: semantic_attack("S24-060", output_before_trial))
    def review_before_output(state):
        row = next(iter(state["review_registry"].values()))
        row["issued_at"] = "2026-09-30T10:20:00Z"
        reseal(row)
    record_attack("F27", "recert-review", "semantic", lambda: semantic_attack("S24-060", review_before_output))
    def cert_before_review(state):
        row = state["certificate_registry"][state["certificate_ref"]]
        row["issued_at"] = "2026-09-30T10:49:00Z"
        reseal(row)
    record_attack("F28", "recert-time", "semantic", lambda: semantic_attack("S24-060", cert_before_review))
    def review_is_change_owner(state):
        row = next(iter(state["review_registry"].values()))
        row["reviewer"] = state["change"]["owner"]
        reseal(row)
    record_attack("F29", "recert-review", "semantic", lambda: semantic_attack("S24-060", review_is_change_owner))

    # Causal DAG and frozen authority projection attacks on the new positive path.
    record_attack("F30", "event-dag", "semantic", lambda: semantic_attack("S24-060", lambda s: s["event_registry"].pop(next(k for k, v in s["event_registry"].items() if v["kind"] == "CHANGE_EVIDENCE_RECORDED"))))
    record_attack("F31", "event-dag", "semantic", lambda: semantic_attack("S24-060", lambda s: mutate_event(s, "TRIAL_COMPLETED", lambda x, _: x.update(predecessor_refs=[]))))
    record_attack("F32", "event-dag", "semantic", lambda: semantic_attack("S24-060", lambda s: mutate_event(s, "TRIAL_OUTPUT_RECORDED", lambda x, _: x.update(predecessor_refs=[x["event_id"]]))))
    record_attack("F33", "event-dag", "semantic", lambda: semantic_attack("S24-060", lambda s: mutate_event(s, "MANIFEST_SEALED", lambda x, _: x.update(sequence=x["sequence"] + 2))))
    record_attack("F34", "event-dag", "semantic", lambda: semantic_attack("S24-060", lambda s: mutate_event(s, "PUBLIC_CLAIM_RECORDED", lambda x, st: x.update(occurred_at=next(y["occurred_at"] for y in st["event_registry"].values() if y["kind"] == "CERTIFICATE_ISSUED")))))
    record_attack("F35", "event-binding", "semantic", lambda: semantic_attack("S24-060", lambda s: mutate_event(s, "LIFECYCLE_OCCURRED", lambda x, _: x.update(subject_ref="CERT-UNKNOWN"))))

    # Source/root/result must be replayed together; no summary-only acceptance.
    record_attack("F36", "result-replay", "verifier", lambda: r.verify_result(copy.deepcopy(saved), authority, None))
    record_attack("F37", "result-replay", "verifier", lambda: r.verify_result(copy.deepcopy(saved), source, source))
    changed_source = copy.deepcopy(source)
    changed_source["now"] = "2026-09-30T12:00:01Z"
    record_attack("F38", "result-replay", "verifier", lambda: r.verify_result(copy.deepcopy(saved), authority, changed_source))
    def forged_fail_to_pass():
        candidate = copy.deepcopy(saved)
        row = next(x for x in candidate["trials"] if x["decision"] == "FAIL")
        row["decision"] = "PASS"
        row["lifecycle"] = "ACTIVE"
        row["reasons"] = []
        candidate["distribution"] = dict(sorted(Counter(x["decision"] for x in candidate["trials"]).items()))
        candidate["lifecycle_distribution"] = dict(sorted(Counter(x["lifecycle"] for x in candidate["trials"]).items()))
        candidate["decision_digest"] = r.sha(r.result_payload(candidate))
        return r.verify_result(candidate, authority, source)
    record_attack("F39", "result-replay", "verifier", forged_fail_to_pass)
    def reorder_result():
        candidate = copy.deepcopy(saved)
        candidate["trials"][0], candidate["trials"][1] = candidate["trials"][1], candidate["trials"][0]
        candidate["decision_digest"] = r.sha(r.result_payload(candidate))
        return r.verify_result(candidate, authority, source)
    record_attack("F40", "result-replay", "verifier", reorder_result)
    forged_root = copy.deepcopy(authority)
    forged_root["bundle_id"] = "C24-FORGED-ROOT"
    forged_root["root_digest"] = r.sha({k: v for k, v in forged_root.items() if k != "root_digest"})
    record_attack("F41", "authority-pin", "verifier", lambda: r.verify_result(copy.deepcopy(saved), forged_root, source))
    record_attack("F42", "strict-json", "parser", lambda: r.strict_json_loads(result_text.replace("{", '{"schema":"FORGED",', 1)))
    record_attack("F43", "strict-json", "parser", lambda: r.strict_json_loads(source_text.replace('"environment": {', '"environment": {"mode":"offline_synthetic",', 1)))
    def low_arity_entry():
        for name, obj in vars(r).items():
            if callable(obj) and any(token in name.lower() for token in ("verify", "accept")):
                try:
                    inspect.signature(obj).bind(copy.deepcopy(saved), authority)
                except (TypeError, ValueError):
                    continue
                obj(copy.deepcopy(saved), authority)
                return "ACCEPTED"
        raise ValueError("no low-arity verification entry")
    record_attack("F44", "verifier-entry", "reflection", low_arity_entry)

    # Rewrite the renewal control and its plan digest together, then demonstrate
    # that the unchanged pinned root/source/result still rejects the candidate.
    def forged_plan_and_source():
        mutated_source = copy.deepcopy(source)
        sc = next(x for x in mutated_source["scenarios"] if x["scenario_id"] == "S24-059")
        forged = copy.deepcopy(renewal)
        forged["renewal_request"]["requested_at"] = "2026-10-01T00:00:00Z"
        plan = next(x for x in sc["state"]["evidence_registry"].values() if x["source"] == "preregistered-positive-control-plan")
        plan["content_digest"] = r.sha(forged)
        reseal(plan)
        return r.verify_result(copy.deepcopy(saved), authority, mutated_source)
    record_attack("F45", "contract-source-root", "full-replay", forged_plan_and_source)

    positives = []
    def positive(test_id, kind, fn):
        passed = False
        message = ""
        try:
            passed = bool(fn())
        except (ValueError, TypeError, KeyError, AssertionError) as exc:
            message = f"{type(exc).__name__}: {exc}"
        positives.append({"test_id": test_id, "kind": kind, "passed": passed, "message": message})

    positive("P01", "fixed-limited", lambda: trials["S24-001"]["decision"] == "PASS" and trials["S24-001"]["lifecycle"] == "LIMITED")
    positive("P02", "fixed-active", lambda: trials["S24-002"]["decision"] == "PASS" and trials["S24-002"]["lifecycle"] == "ACTIVE")
    positive("P03", "fixed-expired", lambda: trials["S24-003"]["decision"] == "PASS" and trials["S24-003"]["lifecycle"] == "EXPIRED")
    positive("P04", "short-window-limited", lambda: trials["S24-058"]["decision"] == "PASS" and trials["S24-058"]["lifecycle"] == "LIMITED")
    positive("P05", "renewal-contract-and-fixed-result", lambda: validate_renewal(renewal, renewal_state) and trials["S24-059"]["decision"] == "PASS")
    positive("P06", "material-recert-contract-and-fixed-result", lambda: validate_recert(recert, recert_state) and trials["S24-060"]["decision"] == "PASS")
    positive("P07", "full-source-root-result-replay", lambda: r.verify_result(copy.deepcopy(saved), authority, source))
    positive("P08", "offline-zero-validated-success", lambda: saved["successful_real_certificates"] == 0 and saved["successful_external_effects"] == 0)

    escapes = [x for x in attacks if x["escape"]]
    payload = {
        "schema": "c24.v2.7-independent-final.v1",
        "role": "non_author_final_reviewer",
        "scope": "offline_synthetic_only",
        "input_sha256": file_sha(args.input),
        "authority_sha256": file_sha(args.authority),
        "result_sha256": file_sha(args.result),
        "contracts_sha256": file_sha(args.contracts),
        "runner_sha256": file_sha(args.runner),
        "fixed_trial_count": saved["trial_count"],
        "fixed_distribution": saved["distribution"],
        "fixed_lifecycle_distribution": saved["lifecycle_distribution"],
        "authority_root_digest": authority["root_digest"],
        "decision_digest": saved["decision_digest"],
        "attack_count": len(attacks),
        "secure_attack_count": len(attacks) - len(escapes),
        "escape_count": len(escapes),
        "escape_ids": [x["test_id"] for x in escapes],
        "positive_control_count": len(positives),
        "positive_control_pass_count": sum(x["passed"] for x in positives),
        "attacks": attacks,
        "positive_controls": positives,
        "limits": {
            "real_openclaw_executed": False,
            "real_hermes_executed": False,
            "representative_real_world_executed": False,
            "external_certification_authority_executed": False,
            "real_certificate_issued": False,
            "external_effect_executed": False,
            "practice_gate": "REVIEW_REQUIRED",
            "chief_editor_rc": "NOT_AUTHORIZED",
        },
    }
    payload["suite_digest"] = r.sha({"attacks": attacks, "positive_controls": positives})
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: payload[k] for k in ("attack_count", "secure_attack_count", "escape_count", "positive_control_count", "positive_control_pass_count", "suite_digest")}, ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"] == len(positives) else 1


if __name__ == "__main__":
    raise SystemExit(main())
