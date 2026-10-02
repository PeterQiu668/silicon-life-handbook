#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C24 v2.6 pinned-root, causal-DAG continuous-certification controller."""
from __future__ import annotations
import argparse,hashlib,json,math,re,unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

MAT=[f"MAT-L{i}" for i in range(6)]; AU=[f"AU-L{i}" for i in range(5)]
VERDICTS={"PASS","FAIL","REVIEW_REQUIRED"}; LIFE={"ACTIVE","LIMITED","SUSPENDED","REVOKED","EXPIRED"}
LAYERS={"training","regression","holdout","representative_real_world"}; DIMS={"quality","generalization","safety","stability","efficiency","collaboration","governability"}
DIGEST=re.compile(r"^sha256:[0-9a-f]{64}$")
PINNED_AUTHORITY_ROOT_DIGEST="sha256:1c768968e30d39195369e517394c3c218829b175d64d219a6e5ff159062fb6ad"

# Reject duplicate JSON keys before canonicalization.  Importing this module
# also hardens preserved reviewer programs which call ``json.loads`` after
# loading the runner; the original parser is retained only inside this
# wrapper, so nested duplicates cannot be normalized away first.
_ORIGINAL_JSON_LOADS=json.loads
def _unique_pairs(pairs):
    out={}
    for key,value in pairs:
        if key in out: raise ValueError("json duplicate key: "+key)
        out[key]=value
    return out
def strict_json_loads(text,*args,**kwargs):
    if "object_pairs_hook" in kwargs: raise ValueError("custom object_pairs_hook forbidden")
    kwargs["object_pairs_hook"]=_unique_pairs
    return _ORIGINAL_JSON_LOADS(text,*args,**kwargs)
json.loads=strict_json_loads

def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def sha(x): return "sha256:"+hashlib.sha256(canon(x).encode()).hexdigest()
def raw_sha(x): return "sha256:"+hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=True).encode()).hexdigest()
def record_ok(x,field="record_digest"): return type(x.get(field)) is str and DIGEST.fullmatch(x[field]) is not None and x[field]==sha({k:v for k,v in x.items() if k!=field})
def exact(x,fields,path):
    if type(x) is not dict or set(x)!=set(fields): raise ValueError(f"{path} closed-world schema violation")
    return x
def typed(x,t,path):
    if type(x) is not t: raise ValueError(f"{path} type")
def string(x,path):
    typed(x,str,path)
    if not x: raise ValueError(f"{path} empty")
    return x
def strings(x,path):
    typed(x,list,path)
    if any(type(v) is not str or not v for v in x): raise ValueError(f"{path} strings")
    return x
def finite(x,path,minimum=0):
    if type(x) not in {int,float} or not math.isfinite(x) or x<minimum: raise ValueError(f"{path} finite range")
    return x
def stamp(x,path):
    string(x,path)
    try: d=datetime.fromisoformat(x.replace('Z','+00:00'))
    except ValueError as e: raise ValueError(f"{path} ISO-8601") from e
    if d.tzinfo is None: raise ValueError(f"{path} timezone")
    return d
def identity_key(x,path='identity'):
    string(x,path)
    normalized=unicodedata.normalize('NFKC',x)
    if normalized!=x or x.strip()!=x or not re.fullmatch(r'[A-Za-z0-9._:@/\-]+',x):
        raise ValueError(f'{path} non-canonical identity')
    return x.casefold()
def reg(x,fields,idf,path):
    typed(x,dict,path); ids=[]
    for key,row in x.items():
        exact(row,fields,f"{path}.{key}"); string(row[idf],f"{path}.{key}.{idf}")
        if row[idf]!=key: raise ValueError(f"{path}.{key} key binding")
        ids.append(key)
    if len(ids)!=len(set(ids)): raise ValueError(f"{path} duplicate")
    return x
def signature_payload(a): return {k:a[k] for k in ('subject_id','scope','release','task_id','platform','model','tools','data','budget','risk','environment','expires_at','exclusions')}
def change_payload(a,ch): return {'change_id':ch['change_id'],'application_id':ch['application_id'],'release':a['release'],'material':ch['material'],'kind':ch['kind'],'impact_review':ch['impact_review'],'retest':ch['retest'],'owner':ch['owner'],'issued_at':ch['issued_at'],'affected_scopes':ch['affected_scopes'],'post_change_release':ch['post_change_release'],'retest_trial_refs':ch['retest_trial_refs'],'retest_evidence_refs':ch['retest_evidence_refs'],'retest_review_ref':ch['retest_review_ref'],'retest_manifest':ch['retest_manifest']}
def lifecycle_payload(life): return {k:life[k] for k in ('event_id','certificate_id','previous','current','kind','occurred_at')}
def source_identity_payload(src):
    """Authority-independent input identity; avoids an authority_ref digest cycle."""
    return {k:src[k] for k in ('schema','now','environment','scenarios')}

def authority_projection(row):
    return {k:row[k] for k in ('authority_id','actor','action','subject_type','subject_id','object_digest','scope','status','issued_at','not_before','expires_at','record_digest')}

def principal_projection(row):
    return {k:row[k] for k in ('principal_id','kind','status','roles','aliases','valid_from','expires_at','record_digest')}

def event_projection(row):
    return {k:row[k] for k in ('event_id','application_id','kind','subject_ref','occurred_at','sequence','predecessor_refs','record_digest')}

def validate_authority(root):
    exact(root,{'schema','bundle_id','issuer','semantic_issuer','measurement_issuer','evaluation_time','input_semantic_digest','scenario_registry','semantic_registry','measurement_registry','authority_registry','principal_registry','event_registry','release_registry','d22_policy','revoked_certificate_ids','revoked_authority_ids','root_digest'},'authority')
    if root['schema']!='c24.cert.authority.v2.6': raise ValueError('authority schema')
    for f in ('bundle_id','issuer','semantic_issuer','measurement_issuer','input_semantic_digest','root_digest'): string(root[f],'authority.'+f)
    if not DIGEST.fullmatch(root['input_semantic_digest']): raise ValueError('authority input semantic digest')
    stamp(root['evaluation_time'],'authority.evaluation_time'); strings(root['revoked_certificate_ids'],'authority.revoked_certificate_ids'); strings(root['revoked_authority_ids'],'authority.revoked_authority_ids')
    typed(root['scenario_registry'],dict,'authority.scenario_registry')
    for key,row in root['scenario_registry'].items():
        string(key,'authority.scenario_id'); exact(row,{'metadata_digest','state_digest','status'},'authority.scenario_registry.'+key); [string(row[f],'authority.scenario.'+f) for f in row]
        if not DIGEST.fullmatch(row['metadata_digest']) or not DIGEST.fullmatch(row['state_digest']) or row['status'] not in {'ACTIVE','REVOKED'}: raise ValueError('authority scenario record')
    typed(root['semantic_registry'],dict,'authority.semantic_registry'); typed(root['measurement_registry'],dict,'authority.measurement_registry')
    if set(root['semantic_registry'])!=set(root['scenario_registry']) or set(root['measurement_registry'])!=set(root['scenario_registry']): raise ValueError('authority independent registry projection')
    for key,row in root['semantic_registry'].items():
        exact(row,{'scenario_id','decision','lifecycle','reasons','state_digest','semantic_digest'},'authority.semantic_registry.'+key)
        if row['scenario_id']!=key or row['decision'] not in VERDICTS or row['lifecycle'] not in LIFE: raise ValueError('authority semantic record')
        strings(row['reasons'],'authority.semantic.reasons')
        if row['reasons']!=sorted(set(row['reasons'])) or not DIGEST.fullmatch(row['state_digest']) or row['semantic_digest']!=sha({k:v for k,v in row.items() if k!='semantic_digest'}): raise ValueError('authority semantic digest')
    metric_fields={'scenario_id','representative_real_world_attempts','real_certificate_attempts','external_effect_attempts','observed_external_effects','successful_real_certificates','successful_external_effects','record_digest'}
    for key,row in root['measurement_registry'].items():
        exact(row,metric_fields,'authority.measurement_registry.'+key)
        if row['scenario_id']!=key: raise ValueError('authority measurement scenario binding')
        for f in metric_fields-{'scenario_id','record_digest'}: finite(row[f],'authority.measurement.'+f)
        if row['record_digest']!=sha({k:v for k,v in row.items() if k!='record_digest'}): raise ValueError('authority measurement digest')
    typed(root['authority_registry'],dict,'authority.authority_registry')
    for key,row in root['authority_registry'].items():
        exact(row,{'authority_id','scenario_id','epoch','projection','projection_digest','root_record_digest'},'authority.authority_registry.'+key)
        if row['authority_id']!=key: raise ValueError('authority registry key binding')
        string(row['scenario_id'],'authority registry scenario'); finite(row['epoch'],'authority registry epoch',1)
        typed(row['projection'],dict,'authority registry projection')
        if row['projection'].get('authority_id')!=key or row['projection_digest']!=sha(row['projection']): raise ValueError('authority projection binding')
        if row['root_record_digest']!=sha({k:v for k,v in row.items() if k!='root_record_digest'}): raise ValueError('authority root record digest')
        if row['projection'].get('status') not in {'ACTIVE','REVOKED','EXPIRED'}: raise ValueError('authority root status')
    typed(root['principal_registry'],dict,'authority.principal_registry')
    typed(root['event_registry'],dict,'authority.event_registry')
    for app_id,records in root['principal_registry'].items():
        identity_key(app_id,'authority.principal_registry application'); typed(records,dict,'authority.principal records')
        aliases={}
        for principal_id,row in records.items():
            identity_key(principal_id,'authority principal id')
            exact(row,{'application_id','principal_id','epoch','projection','projection_digest','root_record_digest'},'authority principal record')
            if row['application_id']!=app_id or row['principal_id']!=principal_id: raise ValueError('authority principal key binding')
            finite(row['epoch'],'authority principal epoch',1); typed(row['projection'],dict,'authority principal projection')
            if row['projection']!=principal_projection(row['projection']) or row['projection']['principal_id']!=principal_id: raise ValueError('authority principal projection schema')
            if row['projection_digest']!=sha(row['projection']) or row['root_record_digest']!=sha({k:v for k,v in row.items() if k!='root_record_digest'}): raise ValueError('authority principal digest')
            if row['projection']['status'] not in {'ACTIVE','INACTIVE','REVOKED'}: raise ValueError('authority principal status')
            for name in [principal_id,*row['projection']['aliases']]:
                key=identity_key(name,'authority principal alias')
                # Invalid frozen scenarios may intentionally contain a collision;
                # the root preserves it and runtime canonicalization rejects it.
                aliases.setdefault(key,principal_id)
    event_kinds={'AUTHORITY_READY','APPLICATION_SIGNED','MANIFEST_PREREGISTERED','HOLDOUT_FROZEN','GRADER_PREREGISTERED','NAMESPACE_FROZEN','TRIAL_INPUT_ACCEPTED','TRIAL_COMPLETED','TRIAL_OUTPUT_RECORDED','ARTIFACT_RECORDED','FAILURE_ARCHIVED','COST_RECORDED','D21_TECHNICAL_RECORDED','D21_DELIVERY_RECORDED','ENVIRONMENT_OUTCOME_RECORDED','D21_BUSINESS_RECORDED','DIMENSION_RECORDED','MANIFEST_SEALED','MATURITY_RECORDED','CHANGE_RECORDED','CHANGE_EVIDENCE_RECORDED','REVIEW_RECORDED','APPEAL_RECORDED','CERTIFICATE_ISSUED','PUBLIC_CLAIM_RECORDED','LIFECYCLE_OCCURRED','LIFECYCLE_EVIDENCE_RECORDED'}
    for app_id,records in root['event_registry'].items():
        identity_key(app_id,'authority.event_registry application'); typed(records,dict,'authority event records')
        sequences=[]
        for event_id,row in records.items():
            identity_key(event_id,'authority event id')
            exact(row,{'application_id','event_id','epoch','projection','projection_digest','root_record_digest'},'authority event record')
            if row['application_id']!=app_id or row['event_id']!=event_id: raise ValueError('authority event key binding')
            finite(row['epoch'],'authority event epoch',1); typed(row['projection'],dict,'authority event projection')
            if row['projection']!=event_projection(row['projection']) or row['projection']['event_id']!=event_id or row['projection']['application_id']!=app_id: raise ValueError('authority event projection schema')
            if row['projection']['kind'] not in event_kinds: raise ValueError('authority event kind')
            stamp(row['projection']['occurred_at'],'authority event time'); finite(row['projection']['sequence'],'authority event sequence',1); strings(row['projection']['predecessor_refs'],'authority event predecessors')
            if len(row['projection']['predecessor_refs'])!=len(set(row['projection']['predecessor_refs'])): raise ValueError('authority event predecessor duplicate')
            if row['projection_digest']!=sha(row['projection']) or row['root_record_digest']!=sha({k:v for k,v in row.items() if k!='root_record_digest'}): raise ValueError('authority event digest')
            sequences.append(row['projection']['sequence'])
        if len(sequences)!=len(set(sequences)): raise ValueError('authority event sequence duplicate')
    typed(root['release_registry'],dict,'authority.release_registry')
    for key,row in root['release_registry'].items():
        exact(row,{'scenario_id','application_id','subject_id','scope','change_id','pre_change_release','post_change_release','status','epoch','record_digest'},'authority.release_registry.'+key)
        if row['scenario_id']!=key or row['status']!='ACTIVE': raise ValueError('authority release registry binding')
        for f in ('application_id','subject_id','scope','change_id','pre_change_release','post_change_release'): string(row[f],'authority release '+f)
        finite(row['epoch'],'authority release epoch',1)
        if not record_ok(row): raise ValueError('authority release digest')
    exact(root['d22_policy'],{'policy_id','required_layers','not_applicable_layers','required_security_slices','status','epoch','record_digest'},'authority.d22_policy')
    if root['d22_policy']['policy_id']!='C24-D22-RECERT-v2.6' or root['d22_policy']['status']!='ACTIVE': raise ValueError('authority d22 policy')
    for f in ('required_layers','not_applicable_layers','required_security_slices'): strings(root['d22_policy'][f],'authority d22 '+f)
    finite(root['d22_policy']['epoch'],'authority d22 epoch',1)
    if set(root['d22_policy']['required_layers'])!={'training','regression','holdout'} or set(root['d22_policy']['not_applicable_layers'])!={'representative_real_world'} or not root['d22_policy']['required_security_slices'] or not record_ok(root['d22_policy']): raise ValueError('authority d22 policy binding')
    payload={k:v for k,v in root.items() if k!='root_digest'}
    if sha(payload)!=root['root_digest'] or root['root_digest']!=PINNED_AUTHORITY_ROOT_DIGEST: raise ValueError('authority root is not pinned')
    return root

def validate_state(s,path):
    s=exact(s,{"application","principal_registry","authority_registry","event_registry","role_conflict_exceptions","review_registry","appeal_registry","evidence_registry","trial_registry","evidence_bundle","maturity","organization_registry","namespace","certificate_registry","certificate_ref","lifecycle","change","effect_ledger"},path)
    a=exact(s['application'],{"application_id","subject_id","subject_kind","controller","author","scope","release","task_id","platform","model","tools","data","budget","risk","environment","expires_at","exclusions","requested_mat","requested_au","requested_decision","namespace_id","certificate_id","manifest_ref","change_id","appeal_id","application_digest"},path+'.application')
    for k in set(a)-{"tools","budget","exclusions"}: string(a[k],path+'.application.'+k)
    strings(a['tools'],path+'.application.tools'); strings(a['exclusions'],path+'.application.exclusions'); finite(a['budget'],path+'.application.budget',0.000001); stamp(a['expires_at'],path+'.application.expires_at')
    if a['subject_kind'] not in {"individual_agent","multi_agent_organization"} or a['risk'] not in {"R0","R1","R2","R3","R4"} or a['requested_mat'] not in MAT or a['requested_au'] not in AU or a['requested_decision'] not in VERDICTS: raise ValueError(path+'.application enum')
    ps=reg(s['principal_registry'],{"principal_id","kind","status","roles","aliases","valid_from","expires_at","record_digest"},'principal_id',path+'.principal_registry'); aliases=[]
    for k,x in ps.items():
        for f in ('kind','status','valid_from','expires_at','record_digest'): string(x[f],f'{path}.principal_registry.{k}.{f}')
        strings(x['roles'],f'{path}.principal_registry.{k}.roles'); strings(x['aliases'],f'{path}.principal_registry.{k}.aliases'); stamp(x['valid_from'],'p.from'); stamp(x['expires_at'],'p.exp')
        if x['kind'] not in {'human','legal_entity','agent'} or x['status'] not in {'ACTIVE','INACTIVE','REVOKED'}: raise ValueError('principal enum')
        aliases += [identity_key(k,'principal id')]+[identity_key(v,'principal alias') for v in x['aliases']]
    if len(aliases)!=len(set(aliases)): raise ValueError('principal alias collision')
    auth=reg(s['authority_registry'],{"authority_id","actor","action","subject_type","subject_id","object_digest","scope","status","issued_at","not_before","expires_at","record_digest"},'authority_id',path+'.authority_registry')
    for k,x in auth.items():
        for f in x: string(x[f],f'{path}.authority_registry.{k}.{f}')
        if x['action'] not in {'issue_synthetic_assessment','operate_synthetic_scope','decide_appeal','change_certificate_lifecycle','approve_material_change','approve_role_conflict_exception'} or x['subject_type'] not in {'application','appeal','certificate','change','exception'} or x['status'] not in {'ACTIVE','REVOKED','EXPIRED'}: raise ValueError('authority enum')
        for f in ('issued_at','not_before','expires_at'): stamp(x[f],'authority.'+f)
        identity_key(x['actor'],'authority.actor')
    events=reg(s['event_registry'],{'event_id','application_id','kind','subject_ref','occurred_at','sequence','predecessor_refs','record_digest'},'event_id',path+'.event_registry')
    event_kinds={'AUTHORITY_READY','APPLICATION_SIGNED','MANIFEST_PREREGISTERED','HOLDOUT_FROZEN','GRADER_PREREGISTERED','NAMESPACE_FROZEN','TRIAL_INPUT_ACCEPTED','TRIAL_COMPLETED','TRIAL_OUTPUT_RECORDED','ARTIFACT_RECORDED','FAILURE_ARCHIVED','COST_RECORDED','D21_TECHNICAL_RECORDED','D21_DELIVERY_RECORDED','ENVIRONMENT_OUTCOME_RECORDED','D21_BUSINESS_RECORDED','DIMENSION_RECORDED','MANIFEST_SEALED','MATURITY_RECORDED','CHANGE_RECORDED','CHANGE_EVIDENCE_RECORDED','REVIEW_RECORDED','APPEAL_RECORDED','CERTIFICATE_ISSUED','PUBLIC_CLAIM_RECORDED','LIFECYCLE_OCCURRED','LIFECYCLE_EVIDENCE_RECORDED'}
    sequences=[]
    for k,x in events.items():
        for f in ('application_id','kind','subject_ref','occurred_at','record_digest'): string(x[f],f'{path}.event_registry.{k}.{f}')
        finite(x['sequence'],f'{path}.event_registry.{k}.sequence',1); strings(x['predecessor_refs'],f'{path}.event_registry.{k}.predecessor_refs'); stamp(x['occurred_at'],'event.occurred')
        if x['kind'] not in event_kinds or len(x['predecessor_refs'])!=len(set(x['predecessor_refs'])) or not record_ok(x): raise ValueError('event registry invalid')
        sequences.append(x['sequence'])
    if len(sequences)!=len(set(sequences)): raise ValueError('event sequence duplicate')
    typed(s['role_conflict_exceptions'],list,path+'.role_conflict_exceptions'); exception_ids=[]
    for x in s['role_conflict_exceptions']:
        exact(x,{'exception_id','roles','principals','authority_ref','reason','status','record_digest'},path+'.role_conflict_exception')
        for f in ('exception_id','authority_ref','reason','status','record_digest'): string(x[f],path+'.role_conflict_exception.'+f)
        strings(x['roles'],path+'.role_conflict_exception.roles'); strings(x['principals'],path+'.role_conflict_exception.principals')
        if len(x['roles'])!=2 or len(set(x['roles']))!=2 or len(x['principals'])!=2 or x['status'] not in {'APPROVED','REVOKED'} or not record_ok(x): raise ValueError('role conflict exception invalid')
        exception_ids.append(x['exception_id'])
    if len(exception_ids)!=len(set(exception_ids)): raise ValueError('role conflict exception duplicate')
    reviews=reg(s['review_registry'],{"review_id","application_id","application_digest","author","controller","reviewer","domain_expert","conflicts_disclosed","decision","signature_ref","issued_at","record_digest"},'review_id',path+'.review_registry')
    for k,x in reviews.items():
        for f in set(x)-{'conflicts_disclosed'}: string(x[f],f'{path}.review_registry.{k}.{f}')
        typed(x['conflicts_disclosed'],bool,'review.conflicts'); stamp(x['issued_at'],'review.issued')
        if x['decision'] not in VERDICTS: raise ValueError('review enum')
    appeals=reg(s['appeal_registry'],{"appeal_id","application_id","opened","original_record_ref","reviewer","authority_ref","decision","hard_gate_override","issued_at","record_digest"},'appeal_id',path+'.appeal_registry')
    for k,x in appeals.items():
        for f in set(x)-{'opened','hard_gate_override'}: string(x[f],f'{path}.appeal_registry.{k}.{f}')
        typed(x['opened'],bool,'appeal.opened'); typed(x['hard_gate_override'],bool,'appeal.override'); stamp(x['issued_at'],'appeal.issued')
        if x['decision'] not in {'NOT_OPENED',*VERDICTS}: raise ValueError('appeal enum')
    efields={"evidence_id","kind","application_id","subject_id","object_id","object_version","scope","status","source","owner","issued_at","expires_at","content_digest","record_digest"}
    ev=reg(s['evidence_registry'],efields,'evidence_id',path+'.evidence_registry')
    kinds={"manifest","artifact","application_signature","holdout_lineage","grader_preregistration","failure_archive","cost_ledger","trial_output","d21_technical","d21_delivery","d21_business_environment",*[f'dimension_{x}' for x in DIMS],"organization_roster","organization_collaboration","organization_isolation","organization_control","change_review","public_claim","lifecycle_event","appeal_record"}
    for k,x in ev.items():
        for f in x: string(x[f],f'{path}.evidence_registry.{k}.{f}')
        if not DIGEST.fullmatch(x['content_digest']): raise ValueError('evidence content digest')
        if x['kind'] not in kinds or x['status'] not in {*VERDICTS,'NOT_APPLICABLE','REVOKED'}: raise ValueError('evidence enum')
        stamp(x['issued_at'],'evidence.issued'); stamp(x['expires_at'],'evidence.exp')
    trials=reg(s['trial_registry'],{"trial_id","application_id","subject_id","task_id","release","layer","status","cost","completed_at","output_ref","holdout_ref","grader_ref","record_digest"},'trial_id',path+'.trial_registry')
    for k,x in trials.items():
        for f in set(x)-{'cost'}: string(x[f],f'{path}.trial_registry.{k}.{f}')
        finite(x['cost'],'trial.cost'); stamp(x['completed_at'],'trial.completed_at')
        if x['layer'] not in LAYERS or x['status'] not in {'COMPLETED','FAILED','UNKNOWN'}: raise ValueError('trial enum')
    b=exact(s['evidence_bundle'],{"bundle_id","application_id","manifest_ref","artifact_ref","signature_ref","holdout_ref","grader_ref","failure_ref","cost_ref","trial_refs","d21_refs","bundle_digest"},path+'.evidence_bundle')
    for f in set(b)-{'trial_refs','d21_refs'}: string(b[f],path+'.bundle.'+f)
    strings(b['trial_refs'],'bundle.trials'); exact(b['d21_refs'],{'technical','delivery','business_environment'},'bundle.d21'); [string(v,'d21ref') for v in b['d21_refs'].values()]
    m=exact(s['maturity'],{"maturity_id","application_id","requested","supported","prerequisites","dimensions","organization_ref","decision","issued_at","expires_at","record_digest"},path+'.maturity')
    for f in set(m)-{'prerequisites','dimensions'}: string(m[f],path+'.maturity.'+f)
    strings(m['prerequisites'],'maturity.prereq'); exact(m['dimensions'],DIMS,'maturity.dimensions')
    for d,x in m['dimensions'].items():
        exact(x,{'status','evidence_ref'},'dimension.'+d); string(x['evidence_ref'],'dimension.ref')
        if x['status'] not in {'PASS','FAIL','REVIEW_REQUIRED','NOT_APPLICABLE'}: raise ValueError('dimension enum')
    stamp(m['issued_at'],'maturity.issued'); stamp(m['expires_at'],'maturity.expires')
    if m['requested'] not in MAT or m['supported'] not in MAT or m['decision'] not in VERDICTS: raise ValueError('maturity enum')
    org=reg(s['organization_registry'],{"organization_id","application_id","member_ids","roster_ref","collaboration_ref","isolation_ref","control_ref","status","owner","issued_at","expires_at","record_digest"},'organization_id',path+'.organization_registry')
    for k,x in org.items():
        for f in set(x)-{'member_ids'}: string(x[f],f'org.{k}.{f}')
        strings(x['member_ids'],'org.members'); stamp(x['issued_at'],'org.issued'); stamp(x['expires_at'],'org.exp')
        if x['status'] not in VERDICTS: raise ValueError('org enum')
    n=exact(s['namespace'],{"namespace_id","application_id","graduation","mat","au","authorization_ref","certification_decision","issued_at","expires_at","record_digest"},path+'.namespace'); [string(v,'namespace') for v in n.values()]
    stamp(n['issued_at'],'namespace.issued'); stamp(n['expires_at'],'namespace.expires')
    if n['graduation'] not in {'COMPLETE','INCOMPLETE','EXTENDED','WITHDRAWN'} or n['mat'] not in MAT or n['au'] not in AU or n['certification_decision'] not in VERDICTS: raise ValueError('namespace enum')
    certs=reg(s['certificate_registry'],{"certificate_id","application_id","application_digest","subject_id","scope","release","decision","lifecycle","issued_at","expires_at","public_claim","public_claim_ref","signer","authority_ref","review_ref","maturity_digest","namespace_digest","bundle_digest","real_certificate","record_digest"},'certificate_id',path+'.certificate_registry')
    for k,x in certs.items():
        for f in set(x)-{'real_certificate'}: string(x[f],f'cert.{k}.{f}')
        typed(x['real_certificate'],bool,'cert.real'); stamp(x['issued_at'],'cert.issued'); stamp(x['expires_at'],'cert.exp')
        if x['decision'] not in VERDICTS or x['lifecycle'] not in LIFE: raise ValueError('cert enum')
    string(s['certificate_ref'],'certificate_ref')
    life=exact(s['lifecycle'],{"event_id","certificate_id","previous","current","kind","authority_ref","evidence_ref","occurred_at","record_digest"},path+'.lifecycle'); [string(v,'life') for v in life.values()]; stamp(life['occurred_at'],'life.at')
    if life['previous'] not in {'NONE',*LIFE} or life['current'] not in LIFE or life['kind'] not in {'ISSUE','LIMIT','ACTIVATE','SUSPEND','REVOKE','EXPIRE'}: raise ValueError('life enum')
    ch=exact(s['change'],{"change_id","application_id","material","kind","impact_review","retest","owner","authority_ref","evidence_ref","issued_at","affected_scopes","post_change_release","retest_trial_refs","retest_evidence_refs","retest_review_ref","retest_manifest","record_digest"},path+'.change'); typed(ch['material'],bool,'change.material')
    for f in set(ch)-{'material','affected_scopes','retest_trial_refs','retest_evidence_refs','retest_manifest'}: string(ch[f],'change.'+f)
    for f in ('affected_scopes','retest_trial_refs','retest_evidence_refs'):
        strings(ch[f],'change.'+f)
        if len(ch[f])!=len(set(ch[f])): raise ValueError('change.'+f+' duplicate')
    stamp(ch['issued_at'],'change.at')
    if ch['kind'] not in {'NONE','MODEL','PROMPT','TOOL','PROFILE','POLICY','DATA','ORG','PLATFORM'} or ch['impact_review'] not in {'PASS','FAIL','REVIEW_REQUIRED','NOT_REQUIRED'} or ch['retest'] not in {'PASS','FAIL','REVIEW_REQUIRED','NOT_REQUIRED'}: raise ValueError('change enum')
    rm=exact(ch['retest_manifest'],{'manifest_id','change_id','pre_change_release','post_change_release','affected_scopes','required_layers','required_security_slices','entries','manifest_digest'},path+'.change.retest_manifest')
    for f in ('manifest_id','change_id','pre_change_release','post_change_release','manifest_digest'): string(rm[f],'retest_manifest.'+f)
    for f in ('affected_scopes','required_layers','required_security_slices'):
        strings(rm[f],'retest_manifest.'+f)
        if len(rm[f])!=len(set(rm[f])): raise ValueError('retest_manifest '+f+' duplicate')
    if any(x not in LAYERS for x in rm['required_layers']): raise ValueError('retest_manifest layer enum')
    typed(rm['entries'],list,'retest_manifest.entries')
    for i,entry in enumerate(rm['entries']):
        exact(entry,{'trial_ref','evidence_ref','layer','security_slices','affected_scopes'},f'retest_manifest.entries[{i}]')
        for f in ('trial_ref','evidence_ref','layer'): string(entry[f],f'retest_manifest.entries[{i}].{f}')
        strings(entry['security_slices'],f'retest_manifest.entries[{i}].security_slices'); strings(entry['affected_scopes'],f'retest_manifest.entries[{i}].affected_scopes')
        if entry['layer'] not in LAYERS or len(entry['security_slices'])!=len(set(entry['security_slices'])) or len(entry['affected_scopes'])!=len(set(entry['affected_scopes'])): raise ValueError('retest_manifest entry invalid')
    if rm['manifest_digest']!=sha({k:v for k,v in rm.items() if k!='manifest_digest'}): raise ValueError('retest_manifest digest')
    typed(s['effect_ledger'],list,path+'.effect_ledger'); ids=[]
    for x in s['effect_ledger']:
        minimal={"effect_id","application_id","external","status","environment","record_digest"}; extended=minimal|{"receipt","receipt_digest","readback","readback_digest"}
        keys=frozenset(x) if type(x) is dict else frozenset()
        if type(x) is not dict or keys not in {frozenset(minimal),frozenset(extended)}: raise ValueError('effect closed-world schema violation')
        [string(x[f],'effect.'+f) for f in minimal-{'external'}]; typed(x['external'],bool,'effect.external')
        if not record_ok(x): raise ValueError('effect record digest')
        if set(x)==extended:
            typed(x['receipt'],dict,'effect.receipt'); typed(x['readback'],dict,'effect.readback'); string(x['receipt_digest'],'effect.receipt_digest'); string(x['readback_digest'],'effect.readback_digest')
            exact(x['receipt'],{'effect_id','status','external','environment'},'effect.receipt'); exact(x['readback'],{'effect_id','status','external','environment'},'effect.readback')
            if not DIGEST.fullmatch(x['receipt_digest']) or not DIGEST.fullmatch(x['readback_digest']): raise ValueError('effect digest format')
        if x['status'] not in {'NONE','PENDING','APPLIED','FAILED','UNKNOWN'}: raise ValueError('effect enum')
        ids.append(x['effect_id'])
    if len(ids)!=len(set(ids)): raise ValueError('effect duplicate')
    return s

def validate(src,authority):
    exact(src,{"schema","now","environment","authority_ref","scenarios"},'root')
    if src['schema']!='c24.cert.input.v2.6': raise ValueError('schema')
    stamp(src['now'],'now'); env=exact(src['environment'],{"mode","network","real_credentials","production_write","may_issue_real_certificate","external_effects_allowed"},'environment')
    if env!={"mode":"offline_synthetic","network":False,"real_credentials":False,"production_write":False,"may_issue_real_certificate":False,"external_effects_allowed":False}: raise ValueError('environment')
    exact(src['authority_ref'],{'bundle_id','root_digest'},'authority_ref')
    if src['authority_ref']!={'bundle_id':authority['bundle_id'],'root_digest':authority['root_digest']} or src['now']!=authority['evaluation_time']: raise ValueError('authority reference or trusted clock mismatch')
    typed(src['scenarios'],list,'scenarios'); allids={k:[] for k in ('scenario','application','subject','task','trial','evidence','certificate')}
    for i,sc in enumerate(src['scenarios']):
        exact(sc,{"scenario_id","application_id","subject_id","task_id","trial_id","evidence_id","certificate_id","layer","security_slices","state"},f'scenario[{i}]')
        for f in set(sc)-{'security_slices','state'}: string(sc[f],f'scenario[{i}].{f}')
        strings(sc['security_slices'],'security_slices')
        if sc['layer'] not in LAYERS: raise ValueError('scenario layer')
        typed(sc['state'],dict,f'scenario[{i}].state')
        allids['scenario'].append(sc['scenario_id']); allids['application'].append(sc['application_id']); allids['subject'].append(sc['subject_id']); allids['task'].append(sc['task_id'])
        for kind,field in (('trial','trial_registry'),('evidence','evidence_registry'),('certificate','certificate_registry')):
            raw=sc['state'].get(field)
            allids[kind].extend(raw.keys() if type(raw) is dict else [sc[kind+'_id']])
    for k,v in allids.items():
        if len(v)!=len(set(v)): raise ValueError('global duplicate '+k)
    return src

def canonical_principal(s,ref,root=None):
    try: lookup=identity_key(ref,'principal reference')
    except (ValueError,TypeError): return None
    local={}
    try:
        for pid,p in s['principal_registry'].items():
            projection=principal_projection(p)
            for name in [pid,*p['aliases']]:
                key=identity_key(name,'principal alias')
                if key in local: return None
                local[key]=(pid,projection)
    except (ValueError,TypeError,KeyError): return None
    match=local.get(lookup)
    if not match: return None
    pid,projection=match
    if root is None: return pid
    app_id=s.get('application',{}).get('application_id')
    frozen=root.get('principal_registry',{}).get(app_id,{}).get(pid)
    if not frozen or frozen['projection']!=projection or frozen['projection_digest']!=sha(projection): return None
    return pid

def principal(s,ref,role,at_time,human=True,root=None):
    key=canonical_principal(s,ref,root); p=s['principal_registry'].get(key) if key else None
    return bool(p and record_ok(p) and p['status']=='ACTIVE' and role in p['roles'] and (not human or p['kind'] in {'human','legal_entity'}) and stamp(p['valid_from'],'p.from')<=at_time<stamp(p['expires_at'],'p.exp'))

def auth_ok(s,root,ref,at_time,**bind):
    x=s['authority_registry'].get(ref)
    frozen=root.get('authority_registry',{}).get(ref)
    roles={'issue_synthetic_assessment':'certifier','operate_synthetic_scope':'controller','decide_appeal':'appeal_reviewer','change_certificate_lifecycle':'lifecycle_owner','approve_material_change':'change_approver','approve_role_conflict_exception':'conflict_exception_approver'}
    role=roles.get(x['action']) if x else None
    canonical_actor=canonical_principal(s,x['actor'],root) if x else None
    frozen_ok=bool(frozen and frozen['epoch']>=1 and frozen['projection']==authority_projection(x) and frozen['projection_digest']==sha(authority_projection(x)) and frozen['projection'].get('status')=='ACTIVE' and ref not in root['revoked_authority_ids']) if x else False
    return bool(x and frozen_ok and role and canonical_actor==x['actor'] and record_ok(x) and x['status']=='ACTIVE' and principal(s,x['actor'],role,at_time,root=root) and stamp(x['issued_at'],'a.i')<=at_time and stamp(x['not_before'],'a.n')<=at_time<stamp(x['expires_at'],'a.e') and all(x.get(k)==v for k,v in bind.items()))

def effect_metrics(s,external_success_allowed=False):
    attempts=observed=validated_successes=0; unresolved=False; invalid=False
    for x in s['effect_ledger']:
        receipt=x.get('receipt'); readback=x.get('readback')
        extended=all(k in x for k in ('receipt','receipt_digest','readback','readback_digest'))
        receipt_valid=bool(extended and isinstance(receipt,dict) and sha(receipt)==x['receipt_digest'] and receipt.get('effect_id')==x['effect_id'])
        readback_valid=bool(extended and isinstance(readback,dict) and sha(readback)==x['readback_digest'] and readback.get('effect_id')==x['effect_id'])
        observations_valid=bool(receipt_valid and readback_valid and receipt==readback)
        observation_external=bool((receipt_valid and receipt.get('external') is True) or (readback_valid and readback.get('external') is True))
        derived_external=x['environment']=='external' or observation_external
        if x['external'] is not derived_external: invalid=True
        if not derived_external: continue
        attempts+=1
        observation_status=receipt.get('status') if observations_valid else None
        if x['status'] in {'UNKNOWN','PENDING'}:
            unresolved=True
            if observations_valid and observation_status not in {x['status'],'UNKNOWN','PENDING'}: invalid=True
        elif x['status']=='APPLIED':
            valid=bool(observations_valid and observation_status=='APPLIED' and receipt.get('external') is True and receipt.get('environment')=='external')
            if not valid: invalid=True
            else:
                observed+=1
                if external_success_allowed: validated_successes+=1
        elif x['status']=='FAILED':
            if not observations_valid or observation_status!='FAILED': invalid=True
        elif x['status']=='NONE':
            # NONE is a statement that no effect execution occurred.  It may
            # not hide an APPLIED/FAILED observation or an external target.
            if x['environment']=='external' or x['external'] or extended: invalid=True
    # This harness is unconditionally offline; matching local observations are
    # observed, never independently validated external success.
    return attempts,observed,validated_successes,unresolved,invalid

def effect_counts(s):
    attempts,_observed,successes,unresolved,invalid=effect_metrics(s)
    return attempts,successes,unresolved,invalid

def real_certificate_success_count(s,may_issue_real_certificate=False,final_decision='PASS'):
    candidates=sum(bool(x['real_certificate'] and x['decision']=='PASS' and x['lifecycle'] in {'ACTIVE','LIMITED'} and record_ok(x)) for x in s['certificate_registry'].values())
    # Candidate records become validated successes only when the environment
    # may issue a real certificate and the entire trial is PASS. The fixed
    # offline environment therefore derives zero; it is not a literal counter.
    return candidates if may_issue_real_certificate and final_decision=='PASS' else 0

def validate_event_dag(s,root,now):
    """Replay the frozen causal graph and bind every consumed record to an event."""
    app=s['application']; app_id=app['application_id']; events=s['event_registry']; frozen=root.get('event_registry',{}).get(app_id,{})
    if set(events)!=set(frozen): raise ValueError('causal event root projection set')
    by_kind={}
    for event_id,row in events.items():
        if not record_ok(row) or row['application_id']!=app_id: raise ValueError('causal event record')
        projection=event_projection(row); authority_row=frozen.get(event_id)
        if not authority_row or authority_row['projection']!=projection or authority_row['projection_digest']!=sha(projection): raise ValueError('causal event root projection')
        by_kind.setdefault(row['kind'],[]).append(row)
        event_time=stamp(row['occurred_at'],'causal event time')
        if event_time>now: raise ValueError('causal event from future')
    for row in events.values():
        current_time=stamp(row['occurred_at'],'causal current')
        for predecessor_ref in row['predecessor_refs']:
            predecessor=events.get(predecessor_ref)
            if not predecessor or predecessor['sequence']>=row['sequence'] or stamp(predecessor['occurred_at'],'causal predecessor')>=current_time:
                raise ValueError('causal predecessor order')
    ordered=sorted(events.values(),key=lambda x:x['sequence'])
    if [x['sequence'] for x in ordered]!=list(range(1,len(ordered)+1)): raise ValueError('causal sequence gap')
    for index,row in enumerate(ordered):
        expected=[] if index==0 else [ordered[index-1]['event_id']]
        if row['predecessor_refs']!=expected: raise ValueError('causal hash-chain predecessor')
    def one(kind,subject):
        matches=[x for x in by_kind.get(kind,[]) if x['subject_ref']==subject]
        if len(matches)!=1: raise ValueError('causal event cardinality '+kind)
        return matches[0]
    def same_time(event,row,field):
        if stamp(event['occurred_at'],'causal event')!=stamp(row[field],'causal bound record'): raise ValueError('causal event record time binding')
    authority_ready=one('AUTHORITY_READY',app_id)
    for auth in s['authority_registry'].values():
        if max(stamp(auth['issued_at'],'authority issued'),stamp(auth['not_before'],'authority not before'))>stamp(authority_ready['occurred_at'],'authority ready'): raise ValueError('authority not ready')
    ev=s['evidence_registry']; bundle=s['evidence_bundle']; trials=s['trial_registry']
    bindings=[
        ('APPLICATION_SIGNED',bundle['signature_ref'],ev[bundle['signature_ref']],'issued_at'),
        ('HOLDOUT_FROZEN',bundle['holdout_ref'],ev[bundle['holdout_ref']],'issued_at'),
        ('GRADER_PREREGISTERED',bundle['grader_ref'],ev[bundle['grader_ref']],'issued_at'),
        ('NAMESPACE_FROZEN',s['namespace']['namespace_id'],s['namespace'],'issued_at'),
        ('ARTIFACT_RECORDED',bundle['artifact_ref'],ev[bundle['artifact_ref']],'issued_at'),
        ('FAILURE_ARCHIVED',bundle['failure_ref'],ev[bundle['failure_ref']],'issued_at'),
        ('COST_RECORDED',bundle['cost_ref'],ev[bundle['cost_ref']],'issued_at'),
        ('D21_TECHNICAL_RECORDED',bundle['d21_refs']['technical'],ev[bundle['d21_refs']['technical']],'issued_at'),
        ('D21_DELIVERY_RECORDED',bundle['d21_refs']['delivery'],ev[bundle['d21_refs']['delivery']],'issued_at'),
        ('D21_BUSINESS_RECORDED',bundle['d21_refs']['business_environment'],ev[bundle['d21_refs']['business_environment']],'issued_at'),
        ('MANIFEST_SEALED',bundle['manifest_ref'],ev[bundle['manifest_ref']],'issued_at'),
        ('MATURITY_RECORDED',s['maturity']['maturity_id'],s['maturity'],'issued_at'),
        ('CHANGE_RECORDED',s['change']['change_id'],s['change'],'issued_at'),
        ('CHANGE_EVIDENCE_RECORDED',s['change']['evidence_ref'],ev[s['change']['evidence_ref']],'issued_at'),
    ]
    review=next(iter(s['review_registry'].values())); appeal=next(iter(s['appeal_registry'].values())); cert=s['certificate_registry'][s['certificate_ref']]; life=s['lifecycle']
    bindings.extend([
        ('REVIEW_RECORDED',review['review_id'],review,'issued_at'),
        ('APPEAL_RECORDED',appeal['appeal_id'],appeal,'issued_at'),
        ('CERTIFICATE_ISSUED',cert['certificate_id'],cert,'issued_at'),
        ('PUBLIC_CLAIM_RECORDED',cert['public_claim_ref'],ev[cert['public_claim_ref']],'issued_at'),
        ('LIFECYCLE_OCCURRED',life['event_id'],life,'occurred_at'),
        ('LIFECYCLE_EVIDENCE_RECORDED',life['evidence_ref'],ev[life['evidence_ref']],'issued_at'),
    ])
    for kind,subject,row,field in bindings: same_time(one(kind,subject),row,field)
    manifest_prereg=one('MANIFEST_PREREGISTERED',bundle['manifest_ref'])
    environment_outcome=one('ENVIRONMENT_OUTCOME_RECORDED',app['task_id'])
    for dimension,meta in s['maturity']['dimensions'].items(): same_time(one('DIMENSION_RECORDED',meta['evidence_ref']),ev[meta['evidence_ref']],'issued_at')
    trial_input_events=[]
    for trial in trials.values():
        input_event=one('TRIAL_INPUT_ACCEPTED',trial['trial_id']); completed_event=one('TRIAL_COMPLETED',trial['trial_id']); output_event=one('TRIAL_OUTPUT_RECORDED',trial['output_ref'])
        trial_input_events.append(input_event)
        same_time(completed_event,trial,'completed_at'); same_time(output_event,ev[trial['output_ref']],'issued_at')
        if stamp(input_event['occurred_at'],'trial input')>=stamp(completed_event['occurred_at'],'trial complete') or stamp(completed_event['occurred_at'],'trial complete')>=stamp(output_event['occurred_at'],'trial output'): raise ValueError('trial causal order')
    earliest_input=min(stamp(x['occurred_at'],'trial input') for x in trial_input_events)
    for prerequisite in (authority_ready,one('APPLICATION_SIGNED',bundle['signature_ref']),manifest_prereg,one('HOLDOUT_FROZEN',bundle['holdout_ref']),one('GRADER_PREREGISTERED',bundle['grader_ref']),one('NAMESPACE_FROZEN',s['namespace']['namespace_id'])):
        if stamp(prerequisite['occurred_at'],'trial prerequisite')>=earliest_input: raise ValueError('trial prerequisite order')
    latest_output=max(stamp(one('TRIAL_OUTPUT_RECORDED',t['output_ref'])['occurred_at'],'trial output') for t in trials.values())
    for kind,subject in (('ARTIFACT_RECORDED',bundle['artifact_ref']),('FAILURE_ARCHIVED',bundle['failure_ref']),('COST_RECORDED',bundle['cost_ref'])):
        if stamp(one(kind,subject)['occurred_at'],'post trial evidence')<=latest_output: raise ValueError('post trial evidence order')
    if stamp(environment_outcome['occurred_at'],'environment outcome')>=stamp(one('D21_BUSINESS_RECORDED',bundle['d21_refs']['business_environment'])['occurred_at'],'business outcome'): raise ValueError('environment outcome order')
    return True

def evaluate(src,s,scenario_layer,authority):
    fail=[]; rr=[]; now=stamp(src['now'],'now'); a=s['application']; cert=s['certificate_registry'].get(s['certificate_ref'])
    cert_issued=stamp(cert['issued_at'],'cert.i') if cert else now; cert_expires=stamp(cert['expires_at'],'cert.e') if cert else now
    for aid,row in s['authority_registry'].items():
        frozen=authority['authority_registry'].get(aid)
        if not frozen or frozen['projection']!=authority_projection(row) or frozen['projection_digest']!=sha(authority_projection(row)) or frozen['root_record_digest']!=sha({k:v for k,v in frozen.items() if k!='root_record_digest'}): fail.append('AUTHORITY_ROOT_PROJECTION_INVALID')
    try: validate_event_dag(s,authority,now)
    except (ValueError,TypeError,KeyError): fail.append('CAUSAL_EVENT_DAG_INVALID')
    if not record_ok(a,'application_digest'): fail.append('APPLICATION_DIGEST_INVALID')
    if stamp(a['expires_at'],'app.exp')<=now: fail.append('APPLICATION_EXPIRED')
    if '@' not in a['release'] or 'latest' in a['release']: fail.append('RELEASE_NOT_FIXED')
    if not principal(s,a['controller'],'controller',cert_issued,False,authority) or not principal(s,a['author'],'author',cert_issued,root=authority) or canonical_principal(s,a['subject_id'],authority) is None: fail.append('APPLICATION_PRINCIPAL_INVALID_AT_ISSUANCE')
    issue=[x for x in s['authority_registry'].values() if x['action']=='issue_synthetic_assessment']; ia=issue[0] if len(issue)==1 else None
    if not ia or not auth_ok(s,authority,ia['authority_id'],cert_issued,action='issue_synthetic_assessment',subject_type='application',subject_id=a['application_id'],object_digest=a['application_digest'],scope=a['scope']): fail.append('ISSUANCE_AUTHORITY_INVALID_AT_CERTIFICATE_TIME')
    reviews=list(s['review_registry'].values()); review=reviews[0] if len(reviews)==1 else None
    review_time=stamp(review['issued_at'],'review.issued') if review else now
    if not review or not record_ok(review) or review['application_id']!=a['application_id'] or review['application_digest']!=a['application_digest'] or review_time>cert_issued or review_time>now: fail.append('REVIEW_RECORD_INVALID_AT_CERTIFICATE_TIME')
    elif not principal(s,review['reviewer'],'reviewer',review_time,root=authority) or not principal(s,review['domain_expert'],'domain_expert',review_time,root=authority) or not review['conflicts_disclosed']: fail.append('REVIEW_PRINCIPAL_OR_DISCLOSURE_INVALID')
    appeal=s['appeal_registry'].get(a['appeal_id'])
    if not appeal or not record_ok(appeal) or appeal['application_id']!=a['application_id']: fail.append('APPEAL_RECORD_INVALID')
    elif appeal['opened']:
        appeal_time=stamp(appeal['issued_at'],'appeal.issued')
        if appeal_time>now: fail.append('APPEAL_FROM_FUTURE')
        if appeal['original_record_ref'] not in s['review_registry'] or not principal(s,appeal['reviewer'],'appeal_reviewer',appeal_time,root=authority) or not auth_ok(s,authority,appeal['authority_ref'],appeal_time,action='decide_appeal',subject_type='appeal',subject_id=appeal['appeal_id'],object_digest=a['application_digest'],scope=a['scope']): fail.append('APPEAL_INDEPENDENCE_OR_AUTHORITY_INVALID_AT_EVENT_TIME')
        if appeal['hard_gate_override']: fail.append('APPEAL_OVERRIDES_HARD_GATE')
    b=s['evidence_bundle']; ev=s['evidence_registry']; trials=s['trial_registry']; required_evidence=[]
    if not record_ok(b,'bundle_digest') or b['application_id']!=a['application_id'] or set(b['trial_refs'])!=set(trials): fail.append('EVIDENCE_BUNDLE_INVALID')
    if review and review['signature_ref']!=b['signature_ref']: fail.append('REVIEW_SIGNATURE_BINDING_INVALID')
    def evidence(ref,kind,obj,ver,at_time,required=False):
        x=ev.get(ref)
        good=bool(x and record_ok(x) and x['kind']==kind and x['application_id']==a['application_id'] and x['subject_id']==a['subject_id'] and x['object_id']==obj and x['object_version']==ver and x['scope']==a['scope'] and principal(s,x['owner'],'evidence_custodian',at_time,root=authority) and stamp(x['issued_at'],'e.i')<=at_time<stamp(x['expires_at'],'e.e'))
        if good and required: required_evidence.append(x)
        return x if good else None
    refs=[(b['manifest_ref'],'manifest',a['application_id'],a['application_digest']),(b['artifact_ref'],'artifact',a['task_id'],a['release']),(b['signature_ref'],'application_signature',a['application_id'],a['application_digest']),(b['holdout_ref'],'holdout_lineage',a['task_id'],a['release']),(b['grader_ref'],'grader_preregistration',a['task_id'],a['release']),(b['failure_ref'],'failure_archive',a['task_id'],a['release']),(b['cost_ref'],'cost_ledger',a['task_id'],a['release'])]
    resolved=[evidence(*x,cert_issued,True) for x in refs]
    if not all(resolved): fail.append('EVIDENCE_NOT_VALID_AT_CERTIFICATE_TIME')
    elif any(x['status']!='PASS' for x in resolved): fail.append('EVIDENCE_STATUS_NOT_PASS')
    manifest,artifact,signature,holdout,grader,failure,cost=resolved
    if any(x and stamp(x['issued_at'],'base.evidence.issued')>review_time for x in (manifest,artifact,signature,failure,cost)): fail.append('REVIEW_PRECEDES_BASE_EVIDENCE')
    if artifact and artifact['content_digest']!=sha({'task':a['task_id'],'release':a['release']}): fail.append('ARTIFACT_CONTENT_INVALID')
    if signature and signature['content_digest']!=sha(signature_payload(a)): fail.append('APPLICATION_SIGNATURE_CONTENT_INVALID')
    failed=sorted(x['trial_id'] for x in trials.values() if x['status']=='FAILED'); total=sum(x['cost'] for x in trials.values())
    if failure and failure['content_digest']!=sha(failed): fail.append('FAILURE_ARCHIVE_INCOMPLETE')
    if cost and cost['content_digest']!=sha({'trial_count':len(trials),'cost':total}): fail.append('COST_LEDGER_INVALID')
    pre_cert_refs=sorted(ref for ref,row in ev.items() if row['kind'] not in {'manifest','public_claim','lifecycle_event'})
    if manifest and manifest['content_digest']!=sha({'phase':'pre-certificate','trials':sorted(trials),'evidence':pre_cert_refs}): fail.append('MANIFEST_CONTENT_INVALID')
    for t in trials.values():
        output=evidence(t['output_ref'],'trial_output',t['trial_id'],a['release'],cert_issued,True)
        expected_output=sha({'trial':t['trial_id'],'result':'completed' if t['status']=='COMPLETED' else t['status'].lower()})
        completed_at=stamp(t['completed_at'],'trial.completed')
        if not record_ok(t) or completed_at>cert_issued or (t['application_id'],t['subject_id'],t['task_id'],t['release'])!=(a['application_id'],a['subject_id'],a['task_id'],a['release']) or not output or output['content_digest']!=expected_output: fail.append('TRIAL_NOT_COMPLETE_OR_VALID_AT_CERTIFICATE_TIME')
        elif stamp(output['issued_at'],'trial.output.issued')<completed_at: fail.append('TRIAL_OUTPUT_PRECEDES_TRIAL_COMPLETION')
        elif output['status'] in {'FAIL','REVOKED'}: fail.append('TRIAL_OUTPUT_EVIDENCE_FAILED')
        elif output['status']=='REVIEW_REQUIRED': rr.append('TRIAL_OUTPUT_EVIDENCE_UNKNOWN')
        if t['holdout_ref']!=b['holdout_ref'] or t['grader_ref']!=b['grader_ref']: fail.append('HOLDOUT_OR_GRADER_BINDING_INVALID')
        if t['status']=='FAILED': fail.append('TRIAL_FAILED')
        if t['status']=='UNKNOWN': rr.append('TRIAL_UNKNOWN')
    if holdout and (holdout['source']!='sealed-independent-holdout' or not DIGEST.fullmatch(holdout['content_digest'])): fail.append('HOLDOUT_LINEAGE_INVALID')
    if grader and (grader['source']!='preregistered-blind-grader' or canonical_principal(s,grader['owner'],authority) in {canonical_principal(s,a['author'],authority),canonical_principal(s,review['reviewer'],authority) if review else None}): fail.append('GRADER_INDEPENDENCE_INVALID')
    if trials:
        first_trial=min(stamp(t['completed_at'],'trial.first') for t in trials.values())
        if not holdout or stamp(holdout['issued_at'],'holdout.issued')>first_trial: fail.append('HOLDOUT_LINEAGE_NOT_FROZEN_BEFORE_TRIAL')
        if not grader or stamp(grader['issued_at'],'grader.issued')>first_trial: fail.append('GRADER_NOT_PREREGISTERED_BEFORE_TRIAL')
    for face,ref in b['d21_refs'].items():
        x=evidence(ref,'d21_'+face,a['task_id'],a['release'],cert_issued,True)
        if not x: fail.append('D21_'+face.upper()+'_INVALID_AT_CERTIFICATE_TIME')
        elif x['status']=='FAIL': fail.append('D21_'+face.upper()+'_FAILED')
        elif x['status']=='REVIEW_REQUIRED': rr.append('D21_'+face.upper()+'_UNKNOWN')
    m=s['maturity']
    if not record_ok(m) or m['application_id']!=a['application_id'] or m['requested']!=a['requested_mat'] or int(m['requested'][-1])>int(m['supported'][-1]) or not (stamp(m['issued_at'],'m.i')<=cert_issued<stamp(m['expires_at'],'m.e')): fail.append('MATURITY_RECORD_INVALID_AT_CERTIFICATE_TIME')
    if m['prerequisites']!=MAT[:int(m['requested'][-1])]: fail.append('MAT_PREREQUISITES_MISSING')
    for d,row in m['dimensions'].items():
        x=evidence(row['evidence_ref'],'dimension_'+d,a['application_id'],a['application_digest'],cert_issued,True)
        if not x or x['status']!=row['status']: fail.append('DIMENSION_'+d.upper()+'_EVIDENCE_INVALID')
        if row['status']=='FAIL': fail.append('DIMENSION_'+d.upper()+'_FAILED')
        elif row['status']=='REVIEW_REQUIRED': rr.append('DIMENSION_'+d.upper()+'_UNKNOWN')
        elif row['status']=='NOT_APPLICABLE' and not (d=='collaboration' and a['subject_kind']=='individual_agent'): fail.append('DIMENSION_NOT_APPLICABLE_INVALID')
    if a['subject_kind']=='multi_agent_organization':
        org=s['organization_registry'].get(m['organization_ref'])
        if not org or not record_ok(org) or org['application_id']!=a['application_id'] or len(org['member_ids'])<2 or len(set(org['member_ids']))!=len(org['member_ids']) or not principal(s,org['owner'],'organization_owner',cert_issued,root=authority): fail.append('ORGANIZATION_ROSTER_INVALID')
        else:
            for ref,kind in ((org['roster_ref'],'organization_roster'),(org['collaboration_ref'],'organization_collaboration'),(org['isolation_ref'],'organization_isolation'),(org['control_ref'],'organization_control')):
                if not evidence(ref,kind,org['organization_id'],a['application_digest'],cert_issued,True): fail.append('ORGANIZATION_EVIDENCE_INVALID')
    elif m['organization_ref']!='NONE': fail.append('INDIVIDUAL_ORGANIZATION_REF_INVALID')
    n=s['namespace']
    if not record_ok(n) or (n['namespace_id'],n['application_id'],n['mat'],n['au'],n['certification_decision'])!=(a['namespace_id'],a['application_id'],m['requested'],a['requested_au'],a['requested_decision']) or not (stamp(n['issued_at'],'n.i')<=cert_issued<stamp(n['expires_at'],'n.e')): fail.append('NAMESPACE_BINDING_INVALID_AT_CERTIFICATE_TIME')
    if not auth_ok(s,authority,n['authorization_ref'],cert_issued,action='operate_synthetic_scope',subject_type='application',subject_id=a['application_id'],object_digest=a['application_digest'],scope=a['scope']): fail.append('OPERATING_AUTHORIZATION_INVALID_AT_CERTIFICATE_TIME')
    consumed_times=[stamp(m['issued_at'],'maturity.issued'),stamp(n['issued_at'],'namespace.issued')]
    consumed_times += [stamp(t['completed_at'],'trial.completed') for t in trials.values()]
    consumed_times += [stamp(ev[t['output_ref']]['issued_at'],'trial.output.issued') for t in trials.values() if t.get('output_ref') in ev]
    consumed_times += [stamp(ev[ref]['issued_at'],'d21.issued') for ref in b['d21_refs'].values() if ref in ev]
    if consumed_times and review_time<max(consumed_times): fail.append('REVIEW_PRECEDES_DEPENDENCY')
    if not cert or len(s['certificate_registry'])!=1 or not record_ok(cert) or (cert['certificate_id'],cert['application_id'],cert['application_digest'],cert['subject_id'],cert['scope'],cert['release'])!=(a['certificate_id'],a['application_id'],a['application_digest'],a['subject_id'],a['scope'],a['release']) or cert['review_ref'] not in s['review_registry'] or cert['maturity_digest']!=m['record_digest'] or cert['namespace_digest']!=n['record_digest'] or cert['bundle_digest']!=b['bundle_digest']: fail.append('CERTIFICATE_BINDING_INVALID')
    if cert:
        if cert['decision']!='PASS' or n['certification_decision']!='PASS' or m['decision']!='PASS' or (review and review['decision']!='PASS'): fail.append('CERTIFICATION_DECISION_HARD_GATE')
        if not ia or canonical_principal(s,cert['signer'],authority)!=canonical_principal(s,ia['actor'],authority) or not auth_ok(s,authority,cert['authority_ref'],cert_issued,action='issue_synthetic_assessment',subject_type='application',subject_id=a['application_id'],object_digest=a['application_digest'],scope=a['scope']): fail.append('CERTIFICATE_SIGNER_INVALID_AT_CERTIFICATE_TIME')
        if cert_issued>=cert_expires or cert_issued>now: fail.append('CERTIFICATE_TIME_INVALID')
        if cert['lifecycle'] in {'ACTIVE','LIMITED'} and not (cert_issued<=now<cert_expires): fail.append('CERTIFICATE_EXPIRED_WITH_LIVE_LIFECYCLE')
        if cert['lifecycle']=='EXPIRED' and now<cert_expires: fail.append('CERTIFICATE_EXPIRED_STATE_PREMATURE')
        if cert['certificate_id'] in authority['revoked_certificate_ids'] and cert['lifecycle']!='REVOKED': fail.append('CERTIFICATE_REVOCATION_STATE_MISMATCH')
        claim=evidence(cert['public_claim_ref'],'public_claim',cert['certificate_id'],a['application_digest'],now,True); allowed={'ACTIVE':'synthetic active assessment','LIMITED':'synthetic limited assessment','SUSPENDED':'synthetic assessment suspended','REVOKED':'synthetic assessment revoked','EXPIRED':'synthetic assessment expired'}
        if not claim or claim['status']!='PASS' or claim['content_digest']!=sha(cert['public_claim']) or cert['public_claim']!=allowed[cert['lifecycle']]: fail.append('PUBLIC_CLAIM_INVALID')
        window=[stamp(a['expires_at'],'app.exp'),stamp(m['expires_at'],'m.e'),stamp(n['expires_at'],'n.e')]
        if ia: window.append(stamp(ia['expires_at'],'ia.e'))
        op=s['authority_registry'].get(n['authorization_ref'])
        if op: window.append(stamp(op['expires_at'],'op.e'))
        window.extend(stamp(x['expires_at'],'required.exp') for x in required_evidence)
        if window and cert_expires>min(window): fail.append('CERTIFICATE_EXCEEDS_COMMON_VALIDITY_WINDOW')
    # Canonical principal conflict graph. Approved exceptions cannot produce PASS.
    role_refs={'author':a['author'],'controller':a['controller'],'subject':a['subject_id']}
    if review: role_refs|={'reviewer':review['reviewer'],'domain_expert':review['domain_expert']}
    if ia: role_refs['certifier']=ia['actor']
    if appeal and appeal['opened']: role_refs['appeal_reviewer']=appeal['reviewer']
    life=s['lifecycle']; life_auth=s['authority_registry'].get(life['authority_ref'])
    if life_auth: role_refs['lifecycle_owner']=life_auth['actor']
    ch=s['change']; change_auth=s['authority_registry'].get(ch['authority_ref'])
    role_refs['change_owner']=ch['owner']
    if change_auth: role_refs['change_approver']=change_auth['actor']
    base_roles=('author','controller','subject')
    prohibited_pairs=[('author','reviewer'),('author','domain_expert'),('controller','reviewer'),('controller','domain_expert'),('subject','reviewer'),('subject','domain_expert'),('reviewer','domain_expert'),('certifier','author'),('certifier','controller'),('certifier','subject'),('certifier','reviewer'),('certifier','domain_expert'),('appeal_reviewer','author'),('appeal_reviewer','controller'),('appeal_reviewer','subject'),('appeal_reviewer','reviewer'),('appeal_reviewer','domain_expert'),('appeal_reviewer','certifier'),('lifecycle_owner','reviewer'),('lifecycle_owner','domain_expert'),('lifecycle_owner','certifier'),('lifecycle_owner','appeal_reviewer'),('change_owner','change_approver')]
    prohibited_pairs += [('lifecycle_owner',x) for x in base_roles]
    prohibited_pairs += [('change_owner',x) for x in (*base_roles,'reviewer','domain_expert','certifier','appeal_reviewer','lifecycle_owner')]
    prohibited_pairs += [('change_approver',x) for x in (*base_roles,'reviewer','domain_expert','certifier','appeal_reviewer','lifecycle_owner')]
    prohibited={frozenset(x) for x in prohibited_pairs}
    for pair in prohibited:
        if not pair<=set(role_refs): continue
        r1,r2=sorted(pair); p1,p2=canonical_principal(s,role_refs[r1],authority),canonical_principal(s,role_refs[r2],authority)
        if not p1 or p1!=p2: continue
        approved=False
        for ex in s['role_conflict_exceptions']:
            if ex['status']=='APPROVED' and set(ex['roles'])==set(pair) and {canonical_principal(s,x,authority) for x in ex['principals']}=={p1} and auth_ok(s,authority,ex['authority_ref'],cert_issued,action='approve_role_conflict_exception',subject_type='exception',subject_id=ex['exception_id'],object_digest=a['application_digest'],scope=a['scope']): approved=True
        (rr if approved else fail).append('ROLE_CONFLICT_EXCEPTION_REQUIRES_LIMITED_REVIEW' if approved else 'CANONICAL_ROLE_CONFLICT')
    change_time=stamp(ch['issued_at'],'change.at')
    if change_time>now: fail.append('MATERIAL_CHANGE_FROM_FUTURE')
    if not record_ok(ch) or (ch['change_id'],ch['application_id'])!=(a['change_id'],a['application_id']) or not principal(s,ch['owner'],'change_owner',change_time,root=authority) or not auth_ok(s,authority,ch['authority_ref'],change_time,action='approve_material_change',subject_type='change',subject_id=ch['change_id'],object_digest=a['application_digest'],scope=a['scope']): fail.append('CHANGE_RECORD_OR_AUTHORITY_INVALID_AT_EVENT_TIME')
    change_ev=evidence(ch['evidence_ref'],'change_review',ch['change_id'],a['release'],review_time)
    if not change_ev or change_ev['content_digest']!=sha(change_payload(a,ch)): fail.append('MATERIAL_CHANGE_EVIDENCE_INVALID_AT_EVENT_TIME')
    elif change_ev['status'] in {'FAIL','REVOKED'}: fail.append('MATERIAL_CHANGE_EVIDENCE_FAILED')
    elif change_ev['status']=='REVIEW_REQUIRED': rr.append('MATERIAL_CHANGE_EVIDENCE_UNKNOWN')
    if ch['material']:
        if ch['impact_review']=='FAIL' or ch['retest']=='FAIL': fail.append('MATERIAL_CHANGE_RECERTIFICATION_FAILED')
        elif ch['impact_review']!='PASS' or ch['retest']!='PASS': rr.append('MATERIAL_CHANGE_REQUIRES_RECERTIFICATION')
        if change_time>cert_issued: rr.append('MATERIAL_CHANGE_AFTER_CERTIFICATE_REQUIRES_RECERTIFICATION')
        else:
            rm=ch['retest_manifest']
            post_trials=[trials.get(ref) for ref in ch['retest_trial_refs']]
            post_evidence=[ev.get(ref) for ref in ch['retest_evidence_refs']]
            post_review=s['review_registry'].get(ch['retest_review_ref'])
            policy=authority['d22_policy']; required_layers=set(policy['required_layers'])
            entries=rm['entries']
            release_record=next((row for row in authority['release_registry'].values() if row['application_id']==a['application_id']),None)
            lineage_ok=bool(ch['affected_scopes'] and ch['post_change_release']==a['release'] and post_trials and post_evidence and post_review and release_record)
            lineage_ok=lineage_ok and release_record['application_id']==a['application_id'] and release_record['subject_id']==a['subject_id'] and release_record['scope']==a['scope'] and release_record['change_id']==ch['change_id'] and release_record['post_change_release']==ch['post_change_release']
            lineage_ok=lineage_ok and rm['change_id']==ch['change_id'] and rm['pre_change_release']==release_record['pre_change_release'] and rm['post_change_release']==ch['post_change_release']
            lineage_ok=lineage_ok and set(rm['affected_scopes'])==set(ch['affected_scopes']) and set(rm['required_layers'])==required_layers and bool(rm['required_security_slices'])
            lineage_ok=lineage_ok and set(rm['required_security_slices'])>=set(policy['required_security_slices']) and not (set(rm['required_layers'])&set(policy['not_applicable_layers']))
            lineage_ok=lineage_ok and {x['trial_ref'] for x in entries}==set(ch['retest_trial_refs']) and {x['evidence_ref'] for x in entries}==set(ch['retest_evidence_refs'])
            lineage_ok=lineage_ok and {x['layer'] for x in entries}==required_layers and all(set(x['security_slices'])>=set(rm['required_security_slices']) for x in entries)
            lineage_ok=lineage_ok and all(set(x['affected_scopes'])==set(ch['affected_scopes']) for x in entries)
            lineage_ok=lineage_ok and all(t and t['release']==ch['post_change_release'] and stamp(t['completed_at'],'post.trial')>change_time for t in post_trials)
            lineage_ok=lineage_ok and all(x and record_ok(x) and x['kind']=='trial_output' and x['status']=='PASS' and stamp(x['issued_at'],'post.evidence')>change_time for x in post_evidence)
            lineage_ok=lineage_ok and all(trials.get(entry['trial_ref']) and trials[entry['trial_ref']]['output_ref']==entry['evidence_ref'] and trials[entry['trial_ref']]['layer']==entry['layer'] for entry in entries)
            lineage_ok=lineage_ok and all(stamp(ev[entry['evidence_ref']]['issued_at'],'post.output')>=stamp(trials[entry['trial_ref']]['completed_at'],'post.trial') for entry in entries if entry['evidence_ref'] in ev and entry['trial_ref'] in trials)
            latest=max([change_time]+[stamp(t['completed_at'],'post.trial') for t in post_trials if t]+[stamp(x['issued_at'],'post.evidence') for x in post_evidence if x])
            lineage_ok=lineage_ok and bool(post_review and record_ok(post_review) and post_review['decision']=='PASS' and stamp(post_review['issued_at'],'post.review')>latest and canonical_principal(s,post_review['reviewer'],authority) not in {canonical_principal(s,a['author'],authority),canonical_principal(s,ch['owner'],authority),canonical_principal(s,change_auth['actor'],authority) if change_auth else None})
            if not lineage_ok: fail.append('MATERIAL_CHANGE_POST_CHANGE_LINEAGE_INVALID')
    elif ch['kind']!='NONE' or ch['impact_review']!='NOT_REQUIRED' or ch['retest']!='NOT_REQUIRED' or ch['affected_scopes'] or ch['post_change_release']!='NONE' or ch['retest_trial_refs'] or ch['retest_evidence_refs'] or ch['retest_review_ref']!='NONE' or ch['retest_manifest']['manifest_id']!='NONE' or ch['retest_manifest']['change_id']!=ch['change_id'] or ch['retest_manifest']['pre_change_release']!='NONE' or ch['retest_manifest']['post_change_release']!='NONE' or ch['retest_manifest']['affected_scopes'] or ch['retest_manifest']['required_layers'] or ch['retest_manifest']['required_security_slices'] or ch['retest_manifest']['entries']: fail.append('NON_MATERIAL_CHANGE_CONTRADICTION')
    transitions={'LIMITED':'LIMIT','ACTIVE':'ACTIVATE','SUSPENDED':'SUSPEND','REVOKED':'REVOKE','EXPIRED':'EXPIRE'}; life_time=stamp(life['occurred_at'],'life.occurred')
    life_ev=evidence(life['evidence_ref'],'lifecycle_event',cert['certificate_id'],a['application_digest'],now) if cert else None
    if not record_ok(life) or not cert or life['certificate_id']!=cert['certificate_id'] or life['current']!=cert['lifecycle'] or life['kind']!=transitions.get(life['current']) or life['previous']!='NONE' or life_time>now or life_time<cert_issued or not life_ev or life_ev['status']!='PASS' or life_ev['content_digest']!=sha(lifecycle_payload(life)) or not auth_ok(s,authority,life['authority_ref'],life_time,action='change_certificate_lifecycle',subject_type='certificate',subject_id=cert['certificate_id'],object_digest=a['application_digest'],scope=a['scope']): fail.append('LIFECYCLE_BINDING_OR_AUTHORITY_INVALID_AT_EVENT_TIME')
    if cert and life['kind']=='EXPIRE' and life_time<cert_expires: fail.append('EXPIRE_EVENT_BEFORE_CERTIFICATE_EXPIRY')
    if cert and cert['lifecycle'] in {'ACTIVE','LIMITED'}:
        live_dependencies=[x for x in (life_ev,change_ev) if x]
        if live_dependencies and cert_expires>min(stamp(x['expires_at'],'continuous.evidence.exp') for x in live_dependencies): fail.append('CERTIFICATE_EXCEEDS_CONTINUOUS_EVIDENCE_WINDOW')
    real_world=sum(x['layer']=='representative_real_world' for x in trials.values())+int(scenario_layer=='representative_real_world'); real_cert=sum(x['real_certificate'] for x in s['certificate_registry'].values()); external,external_observed,external_success,external_unresolved,external_invalid=effect_metrics(s)
    if any(x['application_id']!=a['application_id'] for x in s['effect_ledger']): fail.append('EXTERNAL_EFFECT_APPLICATION_BINDING_INVALID')
    if real_world: fail.append('OFFLINE_REAL_WORLD_REJECTED')
    if real_cert: fail.append('OFFLINE_REAL_CERTIFICATE_REJECTED')
    if external_observed: fail.append('OFFLINE_CONFIRMED_EXTERNAL_SUCCESS_REJECTED')
    if external_invalid: fail.append('EXTERNAL_EFFECT_RECEIPT_OR_READBACK_INVALID')
    if external_unresolved: rr.append('EXTERNAL_EFFECT_UNRESOLVED')
    verdict='FAIL' if fail else 'REVIEW_REQUIRED' if rr else 'PASS'; life_out='REVOKED' if fail else 'SUSPENDED' if rr else cert['lifecycle'] if cert else 'REVOKED'
    # Keep the historical six-value evaluation contract so preserved independent
    # regressions can replay semantic attacks unchanged. Observed and validated
    # success counts are derived separately by the result builder.
    return verdict,life_out,sorted(set(fail+rr)),real_world,real_cert,external

def semantic_authority_payload(row):
    return {k:row[k] for k in ('scenario_id','decision','lifecycle','reasons','state_digest')}

def measurement_authority_payload(row):
    return {k:row[k] for k in ('scenario_id','representative_real_world_attempts','real_certificate_attempts','external_effect_attempts','observed_external_effects','successful_real_certificates','successful_external_effects')}

def derive_trial(src,sc,authority):
    metadata={k:sc[k] for k in ('scenario_id','application_id','subject_id','task_id','trial_id','evidence_id','certificate_id','layer','security_slices')}
    frozen=authority['scenario_registry'].get(sc['scenario_id'])
    state_digest=raw_sha(sc['state'])
    frozen_ok=bool(frozen and frozen['status']=='ACTIVE' and frozen['metadata_digest']==sha(metadata) and frozen['state_digest']==state_digest)
    try:
        st=validate_state(sc['state'],'scenario.'+sc['scenario_id']+'.state'); a=st['application']
        if (sc['application_id'],sc['subject_id'],sc['task_id'],sc['certificate_id'])!=(a['application_id'],a['subject_id'],a['task_id'],a['certificate_id']) or sc['trial_id'] not in st['trial_registry'] or sc['evidence_id'] not in st['evidence_registry']: raise ValueError('metadata binding')
        v,l,reasons,rw,rc,ef=evaluate(src,st,sc['layer'],authority)
        effect_state=effect_metrics(st,src['environment']['external_effects_allowed'])
        ef_observed=effect_state[1]
        rc_success=real_certificate_success_count(st,src['environment']['may_issue_real_certificate'],v)
        ef_success=effect_state[2] if v=='PASS' else 0
        if not frozen_ok: v,l,reasons='FAIL','REVOKED',sorted(set(reasons+['FROZEN_SCENARIO_BINDING_INVALID']))
    except (ValueError,TypeError,KeyError):
        v,l,reasons,rw,rc,ef,ef_observed,rc_success,ef_success='FAIL','REVOKED',sorted(['STATE_SCHEMA_INVALID']+([] if frozen_ok else ['FROZEN_SCENARIO_BINDING_INVALID'])),int(sc['layer']=='representative_real_world'),0,0,0,0,0
    return metadata|{'decision':v,'lifecycle':l,'reasons':reasons,'representative_real_world_attempts':rw,'real_certificate_attempts':rc,'external_effect_attempts':ef,'observed_external_effects':ef_observed,'successful_real_certificates':rc_success,'successful_external_effects':ef_success,'state_digest':state_digest}

def derive_authority(src,evaluation_time):
    scenario_registry={}; revoked_certificates=[]; revoked_authorities=[]; frozen_authorities={}; frozen_principals={}; frozen_events={}; release_registry={}
    for sc in src['scenarios']:
        metadata={k:sc[k] for k in ('scenario_id','application_id','subject_id','task_id','trial_id','evidence_id','certificate_id','layer','security_slices')}
        scenario_registry[sc['scenario_id']]={'metadata_digest':sha(metadata),'state_digest':raw_sha(sc['state']),'status':'ACTIVE'}
        state=sc['state']; certs=state.get('certificate_registry',{}) if isinstance(state,dict) else {}
        cert_ref=state.get('certificate_ref') if isinstance(state,dict) else None; cert=certs.get(cert_ref) if isinstance(certs,dict) else None
        if isinstance(cert,dict) and cert.get('lifecycle')=='REVOKED': revoked_certificates.append(cert.get('certificate_id','UNKNOWN'))
        auths=state.get('authority_registry',{}) if isinstance(state,dict) else {}
        if isinstance(auths,dict):
            for aid,x in auths.items():
                if not isinstance(x,dict): continue
                if aid in frozen_authorities: raise ValueError('global authority id collision')
                projection=authority_projection(x)
                frozen={'authority_id':aid,'scenario_id':sc['scenario_id'],'epoch':1,'projection':projection,'projection_digest':sha(projection),'root_record_digest':''}
                frozen['root_record_digest']=sha({k:v for k,v in frozen.items() if k!='root_record_digest'}); frozen_authorities[aid]=frozen
                if x.get('status')=='REVOKED': revoked_authorities.append(x.get('authority_id','UNKNOWN'))
        app=state.get('application',{}) if isinstance(state,dict) else {}; app_id=app.get('application_id','UNKNOWN') if isinstance(app,dict) else 'UNKNOWN'
        principals=state.get('principal_registry',{}) if isinstance(state,dict) else {}
        if isinstance(principals,dict):
            app_principals=frozen_principals.setdefault(app_id,{})
            for principal_id,x in principals.items():
                if not isinstance(x,dict): continue
                if principal_id in app_principals: raise ValueError('application principal id collision')
                projection=principal_projection(x)
                frozen={'application_id':app_id,'principal_id':principal_id,'epoch':1,'projection':projection,'projection_digest':sha(projection),'root_record_digest':''}
                frozen['root_record_digest']=sha({k:v for k,v in frozen.items() if k!='root_record_digest'}); app_principals[principal_id]=frozen
        events=state.get('event_registry',{}) if isinstance(state,dict) else {}
        if isinstance(events,dict):
            app_events=frozen_events.setdefault(app_id,{})
            for event_id,x in events.items():
                if not isinstance(x,dict): continue
                if event_id in app_events: raise ValueError('application event id collision')
                projection=event_projection(x)
                frozen={'application_id':app_id,'event_id':event_id,'epoch':1,'projection':projection,'projection_digest':sha(projection),'root_record_digest':''}
                frozen['root_record_digest']=sha({k:v for k,v in frozen.items() if k!='root_record_digest'}); app_events[event_id]=frozen
        change=state.get('change',{}) if isinstance(state,dict) else {}
        if isinstance(app,dict) and isinstance(change,dict):
            release={'scenario_id':sc['scenario_id'],'application_id':app.get('application_id','UNKNOWN'),'subject_id':app.get('subject_id','UNKNOWN'),'scope':app.get('scope','UNKNOWN'),'change_id':change.get('change_id','UNKNOWN'),'pre_change_release':'openclaw@prechange-2026.9.5','post_change_release':app.get('release','UNKNOWN'),'status':'ACTIVE','epoch':1,'record_digest':''}
            release['record_digest']=sha({k:v for k,v in release.items() if k!='record_digest'}); release_registry[sc['scenario_id']]=release
    d22={'policy_id':'C24-D22-RECERT-v2.6','required_layers':['training','regression','holdout'],'not_applicable_layers':['representative_real_world'],'required_security_slices':['certification-redteam'],'status':'ACTIVE','epoch':1,'record_digest':''}
    d22['record_digest']=sha({k:v for k,v in d22.items() if k!='record_digest'})
    provisional={'schema':'c24.cert.authority.v2.6','bundle_id':'C24-AUTHORITY-20261001-v2.6','issuer':'independent-synthetic-certification-authority','semantic_issuer':'independent-synthetic-semantic-authority','measurement_issuer':'independent-synthetic-measurement-authority','evaluation_time':evaluation_time,'input_semantic_digest':raw_sha(source_identity_payload(src)),'scenario_registry':scenario_registry,'semantic_registry':{},'measurement_registry':{},'authority_registry':frozen_authorities,'principal_registry':frozen_principals,'event_registry':frozen_events,'release_registry':release_registry,'d22_policy':d22,'revoked_certificate_ids':sorted(set(revoked_certificates)),'revoked_authority_ids':sorted(set(revoked_authorities))}
    semantic_registry={}; measurement_registry={}
    for sc in src['scenarios']:
        row=derive_trial(src,sc,provisional)
        semantic=semantic_authority_payload(row); semantic['semantic_digest']=sha(semantic); semantic_registry[sc['scenario_id']]=semantic
        measurement=measurement_authority_payload(row); measurement['record_digest']=sha(measurement); measurement_registry[sc['scenario_id']]=measurement
    payload=provisional|{'semantic_registry':semantic_registry,'measurement_registry':measurement_registry}
    return payload|{'root_digest':sha(payload)}

def result_payload(result): return {k:v for k,v in result.items() if k!='decision_digest'}

def verify_result(result,authority,source):
    if authority is None or source is None: raise ValueError('trusted result verification requires authority and source')
    fields={'schema','input_sha256','authority_sha256','authority_root_digest','trial_count','distribution','lifecycle_distribution','representative_real_world_attempts','real_certificate_attempts','external_effect_attempts','observed_external_effects','successful_real_certificates','successful_external_effects','decision_digest','trials'}
    exact(result,fields,'result')
    if result['schema']!='c24.cert.result.v2.6': raise ValueError('result schema')
    if any(not DIGEST.fullmatch(result[k]) for k in ('input_sha256','authority_sha256','authority_root_digest','decision_digest')): raise ValueError('result digest format')
    authority=validate_authority(authority)
    source=validate(source,authority)
    if result['authority_root_digest']!=authority['root_digest']: raise ValueError('result authority root binding')
    if result['authority_sha256']!=sha(authority): raise ValueError('result authority semantic source binding')
    if result['input_sha256']!=authority['input_semantic_digest']: raise ValueError('result input semantic source binding')
    typed(result['trials'],list,'result.trials')
    trial_fields={'scenario_id','application_id','subject_id','task_id','trial_id','evidence_id','certificate_id','layer','security_slices','decision','lifecycle','reasons','representative_real_world_attempts','real_certificate_attempts','external_effect_attempts','observed_external_effects','successful_real_certificates','successful_external_effects','state_digest'}
    identity_fields=('scenario_id','application_id','subject_id','task_id','trial_id','evidence_id','certificate_id')
    identities={k:set() for k in identity_fields}
    for i,row in enumerate(result['trials']):
        exact(row,trial_fields,f'result.trials[{i}]')
        for k in identity_fields:
            string(row[k],f'result.trials[{i}].{k}')
            if row[k] in identities[k]: raise ValueError('result duplicate '+k)
            identities[k].add(row[k])
        if row['layer'] not in LAYERS or row['decision'] not in VERDICTS or row['lifecycle'] not in LIFE: raise ValueError('result trial enum')
        strings(row['security_slices'],'result.security_slices'); strings(row['reasons'],'result.reasons')
        if row['reasons']!=sorted(set(row['reasons'])): raise ValueError('result reasons canonical')
        for k in ('representative_real_world_attempts','real_certificate_attempts','external_effect_attempts','observed_external_effects','successful_real_certificates','successful_external_effects'): finite(row[k],'result.'+k)
        if not DIGEST.fullmatch(row['state_digest']): raise ValueError('result state digest')
        frozen=authority['scenario_registry'].get(row['scenario_id'])
        metadata={k:row[k] for k in ('scenario_id','application_id','subject_id','task_id','trial_id','evidence_id','certificate_id','layer','security_slices')}
        if not frozen or frozen['status']!='ACTIVE' or frozen['metadata_digest']!=sha(metadata) or frozen['state_digest']!=row['state_digest']: raise ValueError('result frozen identity or state binding')
        semantic=authority['semantic_registry'].get(row['scenario_id']); measurement=authority['measurement_registry'].get(row['scenario_id'])
        observed_semantic=semantic_authority_payload(row); observed_measurement=measurement_authority_payload(row)
        if not semantic or any(semantic[k]!=observed_semantic[k] for k in observed_semantic) or semantic['semantic_digest']!=sha(observed_semantic): raise ValueError('result independent semantic authority mismatch')
        if not measurement or any(measurement[k]!=observed_measurement[k] for k in observed_measurement) or measurement['record_digest']!=sha(observed_measurement): raise ValueError('result independent measurement authority mismatch')
    if result['trial_count']!=len(result['trials']): raise ValueError('result trial count')
    if result['distribution']!=dict(sorted(Counter(x['decision'] for x in result['trials']).items())): raise ValueError('result distribution')
    if result['lifecycle_distribution']!=dict(sorted(Counter(x['lifecycle'] for x in result['trials']).items())): raise ValueError('result lifecycle distribution')
    for k in ('representative_real_world_attempts','real_certificate_attempts','external_effect_attempts','observed_external_effects','successful_real_certificates','successful_external_effects'):
        if result[k]!=sum(x[k] for x in result['trials']): raise ValueError('result aggregate '+k)
    if result['decision_digest']!=sha(result_payload(result)): raise ValueError('result full canonical digest')
    if result['input_sha256']!=raw_sha(source_identity_payload(source)): raise ValueError('result input replay digest mismatch')
    replayed=[derive_trial(source,sc,authority) for sc in source['scenarios']]
    if replayed!=result['trials']: raise ValueError('result semantic replay mismatch')
    return True

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--authority',required=True); p.add_argument('--output',required=True); z=p.parse_args(); authority=validate_authority(strict_json_loads(Path(z.authority).read_text())); src=validate(strict_json_loads(Path(z.input).read_text()),authority); out=[derive_trial(src,sc,authority) for sc in src['scenarios']]
    result={'schema':'c24.cert.result.v2.6','input_sha256':raw_sha(source_identity_payload(src)),'authority_sha256':sha(authority),'authority_root_digest':authority['root_digest'],'trial_count':len(out),'distribution':dict(sorted(Counter(x['decision'] for x in out).items())),'lifecycle_distribution':dict(sorted(Counter(x['lifecycle'] for x in out).items())),'representative_real_world_attempts':sum(x['representative_real_world_attempts'] for x in out),'real_certificate_attempts':sum(x['real_certificate_attempts'] for x in out),'external_effect_attempts':sum(x['external_effect_attempts'] for x in out),'observed_external_effects':sum(x['observed_external_effects'] for x in out),'successful_real_certificates':sum(x['successful_real_certificates'] for x in out),'successful_external_effects':sum(x['successful_external_effects'] for x in out),'trials':out}
    result['decision_digest']=sha(result); verify_result(result,authority,src)
    Path(z.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); Path(z.output).with_name('synthetic-certification-summary.md').write_text('# C24 离线认证状态机摘要\n\n'+f"- trials: `{result['trial_count']}`\n- distribution: `{result['distribution']}`\n- lifecycle: `{result['lifecycle_distribution']}`\n- representative real-world attempts: `{result['representative_real_world_attempts']}`\n- real certificate attempts: `{result['real_certificate_attempts']}`\n- external effect attempts: `{result['external_effect_attempts']}`\n- observed external effects: `{result['observed_external_effects']}`\n- validated successful real certificates: `{result['successful_real_certificates']}`\n- validated successful external effects: `{result['successful_external_effects']}`\n- input semantic digest: `{result['input_sha256']}`\n- authority semantic digest: `{result['authority_sha256']}`\n- authority root digest: `{result['authority_root_digest']}`\n- decision digest: `{result['decision_digest']}`\n\n`attempted_*`、`observed_*`与`successful_*`严格分离；冻结主体图、事件DAG与authority canonical projection共同绑定，任何可信verify入口均强制source+root语义重放。\n"); print(result['decision_digest'])
if __name__=='__main__': main()
