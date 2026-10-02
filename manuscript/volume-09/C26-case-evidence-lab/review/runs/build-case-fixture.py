#!/usr/bin/env python3
"""Build the deterministic C23 v2.7 semantic-replay fixture."""
from pathlib import Path
import argparse, importlib.util, json

HERE=Path(__file__).resolve().parent
AUTHORITY_OUTPUT=HERE/"frozen-evidence-root.yaml"
spec=importlib.util.spec_from_file_location("c23runner",HERE/"run-case-harness.py")
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def h(value): return r.digest(value)
def seal(record):
    record=dict(record); record["record_digest"]=h(record); return record

def scenario(n,mode="PASS"):
    p=f"S{n:02d}"; case=f"CASE.RECORD.{p}"; subject=f"SUBJECT.{p}"; run=f"RUN.{p}"
    task=f"TASK.{p}"; trial=f"TRIAL.{p}"; evidence=f"EVIDENCE.{p}"; author=f"PRINCIPAL.AUTHOR.{p}"; authority=f"PRINCIPAL.AUTHORITY.{p}"
    ids={"identity":f"IDENTITY.{p}","authorization":f"AUTHORIZATION.{p}","source":f"SOURCE.{p}","redaction":f"REDACTION.{p}","publication":f"PUBLICATION.{p}","reviewer":f"REVIEWER.{p}","assignment":f"ASSIGNMENT.AUTHOR.{p}","environment":f"ENVIRONMENT.{p}","oc":f"RELEASE.OPENCLAW.{p}","he":f"RELEASE.HERMES.{p}","task_auth":f"AUTHORITY.TASK.{p}","input_auth":f"AUTHORITY.INPUT.{p}","permission_auth":f"AUTHORITY.PERMISSION.{p}","dataset_auth":f"AUTHORITY.DATASET.{p}","grader_auth":f"AUTHORITY.GRADER.{p}","bb":f"BUDGET.BASELINE.{p}","cb":f"BUDGET.CANDIDATE.{p}","d21":f"D21.{p}","migration":f"MIGRATION.{p}","effect":f"EFFECT.{p}"}
    private=h({"private_case":p}); public=h({"public_case":p}); mapping=h({"private":private,"public":public})
    reviewer_principal=f"PRINCIPAL.REVIEWER.{p}"
    task_spec={"task":task}; input_spec={"input":p}; permissions=["READ.SYNTHETIC"]; data_spec={"dataset":"SYNTHETIC","case":p,"rights":"SYNTHETIC_ONLY","environment":"OFFLINE_SYNTHETIC"}; eval_spec={"grader_principal_id":reviewer_principal,"rubric":"FROZEN-C23-V1"}
    task_d=h(task_spec); input_d=h(input_spec); perm_d=h(permissions); data_d=h(data_spec); eval_d=h(eval_spec)
    def evidence_payload(dimension,state):
        return {"dimension":dimension,"state":state,"case_record_id":case,"task_id":task,"run_id":run,"evidence_id":evidence}
    failure_id=f"FAILURE.{p}.01"; trial_ids=[f"TRIAL.{p}.{i:02d}" for i in range(1,4)]
    artifact_payloads=[
      (f"ARTIFACT.PUBLIC.{p}","PUBLIC_CASE",{"public_case":p},"2026-09-30T11:54:00Z"),
      (f"ARTIFACT.TECHNICAL.{p}","TECHNICAL_EVIDENCE",evidence_payload("TECHNICAL","PASS"),"2026-09-30T11:54:10Z"),
      (f"ARTIFACT.DELIVERY.{p}","DELIVERY_EVIDENCE",evidence_payload("DELIVERY","PASS"),"2026-09-30T11:54:20Z"),
      (f"ARTIFACT.ACCEPTANCE.{p}","ACCEPTANCE_EVIDENCE",evidence_payload("ACCEPTANCE","PASS"),"2026-09-30T11:54:30Z"),
      (f"ARTIFACT.FAILURE.{p}","FAILURE_LOG",{"failure_id":failure_id,"trial_id":trial_ids[1],"outcome":"FAIL"},"2026-09-30T11:54:40Z"),
    ]
    artifacts=[seal({"artifact_id":aid,"case_record_id":case,"case_version":1,"task_id":task,"run_id":run,"evidence_id":evidence,"kind":kind,"payload":payload,"content_digest":h(payload),"status":"ACTIVE","source_id":ids["source"],"recorded_at":when}) for aid,kind,payload,when in artifact_payloads]
    authority_refs={"task_authority_ref":ids["task_auth"],"input_authority_ref":ids["input_auth"],"permission_authority_ref":ids["permission_auth"],"dataset_authority_ref":ids["dataset_auth"],"grader_authority_ref":ids["grader_auth"]}
    base_budget={"case_record_id":case,"case_version":1,"task_id":task,"run_id":run,**authority_refs,"task_spec":task_spec,"task_digest":task_d,"input_spec":input_spec,"input_digest":input_d,"risk":"R2","permissions":permissions,"permissions_digest":perm_d,"data_spec":data_spec,"data_digest":data_d,"eval_spec":eval_spec,"eval_digest":eval_d,"model_usd":10,"tool_usd":5,"compute_usd":2,"human_minutes":20,"human_usd":8,"elapsed_seconds":120,"total_usd":25,"status":"ACTIVE"}
    identity={"identity_id":ids["identity"],"case_record_id":case,"case_version":1,"subject_id":subject,"case_type":"SYNTHETIC","missing_elements":[],"inference_list":[],"status":"ACTIVE","revoked_at":None,"authority_principal_id":authority,"source_digest":private}
    authorization={"authorization_id":ids["authorization"],"case_record_id":case,"case_version":1,"subject_id":subject,"principal_id":authority,"scopes":["RUN_SYNTHETIC","PUBLISH_SYNTHETIC","MIGRATE_SYNTHETIC"],"valid_from":"2026-09-01T00:00:00Z","valid_until":"2026-10-31T23:59:59Z","status":"ACTIVE","revoked_at":None,"source_digest":private}
    source={"source_id":ids["source"],"case_record_id":case,"case_version":1,"subject_id":subject,"origin":"SYNTHETIC_BUILDER","authorization_status":"PASS","copyright_status":"PASS","missing_elements":[],"inference_list":[],"status":"ACTIVE","private_content":{"private_case":p},"private_content_digest":private,"authority_principal_id":authority}
    redaction={"redaction_id":ids["redaction"],"case_record_id":case,"case_version":1,"subject_id":subject,"private_content_digest":private,"public_content":{"public_case":p},"public_content_digest":public,"mapping":{"private":private,"public":public},"mapping_digest":mapping,"status":"ACTIVE","authorized_by_principal_id":authority}
    publication={"publication_id":ids["publication"],"case_record_id":case,"case_version":1,"subject_id":subject,"public_artifact_id":f"ARTIFACT.PUBLIC.{p}","public_content_digest":public,"redaction_id":ids["redaction"],"reviewer_id":ids["reviewer"],"authorization_id":ids["authorization"],"scope":"PUBLIC_SYNTHETIC","status":"ACTIVE","released_at":"2026-09-30T11:59:00Z"}
    reviewer={"reviewer_id":ids["reviewer"],"principal_id":reviewer_principal,"aliases":[f"PRINCIPAL.REVIEWER.ALIAS.{p}"],"roles":["ROLE.INDEPENDENT.REVIEWER"],"independence_group":f"GROUP.REVIEW.{p}","reviewed_at":"2026-09-30T11:58:00Z","status":"ACTIVE"}
    principals=[
      seal({"principal_record_id":f"PRINCIPAL.RECORD.AUTHOR.{p}","principal_id":author,"roles":["ROLE.CASE.AUTHOR"],"independence_group":f"GROUP.AUTHOR.{p}","status":"ACTIVE"}),
      seal({"principal_record_id":f"PRINCIPAL.RECORD.AUTHORITY.{p}","principal_id":authority,"roles":["ROLE.CASE.AUTHORITY"],"independence_group":f"GROUP.AUTHORITY.{p}","status":"ACTIVE"}),
      seal({"principal_record_id":f"PRINCIPAL.RECORD.REVIEWER.{p}","principal_id":reviewer["principal_id"],"roles":["ROLE.INDEPENDENT.REVIEWER"],"independence_group":reviewer["independence_group"],"status":"ACTIVE"}),
    ]
    aliases=[
      seal({"alias_record_id":f"ALIAS.RECORD.AUTHOR.{p}","alias_id":f"PRINCIPAL.AUTHOR.ALIAS.{p}","canonical_principal_id":author,"status":"ACTIVE"}),
      seal({"alias_record_id":f"ALIAS.RECORD.AUTHORITY.{p}","alias_id":f"PRINCIPAL.AUTHORITY.ALIAS.{p}","canonical_principal_id":authority,"status":"ACTIVE"}),
      seal({"alias_record_id":f"ALIAS.RECORD.REVIEWER.{p}","alias_id":reviewer["aliases"][0],"canonical_principal_id":reviewer["principal_id"],"status":"ACTIVE"}),
    ]
    assignment={"assignment_id":ids["assignment"],"principal_id":author,"role":"ROLE.CASE.AUTHOR","subject_id":subject,"case_record_id":case,"case_version":1,"valid_from":"2026-09-01T00:00:00Z","valid_until":"2026-10-31T23:59:59Z","status":"ACTIVE"}
    env={"environment_id":ids["environment"],"version":"C23-OFFLINE-1.0","manifest":{"environment":p,"version":"1.0"},"manifest_digest":h({"environment":p,"version":"1.0"}),"mode":"OFFLINE_SYNTHETIC","network_accessed":False,"real_credentials_used":False,"production_write":False,"status":"ACTIVE"}
    oc={"release_id":ids["oc"],"platform":"OPENCLAW","version":r.OPENCLAW[0],"commit":r.OPENCLAW[1],"status":"ACTIVE","release_digest":h({"platform":"OPENCLAW","version":r.OPENCLAW[0],"commit":r.OPENCLAW[1]})}
    he={"release_id":ids["he"],"platform":"HERMES","version":r.HERMES[0],"commit":r.HERMES[1],"status":"ACTIVE","release_digest":h({"platform":"HERMES","version":r.HERMES[0],"commit":r.HERMES[1]})}
    task_authority={"task_authority_id":ids["task_auth"],"case_record_id":case,"case_version":1,"task_id":task,"task_spec":task_spec,"task_digest":task_d,"status":"ACTIVE"}
    input_authority={"input_authority_id":ids["input_auth"],"case_record_id":case,"case_version":1,"task_id":task,"input_spec":input_spec,"input_digest":input_d,"status":"ACTIVE"}
    permission_authority={"permission_authority_id":ids["permission_auth"],"case_record_id":case,"case_version":1,"task_id":task,"allowed_permissions":permissions,"permissions_digest":perm_d,"environment_mode":"OFFLINE_SYNTHETIC","status":"ACTIVE"}
    dataset_authority={"dataset_authority_id":ids["dataset_auth"],"case_record_id":case,"case_version":1,"task_id":task,"data_spec":data_spec,"data_digest":data_d,"rights_status":"PASS","allowed_environment_mode":"OFFLINE_SYNTHETIC","allowed_case_types":["RECONSTRUCTED","SYNTHETIC","VENDOR-CLAIM"],"status":"ACTIVE"}
    grader_authority={"grader_authority_id":ids["grader_auth"],"case_record_id":case,"case_version":1,"task_id":task,"grader_principal_id":reviewer_principal,"eval_spec":eval_spec,"eval_digest":eval_d,"independence_required":True,"status":"ACTIVE"}
    bb={"budget_id":ids["bb"],"side":"BASELINE",**base_budget}; cb={"budget_id":ids["cb"],"side":"CANDIDATE",**base_budget}
    d21={"d21_id":ids["d21"],"case_record_id":case,"case_version":1,"task_id":task,"run_id":run,"evidence_id":evidence,"technical":"PASS","delivery":"PASS","business_environment":"PASS","technical_evidence_id":f"ARTIFACT.TECHNICAL.{p}","delivery_evidence_id":f"ARTIFACT.DELIVERY.{p}","acceptance_evidence_id":f"ARTIFACT.ACCEPTANCE.{p}","status":"ACTIVE","recorded_at":"2026-09-30T11:56:00Z"}
    bcontract={"case_record_id":case,"case_version":1,"task_id":task,"run_id":run,**authority_refs,"task_digest":task_d,"input_digest":input_d,"budget_id":ids["bb"],"budget_contract_digest":"PENDING","risk":"R2","permissions_digest":perm_d,"data_digest":data_d,"eval_digest":eval_d}
    ccontract={**bcontract,"budget_id":ids["cb"]}
    migration={"migration_id":ids["migration"],"case_record_id":case,"case_version":1,"task_id":task,"run_id":run,"evidence_id":evidence,"baseline_release_id":ids["oc"],"candidate_release_id":ids["he"],"baseline_contract":bcontract,"candidate_contract":ccontract,"unsupported_capabilities":[],"adapter_differences":[],"status":"ACTIVE"}
    effect_view={"effect_id":ids["effect"],"effect_kind":"NONE","external":False,"authorized":True,"status":"NONE"}
    effect={"effect_id":ids["effect"],"case_record_id":case,"task_id":task,"run_id":run,"evidence_id":evidence,"effect_kind":"NONE","external":False,"authorized":True,"receipt":effect_view,"receipt_digest":h(effect_view),"readback":effect_view,"readback_digest":h(effect_view),"status":"ACTIVE","recorded_at":"2026-09-30T11:55:10Z"}
    trial_records=[seal({"trial_record_id":f"TRIAL.RECORD.{p}.{i:02d}","trial_id":tid,"case_record_id":case,"task_id":task,"run_id":run,"evidence_id":evidence,"status":"FAIL" if i==2 else "PASS","failure_ref":failure_id if i==2 else "NONE","recorded_at":f"2026-09-30T11:{50+i:02d}:00Z"}) for i,tid in enumerate(trial_ids,1)]
    failure_records=[seal({"failure_id":failure_id,"case_record_id":case,"task_id":task,"trial_id":trial_ids[1],"run_id":run,"evidence_id":evidence,"artifact_id":f"ARTIFACT.FAILURE.{p}","status":"ACTIVE","recorded_at":"2026-09-30T11:54:35Z"})]
    trial=trial_ids[0]
    raw={"case_version":1,"subject_id":subject,"author_principal_id":author,"author_assignment_ref":ids["assignment"],"identity_ref":ids["identity"],"authorization_ref":ids["authorization"],"source_ref":ids["source"],"redaction_ref":ids["redaction"],"publication_ref":ids["publication"],"reviewer_ref":ids["reviewer"],"environment_ref":ids["environment"],"baseline_release_ref":ids["oc"],"candidate_release_ref":ids["he"],**authority_refs,"baseline_budget_ref":ids["bb"],"candidate_budget_ref":ids["cb"],"artifact_refs":[x["artifact_id"] for x in artifacts],"d21_ref":ids["d21"],"migration_ref":ids["migration"],"effect_refs":[ids["effect"]],"trial_refs":[x["trial_record_id"] for x in trial_records],"failure_refs":[failure_id],"trial_count":3,"failure_count":1,"failures_preserved":True,"holdout_accessed":False,"grader_private_access":False}
    if mode=="IDENTITY_REVOKED": identity.update(status="REVOKED",revoked_at="2026-09-29T12:00:00Z")
    elif mode=="AUTH_REVOKED": authorization.update(status="REVOKED",revoked_at="2026-09-29T12:00:00Z")
    elif mode=="SOURCE_FAIL": source["authorization_status"]="FAIL"
    elif mode=="BUDGET_UNFAIR": cb.update(model_usd=20,total_usd=35)
    elif mode=="PERMISSION_UNFAIR": cb["permissions"]=["READ.SYNTHETIC","WRITE.PRODUCTION"]; cb["permissions_digest"]=h(cb["permissions"]); migration["candidate_contract"]["permissions_digest"]=cb["permissions_digest"]
    elif mode=="NO_TRIAL": raw["trial_count"]=0; raw["failure_count"]=0
    elif mode=="ARTIFACT_UNKNOWN": artifacts[0].update(status="UNKNOWN"); artifacts[0]=seal({k:v for k,v in artifacts[0].items() if k!="record_digest"})
    elif mode=="D21_UNKNOWN":
        d21["delivery"]="UNKNOWN"
        delivery=next(x for x in artifacts if x["kind"]=="DELIVERY_EVIDENCE")
        delivery["payload"]["state"]="UNKNOWN"; delivery["content_digest"]=h(delivery["payload"]); delivery=seal({k:v for k,v in delivery.items() if k!="record_digest"})
        artifacts=[delivery if x["kind"]=="DELIVERY_EVIDENCE" else x for x in artifacts]
    elif mode=="FAILURE_DELETED": raw["failures_preserved"]=False
    elif mode=="HOLDOUT": raw["holdout_accessed"]=True
    elif mode=="SELF_REVIEW": reviewer["aliases"].append(author)
    elif mode=="REDACTION_MISMATCH": publication["public_content_digest"]=h({"different":"public"})
    elif mode=="VENDOR": identity["case_type"]="VENDOR-CLAIM"; source["origin"]="VENDOR_PUBLIC_PAGE"
    elif mode=="IDENTITY_UNKNOWN": identity["status"]="UNKNOWN"; source["status"]="UNKNOWN"
    elif mode=="COMBINED": raw["holdout_accessed"]=True; reviewer["aliases"].append(author)
    elif mode=="REVOKED_BASELINE": oc["status"]="REVOKED"
    elif mode=="REVOKED_CANDIDATE": he["status"]="REVOKED"
    elif mode=="REVIEWER_NO_ROLE": reviewer["roles"]=["ROLE.CASE.AUTHOR"]; principals[2]["roles"]=["ROLE.CASE.AUTHOR"]; principals[2]=seal({k:v for k,v in principals[2].items() if k!="record_digest"})
    elif mode=="EFFECT_REVOKED": effect["status"]="REVOKED"
    elif mode=="EFFECT_INTERNAL_MISMATCH": effect["effect_kind"]="SYNTHETIC_WRITE"; effect["receipt"]={**effect_view,"effect_kind":"SYNTHETIC_WRITE","status":"APPLIED"}; effect["receipt_digest"]=h(effect["receipt"])
    elif mode=="BUDGET_REVOKED": bb["status"]="REVOKED"; cb["status"]="REVOKED"
    elif mode=="ADAPTER_DIFF": migration["adapter_differences"]=[{"category":"STATE_CARRIER","criticality":"NON_CRITICAL","affected_contract":"STATE_TRANSPORT","evidence_ref":f"ARTIFACT.TECHNICAL.{p}","owner":authority,"disposition":"REVIEW_REQUIRED"}]
    elif mode=="UNBOUND_IDS": task=f"TASK.UNBOUND.{p}"; evidence=f"EVIDENCE.UNBOUND.{p}"
    elif mode=="FAKE_DISTRIBUTION": raw["trial_count"]=99; raw["failure_count"]=0; raw["failures_preserved"]=False
    elif mode=="FUTURE_PUBLICATION": publication["released_at"]="2026-09-30T12:01:00Z"
    elif mode=="UNKNOWN_RELEASE": he["status"]="UNKNOWN"
    elif mode=="UNKNOWN_BUDGET": cb["status"]="UNKNOWN"
    elif mode=="CRITICAL_ADAPTER": migration["adapter_differences"]=[{"category":"PERMISSION","criticality":"CRITICAL","affected_contract":"PERMISSIONS","evidence_ref":f"ARTIFACT.TECHNICAL.{p}","owner":authority,"disposition":"FAIL"}]
    elif mode=="INTERNAL_UNAUTHORIZED": effect["authorized"]=False; effect["receipt"]={**effect_view,"authorized":False}; effect["receipt_digest"]=h(effect["receipt"]); effect["readback"]={**effect_view,"authorized":False}; effect["readback_digest"]=h(effect["readback"])
    elif mode=="TRIAL_EVIDENCE_MISMATCH": trial_records[0]["evidence_id"]="EVIDENCE.WRONG"; trial_records[0]=seal({k:v for k,v in trial_records[0].items() if k!="record_digest"})
    contract_keys=("case_record_id","case_version","task_id","run_id","side","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","task_digest","input_digest","risk","permissions_digest","data_digest","eval_digest","model_usd","tool_usd","compute_usd","human_minutes","human_usd","elapsed_seconds","total_usd")
    for budget in (bb,cb): budget["contract_digest"]=h({k:budget[k] for k in contract_keys})
    migration["baseline_contract"]["budget_contract_digest"]=bb["contract_digest"]
    migration["candidate_contract"]["budget_contract_digest"]=cb["contract_digest"]
    records={"case_identity_registry":[seal(identity)],"authorization_registry":[seal(authorization)],"source_registry":[seal(source)],"redaction_registry":[seal(redaction)],"publication_registry":[seal(publication)],"reviewer_registry":[seal(reviewer)],"principal_registry":principals,"alias_registry":aliases,"author_assignment_registry":[seal(assignment)],"environment_registry":[seal(env)],"release_registry":[seal(oc),seal(he)],"task_authority_registry":[seal(task_authority)],"input_authority_registry":[seal(input_authority)],"permission_authority_registry":[seal(permission_authority)],"dataset_authority_registry":[seal(dataset_authority)],"grader_authority_registry":[seal(grader_authority)],"budget_registry":[seal(bb),seal(cb)],"artifact_registry":artifacts,"d21_registry":[seal(d21)],"migration_registry":[seal(migration)],"effect_registry":[seal(effect)],"trial_registry":trial_records,"failure_registry":failure_records}
    s={"scenario_id":p,"case_record_id":case,"task_id":task,"trial_id":trial,"run_id":run,"evidence_id":evidence,"raw_state":raw}
    return s,records

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--input-output",default=str(HERE/"synthetic-case-input.yaml")); parser.add_argument("--authority-output",default=str(AUTHORITY_OUTPUT)); args=parser.parse_args()
    modes=["PASS","IDENTITY_REVOKED","AUTH_REVOKED","SOURCE_FAIL","BUDGET_UNFAIR","PERMISSION_UNFAIR","NO_TRIAL","ARTIFACT_UNKNOWN","D21_UNKNOWN","FAILURE_DELETED","HOLDOUT","SELF_REVIEW","REDACTION_MISMATCH","VENDOR","IDENTITY_UNKNOWN","COMBINED","PASS","REVOKED_BASELINE","REVOKED_CANDIDATE","REVIEWER_NO_ROLE","EFFECT_REVOKED","EFFECT_INTERNAL_MISMATCH","BUDGET_REVOKED","ADAPTER_DIFF","UNBOUND_IDS","FAKE_DISTRIBUTION","FUTURE_PUBLICATION","UNKNOWN_RELEASE","UNKNOWN_BUDGET","CRITICAL_ADAPTER","INTERNAL_UNAUTHORIZED","TRIAL_EVIDENCE_MISMATCH"]
    registries={k:[] for k in ["case_identity_registry","authorization_registry","source_registry","redaction_registry","publication_registry","reviewer_registry","principal_registry","alias_registry","author_assignment_registry","environment_registry","release_registry","task_authority_registry","input_authority_registry","permission_authority_registry","dataset_authority_registry","grader_authority_registry","budget_registry","artifact_registry","d21_registry","migration_registry","effect_registry","trial_registry","failure_registry"]}; scenarios=[]
    for n,mode in enumerate(modes,1):
        s,recs=scenario(n,mode); scenarios.append(s)
        for k,v in recs.items(): registries[k].extend(v)
    registries["real_case_manifest"]=[]
    suite={"suite_id":"SUITE.C23.CASE.V27","build_id":"BUILD.C23.20261001.V27","evaluation_time":"2026-09-30T12:00:00Z"}
    doc={"schema_version":r.SCHEMA,"suite":suite,"environment":{"mode":"OFFLINE_SYNTHETIC","offline":True,"network_accessed":False,"real_credentials_used":False,"production_write":False},"registries":registries,"scenarios":scenarios}
    authority_root={"schema_version":r.AUTHORITY_SCHEMA,"suite_manifest":r.suite_manifest(suite,scenarios),"registries":registries}
    authority_root["root_digest"]=h(r.root_payload(authority_root))
    Path(args.authority_output).write_text(json.dumps(authority_root,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    Path(args.input_output).write_text(json.dumps(doc,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(authority_root["root_digest"])
if __name__=="__main__": main()
