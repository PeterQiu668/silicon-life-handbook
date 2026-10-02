#!/usr/bin/env python3
"""C24 v2.6 author regressions for causal DAG, rooted principals and verifier closure."""
from __future__ import annotations
import argparse,copy,importlib.util,json
from pathlib import Path

def load(path):
    spec=importlib.util.spec_from_file_location('c24_v26_runner',path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--authority',required=True); p.add_argument('--runner',required=True); p.add_argument('--result',required=True); p.add_argument('--output',required=True); z=p.parse_args()
    r=load(z.runner); source=r.strict_json_loads(Path(z.input).read_text()); authority=r.validate_authority(r.strict_json_loads(Path(z.authority).read_text())); source=r.validate(source,authority); saved=r.strict_json_loads(Path(z.result).read_text()); r.verify_result(saved,authority,source)
    rows={x['scenario_id']:x for x in source['scenarios']}; active_id=next(x['scenario_id'] for x in saved['trials'] if x['decision']=='PASS' and x['lifecycle']=='ACTIVE'); active=rows[active_id]; bad_actor=rows['S24-004']
    attacks=[]; positives=[]
    def seal(x,field='record_digest'): x[field]=r.sha({k:v for k,v in x.items() if k!=field})
    def evidence(s,kind): return next(x for x in s['evidence_registry'].values() if x['kind']==kind)
    def event(s,kind,subject=None):
        matches=[x for x in s['event_registry'].values() if x['kind']==kind and (subject is None or x['subject_ref']==subject)]
        if len(matches)!=1: raise ValueError('event cardinality')
        return matches[0]
    def semantic(test_id,family,mutate,base=active):
        state=copy.deepcopy(base['state']); actual='PASS'; reasons=[]; message=''
        try:
            mutate(state); state=r.validate_state(state,'v26.'+test_id); actual,_,reasons,*_=r.evaluate(source,state,base['layer'],authority)
        except (ValueError,TypeError,KeyError) as exc: actual='SCHEMA_REJECT'; reasons=[str(exc)]; message=str(exc)
        secure=actual!='PASS'; attacks.append({'test_id':test_id,'family':family,'actual':actual,'reasons':reasons,'secure':secure,'escape':not secure,'message':message})
    def move_evidence(kind,when):
        def mutate(s): row=evidence(s,kind); row['issued_at']=when; seal(row)
        return mutate
    for ident,kind,when in (
        ('V26-001','artifact','2026-09-30T10:00:00Z'),('V26-002','failure_archive','2026-09-30T10:00:00Z'),('V26-003','cost_ledger','2026-09-30T10:00:00Z'),('V26-004','manifest','2026-09-30T10:00:00Z'),('V26-005','d21_technical','2026-09-30T10:00:00Z'),('V26-006','d21_delivery','2026-09-30T10:00:00Z'),('V26-007','d21_business_environment','2026-09-30T10:00:00Z'),('V26-008','change_review','2026-09-30T10:00:00Z'),('V26-009','public_claim','2026-09-30T10:00:00Z'),('V26-010','lifecycle_event','2026-09-30T10:00:00Z')):
        semantic(ident,'causal-record-binding',move_evidence(kind,when))
    def output_equal_complete(s):
        trial=sorted(s['trial_registry'].values(),key=lambda x:x['trial_id'])[0]; out=s['evidence_registry'][trial['output_ref']]; out['issued_at']=trial['completed_at']; seal(out)
    semantic('V26-011','causal-equal-time',output_equal_complete)
    def prereg_equal_input(s,kind):
        first=min(x['occurred_at'] for x in s['event_registry'].values() if x['kind']=='TRIAL_INPUT_ACCEPTED'); row=evidence(s,kind); row['issued_at']=first; seal(row)
    semantic('V26-012','causal-prerequisite',lambda s:prereg_equal_input(s,'holdout_lineage'))
    semantic('V26-013','causal-prerequisite',lambda s:prereg_equal_input(s,'grader_preregistration'))
    def dependency_equal_review(s,target):
        when=next(iter(s['review_registry'].values()))['issued_at']
        if target=='maturity':
            s['maturity']['issued_at']=when; seal(s['maturity']); cert=s['certificate_registry'][s['certificate_ref']]; cert['maturity_digest']=s['maturity']['record_digest']; seal(cert)
        elif target=='namespace':
            s['namespace']['issued_at']=when; seal(s['namespace']); cert=s['certificate_registry'][s['certificate_ref']]; cert['namespace_digest']=s['namespace']['record_digest']; seal(cert)
        else:
            row=evidence(s,target); row['issued_at']=when; seal(row)
    semantic('V26-014','causal-review',lambda s:dependency_equal_review(s,'maturity'))
    semantic('V26-015','causal-review',lambda s:dependency_equal_review(s,'namespace'))
    semantic('V26-016','causal-review',lambda s:dependency_equal_review(s,'d21_technical'))
    def alias_unknown(s): row=s['principal_registry']['CERTIFIER-004']; row['aliases'].append('UNKNOWN'); seal(row)
    def materialize_unknown(s):
        row=copy.deepcopy(s['principal_registry']['CERTIFIER-004']); row.update(principal_id='UNKNOWN',aliases=[]); seal(row); s['principal_registry']['UNKNOWN']=row; cert=s['certificate_registry'][s['certificate_ref']]; cert['signer']='UNKNOWN'; seal(cert)
    semantic('V26-017','principal-shadow',alias_unknown,bad_actor)
    semantic('V26-018','principal-shadow',materialize_unknown,bad_actor)
    def signer_value(value):
        def mutate(s): cert=s['certificate_registry'][s['certificate_ref']]; cert['signer']=value; seal(cert)
        return mutate
    semantic('V26-019','identity-normalization',signer_value('CERTIFIER-002 '))
    semantic('V26-020','identity-normalization',signer_value('ＣＥＲＴＩＦＩＥＲ-002'))
    def alias_collision(s):
        ids=sorted(s['principal_registry']); s['principal_registry'][ids[0]]['aliases']=[ids[1]]; seal(s['principal_registry'][ids[0]])
    def alias_cycle(s):
        ids=sorted(s['principal_registry'])[:2]; s['principal_registry'][ids[0]]['aliases']=[ids[1]]; s['principal_registry'][ids[1]]['aliases']=[ids[0]]; seal(s['principal_registry'][ids[0]]); seal(s['principal_registry'][ids[1]])
    semantic('V26-021','identity-collision',alias_collision)
    semantic('V26-022','identity-cycle',alias_cycle)
    def local_principal_status(s): row=s['principal_registry']['CERTIFIER-002']; row['status']='REVOKED'; seal(row)
    semantic('V26-023','principal-root',local_principal_status)
    def event_mut(kind,fn):
        def mutate(s): row=event(s,kind); fn(row); seal(row)
        return mutate
    semantic('V26-024','event-root',event_mut('ARTIFACT_RECORDED',lambda x:x.update(sequence=x['sequence']+100)))
    semantic('V26-025','event-root',event_mut('ARTIFACT_RECORDED',lambda x:x.update(predecessor_refs=[])))
    def equal_predecessor_time(row): row['occurred_at']='2026-09-30T10:26:00Z'
    semantic('V26-026','event-equal-time',event_mut('ARTIFACT_RECORDED',equal_predecessor_time))
    semantic('V26-027','event-predecessor',event_mut('ARTIFACT_RECORDED',lambda x:x.update(predecessor_refs=['EVT-UNKNOWN'])))
    semantic('V26-028','event-kind',event_mut('ARTIFACT_RECORDED',lambda x:x.update(kind='COST_RECORDED')))
    def cross_event(s):
        row=event(s,'ARTIFACT_RECORDED'); other=next(x for x in rows.values() if x is not active); row['predecessor_refs']=[next(iter(other['state']['event_registry']))]; seal(row)
    semantic('V26-029','event-cross-scenario',cross_event)

    def root_attack(test_id,family,mutate):
        candidate=copy.deepcopy(authority); accepted=False; message=''
        try:
            mutate(candidate)
            for registry in ('principal_registry','event_registry'):
                for records in candidate[registry].values():
                    for record in records.values():
                        record['projection_digest']=r.sha(record['projection']); record['root_record_digest']=r.sha({k:v for k,v in record.items() if k!='root_record_digest'})
            candidate['root_digest']=r.sha({k:v for k,v in candidate.items() if k!='root_digest'}); r.validate_authority(candidate); accepted=True
        except (ValueError,TypeError,KeyError) as exc: message=str(exc)
        attacks.append({'test_id':test_id,'family':family,'actual':'ACCEPTED' if accepted else 'REJECT','reasons':[message] if message else [],'secure':not accepted,'escape':accepted,'message':message})
    app=active['application_id']
    root_attack('V26-030','principal-root-reseal',lambda q:q['principal_registry'][app]['CERTIFIER-002']['projection'].update(status='REVOKED'))
    root_attack('V26-031','principal-root-alias-reseal',lambda q:q['principal_registry'][app]['CERTIFIER-002']['projection']['aliases'].append('UNKNOWN'))
    root_attack('V26-032','event-root-reseal',lambda q:q['event_registry'][app][next(iter(q['event_registry'][app]))]['projection'].update(sequence=999))
    root_attack('V26-033','event-root-remove',lambda q:q['event_registry'][app].pop(next(iter(q['event_registry'][app]))))

    def result_attack(test_id,family,invoke):
        accepted=False; message=''
        try: invoke(); accepted=True
        except (ValueError,TypeError,KeyError) as exc: message=str(exc)
        attacks.append({'test_id':test_id,'family':family,'actual':'ACCEPTED' if accepted else 'REJECT','reasons':[message] if message else [],'secure':not accepted,'escape':accepted,'message':message})
    result_attack('V26-034','verifier-required-root',lambda:r.verify_result(copy.deepcopy(saved)))
    result_attack('V26-035','verifier-required-root',lambda:r.verify_result(copy.deepcopy(saved),authority,None))
    result_attack('V26-036','verifier-required-root',lambda:r.verify_result(copy.deepcopy(saved),None,source))
    result_attack('V26-037','verifier-root-source-swap',lambda:r.verify_result(copy.deepcopy(saved),source,authority))
    def rewritten_result():
        candidate=copy.deepcopy(saved); row=next(x for x in candidate['trials'] if x['decision']=='FAIL'); row['decision']='PASS'; row['reasons']=[]
        from collections import Counter
        candidate['distribution']=dict(sorted(Counter(x['decision'] for x in candidate['trials']).items())); candidate['decision_digest']=r.sha(r.result_payload(candidate)); return candidate
    result_attack('V26-038','verifier-semantic-replay',lambda:r.verify_result(rewritten_result(),authority,source))
    wrong_source=copy.deepcopy(source); wrong_source['authority_ref']['root_digest']='sha256:'+'0'*64
    result_attack('V26-039','verifier-source-binding',lambda:r.verify_result(copy.deepcopy(saved),authority,wrong_source))
    other_root=copy.deepcopy(authority); other_root['bundle_id']='C24-AUTHORITY-FORGED'; other_root['root_digest']=r.sha({k:v for k,v in other_root.items() if k!='root_digest'})
    result_attack('V26-040','verifier-root-binding',lambda:r.verify_result(copy.deepcopy(saved),other_root,source))
    def parse_attack(test_id,text,kind):
        accepted=False; message=''
        try:
            value=r.strict_json_loads(text)
            if kind=='source': r.validate(value,authority)
            elif kind=='root': r.validate_authority(value)
            else: r.verify_result(value,authority,source)
            accepted=True
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as exc: message=str(exc)
        attacks.append({'test_id':test_id,'family':'duplicate-json','actual':'ACCEPTED' if accepted else 'REJECT','reasons':[message] if message else [],'secure':not accepted,'escape':accepted,'message':message})
    source_text=Path(z.input).read_text(); root_text=Path(z.authority).read_text(); result_text=Path(z.result).read_text()
    parse_attack('V26-041',source_text.replace('{','{"schema":"FORGED",',1),'source')
    parse_attack('V26-042',root_text.replace('{','{"schema":"FORGED",',1),'root')
    parse_attack('V26-043',result_text.replace('{','{"schema":"FORGED",',1),'result')

    for test_id,scenario_id in (('P01_LIMITED','S24-001'),('P02_ACTIVE','S24-002'),('P03_EXPIRED','S24-003'),('P04_SHORT_WINDOW','S24-058')):
        row=next(x for x in saved['trials'] if x['scenario_id']==scenario_id); positives.append({'test_id':test_id,'decision':row['decision'],'lifecycle':row['lifecycle'],'reasons':row['reasons'],'passed':row['decision']=='PASS'})
    payload={'schema':'c24.cert.v2.6-author-regression.v1','attack_count':len(attacks),'secure_count':sum(x['secure'] for x in attacks),'escape_count':sum(x['escape'] for x in attacks),'positive_count':len(positives),'positive_pass_count':sum(x['passed'] for x in positives),'attacks':attacks,'positive_controls':positives}
    payload['suite_digest']=r.sha({'attacks':attacks,'positive_controls':positives}); Path(z.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({k:payload[k] for k in ('attack_count','secure_count','escape_count','positive_count','positive_pass_count','suite_digest')},ensure_ascii=False)); return 0 if payload['escape_count']==0 and payload['positive_pass_count']==len(positives) else 1

if __name__=='__main__': raise SystemExit(main())
