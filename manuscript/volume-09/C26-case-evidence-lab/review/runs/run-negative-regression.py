#!/usr/bin/env python3
"""Author negative mutations against the C23 v2.3 frozen-root contract."""
import argparse, copy, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("c23runner",HERE/"run-case-harness.py")
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def reseal(rec): rec["record_digest"]=r.digest({k:v for k,v in rec.items() if k!="record_digest"})
def rec(doc,name,i=0): return doc["registries"][name][i]
def s(doc,i=0): return doc["scenarios"][i]
def setv(path,value):
    def mutate(doc):
        cur=doc
        for key in path[:-1]: cur=cur[key]
        cur[path[-1]]=value
    return mutate
def record_change(reg,key,value,i=0,after=None):
    def mutate(doc):
        x=rec(doc,reg,i); x[key]=value
        if after: after(x)
        reseal(x)
    return mutate
def release_change(key,value):
    def mutate(doc):
        x=rec(doc,"release_registry"); x[key]=value; x["release_digest"]=r.digest({"platform":x["platform"],"version":x["version"],"commit":x["commit"]}); reseal(x)
    return mutate
def raw_change(key,value):
    return lambda doc: s(doc)["raw_state"].__setitem__(key,value)
def migration_contract(side,key,value):
    def mutate(doc):
        x=rec(doc,"migration_registry"); x[side][key]=value; reseal(x)
    return mutate
def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--authority-root",required=True); p.add_argument("--output",required=True); a=p.parse_args(); base=json.loads(Path(a.input).read_text()); authority_root=json.loads(Path(a.authority_root).read_text())
    author=s(base)["raw_state"]["author_principal_id"]
    def dup(field): return lambda d: d["scenarios"][1].__setitem__(field,d["scenarios"][0][field])
    def add_unknown_root(d): d["oracle_hint"]="PASS"
    def add_unknown_raw(d): s(d)["raw_state"]["mutation"]="dummy"
    def duplicate_scenario(d): d["scenarios"].append(copy.deepcopy(d["scenarios"][0]))
    def real_manifest(d): d["registries"]["real_case_manifest"].append({"verified":True})
    def private_content_tamper(d):
        x=rec(d,"source_registry"); x["private_content"]={"tampered":True}; reseal(x)
    def artifact_payload_tamper(d):
        x=rec(d,"artifact_registry"); x["payload"]={"tampered":True}; reseal(x)
    def env_manifest_tamper(d):
        x=rec(d,"environment_registry"); x["manifest"]={"tampered":True}; reseal(x)
    def mapping_tamper(d):
        x=rec(d,"redaction_registry"); x["mapping"]={"dummy":True}; reseal(x)
    def reviewer_alias(d):
        x=rec(d,"reviewer_registry"); x["aliases"].append(author); reseal(x)
    def pub_wrong_redaction(d):
        x=rec(d,"publication_registry"); x["redaction_id"]=d["scenarios"][1]["raw_state"]["redaction_ref"]; reseal(x)
    def pub_wrong_digest(d):
        x=rec(d,"publication_registry"); x["public_content_digest"]=r.digest({"wrong":True}); reseal(x)
    def artifact_wrong(key,value):
        def mutate(d): x=rec(d,"artifact_registry"); x[key]=value; reseal(x)
        return mutate
    def d21_change(key,value):
        def mutate(d): x=rec(d,"d21_registry"); x[key]=value; reseal(x)
        return mutate
    def migration_change(key,value):
        def mutate(d): x=rec(d,"migration_registry"); x[key]=value; reseal(x)
        return mutate
    def external_effect(d):
        x=rec(d,"effect_registry"); x.update(effect_kind="EXTERNAL_WRITE",external=True); reseal(x)
    def hard_unknown(d):
        raw_change("holdout_accessed",True)(d); d21_change("delivery","UNKNOWN")(d)
    def bad_release_duplicate(d):
        x=copy.deepcopy(rec(d,"release_registry")); d["registries"]["release_registry"].append(x)
    def budget_total(d):
        x=rec(d,"budget_registry",1); x["total_usd"]=999; reseal(x)
    def fake_input_digest(d):
        x=rec(d,"budget_registry",1); x["input_spec"]={"forged":"input"}; reseal(x)
    def self_authorize(d):
        principal=s(d)["raw_state"]["author_principal_id"]
        for reg,key in (("case_identity_registry","authority_principal_id"),("authorization_registry","principal_id"),("source_registry","authority_principal_id"),("redaction_registry","authorized_by_principal_id")):
            x=rec(d,reg); x[key]=principal; reseal(x)
    def coherent_wrong_mapping(d):
        x=rec(d,"redaction_registry"); x["mapping"]={"private":H,"public":H}; x["mapping_digest"]=r.digest(x["mapping"]); reseal(x)
    def coherent_wrong_public_artifact(d):
        x=rec(d,"artifact_registry"); x["payload"]={"different":"public"}; x["content_digest"]=r.digest(x["payload"]); reseal(x)
    def revoked_budgets(d):
        for i in (0,1):
            x=rec(d,"budget_registry",i); x["status"]="REVOKED"; reseal(x)
    def reviewer_role_removed(d):
        x=rec(d,"reviewer_registry"); x["roles"]=["ROLE.CASE.AUTHOR"]; reseal(x)
    def receipt_readback_mismatch(d):
        x=rec(d,"effect_registry"); x["readback"]={**x["readback"],"status":"APPLIED"}; x["readback_digest"]=r.digest(x["readback"]); reseal(x)
    def adapter_difference(d):
        x=rec(d,"migration_registry"); x["adapter_differences"]=["NATIVE.STATE.CARRIER.DIFFERS"]; reseal(x)
    def revoke_effect(d):
        x=rec(d,"effect_registry"); x["status"]="REVOKED"; reseal(x)
    def future_publication(d):
        x=rec(d,"publication_registry"); x["released_at"]="2026-09-30T12:01:00Z"; reseal(x)
    def unauthorized_internal(d):
        x=rec(d,"effect_registry"); x["authorized"]=False
        for name in ("receipt","readback"):
            x[name]["authorized"]=False; x[name+"_digest"]=r.digest(x[name])
        reseal(x)
    H=r.digest({"different":True})
    tests=[
      ("N01_UNKNOWN_ROOT","REJECT",add_unknown_root),("N02_WRONG_SCHEMA","REJECT",setv(["schema_version"],"c23.case.input.v1")),
      ("N03_WRONG_ENV_BOOL","REJECT",setv(["environment","offline"],1)),("N04_BAD_TIMESTAMP","REJECT",setv(["suite","evaluation_time"],"not-time")),
      ("N05_UNKNOWN_RAW_FIELD","REJECT",add_unknown_raw),("N06_RAW_WRONG_TYPE","REJECT",raw_change("trial_count","3")),
      ("N07_DUP_SCENARIO","REJECT",duplicate_scenario),("N08_DUP_CASE","REJECT",dup("case_record_id")),("N09_DUP_TASK","REJECT",dup("task_id")),
      ("N10_DUP_TRIAL","REJECT",dup("trial_id")),("N11_DUP_RUN","REJECT",dup("run_id")),("N12_DUP_EVIDENCE","REJECT",dup("evidence_id")),
      ("N13_VERIFIED_REAL","REJECT",record_change("case_identity_registry","case_type","VERIFIED-REAL")),
      ("N14_ANON_REAL","REJECT",record_change("case_identity_registry","case_type","ANONYMIZED-REAL")),("N15_REAL_MANIFEST","REJECT",real_manifest),
      ("N16_FLOATING_RELEASE","FAIL",release_change("version","latest")),("N17_WRONG_RELEASE_COMMIT","FAIL",release_change("commit","0"*40)),
      ("N18_ILLEGAL_RISK","REJECT",record_change("budget_registry","risk","R9",1)),("N19_NEGATIVE_BUDGET","REJECT",record_change("budget_registry","model_usd",-1,1)),
      ("N20_NONFINITE_BUDGET","REJECT",record_change("budget_registry","model_usd",float("nan"),1)),("N21_TOTAL_MISMATCH","FAIL",budget_total),
      ("N22_SOURCE_SAME_DIGEST_WRONG_CONTENT","REJECT",private_content_tamper),("N23_ARTIFACT_SAME_DIGEST_WRONG_CONTENT","REJECT",artifact_payload_tamper),
      ("N24_ENV_SAME_DIGEST_WRONG_CONTENT","REJECT",env_manifest_tamper),("N25_REDACTION_DUMMY_MAPPING","REJECT",mapping_tamper),
      ("N26_COPYRIGHT_FAIL","FAIL",record_change("source_registry","copyright_status","FAIL")),("N27_SOURCE_UNAUTHORIZED","FAIL",record_change("source_registry","authorization_status","FAIL")),
      ("N28_AUTH_EXPIRED","FAIL",record_change("authorization_registry","valid_until","2026-09-29T00:00:00Z")),
      ("N29_AUTH_REVOKED","FAIL",record_change("authorization_registry","status","REVOKED",after=lambda x:x.update(revoked_at="2026-09-29T00:00:00Z"))),
      ("N30_WRONG_SUBJECT_BINDING","FAIL",record_change("case_identity_registry","subject_id","SUBJECT.WRONG")),
      ("N31_WRONG_VERSION_BINDING","FAIL",record_change("case_identity_registry","case_version",2)),("N32_AUTHOR_ALIAS_REVIEWER","FAIL",reviewer_alias),
      ("N33_REVIEWER_REVOKED","FAIL",record_change("reviewer_registry","status","REVOKED")),("N34_PUBLIC_MAPPING_REF_WRONG","FAIL",pub_wrong_redaction),
      ("N35_PUBLIC_PRIVATE_DIGEST_WRONG","FAIL",pub_wrong_digest),("N36_ARTIFACT_CASE_WRONG","FAIL",artifact_wrong("case_record_id","CASE.RECORD.WRONG")),
      ("N37_ARTIFACT_RUN_WRONG","FAIL",artifact_wrong("run_id","RUN.WRONG")),("N38_D21_TECH_FAIL","FAIL",d21_change("technical","FAIL")),
      ("N39_D21_DELIVERY_FAIL","FAIL",d21_change("delivery","FAIL")),("N40_D21_BUSINESS_FAIL","FAIL",d21_change("business_environment","FAIL")),
      ("N41_D21_UNKNOWN_WITH_FROZEN_ROOT_TAMPER","FAIL",d21_change("delivery","UNKNOWN")),("N42_MIGRATION_TASK_UNFAIR","FAIL",migration_contract("candidate_contract","task_digest",H)),
      ("N43_MIGRATION_INPUT_UNFAIR","FAIL",migration_contract("candidate_contract","input_digest",H)),("N44_MIGRATION_RISK_UNFAIR","FAIL",migration_contract("candidate_contract","risk","R3")),
      ("N45_MIGRATION_PERMISSION_UNFAIR","FAIL",migration_contract("candidate_contract","permissions_digest",H)),("N46_MIGRATION_DATA_UNFAIR","FAIL",migration_contract("candidate_contract","data_digest",H)),
      ("N47_MIGRATION_EVAL_UNFAIR","FAIL",migration_contract("candidate_contract","eval_digest",H)),("N48_MIGRATION_BUDGET_REF_WRONG","FAIL",migration_contract("candidate_contract","budget_id",s(base,1)["raw_state"]["candidate_budget_ref"])),
      ("N49_UNSUPPORTED_CAPABILITY_ROOT_TAMPER","FAIL",migration_change("unsupported_capabilities",["STATE.ADAPTER.UNAVAILABLE"])),
      ("N50_FAILURE_DELETED","FAIL",raw_change("failures_preserved",False)),("N51_HOLDOUT_LEAK","FAIL",raw_change("holdout_accessed",True)),
      ("N52_GRADER_LEAK","FAIL",raw_change("grader_private_access",True)),("N53_HARD_PLUS_UNKNOWN","FAIL",hard_unknown),
      ("N54_EXTERNAL_EFFECT","FAIL",external_effect),("N55_BAD_D21_ENUM","REJECT",d21_change("technical","ERROR")),
      ("N56_DUP_ARTIFACT_REF","REJECT",raw_change("artifact_refs",s(base)["raw_state"]["artifact_refs"]+[s(base)["raw_state"]["artifact_refs"][0]])),
      ("N57_UNKNOWN_REGISTRY_FIELD","REJECT",lambda d:rec(d,"authorization_registry").__setitem__("self_attested",True)),
      ("N58_DUP_GLOBAL_REGISTRY_ID","REJECT",bad_release_duplicate),("N59_ENV_PRODUCTION_WRITE","FAIL",record_change("environment_registry","production_write",True)),
      ("N60_AUTH_SCOPE_MISSING","FAIL",record_change("authorization_registry","scopes",["RUN_SYNTHETIC"])),
      ("N61_UNVERSIONED_ENVIRONMENT","REJECT",record_change("environment_registry","version","")),
      ("N62_FAKE_INPUT_DIGEST","REJECT",fake_input_digest),
      ("N63_AUTHORITY_PRINCIPAL_MISMATCH","FAIL",record_change("authorization_registry","principal_id","PRINCIPAL.WRONG.AUTHORITY")),
      ("N64_SELF_AUTHORIZATION","FAIL",self_authorize),
      ("N65_CROSS_TYPE_GLOBAL_ID_COLLISION","REJECT",lambda d:s(d).__setitem__("task_id",s(d)["evidence_id"])),
      ("N66_COHERENT_BUT_WRONG_REDACTION_MAPPING","REJECT",coherent_wrong_mapping),
      ("N67_PUBLIC_ARTIFACT_CONTENT_MISMATCH","FAIL",coherent_wrong_public_artifact),
      ("N68_REVOKED_BASELINE_RELEASE","FAIL",record_change("release_registry","status","REVOKED",0)),
      ("N69_REVOKED_CANDIDATE_RELEASE","FAIL",record_change("release_registry","status","REVOKED",1)),
      ("N70_REVIEWER_ROLE_REMOVED","FAIL",reviewer_role_removed),
      ("N71_EFFECT_REVOKED","FAIL",revoke_effect),
      ("N72_INTERNAL_RECEIPT_READBACK_MISMATCH","FAIL",receipt_readback_mismatch),
      ("N73_REVOKED_BUDGETS","FAIL",revoked_budgets),
      ("N74_ADAPTER_DIFFERENCE_TAMPER","FAIL",adapter_difference),
      ("N75_SCENARIO_TASK_UNBOUND","FAIL",lambda d:s(d).__setitem__("task_id","TASK.UNBOUND.N75")),
      ("N76_FAKE_TRIAL_DISTRIBUTION","FAIL",lambda d:(raw_change("trial_count",99)(d),raw_change("failure_count",0)(d),raw_change("failures_preserved",False)(d))),
      ("N77_PUBLICATION_AFTER_EVALUATION","FAIL",future_publication),
      ("N78_FAILURE_REFERENCE_REMOVED","FAIL",raw_change("failure_refs",[])),
      ("N79_INTERNAL_EFFECT_UNAUTHORIZED","FAIL",unauthorized_internal),
    ]
    details=[]
    for tid,expected,mutate in tests:
        doc=copy.deepcopy(base); actual="ERROR"; message=""
        try:
            mutate(doc); out=r.evaluate(doc,authority_root); actual=next(x["derived"]["verdict"] for x in out["trials"] if x["scenario_id"]=="S01")
        except Exception as e: actual="REJECT"; message=str(e)
        allowed={expected}|({"REJECT"} if expected=="FAIL" else set())
        passed=actual in allowed
        details.append({"test_id":tid,"secure_expected_outcomes":sorted(allowed),"actual":actual,"passed":passed,"message":message})
    summary={"schema_version":"c23.negative-regression.v2.3","test_count":len(details),"passed_count":sum(x["passed"] for x in details),"failed_count":sum(not x["passed"] for x in details),"all_passed":all(x["passed"] for x in details),"tests":details}
    summary["suite_digest"]=r.digest([(x["test_id"],x["actual"],x["message"]) for x in details])
    Path(a.output).write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    if not summary["all_passed"]:
        for x in details:
            if not x["passed"]: print(x)
        raise SystemExit(1)
    print(f"{summary['passed_count']}/{summary['test_count']}")
if __name__=="__main__": main()
