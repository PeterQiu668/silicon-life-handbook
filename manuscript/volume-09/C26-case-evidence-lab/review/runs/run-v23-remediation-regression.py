#!/usr/bin/env python3
"""C23 v2.3 remediation and adjacent negative regression.

Input-only attacks exercise the frozen suite/projection contract.  Authorized
repin cases rebuild the complete manifest/root and then exercise semantic
assignment, alias, adapter, D21/failure/effect controls.
"""
import argparse, copy, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("c23runner",HERE/"run-case-harness.py")
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def reseal(record):
    record["record_digest"]=r.digest({k:v for k,v in record.items() if k!="record_digest"})

def scenario(doc,sid="S01"):
    return next(x for x in doc["scenarios"] if x["scenario_id"]==sid)

def record(doc,name,key,value):
    return next(x for x in doc["registries"][name] if x[key]==value)

def repin(doc,root):
    root["registries"]=copy.deepcopy(doc["registries"])
    root["suite_manifest"]=r.suite_manifest(doc["suite"],doc["scenarios"])
    root["root_digest"]=r.digest(r.root_payload(root))
    r.PINNED_AUTHORITY_ROOT_DIGEST=root["root_digest"]

def run(base,authority,mutate,repinned=False,target="S01"):
    doc=copy.deepcopy(base); root=copy.deepcopy(authority); old=r.PINNED_AUTHORITY_ROOT_DIGEST
    try:
        mutate(doc,root)
        if repinned: repin(doc,root)
        out=r.evaluate(doc,root)
        row=next((x for x in out["trials"] if x["scenario_id"]==target),None)
        return row["derived"]["verdict"] if row else "MISSING_TARGET", ""
    except Exception as exc:
        return "REJECT",str(exc)
    finally:
        r.PINNED_AUTHORITY_ROOT_DIGEST=old

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--authority-root",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    base=json.loads(Path(a.input).read_text()); authority=json.loads(Path(a.authority_root).read_text())
    tests=[]
    def add(test_id,expected,mutate,repinned=False,target="S01"): tests.append((test_id,set(expected),mutate,repinned,target))

    # Suite/inventory/provenance controls.
    add("R01_DELETE_SCENARIO",{"REJECT"},lambda d,z:d["scenarios"].pop())
    add("R02_REORDER_SCENARIOS",{"REJECT"},lambda d,z:d["scenarios"].reverse())
    add("R03_RENAME_SCENARIO",{"REJECT"},lambda d,z:scenario(d).__setitem__("scenario_id","SCENARIO.RENAMED"),target="SCENARIO.RENAMED")
    add("R04_RENAME_BUILD",{"REJECT"},lambda d,z:d["suite"].__setitem__("build_id","BUILD.C23.TAMPERED"))
    add("R05_SHIFT_EVALUATION_TIME",{"REJECT"},lambda d,z:d["suite"].__setitem__("evaluation_time","2026-09-30T11:59:30Z"))
    add("R06_DUPLICATE_SCENARIO",{"REJECT"},lambda d,z:d["scenarios"].append(copy.deepcopy(d["scenarios"][0])))

    # Exact scenario projection and bidirectional failure/effect/D21 controls.
    add("R07_DELETE_FAIL_TRIAL",{"REJECT"},lambda d,z:scenario(d)["raw_state"]["trial_refs"].pop(1))
    add("R08_DELETE_FAILURE_REF",{"REJECT"},lambda d,z:scenario(d)["raw_state"].__setitem__("failure_refs",[]))
    add("R09_DELETE_EFFECT_REF",{"REJECT"},lambda d,z:scenario(d)["raw_state"].__setitem__("effect_refs",[]))
    kinds=["PUBLIC","TECHNICAL","DELIVERY","ACCEPTANCE","FAILURE"]
    for offset,kind in enumerate(kinds,10):
        add(f"R{offset:02d}_DELETE_{kind}_ARTIFACT",{"REJECT"},lambda d,z,k=kind:scenario(d)["raw_state"].__setitem__("artifact_refs",[x for x in scenario(d)["raw_state"]["artifact_refs"] if f"ARTIFACT.{k}." not in x]))
    add("R15_CROSS_CASE_EFFECT",{"REJECT"},lambda d,z:scenario(d)["raw_state"].__setitem__("effect_refs",scenario(d,"S02")["raw_state"]["effect_refs"]))
    add("R16_CROSS_CASE_TRIAL",{"REJECT"},lambda d,z:scenario(d)["raw_state"].__setitem__("trial_refs",scenario(d,"S02")["raw_state"]["trial_refs"]))
    add("R17_CROSS_CASE_FAILURE",{"REJECT"},lambda d,z:scenario(d)["raw_state"].__setitem__("failure_refs",scenario(d,"S02")["raw_state"]["failure_refs"]))

    # Assignment and alias normalization.
    add("R18_CROSS_CASE_AUTHOR_INPUT",{"REJECT"},lambda d,z:scenario(d)["raw_state"].__setitem__("author_principal_id","PRINCIPAL.AUTHOR.S17"))
    def revoke_assignment(d,z):
        x=record(d,"author_assignment_registry","assignment_id","ASSIGNMENT.AUTHOR.S01"); x["status"]="REVOKED"; reseal(x)
    add("R19_REVOKED_AUTHOR_ASSIGNMENT",{"FAIL"},revoke_assignment,True)
    def wrong_assignment_subject(d,z):
        x=record(d,"author_assignment_registry","assignment_id","ASSIGNMENT.AUTHOR.S01"); x["subject_id"]="SUBJECT.S17"; reseal(x)
    add("R20_AUTHOR_ASSIGNMENT_WRONG_SUBJECT",{"FAIL"},wrong_assignment_subject,True)
    def wrong_assignment_version(d,z):
        x=record(d,"author_assignment_registry","assignment_id","ASSIGNMENT.AUTHOR.S01"); x["case_version"]=2; reseal(x)
    add("R21_AUTHOR_ASSIGNMENT_WRONG_VERSION",{"FAIL"},wrong_assignment_version,True)
    def author_alias_to_reviewer(d,z):
        x=record(d,"alias_registry","alias_record_id","ALIAS.RECORD.AUTHOR.S01"); x["canonical_principal_id"]="PRINCIPAL.REVIEWER.S01"; reseal(x)
        scenario(d)["raw_state"]["author_principal_id"]="PRINCIPAL.AUTHOR.ALIAS.S01"
    add("R22_AUTHOR_ALIAS_TO_REVIEWER",{"FAIL"},author_alias_to_reviewer,True)

    # Structured adapter object: valid repins exercise semantics, not substrings.
    def set_adapter(d,obj):
        x=record(d,"migration_registry","migration_id","MIGRATION.S01"); x["adapter_differences"]=[obj]; reseal(x)
    def adapter(category,criticality,contract,disposition,owner="PRINCIPAL.AUTHORITY.S01",evidence="ARTIFACT.TECHNICAL.S01"):
        return {"category":category,"criticality":criticality,"affected_contract":contract,"evidence_ref":evidence,"owner":owner,"disposition":disposition}
    add("R23_CRITICAL_AUTHORIZATION_ENUM",{"FAIL"},lambda d,z:set_adapter(d,adapter("AUTHORIZATION","CRITICAL","AUTHORITY","FAIL")),True)
    add("R24_CRITICAL_TERMINAL_ENUM",{"FAIL"},lambda d,z:set_adapter(d,adapter("TERMINAL_STATE","CRITICAL","D21_TERMINAL","FAIL")),True)
    add("R25_CRITICAL_CATEGORY_DOWNPLAYED",{"FAIL"},lambda d,z:set_adapter(d,adapter("SECURITY","NON_CRITICAL","SECURITY_BOUNDARY","REVIEW_REQUIRED")),True)
    add("R26_NONCRITICAL_REVIEW",{"REVIEW_REQUIRED"},lambda d,z:set_adapter(d,adapter("STATE_CARRIER","NON_CRITICAL","STATE_TRANSPORT","REVIEW_REQUIRED")),True)
    add("R27_ADAPTER_WRONG_OWNER",{"FAIL"},lambda d,z:set_adapter(d,adapter("STATE_CARRIER","NON_CRITICAL","STATE_TRANSPORT","REVIEW_REQUIRED",owner="PRINCIPAL.AUTHORITY.S17")),True)
    add("R28_ADAPTER_CROSS_CASE_EVIDENCE",{"FAIL"},lambda d,z:set_adapter(d,adapter("STATE_CARRIER","NON_CRITICAL","STATE_TRANSPORT","REVIEW_REQUIRED",evidence="ARTIFACT.TECHNICAL.S17")),True)
    add("R29_FREE_TEXT_ADAPTER_REJECTED",{"REJECT"},lambda d,z:set_adapter(d,"PRIVILEGE.BOUNDARY.DIFFERS"),True)
    add("R30_UNKNOWN_ADAPTER_CATEGORY",{"REJECT"},lambda d,z:set_adapter(d,adapter("PRIVILEGE","CRITICAL","AUTHORITY","FAIL")),True)

    rows=[]
    for test_id,expected,mutate,repinned,target in tests:
        actual,message=run(base,authority,mutate,repinned,target)
        rows.append({"test_id":test_id,"secure_expected_outcomes":sorted(expected),"actual":actual,"passed":actual in expected,"message":message})
    payload={"schema_version":"c23.v2.3.remediation-regression.v1","test_count":len(rows),"passed_count":sum(x["passed"] for x in rows),"failed_count":sum(not x["passed"] for x in rows),"all_passed":all(x["passed"] for x in rows),"tests":rows}
    payload["suite_digest"]=r.digest([(x["test_id"],x["actual"],x["message"]) for x in rows])
    Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:payload[k] for k in ("test_count","passed_count","failed_count","suite_digest")},ensure_ascii=False))
    return 0 if payload["all_passed"] else 1

if __name__=="__main__": raise SystemExit(main())
