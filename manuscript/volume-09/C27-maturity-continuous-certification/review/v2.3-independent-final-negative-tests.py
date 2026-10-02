#!/usr/bin/env python3
"""Unannounced non-author near-neighbour tests for C24 v2.3.

Reviewer oracles are stated in this file and are not read from fixture names,
mutation labels, or author-side expected values.  Semantic evaluation is kept
separate from frozen-root rejection so a root mismatch cannot hide fail-open
certification logic.
"""
from __future__ import annotations

import argparse, copy, hashlib, importlib.util, json
from collections import Counter
from pathlib import Path


def load(path: Path):
    spec=importlib.util.spec_from_file_location("c24_v23_independent_final_runner",path)
    module=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(module); return module


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True); p.add_argument("--authority",required=True)
    p.add_argument("--runner",required=True); p.add_argument("--result",required=True)
    p.add_argument("--output",required=True); z=p.parse_args()
    input_path=Path(z.input); authority_path=Path(z.authority); runner_path=Path(z.runner); result_path=Path(z.result)
    r=load(runner_path); raw_source=json.loads(input_path.read_text()); raw_authority=json.loads(authority_path.read_text()); saved=json.loads(result_path.read_text())
    authority=r.validate_authority(copy.deepcopy(raw_authority)); source=r.validate(copy.deepcopy(raw_source),authority); r.verify_result(copy.deepcopy(saved),authority)
    by_id={x["scenario_id"]:x for x in source["scenarios"]}
    active_id=next(x["scenario_id"] for x in saved["trials"] if x["decision"]=="PASS" and x["lifecycle"]=="ACTIVE")
    expired_id=next(x["scenario_id"] for x in saved["trials"] if x["decision"]=="PASS" and x["lifecycle"]=="EXPIRED")
    active=by_id[active_id]; expired=by_id[expired_id]

    def seal(row,field="record_digest"): row[field]=r.sha({k:v for k,v in row.items() if k!=field})
    def auth(state,action): return next(x for x in state["authority_registry"].values() if x["action"]==action)
    def evidence(state,kind): return next(x for x in state["evidence_registry"].values() if x["kind"]==kind)
    rows=[]

    def semantic(test_id,family,mutate,*,control=active,secure=lambda decision,lifecycle,reasons: decision!="PASS"):
        scenario=copy.deepcopy(control); state=scenario["state"]; actual="ERROR"; lifecycle="REVOKED"; reasons=[]; message=""
        frozen=authority["scenario_registry"].get(scenario["scenario_id"])
        try:
            mutate(state); checked=r.validate_state(state,"v23-independent."+test_id)
            actual,lifecycle,reasons,*_=r.evaluate(source,checked,scenario["layer"],authority)
        except (ValueError,TypeError,KeyError) as exc:
            actual="SCHEMA_REJECT"; message=str(exc); reasons=[message]
        blackbox_rejects=not bool(frozen and frozen["status"]=="ACTIVE" and frozen["state_digest"]==r.raw_sha(state))
        ok=bool(secure(actual,lifecycle,reasons))
        rows.append({"test_id":test_id,"family":family,"layer":"semantic_legal_reseal","actual_decision":actual,"actual_lifecycle":lifecycle,"actual_reasons":reasons,"secure_contract_passed":ok,"escape":not ok,"blackbox_frozen_binding_rejects":blackbox_rejects,"message":message})

    def zero_duration_expired(state):
        cert=state["certificate_registry"][state["certificate_ref"]]
        cert.update(issued_at="2026-09-30T11:50:00Z",expires_at="2026-09-30T11:50:00Z",lifecycle="EXPIRED",public_claim="synthetic assessment expired")
        claim=state["evidence_registry"][cert["public_claim_ref"]]; claim["content_digest"]=r.sha(cert["public_claim"]); seal(claim); seal(cert)
        life=state["lifecycle"]; life.update(current="EXPIRED",kind="EXPIRE",occurred_at="2026-09-30T11:50:00Z"); seal(life)
        ev=state["evidence_registry"][life["evidence_ref"]]; ev["content_digest"]=r.sha(r.lifecycle_payload(life)); seal(ev)

    def exceeds_common_window(state):
        cert=state["certificate_registry"][state["certificate_ref"]]; cert["expires_at"]="2026-10-30T00:00:01Z"; seal(cert)

    def alias_role(state,role,application_field,authority_action,review_field=None):
        principal_id=state["application"][application_field]; alias=principal_id+".ALIAS.V23"
        principal=state["principal_registry"][principal_id]; principal["roles"]=sorted(set(principal["roles"]+[role])); principal["aliases"].append(alias); seal(principal)
        if authority_action:
            row=auth(state,authority_action); row["actor"]=alias; seal(row)
        if review_field:
            review=next(iter(state["review_registry"].values())); review[review_field]=alias; seal(review)
        return alias

    def lifecycle_alias_author(state): alias_role(state,"lifecycle_owner","author","change_certificate_lifecycle")
    def reviewer_alias_author(state): alias_role(state,"reviewer","author",None,"reviewer")
    def change_alias_author(state):
        alias=alias_role(state,"change_owner","author",None); principal=state["principal_registry"][state["application"]["author"]]; principal["roles"].append("change_approver"); principal["roles"]=sorted(set(principal["roles"])); seal(principal)
        state["change"]["owner"]=alias; seal(state["change"]); row=auth(state,"approve_material_change"); row["actor"]=alias; seal(row)
        ev=state["evidence_registry"][state["change"]["evidence_ref"]]; ev["content_digest"]=r.sha(r.change_payload(state["application"],state["change"])); seal(ev)

    def material_lineage(state,mode):
        app=state["application"]; ch=state["change"]; trials=list(state["trial_registry"].values()); review=next(iter(state["review_registry"].values()))
        trial=trials[0]; trial["completed_at"]="2026-09-30T11:20:00Z"; seal(trial)
        if mode=="matching_output": ev=state["evidence_registry"][trial["output_ref"]]
        elif mode=="mismatched_output": ev=state["evidence_registry"][trials[1]["output_ref"]]
        else: ev=state["evidence_registry"][state["certificate_registry"][state["certificate_ref"]]["public_claim_ref"]]
        ev["issued_at"]="2026-09-30T11:21:00Z"; seal(ev)
        ch.update(material=True,kind="MODEL",impact_review="PASS",retest="PASS",issued_at="2026-09-30T11:05:00Z",affected_scopes=["MODEL"],post_change_release=app["release"],retest_trial_refs=[trial["trial_id"]],retest_evidence_refs=[ev["evidence_id"]],retest_review_ref=review["review_id"]); seal(ch)
        cev=state["evidence_registry"][ch["evidence_ref"]]; cev["content_digest"]=r.sha(r.change_payload(app,ch)); seal(cev)

    def external_contradiction(state,status,top_external=True):
        app=state["application"]; obs={"effect_id":"EFFECT.INDEPENDENT.V23","status":"APPLIED","external":True,"environment":"external"}
        effect={"effect_id":obs["effect_id"],"application_id":app["application_id"],"external":top_external,"status":status,"environment":"external","receipt":copy.deepcopy(obs),"receipt_digest":r.sha(obs),"readback":copy.deepcopy(obs),"readback_digest":r.sha(obs)}; seal(effect); state["effect_ledger"]=[effect]

    semantic("N01_ZERO_DURATION_EXPIRED_CERTIFICATE","certificate-window",zero_duration_expired)
    semantic("N02_CERTIFICATE_EXCEEDS_COMMON_WINDOW_BY_ONE_SECOND","certificate-window",exceeds_common_window)
    semantic("N03_LIFECYCLE_OWNER_AUTHOR_ALIAS","alias-canonicalization",lifecycle_alias_author)
    semantic("N04_REVIEWER_AUTHOR_ALIAS","alias-canonicalization",reviewer_alias_author)
    semantic("N05_CHANGE_OWNER_APPROVER_AUTHOR_ALIAS","alias-canonicalization",change_alias_author)
    semantic("N06_MATERIAL_CHANGE_SINGLE_TRAINING_TRIAL","post-change-lineage",lambda s:material_lineage(s,"matching_output"))
    semantic("N07_MATERIAL_CHANGE_MISMATCHED_TRIAL_OUTPUT","post-change-lineage",lambda s:material_lineage(s,"mismatched_output"))
    semantic("N08_MATERIAL_CHANGE_PUBLIC_CLAIM_AS_RETEST_EVIDENCE","post-change-lineage",lambda s:material_lineage(s,"public_claim"))
    semantic("N09_EXTERNAL_NONE_WITH_APPLIED_OBSERVATIONS","external-effect-derivation",lambda s:external_contradiction(s,"NONE"))
    semantic("N10_EXTERNAL_FAILED_WITH_APPLIED_OBSERVATIONS","external-effect-derivation",lambda s:external_contradiction(s,"FAILED"))
    semantic("N11_EXTERNAL_APPLIED_TOP_FALSE","external-effect-derivation",lambda s:external_contradiction(s,"APPLIED",False))

    def result_case(test_id,family,mutate,rehash=True):
        candidate=copy.deepcopy(saved); mutate(candidate)
        if rehash: candidate["decision_digest"]=r.sha(r.result_payload(candidate))
        actual="ACCEPTED"; message=""
        try: r.verify_result(candidate,authority)
        except (ValueError,TypeError,KeyError) as exc: actual="REJECT"; message=str(exc)
        ok=actual=="REJECT"; rows.append({"test_id":test_id,"family":family,"layer":"persisted-result-verifier","actual":actual,"secure_contract_passed":ok,"escape":not ok,"message":message})

    def coherent_real_success(x): x["trials"][0]["successful_real_certificates"]=1; x["successful_real_certificates"]=1
    def coherent_external_success(x): x["trials"][0]["successful_external_effects"]=1; x["successful_external_effects"]=1
    def coherent_observed(x): x["trials"][0]["observed_external_effects"]=1; x["observed_external_effects"]=1
    def coherent_decision(x):
        row=next(y for y in x["trials"] if y["decision"]=="FAIL"); row.update(decision="PASS",lifecycle="ACTIVE",reasons=[])
        x["distribution"]=dict(sorted(Counter(y["decision"] for y in x["trials"]).items())); x["lifecycle_distribution"]=dict(sorted(Counter(y["lifecycle"] for y in x["trials"]).items()))
    result_case("N12_COHERENT_REAL_SUCCESS_REHASH","success-count",coherent_real_success)
    result_case("N13_COHERENT_EXTERNAL_SUCCESS_REHASH","success-count",coherent_external_success)
    result_case("N14_COHERENT_OBSERVED_EXTERNAL_REHASH","success-count",coherent_observed)
    result_case("N15_COHERENT_DECISION_LIFECYCLE_REHASH","result-replay",coherent_decision)
    result_case("N16_STALE_DIGEST_MUTATION","result-digest",lambda x:x.update(trial_count=x["trial_count"]+1),False)

    def serialized(test_id,family,raw,kind):
        actual="ACCEPTED"; message=""
        try:
            parsed=json.loads(raw)
            if kind=="input": r.validate(parsed,authority)
            elif kind=="authority": r.validate_authority(parsed)
            else: r.verify_result(parsed,authority)
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as exc: actual="REJECT"; message=str(exc)
        ok=actual=="REJECT"; rows.append({"test_id":test_id,"family":family,"layer":"serialized-json-boundary","actual":actual,"secure_contract_passed":ok,"escape":not ok,"message":message})

    input_text=input_path.read_text(); authority_text=authority_path.read_text(); result_text=result_path.read_text()
    serialized("N17_INPUT_DUPLICATE_TOP_LEVEL_NOW","json-duplicate-key",input_text.replace("{",'{\n  "now": "1900-01-01T00:00:00Z",',1),"input")
    serialized("N18_INPUT_DUPLICATE_NESTED_BUDGET","json-duplicate-key",input_text.replace('"budget": 100.0','"budget": -1,\n          "budget": 100.0',1),"input")
    serialized("N19_AUTHORITY_DUPLICATE_ROOT_DIGEST","json-duplicate-key",authority_text.replace('"root_digest":','"root_digest": "sha256:'+'0'*64+'",\n  "root_digest":',1),"authority")
    serialized("N20_RESULT_DUPLICATE_TOP_LEVEL_TRIAL_COUNT","json-duplicate-key",result_text.replace("{",'{\n  "trial_count": 999,',1),"result")
    serialized("N21_RESULT_DUPLICATE_NESTED_DECISION","json-duplicate-key",result_text.replace('"decision": "PASS"','"decision": "FAIL",\n      "decision": "PASS"',1),"result")

    positives=[]
    def positive(test_id,mutate):
        scenario=copy.deepcopy(active); state=scenario["state"]; actual="ERROR"; lifecycle="REVOKED"; reasons=[]
        try:
            mutate(state); checked=r.validate_state(state,"positive."+test_id); actual,lifecycle,reasons,*_=r.evaluate(source,checked,scenario["layer"],authority)
        except (ValueError,TypeError,KeyError) as exc: reasons=[str(exc)]
        positives.append({"test_id":test_id,"decision":actual,"lifecycle":lifecycle,"reasons":reasons,"passed":actual=="PASS"})
    positive("P01_UNCHANGED_ACTIVE_PASS",lambda s:None)
    def legal_renewal(state):
        cert=state["certificate_registry"][state["certificate_ref"]]; cert["issued_at"]="2026-09-30T11:52:00Z"; cert["expires_at"]="2026-10-20T00:00:00Z"; seal(cert)
    positive("P02_LEGAL_RENEWAL_PASS",legal_renewal)

    attacks=[x for x in rows]
    payload={"schema":"c24.cert.v2.3-independent-final-negative.v1","review_role":"non_author","oracle_source":"reviewer_defined_without_author_expected","scope":"offline_synthetic_semantic_serialized_and_result_integrity","input_sha256":"sha256:"+hashlib.sha256(input_path.read_bytes()).hexdigest(),"authority_sha256":"sha256:"+hashlib.sha256(authority_path.read_bytes()).hexdigest(),"runner_sha256":"sha256:"+hashlib.sha256(runner_path.read_bytes()).hexdigest(),"result_sha256":"sha256:"+hashlib.sha256(result_path.read_bytes()).hexdigest(),"attack_count":len(attacks),"secure_count":sum(x["secure_contract_passed"] for x in attacks),"escape_count":sum(x["escape"] for x in attacks),"positive_count":len(positives),"positive_pass_count":sum(x["passed"] for x in positives),"attacks":attacks,"positive_controls":positives,"limits":{"real_runtime_executed":False,"real_certificate_issued":False,"real_external_effect_executed":False,"practice_gate":"REVIEW_REQUIRED","editor_chief_rc":"NOT_AUTHORIZED"}}
    payload["suite_digest"]=r.sha({"attacks":attacks,"positive_controls":positives})
    Path(z.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:payload[k] for k in ("attack_count","secure_count","escape_count","positive_count","positive_pass_count","suite_digest")},ensure_ascii=False))
    return 0 if payload["escape_count"]==0 and payload["positive_pass_count"]==payload["positive_count"] else 1


if __name__=="__main__": raise SystemExit(main())
