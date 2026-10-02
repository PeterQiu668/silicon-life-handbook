#!/usr/bin/env python3
"""C24 v2.7 author regression for legal renewal and material-change reachability."""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from datetime import datetime
from pathlib import Path


def load(path):
    spec=importlib.util.spec_from_file_location("c24_v27_runner",path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def at(value):
    return datetime.fromisoformat(value.replace("Z","+00:00"))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True); p.add_argument("--authority",required=True)
    p.add_argument("--runner",required=True); p.add_argument("--result",required=True)
    p.add_argument("--contracts",required=True); p.add_argument("--output",required=True)
    a=p.parse_args(); r=load(a.runner)
    source=r.strict_json_loads(Path(a.input).read_text()); authority=r.validate_authority(r.strict_json_loads(Path(a.authority).read_text()))
    source=r.validate(source,authority); saved=r.strict_json_loads(Path(a.result).read_text()); r.verify_result(saved,authority,source)
    contract_set=r.strict_json_loads(Path(a.contracts).read_text())
    if set(contract_set)!={"schema","scope","controls","limits"} or contract_set["schema"]!="c24.cert.positive-controls.v2.7" or len(contract_set["controls"])!=2: raise ValueError("positive contract set schema")
    controls={x["kind"]:x for x in contract_set["controls"]}; scenarios={x["scenario_id"]:x for x in source["scenarios"]}; trials={x["scenario_id"]:x for x in saved["trials"]}
    renewal_state=scenarios["S24-059"]["state"]; recert_state=scenarios["S24-060"]["state"]
    attacks=[]; positives=[]

    def record_ok(row,field="record_digest"):
        return row.get(field)==r.sha({k:v for k,v in row.items() if k!=field})

    def plan_bound(state,control):
        matches=[x for x in state["evidence_registry"].values() if x["kind"]=="appeal_record" and x["source"]=="preregistered-positive-control-plan" and x["object_id"]==control["control_id"]]
        if len(matches)!=1 or matches[0]["content_digest"]!=r.sha(control) or not record_ok(matches[0]): raise ValueError("positive control plan is not frozen in state")

    def active_issue(state,ref,when):
        app=state["application"]; row=state["authority_registry"].get(ref)
        if not row or not r.auth_ok(state,authority,ref,at(when),action="issue_synthetic_assessment",subject_type="application",subject_id=app["application_id"],object_digest=app["application_digest"],scope=app["scope"]): raise ValueError("issuance authority invalid")
        return row

    def disposition(control,state):
        rw=control["representative_real_world"]
        if set(rw)!={"status","policy_authority_ref","approval_authority_ref","reason"} or rw["status"]!="NOT_APPLICABLE" or not rw["reason"].strip(): raise ValueError("representative real-world disposition invalid")
        if rw["policy_authority_ref"]!=authority["d22_policy"]["policy_id"] or "representative_real_world" not in authority["d22_policy"]["not_applicable_layers"]: raise ValueError("representative real-world policy authority invalid")
        active_issue(state,rw["approval_authority_ref"],state["certificate_registry"][state["certificate_ref"]]["issued_at"])

    def positive_trial(sid):
        row=trials[sid]
        if row["decision"]!="PASS" or row["lifecycle"]!="ACTIVE" or row["reasons"]: raise ValueError("positive scenario did not reach PASS/ACTIVE")

    def validate_renewal(control,state=renewal_state,enforce_plan=True):
        if control["schema"]!="c24.cert.positive-control.v2.7" or control["kind"]!="LEGAL_RENEWAL": raise ValueError("renewal control identity")
        app=state["application"]; cert=state["certificate_registry"][state["certificate_ref"]]; review=next(iter(state["review_registry"].values())); original=control["original_certificate"]; old_app=control["original_application"]; old_auth=control["original_authority"]; old_review=control["original_review"]; old_bundle=control["original_bundle"]; old_maturity=control["original_maturity"]; old_namespace=control["original_namespace"]; old_claim=control["original_public_claim"]; request=control["renewal_request"]
        if not all(record_ok(x) for x in (original,old_app,old_auth,old_review,old_bundle,old_maturity,old_namespace,old_claim)): raise ValueError("original certificate chain digest")
        if (control["application_id"],control["subject_id"],control["scope"],control["release"])!=(app["application_id"],app["subject_id"],app["scope"],app["release"]): raise ValueError("renewal control scope binding")
        if original["certificate_id"]==cert["certificate_id"] or original["subject_id"]!=cert["subject_id"] or original["scope"]!=cert["scope"] or original["release"]!=cert["release"]: raise ValueError("original/current certificate binding")
        if (original["application_id"],original["application_digest"])!=(old_app["application_id"],old_app["record_digest"]) or old_app["subject_id"]!=app["subject_id"] or old_app["scope"]!=app["scope"] or old_app["release"]!=app["release"]: raise ValueError("original application binding")
        if original["authority_ref"]!=old_auth["authority_id"] or old_auth["subject_id"]!=old_app["application_id"] or old_auth["object_digest"]!=old_app["record_digest"] or old_auth["action"]!="issue_synthetic_assessment" or old_auth["status"]!="ACTIVE": raise ValueError("original issuance authority invalid")
        if original["review_ref"]!=old_review["review_id"] or old_review["application_id"]!=old_app["application_id"] or old_review["application_digest"]!=old_app["record_digest"] or old_review["reviewer"] in {old_review["author"],old_review["controller"],old_review["domain_expert"]} or old_review["domain_expert"] in {old_review["author"],old_review["controller"]}: raise ValueError("original independent review invalid")
        if original["bundle_digest"]!=old_bundle["record_digest"] or original["maturity_digest"]!=old_maturity["record_digest"] or original["namespace_digest"]!=old_namespace["record_digest"] or original["public_claim_ref"]!=old_claim["evidence_id"] or old_claim["certificate_id"]!=original["certificate_id"]: raise ValueError("original certificate evidence binding")
        if not (at(old_app["issued_at"])<=at(old_auth["issued_at"])<=at(old_bundle["issued_at"])<=at(old_maturity["issued_at"])<=at(old_namespace["issued_at"])<=at(old_review["issued_at"])<=at(original["issued_at"])<at(original["expires_at"])): raise ValueError("original certificate causal window invalid")
        if review["reviewer"] in {review["author"],review["controller"],review["domain_expert"]} or review["domain_expert"] in {review["author"],review["controller"]}: raise ValueError("renewal independent review invalid")
        if request["previous_certificate_ref"]!=original["certificate_id"] or request["current_certificate_ref"]!=cert["certificate_id"] or request["independent_review_ref"]!=review["review_id"] or request["issuance_authority_ref"]!=cert["authority_ref"]: raise ValueError("renewal request binding")
        order=control["lifecycle_order"]; kinds=[x["kind"] for x in order]; expected=["ORIGINAL_CERTIFICATE_ISSUED","RENEWAL_REQUESTED","INDEPENDENT_REVIEW_RECORDED","RENEWED_CERTIFICATE_ISSUED","RENEWED_CERTIFICATE_ACTIVATED","ORIGINAL_CERTIFICATE_EXPIRES"]
        times=[at(x["occurred_at"]) for x in order]
        if kinds!=expected or times!=sorted(times) or len(set(times))!=len(times): raise ValueError("renewal lifecycle order invalid")
        if not (at(original["issued_at"])<at(request["requested_at"])<at(review["issued_at"])<at(cert["issued_at"])<at(original["expires_at"])): raise ValueError("renewal temporal window invalid")
        if order[0]["occurred_at"]!=original["issued_at"] or order[1]["occurred_at"]!=request["requested_at"] or order[2]["occurred_at"]!=review["issued_at"] or order[3]["occurred_at"]!=cert["issued_at"] or order[4]["occurred_at"]!=state["lifecycle"]["occurred_at"] or order[5]["occurred_at"]!=original["expires_at"]: raise ValueError("renewal lifecycle record binding")
        active_issue(state,request["issuance_authority_ref"],cert["issued_at"]); disposition(control,state); positive_trial("S24-059")
        if enforce_plan: plan_bound(state,control)
        return True

    def validate_recert(control,state=recert_state,enforce_plan=True):
        if control["schema"]!="c24.cert.positive-control.v2.7" or control["kind"]!="LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION": raise ValueError("recert control identity")
        app=state["application"]; change=state["change"]; cert=state["certificate_registry"][state["certificate_ref"]]; review=state["review_registry"].get(change["retest_review_ref"]); entries=change["retest_manifest"]["entries"]
        if not change["material"] or change["impact_review"]!="PASS" or change["retest"]!="PASS": raise ValueError("material change decision invalid")
        if control["application_id"]!=app["application_id"] or control["change_ref"]!=change["change_id"] or control["post_change_release"]!=app["release"] or change["post_change_release"]!=app["release"]: raise ValueError("post-change release binding")
        if set(control["required_layers"])!={"training","regression","holdout"} or set(change["retest_manifest"]["required_layers"])!=set(control["required_layers"]): raise ValueError("three-layer retest incomplete")
        if set(control["required_security_slices"])!={"certification-redteam"} or set(change["retest_manifest"]["required_security_slices"])!=set(control["required_security_slices"]): raise ValueError("security slice contract invalid")
        if {x["layer"] for x in entries}!={"training","regression","holdout"} or {x["trial_ref"] for x in entries}!=set(control["trial_refs"]) or {x["evidence_ref"] for x in entries}!=set(control["output_refs"]): raise ValueError("retest entry projection invalid")
        change_time=at(change["issued_at"]); latest=change_time
        for entry in entries:
            trial=state["trial_registry"].get(entry["trial_ref"]); output=state["evidence_registry"].get(entry["evidence_ref"])
            if not trial or not output or trial["output_ref"]!=entry["evidence_ref"] or trial["layer"]!=entry["layer"] or trial["release"]!=app["release"] or output["object_version"]!=app["release"]: raise ValueError("trial/output/release binding invalid")
            if not set(entry["security_slices"])>=set(control["required_security_slices"]): raise ValueError("entry security slice missing")
            if not (change_time<at(trial["completed_at"])<=at(output["issued_at"])): raise ValueError("post-change trial/output order invalid")
            latest=max(latest,at(output["issued_at"]))
        if not review or review["review_id"]!=control["independent_review_ref"] or at(review["issued_at"])<=latest: raise ValueError("post-change independent review timing invalid")
        if review["reviewer"] in {review["author"],review["controller"],review["domain_expert"],change["owner"]}: raise ValueError("post-change independent review conflict")
        if not (at(review["issued_at"])<at(cert["issued_at"])<=at(state["lifecycle"]["occurred_at"])): raise ValueError("review/certificate/lifecycle order invalid")
        active_issue(state,control["issuance_authority_ref"],cert["issued_at"]); disposition(control,state); positive_trial("S24-060")
        if enforce_plan: plan_bound(state,control)
        return True

    validators={"LEGAL_RENEWAL":validate_renewal,"LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION":validate_recert}
    for kind,validator in validators.items():
        control=controls[kind]; passed=False; message=""
        try: passed=bool(validator(control))
        except (ValueError,TypeError,KeyError) as exc: message=str(exc)
        positives.append({"test_id":"P27-RENEWAL" if kind=="LEGAL_RENEWAL" else "P27-MATERIAL-RECERT","kind":kind,"passed":passed,"message":message})

    def contract_attack(test_id,family,kind,mutate,state_mutate=None):
        control=copy.deepcopy(controls[kind]); state=copy.deepcopy(renewal_state if kind=="LEGAL_RENEWAL" else recert_state); message=""; accepted=False
        try:
            mutate(control)
            if state_mutate: state_mutate(state)
            if kind=="LEGAL_RENEWAL": validate_renewal(control,state)
            else: validate_recert(control,state)
            accepted=True
        except (ValueError,TypeError,KeyError) as exc: message=str(exc)
        attacks.append({"test_id":test_id,"family":family,"actual":"ACCEPTED" if accepted else "REJECT","secure":not accepted,"escape":accepted,"message":message})

    contract_attack("V27-001","renewal-identity","LEGAL_RENEWAL",lambda c:c["original_certificate"].update(certificate_id=c["renewal_request"]["current_certificate_ref"]))
    contract_attack("V27-002","renewal-window","LEGAL_RENEWAL",lambda c:c["renewal_request"].update(requested_at=c["original_certificate"]["expires_at"]))
    contract_attack("V27-003","renewal-window","LEGAL_RENEWAL",lambda c:c["original_certificate"].update(expires_at="2026-09-30T10:59:00Z"))
    contract_attack("V27-004","renewal-dag","LEGAL_RENEWAL",lambda c:c["lifecycle_order"].__setitem__(3,copy.deepcopy(c["lifecycle_order"][2])))
    contract_attack("V27-005","renewal-review","LEGAL_RENEWAL",lambda c:c["original_review"].update(reviewer=c["original_review"]["author"]))
    contract_attack("V27-006","renewal-review","LEGAL_RENEWAL",lambda c:None,lambda s:next(iter(s["review_registry"].values())).update(reviewer=s["application"]["author"]))
    contract_attack("V27-007","renewal-authority","LEGAL_RENEWAL",lambda c:c["renewal_request"].update(issuance_authority_ref="AUTH-UNKNOWN"))
    contract_attack("V27-008","renewal-na","LEGAL_RENEWAL",lambda c:c["representative_real_world"].update(reason=""))
    contract_attack("V27-009","renewal-na","LEGAL_RENEWAL",lambda c:c["representative_real_world"].update(policy_authority_ref="POLICY-UNKNOWN"))
    contract_attack("V27-010","renewal-plan-binding","LEGAL_RENEWAL",lambda c:c.update(control_id="C24-POS-RENEWAL-FORGED"))
    contract_attack("V27-011","recert-layer","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:c["required_layers"].remove("holdout"))
    contract_attack("V27-012","recert-release","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:c.update(post_change_release="openclaw@forged"))
    contract_attack("V27-013","recert-security","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:c.update(required_security_slices=[]))
    contract_attack("V27-014","recert-output","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:c["output_refs"].__setitem__(1,c["output_refs"][0]))
    contract_attack("V27-015","recert-na","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:c["representative_real_world"].update(approval_authority_ref="AUTH-UNKNOWN"))
    contract_attack("V27-016","recert-na","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:c["representative_real_world"].update(status="PASS"))
    def remove_security(state): state["change"]["retest_manifest"]["entries"][0]["security_slices"]=[]
    contract_attack("V27-017","recert-security","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:None,remove_security)
    def output_before_change(state):
        ref=state["change"]["retest_trial_refs"][0]; trial=state["trial_registry"][ref]; trial["completed_at"]="2026-09-30T09:34:00Z"; state["evidence_registry"][trial["output_ref"]]["issued_at"]="2026-09-30T09:34:30Z"
    contract_attack("V27-018","recert-causality","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:None,output_before_change)
    def review_before_outputs(state): next(iter(state["review_registry"].values()))["issued_at"]="2026-09-30T10:20:00Z"
    contract_attack("V27-019","recert-review","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:None,review_before_outputs)
    def cert_before_review(state): state["certificate_registry"][state["certificate_ref"]]["issued_at"]="2026-09-30T10:49:00Z"
    contract_attack("V27-020","recert-causality","LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION",lambda c:None,cert_before_review)

    # The two positive scenarios also remain fully accepted by the canonical
    # source+root result verifier, not merely by the author-side control checks.
    full_replay=bool(r.verify_result(copy.deepcopy(saved),authority,source))
    payload={"schema":"c24.cert.v2.7-positive-control-regression.v1","scope":"offline_synthetic_author_only","fixed_trial_count":saved["trial_count"],"fixed_distribution":saved["distribution"],"fixed_lifecycle_distribution":saved["lifecycle_distribution"],"attack_count":len(attacks),"secure_count":sum(x["secure"] for x in attacks),"escape_count":sum(x["escape"] for x in attacks),"positive_count":len(positives),"positive_pass_count":sum(x["passed"] for x in positives),"full_result_replay_passed":full_replay,"attacks":attacks,"positive_controls":positives,"limits":{"representative_real_world_executed":False,"real_certificate_issued":False,"external_effects_executed":False,"practice_gate":"REVIEW_REQUIRED","author_self_approval":False}}
    payload["suite_digest"]=r.sha({"attacks":attacks,"positive_controls":positives,"full_result_replay_passed":full_replay})
    Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:payload[k] for k in ("attack_count","secure_count","escape_count","positive_count","positive_pass_count","full_result_replay_passed","suite_digest")},ensure_ascii=False))
    return 0 if payload["escape_count"]==0 and payload["positive_pass_count"]==payload["positive_count"] and full_replay else 1


if __name__=="__main__": raise SystemExit(main())
