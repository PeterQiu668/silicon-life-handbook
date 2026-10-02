#!/usr/bin/env python3
"""Replay the v2.3 independent 25 attacks and v2.4 effect/readback neighbors."""
from __future__ import annotations
import copy, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load():
    spec=importlib.util.spec_from_file_location("c19v24",HERE/"run-security-harness.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def main():
    r=load(); raw=json.loads((HERE/"synthetic-security-input.yaml").read_text()); raw_auth=json.loads((HERE/"frozen-security-authority.yaml").read_text()); auth=r.validate_authority_bundle(copy.deepcopy(raw_auth)); src=r.validate_source(copy.deepcopy(raw),auth); rows=[]
    def add(i,f,a,reasons,required=None,expected="FAIL"):
        ok=(a=="PASS") if expected=="PASS" else (a in {"FAIL","SCHEMA_REJECT"} and (required is None or required in reasons)); rows.append({"attack_id":i,"family":f,"expected":expected,"actual":a,"required_reason":required or "ANY_HARD_REJECTION","matched":ok,"reasons":sorted(set(reasons))})
    def state(i,f,mut,sid="S01",required=None,authmut=None,expected="FAIL"):
        sc=copy.deepcopy(next(x for x in src["scenarios"] if x["id"]==sid)); aa=copy.deepcopy(auth); mut(sc["state"]); authmut and authmut(aa)
        try: r.validate_state(sc["state"],i); a,h,v,_=r.evaluate(sc,src,aa); reasons=h+v
        except Exception as e: a,reasons="SCHEMA_REJECT",[str(e)]
        add(i,f,a,reasons,required,expected)
    def source(i,f,mut):
        x=copy.deepcopy(raw); mut(x)
        try: y=r.validate_source(x,auth); z=r.build_result(y,auth); q=next(t for t in z["trials"] if t["scenario_id"]=="S01"); a,reasons=q["decision"],q["reasons"]
        except Exception as e: a,reasons="SCHEMA_REJECT",[str(e)]
        add(i,f,a,reasons)
    def root(i,f,mut):
        a=copy.deepcopy(raw_auth); mut(a); a["root_digest"]=r.digest({k:v for k,v in a.items() if k!="root_digest"})
        try:r.validate_authority_bundle(a); x,reasons="PASS",[]
        except Exception as e:x,reasons="SCHEMA_REJECT",[str(e)]
        add(i,f,x,reasons)

    root("principal-alias-root-resealed","v23-root",lambda a:a["registries"]["principals"].update({"alias":copy.deepcopy(a["registries"]["principals"]["principal-agent-a"])}))
    root("session-revoked-root-resealed","v23-root",lambda a:a["registries"]["sessions"]["session-a"].update(status="REVOKED",revoked_at="2026-09-30T11:00:00Z"))
    root("test-definition-revoked-root-resealed","v23-root",lambda a:a["registries"]["test_definitions"]["S01"].update(status="REVOKED"))
    root("test-evidence-content-resealed","v23-root",lambda a:a["registries"]["test_evidence"]["test-evidence-s01"].update(content_digest=r.digest("bad")))
    root("audit-anchor-self-signed-root-resealed","v23-root",lambda a:a["registries"]["audit_anchors"]["audit-C19-v2.4"].update(final_digest=r.digest("bad")))
    state("principal-zero-width-alias","v23-identity",lambda s:s["identity"].update(principal="principal-agent-a\u200b"))
    state("service-name-whitespace-alias","v23-identity",lambda s:s["identity"].update(service="gateway-test "))
    state("observed-session-revoked","v23-session",lambda s:s["tenant_session"].update(status="REVOKED",revoked_at="2026-09-30T11:00:00Z"))
    state("observed-session-self-extended","v23-session",lambda s:s["tenant_session"].update(expires_at="2027-10-01T00:00:00Z"))
    source("evaluation-before-session-authority-window","v23-session",lambda s:s.update(evaluation_time="2026-09-29T23:59:59Z"))
    state("approval-id-alias","v23-authority",lambda s:s["approval"].update(approval_id="approval-1-alias"))
    state("grant-id-alias","v23-authority",lambda s:s["grant"].update(grant_id="grant-1-alias"))
    source("test-ref-alias","v23-test",lambda s:s["scenarios"][0].update(test_ref="S01-alias"))
    source("task-trial-alias","v23-test",lambda s:s["scenarios"][0].update(task_id="task-alias",trial_id="trial-alias"))
    def relabel(s): s["scenarios"][0].update(layer="holdout"); s["declared_layers"].update(training=3,holdout=16)
    source("scenario-layer-relabel-with-counts","v23-test",relabel)
    source("scenario-self-claims-red-team","v23-test",lambda s:s["scenarios"][0].update(security_red_team=True))
    source("scenario-self-claims-shadow","v23-test",lambda s:s["scenarios"][0].update(synthetic_shadow=True))
    state("none-effect-claims-external","v23-effect",lambda s:s["effects"][0].update(external_side_effect=True))
    state("executed-effect-declared-external","v23-effect",lambda s:s["effects"][0].update(external_side_effect=True),sid="S16",required="EXTERNAL_EFFECT_CONTRACT_VIOLATION")
    state("receipt-target-substitution","v23-receipt",lambda s:(s["receipts"][0].update(target="different"),s["receipts"][0].update(digest=r.digest({k:v for k,v in s["receipts"][0].items() if k!="digest"}))),sid="S16",required="EFFECT_RECEIPT_OBJECT_BINDING_INVALID")
    state("receipt-executor-alias","v23-receipt",lambda s:(s["receipts"][0].update(executor="alias"),s["receipts"][0].update(digest=r.digest({k:v for k,v in s["receipts"][0].items() if k!="digest"}))),sid="S16",required="EFFECT_RECEIPT_OBJECT_BINDING_INVALID")
    state("readback-before-execution","v23-readback",lambda s:None,sid="S16",required="EFFECT_READBACK_TIME_INVALID",authmut=lambda a:(a["registries"]["readbacks"]["readback-incident"].update(observed_at="2026-09-30T11:00:00Z"),a["registries"]["readbacks"]["readback-incident"].update(record_digest=r.digest({k:v for k,v in a["registries"]["readbacks"]["readback-incident"].items() if k!="record_digest"}))))
    def preauth(s):
        s["effects"][0]["executed_at"]="2026-09-29T23:00:00Z"; s["receipts"][0].update(executed_at="2026-09-29T23:00:00Z",issued_at="2026-09-29T23:00:01Z"); s["receipts"][0]["digest"]=r.digest({k:v for k,v in s["receipts"][0].items() if k!="digest"})
    state("effect-executes-before-all-authority-windows","v23-escape-closure",preauth,sid="S16",required="EFFECT_EXECUTION_OUTSIDE_AUTHORITY_WINDOW")
    state("readback-after-evaluation","v23-escape-closure",lambda s:None,sid="S16",required="EFFECT_READBACK_TIME_INVALID",authmut=lambda a:(a["registries"]["readbacks"]["readback-incident"].update(observed_at="2026-10-02T00:00:00Z"),a["registries"]["readbacks"]["readback-incident"].update(record_digest=r.digest({k:v for k,v in a["registries"]["readbacks"]["readback-incident"].items() if k!="record_digest"}))))
    state("audit-local-chain-self-resealed","v23-audit",lambda s:s["audit"]["events"][-1]["payload"].update(outcome="FAILED"))

    state("terminal-effect-pass-control","v24-positive",lambda s:None,sid="S23",expected="PASS")
    state("authorization-snapshot-substitution","v24-snapshot",lambda s:s["effects"][0].update(authorization_snapshot_digest=r.digest("wrong")),sid="S23",required="EFFECT_AUTHORIZATION_SNAPSHOT_INVALID")
    state("receipt-snapshot-substitution","v24-snapshot",lambda s:(s["receipts"][0].update(authorization_snapshot_digest=r.digest("wrong")),s["receipts"][0].update(digest=r.digest({k:v for k,v in s["receipts"][0].items() if k!="digest"}))),sid="S23",required="EFFECT_RECEIPT_OBJECT_BINDING_INVALID")
    state("receipt-issued-before-execution","v24-time",lambda s:(s["receipts"][0].update(issued_at="2026-09-30T11:00:00Z"),s["receipts"][0].update(digest=r.digest({k:v for k,v in s["receipts"][0].items() if k!="digest"}))),sid="S23",required="EFFECT_READBACK_TIME_INVALID")
    state("credential-revoked-before-effect","v24-time",lambda s:s["credential"].update(revoked_at="2026-09-30T11:00:00Z"),sid="S23",required="EFFECT_EXECUTION_OUTSIDE_AUTHORITY_WINDOW")
    state("grant-issued-after-effect","v24-time",lambda s:s["grant"].update(issued_at="2026-09-30T12:00:00Z"),sid="S23",required="EFFECT_EXECUTION_OUTSIDE_AUTHORITY_WINDOW")
    state("session-not-before-after-effect","v24-time",lambda s:s["tenant_session"].update(not_before="2026-09-30T12:00:00Z"),sid="S23",required="EFFECT_EXECUTION_OUTSIDE_AUTHORITY_WINDOW")
    state("readback-observer-equals-executor","v24-readback",lambda s:None,sid="S23",required="EFFECT_READBACK_AUTHORITY_INVALID",authmut=lambda a:(a["registries"]["readbacks"]["readback-pass"].update(observer="principal-agent-a",authority_ref="principal-agent-a"),a["registries"]["readbacks"]["readback-pass"].update(record_digest=r.digest({k:v for k,v in a["registries"]["readbacks"]["readback-pass"].items() if k!="record_digest"}))))
    state("audit-effect-digest-substitution","v24-audit",lambda s:s["audit"]["events"][-1]["payload"].update(effect_digest=r.digest("wrong")),sid="S23",required="TERMINAL_EFFECT_NOT_IN_AUDIT")

    historical=rows[:25]; output={"schema_version":"c19.security.effect-time-readback.v2.4","attack_count":len(rows),"matched_count":sum(x["matched"] for x in rows),"escape_count":sum(not x["matched"] for x in rows),"historical_v2_3_attack_count":25,"historical_v2_3_matched_count":sum(x["matched"] for x in historical),"suite_digest":r.digest(rows),"attacks":rows}; (HERE/"v2.4-effect-time-readback-regression-results.yaml").write_text(json.dumps(output,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); print(json.dumps({k:output[k] for k in ("attack_count","matched_count","escape_count","historical_v2_3_matched_count","suite_digest")},ensure_ascii=False)); raise SystemExit(1 if output["escape_count"] else 0)
if __name__=="__main__": main()
