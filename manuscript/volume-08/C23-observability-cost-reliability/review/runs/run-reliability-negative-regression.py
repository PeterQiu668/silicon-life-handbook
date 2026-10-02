#!/usr/bin/env python3
"""Independent negative controls for the C20 v2.1 closed-world evaluator."""
from __future__ import annotations
import argparse, copy, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("c20_runner",HERE/"run-reliability-harness.py")
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)

def reseal(record):
    record.pop("digest",None);record["digest"]=runner.sha(record)
def s01(d):return d["scenarios"][0]
def ref(sc,key):return sc["state"][key]
def registry_record(d,name,reference):return d["authorities"][name][reference]

def schema_case(name,base,mutate):
    d=copy.deepcopy(base);mutate(d)
    try:runner.validate(d);actual="NOT_REJECTED";ok=False
    except runner.ValidationError as e:actual=f"REJECTED:{e}";ok=True
    return {"control_id":name,"mode":"schema_rejection","passed":ok,"actual":actual}
def decision_case(name,base,mutate,decision,reason=None):
    d=copy.deepcopy(base);mutate(d);runner.validate(d);sc=s01(d)
    actual=runner.evaluate(sc,d["authorities"],runner.time(d["suite"]["evaluation_time"],"evaluation_time"))
    reasons=actual["hard_failures"]+actual["review_items"]
    ok=actual["decision"]==decision and (reason is None or reason in reasons)
    return {"control_id":name,"mode":"state_derived_decision","passed":ok,"expected_decision":decision,"expected_reason":reason,"actual_decision":actual["decision"],"actual_reasons":reasons}

def main():
    p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--output",required=True);z=p.parse_args()
    base=json.loads(Path(z.input).read_text());runner.validate(base);cases=[]
    cases += [
      schema_case("N01_wrong_root_version",base,lambda d:d.__setitem__("schema_version","c20.reliability.input.v999")),
      schema_case("N02_unknown_root_field",base,lambda d:d.__setitem__("dummy",True)),
      schema_case("N03_unknown_scenario_field",base,lambda d:s01(d).__setitem__("dummy",True)),
      schema_case("N04_unknown_state_field",base,lambda d:s01(d)["state"].__setitem__("dummy",True)),
      schema_case("N05_unknown_nested_field",base,lambda d:s01(d)["state"]["task"].__setitem__("dummy",True)),
      schema_case("N06_wrong_nested_type",base,lambda d:s01(d)["state"]["retry"].__setitem__("attempts","2")),
      schema_case("N07_illegal_fifth_layer",base,lambda d:s01(d).__setitem__("dataset_layer","security")),
      schema_case("N08_synthetic_claims_real_layer",base,lambda d:s01(d).__setitem__("dataset_layer","representative_real_world")),
      schema_case("N09_self_filled_real_manifest",base,lambda d:d["authorities"]["real_world_evidence_manifest"].__setitem__("fake",{"verified":True})),
      schema_case("N10_duplicate_scenario_id",base,lambda d:d["scenarios"][1].__setitem__("scenario_id",s01(d)["scenario_id"])),
      schema_case("N11_duplicate_task_id",base,lambda d:d["scenarios"][1].__setitem__("task_id",s01(d)["task_id"])),
      schema_case("N12_duplicate_trial_id",base,lambda d:d["scenarios"][1].__setitem__("trial_id",s01(d)["trial_id"])),
      schema_case("N13_duplicate_run_id",base,lambda d:d["scenarios"][1].__setitem__("run_id",s01(d)["run_id"])),
      schema_case("N14_cross_run_identity",base,lambda d:s01(d)["state"]["task"].__setitem__("run_id","other-run")),
      schema_case("N15_registry_digest_tamper",base,lambda d:registry_record(d,"authority_registry",ref(s01(d),"authority_ref")).__setitem__("actor_id","attacker")),
      schema_case("N16_unknown_registry_field",base,lambda d:registry_record(d,"policy_registry",ref(s01(d),"policy_ref")).__setitem__("dummy",True)),
    ]
    def tech_missing(d):s01(d)["state"]["technical"]["terminal_ref"]="terminal://missing"
    def delivery_contradiction(d):
        r=registry_record(d,"delivery_registry",s01(d)["state"]["delivery"]["delivery_ref"]);r["target_visible"]=False;reseal(r)
    def acceptance_contradiction(d):
        r=registry_record(d,"acceptance_registry",s01(d)["state"]["acceptance"]["acceptance_ref"]);r["artifact_valid"]=False;reseal(r)
    def event_digest(d):s01(d)["state"]["event_chain"][0]["payload"]={"tampered":True}
    def evidence_missing(d):s01(d)["state"]["evidence_refs"].append("evidence://missing")
    def fake_authority(d):
        r=registry_record(d,"authority_registry",ref(s01(d),"authority_ref"));r["actor_id"]="attacker";reseal(r)
    def fake_policy(d):
        r=registry_record(d,"policy_registry",ref(s01(d),"policy_ref"));r["object_ref"]="production://other";reseal(r)
    def bad_receipt(d):
        r=registry_record(d,"effect_registry",s01(d)["state"]["effect"]["effect_ref"]);r.update({"state":"ACKNOWLEDGED","receipt_ref":"receipt://fake","receipt_valid":False,"readback_state":"UNKNOWN"});reseal(r)
    def recovery_unanchored(d):s01(d)["state"]["recovery"]["recovery_ref"]="recovery://missing"
    def external_effect(d):
        r=registry_record(d,"effect_registry",s01(d)["state"]["effect"]["effect_ref"]);r.update({"state":"COMMITTED","is_external":True,"observed_count":1,"readback_state":"CHANGED"});reseal(r)
    def hard_unknown(d):
        r=registry_record(d,"technical_terminal_registry",s01(d)["state"]["technical"]["terminal_ref"]);r["status"]="UNKNOWN";reseal(r);s01(d)["state"]["telemetry"]["canary_in_export"]=True
    def technical_unknown(d):
        r=registry_record(d,"technical_terminal_registry",s01(d)["state"]["technical"]["terminal_ref"]);r["status"]="UNKNOWN";reseal(r)
    def invalid_terminal_enum(d):
        r=registry_record(d,"technical_terminal_registry",s01(d)["state"]["technical"]["terminal_ref"]);r["status"]="MAYBE";reseal(r)
    def stale_authority(d):
        r=registry_record(d,"authority_registry",ref(s01(d),"authority_ref"));r["valid_until"]="2026-09-30T11:00:00Z";reseal(r)
    def wrong_chain_anchor(d):
        r=next(iter(d["authorities"]["event_chain_registry"].values()));r["head_digest"]="sha256:"+"0"*64;reseal(r)
    def wrong_evidence_binding(d):
        e=s01(d)["state"]["event_chain"][0];r=d["authorities"]["evidence_registry"][e["event_id"]];r["run_id"]="other-run";reseal(r)
    def recovery_conflict(d):
        r=registry_record(d,"recovery_registry",s01(d)["state"]["recovery"]["recovery_ref"]);r["checkpoint_valid"]=False;reseal(r)
    def invalid_effect_enum(d):
        r=registry_record(d,"effect_registry",s01(d)["state"]["effect"]["effect_ref"]);r["state"]="MAGIC";reseal(r)
    cases += [
      decision_case("N17_missing_technical_terminal",base,tech_missing,"FAIL","TECHNICAL_TERMINAL_UNRESOLVED"),
      decision_case("N18_delivery_visibility_contradiction",base,delivery_contradiction,"FAIL","DELIVERY_RECEIPT_VISIBILITY_CONTRADICTION"),
      decision_case("N19_acceptance_contradiction",base,acceptance_contradiction,"FAIL","ACCEPTANCE_CONTRADICTION"),
      decision_case("N20_wrong_event_digest",base,event_digest,"FAIL","EVENT_CANONICAL_DIGEST_MISMATCH"),
      decision_case("N21_unresolved_evidence",base,evidence_missing,"FAIL","EVIDENCE_REF_UNRESOLVED"),
      decision_case("N22_fake_authority",base,fake_authority,"FAIL","AUTHORITY_ACTOR_MISMATCH"),
      decision_case("N23_fake_policy",base,fake_policy,"FAIL","REQUEST_OUTSIDE_POLICY"),
      decision_case("N24_fake_receipt_readback",base,bad_receipt,"FAIL","TOOL_SUCCESS_ENVIRONMENT_DIVERGED"),
      decision_case("N25_unanchored_recovery",base,recovery_unanchored,"FAIL","RECOVERY_REF_UNRESOLVED"),
      decision_case("N26_external_effect",base,external_effect,"FAIL","OFFLINE_EXTERNAL_EFFECT_DETECTED"),
      decision_case("N27_hard_plus_unknown_noncompensatory",base,hard_unknown,"FAIL","OBSERVABILITY_CANARY_LEAK"),
      decision_case("N28_unknown_maps_review",base,technical_unknown,"REVIEW_REQUIRED","TECHNICAL_TERMINAL_UNKNOWN"),
      schema_case("N29_invalid_terminal_enum",base,invalid_terminal_enum),
      decision_case("N30_expired_authority",base,stale_authority,"FAIL","AUTHORITY_INACTIVE_OR_EXPIRED"),
      decision_case("N31_wrong_chain_anchor",base,wrong_chain_anchor,"FAIL","EVENT_CHAIN_ANCHOR_MISMATCH"),
      decision_case("N32_wrong_evidence_binding",base,wrong_evidence_binding,"FAIL","EVENT_EVIDENCE_UNRESOLVED_OR_MISMATCHED"),
      decision_case("N33_recovery_registry_conflict",base,recovery_conflict,"FAIL","RECOVERY_READBACK_CONTRADICTION"),
      schema_case("N34_invalid_effect_enum",base,invalid_effect_enum),
    ]
    def claim_unknown(d):s01(d)["state"]["claim"]["completion"]="unknown"
    def explicit_technical_failure(d):
        claim_unknown(d);r=registry_record(d,"technical_terminal_registry",s01(d)["state"]["technical"]["terminal_ref"]);r["status"]="ERROR";reseal(r)
    def explicit_delivery_failure(d):
        claim_unknown(d);r=registry_record(d,"delivery_registry",s01(d)["state"]["delivery"]["delivery_ref"]);r.update({"state":"NOT_DELIVERED","target_visible":False});reseal(r)
    def explicit_acceptance_failure(d):
        claim_unknown(d);r=registry_record(d,"acceptance_registry",s01(d)["state"]["acceptance"]["acceptance_ref"]);r.update({"artifact_valid":False,"business_status":"FAIL","environment_status":"DIVERGED"});reseal(r)
    def explicit_recovery_failure(d):
        claim_unknown(d);r=registry_record(d,"recovery_registry",s01(d)["state"]["recovery"]["recovery_ref"]);r.update({"status":"FAILED","probe_status":"FAIL"});reseal(r)
    def negative_observed_count(d):
        r=registry_record(d,"effect_registry",s01(d)["state"]["effect"]["effect_ref"]);r.update({"observed_count":-1,"is_external":True});reseal(r)
    def negative_attempts(d):s01(d)["state"]["retry"]["attempts"]=-1
    def sampling_out_of_range(d):s01(d)["state"]["telemetry"]["sampling_rate"]=2
    def invalid_event_time(d):s01(d)["state"]["event_chain"][0]["occurred_at"]="not-a-time"
    def duplicate_seq(d):s01(d)["state"]["event_chain"][1]["seq"]=1
    def duplicate_evidence_ref(d):s01(d)["state"]["evidence_refs"].append(s01(d)["state"]["evidence_refs"][0])
    def nonfinite_cost(d):s01(d)["state"]["cost"]["model_usd"]=float("nan")
    cases += [
      decision_case("N36_explicit_technical_failure_without_completion_claim",base,explicit_technical_failure,"FAIL","TECHNICAL_TERMINAL_FAILED"),
      decision_case("N37_explicit_delivery_failure_without_completion_claim",base,explicit_delivery_failure,"FAIL","DELIVERY_FAILED"),
      decision_case("N38_explicit_acceptance_failure_without_completion_claim",base,explicit_acceptance_failure,"FAIL","ACCEPTANCE_FAILED"),
      decision_case("N39_explicit_recovery_failure_without_recovery_claim",base,explicit_recovery_failure,"FAIL","RECOVERY_FAILED"),
      schema_case("N40_negative_external_observed_count",base,negative_observed_count),
      schema_case("N41_negative_retry_attempts",base,negative_attempts),
      schema_case("N42_sampling_rate_out_of_range",base,sampling_out_of_range),
      schema_case("N43_invalid_event_occurred_at",base,invalid_event_time),
      schema_case("N44_duplicate_event_seq",base,duplicate_seq),
      schema_case("N45_duplicate_evidence_refs",base,duplicate_evidence_ref),
      schema_case("N46_nonfinite_cost",base,nonfinite_cost),
    ]
    # Case name and expected oracle are report metadata, never decision inputs.
    inert=copy.deepcopy(base);s01(inert)["scenario_id"]="FAIL-NAME-MUST-NOT-CONTROL";s01(inert)["expected_decision"]="FAIL";runner.validate(inert)
    actual=runner.evaluate(s01(inert),inert["authorities"],runner.time(inert["suite"]["evaluation_time"],"evaluation_time"))
    cases.append({"control_id":"N35_case_name_and_expected_inert","mode":"decision_invariance","passed":actual["decision"]=="PASS","actual_decision":actual["decision"]})
    output={"schema_version":"c20.reliability.negative-regression.v2.1","control_count":len(cases),"passed_count":sum(x["passed"] for x in cases),"failed_count":sum(not x["passed"] for x in cases),"all_passed":all(x["passed"] for x in cases),"controls":cases}
    Path(z.output).write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n")
    if not output["all_passed"]:raise SystemExit(1)
if __name__=="__main__":main()
