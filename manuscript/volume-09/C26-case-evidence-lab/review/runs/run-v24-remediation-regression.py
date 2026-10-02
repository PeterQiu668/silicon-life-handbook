#!/usr/bin/env python3
"""C23 v2.4 seven-control remediation regression plus a legal repin PASS."""
import argparse, copy, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
r=load(HERE/"run-case-harness.py","c23runner")
attacks=load(HERE.parent/"v2.3-independent-negative-tests.py","c23_v23_attacks")

def reseal(x): x["record_digest"]=r.digest({k:v for k,v in x.items() if k!="record_digest"})
def repin(doc,root):
    root["registries"]=copy.deepcopy(doc["registries"]); root["suite_manifest"]=r.suite_manifest(doc["suite"],doc["scenarios"]); root["root_digest"]=r.digest(r.root_payload(root)); r.PINNED_AUTHORITY_ROOT_DIGEST=root["root_digest"]
def scenario(doc): return next(x for x in doc["scenarios"] if x["scenario_id"]=="S01")
def record(doc,registry,key,value): return next(x for x in doc["registries"][registry] if x[key]==value)
def run_semantic(base,root,mutate,expected):
    doc=copy.deepcopy(base); authority=copy.deepcopy(root); old=r.PINNED_AUTHORITY_ROOT_DIGEST
    try:
        mutate(doc); repin(doc,authority); result=r.evaluate(doc,authority); actual=next(x["derived"]["verdict"] for x in result["trials"] if x["scenario_id"]=="S01"); message=""
    except Exception as exc: actual="REJECT"; message=str(exc)
    finally: r.PINNED_AUTHORITY_ROOT_DIGEST=old
    return actual,actual in expected,message
def run_output(base_result,root,mutate):
    result=copy.deepcopy(base_result); mutate(result)
    try: r.verify_result(result,root); return "ACCEPTED",False,""
    except Exception as exc: return "REJECT",True,str(exc)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--authority-root",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    base=json.loads(Path(a.input).read_text()); root=json.loads(Path(a.authority_root).read_text()); baseline=r.evaluate(copy.deepcopy(base),copy.deepcopy(root))
    semantic=[
      ("V01_EXACT_D21_PROJECTION",attacks.mutate_orphan_failed_d21,{"FAIL","REJECT"}),
      ("V02_ACTIVE_COAUTHOR_BREAKS_INDEPENDENCE",attacks.mutate_reviewer_also_case_author,{"FAIL","REJECT"}),
      ("V03_ASSIGNMENT_AFTER_PUBLICATION",attacks.mutate_assignment_starts_after_publication,{"FAIL","REJECT"}),
      ("V04_TRIAL_AFTER_EVALUATION",lambda d:attacks.mutate_trial_time(d,r,"2026-09-30T12:01:00Z"),{"FAIL","REVIEW_REQUIRED","REJECT"}),
      ("V05_TRIAL_BEFORE_AUTHORIZATION",lambda d:attacks.mutate_trial_time(d,r,"2026-08-31T23:59:59Z"),{"FAIL","REVIEW_REQUIRED","REJECT"}),
      ("V06_REVIEW_PUBLICATION_PRECEDE_EVIDENCE",attacks.mutate_publication_precedes_trials,{"FAIL","REVIEW_REQUIRED","REJECT"}),
      ("V07_PASS_POINTS_TO_FAILURE",attacks.mutate_pass_trial_points_to_failure,{"FAIL","REJECT"}),
      ("V08_SHARED_FAILURE_LOG",attacks.mutate_two_failures_share_one_log,{"FAIL","REJECT"}),
      ("V09_UNLINKED_FAILURE_LOG",attacks.mutate_unlinked_failure_log,{"FAIL","REJECT"}),
      ("V10_EFFECT_KIND_DERIVES_EXTERNAL",attacks.mutate_external_write_hidden_by_false_flag,{"FAIL","REJECT"}),
      ("V11_D21_CONTENT_CONTRADICTION",attacks.mutate_d21_content_contradiction,{"FAIL","REVIEW_REQUIRED","REJECT"}),
      ("V12_AUTHORITY_ADAPTER_MATRIX",lambda d:attacks.set_adapter(d,r,attacks.adapter("STATE_CARRIER","NON_CRITICAL","AUTHORITY","REVIEW_REQUIRED")),{"FAIL","REJECT"}),
      ("V13_SECURITY_ADAPTER_MATRIX",lambda d:attacks.set_adapter(d,r,attacks.adapter("TOOL_SCHEMA","NON_CRITICAL","SECURITY_BOUNDARY","ACCEPTED")),{"FAIL","REJECT"}),
      ("V14_D21_ADAPTER_MATRIX",lambda d:attacks.set_adapter(d,r,attacks.adapter("MESSAGE_SEMANTICS","NON_CRITICAL","D21_TERMINAL","ACCEPTED")),{"FAIL","REJECT"}),
    ]
    rows=[]
    for test_id,mutate,expected in semantic:
        actual,passed,message=run_semantic(base,root,mutate,expected); rows.append({"test_id":test_id,"layer":"semantic","actual":actual,"secure_expected_outcomes":sorted(expected),"passed":passed,"message":message})
    output_attacks=[
      ("V15_RESULT_IDENTITY",lambda x:x["trials"][0].update(scenario_id="SCENARIO.OTHER",case_record_id="CASE.RECORD.OTHER",task_id="TASK.OTHER",run_id="RUN.OTHER",evidence_id="EVIDENCE.OTHER")),
      ("V16_RESULT_DISTRIBUTION",lambda x:x.__setitem__("distribution",{"PASS":32})),
      ("V17_RESULT_TRIAL_COUNT",lambda x:x.__setitem__("trial_count",1)),
      ("V18_RESULT_REAL_COUNT",lambda x:x.__setitem__("accepted_real_claim_count",1)),
      ("V19_RESULT_EFFECT_COUNT",lambda x:x.__setitem__("external_effect_count",1)),
      ("V20_RESULT_UNKNOWN_FIELD",lambda x:x.__setitem__("oracle_hint","PASS")),
      ("V21_RESULT_REASON_TAMPER",lambda x:x["trials"][0]["derived"]["reasons"].append("FORGED")),
      ("V22_RESULT_IDENTITY_REHASH",lambda x:(x["trials"][0].__setitem__("scenario_id","SCENARIO.OTHER"),x.__setitem__("decision_digest",r.digest({k:v for k,v in x.items() if k!="decision_digest"})))),
    ]
    for test_id,mutate in output_attacks:
        actual,passed,message=run_output(baseline,root,mutate); rows.append({"test_id":test_id,"layer":"result_envelope","actual":actual,"secure_expected_outcomes":["REJECT"],"passed":passed,"message":message})
    # A semantically legal, newly pinned evidence timestamp remains admissible.
    def legal_repin(doc):
        trial=record(doc,"trial_registry","trial_record_id","TRIAL.RECORD.S01.01"); trial["recorded_at"]="2026-09-30T11:51:30Z"; reseal(trial)
    actual,passed,message=run_semantic(base,root,legal_repin,{"PASS"}); rows.append({"test_id":"V23_LEGAL_REPIN_PASS","layer":"non_total_rejection","actual":actual,"secure_expected_outcomes":["PASS"],"passed":passed,"message":message})
    out={"schema_version":"c23.v2.4.remediation-regression.v1","baseline_distribution":baseline["distribution"],"baseline_decision_digest":baseline["decision_digest"],"test_count":len(rows),"passed_count":sum(x["passed"] for x in rows),"failed_count":sum(not x["passed"] for x in rows),"all_passed":all(x["passed"] for x in rows),"tests":rows}
    out["suite_digest"]=r.digest([(x["test_id"],x["actual"],x["message"]) for x in rows]); Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ("test_count","passed_count","failed_count","suite_digest")},ensure_ascii=False)); return 0 if out["all_passed"] else 1

if __name__=="__main__": raise SystemExit(main())
