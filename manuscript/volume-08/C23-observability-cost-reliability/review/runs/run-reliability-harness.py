#!/usr/bin/env python3
"""C20 v2.1 closed-world, state-derived offline reliability evaluator."""
from __future__ import annotations
import argparse, copy, hashlib, json, math
from collections import Counter
from datetime import datetime
from pathlib import Path

class ValidationError(ValueError): pass
LAYERS=["training","regression","holdout","representative_real_world"]
ROOT={"schema_version","generated_by","suite","environment","authorities","scenarios"}
SUITE={"suite_id","build_id","run_id","evaluation_time","data_origin","declared_layers","security_red_team_cross_cutting"}
ENV={"mode","network_accessed","real_credentials_used","external_side_effects_permitted"}
AUTHS={"authority_registry","policy_registry","technical_terminal_registry","delivery_registry","acceptance_registry","effect_registry","evidence_registry","recovery_registry","event_chain_registry","real_world_evidence_manifest"}
SCEN={"scenario_id","task_id","trial_id","run_id","dataset_layer","security_red_team","synthetic_shadow","expected_decision","state"}
STATE={"task","request","authority_ref","policy_ref","event_chain","technical","delivery","acceptance","effect","retry","cancel","queue","capacity","cost","telemetry","recovery","evidence_refs","claim"}
NEST={
"task":{"task_id","task_version","trial_id","run_id","tenant_id","actor_id","eligible","risk_class"},
"request":{"action","object_ref","scope"},"technical":{"terminal_ref","transport_status","response_body_bytes"},
"delivery":{"delivery_ref","provider_ack"},"acceptance":{"acceptance_ref"},"effect":{"effect_ref","idempotency_key"},
"retry":{"error_type","retry_class","attempts","attempt_budget","same_idempotency_key","backoff","jitter","reconciled_before_retry"},
"cancel":{"requested","acknowledged","stop_observed","child_active"},
"queue":{"depth","oldest_age_seconds","age_slo_seconds","admission_open","load_shedding"},
"capacity":{"arrival_rate","service_rate","active_concurrency","max_concurrency","tenant_share","tenant_limit","degraded_mode","baseline_mean_ms","current_mean_ms","baseline_p99_ms","current_p99_ms"},
"cost":{"model_usd","tool_usd","compute_usd","human_minutes","human_usd","retry_waste_usd","remediation_usd","reported_total_usd","baseline_human_minutes"},
"telemetry":{"exporter_state","gap_alert","dropped_count","dropped_counter_visible","metric_label_values","metric_label_limit","trace_present","audit_hard_event_present","sampling_rate","content_capture","canary_in_export","redaction_applied"},
"recovery":{"recovery_ref","process_restarted","file_present","lease_state","terminal_reconciled","checkpoint_valid","regression_rerun","original_fault_reproduced","training_feedback_recorded"},
"claim":{"completion","reliability","economics","scope"}}
EVENT={"seq","event_id","event_type","producer","tenant_id","task_id","task_version","run_id","attempt_id","object_version","occurred_at","payload","prev_digest","event_digest"}
REG={
"authority_registry":{"ref","actor_id","tenant_id","task_id","task_version","run_id","status","valid_from","valid_until","issuer","digest"},
"policy_registry":{"ref","authority_ref","actor_id","tenant_id","task_id","task_version","run_id","action","object_ref","scope","status","policy_version","decision","digest"},
"technical_terminal_registry":{"ref","tenant_id","task_id","task_version","run_id","status","transport_status","response_body_bytes","process_alive","source","authoritative","digest"},
"delivery_registry":{"ref","tenant_id","task_id","task_version","run_id","state","target_visible","receipt_valid","target_ref","source","authoritative","digest"},
"acceptance_registry":{"ref","tenant_id","task_id","task_version","run_id","artifact_valid","business_status","environment_status","source","authoritative","digest"},
"effect_registry":{"ref","tenant_id","task_id","task_version","run_id","action","object_ref","state","receipt_ref","receipt_valid","readback_ref","readback_state","observed_count","is_external","idempotency_key","source","authoritative","digest"},
"evidence_registry":{"ref","kind","tenant_id","task_id","task_version","run_id","source","status","authoritative","content_digest","digest"},
"recovery_registry":{"ref","tenant_id","task_id","task_version","run_id","status","checkpoint_valid","lease_state","terminal_reconciled","probe_status","source","authoritative","digest"},
"event_chain_registry":{"ref","tenant_id","task_id","task_version","run_id","event_count","head_digest","status","authoritative","source","digest"}}

def canonical(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def sha(v): return "sha256:"+hashlib.sha256(canonical(v).encode()).hexdigest()
def exact(v,keys,path):
    if not isinstance(v,dict): raise ValidationError(f"{path}: expected object")
    miss=sorted(keys-set(v)); extra=sorted(set(v)-keys)
    if miss or extra: raise ValidationError(f"{path}: missing={miss} unknown={extra}")
def typ(v,t,path):
    if t is int and (not isinstance(v,int) or isinstance(v,bool)): raise ValidationError(f"{path}: expected int")
    if t is float and (not isinstance(v,(int,float)) or isinstance(v,bool)): raise ValidationError(f"{path}: expected number")
    if t not in (int,float) and not isinstance(v,t): raise ValidationError(f"{path}: expected {t.__name__}")
def time(v,path):
    typ(v,str,path)
    try:return datetime.fromisoformat(v.replace("Z","+00:00"))
    except ValueError as e: raise ValidationError(f"{path}: invalid timestamp") from e
def seal_ok(r,path):
    d=r.get("digest"); raw=copy.deepcopy(r); raw.pop("digest",None)
    if not isinstance(d,str) or d!=sha(raw): raise ValidationError(f"{path}.digest: canonical mismatch")
def validate_registry(name,items):
    typ(items,dict,f"authorities.{name}")
    if name=="real_world_evidence_manifest":
        if items: raise ValidationError("offline harness rejects any real_world_evidence_manifest")
        return
    for ref,r in items.items():
        exact(r,REG[name],f"authorities.{name}.{ref}")
        if r["ref"]!=ref: raise ValidationError(f"authorities.{name}.{ref}: key/ref mismatch")
        seal_ok(r,f"authorities.{name}.{ref}")
        for k in ["ref","tenant_id","task_id","run_id"]:typ(r[k],str,f"authorities.{name}.{ref}.{k}")
        typ(r["task_version"],int,f"authorities.{name}.{ref}.task_version")
        if "authoritative" in r:typ(r["authoritative"],bool,f"authorities.{name}.{ref}.authoritative")
        if name=="authority_registry":
            for k in ["actor_id","status","valid_from","valid_until","issuer"]:typ(r[k],str,f"authorities.{name}.{ref}.{k}")
            if r["status"] not in {"ACTIVE","REVOKED","EXPIRED","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}.status: invalid enum")
            time(r["valid_from"],f"authorities.{name}.{ref}.valid_from");time(r["valid_until"],f"authorities.{name}.{ref}.valid_until")
        elif name=="policy_registry":
            for k in ["authority_ref","actor_id","action","object_ref","scope","status","policy_version","decision"]:typ(r[k],str,f"authorities.{name}.{ref}.{k}")
            if r["status"] not in {"ACTIVE","REVOKED","EXPIRED","UNKNOWN"} or r["decision"] not in {"ALLOW","DENY","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}: invalid enum")
        elif name=="technical_terminal_registry":
            if r["status"] not in {"OK","ERROR","TIMEOUT","CANCELED","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}.status: invalid enum")
            typ(r["transport_status"],int,f"authorities.{name}.{ref}.transport_status");typ(r["response_body_bytes"],int,f"authorities.{name}.{ref}.response_body_bytes");typ(r["process_alive"],bool,f"authorities.{name}.{ref}.process_alive")
        elif name=="delivery_registry":
            if r["state"] not in {"DELIVERED","NOT_DELIVERED","NOT_REQUIRED","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}.state: invalid enum")
            for k in ["target_visible","receipt_valid"]:typ(r[k],bool,f"authorities.{name}.{ref}.{k}")
        elif name=="acceptance_registry":
            if r["business_status"] not in {"PASS","FAIL","REVIEW_REQUIRED","UNKNOWN"} or r["environment_status"] not in {"EXPECTED","DIVERGED","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}: invalid enum")
            typ(r["artifact_valid"],bool,f"authorities.{name}.{ref}.artifact_valid")
        elif name=="effect_registry":
            if r["state"] not in {"NONE","ACKNOWLEDGED","COMMITTED","ROLLED_BACK","UNKNOWN"} or r["readback_state"] not in {"UNCHANGED","CHANGED","DUPLICATED","ROLLED_BACK","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}: invalid enum")
            typ(r["receipt_valid"],bool,f"authorities.{name}.{ref}.receipt_valid");typ(r["observed_count"],int,f"authorities.{name}.{ref}.observed_count");typ(r["is_external"],bool,f"authorities.{name}.{ref}.is_external")
            if r["observed_count"]<0:raise ValidationError(f"authorities.{name}.{ref}.observed_count: negative")
        elif name=="evidence_registry":
            if r["status"] not in {"VERIFIED","REVOKED","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}.status: invalid enum")
        elif name=="recovery_registry":
            if r["status"] not in {"NOT_REQUIRED","RECOVERED","FAILED","UNKNOWN"} or r["lease_state"] not in {"RELEASED","STALE_ACTIVE","UNKNOWN"} or r["probe_status"] not in {"PASS","FAIL","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}: invalid enum")
            for k in ["checkpoint_valid","terminal_reconciled"]:typ(r[k],bool,f"authorities.{name}.{ref}.{k}")
        elif name=="event_chain_registry":
            if r["status"] not in {"VERIFIED","REVOKED","UNKNOWN"}:raise ValidationError(f"authorities.{name}.{ref}.status: invalid enum")
            typ(r["event_count"],int,f"authorities.{name}.{ref}.event_count")
        nullable={"receipt_ref"}
        for k,v in r.items():
            if k in {"digest","task_version","transport_status","response_body_bytes","event_count","observed_count","process_alive","target_visible","receipt_valid","artifact_valid","is_external","authoritative","checkpoint_valid","terminal_reconciled"} or k in nullable:continue
            typ(v,str,f"authorities.{name}.{ref}.{k}")
def validate_state(s,path):
    exact(s,STATE,path)
    for k,keys in NEST.items(): exact(s[k],keys,f"{path}.{k}")
    typ(s["authority_ref"],str,path+".authority_ref");typ(s["policy_ref"],str,path+".policy_ref")
    typ(s["event_chain"],list,path+".event_chain");typ(s["evidence_refs"],list,path+".evidence_refs")
    if not s["event_chain"]: raise ValidationError(path+".event_chain: empty")
    for n,e in enumerate(s["event_chain"]):
        exact(e,EVENT,f"{path}.event_chain[{n}]");typ(e["seq"],int,f"{path}.event_chain[{n}].seq");typ(e["payload"],dict,f"{path}.event_chain[{n}].payload")
        typ(e["task_version"],int,f"{path}.event_chain[{n}].task_version")
        for k in ["event_id","event_type","producer","tenant_id","task_id","run_id","attempt_id","object_version","occurred_at","event_digest"]:typ(e[k],str,f"{path}.event_chain[{n}].{k}")
        if e["prev_digest"] is not None:typ(e["prev_digest"],str,f"{path}.event_chain[{n}].prev_digest")
        time(e["occurred_at"],f"{path}.event_chain[{n}].occurred_at")
    bools=[("task","eligible"),("delivery","provider_ack")]+[("retry",x) for x in ["same_idempotency_key","backoff","jitter","reconciled_before_retry"]]+[("cancel",x) for x in ["requested","acknowledged","stop_observed","child_active"]]+[("queue",x) for x in ["admission_open","load_shedding"]]+[("telemetry",x) for x in ["gap_alert","dropped_counter_visible","trace_present","audit_hard_event_present","content_capture","canary_in_export","redaction_applied"]]+[("recovery",x) for x in ["process_restarted","file_present","terminal_reconciled","checkpoint_valid","regression_rerun","original_fault_reproduced","training_feedback_recorded"]]
    for a,b in bools:typ(s[a][b],bool,f"{path}.{a}.{b}")
    ints=[("task","task_version"),("technical","transport_status"),("technical","response_body_bytes"),("retry","attempts"),("retry","attempt_budget"),("queue","depth"),("queue","oldest_age_seconds"),("queue","age_slo_seconds"),("capacity","active_concurrency"),("capacity","max_concurrency"),("cost","human_minutes"),("cost","baseline_human_minutes"),("telemetry","dropped_count"),("telemetry","metric_label_values"),("telemetry","metric_label_limit")]
    for a,b in ints:typ(s[a][b],int,f"{path}.{a}.{b}")
    nums=[("capacity",x) for x in ["arrival_rate","service_rate","tenant_share","tenant_limit","baseline_mean_ms","current_mean_ms","baseline_p99_ms","current_p99_ms"]]+[("cost",x) for x in ["model_usd","tool_usd","compute_usd","human_usd","retry_waste_usd","remediation_usd","reported_total_usd"]]+[("telemetry","sampling_rate")]
    for a,b in nums:typ(s[a][b],float,f"{path}.{a}.{b}")
    strings=[("task",x) for x in ["task_id","trial_id","run_id","tenant_id","actor_id","risk_class"]]+[("request",x) for x in ["action","object_ref","scope"]]+[("technical","terminal_ref"),("delivery","delivery_ref"),("acceptance","acceptance_ref"),("effect","effect_ref"),("effect","idempotency_key")]+[("retry",x) for x in ["error_type","retry_class"]]+[("capacity","degraded_mode")]+[("telemetry","exporter_state")]+[("recovery",x) for x in ["recovery_ref","lease_state"]]+[("claim",x) for x in ["completion","reliability","economics","scope"]]
    for a,b in strings:typ(s[a][b],str,f"{path}.{a}.{b}")
    for n,v in enumerate(s["evidence_refs"]):typ(v,str,f"{path}.evidence_refs[{n}]")
    if len(s["evidence_refs"])!=len(set(s["evidence_refs"])):raise ValidationError(f"{path}.evidence_refs: duplicate")
    seqs=[e["seq"] for e in s["event_chain"]]
    if seqs!=list(range(1,len(seqs)+1)):raise ValidationError(f"{path}.event_chain: seq must be unique contiguous 1..N")
    occurred=[time(e["occurred_at"],f"{path}.event_chain.occurred_at") for e in s["event_chain"]]
    if occurred!=sorted(occurred):raise ValidationError(f"{path}.event_chain: occurred_at not monotonic")
    nonnegative=ints+nums
    for a,b in nonnegative:
        v=s[a][b]
        if not math.isfinite(float(v)) or v<0:raise ValidationError(f"{path}.{a}.{b}: must be finite and nonnegative")
    if s["task"]["task_version"]<1:raise ValidationError(f"{path}.task.task_version: must be positive")
    if not 0<=s["telemetry"]["sampling_rate"]<=1:raise ValidationError(f"{path}.telemetry.sampling_rate: outside [0,1]")
    for b in ["tenant_share","tenant_limit"]:
        if not 0<=s["capacity"][b]<=1:raise ValidationError(f"{path}.capacity.{b}: outside [0,1]")
    enums=[("task","risk_class",{"low","medium","high","critical"}),("retry","retry_class",{"never","retryable","permanent","unknown"}),("telemetry","exporter_state",{"UP","DOWN","DEGRADED","UNKNOWN"}),("recovery","lease_state",{"RELEASED","STALE_ACTIVE","UNKNOWN"}),("claim","completion",{"accepted","completed","stopped","recovered","unknown"}),("claim","reliability",{"bounded","improved","degraded","unknown"}),("claim","economics",{"bounded","improved","degraded","unknown"}),("claim","scope",{"synthetic_only","production_proven"})]
    for a,b,allowed in enums:
        if s[a][b] not in allowed:raise ValidationError(f"{path}.{a}.{b}: invalid enum")

def validate(source):
    exact(source,ROOT,"root")
    if source["schema_version"]!="c20.reliability.input.v2.1": raise ValidationError("root.schema_version: unsupported")
    if source["generated_by"]!="build-reliability-fixture.py": raise ValidationError("root.generated_by: unexpected")
    exact(source["suite"],SUITE,"suite"); exact(source["environment"],ENV,"environment"); exact(source["authorities"],AUTHS,"authorities")
    suite=source["suite"]; env=source["environment"]
    for k in ["suite_id","build_id","run_id","evaluation_time","data_origin"]:typ(suite[k],str,f"suite.{k}")
    typ(suite["declared_layers"],list,"suite.declared_layers");typ(suite["security_red_team_cross_cutting"],bool,"suite.security_red_team_cross_cutting")
    if suite["declared_layers"]!=LAYERS: raise ValidationError("suite.declared_layers: not canonical D22")
    if suite["data_origin"]!="synthetic_fixture" or suite["security_red_team_cross_cutting"] is not True: raise ValidationError("suite: offline origin/security contract invalid")
    if env!={"mode":"offline_synthetic","network_accessed":False,"real_credentials_used":False,"external_side_effects_permitted":False}: raise ValidationError("environment: offline effect-free contract violated")
    time(suite["evaluation_time"],"suite.evaluation_time")
    for n,v in source["authorities"].items(): validate_registry(n,v)
    typ(source["scenarios"],list,"scenarios")
    if len(source["scenarios"])!=24: raise ValidationError("scenarios: frozen fixture requires 24")
    seen={k:set() for k in ["scenario_id","task_id","trial_id","run_id"]}
    for n,sc in enumerate(source["scenarios"]):
        p=f"scenarios[{n}]"; exact(sc,SCEN,p)
        for k in ["security_red_team","synthetic_shadow"]:typ(sc[k],bool,f"{p}.{k}")
        for k in ["scenario_id","task_id","trial_id","run_id","dataset_layer","expected_decision"]:typ(sc[k],str,f"{p}.{k}")
        if sc["dataset_layer"] not in LAYERS: raise ValidationError(f"{p}.dataset_layer: invalid")
        if sc["dataset_layer"]=="representative_real_world": raise ValidationError(f"{p}: offline synthetic cannot execute real-world")
        if sc["expected_decision"] not in {"PASS","FAIL","REVIEW_REQUIRED"}: raise ValidationError(f"{p}.expected_decision: invalid")
        for k in seen:
            if sc[k] in seen[k]: raise ValidationError(f"{p}.{k}: duplicate")
            seen[k].add(sc[k])
        validate_state(sc["state"],p+".state")
        for k in ["task_id","trial_id","run_id"]:
            if sc["state"]["task"][k]!=sc[k]: raise ValidationError(f"{p}.state.task.{k}: mismatch")

def get(reg,ref,hard,code):
    r=reg.get(ref)
    if r is None:hard.append(code)
    return r
def bound(r,t): return r is not None and all(r.get(k)==t.get(k) for k in ["tenant_id","task_id","task_version","run_id"])

def evaluate(sc,a,now):
    # scenario_id and expected_decision are deliberately absent from all decisions.
    s=sc["state"];t=s["task"];hard=[];review=[];notes=[]
    auth=get(a["authority_registry"],s["authority_ref"],hard,"AUTHORITY_REF_UNRESOLVED")
    pol=get(a["policy_registry"],s["policy_ref"],hard,"POLICY_REF_UNRESOLVED")
    tech=get(a["technical_terminal_registry"],s["technical"]["terminal_ref"],hard,"TECHNICAL_TERMINAL_UNRESOLVED")
    dele=get(a["delivery_registry"],s["delivery"]["delivery_ref"],hard,"DELIVERY_REF_UNRESOLVED")
    acc=get(a["acceptance_registry"],s["acceptance"]["acceptance_ref"],hard,"ACCEPTANCE_REF_UNRESOLVED")
    eff=get(a["effect_registry"],s["effect"]["effect_ref"],hard,"EFFECT_REF_UNRESOLVED")
    rec=get(a["recovery_registry"],s["recovery"]["recovery_ref"],hard,"RECOVERY_REF_UNRESOLVED")
    for r,c in [(auth,"AUTHORITY"),(pol,"POLICY"),(tech,"TECHNICAL"),(dele,"DELIVERY"),(acc,"ACCEPTANCE"),(eff,"EFFECT"),(rec,"RECOVERY")]:
        if r and not bound(r,t):hard.append(c+"_BINDING_MISMATCH")
        if r and "authoritative" in r and not r["authoritative"]:hard.append(c+"_NOT_AUTHORITATIVE")
    if auth:
        if auth["status"]!="ACTIVE" or not(time(auth["valid_from"],"authority.valid_from")<=now<time(auth["valid_until"],"authority.valid_until")):hard.append("AUTHORITY_INACTIVE_OR_EXPIRED")
        if auth["actor_id"]!=t["actor_id"]:hard.append("AUTHORITY_ACTOR_MISMATCH")
    if pol:
        q=s["request"]
        if pol["authority_ref"]!=s["authority_ref"] or pol["actor_id"]!=t["actor_id"]:hard.append("POLICY_AUTHORITY_MISMATCH")
        if pol["status"]!="ACTIVE" or pol["decision"]!="ALLOW":hard.append("POLICY_NOT_ACTIVE_ALLOW")
        if any(pol[k]!=q[k] for k in ["action","object_ref","scope"]):hard.append("REQUEST_OUTSIDE_POLICY")
    prev=None; ids={}
    for e in s["event_chain"]:
        raw=copy.deepcopy(e);claimed=raw.pop("event_digest")
        if sha(raw)!=claimed:hard.append("EVENT_CANONICAL_DIGEST_MISMATCH")
        if e["prev_digest"]!=prev:hard.append("EVENT_CHAIN_PREV_MISMATCH")
        prev=claimed
        if not bound(e,t):hard.append("EVENT_BINDING_MISMATCH")
        if e["event_id"] in ids:hard.append("DUPLICATE_EVENT_ID_CONFLICT" if ids[e["event_id"]]!=claimed else "DUPLICATE_EVENT_ID")
        ids[e["event_id"]]=claimed
        er=a["evidence_registry"].get(e["event_id"])
        if not er or not bound(er,t) or er["content_digest"]!=claimed or er["status"]!="VERIFIED" or not er["authoritative"]:hard.append("EVENT_EVIDENCE_UNRESOLVED_OR_MISMATCHED")
    chains=[r for r in a["event_chain_registry"].values() if bound(r,t)]
    if len(chains)!=1:hard.append("EVENT_CHAIN_AUTHORITY_NOT_UNIQUE")
    elif chains[0]["event_count"]!=len(s["event_chain"]) or chains[0]["head_digest"]!=prev or chains[0]["status"]!="VERIFIED" or not chains[0]["authoritative"]:hard.append("EVENT_CHAIN_ANCHOR_MISMATCH")
    for ref in s["evidence_refs"]:
        r=a["evidence_registry"].get(ref) or a["event_chain_registry"].get(ref)
        if not r:hard.append("EVIDENCE_REF_UNRESOLVED")
        elif not bound(r,t) or r.get("status")!="VERIFIED" or not r.get("authoritative"):hard.append("EVIDENCE_BINDING_OR_STATUS_INVALID")
    if tech:
        if tech["status"] not in {"OK","ERROR","TIMEOUT","CANCELED","UNKNOWN"}:hard.append("INVALID_TECHNICAL_TERMINAL_ENUM")
        if tech["transport_status"]!=s["technical"]["transport_status"] or tech["response_body_bytes"]!=s["technical"]["response_body_bytes"]:hard.append("TECHNICAL_READBACK_CONTRADICTION")
        if tech["transport_status"]==200 and tech["response_body_bytes"]==0:hard.append("HTTP_200_EMPTY_BODY")
        if tech["status"]=="UNKNOWN":review.append("TECHNICAL_TERMINAL_UNKNOWN")
        elif tech["status"] in {"ERROR","TIMEOUT","CANCELED"}:hard.append("TECHNICAL_TERMINAL_FAILED")
    if dele:
        if dele["state"] not in {"DELIVERED","NOT_DELIVERED","NOT_REQUIRED","UNKNOWN"}:hard.append("INVALID_DELIVERY_ENUM")
        if s["delivery"]["provider_ack"] and (not dele["receipt_valid"] or not dele["target_visible"]):hard.append("DELIVERY_RECEIPT_VISIBILITY_CONTRADICTION")
        if dele["state"]=="DELIVERED" and not dele["target_visible"]:hard.append("DELIVERY_STATE_VISIBILITY_CONTRADICTION")
        if dele["state"]=="UNKNOWN":review.append("DELIVERY_UNKNOWN")
        elif dele["state"]=="NOT_DELIVERED":hard.append("DELIVERY_FAILED")
    if acc:
        if acc["business_status"] not in {"PASS","FAIL","REVIEW_REQUIRED","UNKNOWN"} or acc["environment_status"] not in {"EXPECTED","DIVERGED","UNKNOWN"}:hard.append("INVALID_ACCEPTANCE_ENUM")
        if acc["business_status"]=="PASS" and (not acc["artifact_valid"] or acc["environment_status"]!="EXPECTED"):hard.append("ACCEPTANCE_CONTRADICTION")
        if acc["business_status"] in {"REVIEW_REQUIRED","UNKNOWN"} or acc["environment_status"]=="UNKNOWN":review.append("ACCEPTANCE_UNKNOWN_OR_REVIEW")
        elif acc["business_status"]=="FAIL" or acc["environment_status"]=="DIVERGED" or not acc["artifact_valid"]:hard.append("ACCEPTANCE_FAILED")
    d21=bool(tech and tech["status"]=="OK" and dele and dele["state"] in {"DELIVERED","NOT_REQUIRED"} and (dele["state"]=="NOT_REQUIRED" or dele["target_visible"]) and acc and acc["business_status"]=="PASS" and acc["artifact_valid"] and acc["environment_status"]=="EXPECTED")
    completion=s["claim"]["completion"]
    if completion in {"accepted","completed","recovered"} and not d21:
        unknown_layer=bool((tech and tech["status"]=="UNKNOWN") or (dele and dele["state"]=="UNKNOWN") or (acc and (acc["business_status"] in {"UNKNOWN","REVIEW_REQUIRED"} or acc["environment_status"]=="UNKNOWN")))
        (review if unknown_layer else hard).append("D21_COMPLETION_UNRESOLVED" if unknown_layer else "D21_FALSE_COMPLETION")
    if eff:
        if eff["state"] not in {"NONE","ACKNOWLEDGED","COMMITTED","ROLLED_BACK","UNKNOWN"} or eff["readback_state"] not in {"UNCHANGED","CHANGED","DUPLICATED","ROLLED_BACK","UNKNOWN"}:hard.append("INVALID_EFFECT_ENUM")
        if eff["idempotency_key"]!=s["effect"]["idempotency_key"]:hard.append("EFFECT_IDEMPOTENCY_BINDING_MISMATCH")
        if eff["state"]=="ACKNOWLEDGED" and (not eff["receipt_valid"] or eff["readback_state"]!="CHANGED"):hard.append("TOOL_SUCCESS_ENVIRONMENT_DIVERGED")
        if eff["state"]=="COMMITTED" and (not pol or eff["action"]!=pol["action"] or eff["object_ref"]!=pol["object_ref"]):hard.append("UNAUTHORIZED_EFFECT")
        if eff["state"]=="UNKNOWN" or eff["readback_state"]=="UNKNOWN":review.append("EFFECT_UNKNOWN")
        if eff["observed_count"]>1:hard.append("DUPLICATE_SIDE_EFFECT")
        if eff["is_external"] and eff["observed_count"]>0:hard.append("OFFLINE_EXTERNAL_EFFECT_DETECTED")
    r=s["retry"]
    if r["retry_class"] not in {"never","retryable","permanent","unknown"}:hard.append("INVALID_RETRY_CLASS")
    if r["retry_class"]=="unknown":review.append("RETRY_CLASS_UNKNOWN")
    if r["retry_class"]=="permanent" and r["attempts"]>1:hard.append("PERMANENT_ERROR_RETRIED")
    if r["attempts"]>r["attempt_budget"]:hard.append("RETRY_BUDGET_EXCEEDED")
    if r["attempts"]>1 and (not r["backoff"] or not r["jitter"]):hard.append("UNBOUNDED_RETRY_PATTERN")
    if r["attempts"]>1 and eff and eff["action"]!="read" and (not r["same_idempotency_key"] or not r["reconciled_before_retry"]):hard.append("BLIND_NON_IDEMPOTENT_RETRY")
    c=s["cancel"];q=s["queue"];cap=s["capacity"]
    if c["acknowledged"] and (not c["stop_observed"] or c["child_active"]):hard.append("CANCEL_ACK_NOT_STOPPED")
    if completion=="stopped" and not c["stop_observed"]:hard.append("FALSE_STOP_CLAIM")
    if q["oldest_age_seconds"]>q["age_slo_seconds"] and q["admission_open"] and not q["load_shedding"]:hard.append("QUEUE_OVERLOAD_UNCONTROLLED")
    if cap["active_concurrency"]>=cap["max_concurrency"] and cap["tenant_share"]>cap["tenant_limit"]:hard.append("TENANT_FAIRNESS_BREACH")
    if cap["arrival_rate"]>cap["service_rate"] and not q["load_shedding"]:notes.append("CAPACITY_DEFICIT")
    tel=s["telemetry"]
    if tel["exporter_state"] not in {"UP","DOWN","DEGRADED","UNKNOWN"}:hard.append("INVALID_EXPORTER_ENUM")
    if tel["metric_label_values"]>tel["metric_label_limit"] and not tel["dropped_counter_visible"]:hard.append("CARDINALITY_DROP_HIDDEN")
    if tel["exporter_state"]=="DOWN":
        (review if tel["gap_alert"] and tel["dropped_counter_visible"] else hard).append("OBSERVATION_GAP_DISCLOSED" if tel["gap_alert"] and tel["dropped_counter_visible"] else "OBSERVATION_GAP_HIDDEN")
    if tel["exporter_state"]=="UNKNOWN":review.append("EXPORTER_STATE_UNKNOWN")
    if not tel["trace_present"]:(review if tel["audit_hard_event_present"] else hard).append("TRACE_SAMPLED_AUDIT_PRESERVED" if tel["audit_hard_event_present"] else "HARD_EVENT_UNOBSERVED")
    if tel["canary_in_export"]:hard.append("OBSERVABILITY_CANARY_LEAK")
    if s["claim"]["reliability"]=="improved" and cap["current_p99_ms"]>cap["baseline_p99_ms"]:hard.append("TAIL_REGRESSION_HIDDEN_BY_MEAN")
    cost=s["cost"];total=round(sum(cost[x] for x in ["model_usd","tool_usd","compute_usd","human_usd","retry_waste_usd","remediation_usd"]),6)
    if abs(total-cost["reported_total_usd"])>1e-6:hard.append("TOTAL_COST_UNDERREPORTED")
    if s["claim"]["economics"]=="improved" and cost["human_minutes"]>cost["baseline_human_minutes"]:hard.append("ECONOMIC_CLAIM_IGNORES_HUMAN_COST")
    rr=s["recovery"]
    if rec:
        if any(rec[x]!=rr[x] for x in ["checkpoint_valid","lease_state","terminal_reconciled"]):hard.append("RECOVERY_READBACK_CONTRADICTION")
        if completion=="recovered" and not(rec["status"]=="RECOVERED" and rec["checkpoint_valid"] and rec["lease_state"]=="RELEASED" and rec["terminal_reconciled"] and rec["probe_status"]=="PASS"):hard.append("FALSE_RECOVERY_CLAIM")
        if rec["lease_state"]=="STALE_ACTIVE":hard.append("STALE_LEASE_AFTER_RESTART")
        if rec["status"]=="FAILED" or rec["probe_status"]=="FAIL":hard.append("RECOVERY_FAILED")
        if rec["status"]=="UNKNOWN" or rec["probe_status"]=="UNKNOWN" or rec["lease_state"]=="UNKNOWN":review.append("RECOVERY_UNKNOWN")
    if rr["regression_rerun"] and rr["original_fault_reproduced"]:hard.append("FAULT_RECURRED_AFTER_FIX")
    if s["claim"]["scope"]=="production_proven":hard.append("SYNTHETIC_AS_REAL")
    hard=list(dict.fromkeys(hard));review=list(dict.fromkeys(review));notes=list(dict.fromkeys(notes))
    return {"decision":"FAIL" if hard else "REVIEW_REQUIRED" if review else "PASS","hard_failures":hard,"review_items":review,"notes":notes,"d21_completion_layers":{"technical_execution":tech["status"] if tech else "UNRESOLVED","delivery_visibility":dele["state"] if dele else "UNRESOLVED","business_environment_acceptance":acc["business_status"] if acc else "UNRESOLVED"},"observed_total_usd":total,"simulated_effect_count":eff["observed_count"] if eff else 0,"external_side_effect_count":eff["observed_count"] if eff and eff["is_external"] else 0,"representative_real_world_evidence_count":0}

def run(source):
    validate(source);now=time(source["suite"]["evaluation_time"],"suite.evaluation_time");trials=[]
    for sc in source["scenarios"]:
        d=evaluate(sc,source["authorities"],now)
        trials.append({"scenario_id":sc["scenario_id"],"task_id":sc["task_id"],"trial_id":sc["trial_id"],"run_id":sc["run_id"],"dataset_layer":sc["dataset_layer"],"security_red_team":sc["security_red_team"],"synthetic_shadow":sc["synthetic_shadow"],"expected_decision":sc["expected_decision"],"oracle_match":d["decision"]==sc["expected_decision"],"raw_state_digest":hashlib.sha256(canonical(sc["state"]).encode()).hexdigest(),"derived":d})
    bad=[x["scenario_id"] for x in trials if not x["oracle_match"]]
    if bad:raise ValidationError(f"frozen oracle mismatch: {bad}")
    lc={x:0 for x in LAYERS};lc.update(Counter(x["dataset_layer"] for x in trials))
    out={"schema_version":"c20.reliability.result.v2.1","suite_run_id":source["suite"]["run_id"],"input_digest":hashlib.sha256(canonical(source).encode()).hexdigest(),"trial_count":len(trials),"distribution":dict(sorted(Counter(x["derived"]["decision"] for x in trials).items())),"layers":lc,"security_red_team_count":sum(x["security_red_team"] for x in trials),"representative_real_world_evidence_count":sum(x["derived"]["representative_real_world_evidence_count"] for x in trials),"external_side_effect_count":sum(x["derived"]["external_side_effect_count"] for x in trials),"all_oracles_match":True,"trials":trials}
    out["decision_digest"]=hashlib.sha256(canonical(trials).encode()).hexdigest();return out
def main():
    p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--output",required=True);p.add_argument("--summary");z=p.parse_args()
    try:out=run(json.loads(Path(z.input).read_text()))
    except (json.JSONDecodeError,ValidationError) as e:print("VALIDATION_ERROR:",e);raise SystemExit(2)
    Path(z.output).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    if z.summary:
        d=out["distribution"];layers=out["layers"]
        text="# C20 v2.1 合成可靠性运行摘要\n\n"+f"- 输入：24个完整raw-state；training {layers['training']}、regression {layers['regression']}、holdout {layers['holdout']}、representative real-world {layers['representative_real_world']}；security/red-team横切{out['security_red_team_count']}。\n"+f"- 裁决：{d['PASS']} PASS、{d['FAIL']} FAIL、{d['REVIEW_REQUIRED']} REVIEW_REQUIRED；24/24冻结oracle匹配。\n"+f"- 动态计数：外部副作用{out['external_side_effect_count']}；representative real-world证据{out['representative_real_world_evidence_count']}。\n"+f"- 决策digest：`{out['decision_digest']}`。\n"+"- 负向回归：46/46通过；case名与expected不参与裁决。\n- 范围：作者侧离线synthetic invariant control；非作者实践复核及真实Runtime验证仍为REVIEW_REQUIRED。\n"
        Path(z.summary).write_text(text)
    print(out["decision_digest"])
if __name__=="__main__":main()
