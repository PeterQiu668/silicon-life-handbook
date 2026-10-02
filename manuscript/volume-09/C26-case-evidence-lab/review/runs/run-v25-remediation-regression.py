#!/usr/bin/env python3
"""C23 v2.5 author remediation regression.

The suite starts from S01, re-seals every changed record and re-pins a complete
authority root.  Serialized attacks are kept as hostile bytes until the strict
duplicate-key loader runs.  No case name or expected result participates in the
production decision.
"""
from pathlib import Path
import argparse, copy, importlib.util, json


def load(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True); p.add_argument("--authority-root",required=True)
    p.add_argument("--runner",required=True); p.add_argument("--output",required=True)
    a=p.parse_args(); r=load(Path(a.runner),"c23_v25_runner")
    base=r.strict_json_loads(Path(a.input).read_text()); authority=r.strict_json_loads(Path(a.authority_root).read_text())
    baseline=r.evaluate(copy.deepcopy(base),copy.deepcopy(authority))

    def seal(record):
        record["record_digest"]=r.digest({k:v for k,v in record.items() if k!="record_digest"})
    def s01(doc): return next(x for x in doc["scenarios"] if x["scenario_id"]=="S01")
    def rec(doc,registry,key,value): return next(x for x in doc["registries"][registry] if x[key]==value)
    def art(doc,aid): return rec(doc,"artifact_registry","artifact_id",aid)
    def repin(doc,root):
        root["registries"]=copy.deepcopy(doc["registries"])
        root["suite_manifest"]=r.suite_manifest(doc["suite"],doc["scenarios"])
        root["root_digest"]=r.digest(r.root_payload(root)); r.PINNED_AUTHORITY_ROOT_DIGEST=root["root_digest"]

    def duplicate_technical(doc):
        x=copy.deepcopy(art(doc,"ARTIFACT.TECHNICAL.S01")); x["artifact_id"]="ARTIFACT.TECHNICAL.DUP.S01"; seal(x)
        doc["registries"]["artifact_registry"].append(x); s01(doc)["raw_state"]["artifact_refs"].append(x["artifact_id"])
    def duplicate_principal(doc):
        x=copy.deepcopy(rec(doc,"principal_registry","principal_id","PRINCIPAL.AUTHOR.S01")); x["principal_record_id"]="PRINCIPAL.RECORD.AUTHOR.DUP.S01"; seal(x); doc["registries"]["principal_registry"].append(x)
    def extra_release(doc):
        x=copy.deepcopy(rec(doc,"release_registry","release_id","RELEASE.OPENCLAW.S01")); x["release_id"]="RELEASE.OPENCLAW.EXTRA.S01"; seal(x); doc["registries"]["release_registry"].append(x)
    def extra_budget(doc):
        x=copy.deepcopy(rec(doc,"budget_registry","budget_id","BUDGET.BASELINE.S01")); x["budget_id"]="BUDGET.EXTRA.S01"; seal(x); doc["registries"]["budget_registry"].append(x)
    def d21_before_support(doc):
        x=rec(doc,"d21_registry","d21_id","D21.S01"); x["recorded_at"]="2026-09-30T11:54:00Z"; seal(x)
    def d21_before_effect(doc):
        x=rec(doc,"d21_registry","d21_id","D21.S01"); x["recorded_at"]="2026-09-30T11:55:00Z"; seal(x)
    def failure_before_trial(doc):
        x=rec(doc,"failure_registry","failure_id","FAILURE.S01.01"); x["recorded_at"]="2026-09-30T11:51:30Z"; seal(x)
    def log_before_failure(doc):
        x=art(doc,"ARTIFACT.FAILURE.S01"); x["recorded_at"]="2026-09-30T11:54:30Z"; seal(x)
    def adapter_public(doc):
        x=rec(doc,"migration_registry","migration_id","MIGRATION.S01"); x["adapter_differences"]=[{"category":"TOOL_SCHEMA","criticality":"NON_CRITICAL","affected_contract":"TOOL_INTERFACE","evidence_ref":"ARTIFACT.PUBLIC.S01","owner":"PRINCIPAL.AUTHORITY.S01","disposition":"ACCEPTED"}]; seal(x)
    def adapter_failure_log(doc):
        x=rec(doc,"migration_registry","migration_id","MIGRATION.S01"); x["adapter_differences"]=[{"category":"TOOL_SCHEMA","criticality":"NON_CRITICAL","affected_contract":"TOOL_INTERFACE","evidence_ref":"ARTIFACT.FAILURE.S01","owner":"PRINCIPAL.AUTHORITY.S01","disposition":"ACCEPTED"}]; seal(x)
    def baseline_contract_forged(doc):
        x=rec(doc,"migration_registry","migration_id","MIGRATION.S01"); x["baseline_contract"]["task_digest"]=r.digest({"forged":"baseline"}); seal(x)
    def candidate_contract_forged(doc):
        x=rec(doc,"migration_registry","migration_id","MIGRATION.S01"); x["candidate_contract"]["task_digest"]=r.digest({"forged":"candidate"}); seal(x)
    def model_tool_swap(doc):
        x=rec(doc,"budget_registry","budget_id","BUDGET.CANDIDATE.S01"); x["model_usd"]+=1; x["tool_usd"]-=1; seal(x)
    def human_compute_swap(doc):
        x=rec(doc,"budget_registry","budget_id","BUDGET.CANDIDATE.S01"); x["human_usd"]+=1; x["compute_usd"]-=1; seal(x)
    def human_time_mismatch(doc):
        x=rec(doc,"budget_registry","budget_id","BUDGET.CANDIDATE.S01"); x["human_minutes"]+=1; seal(x)
    def resource_permission_mismatch(doc):
        x=rec(doc,"budget_registry","budget_id","BUDGET.CANDIDATE.S01"); x["permissions"]=["READ.SYNTHETIC","WRITE.SYNTHETIC"]; x["permissions_digest"]=r.digest(x["permissions"]); seal(x)
    def vendor_under_synthetic(doc):
        x=rec(doc,"source_registry","source_id","SOURCE.S01"); x["origin"]="VENDOR_PUBLIC_PAGE"; seal(x)
    def reconstruction_under_synthetic(doc):
        x=rec(doc,"source_registry","source_id","SOURCE.S01"); x["origin"]="RECONSTRUCTION"; seal(x)
    def vendor_claim_adapter(doc):
        ident=rec(doc,"case_identity_registry","identity_id","IDENTITY.S01"); ident["case_type"]="VENDOR-CLAIM"; seal(ident)
        source=rec(doc,"source_registry","source_id","SOURCE.S01"); source["origin"]="VENDOR_PUBLIC_PAGE"; seal(source)
        x=rec(doc,"migration_registry","migration_id","MIGRATION.S01"); x["adapter_differences"]=[{"category":"TOOL_SCHEMA","criticality":"NON_CRITICAL","affected_contract":"TOOL_INTERFACE","evidence_ref":"ARTIFACT.TECHNICAL.S01","owner":"PRINCIPAL.AUTHORITY.S01","disposition":"ACCEPTED"}]; seal(x)
    def legal_repin(doc):
        x=rec(doc,"trial_registry","trial_record_id","TRIAL.RECORD.S01.02"); x["recorded_at"]="2026-09-30T11:52:20Z"; seal(x)
    def legal_adapter(doc):
        x=rec(doc,"migration_registry","migration_id","MIGRATION.S01"); x["adapter_differences"]=[{"category":"TOOL_SCHEMA","criticality":"NON_CRITICAL","affected_contract":"TOOL_INTERFACE","evidence_ref":"ARTIFACT.TECHNICAL.S01","owner":"PRINCIPAL.AUTHORITY.S01","disposition":"ACCEPTED"}]; seal(x)

    semantic=[
      ("V25-01_DUPLICATE_TECHNICAL_SEMANTIC",duplicate_technical,{"FAIL","REJECT"}),
      ("V25-02_DUPLICATE_PRINCIPAL_SEMANTIC",duplicate_principal,{"FAIL","REJECT"}),
      ("V25-03_EXTRA_RELEASE_PROJECTION",extra_release,{"FAIL","REJECT"}),
      ("V25-04_EXTRA_BUDGET_PROJECTION",extra_budget,{"FAIL","REJECT"}),
      ("V25-05_D21_BEFORE_SUPPORT",d21_before_support,{"FAIL","REJECT"}),
      ("V25-06_D21_BEFORE_EFFECT",d21_before_effect,{"FAIL","REJECT"}),
      ("V25-07_FAILURE_BEFORE_TRIAL",failure_before_trial,{"FAIL","REJECT"}),
      ("V25-08_FAILURE_LOG_BEFORE_FAILURE",log_before_failure,{"FAIL","REJECT"}),
      ("V25-09_ADAPTER_PUBLIC_CASE",adapter_public,{"FAIL","REVIEW_REQUIRED","REJECT"}),
      ("V25-10_ADAPTER_FAILURE_LOG",adapter_failure_log,{"FAIL","REVIEW_REQUIRED","REJECT"}),
      ("V25-11_BASELINE_CONTRACT_FORGED",baseline_contract_forged,{"FAIL","REJECT"}),
      ("V25-12_CANDIDATE_CONTRACT_FORGED",candidate_contract_forged,{"FAIL","REJECT"}),
      ("V25-13_EQUAL_TOTAL_MODEL_TOOL_SWAP",model_tool_swap,{"FAIL","REJECT"}),
      ("V25-14_EQUAL_TOTAL_HUMAN_COMPUTE_SWAP",human_compute_swap,{"FAIL","REJECT"}),
      ("V25-15_HUMAN_TIME_MISMATCH",human_time_mismatch,{"FAIL","REJECT"}),
      ("V25-16_RESOURCE_PERMISSION_MISMATCH",resource_permission_mismatch,{"FAIL","REJECT"}),
      ("V25-17_VENDOR_SOURCE_SYNTHETIC",vendor_under_synthetic,{"FAIL","REVIEW_REQUIRED","REJECT"}),
      ("V25-18_RECONSTRUCTION_SOURCE_SYNTHETIC",reconstruction_under_synthetic,{"FAIL","REVIEW_REQUIRED","REJECT"}),
      ("V25-19_VENDOR_EVIDENCE_AS_ADAPTER",vendor_claim_adapter,{"FAIL","REVIEW_REQUIRED","REJECT"}),
    ]
    rows=[]; old_pin=r.PINNED_AUTHORITY_ROOT_DIGEST
    for tid,mut,secure in semantic:
        doc=copy.deepcopy(base); root=copy.deepcopy(authority); actual="ERROR"; message=""
        try:
            mut(doc); repin(doc,root); result=r.evaluate(doc,root)
            actual=next(x["derived"]["verdict"] for x in result["trials"] if x["scenario_id"]=="S01")
        except Exception as exc: actual="REJECT"; message=str(exc)
        finally: r.PINNED_AUTHORITY_ROOT_DIGEST=old_pin
        rows.append({"test_id":tid,"layer":"semantic_legal_repin","actual":actual,"secure_expected_outcomes":sorted(secure),"secure_contract_passed":actual in secure,"message":message})

    baseline_text=json.dumps(baseline,ensure_ascii=False,indent=2,sort_keys=True)
    input_text=json.dumps(base,ensure_ascii=False,indent=2,sort_keys=True)
    root_text=json.dumps(authority,ensure_ascii=False,indent=2,sort_keys=True)
    serialized=[
      ("V25-20_INPUT_DUPLICATE_TOP",input_text.replace("{",'{\n  "schema_version": "hostile",',1),"input"),
      ("V25-21_INPUT_DUPLICATE_NESTED",input_text.replace('"case_version": 1','"case_version": 99,\n        "case_version": 1',1),"input"),
      ("V25-22_RESULT_DUPLICATE_TOP",baseline_text.replace("{",'{\n  "trial_count": 999,',1),"result"),
      ("V25-23_RESULT_DUPLICATE_PROVENANCE",baseline_text.replace('"authority_root_digest":','"authority_root_digest": "'+'0'*64+'",\n    "authority_root_digest":',1),"result"),
      ("V25-24_ROOT_DUPLICATE_TOP",root_text.replace("{",'{\n  "schema_version": "hostile",',1),"root"),
      ("V25-25_ROOT_DUPLICATE_NESTED",root_text.replace('"suite_id":','"suite_id": "hostile",\n    "suite_id":',1),"root"),
    ]
    for tid,raw,kind in serialized:
        actual="ACCEPTED"; message=""
        try:
            obj=r.strict_json_loads(raw)
            if kind=="input": r.evaluate(obj,copy.deepcopy(authority))
            elif kind=="root": r.validate_authority_root(obj)
            else:
                r.verify_result(obj,authority)
                if r.canonical(obj)!=r.canonical(baseline): raise ValueError("result replay mismatch")
        except Exception as exc: actual="REJECT"; message=str(exc)
        rows.append({"test_id":tid,"layer":"serialized_duplicate_key","actual":actual,"secure_expected_outcomes":["REJECT"],"secure_contract_passed":actual=="REJECT","message":message})

    controls=[]
    for tid,mut in (("V25-C01_LEGAL_NEW_ROOT_PASS",legal_repin),("V25-C02_LEGAL_ADAPTER_PASS",legal_adapter)):
        doc=copy.deepcopy(base); root=copy.deepcopy(authority); actual="ERROR"; message=""
        try:
            mut(doc); repin(doc,root); result=r.evaluate(doc,root)
            actual=next(x["derived"]["verdict"] for x in result["trials"] if x["scenario_id"]=="S01")
        except Exception as exc: actual="REJECT"; message=str(exc)
        finally: r.PINNED_AUTHORITY_ROOT_DIGEST=old_pin
        controls.append({"test_id":tid,"layer":"positive_neighbor","actual":actual,"secure_expected_outcomes":["PASS"],"secure_contract_passed":actual=="PASS","message":message})
    rows.extend(controls); attacks=[x for x in rows if x["layer"]!="positive_neighbor"]
    payload={"schema_version":"c23.v2.5.author-remediation-regression.v1","baseline_distribution":baseline["distribution"],"baseline_decision_digest":baseline["decision_digest"],"attack_count":len(attacks),"secure_attack_count":sum(x["secure_contract_passed"] for x in attacks),"escape_count":sum(not x["secure_contract_passed"] for x in attacks),"positive_control_count":len(controls),"positive_control_pass_count":sum(x["secure_contract_passed"] for x in controls),"tests":rows}
    payload["suite_digest"]=r.digest([(x["test_id"],x["actual"],x["message"],x["secure_contract_passed"]) for x in rows])
    Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:payload[k] for k in ("attack_count","secure_attack_count","escape_count","positive_control_count","positive_control_pass_count","suite_digest")},ensure_ascii=False))
    return 0 if payload["escape_count"]==0 and payload["positive_control_pass_count"]==payload["positive_control_count"] else 1


if __name__=="__main__": raise SystemExit(main())
