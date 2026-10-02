#!/usr/bin/env python3
"""C23 v2.6 author regression for authority, causality and evidence scope."""
from pathlib import Path
import argparse, copy, importlib.util, json


def load(path):
    spec=importlib.util.spec_from_file_location("c23_v26_runner",path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True); p.add_argument("--authority-root",required=True)
    p.add_argument("--runner",required=True); p.add_argument("--output",required=True)
    a=p.parse_args(); r=load(Path(a.runner))
    base=r.strict_json_loads(Path(a.input).read_text()); authority=r.strict_json_loads(Path(a.authority_root).read_text())
    baseline=r.evaluate(copy.deepcopy(base),copy.deepcopy(authority))

    def seal(x): x["record_digest"]=r.digest({k:v for k,v in x.items() if k!="record_digest"})
    def rec(doc,registry,key,value): return next(x for x in doc["registries"][registry] if x[key]==value)
    def scenario(doc,sid="S01"): return next(x for x in doc["scenarios"] if x["scenario_id"]==sid)
    def repin(doc,root):
        root["registries"]=copy.deepcopy(doc["registries"]); root["suite_manifest"]=r.suite_manifest(doc["suite"],doc["scenarios"])
        root["root_digest"]=r.digest(r.root_payload(root)); r.PINNED_AUTHORITY_ROOT_DIGEST=root["root_digest"]
    contract_keys=("case_record_id","case_version","task_id","run_id","side","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","task_digest","input_digest","risk","permissions_digest","data_digest","eval_digest","model_usd","tool_usd","compute_usd","human_minutes","human_usd","elapsed_seconds","total_usd")
    def reseal_budget(doc,budget_id):
        b=rec(doc,"budget_registry","budget_id",budget_id); b["contract_digest"]=r.digest({k:b[k] for k in contract_keys}); seal(b); return b
    def sync_migration_budget(doc):
        m=rec(doc,"migration_registry","migration_id","MIGRATION.S01")
        for side,bid in (("baseline_contract","BUDGET.BASELINE.S01"),("candidate_contract","BUDGET.CANDIDATE.S01")):
            b=rec(doc,"budget_registry","budget_id",bid); m[side]["budget_contract_digest"]=b["contract_digest"]
        seal(m)
    def change_budget_pair(doc,spec_field,digest_field,value):
        for bid in ("BUDGET.BASELINE.S01","BUDGET.CANDIDATE.S01"):
            b=rec(doc,"budget_registry","budget_id",bid); b[spec_field]=copy.deepcopy(value); b[digest_field]=r.digest(value); reseal_budget(doc,bid)
        m=rec(doc,"migration_registry","migration_id","MIGRATION.S01")
        for side in ("baseline_contract","candidate_contract"): m[side][digest_field]=r.digest(value)
        sync_migration_budget(doc)

    def late_failure_log(doc,when):
        x=rec(doc,"artifact_registry","artifact_id","ARTIFACT.FAILURE.S01"); x["recorded_at"]=when; seal(x)
    def twin_task(doc): change_budget_pair(doc,"task_spec","task_digest",{"task":"TASK.FORGED.BOTH"})
    def twin_input(doc): change_budget_pair(doc,"input_spec","input_digest",{"input":"FORGED.BOTH"})
    def twin_permissions(doc): change_budget_pair(doc,"permissions","permissions_digest",["READ.SYNTHETIC","WRITE.PRODUCTION"])
    def twin_data(doc): change_budget_pair(doc,"data_spec","data_digest",{"dataset":"PRODUCTION_CUSTOMER","case":"S01","rights":"CLAIMED","environment":"PRODUCTION"})
    def twin_grader(doc): change_budget_pair(doc,"eval_spec","eval_digest",{"grader_principal_id":"PRINCIPAL.AUTHOR.S01","rubric":"AUTHOR-SELF"})
    def swap_budget_pair(doc):
        a,b=scenario(doc,"S01"),scenario(doc,"S17")
        for key in ("baseline_budget_ref","candidate_budget_ref"): a["raw_state"][key],b["raw_state"][key]=b["raw_state"][key],a["raw_state"][key]
        ma=rec(doc,"migration_registry","migration_id","MIGRATION.S01"); mb=rec(doc,"migration_registry","migration_id","MIGRATION.S17")
        for side in ("baseline_contract","candidate_contract"): ma[side],mb[side]=copy.deepcopy(mb[side]),copy.deepcopy(ma[side])
        seal(ma); seal(mb)
    def reconstruct_empty(doc):
        i=rec(doc,"case_identity_registry","identity_id","IDENTITY.S01"); s=rec(doc,"source_registry","source_id","SOURCE.S01")
        i["case_type"]="RECONSTRUCTED"; s["origin"]="RECONSTRUCTION"; seal(i); seal(s)
    def reconstruct_mismatch(doc):
        i=rec(doc,"case_identity_registry","identity_id","IDENTITY.S01"); s=rec(doc,"source_registry","source_id","SOURCE.S01")
        i.update(case_type="RECONSTRUCTED",missing_elements=["ORIGINAL.INPUT"],inference_list=["INFERRED.TIMELINE"])
        s.update(origin="RECONSTRUCTION",missing_elements=["ORIGINAL.INPUT"],inference_list=["DIFFERENT.INFERENCE"]); seal(i); seal(s)
    def cross_ref(doc,key,other): scenario(doc)["raw_state"][key]=scenario(doc,other)["raw_state"][key]
    def budget_scope(doc,field,value):
        for bid in ("BUDGET.BASELINE.S01","BUDGET.CANDIDATE.S01"):
            b=rec(doc,"budget_registry","budget_id",bid); b[field]=value; reseal_budget(doc,bid)
        m=rec(doc,"migration_registry","migration_id","MIGRATION.S01")
        for side in ("baseline_contract","candidate_contract"): m[side][field]=value
        sync_migration_budget(doc)
    def swap_sides(doc):
        bb=rec(doc,"budget_registry","budget_id","BUDGET.BASELINE.S01"); cb=rec(doc,"budget_registry","budget_id","BUDGET.CANDIDATE.S01")
        bb["side"],cb["side"]=cb["side"],bb["side"]; reseal_budget(doc,bb["budget_id"]); reseal_budget(doc,cb["budget_id"]); sync_migration_budget(doc)
    def stale_contract_digest(doc):
        b=rec(doc,"budget_registry","budget_id","BUDGET.BASELINE.S01"); b["model_usd"]+=1; seal(b)
    def stale_migration_digest(doc):
        m=rec(doc,"migration_registry","migration_id","MIGRATION.S01"); m["baseline_contract"]["budget_contract_digest"]="0"*64; seal(m)
    def repin_permission_production(doc):
        p=rec(doc,"permission_authority_registry","permission_authority_id","AUTHORITY.PERMISSION.S01"); perms=["READ.SYNTHETIC","WRITE.PRODUCTION"]
        p["allowed_permissions"]=perms; p["permissions_digest"]=r.digest(perms); seal(p); twin_permissions(doc)
    def repin_dataset_production(doc):
        d=rec(doc,"dataset_authority_registry","dataset_authority_id","AUTHORITY.DATASET.S01"); spec={"dataset":"PRODUCTION_CUSTOMER","case":"S01","rights":"CLAIMED","environment":"PRODUCTION"}
        d["data_spec"]=spec; d["data_digest"]=r.digest(spec); d["rights_status"]="PASS"; seal(d); twin_data(doc)
    def repin_self_grader(doc):
        g=rec(doc,"grader_authority_registry","grader_authority_id","AUTHORITY.GRADER.S01"); spec={"grader_principal_id":"PRINCIPAL.AUTHOR.S01","rubric":"AUTHOR-SELF"}
        g["grader_principal_id"]="PRINCIPAL.AUTHOR.S01"; g["eval_spec"]=spec; g["eval_digest"]=r.digest(spec); seal(g); twin_grader(doc)
    def legal_task(doc):
        spec={"task":"TASK.S01","variant":"LEGAL.CLARIFICATION"}; d=r.digest(spec)
        t=rec(doc,"task_authority_registry","task_authority_id","AUTHORITY.TASK.S01"); t["task_spec"]=spec; t["task_digest"]=d; seal(t); change_budget_pair(doc,"task_spec","task_digest",spec)
    def legal_input(doc):
        spec={"input":"S01","locale":"ZH-CN"}; d=r.digest(spec)
        x=rec(doc,"input_authority_registry","input_authority_id","AUTHORITY.INPUT.S01"); x["input_spec"]=spec; x["input_digest"]=d; seal(x); change_budget_pair(doc,"input_spec","input_digest",spec)

    attacks=[
      ("V26-01_FAILURE_LOG_AFTER_D21",lambda d:late_failure_log(d,"2026-09-30T11:57:00Z")),
      ("V26-02_FAILURE_LOG_AFTER_REVIEW",lambda d:late_failure_log(d,"2026-09-30T11:58:30Z")),
      ("V26-03_FAILURE_LOG_AFTER_PUBLICATION",lambda d:late_failure_log(d,"2026-09-30T11:59:30Z")),
      ("V26-04_TWIN_FORGED_TASK",twin_task),("V26-05_TWIN_FORGED_INPUT",twin_input),
      ("V26-06_TWIN_PERMISSION_EXPANSION",twin_permissions),("V26-07_TWIN_PRODUCTION_DATA",twin_data),
      ("V26-08_TWIN_AUTHOR_SELF_GRADER",twin_grader),("V26-09_CROSS_SCENARIO_BUDGET_PAIR",swap_budget_pair),
      ("V26-10_RECONSTRUCTED_EMPTY_LIMITATIONS",reconstruct_empty),("V26-11_RECONSTRUCTED_SOURCE_MISMATCH",reconstruct_mismatch),
      ("V26-12_CROSS_TASK_AUTHORITY_REF",lambda d:cross_ref(d,"task_authority_ref","S17")),
      ("V26-13_CROSS_INPUT_AUTHORITY_REF",lambda d:cross_ref(d,"input_authority_ref","S17")),
      ("V26-14_CROSS_PERMISSION_AUTHORITY_REF",lambda d:cross_ref(d,"permission_authority_ref","S17")),
      ("V26-15_CROSS_DATASET_AUTHORITY_REF",lambda d:cross_ref(d,"dataset_authority_ref","S17")),
      ("V26-16_CROSS_GRADER_AUTHORITY_REF",lambda d:cross_ref(d,"grader_authority_ref","S17")),
      ("V26-17_BUDGET_RUN_REBIND",lambda d:budget_scope(d,"run_id","RUN.FORGED.S01")),
      ("V26-18_BUDGET_CASE_REBIND",lambda d:budget_scope(d,"case_record_id","CASE.RECORD.S17")),
      ("V26-19_BUDGET_SIDE_SWAP",swap_sides),("V26-20_STALE_BUDGET_CONTRACT_DIGEST",stale_contract_digest),
      ("V26-21_STALE_MIGRATION_BUDGET_DIGEST",stale_migration_digest),
      ("V26-22_REPIN_PRODUCTION_PERMISSION",repin_permission_production),
      ("V26-23_REPIN_PRODUCTION_DATASET",repin_dataset_production),
      ("V26-24_REPIN_AUTHOR_SELF_GRADER",repin_self_grader),
    ]
    rows=[]; old_pin=r.PINNED_AUTHORITY_ROOT_DIGEST
    for tid,mut in attacks:
        doc=copy.deepcopy(base); root=copy.deepcopy(authority); actual="ERROR"; message=""; reasons=[]
        try:
            mut(doc); repin(doc,root); result=r.evaluate(doc,root); target=next(x for x in result["trials"] if x["scenario_id"]=="S01")
            actual=target["derived"]["verdict"]; reasons=target["derived"]["reasons"]
        except Exception as exc: actual="REJECT"; message=str(exc)
        finally: r.PINNED_AUTHORITY_ROOT_DIGEST=old_pin
        rows.append({"test_id":tid,"actual":actual,"reasons":reasons,"secure_expected_outcomes":["FAIL","REJECT"],"secure_contract_passed":actual in {"FAIL","REJECT"},"message":message})
    controls=[]
    for tid,mut in (("V26-C01_LEGAL_TASK_REPIN",legal_task),("V26-C02_LEGAL_INPUT_REPIN",legal_input)):
        doc=copy.deepcopy(base); root=copy.deepcopy(authority); actual="ERROR"; message=""; reasons=[]
        try:
            mut(doc); repin(doc,root); result=r.evaluate(doc,root); target=next(x for x in result["trials"] if x["scenario_id"]=="S01")
            actual=target["derived"]["verdict"]; reasons=target["derived"]["reasons"]
        except Exception as exc: actual="REJECT"; message=str(exc)
        finally: r.PINNED_AUTHORITY_ROOT_DIGEST=old_pin
        controls.append({"test_id":tid,"actual":actual,"reasons":reasons,"secure_expected_outcomes":["PASS"],"secure_contract_passed":actual=="PASS","message":message})
    payload={"schema_version":"c23.v2.6.author-remediation-regression.v1","baseline_distribution":baseline["distribution"],"baseline_decision_digest":baseline["decision_digest"],"attack_count":len(rows),"secure_attack_count":sum(x["secure_contract_passed"] for x in rows),"escape_count":sum(not x["secure_contract_passed"] for x in rows),"positive_control_count":len(controls),"positive_control_pass_count":sum(x["secure_contract_passed"] for x in controls),"tests":rows+controls}
    payload["suite_digest"]=r.digest([(x["test_id"],x["actual"],x["reasons"],x["message"],x["secure_contract_passed"]) for x in payload["tests"]])
    Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:payload[k] for k in ("attack_count","secure_attack_count","escape_count","positive_control_count","positive_control_pass_count","suite_digest")},ensure_ascii=False))
    return 0 if payload["escape_count"]==0 and payload["positive_control_pass_count"]==len(controls) else 1


if __name__=="__main__": raise SystemExit(main())
