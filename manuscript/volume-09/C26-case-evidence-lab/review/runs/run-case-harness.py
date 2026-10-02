#!/usr/bin/env python3
"""C23 closed-world, state-derived offline evidence harness.

Decisions never depend on scenario names, expected decisions, mutation labels,
or case prose. VERIFIED-REAL and ANONYMIZED-REAL are rejected before evaluation:
this offline harness is not a real-case authority.
"""
import argparse, hashlib, json, math, re, types
from collections import Counter
from datetime import datetime
from pathlib import Path

SCHEMA="c23.case.input.v2.7"; RESULT_SCHEMA="c23.case.result.v2.7"; AUTHORITY_SCHEMA="c23.case.authority-root.v2.7"
PIN_REGISTRY_SHA256="8eb8868ca19e716f333ea1f5a85241ccadd47682fd9a78db171ee28826cdd5ad"
# Historical author-side regression programs read and write this name while
# constructing mutated roots.  It is an inert compatibility marker: neither
# evaluate nor the trusted raw verifier reads it, and it is never a trust pin.
PINNED_AUTHORITY_ROOT_DIGEST="RETIRED_AUTHOR_TEST_COMPATIBILITY_ONLY"
OPENCLAW=("v2026.9.6","eb377ac59e6c9fd6c7705028034812becf00271b")
HERMES=("0.20.1","f80f453ae0679347e38abc917c7f94f717bf96c5")
CASE_TYPES={"VERIFIED-REAL","ANONYMIZED-REAL","RECONSTRUCTED","SYNTHETIC","VENDOR-CLAIM"}
STATUS={"ACTIVE","REVOKED","UNKNOWN"}; SHA=re.compile(r"^[0-9a-f]{64}$"); GIT=re.compile(r"^[0-9a-f]{40}$"); IDENT=re.compile(r"^[A-Z][A-Z0-9_.:-]{2,127}$")

def _unique_object_pairs(pairs):
    out={}
    for key,value in pairs:
        if key in out: raise ValueError("json: duplicate object key "+key)
        out[key]=value
    return out
def _make_strict_json_parser():
    # Capture a configured decoder object, not a permissive loads alias.  The
    # returned parser accepts serialized JSON only and rejects trailing bytes.
    def reject_constant(value): raise ValueError("json: non-finite constant forbidden: "+value)
    def finite_float(value):
        parsed=float(value)
        if not math.isfinite(parsed): raise ValueError("json: non-finite float forbidden: "+value)
        return parsed
    decoder=json.JSONDecoder(object_pairs_hook=_unique_object_pairs,parse_constant=reject_constant,parse_float=finite_float)
    def parse(payload):
        if isinstance(payload,bytes):
            payload=payload.decode("utf-8","strict")
        if type(payload) is not str:
            raise TypeError("json: raw UTF-8 bytes or text required; parsed objects are forbidden")
        value,end=decoder.raw_decode(payload.lstrip())
        leading=len(payload)-len(payload.lstrip())
        if payload[leading+end:].strip():
            raise ValueError("json: trailing content forbidden")
        return value
    return parse
strict_json_loads=_make_strict_json_parser()
del _make_strict_json_parser

def canonical(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def digest(v): return hashlib.sha256(canonical(v).encode()).hexdigest()
def exact(v,keys,label):
    if not isinstance(v,dict) or set(v)!=set(keys): raise ValueError(f"{label}: closed-world keys mismatch")
def enum(v,allowed,label):
    if not isinstance(v,str) or v not in allowed: raise ValueError(f"{label}: invalid enum")
def string(v,label):
    if not isinstance(v,str) or not v: raise ValueError(f"{label}: non-empty string required")
def ident(v,label):
    string(v,label)
    if not IDENT.fullmatch(v): raise ValueError(f"{label}: invalid id")
def sha(v,label):
    if not isinstance(v,str) or not SHA.fullmatch(v): raise ValueError(f"{label}: sha256 required")
def git_sha(v,label):
    if not isinstance(v,str) or not GIT.fullmatch(v): raise ValueError(f"{label}: full 40-hex git commit required")
def boolean(v,label):
    if type(v) is not bool: raise ValueError(f"{label}: bool required")
def number(v,label,minimum=0):
    if type(v) not in (int,float) or not math.isfinite(v) or v<minimum: raise ValueError(f"{label}: finite number out of range")
def integer(v,label,minimum=0):
    if type(v) is not int or v<minimum: raise ValueError(f"{label}: integer out of range")
def timestamp(v,label):
    string(v,label)
    if not v.endswith("Z"): raise ValueError(f"{label}: UTC Z timestamp required")
    try: datetime.fromisoformat(v[:-1]+"+00:00")
    except ValueError as e: raise ValueError(f"{label}: invalid timestamp") from e
def dt(v): return datetime.fromisoformat(v[:-1]+"+00:00")
def validate_record(r,keys,id_key,label):
    exact(r,list(keys)+["record_digest"],label); ident(r[id_key],label+"."+id_key); sha(r["record_digest"],label+".record_digest")
    if r["record_digest"]!=digest({k:v for k,v in r.items() if k!="record_digest"}): raise ValueError(label+": canonical digest mismatch")
def index_records(records,id_key,label,global_refs):
    if not isinstance(records,list): raise ValueError(label+": list required")
    out={}
    for i,r in enumerate(records):
        if not isinstance(r,dict) or id_key not in r: raise ValueError(f"{label}[{i}]: malformed")
        ref=r[id_key]; ident(ref,f"{label}[{i}].{id_key}")
        if ref in out or ref in global_refs: raise ValueError(label+": duplicate global id "+ref)
        out[ref]=r; global_refs.add(ref)
    return out

def scenario_manifest_entry(s):
    raw=s["raw_state"]
    return {
        "scenario_id":s["scenario_id"],"case_record_id":s["case_record_id"],"subject_id":raw["subject_id"],
        "task_id":s["task_id"],"trial_id":s["trial_id"],"run_id":s["run_id"],"evidence_id":s["evidence_id"],
        "case_version":raw["case_version"],"author_principal_id":raw["author_principal_id"],
        "raw_refs":{k:raw[k] for k in sorted(raw) if k.endswith("_ref")},
        "artifact_refs":raw["artifact_refs"],"effect_refs":raw["effect_refs"],"trial_refs":raw["trial_refs"],"failure_refs":raw["failure_refs"],
        "raw_state_digest":digest(raw),
    }
def suite_manifest(suite,scenarios):
    entries=[scenario_manifest_entry(s) for s in scenarios]
    payload={"suite_id":suite["suite_id"],"build_id":suite["build_id"],"evaluation_time":suite["evaluation_time"],"input_schema_version":SCHEMA,"result_schema_version":RESULT_SCHEMA,"scenario_manifest":entries}
    return payload|{"scenario_manifest_digest":digest(entries)}
def root_payload(root): return {"schema_version":root["schema_version"],"suite_manifest":root["suite_manifest"],"registries":root["registries"]}
def validate_authority_root(root,expected_root_digest=None):
    # The one-argument form is author-side structural validation only.  The
    # trusted closure always supplies an independently registered digest.
    if expected_root_digest is None:
        if not isinstance(root,dict) or "root_digest" not in root: raise TypeError("authority_root: parsed root required")
        expected_root_digest=root["root_digest"]
    sha(expected_root_digest,"authority_root.expected_pin")
    exact(root,["schema_version","suite_manifest","registries","root_digest"],"authority_root")
    if root["schema_version"]!=AUTHORITY_SCHEMA: raise ValueError("authority_root: unsupported schema")
    manifest=root["suite_manifest"]
    exact(manifest,["suite_id","build_id","evaluation_time","input_schema_version","result_schema_version","scenario_manifest","scenario_manifest_digest"],"authority_root.suite_manifest")
    ident(manifest["suite_id"],"authority_root.suite_id"); ident(manifest["build_id"],"authority_root.build_id"); timestamp(manifest["evaluation_time"],"authority_root.evaluation_time")
    if manifest["input_schema_version"]!=SCHEMA or manifest["result_schema_version"]!=RESULT_SCHEMA: raise ValueError("authority_root: suite schema/version mismatch")
    if not isinstance(manifest["scenario_manifest"],list) or not manifest["scenario_manifest"]: raise ValueError("authority_root: scenario manifest required")
    manifest_ids=set()
    entry_keys=["scenario_id","case_record_id","subject_id","task_id","trial_id","run_id","evidence_id","case_version","author_principal_id","raw_refs","artifact_refs","effect_refs","trial_refs","failure_refs","raw_state_digest"]
    for i,entry in enumerate(manifest["scenario_manifest"]):
        q=f"authority_root.scenario_manifest[{i}]"; exact(entry,entry_keys,q)
        for k in ("scenario_id","case_record_id","subject_id","task_id","trial_id","run_id","evidence_id","author_principal_id"): ident(entry[k],q+"."+k)
        if entry["scenario_id"] in manifest_ids: raise ValueError("authority_root: duplicate scenario id")
        manifest_ids.add(entry["scenario_id"]); integer(entry["case_version"],q+".case_version",1); sha(entry["raw_state_digest"],q+".raw_state_digest")
        if not isinstance(entry["raw_refs"],dict) or not entry["raw_refs"]: raise ValueError(q+".raw_refs: non-empty object required")
        for k,v in entry["raw_refs"].items(): string(k,q+".raw_refs.key"); ident(v,q+".raw_refs."+k)
        for k in ("artifact_refs","effect_refs","trial_refs","failure_refs"):
            if not isinstance(entry[k],list) or (k!="failure_refs" and not entry[k]) or len(entry[k])!=len(set(entry[k])): raise ValueError(q+"."+k+": unique projection required")
            for ref in entry[k]: ident(ref,q+"."+k)
    sha(manifest["scenario_manifest_digest"],"authority_root.scenario_manifest_digest")
    if manifest["scenario_manifest_digest"]!=digest(manifest["scenario_manifest"]): raise ValueError("authority_root: scenario manifest digest mismatch")
    sha(root["root_digest"],"authority_root.root_digest")
    if root["root_digest"]!=digest(root_payload(root)): raise ValueError("authority_root: canonical digest mismatch")
    if root["root_digest"]!=expected_root_digest: raise ValueError("authority_root: independently pinned digest mismatch")

def validate_document(src,authority_root):
    exact(src,["schema_version","suite","environment","registries","scenarios"],"root")
    if src["schema_version"]!=SCHEMA: raise ValueError("root: unsupported schema")
    exact(src["suite"],["suite_id","build_id","evaluation_time"],"suite"); ident(src["suite"]["suite_id"],"suite.suite_id"); ident(src["suite"]["build_id"],"suite.build_id"); timestamp(src["suite"]["evaluation_time"],"suite.evaluation_time")
    exact(src["environment"],["mode","offline","network_accessed","real_credentials_used","production_write"],"environment")
    for key in ("offline","network_accessed","real_credentials_used","production_write"): boolean(src["environment"][key],"environment."+key)
    expected_env={"mode":"OFFLINE_SYNTHETIC","offline":True,"network_accessed":False,"real_credentials_used":False,"production_write":False}
    if src["environment"]!=expected_env: raise ValueError("environment: offline invariant violated")
    names=["case_identity_registry","authorization_registry","source_registry","redaction_registry","publication_registry","reviewer_registry","principal_registry","alias_registry","author_assignment_registry","environment_registry","release_registry","task_authority_registry","input_authority_registry","permission_authority_registry","dataset_authority_registry","grader_authority_registry","budget_registry","artifact_registry","d21_registry","migration_registry","effect_registry","trial_registry","failure_registry","real_case_manifest"]
    exact(src["registries"],names,"registries")
    if src["registries"]["real_case_manifest"]!=[]: raise ValueError("offline runner rejects real_case_manifest unconditionally")
    id_keys={"case_identity_registry":"identity_id","authorization_registry":"authorization_id","source_registry":"source_id","redaction_registry":"redaction_id","publication_registry":"publication_id","reviewer_registry":"reviewer_id","principal_registry":"principal_record_id","alias_registry":"alias_record_id","author_assignment_registry":"assignment_id","environment_registry":"environment_id","release_registry":"release_id","task_authority_registry":"task_authority_id","input_authority_registry":"input_authority_id","permission_authority_registry":"permission_authority_id","dataset_authority_registry":"dataset_authority_id","grader_authority_registry":"grader_authority_id","budget_registry":"budget_id","artifact_registry":"artifact_id","d21_registry":"d21_id","migration_registry":"migration_id","effect_registry":"effect_id","trial_registry":"trial_record_id","failure_registry":"failure_id"}
    refs=set(); idx={n:index_records(src["registries"][n],k,n,refs) for n,k in id_keys.items()}
    for name,records in idx.items():
      for ref,r in records.items():
        q=name+"."+ref
        if name=="case_identity_registry":
            validate_record(r,["identity_id","case_record_id","case_version","subject_id","case_type","missing_elements","inference_list","status","revoked_at","authority_principal_id","source_digest"],"identity_id",q)
            for k in ("case_record_id","subject_id","authority_principal_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["case_type"],CASE_TYPES,q+".case_type"); enum(r["status"],STATUS,q+".status"); sha(r["source_digest"],q+".source_digest")
            if r["case_type"] in {"VERIFIED-REAL","ANONYMIZED-REAL"}: raise ValueError("offline runner rejects real case identities unconditionally")
            for k in ("missing_elements","inference_list"):
                if not isinstance(r[k],list) or len(r[k])!=len(set(r[k])): raise ValueError(q+"."+k+": unique list required")
                for x in r[k]: string(x,q+"."+k)
            if r["revoked_at"] is not None: timestamp(r["revoked_at"],q+".revoked_at")
        elif name=="authorization_registry":
            validate_record(r,["authorization_id","case_record_id","case_version","subject_id","principal_id","scopes","valid_from","valid_until","status","revoked_at","source_digest"],"authorization_id",q)
            for k in ("case_record_id","subject_id","principal_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); timestamp(r["valid_from"],q+".valid_from"); timestamp(r["valid_until"],q+".valid_until"); enum(r["status"],STATUS,q+".status"); sha(r["source_digest"],q+".source_digest")
            if not isinstance(r["scopes"],list) or not r["scopes"] or len(r["scopes"])!=len(set(r["scopes"])): raise ValueError(q+": scopes invalid")
            for x in r["scopes"]: enum(x,{"RUN_SYNTHETIC","PUBLISH_SYNTHETIC","MIGRATE_SYNTHETIC"},q+".scopes")
            if r["revoked_at"] is not None: timestamp(r["revoked_at"],q+".revoked_at")
        elif name=="source_registry":
            validate_record(r,["source_id","case_record_id","case_version","subject_id","origin","authorization_status","copyright_status","missing_elements","inference_list","status","private_content","private_content_digest","authority_principal_id"],"source_id",q)
            for k in ("case_record_id","subject_id","authority_principal_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["origin"],{"SYNTHETIC_BUILDER","RECONSTRUCTION","VENDOR_PUBLIC_PAGE"},q+".origin"); enum(r["authorization_status"],{"PASS","FAIL","UNKNOWN"},q+".authorization_status"); enum(r["copyright_status"],{"PASS","FAIL","UNKNOWN"},q+".copyright_status"); enum(r["status"],STATUS,q+".status"); sha(r["private_content_digest"],q+".private_content_digest")
            if not isinstance(r["private_content"],dict) or r["private_content_digest"]!=digest(r["private_content"]): raise ValueError(q+": private content digest mismatch")
            for k in ("missing_elements","inference_list"):
                if not isinstance(r[k],list) or len(r[k])!=len(set(r[k])): raise ValueError(q+"."+k+": unique list required")
                for x in r[k]: string(x,q+"."+k)
        elif name=="redaction_registry":
            validate_record(r,["redaction_id","case_record_id","case_version","subject_id","private_content_digest","public_content","public_content_digest","mapping","mapping_digest","status","authorized_by_principal_id"],"redaction_id",q)
            for k in ("case_record_id","subject_id","authorized_by_principal_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["status"],STATUS,q+".status")
            for k in ("private_content_digest","public_content_digest","mapping_digest"): sha(r[k],q+"."+k)
            if not isinstance(r["public_content"],dict) or r["public_content_digest"]!=digest(r["public_content"]): raise ValueError(q+": public content digest mismatch")
            if not isinstance(r["mapping"],dict) or r["mapping_digest"]!=digest(r["mapping"]): raise ValueError(q+": mapping digest mismatch")
            exact(r["mapping"],["private","public"],q+".mapping")
            if r["mapping"]["private"]!=r["private_content_digest"] or r["mapping"]["public"]!=r["public_content_digest"]: raise ValueError(q+": mapping values do not bind content digests")
        elif name=="publication_registry":
            validate_record(r,["publication_id","case_record_id","case_version","subject_id","public_artifact_id","public_content_digest","redaction_id","reviewer_id","authorization_id","scope","status","released_at"],"publication_id",q)
            for k in ("case_record_id","subject_id","public_artifact_id","redaction_id","reviewer_id","authorization_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); sha(r["public_content_digest"],q+".public_content_digest"); enum(r["scope"],{"INTERNAL","PUBLIC_SYNTHETIC"},q+".scope"); enum(r["status"],STATUS,q+".status"); timestamp(r["released_at"],q+".released_at")
        elif name=="reviewer_registry":
            validate_record(r,["reviewer_id","principal_id","aliases","roles","independence_group","reviewed_at","status"],"reviewer_id",q)
            ident(r["principal_id"],q+".principal_id"); ident(r["independence_group"],q+".independence_group"); timestamp(r["reviewed_at"],q+".reviewed_at"); enum(r["status"],STATUS,q+".status")
            for k in ("aliases","roles"):
                if not isinstance(r[k],list) or not r[k] or len(r[k])!=len(set(r[k])): raise ValueError(q+"."+k+": unique list required")
                for x in r[k]: ident(x,q+"."+k)
        elif name=="principal_registry":
            validate_record(r,["principal_record_id","principal_id","roles","independence_group","status"],"principal_record_id",q)
            ident(r["principal_id"],q+".principal_id"); ident(r["independence_group"],q+".independence_group"); enum(r["status"],STATUS,q+".status")
            if not isinstance(r["roles"],list) or not r["roles"] or len(r["roles"])!=len(set(r["roles"])): raise ValueError(q+".roles: unique list required")
            for x in r["roles"]: ident(x,q+".roles")
        elif name=="alias_registry":
            validate_record(r,["alias_record_id","alias_id","canonical_principal_id","status"],"alias_record_id",q)
            ident(r["alias_id"],q+".alias_id"); ident(r["canonical_principal_id"],q+".canonical_principal_id"); enum(r["status"],STATUS,q+".status")
        elif name=="author_assignment_registry":
            validate_record(r,["assignment_id","principal_id","role","subject_id","case_record_id","case_version","valid_from","valid_until","status"],"assignment_id",q)
            for k in ("principal_id","role","subject_id","case_record_id"): ident(r[k],q+"."+k)
            if r["role"]!="ROLE.CASE.AUTHOR": raise ValueError(q+": author role required")
            integer(r["case_version"],q+".case_version",1); timestamp(r["valid_from"],q+".valid_from"); timestamp(r["valid_until"],q+".valid_until"); enum(r["status"],STATUS,q+".status")
        elif name=="environment_registry":
            validate_record(r,["environment_id","version","manifest","manifest_digest","mode","network_accessed","real_credentials_used","production_write","status"],"environment_id",q)
            string(r["version"],q+".version"); sha(r["manifest_digest"],q+".manifest_digest"); enum(r["mode"],{"OFFLINE_SYNTHETIC"},q+".mode"); enum(r["status"],STATUS,q+".status")
            if not isinstance(r["manifest"],dict) or r["manifest_digest"]!=digest(r["manifest"]): raise ValueError(q+": manifest digest mismatch")
            for k in ("network_accessed","real_credentials_used","production_write"): boolean(r[k],q+"."+k)
        elif name=="release_registry":
            validate_record(r,["release_id","platform","version","commit","status","release_digest"],"release_id",q)
            enum(r["platform"],{"OPENCLAW","HERMES"},q+".platform"); string(r["version"],q+".version"); git_sha(r["commit"],q+".commit"); enum(r["status"],STATUS,q+".status"); sha(r["release_digest"],q+".release_digest")
            if r["release_digest"]!=digest({"platform":r["platform"],"version":r["version"],"commit":r["commit"]}): raise ValueError(q+": release digest mismatch")
        elif name=="task_authority_registry":
            validate_record(r,["task_authority_id","case_record_id","case_version","task_id","task_spec","task_digest","status"],"task_authority_id",q)
            for k in ("case_record_id","task_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["status"],STATUS,q+".status"); sha(r["task_digest"],q+".task_digest")
            if not isinstance(r["task_spec"],dict) or r["task_digest"]!=digest(r["task_spec"]): raise ValueError(q+": task authority digest mismatch")
        elif name=="input_authority_registry":
            validate_record(r,["input_authority_id","case_record_id","case_version","task_id","input_spec","input_digest","status"],"input_authority_id",q)
            for k in ("case_record_id","task_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["status"],STATUS,q+".status"); sha(r["input_digest"],q+".input_digest")
            if not isinstance(r["input_spec"],dict) or r["input_digest"]!=digest(r["input_spec"]): raise ValueError(q+": input authority digest mismatch")
        elif name=="permission_authority_registry":
            validate_record(r,["permission_authority_id","case_record_id","case_version","task_id","allowed_permissions","permissions_digest","environment_mode","status"],"permission_authority_id",q)
            for k in ("case_record_id","task_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["environment_mode"],{"OFFLINE_SYNTHETIC"},q+".environment_mode"); enum(r["status"],STATUS,q+".status"); sha(r["permissions_digest"],q+".permissions_digest")
            if not isinstance(r["allowed_permissions"],list) or not r["allowed_permissions"] or len(r["allowed_permissions"])!=len(set(r["allowed_permissions"])): raise ValueError(q+": allowed permissions invalid")
            for x in r["allowed_permissions"]: ident(x,q+".allowed_permissions")
            if not set(r["allowed_permissions"]).issubset({"READ.SYNTHETIC","WRITE.SYNTHETIC"}): raise ValueError(q+": production or unknown permission forbidden in offline authority")
            if r["permissions_digest"]!=digest(r["allowed_permissions"]): raise ValueError(q+": permission authority digest mismatch")
        elif name=="dataset_authority_registry":
            validate_record(r,["dataset_authority_id","case_record_id","case_version","task_id","data_spec","data_digest","rights_status","allowed_environment_mode","allowed_case_types","status"],"dataset_authority_id",q)
            for k in ("case_record_id","task_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); sha(r["data_digest"],q+".data_digest"); enum(r["rights_status"],{"PASS","FAIL","UNKNOWN"},q+".rights_status"); enum(r["allowed_environment_mode"],{"OFFLINE_SYNTHETIC"},q+".allowed_environment_mode"); enum(r["status"],STATUS,q+".status")
            if not isinstance(r["data_spec"],dict) or r["data_digest"]!=digest(r["data_spec"]): raise ValueError(q+": dataset authority digest mismatch")
            if r["data_spec"].get("dataset")!="SYNTHETIC" or r["data_spec"].get("rights")!="SYNTHETIC_ONLY" or r["data_spec"].get("environment")!="OFFLINE_SYNTHETIC": raise ValueError(q+": production or rights-unknown dataset forbidden in offline authority")
            if not isinstance(r["allowed_case_types"],list) or not r["allowed_case_types"] or len(r["allowed_case_types"])!=len(set(r["allowed_case_types"])): raise ValueError(q+": allowed case types invalid")
            for x in r["allowed_case_types"]: enum(x,CASE_TYPES,q+".allowed_case_types")
        elif name=="grader_authority_registry":
            validate_record(r,["grader_authority_id","case_record_id","case_version","task_id","grader_principal_id","eval_spec","eval_digest","independence_required","status"],"grader_authority_id",q)
            for k in ("case_record_id","task_id","grader_principal_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); sha(r["eval_digest"],q+".eval_digest"); boolean(r["independence_required"],q+".independence_required"); enum(r["status"],STATUS,q+".status")
            if not isinstance(r["eval_spec"],dict) or r["eval_digest"]!=digest(r["eval_spec"]): raise ValueError(q+": grader authority digest mismatch")
        elif name=="budget_registry":
            validate_record(r,["budget_id","case_record_id","case_version","task_id","run_id","side","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","task_spec","task_digest","input_spec","input_digest","risk","permissions","permissions_digest","data_spec","data_digest","eval_spec","eval_digest","model_usd","tool_usd","compute_usd","human_minutes","human_usd","elapsed_seconds","total_usd","contract_digest","status"],"budget_id",q)
            for k in ("case_record_id","task_id","run_id","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["side"],{"BASELINE","CANDIDATE"},q+".side")
            for k in ("task_digest","input_digest","permissions_digest","data_digest","eval_digest"): sha(r[k],q+"."+k)
            for k in ("task_spec","input_spec","data_spec","eval_spec"):
                if not isinstance(r[k],dict): raise ValueError(q+"."+k+": object required")
            if not isinstance(r["permissions"],list) or not r["permissions"] or len(r["permissions"])!=len(set(r["permissions"])): raise ValueError(q+".permissions: unique non-empty list required")
            for x in r["permissions"]: ident(x,q+".permissions")
            if r["task_digest"]!=digest(r["task_spec"]) or r["input_digest"]!=digest(r["input_spec"]) or r["permissions_digest"]!=digest(r["permissions"]) or r["data_digest"]!=digest(r["data_spec"]) or r["eval_digest"]!=digest(r["eval_spec"]): raise ValueError(q+": comparison payload digest mismatch")
            enum(r["risk"],{"R0","R1","R2","R3","R4"},q+".risk"); enum(r["status"],STATUS,q+".status")
            for k in ("model_usd","tool_usd","compute_usd","human_minutes","human_usd","elapsed_seconds","total_usd"): number(r[k],q+"."+k)
            sha(r["contract_digest"],q+".contract_digest")
            contract_keys=("case_record_id","case_version","task_id","run_id","side","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","task_digest","input_digest","risk","permissions_digest","data_digest","eval_digest","model_usd","tool_usd","compute_usd","human_minutes","human_usd","elapsed_seconds","total_usd")
            if r["contract_digest"]!=digest({k:r[k] for k in contract_keys}): raise ValueError(q+": budget contract digest mismatch")
        elif name=="artifact_registry":
            validate_record(r,["artifact_id","case_record_id","case_version","task_id","run_id","evidence_id","kind","payload","content_digest","status","source_id","recorded_at"],"artifact_id",q)
            for k in ("case_record_id","task_id","run_id","evidence_id","source_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["kind"],{"PUBLIC_CASE","TECHNICAL_EVIDENCE","DELIVERY_EVIDENCE","ACCEPTANCE_EVIDENCE","FAILURE_LOG"},q+".kind"); sha(r["content_digest"],q+".content_digest"); enum(r["status"],STATUS,q+".status")
            if not isinstance(r["payload"],dict) or r["content_digest"]!=digest(r["payload"]): raise ValueError(q+": artifact payload digest mismatch")
            timestamp(r["recorded_at"],q+".recorded_at")
        elif name=="d21_registry":
            validate_record(r,["d21_id","case_record_id","case_version","task_id","run_id","evidence_id","technical","delivery","business_environment","technical_evidence_id","delivery_evidence_id","acceptance_evidence_id","status","recorded_at"],"d21_id",q)
            for k in ("case_record_id","task_id","run_id","evidence_id","technical_evidence_id","delivery_evidence_id","acceptance_evidence_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["technical"],{"PASS","FAIL","UNKNOWN"},q+".technical"); enum(r["delivery"],{"PASS","FAIL","UNKNOWN"},q+".delivery"); enum(r["business_environment"],{"PASS","FAIL","UNKNOWN"},q+".business_environment"); enum(r["status"],STATUS,q+".status"); timestamp(r["recorded_at"],q+".recorded_at")
        elif name=="migration_registry":
            validate_record(r,["migration_id","case_record_id","case_version","task_id","run_id","evidence_id","baseline_release_id","candidate_release_id","baseline_contract","candidate_contract","unsupported_capabilities","adapter_differences","status"],"migration_id",q)
            for k in ("case_record_id","task_id","run_id","evidence_id","baseline_release_id","candidate_release_id"): ident(r[k],q+"."+k)
            integer(r["case_version"],q+".case_version",1); enum(r["status"],STATUS,q+".status")
            for side in ("baseline_contract","candidate_contract"):
                exact(r[side],["case_record_id","case_version","task_id","run_id","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","task_digest","input_digest","budget_id","budget_contract_digest","risk","permissions_digest","data_digest","eval_digest"],q+"."+side)
                for k in ("case_record_id","task_id","run_id","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","budget_id"): ident(r[side][k],q+"."+side+"."+k)
                integer(r[side]["case_version"],q+"."+side+".case_version",1)
                for k in ("task_digest","input_digest","permissions_digest","data_digest","eval_digest"): sha(r[side][k],q+"."+side+"."+k)
                sha(r[side]["budget_contract_digest"],q+"."+side+".budget_contract_digest"); enum(r[side]["risk"],{"R0","R1","R2","R3","R4"},q+"."+side+".risk")
            if not isinstance(r["unsupported_capabilities"],list) or len(r["unsupported_capabilities"])!=len(set(r["unsupported_capabilities"])): raise ValueError(q+".unsupported_capabilities: unique list required")
            for x in r["unsupported_capabilities"]: string(x,q+".unsupported_capabilities")
            if not isinstance(r["adapter_differences"],list): raise ValueError(q+".adapter_differences: list required")
            seen_differences=set()
            categories={"PERMISSION","AUTHORIZATION","DATA","EVALUATION","TERMINAL_STATE","SECURITY","STATE_CARRIER","TOOL_SCHEMA","MESSAGE_SEMANTICS"}
            contracts={"PERMISSIONS","AUTHORITY","DATA","GRADER","D21_TERMINAL","SECURITY_BOUNDARY","STATE_TRANSPORT","TOOL_INTERFACE","MESSAGE_PROTOCOL"}
            for j,x in enumerate(r["adapter_differences"]):
                label=f"{q}.adapter_differences[{j}]"; exact(x,["category","criticality","affected_contract","evidence_ref","owner","disposition"],label)
                enum(x["category"],categories,label+".category"); enum(x["criticality"],{"CRITICAL","NON_CRITICAL"},label+".criticality"); enum(x["affected_contract"],contracts,label+".affected_contract"); ident(x["evidence_ref"],label+".evidence_ref"); ident(x["owner"],label+".owner"); enum(x["disposition"],{"FAIL","REVIEW_REQUIRED","ACCEPTED"},label+".disposition")
                key=canonical(x)
                if key in seen_differences: raise ValueError(q+".adapter_differences: duplicate object")
                seen_differences.add(key)
        elif name=="effect_registry":
            validate_record(r,["effect_id","case_record_id","task_id","run_id","evidence_id","effect_kind","external","authorized","receipt","receipt_digest","readback","readback_digest","status","recorded_at"],"effect_id",q)
            for k in ("case_record_id","task_id","run_id","evidence_id"): ident(r[k],q+"."+k)
            enum(r["effect_kind"],{"NONE","SYNTHETIC_WRITE","EXTERNAL_WRITE"},q+".effect_kind"); boolean(r["external"],q+".external"); boolean(r["authorized"],q+".authorized"); sha(r["receipt_digest"],q+".receipt_digest"); sha(r["readback_digest"],q+".readback_digest"); enum(r["status"],STATUS,q+".status")
            if not isinstance(r["receipt"],dict) or r["receipt_digest"]!=digest(r["receipt"]): raise ValueError(q+": receipt digest mismatch")
            if not isinstance(r["readback"],dict) or r["readback_digest"]!=digest(r["readback"]): raise ValueError(q+": readback digest mismatch")
            timestamp(r["recorded_at"],q+".recorded_at")
        elif name=="trial_registry":
            validate_record(r,["trial_record_id","trial_id","case_record_id","task_id","run_id","evidence_id","status","failure_ref","recorded_at"],"trial_record_id",q)
            for k in ("trial_id","case_record_id","task_id","run_id","evidence_id","failure_ref"): ident(r[k],q+"."+k)
            enum(r["status"],{"PASS","FAIL","UNKNOWN"},q+".status"); timestamp(r["recorded_at"],q+".recorded_at")
        elif name=="failure_registry":
            validate_record(r,["failure_id","case_record_id","task_id","trial_id","run_id","evidence_id","artifact_id","status","recorded_at"],"failure_id",q)
            for k in ("case_record_id","task_id","trial_id","run_id","evidence_id","artifact_id"): ident(r[k],q+"."+k)
            enum(r["status"],STATUS,q+".status"); timestamp(r["recorded_at"],q+".recorded_at")
    if not isinstance(src["scenarios"],list) or not src["scenarios"]: raise ValueError("scenarios: non-empty list required")
    seen={k:set() for k in ("scenario_id","case_record_id","task_id","trial_id","run_id","evidence_id")}; scenario_global=set()
    raw_keys=["case_version","subject_id","author_principal_id","author_assignment_ref","identity_ref","authorization_ref","source_ref","redaction_ref","publication_ref","reviewer_ref","environment_ref","baseline_release_ref","candidate_release_ref","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","baseline_budget_ref","candidate_budget_ref","artifact_refs","d21_ref","migration_ref","effect_refs","trial_refs","failure_refs","trial_count","failure_count","failures_preserved","holdout_accessed","grader_private_access"]
    for i,s in enumerate(src["scenarios"]):
        q=f"scenarios[{i}]"; exact(s,["scenario_id","case_record_id","task_id","trial_id","run_id","evidence_id","raw_state"],q)
        for k in seen:
            ident(s[k],q+"."+k)
            if s[k] in seen[k]: raise ValueError(q+"."+k+": duplicate")
            if s[k] in scenario_global: raise ValueError(q+"."+k+": cross-type global id collision")
            seen[k].add(s[k])
            scenario_global.add(s[k])
        raw=s["raw_state"]; exact(raw,raw_keys,q+".raw_state"); integer(raw["case_version"],q+".case_version",1); ident(raw["subject_id"],q+".subject_id"); ident(raw["author_principal_id"],q+".author_principal_id")
        for k in ("author_assignment_ref","identity_ref","authorization_ref","source_ref","redaction_ref","publication_ref","reviewer_ref","environment_ref","baseline_release_ref","candidate_release_ref","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","baseline_budget_ref","candidate_budget_ref","d21_ref","migration_ref"): ident(raw[k],q+"."+k)
        for k in ("artifact_refs","effect_refs","trial_refs","failure_refs"):
            if not isinstance(raw[k],list) or len(raw[k])!=len(set(raw[k])): raise ValueError(q+"."+k+": unique list required")
            for x in raw[k]: ident(x,q+"."+k)
        integer(raw["trial_count"],q+".trial_count",0); integer(raw["failure_count"],q+".failure_count",0)
        for k in ("failures_preserved","holdout_accessed","grader_private_access"): boolean(raw[k],q+"."+k)
    manifest=authority_root["suite_manifest"]
    if src["suite"]!={k:manifest[k] for k in ("suite_id","build_id","evaluation_time")}: raise ValueError("suite: frozen provenance mismatch")
    actual_manifest=[scenario_manifest_entry(s) for s in src["scenarios"]]
    if actual_manifest!=manifest["scenario_manifest"]: raise ValueError("scenarios: frozen ordered manifest/projection mismatch")
    projected={k:set() for k in ("artifact_refs","effect_refs","trial_refs","failure_refs")}
    for entry in actual_manifest:
        for k in projected: projected[k].update(entry[k])
    registry_projection={"artifact_refs":set(idx["artifact_registry"]),"effect_refs":set(idx["effect_registry"]),"trial_refs":set(idx["trial_registry"]),"failure_refs":set(idx["failure_registry"])}
    for k in projected:
        if projected[k]!=registry_projection[k]: raise ValueError("scenarios: incomplete global "+k+" projection")
    # Every case-scoped single-value registry is an exact projection.  A root
    # may not carry a second, unselected truth for the same case.
    single_projection={
        "identity_ref":"case_identity_registry","authorization_ref":"authorization_registry",
        "source_ref":"source_registry","redaction_ref":"redaction_registry",
        "publication_ref":"publication_registry","reviewer_ref":"reviewer_registry",
        "author_assignment_ref":"author_assignment_registry","environment_ref":"environment_registry",
        "task_authority_ref":"task_authority_registry","input_authority_ref":"input_authority_registry",
        "permission_authority_ref":"permission_authority_registry","dataset_authority_ref":"dataset_authority_registry",
        "grader_authority_ref":"grader_authority_registry",
        "d21_ref":"d21_registry","migration_ref":"migration_registry",
    }
    for raw_key,registry in single_projection.items():
        selected={s["raw_state"][raw_key] for s in src["scenarios"]}
        if selected!=set(idx[registry]): raise ValueError(f"scenarios: incomplete exact {registry} projection")
    paired_projection={
        "release_registry":{
            ref for s in src["scenarios"]
            for ref in (s["raw_state"]["baseline_release_ref"],s["raw_state"]["candidate_release_ref"])
        },
        "budget_registry":{
            ref for s in src["scenarios"]
            for ref in (s["raw_state"]["baseline_budget_ref"],s["raw_state"]["candidate_budget_ref"])
        },
    }
    for registry,selected in paired_projection.items():
        if selected!=set(idx[registry]): raise ValueError(f"scenarios: incomplete exact {registry} projection")
    referenced_principals=set()
    referenced_principals.update(s["raw_state"]["author_principal_id"] for s in src["scenarios"])
    referenced_principals.update(x["principal_id"] for x in idx["authorization_registry"].values())
    referenced_principals.update(x["authority_principal_id"] for x in idx["case_identity_registry"].values())
    referenced_principals.update(x["authority_principal_id"] for x in idx["source_registry"].values())
    referenced_principals.update(x["authorized_by_principal_id"] for x in idx["redaction_registry"].values())
    referenced_principals.update(x["principal_id"] for x in idx["reviewer_registry"].values())
    referenced_principals.update(x["principal_id"] for x in idx["author_assignment_registry"].values())
    referenced_principals.update(x["grader_principal_id"] for x in idx["grader_authority_registry"].values())
    referenced_principals.update(
        difference["owner"] for migration in idx["migration_registry"].values()
        for difference in migration["adapter_differences"]
    )
    alias_to_principal={x["alias_id"]:x["canonical_principal_id"] for x in idx["alias_registry"].values()}
    projected_principals={alias_to_principal.get(x,x) for x in referenced_principals}
    registered_principals={x["principal_id"] for x in idx["principal_registry"].values()}
    if projected_principals!=registered_principals: raise ValueError("scenarios: incomplete exact principal_registry projection")
    semantic_keys={
        "case_identity_registry":lambda x:(x["case_record_id"],x["case_version"],x["subject_id"]),
        "authorization_registry":lambda x:(x["case_record_id"],x["case_version"],x["subject_id"]),
        "source_registry":lambda x:(x["case_record_id"],x["case_version"],x["subject_id"]),
        "redaction_registry":lambda x:(x["case_record_id"],x["case_version"],x["subject_id"]),
        "publication_registry":lambda x:(x["case_record_id"],x["case_version"],x["subject_id"]),
        "author_assignment_registry":lambda x:(x["case_record_id"],x["case_version"],x["subject_id"],x["role"]),
        "task_authority_registry":lambda x:(x["case_record_id"],x["case_version"],x["task_id"]),
        "input_authority_registry":lambda x:(x["case_record_id"],x["case_version"],x["task_id"]),
        "permission_authority_registry":lambda x:(x["case_record_id"],x["case_version"],x["task_id"]),
        "dataset_authority_registry":lambda x:(x["case_record_id"],x["case_version"],x["task_id"]),
        "grader_authority_registry":lambda x:(x["case_record_id"],x["case_version"],x["task_id"]),
        "budget_registry":lambda x:(x["case_record_id"],x["case_version"],x["task_id"],x["run_id"],x["side"]),
        "d21_registry":lambda x:(x["case_record_id"],x["case_version"],x["task_id"],x["run_id"],x["evidence_id"]),
        "migration_registry":lambda x:(x["case_record_id"],x["case_version"],x["task_id"],x["run_id"],x["evidence_id"]),
        "principal_registry":lambda x:x["principal_id"],
        "alias_registry":lambda x:x["alias_id"],
    }
    for registry,key_fn in semantic_keys.items():
        keys=[key_fn(x) for x in idx[registry].values()]
        if len(keys)!=len(set(keys)): raise ValueError(registry+": duplicate semantic key")
    artifact_semantic_keys=[]
    for artifact in idx["artifact_registry"].values():
        base=(artifact["case_record_id"],artifact["case_version"],artifact["task_id"],artifact["run_id"],artifact["evidence_id"],artifact["kind"])
        if artifact["kind"]=="FAILURE_LOG":
            base=base+(artifact["payload"].get("failure_id"),artifact["payload"].get("trial_id"))
        artifact_semantic_keys.append(base)
    if len(artifact_semantic_keys)!=len(set(artifact_semantic_keys)): raise ValueError("artifact_registry: duplicate semantic key")
    return idx

def _evaluate_with_pin(src,authority_root,expected_root_digest):
    validate_authority_root(authority_root,expected_root_digest)
    idx=validate_document(src,authority_root); at=dt(src["suite"]["evaluation_time"]); trials=[]
    frozen_mismatch=src["registries"]!=authority_root["registries"]
    principal_by_id={p["principal_id"]:p for p in idx["principal_registry"].values()}
    alias_to_canonical={}
    for alias in idx["alias_registry"].values():
        if alias["alias_id"] in alias_to_canonical or alias["alias_id"] in principal_by_id: raise ValueError("alias_registry: ambiguous alias")
        if alias["canonical_principal_id"] not in principal_by_id: raise ValueError("alias_registry: canonical principal missing")
        if alias["status"]!="ACTIVE": raise ValueError("alias_registry: inactive alias in frozen root")
        alias_to_canonical[alias["alias_id"]]=alias["canonical_principal_id"]
    def normalize_principal(value):
        return value if value in principal_by_id else alias_to_canonical.get(value)
    for s in src["scenarios"]:
        raw=s["raw_state"]; fail=["FROZEN_REGISTRY_ROOT_MISMATCH"] if frozen_mismatch else []; rr=[]
        def get(reg,ref,reason):
            v=idx[reg].get(ref)
            if v is None: rr.append(reason)
            return v
        identity=get("case_identity_registry",raw["identity_ref"],"IDENTITY_NOT_RESOLVED"); assignment=get("author_assignment_registry",raw["author_assignment_ref"],"AUTHOR_ASSIGNMENT_NOT_RESOLVED"); auth=get("authorization_registry",raw["authorization_ref"],"AUTHORIZATION_NOT_RESOLVED"); source=get("source_registry",raw["source_ref"],"SOURCE_NOT_RESOLVED"); redaction=get("redaction_registry",raw["redaction_ref"],"REDACTION_NOT_RESOLVED"); publication=get("publication_registry",raw["publication_ref"],"PUBLICATION_NOT_RESOLVED"); reviewer=get("reviewer_registry",raw["reviewer_ref"],"REVIEWER_NOT_RESOLVED"); env=get("environment_registry",raw["environment_ref"],"ENVIRONMENT_NOT_RESOLVED"); br=get("release_registry",raw["baseline_release_ref"],"BASELINE_RELEASE_NOT_RESOLVED"); cr=get("release_registry",raw["candidate_release_ref"],"CANDIDATE_RELEASE_NOT_RESOLVED"); ta=get("task_authority_registry",raw["task_authority_ref"],"TASK_AUTHORITY_NOT_RESOLVED"); ia=get("input_authority_registry",raw["input_authority_ref"],"INPUT_AUTHORITY_NOT_RESOLVED"); pa=get("permission_authority_registry",raw["permission_authority_ref"],"PERMISSION_AUTHORITY_NOT_RESOLVED"); da=get("dataset_authority_registry",raw["dataset_authority_ref"],"DATASET_AUTHORITY_NOT_RESOLVED"); ga=get("grader_authority_registry",raw["grader_authority_ref"],"GRADER_AUTHORITY_NOT_RESOLVED"); bb=get("budget_registry",raw["baseline_budget_ref"],"BASELINE_BUDGET_NOT_RESOLVED"); cb=get("budget_registry",raw["candidate_budget_ref"],"CANDIDATE_BUDGET_NOT_RESOLVED"); d21=get("d21_registry",raw["d21_ref"],"D21_NOT_RESOLVED"); migration=get("migration_registry",raw["migration_ref"],"MIGRATION_NOT_RESOLVED"); arts=[get("artifact_registry",x,"ARTIFACT_NOT_RESOLVED") for x in raw["artifact_refs"]]; effects=[get("effect_registry",x,"EFFECT_NOT_RESOLVED") for x in raw["effect_refs"]]; run_trials=[get("trial_registry",x,"TRIAL_NOT_RESOLVED") for x in raw["trial_refs"]]; failures=[get("failure_registry",x,"FAILURE_NOT_RESOLVED") for x in raw["failure_refs"]]
        for r in [x for x in (identity,auth,source,redaction,publication,d21,migration) if x]:
            if r.get("case_record_id")!=s["case_record_id"] or r.get("case_version")!=raw["case_version"]: fail.append("CASE_VERSION_BINDING_MISMATCH")
        for r in (identity,auth,source,redaction,publication):
            if r and r.get("subject_id")!=raw["subject_id"]: fail.append("SUBJECT_BINDING_MISMATCH")
        if identity:
            if identity["status"]=="UNKNOWN": rr.append("CASE_IDENTITY_UNKNOWN")
            elif identity["status"]!="ACTIVE" or identity["revoked_at"] is not None: fail.append("CASE_IDENTITY_REVOKED")
            if source and identity["source_digest"]!=source["private_content_digest"]: fail.append("IDENTITY_SOURCE_DIGEST_MISMATCH")
            if identity["case_type"]=="VENDOR-CLAIM": rr.append("VENDOR_NOT_INDEPENDENT_EVIDENCE")
            if identity["case_type"]=="RECONSTRUCTED":
                if not identity["missing_elements"] or not identity["inference_list"]: fail.append("RECONSTRUCTION_LIMITATIONS_MISSING")
                elif source and (identity["missing_elements"]!=source["missing_elements"] or identity["inference_list"]!=source["inference_list"]): fail.append("RECONSTRUCTION_SOURCE_DIFFERENCE_MISMATCH")
                else: rr.append("RECONSTRUCTED_EVIDENCE_LIMITED")
            elif identity["missing_elements"] or identity["inference_list"]: fail.append("NON_RECONSTRUCTED_LIMITATIONS_PRESENT")
        if auth:
            if auth["status"]!="ACTIVE" or auth["revoked_at"] is not None: fail.append("AUTHORIZATION_INACTIVE")
            if not (datetime.fromisoformat(auth["valid_from"][:-1]+"+00:00")<=at<=datetime.fromisoformat(auth["valid_until"][:-1]+"+00:00")): fail.append("AUTHORIZATION_EXPIRED")
            if not {"RUN_SYNTHETIC","PUBLISH_SYNTHETIC","MIGRATE_SYNTHETIC"}.issubset(set(auth["scopes"])): fail.append("AUTHORIZATION_SCOPE_INSUFFICIENT")
            if source and auth["source_digest"]!=source["private_content_digest"]: fail.append("AUTHORIZATION_SOURCE_DIGEST_MISMATCH")
        author_canonical=normalize_principal(raw["author_principal_id"])
        if not author_canonical: fail.append("AUTHOR_PRINCIPAL_UNKNOWN")
        if assignment:
            assigned_canonical=normalize_principal(assignment["principal_id"])
            if assignment["status"]!="ACTIVE" or assignment["role"]!="ROLE.CASE.AUTHOR" or assigned_canonical!=author_canonical or assignment["subject_id"]!=raw["subject_id"] or assignment["case_record_id"]!=s["case_record_id"] or assignment["case_version"]!=raw["case_version"] or not (dt(assignment["valid_from"])<=at<=dt(assignment["valid_until"])): fail.append("AUTHOR_ASSIGNMENT_INVALID")
        if identity and auth and source and redaction:
            principals={normalize_principal(identity["authority_principal_id"]),normalize_principal(auth["principal_id"]),normalize_principal(source["authority_principal_id"]),normalize_principal(redaction["authorized_by_principal_id"])}
            if len(principals)!=1: fail.append("AUTHORITY_PRINCIPAL_BINDING_MISMATCH")
            elif author_canonical in principals: fail.append("SELF_AUTHORIZATION_FORBIDDEN")
        if source:
            if "UNKNOWN" in (source["status"],source["authorization_status"],source["copyright_status"]): rr.append("SOURCE_REVIEW_UNKNOWN")
            if source["status"]=="REVOKED" or "FAIL" in (source["authorization_status"],source["copyright_status"]): fail.append("SOURCE_OR_COPYRIGHT_INVALID")
            if identity:
                origin_matrix={"SYNTHETIC":"SYNTHETIC_BUILDER","RECONSTRUCTED":"RECONSTRUCTION","VENDOR-CLAIM":"VENDOR_PUBLIC_PAGE"}
                expected_origin=origin_matrix.get(identity["case_type"])
                if expected_origin is None or source["origin"]!=expected_origin: fail.append("CASE_SOURCE_TYPE_MISMATCH")
                if identity["case_type"]!="RECONSTRUCTED" and (source["missing_elements"] or source["inference_list"]): fail.append("SOURCE_DIFFERENCE_CLASS_MISMATCH")
        if redaction:
            if redaction["status"]=="UNKNOWN": rr.append("REDACTION_UNKNOWN")
            elif redaction["status"]!="ACTIVE": fail.append("REDACTION_INACTIVE")
            if source and redaction["private_content_digest"]!=source["private_content_digest"]: fail.append("PRIVATE_DIGEST_MISMATCH")
        if reviewer:
            if reviewer["status"]=="UNKNOWN": rr.append("REVIEWER_UNKNOWN")
            elif reviewer["status"]!="ACTIVE": fail.append("REVIEWER_INACTIVE")
            reviewer_canonical=normalize_principal(reviewer["principal_id"])
            if any(normalize_principal(alias)!=reviewer_canonical for alias in reviewer["aliases"]): fail.append("REVIEWER_ALIAS_BINDING_INVALID")
            if author_canonical==reviewer_canonical: fail.append("REVIEWER_NOT_INDEPENDENT")
            author_principal=principal_by_id.get(author_canonical); authority_principal=principal_by_id.get(normalize_principal(auth["principal_id"]) if auth else "NONE"); reviewer_principal=principal_by_id.get(reviewer_canonical)
            if not author_principal or author_principal["status"]!="ACTIVE" or "ROLE.CASE.AUTHOR" not in author_principal["roles"]: fail.append("AUTHOR_PRINCIPAL_ROLE_INVALID")
            if not authority_principal or authority_principal["status"]!="ACTIVE" or "ROLE.CASE.AUTHORITY" not in authority_principal["roles"]: fail.append("AUTHORITY_PRINCIPAL_ROLE_INVALID")
            if not reviewer_principal or reviewer_principal["status"]!="ACTIVE" or "ROLE.INDEPENDENT.REVIEWER" not in reviewer_principal["roles"] or "ROLE.INDEPENDENT.REVIEWER" not in reviewer["roles"]: fail.append("REVIEWER_ROLE_INVALID")
            if author_principal and reviewer_principal and author_principal["independence_group"]==reviewer_principal["independence_group"]: fail.append("REVIEWER_GROUP_NOT_INDEPENDENT")
            if reviewer_principal and reviewer_principal["independence_group"]!=reviewer["independence_group"]: fail.append("REVIEWER_GROUP_BINDING_MISMATCH")
            # Independence is evaluated against every active author assignment
            # for this case/version, not merely the raw-state-selected author.
            active_case_authors={normalize_principal(x["principal_id"]) for x in idx["author_assignment_registry"].values() if x["status"]=="ACTIVE" and x["case_record_id"]==s["case_record_id"] and x["case_version"]==raw["case_version"] and x["subject_id"]==raw["subject_id"] and dt(x["valid_from"])<=dt(reviewer["reviewed_at"])<=dt(x["valid_until"])}
            if reviewer_canonical in active_case_authors: fail.append("REVIEWER_HAS_ACTIVE_AUTHOR_ASSIGNMENT")
        if ga:
            grader_canonical=normalize_principal(ga["grader_principal_id"])
            grader_principal=principal_by_id.get(grader_canonical)
            if ga["status"]!="ACTIVE" or not ga["independence_required"]: fail.append("GRADER_AUTHORITY_INACTIVE_OR_WEAK")
            if ga["case_record_id"]!=s["case_record_id"] or ga["case_version"]!=raw["case_version"] or ga["task_id"]!=s["task_id"]: fail.append("GRADER_AUTHORITY_BINDING_MISMATCH")
            if not grader_principal or grader_principal["status"]!="ACTIVE" or "ROLE.INDEPENDENT.REVIEWER" not in grader_principal["roles"]: fail.append("GRADER_PRINCIPAL_ROLE_INVALID")
            grader_authors={normalize_principal(x["principal_id"]) for x in idx["author_assignment_registry"].values() if x["status"]=="ACTIVE" and x["case_record_id"]==s["case_record_id"] and x["case_version"]==raw["case_version"]}
            if grader_canonical==author_canonical or grader_canonical in grader_authors: fail.append("GRADER_NOT_INDEPENDENT")
            if reviewer and grader_canonical!=normalize_principal(reviewer["principal_id"]): fail.append("GRADER_REVIEWER_ASSIGNMENT_MISMATCH")
        if publication:
            if publication["status"]=="UNKNOWN": rr.append("PUBLICATION_UNKNOWN")
            elif publication["status"]!="ACTIVE": fail.append("PUBLICATION_INACTIVE")
            if redaction and (publication["redaction_id"]!=redaction["redaction_id"] or publication["public_content_digest"]!=redaction["public_content_digest"]): fail.append("PUBLIC_PRIVATE_MAPPING_MISMATCH")
            if reviewer and publication["reviewer_id"]!=reviewer["reviewer_id"]: fail.append("PUBLICATION_REVIEWER_MISMATCH")
            if auth and publication["authorization_id"]!=auth["authorization_id"]: fail.append("PUBLICATION_AUTHORIZATION_MISMATCH")
            public_artifact=idx["artifact_registry"].get(publication["public_artifact_id"])
            if not public_artifact or public_artifact["status"]=="UNKNOWN": rr.append("PUBLIC_ARTIFACT_UNKNOWN")
            elif public_artifact["kind"]!="PUBLIC_CASE" or public_artifact["status"]!="ACTIVE" or public_artifact["content_digest"]!=publication["public_content_digest"]: fail.append("PUBLIC_ARTIFACT_CONTENT_MISMATCH")
            if auth:
                released=dt(publication["released_at"])
                if not (dt(auth["valid_from"])<=released<=dt(auth["valid_until"])): fail.append("PUBLICATION_OUTSIDE_AUTHORIZATION_WINDOW")
                if released>at: fail.append("PUBLICATION_AFTER_EVALUATION")
                if reviewer and dt(reviewer["reviewed_at"])>released: fail.append("PUBLICATION_BEFORE_REVIEW")
        if env and (env["status"]!="ACTIVE" or env["mode"]!="OFFLINE_SYNTHETIC" or env["network_accessed"] or env["real_credentials_used"] or env["production_write"]): fail.append("ENVIRONMENT_BOUNDARY_VIOLATION")
        if br:
            if br["status"]=="REVOKED": fail.append("BASELINE_RELEASE_REVOKED")
            elif br["status"]=="UNKNOWN": rr.append("BASELINE_RELEASE_UNKNOWN")
            if br["platform"]!="OPENCLAW" or (br["version"],br["commit"])!=OPENCLAW: fail.append("OPENCLAW_RELEASE_NOT_PINNED")
        if cr:
            if cr["status"]=="REVOKED": fail.append("CANDIDATE_RELEASE_REVOKED")
            elif cr["status"]=="UNKNOWN": rr.append("CANDIDATE_RELEASE_UNKNOWN")
            if cr["platform"]!="HERMES" or (cr["version"],cr["commit"])!=HERMES: fail.append("HERMES_RELEASE_NOT_PINNED")
        authorities=(ta,ia,pa,da,ga)
        if all(authorities):
            for authority_record in authorities:
                if authority_record["status"]!="ACTIVE" or authority_record["case_record_id"]!=s["case_record_id"] or authority_record["case_version"]!=raw["case_version"] or authority_record["task_id"]!=s["task_id"]: fail.append("COMPARISON_AUTHORITY_BINDING_INVALID")
            if env and (pa["environment_mode"]!=env["mode"] or da["allowed_environment_mode"]!=env["mode"]): fail.append("COMPARISON_ENVIRONMENT_NOT_AUTHORIZED")
            if identity and identity["case_type"] not in da["allowed_case_types"]: fail.append("DATASET_CASE_TYPE_NOT_AUTHORIZED")
            if da["rights_status"]=="UNKNOWN": rr.append("DATASET_RIGHTS_UNKNOWN")
            elif da["rights_status"]!="PASS": fail.append("DATASET_RIGHTS_INVALID")
        for b,side in ((bb,"BASELINE"),(cb,"CANDIDATE")):
            if b:
                if abs(round(b["model_usd"]+b["tool_usd"]+b["compute_usd"]+b["human_usd"],6)-b["total_usd"])>1e-6: fail.append(side+"_BUDGET_TOTAL_INVALID")
                if b["status"]=="REVOKED": fail.append(side+"_BUDGET_REVOKED")
                elif b["status"]=="UNKNOWN": rr.append(side+"_BUDGET_UNKNOWN")
                if b["case_record_id"]!=s["case_record_id"] or b["case_version"]!=raw["case_version"] or b["task_id"]!=s["task_id"] or b["run_id"]!=s["run_id"] or b["side"]!=side: fail.append(side+"_BUDGET_SCOPE_BINDING_INVALID")
                refs=("task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref")
                if any(b[k]!=raw[k] for k in refs): fail.append(side+"_BUDGET_AUTHORITY_BINDING_INVALID")
                if ta and (b["task_spec"]!=ta["task_spec"] or b["task_digest"]!=ta["task_digest"]): fail.append(side+"_TASK_NOT_AUTHORIZED")
                if ia and (b["input_spec"]!=ia["input_spec"] or b["input_digest"]!=ia["input_digest"]): fail.append(side+"_INPUT_NOT_AUTHORIZED")
                if pa and (b["permissions"]!=pa["allowed_permissions"] or b["permissions_digest"]!=pa["permissions_digest"]): fail.append(side+"_PERMISSIONS_NOT_AUTHORIZED")
                if da and (b["data_spec"]!=da["data_spec"] or b["data_digest"]!=da["data_digest"]): fail.append(side+"_DATASET_NOT_AUTHORIZED")
                if ga and (b["eval_spec"]!=ga["eval_spec"] or b["eval_digest"]!=ga["eval_digest"]): fail.append(side+"_GRADER_NOT_AUTHORIZED")
        parity=("task_digest","input_digest","risk","permissions_digest","data_digest","eval_digest","model_usd","tool_usd","compute_usd","human_minutes","human_usd","elapsed_seconds","total_usd")
        if bb and cb and any(bb[x]!=cb[x] for x in parity): fail.append("COMPARISON_CONTRACT_UNFAIR")
        active=[a for a in arts if a and a["status"]=="ACTIVE"]
        if not raw["artifact_refs"] or len(active)!=len(raw["artifact_refs"]): rr.append("ARTIFACT_INCOMPLETE")
        if any(a and a["status"]=="REVOKED" for a in arts): fail.append("ARTIFACT_REVOKED")
        for a in active:
            if a["case_record_id"]!=s["case_record_id"] or a["case_version"]!=raw["case_version"] or a["run_id"]!=s["run_id"]: fail.append("ARTIFACT_BINDING_MISMATCH")
            if a["task_id"]!=s["task_id"] or a["evidence_id"]!=s["evidence_id"]: fail.append("ARTIFACT_TASK_EVIDENCE_BINDING_MISMATCH")
            if source and a["source_id"]!=source["source_id"]: fail.append("ARTIFACT_SOURCE_MISMATCH")
            if source and source["origin"]=="VENDOR_PUBLIC_PAGE" and a["kind"]!="PUBLIC_CASE": rr.append("VENDOR_SOURCE_NOT_INDEPENDENT_EVIDENCE")
        if publication and publication["public_artifact_id"] not in raw["artifact_refs"]: fail.append("PUBLIC_ARTIFACT_NOT_REFERENCED")
        if d21:
            if d21["task_id"]!=s["task_id"] or d21["run_id"]!=s["run_id"] or d21["evidence_id"]!=s["evidence_id"]: fail.append("D21_TASK_EVIDENCE_BINDING_MISMATCH")
            vals=(d21["technical"],d21["delivery"],d21["business_environment"])
            if d21["status"]=="UNKNOWN" or "UNKNOWN" in vals: rr.append("D21_UNKNOWN")
            if d21["status"]=="REVOKED" or "FAIL" in vals: fail.append("D21_FAILED")
            d21_spec=((d21["technical_evidence_id"],"TECHNICAL_EVIDENCE","TECHNICAL",d21["technical"]),(d21["delivery_evidence_id"],"DELIVERY_EVIDENCE","DELIVERY",d21["delivery"]),(d21["acceptance_evidence_id"],"ACCEPTANCE_EVIDENCE","ACCEPTANCE",d21["business_environment"]))
            for ref,kind,dimension,declared_state in d21_spec:
                a=idx["artifact_registry"].get(ref)
                if not a or a["kind"]!=kind or a["status"]!="ACTIVE" or ref not in raw["artifact_refs"]: fail.append("D21_EVIDENCE_INVALID"); continue
                expected_keys={"dimension","state","case_record_id","task_id","run_id","evidence_id"}
                if set(a["payload"])!=expected_keys or a["payload"].get("dimension")!=dimension or a["payload"].get("state") not in {"PASS","FAIL","UNKNOWN"} or any(a["payload"].get(k)!=s[k] for k in ("case_record_id","task_id","run_id","evidence_id")): fail.append("D21_EVIDENCE_SCHEMA_INVALID")
                elif declared_state!=a["payload"]["state"]: fail.append("D21_STATE_CONTENT_MISMATCH")
        if migration:
            if migration["status"]=="UNKNOWN" or migration["unsupported_capabilities"]: rr.append("MIGRATION_UNSUPPORTED_OR_UNKNOWN")
            elif migration["status"]!="ACTIVE": fail.append("MIGRATION_INACTIVE")
            if br and migration["baseline_release_id"]!=br["release_id"] or cr and migration["candidate_release_id"]!=cr["release_id"]: fail.append("MIGRATION_RELEASE_BINDING_MISMATCH")
            if migration["task_id"]!=s["task_id"] or migration["run_id"]!=s["run_id"] or migration["evidence_id"]!=s["evidence_id"]: fail.append("MIGRATION_TASK_EVIDENCE_BINDING_MISMATCH")
            bc=migration["baseline_contract"]; cc=migration["candidate_contract"]
            if any(bc[k]!=cc[k] for k in ("task_digest","input_digest","risk","permissions_digest","data_digest","eval_digest")): fail.append("MIGRATION_CONTRACT_UNFAIR")
            if bb and bc["budget_id"]!=bb["budget_id"] or cb and cc["budget_id"]!=cb["budget_id"]: fail.append("MIGRATION_BUDGET_BINDING_MISMATCH")
            contract_fields=("case_record_id","case_version","task_id","run_id","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","task_digest","input_digest","risk","permissions_digest","data_digest","eval_digest")
            if bb and any(bc[k]!=bb[k] for k in contract_fields): fail.append("MIGRATION_BASELINE_CONTRACT_NOT_BOUND_TO_BUDGET")
            if cb and any(cc[k]!=cb[k] for k in contract_fields): fail.append("MIGRATION_CANDIDATE_CONTRACT_NOT_BOUND_TO_BUDGET")
            if bb and bc["budget_contract_digest"]!=bb["contract_digest"]: fail.append("MIGRATION_BASELINE_CONTRACT_DIGEST_MISMATCH")
            if cb and cc["budget_contract_digest"]!=cb["contract_digest"]: fail.append("MIGRATION_CANDIDATE_CONTRACT_DIGEST_MISMATCH")
            adapter_matrix={
                "PERMISSION":("PERMISSIONS","CRITICAL","FAIL"),"AUTHORIZATION":("AUTHORITY","CRITICAL","FAIL"),
                "DATA":("DATA","CRITICAL","FAIL"),"EVALUATION":("GRADER","CRITICAL","FAIL"),
                "TERMINAL_STATE":("D21_TERMINAL","CRITICAL","FAIL"),"SECURITY":("SECURITY_BOUNDARY","CRITICAL","FAIL"),
                "STATE_CARRIER":("STATE_TRANSPORT","NON_CRITICAL",None),"TOOL_SCHEMA":("TOOL_INTERFACE","NON_CRITICAL",None),
                "MESSAGE_SEMANTICS":("MESSAGE_PROTOCOL","NON_CRITICAL",None),
            }
            for difference in migration["adapter_differences"]:
                owner=normalize_principal(difference["owner"]); evidence=idx["artifact_registry"].get(difference["evidence_ref"])
                evidence_valid=bool(evidence and evidence["kind"]=="TECHNICAL_EVIDENCE" and evidence["status"]=="ACTIVE" and source and source["origin"]!="VENDOR_PUBLIC_PAGE" and evidence["source_id"]==source["source_id"] and difference["evidence_ref"] in raw["artifact_refs"] and evidence["case_record_id"]==s["case_record_id"] and evidence["case_version"]==raw["case_version"] and evidence["task_id"]==s["task_id"] and evidence["run_id"]==s["run_id"] and evidence["evidence_id"]==s["evidence_id"] and evidence["payload"].get("dimension")=="TECHNICAL")
                if not owner or not auth or owner!=normalize_principal(auth["principal_id"]) or not evidence_valid: fail.append("MIGRATION_ADAPTER_EVIDENCE_OR_OWNER_INVALID")
                contract,criticality,forced=adapter_matrix[difference["category"]]
                if difference["affected_contract"]!=contract or difference["criticality"]!=criticality or (forced and difference["disposition"]!=forced): fail.append("MIGRATION_ADAPTER_CLASSIFICATION_INVALID")
                if not forced and difference["disposition"] not in {"ACCEPTED","REVIEW_REQUIRED"}: fail.append("MIGRATION_ADAPTER_CLASSIFICATION_INVALID")
                if difference["criticality"]=="CRITICAL" or difference["disposition"]=="FAIL": fail.append("MIGRATION_ADAPTER_DIFFERENCE_CRITICAL")
                elif difference["disposition"]=="REVIEW_REQUIRED": rr.append("MIGRATION_ADAPTER_DIFFERENCE_REVIEW")
        actual_trials=[t for t in run_trials if t]
        actual_failures=[f for f in failures if f]
        # Reconstruct one causal clock: authorization -> assignment -> trial and
        # evidence -> independent review -> publication -> evaluation.
        evidence_times=[dt(x["recorded_at"]) for x in actual_trials+actual_failures+[x for x in arts+effects+[d21] if x]]
        if auth and assignment and reviewer and publication and evidence_times:
            start=max(dt(auth["valid_from"]),dt(assignment["valid_from"]))
            end=min(dt(auth["valid_until"]),dt(assignment["valid_until"]))
            reviewed=dt(reviewer["reviewed_at"]); released=dt(publication["released_at"])
            if any(t<start or t>end for t in evidence_times): fail.append("EVIDENCE_OUTSIDE_AUTHORIZATION_ASSIGNMENT_WINDOW")
            if any(t>at for t in evidence_times): fail.append("EVIDENCE_AFTER_EVALUATION")
            if max(evidence_times)>reviewed: fail.append("REVIEW_PRECEDES_EVIDENCE")
            if not (reviewed<=released<=at): fail.append("CAUSAL_PUBLICATION_TIMELINE_INVALID")
        if d21:
            d21_time=dt(d21["recorded_at"])
            d21_support=[idx["artifact_registry"].get(x) for x in (d21["technical_evidence_id"],d21["delivery_evidence_id"],d21["acceptance_evidence_id"])]
            if any(not x or dt(x["recorded_at"])>d21_time for x in d21_support): fail.append("D21_PRECEDES_SUPPORTING_EVIDENCE")
            if any(dt(x["recorded_at"])>d21_time for x in actual_trials+actual_failures+effects if x): fail.append("D21_PRECEDES_TRIAL_FAILURE_OR_EFFECT")
        trial_by_id={x["trial_id"]:x for x in actual_trials}
        for failure in actual_failures:
            trial_record=trial_by_id.get(failure["trial_id"]); failure_log=idx["artifact_registry"].get(failure["artifact_id"])
            if not trial_record or dt(failure["recorded_at"])<dt(trial_record["recorded_at"]): fail.append("FAILURE_PRECEDES_TRIAL")
            if not failure_log or dt(failure_log["recorded_at"])<dt(failure["recorded_at"]): fail.append("FAILURE_LOG_PRECEDES_FAILURE")
            if d21 and failure_log and dt(failure_log["recorded_at"])>dt(d21["recorded_at"]): fail.append("D21_PRECEDES_FAILURE_LOG")
            if reviewer and failure_log and dt(failure_log["recorded_at"])>dt(reviewer["reviewed_at"]): fail.append("REVIEW_PRECEDES_FAILURE_LOG")
            if publication and failure_log and dt(failure_log["recorded_at"])>dt(publication["released_at"]): fail.append("PUBLICATION_PRECEDES_FAILURE_LOG")
        if any(t["status"]=="UNKNOWN" for t in actual_trials): rr.append("TRIAL_OUTCOME_UNKNOWN")
        if any(f["status"]=="REVOKED" for f in actual_failures): fail.append("FAILURE_RECORD_REVOKED")
        elif any(f["status"]=="UNKNOWN" for f in actual_failures): rr.append("FAILURE_RECORD_UNKNOWN")
        if any(t["case_record_id"]!=s["case_record_id"] or t["task_id"]!=s["task_id"] or t["run_id"]!=s["run_id"] or t["evidence_id"]!=s["evidence_id"] for t in actual_trials): fail.append("TRIAL_TASK_EVIDENCE_BINDING_MISMATCH")
        if s["trial_id"] not in {t["trial_id"] for t in actual_trials}: fail.append("SCENARIO_TRIAL_NOT_BOUND")
        if any(f["case_record_id"]!=s["case_record_id"] or f["task_id"]!=s["task_id"] or f["run_id"]!=s["run_id"] or f["evidence_id"]!=s["evidence_id"] for f in actual_failures): fail.append("FAILURE_TASK_EVIDENCE_BINDING_MISMATCH")
        derived_failure_count=sum(t["status"]=="FAIL" for t in actual_trials)
        fail_trials=[t for t in actual_trials if t["status"]=="FAIL"]
        active_failures=[f for f in actual_failures if f["status"]=="ACTIVE"]
        active_failure_by_id={f["failure_id"]:f for f in active_failures}
        failure_log_ids=[a["artifact_id"] for a in arts if a and a["kind"]=="FAILURE_LOG"]
        preserved=(len(fail_trials)==len(active_failures)
            and all(t["failure_ref"]=="NONE" for t in actual_trials if t["status"]!="FAIL")
            and all(t["failure_ref"] in active_failure_by_id and active_failure_by_id[t["failure_ref"]]["trial_id"]==t["trial_id"] for t in fail_trials)
            and len({f["trial_id"] for f in active_failures})==len(active_failures)
            and len({f["artifact_id"] for f in active_failures})==len(active_failures)
            and set(failure_log_ids)=={f["artifact_id"] for f in active_failures}
            and all((lambda a: bool(a and a["kind"]=="FAILURE_LOG" and a["payload"]=={"failure_id":f["failure_id"],"trial_id":f["trial_id"],"outcome":"FAIL"}))(idx["artifact_registry"].get(f["artifact_id"])) for f in active_failures))
        required_kinds={"PUBLIC_CASE","TECHNICAL_EVIDENCE","DELIVERY_EVIDENCE","ACCEPTANCE_EVIDENCE"}|({"FAILURE_LOG"} if derived_failure_count else set())
        projected_kinds={a["kind"] for a in active}
        if projected_kinds!=required_kinds: fail.append("ARTIFACT_PROJECTION_INVALID")
        if raw["trial_count"]!=len(actual_trials) or raw["failure_count"]!=derived_failure_count or raw["failures_preserved"]!=preserved or len(actual_trials)<2 or not preserved: fail.append("RUN_DISTRIBUTION_INVALID")
        if raw["holdout_accessed"] or raw["grader_private_access"]: fail.append("EVALUATION_CONTAMINATED")
        if not effects: fail.append("EFFECT_PROJECTION_EMPTY")
        external=sum(1 for e in effects if e and e["effect_kind"]=="EXTERNAL_WRITE")
        if external: fail.append("OFFLINE_EXTERNAL_EFFECT")
        for e in effects:
            if not e: continue
            if e["case_record_id"]!=s["case_record_id"] or e["task_id"]!=s["task_id"] or e["run_id"]!=s["run_id"] or e["evidence_id"]!=s["evidence_id"]: fail.append("EFFECT_BINDING_MISMATCH")
            if e["status"]=="REVOKED": fail.append("EFFECT_REVOKED")
            elif e["status"]=="UNKNOWN": rr.append("EFFECT_UNKNOWN")
            if not e["authorized"]: fail.append("EFFECT_UNAUTHORIZED")
            derived_external=e["effect_kind"]=="EXTERNAL_WRITE"
            if e["external"] is not derived_external: fail.append("EFFECT_EXTERNAL_DERIVATION_MISMATCH")
            receipt=e["receipt"]; readback=e["readback"]
            expected={"effect_id":e["effect_id"],"effect_kind":e["effect_kind"],"external":e["external"],"authorized":e["authorized"],"status":"NONE" if e["effect_kind"]=="NONE" else "APPLIED"}
            if receipt!=expected or readback!=expected: fail.append("EFFECT_RECEIPT_READBACK_MISMATCH")
        verdict="FAIL" if fail else "REVIEW_REQUIRED" if rr else "PASS"
        accepted_real=int(bool(identity and identity["case_type"] in {"VERIFIED-REAL","ANONYMIZED-REAL"} and identity["status"]=="ACTIVE" and not fail))
        trials.append({k:s[k] for k in ("scenario_id","case_record_id","task_id","trial_id","run_id","evidence_id")}|{"derived":{"verdict":verdict,"reasons":sorted(set(fail+rr)),"external_effect_count":external,"accepted_real_claim_count":accepted_real}})
    distribution=dict(sorted(Counter(t["derived"]["verdict"] for t in trials).items()))
    manifest=authority_root["suite_manifest"]
    provenance={"suite_id":manifest["suite_id"],"build_id":manifest["build_id"],"evaluation_time":manifest["evaluation_time"],"input_schema_version":manifest["input_schema_version"],"result_schema_version":manifest["result_schema_version"],"scenario_manifest_digest":manifest["scenario_manifest_digest"],"authority_root_digest":authority_root["root_digest"]}
    result={"schema_version":RESULT_SCHEMA,"input_schema_version":SCHEMA,"provenance":provenance,"authority_root_digest":authority_root["root_digest"],"trial_count":len(trials),"distribution":distribution,"accepted_real_claim_count":sum(t["derived"]["accepted_real_claim_count"] for t in trials),"external_effect_count":sum(t["derived"]["external_effect_count"] for t in trials),"trials":trials}
    result["decision_digest"]=digest(result)
    return result

def evaluate(src,authority_root):
    """Author-side result generation only; this is not an acceptance API.

    Fixture builders and historical semantic tests work with already parsed
    objects.  Trust is established only by verify_raw_documents/CLI below.
    """
    if not isinstance(authority_root,dict) or "root_digest" not in authority_root:
        raise TypeError("author evaluation requires a parsed authority root")
    return _evaluate_with_pin(src,authority_root,authority_root["root_digest"])

def _freeze_trusted_semantics():
    """Clone the evaluator's whole module-function graph into private globals.

    Ordinary rebinding of public module names cannot affect functions whose
    global lookups resolve against this private dictionary.  Direct closure
    cell or private-dictionary mutation remains arbitrary same-process code
    execution and is deliberately outside this control's claim.
    """
    source_globals=globals(); private={}
    for name,value in tuple(source_globals.items()):
        if not isinstance(value,types.FunctionType): private[name]=value
    captured_dumps=json.dumps; captured_sha256=hashlib.sha256
    def frozen_canonical(value):
        return captured_dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    def frozen_digest(value):
        return captured_sha256(frozen_canonical(value).encode()).hexdigest()
    private["canonical"]=frozen_canonical; private["digest"]=frozen_digest
    for name,value in tuple(source_globals.items()):
        if not isinstance(value,types.FunctionType) or name in {"canonical","digest","_freeze_trusted_semantics"}: continue
        if value.__closure__:
            private[name]=value
        else:
            private[name]=types.FunctionType(value.__code__,private,name,value.__defaults__,None)
            private[name].__kwdefaults__=value.__kwdefaults__
    return private["_evaluate_with_pin"],frozen_canonical

def _read_pin_registry():
    path=Path(__file__).resolve().with_name("frozen-pin-registry.json")
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PIN_REGISTRY_SHA256:
        raise ValueError("pin registry: release-pinned file digest mismatch")
    registry=strict_json_loads(raw)
    exact(registry,["schema_version","registry_id","issuer_principal_id","pins"],"pin_registry")
    if registry["schema_version"]!="c23.pin-authority-registry.v1": raise ValueError("pin registry: unsupported schema")
    ident(registry["registry_id"],"pin_registry.registry_id"); ident(registry["issuer_principal_id"],"pin_registry.issuer_principal_id")
    if not isinstance(registry["pins"],list) or not registry["pins"]: raise ValueError("pin registry: pins required")
    rows=[]; seen=set()
    for i,row in enumerate(registry["pins"]):
        q=f"pin_registry.pins[{i}]"; exact(row,["pin_id","authority_root_digest","issued_at","status","scope"],q)
        ident(row["pin_id"],q+".pin_id"); sha(row["authority_root_digest"],q+".authority_root_digest"); timestamp(row["issued_at"],q+".issued_at")
        if row["status"]!="ACTIVE" or row["scope"]!="OFFLINE_SYNTHETIC": raise ValueError(q+": inactive or out-of-scope pin")
        if row["pin_id"] in seen: raise ValueError("pin registry: duplicate pin id")
        seen.add(row["pin_id"]); rows.append((row["pin_id"],row["authority_root_digest"]))
    return tuple(rows)

def _make_raw_verifier(parse_fn,evaluator_fn,canonical_fn,pin_rows,path_type):
    captured_pins=tuple(pin_rows)
    def read_document(document,label):
        if isinstance(document,path_type): raw=document.read_bytes()
        elif type(document) in (str,bytes): raw=document
        else: raise TypeError(label+": raw JSON bytes, text, or pathlib.Path required; parsed objects are forbidden")
        return parse_fn(raw)
    def verify(result_document,authority_root_document,source_document,*,pin_id="PIN.C23.CURRENT"):
        if type(pin_id) is not str or not pin_id or pin_id=="PENDING": raise ValueError("pin: concrete authorized pin_id required")
        matches=[root_digest for candidate,root_digest in captured_pins if candidate==pin_id]
        if len(matches)!=1: raise ValueError("pin: id is not present in the release-pinned authority registry")
        result=read_document(result_document,"result")
        authority_root=read_document(authority_root_document,"authority_root")
        source=read_document(source_document,"source")
        expected=evaluator_fn(source,authority_root,matches[0])
        if canonical_fn(result)!=canonical_fn(expected): raise ValueError("result: source semantic replay mismatch")
        return True
    return verify

# The verifier closes over the original parser, evaluator and immutable pin
# rows at import time.  Rebinding module globals later cannot alter this core.
_CAPTURED_PIN_ROWS=_read_pin_registry()
_FROZEN_EVALUATOR,_FROZEN_CANONICAL=_freeze_trusted_semantics()
verify_raw_documents=_make_raw_verifier(strict_json_loads,_FROZEN_EVALUATOR,_FROZEN_CANONICAL,_CAPTURED_PIN_ROWS,Path)
del _CAPTURED_PIN_ROWS, _FROZEN_EVALUATOR, _FROZEN_CANONICAL, _make_raw_verifier, _freeze_trusted_semantics

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--authority-root",required=True); p.add_argument("--output",required=True); a=p.parse_args(); result=evaluate(strict_json_loads(Path(a.input).read_bytes()),strict_json_loads(Path(a.authority_root).read_bytes())); Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); print(result["decision_digest"])
if __name__=="__main__": main()
