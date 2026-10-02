#!/usr/bin/env python3
"""C24 v2.5 author regression for causal, authority, D22 and result-source controls."""
from __future__ import annotations
import argparse,copy,importlib.util,json
from pathlib import Path

def load(path):
    spec=importlib.util.spec_from_file_location('c24_v25_runner',path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--authority',required=True); p.add_argument('--runner',required=True); p.add_argument('--result',required=True); p.add_argument('--output',required=True); z=p.parse_args()
    r=load(z.runner); source=r.strict_json_loads(Path(z.input).read_text()); authority=r.validate_authority(r.strict_json_loads(Path(z.authority).read_text())); source=r.validate(source,authority); saved=r.strict_json_loads(Path(z.result).read_text()); r.verify_result(saved,authority,source)
    active_id=next(x['scenario_id'] for x in saved['trials'] if x['decision']=='PASS' and x['lifecycle']=='ACTIVE'); active=next(x for x in source['scenarios'] if x['scenario_id']==active_id); revoked=authority['revoked_authority_ids'][0]
    attacks=[]; positives=[]
    def seal(x,field='record_digest'): x[field]=r.sha({k:v for k,v in x.items() if k!=field})
    def ev(state,kind): return next(x for x in state['evidence_registry'].values() if x['kind']==kind)
    def semantic(test_id,family,mutate):
        state=copy.deepcopy(active['state']); actual='PASS'; reasons=[]; msg=''
        try:
            mutate(state); state=r.validate_state(state,'v25.'+test_id); actual,_,reasons,*_=r.evaluate(source,state,active['layer'],authority)
        except (ValueError,TypeError,KeyError) as exc: actual='SCHEMA_REJECT'; reasons=[str(exc)]; msg=str(exc)
        secure=actual!='PASS'; attacks.append({'test_id':test_id,'family':family,'actual':actual,'reasons':reasons,'secure':secure,'escape':not secure,'message':msg})
    def after(row,time='2026-09-30T11:40:00Z'): row['issued_at']=time; seal(row)
    def trial_output_before(state,index=0):
        trial=sorted(state['trial_registry'].values(),key=lambda x:x['trial_id'])[index]; out=state['evidence_registry'][trial['output_ref']]; out['issued_at']='2026-09-30T11:00:01Z'; seal(out)
    semantic('V25-001','causal',lambda s:trial_output_before(s,0)); semantic('V25-002','causal',lambda s:trial_output_before(s,1)); semantic('V25-003','causal',lambda s:trial_output_before(s,2))
    semantic('V25-004','causal',lambda s:after(ev(s,'grader_preregistration'),'2026-09-30T11:20:00Z'))
    semantic('V25-005','causal',lambda s:after(ev(s,'holdout_lineage'),'2026-09-30T11:20:00Z'))
    semantic('V25-006','causal',lambda s:after(ev(s,'application_signature')))
    semantic('V25-007','causal',lambda s:after(ev(s,'artifact')))
    semantic('V25-008','causal',lambda s:after(ev(s,'manifest')))
    def maturity_after(s):
        after(s['maturity']); cert=s['certificate_registry'][s['certificate_ref']]; cert['maturity_digest']=s['maturity']['record_digest']; seal(cert)
    def namespace_after(s):
        after(s['namespace']); cert=s['certificate_registry'][s['certificate_ref']]; cert['namespace_digest']=s['namespace']['record_digest']; seal(cert)
    semantic('V25-009','causal',maturity_after); semantic('V25-010','causal',namespace_after)
    def trial_after_review(s):
        t=next(iter(s['trial_registry'].values())); t['completed_at']='2026-09-30T11:40:00Z'; seal(t); out=s['evidence_registry'][t['output_ref']]; out['issued_at']='2026-09-30T11:41:00Z'; seal(out)
    semantic('V25-011','causal',trial_after_review)
    semantic('V25-012','causal',lambda s:after(ev(s,'d21_technical')))
    semantic('V25-013','causal',lambda s:after(ev(s,'d21_delivery')))
    semantic('V25-014','causal',lambda s:after(ev(s,'d21_business_environment')))

    def shadow_revoked(s,action):
        old,row=next((k,v) for k,v in s['authority_registry'].items() if v['action']==action); del s['authority_registry'][old]; row['authority_id']=revoked; row['status']='ACTIVE'; seal(row); s['authority_registry'][revoked]=row
        if action=='issue_synthetic_assessment':
            cert=s['certificate_registry'][s['certificate_ref']]; cert['authority_ref']=revoked; cert['signer']=row['actor']; seal(cert)
        elif action=='operate_synthetic_scope': s['namespace']['authorization_ref']=revoked; seal(s['namespace']); cert=s['certificate_registry'][s['certificate_ref']]; cert['namespace_digest']=s['namespace']['record_digest']; seal(cert)
        elif action=='decide_appeal': s['appeal_registry'][s['application']['appeal_id']]['authority_ref']=revoked; seal(s['appeal_registry'][s['application']['appeal_id']])
        elif action=='change_certificate_lifecycle': s['lifecycle']['authority_ref']=revoked; seal(s['lifecycle'])
        elif action=='approve_material_change': s['change']['authority_ref']=revoked; seal(s['change'])
    for n,action in enumerate(('issue_synthetic_assessment','operate_synthetic_scope','decide_appeal','change_certificate_lifecycle','approve_material_change'),15): semantic(f'V25-{n:03d}','authority-root',lambda s,a=action:shadow_revoked(s,a))
    def shadow_field(s,action,field,value):
        row=next(v for v in s['authority_registry'].values() if v['action']==action); row[field]=value; seal(row)
    semantic('V25-020','authority-root',lambda s:shadow_field(s,'operate_synthetic_scope','scope','forged-scope'))
    semantic('V25-021','authority-root',lambda s:shadow_field(s,'change_certificate_lifecycle','status','REVOKED'))
    semantic('V25-022','authority-root',lambda s:shadow_field(s,'approve_material_change','expires_at','2026-12-31T00:00:00Z'))
    semantic('V25-023','authority-root',lambda s:shadow_field(s,'issue_synthetic_assessment','actor',s['application']['controller']))

    def full_recert(s):
        a=s['application']; ch=s['change']; change_at='2026-09-30T11:05:00Z'; entries=[]
        times=(('2026-09-30T11:20:00Z','2026-09-30T11:23:00Z'),('2026-09-30T11:21:00Z','2026-09-30T11:24:00Z'),('2026-09-30T11:22:00Z','2026-09-30T11:25:00Z'))
        for trial,(completed,issued) in zip(sorted(s['trial_registry'].values(),key=lambda x:{'training':0,'regression':1,'holdout':2}[x['layer']]),times):
            trial['completed_at']=completed; seal(trial); out=s['evidence_registry'][trial['output_ref']]; out['issued_at']=issued; seal(out); entries.append({'trial_ref':trial['trial_id'],'evidence_ref':out['evidence_id'],'layer':trial['layer'],'security_slices':['certification-redteam'],'affected_scopes':['MODEL']})
        rm={'manifest_id':'RETEST-V25','change_id':ch['change_id'],'pre_change_release':'openclaw@prechange-2026.9.5','post_change_release':a['release'],'affected_scopes':['MODEL'],'required_layers':['training','regression','holdout'],'required_security_slices':['certification-redteam'],'entries':entries}; rm['manifest_digest']=r.sha(rm)
        review_ref=next(iter(s['review_registry'])); ch.update(material=True,kind='MODEL',impact_review='PASS',retest='PASS',issued_at=change_at,affected_scopes=['MODEL'],post_change_release=a['release'],retest_trial_refs=[x['trial_ref'] for x in entries],retest_evidence_refs=[x['evidence_ref'] for x in entries],retest_review_ref=review_ref,retest_manifest=rm); seal(ch); row=s['evidence_registry'][ch['evidence_ref']]; row['content_digest']=r.sha(r.change_payload(a,ch)); seal(row)
    def reseal_change(s):
        ch=s['change']; rm=ch['retest_manifest']; rm['manifest_digest']=r.sha({k:v for k,v in rm.items() if k!='manifest_digest'}); seal(ch); row=s['evidence_registry'][ch['evidence_ref']]; row['content_digest']=r.sha(r.change_payload(s['application'],ch)); seal(row)
    def recert_mutate(s,fn): full_recert(s); fn(s); reseal_change(s)
    for ident,index in (('V25-024',0),('V25-025',1),('V25-026',2)):
        semantic(ident,'d22-safety',lambda s,i=index:recert_mutate(s,lambda x:x['change']['retest_manifest']['entries'][i].update(security_slices=[])))
    semantic('V25-027','d22-release',lambda s:recert_mutate(s,lambda x:x['change']['retest_manifest'].update(pre_change_release='forged@release')))
    semantic('V25-028','d22-policy',lambda s:recert_mutate(s,lambda x:x['change']['retest_manifest'].update(required_layers=['training'])))
    semantic('V25-029','d22-policy',lambda s:recert_mutate(s,lambda x:x['change']['retest_manifest'].update(required_security_slices=['invented-slice'])))
    def post_output_before(s):
        full_recert(s); entry=s['change']['retest_manifest']['entries'][0]; out=s['evidence_registry'][entry['evidence_ref']]; out['issued_at']='2026-09-30T11:19:00Z'; seal(out); reseal_change(s)
    semantic('V25-030','d22-causal',post_output_before)
    def post_review_before(s):
        full_recert(s); review=next(iter(s['review_registry'].values())); review['issued_at']='2026-09-30T11:21:30Z'; seal(review); reseal_change(s)
    semantic('V25-031','d22-causal',post_review_before)

    def result_attack(test_id,mutate):
        candidate=copy.deepcopy(saved); mutate(candidate); candidate['decision_digest']=r.sha(r.result_payload(candidate)); actual='ACCEPTED'; msg=''
        try:r.verify_result(candidate,authority,source)
        except (ValueError,TypeError,KeyError) as exc:actual='REJECT'; msg=str(exc)
        secure=actual=='REJECT'; attacks.append({'test_id':test_id,'family':'result-source','actual':actual,'reasons':[msg] if msg else [],'secure':secure,'escape':not secure,'message':msg})
    result_attack('V25-032',lambda x:x.update(input_sha256=''))
    result_attack('V25-033',lambda x:x.update(authority_sha256=''))
    result_attack('V25-034',lambda x:x.update(input_sha256=x['authority_sha256']))
    result_attack('V25-035',lambda x:x.update(authority_sha256=x['input_sha256']))
    result_attack('V25-036',lambda x:x.update(input_sha256='sha256:'+'0'*64))
    result_attack('V25-037',lambda x:x.update(authority_sha256='sha256:'+'1'*64))

    def positive(test_id,mutate):
        state=copy.deepcopy(active['state']); decision='ERROR'; reasons=[]
        try: mutate(state); state=r.validate_state(state,'v25.positive.'+test_id); decision,life,reasons,*_=r.evaluate(source,state,active['layer'],authority)
        except (ValueError,TypeError,KeyError) as exc: life='REVOKED'; reasons=[str(exc)]
        positives.append({'test_id':test_id,'decision':decision,'lifecycle':life,'reasons':reasons,'passed':decision=='PASS'})
    positive('P01_ACTIVE',lambda s:None)
    def renewal(s): cert=s['certificate_registry'][s['certificate_ref']]; cert['issued_at']='2026-09-30T11:52:00Z'; cert['expires_at']='2026-10-20T00:00:00Z'; seal(cert)
    positive('P02_RENEWAL',renewal); positive('P03_THREE_LAYER_RECERT',full_recert)
    payload={'schema':'c24.cert.v2.5-author-regression.v1','attack_count':len(attacks),'secure_count':sum(x['secure'] for x in attacks),'escape_count':sum(x['escape'] for x in attacks),'positive_count':len(positives),'positive_pass_count':sum(x['passed'] for x in positives),'attacks':attacks,'positive_controls':positives}
    payload['suite_digest']=r.sha({'attacks':attacks,'positive_controls':positives}); Path(z.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({k:payload[k] for k in ('attack_count','secure_count','escape_count','positive_count','positive_pass_count','suite_digest')},ensure_ascii=False)); return 0 if payload['escape_count']==0 and payload['positive_pass_count']==len(positives) else 1

if __name__=='__main__': raise SystemExit(main())
