#!/usr/bin/env python3
"""Independent C24 v2.6 final attacks; no author expected fields are trusted."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, inspect, json, subprocess, tempfile
from pathlib import Path

def load(path: Path):
    spec=importlib.util.spec_from_file_location("c24_v26_independent",path); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def file_sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--authority',required=True); p.add_argument('--runner',required=True); p.add_argument('--result',required=True); p.add_argument('--output',required=True); a=p.parse_args()
    r=load(Path(a.runner)); source_text=Path(a.input).read_text(); root_text=Path(a.authority).read_text(); result_text=Path(a.result).read_text()
    authority=r.validate_authority(r.strict_json_loads(root_text)); source=r.validate(r.strict_json_loads(source_text),authority); saved=r.strict_json_loads(result_text); r.verify_result(copy.deepcopy(saved),authority,source)
    by_id={x['scenario_id']:x for x in source['scenarios']}; active_id=next(x['scenario_id'] for x in saved['trials'] if x['decision']=='PASS' and x['lifecycle']=='ACTIVE'); active=by_id[active_id]
    attacks=[]; controls=[]
    def seal(row,field='record_digest'): row[field]=r.sha({k:v for k,v in row.items() if k!=field})
    def event(state,kind):
        rows=[x for x in state['event_registry'].values() if x['kind']==kind]
        if len(rows)!=1: raise ValueError('event cardinality '+kind)
        return rows[0]
    def evidence(state,kind): return next(x for x in state['evidence_registry'].values() if x['kind']==kind)
    def semantic(test_id,family,mutate,base=None):
        scenario=base or active; state=copy.deepcopy(scenario['state']); decision='PASS'; lifecycle='ACTIVE'; reasons=[]; message=''
        try:
            mutate(state); state=r.validate_state(state,'independent.'+test_id); decision,lifecycle,reasons,*_=r.evaluate(source,state,scenario['layer'],authority)
        except (ValueError,TypeError,KeyError,IndexError) as exc: decision='SCHEMA_REJECT'; lifecycle='REVOKED'; reasons=[str(exc)]; message=f'{type(exc).__name__}: {exc}'
        secure=decision!='PASS'; attacks.append({'test_id':test_id,'family':family,'channel':'semantic_state','actual':decision,'lifecycle':lifecycle,'reasons':reasons,'secure':secure,'escape':not secure,'message':message})
    def result_attack(test_id,family,invoke):
        accepted=False; message=''
        try: invoke(); accepted=True
        except Exception as exc: message=f'{type(exc).__name__}: {exc}'
        attacks.append({'test_id':test_id,'family':family,'channel':'result_verifier','actual':'ACCEPTED' if accepted else 'REJECT','lifecycle':'N/A','reasons':[],'secure':not accepted,'escape':accepted,'message':message})
    def mutate_event(kind,fn):
        def apply(state): row=event(state,kind); fn(row,state); seal(row)
        return apply

    # Full event-DAG attacks: deletion, branch, cycle, sequence and time binding.
    semantic('I01_EVENT_DELETE','event-dag',lambda s:s['event_registry'].pop(event(s,'ARTIFACT_RECORDED')['event_id']))
    semantic('I02_EVENT_BRANCH','event-dag',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(predecessor_refs=[event(s,'COST_RECORDED')['event_id']])))
    semantic('I03_EVENT_SELF_CYCLE','event-dag',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(predecessor_refs=[x['event_id']])))
    def two_cycle(s):
        x=event(s,'ARTIFACT_RECORDED'); y=event(s,'FAILURE_ARCHIVED'); x['predecessor_refs']=[y['event_id']]; y['predecessor_refs']=[x['event_id']]; seal(x); seal(y)
    semantic('I04_EVENT_TWO_CYCLE','event-dag',two_cycle)
    semantic('I05_SEQUENCE_GAP','event-dag',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(sequence=x['sequence']+50)))
    semantic('I06_SEQUENCE_DUPLICATE','event-dag',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(sequence=event(s,'FAILURE_ARCHIVED')['sequence'])))
    semantic('I07_EQUAL_TIMESTAMP','event-dag',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(occurred_at=event(s,'TRIAL_OUTPUT_RECORDED')['occurred_at'])))
    semantic('I08_REVERSED_TIMESTAMP','event-dag',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(occurred_at='2026-09-30T09:00:00Z')))
    semantic('I09_RECORD_EVENT_TIME_MISMATCH','event-record-binding',lambda s:(evidence(s,'artifact').update(issued_at='2026-09-30T10:31:30Z'),seal(evidence(s,'artifact'))))
    semantic('I10_MANIFEST_PREREG_AFTER_TRIAL','event-dag',mutate_event('MANIFEST_PREREGISTERED',lambda x,s:x.update(occurred_at='2026-09-30T10:01:00Z')))
    semantic('I11_PUBLIC_CLAIM_BEFORE_CERT','event-dag',mutate_event('PUBLIC_CLAIM_RECORDED',lambda x,s:x.update(occurred_at='2026-09-30T10:59:00Z')))
    semantic('I12_LIFECYCLE_BEFORE_CLAIM','event-dag',mutate_event('LIFECYCLE_OCCURRED',lambda x,s:x.update(occurred_at='2026-09-30T11:00:30Z')))
    def manifest_future_member(s):
        m=evidence(s,'manifest'); m['content_digest']=r.sha({'members':[m['evidence_id'],s['certificate_registry'][s['certificate_ref']]['public_claim_ref']]}); seal(m)
    semantic('I13_MANIFEST_PUBLIC_CLAIM_CAUSAL_RING','manifest-causality',manifest_future_member)
    other=next(x for x in source['scenarios'] if x['scenario_id']!=active_id)
    semantic('I14_CROSS_SCENARIO_PREDECESSOR','event-dag',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(predecessor_refs=[next(iter(other['state']['event_registry']))])))
    semantic('I15_EVENT_SUBJECT_SWAP','event-record-binding',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(subject_ref='EV-UNKNOWN')))
    semantic('I16_EVENT_KIND_SWAP','event-record-binding',mutate_event('ARTIFACT_RECORDED',lambda x,s:x.update(kind='COST_RECORDED')))

    # Canonical-principal, alias, role, status and time attacks.
    def alias_collision(s):
        ids=sorted(s['principal_registry']); s['principal_registry'][ids[0]]['aliases']=[ids[1]]; seal(s['principal_registry'][ids[0]])
    def alias_cycle(s):
        ids=sorted(s['principal_registry'])[:2]; s['principal_registry'][ids[0]]['aliases']=[ids[1]]; s['principal_registry'][ids[1]]['aliases']=[ids[0]]; seal(s['principal_registry'][ids[0]]); seal(s['principal_registry'][ids[1]])
    semantic('I17_ALIAS_COLLISION','principal',alias_collision); semantic('I18_ALIAS_CYCLE','principal',alias_cycle)
    def cert_signer(s,value): c=s['certificate_registry'][s['certificate_ref']]; c['signer']=value; seal(c)
    semantic('I19_UNICODE_PRINCIPAL','principal',lambda s:cert_signer(s,'ＣＥＲＴＩＦＩＥＲ-002'))
    semantic('I20_WHITESPACE_PRINCIPAL','principal',lambda s:cert_signer(s,'CERTIFIER-002 '))
    semantic('I21_UNKNOWN_PRINCIPAL','principal',lambda s:cert_signer(s,'UNKNOWN'))
    def principal_field(s,pid,field,value): row=s['principal_registry'][pid]; row[field]=value; seal(row)
    semantic('I22_REVOKED_CERTIFIER','principal',lambda s:principal_field(s,'CERTIFIER-002','status','REVOKED'))
    semantic('I23_STALE_CERTIFIER','principal',lambda s:principal_field(s,'CERTIFIER-002','expires_at','2026-09-29T00:00:00Z'))
    semantic('I24_ROLE_SHADOW_CERTIFIER','principal',lambda s:principal_field(s,'CERTIFIER-002','roles',['reviewer']))
    semantic('I25_CROSS_ROLE_ALIAS','principal',lambda s:principal_field(s,'AUTHOR-002','aliases',['REVIEWER-002']))
    def actor_alias(s):
        row=next(x for x in s['authority_registry'].values() if x['action']=='issue_synthetic_assessment'); row['actor']='CERTIFIER-ALIAS'; seal(row); principal_field(s,'CERTIFIER-002','aliases',['CERTIFIER-ALIAS'])
    semantic('I26_AUTHORITY_ACTOR_ALIAS','principal-authority',actor_alias)

    # D22 and material-change lineage attacks.
    def drop_layer(s,layer):
        ch=s['change']; ch['retest_manifest']['entries']=[x for x in ch['retest_manifest']['entries'] if x['layer']!=layer]; ch['retest_trial_refs']=[x['trial_ref'] for x in ch['retest_manifest']['entries']]; ch['retest_evidence_refs']=[x['evidence_ref'] for x in ch['retest_manifest']['entries']]; seal(ch)
    recert=by_id['S24-058']
    def policy_attack(remove_layer=None,drop_security=False,add_real=False):
        candidate=copy.deepcopy(authority); policy=candidate['d22_policy']
        if remove_layer: policy['required_layers'].remove(remove_layer)
        if drop_security: policy['required_security_slices']=[]
        if add_real: policy['required_layers'].append('representative_real_world'); policy['not_applicable_layers']=[]
        seal(policy); candidate['root_digest']=r.sha({k:v for k,v in candidate.items() if k!='root_digest'}); return candidate
    result_attack('I27_DROP_TRAINING','d22-policy-root',lambda:r.verify_result(copy.deepcopy(saved),policy_attack(remove_layer='training'),source))
    result_attack('I28_DROP_REGRESSION','d22-policy-root',lambda:r.verify_result(copy.deepcopy(saved),policy_attack(remove_layer='regression'),source))
    result_attack('I29_DROP_HOLDOUT','d22-policy-root',lambda:r.verify_result(copy.deepcopy(saved),policy_attack(remove_layer='holdout'),source))
    def drop_security(s):
        ch=s['change']; ch['retest_manifest']['required_security_slices']=[]
        for x in ch['retest_manifest']['entries']: x['security_slices']=[]
        seal(ch)
    result_attack('I30_DROP_SECURITY_SLICE','d22-policy-root',lambda:r.verify_result(copy.deepcopy(saved),policy_attack(drop_security=True),source))
    def fake_real(s):
        ch=s['change']; ch['retest_manifest']['required_layers'].append('representative_real_world'); ch['retest_manifest']['entries'][0]['layer']='representative_real_world'; seal(ch)
    result_attack('I31_REAL_WORLD_IN_OFFLINE_RECERT','d22-policy-root',lambda:r.verify_result(copy.deepcopy(saved),policy_attack(add_real=True),source))
    def output_before_change(s):
        ch=s['change']; trial=s['trial_registry'][ch['retest_trial_refs'][0]]; trial['completed_at']='2026-09-30T10:44:00Z'; seal(trial); out=s['evidence_registry'][trial['output_ref']]; out['issued_at']='2026-09-30T10:44:30Z'; seal(out)
    semantic('I32_POSTCHANGE_OUTPUT_BEFORE_CHANGE','material-change',output_before_change,recert)
    semantic('I33_WRONG_POSTCHANGE_RELEASE','material-change',lambda s:(s['change'].update(post_change_release='openclaw@forged'),seal(s['change'])),recert)
    def borrow_output(s):
        ch=s['change']; entries=ch['retest_manifest']['entries']; entries[1]['evidence_ref']=entries[0]['evidence_ref']; ch['retest_evidence_refs']=[x['evidence_ref'] for x in entries]; seal(ch)
    semantic('I34_CROSS_TRIAL_OUTPUT_BORROW','material-change',borrow_output,recert)

    # All verifier entrances must require the same result+authority+source replay.
    result_attack('I35_VERIFY_NO_ROOT','verifier',lambda:r.verify_result(copy.deepcopy(saved)))
    result_attack('I36_VERIFY_NO_SOURCE','verifier',lambda:r.verify_result(copy.deepcopy(saved),authority,None))
    result_attack('I37_VERIFY_WRONG_ROOT','verifier',lambda:r.verify_result(copy.deepcopy(saved),source,source))
    result_attack('I38_VERIFY_SWAP_ROOT_SOURCE','verifier',lambda:r.verify_result(copy.deepcopy(saved),source,authority))
    changed_source=copy.deepcopy(source); changed_source['now']='2026-09-30T11:59:59Z'
    result_attack('I39_VERIFY_CHANGED_SOURCE','verifier',lambda:r.verify_result(copy.deepcopy(saved),authority,changed_source))
    def forged_result():
        c=copy.deepcopy(saved); row=next(x for x in c['trials'] if x['decision']=='FAIL'); row['decision']='PASS'; row['reasons']=[]; c['decision_digest']=r.sha(r.result_payload(c)); return c
    result_attack('I40_VERIFY_RESEALED_FAIL_TO_PASS','verifier',lambda:r.verify_result(forged_result(),authority,source))
    wrong_root=copy.deepcopy(authority); wrong_root['bundle_id']='FORGED'; wrong_root['root_digest']=r.sha({k:v for k,v in wrong_root.items() if k!='root_digest'})
    result_attack('I41_VERIFY_RESEALED_WRONG_ROOT','verifier',lambda:r.verify_result(copy.deepcopy(saved),wrong_root,source))
    def low_arity_entry():
        for name,obj in vars(r).items():
            if callable(obj) and any(t in name.lower() for t in ('verify','accept')):
                try: inspect.signature(obj).bind(copy.deepcopy(saved),authority)
                except (TypeError,ValueError): continue
                obj(copy.deepcopy(saved),authority); return
        raise AttributeError('no low-arity acceptance callable')
    result_attack('I42_NO_PRIVATE_LOW_ARITY_ENTRY','verifier-inventory',low_arity_entry)
    def cli_missing_source():
        proc=subprocess.run(['python3',a.runner,'--input',a.input,'--output',str(Path(tempfile.gettempdir())/'c24-invalid.json')],capture_output=True,text=True)
        if proc.returncode: raise ValueError('CLI rejected missing authority')
    result_attack('I43_CLI_MISSING_AUTHORITY','verifier-cli',cli_missing_source)
    def duplicate_raw():
        hostile=result_text.replace('{','{"schema":"FORGED",',1); parsed=r.strict_json_loads(hostile); r.verify_result(parsed,authority,source)
    result_attack('I44_DUPLICATE_RESULT_KEY','strict-parser',duplicate_raw)
    def root_reseal(): r.validate_authority(wrong_root)
    result_attack('I45_ROOT_RESEAL_WITHOUT_PIN','authority-root',root_reseal)
    root_from_other=copy.deepcopy(authority); root_from_other['input_semantic_digest']='sha256:'+'0'*64
    result_attack('I46_ROOT_SOURCE_DIGEST_MISMATCH','authority-root',lambda:r.verify_result(copy.deepcopy(saved),root_from_other,source))

    # Positive controls are independent lookups of the fixed legal paths.
    for tid,sid,label in [('P01_ACTIVE','S24-002','active'),('P02_LIMITED','S24-001','limited'),('P03_EXPIRED','S24-003','expired-lifecycle'),('P04_SHORT_WINDOW','S24-058','short-certificate-window')]:
        row=next(x for x in saved['trials'] if x['scenario_id']==sid); controls.append({'test_id':tid,'kind':label,'decision':row['decision'],'lifecycle':row['lifecycle'],'passed':row['decision']=='PASS'})
    controls.append({'test_id':'P05_FULL_RESULT_REPLAY','kind':'result-authority-source-replay','decision':'PASS','lifecycle':'N/A','passed':bool(r.verify_result(copy.deepcopy(saved),authority,source))})
    escapes=[x for x in attacks if x['escape']]
    payload={'schema':'c24.v2.6-independent-final-negative.v1','role':'non_author','input_sha256':file_sha(a.input),'authority_sha256':file_sha(a.authority),'result_sha256':file_sha(a.result),'runner_sha256':file_sha(a.runner),'baseline_distribution':saved['distribution'],'baseline_lifecycle_distribution':saved['lifecycle_distribution'],'baseline_decision_digest':saved['decision_digest'],'authority_root_digest':authority['root_digest'],'attack_count':len(attacks),'secure_attack_count':len(attacks)-len(escapes),'escape_count':len(escapes),'escape_ids':[x['test_id'] for x in escapes],'positive_control_count':len(controls),'positive_control_pass_count':sum(x['passed'] for x in controls),'attacks':attacks,'positive_controls':controls,'limits':{'real_platform_executed':False,'representative_real_world_executed':False,'external_certification_authority_executed':False,'practice_gate':'REVIEW_REQUIRED','chief_editor_rc':'NOT_AUTHORIZED'}}
    payload['suite_digest']=r.sha({'attacks':attacks,'positive_controls':controls}); Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({k:payload[k] for k in ('attack_count','secure_attack_count','escape_count','positive_control_count','positive_control_pass_count','suite_digest')},ensure_ascii=False)); return 0 if not escapes and payload['positive_control_pass_count']==len(controls) else 1

if __name__=='__main__': raise SystemExit(main())
