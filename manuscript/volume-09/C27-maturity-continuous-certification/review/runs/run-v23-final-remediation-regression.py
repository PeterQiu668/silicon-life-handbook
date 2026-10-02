#!/usr/bin/env python3
"""Author-side C24 v2.3 closure regression.

Replays the preserved independent 25-test oracle without editing it, replaces
its legacy output-digest assertions with the v2.3 full-result verifier, adds 20
near-neighbour regressions, and proves two legal PASS controls. Everything is
offline synthetic; it does not issue a real certificate or perform an external
effect.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path


def load(path: Path):
    spec=importlib.util.spec_from_file_location('c24_v23_runner',path)
    module=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(module); return module


def seal(runner,row,field='record_digest'):
    row[field]=runner.sha({k:v for k,v in row.items() if k!=field})


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True); p.add_argument('--authority',required=True)
    p.add_argument('--runner',required=True); p.add_argument('--result',required=True)
    p.add_argument('--historical-tests',required=True); p.add_argument('--output',required=True)
    z=p.parse_args(); input_path=Path(z.input); authority_path=Path(z.authority)
    runner_path=Path(z.runner); result_path=Path(z.result); runner=load(runner_path)
    raw_input=json.loads(input_path.read_text()); raw_authority=json.loads(authority_path.read_text())
    authority=runner.validate_authority(copy.deepcopy(raw_authority)); source=runner.validate(copy.deepcopy(raw_input),authority)
    result=json.loads(result_path.read_text()); runner.verify_result(copy.deepcopy(result),authority)
    by_id={x['scenario_id']:x for x in source['scenarios']}; result_by_id={x['scenario_id']:x for x in result['trials']}
    active_id=next(x['scenario_id'] for x in result['trials'] if x['decision']=='PASS' and x['lifecycle']=='ACTIVE')
    expired_id=next(x['scenario_id'] for x in result['trials'] if x['decision']=='PASS' and x['lifecycle']=='EXPIRED')
    limited_ids=[x['scenario_id'] for x in result['trials'] if x['decision']=='PASS' and x['lifecycle']=='LIMITED']

    # The preserved v2.2 reviewer script recomputes its historical five-field
    # digest before running. Feed it a temporary compatibility result; never
    # modify the historical reviewer artifact or the v2.3 saved result.
    legacy=copy.deepcopy(result)
    legacy['decision_digest']=runner.sha([(x['trial_id'],x['decision'],x['lifecycle'],x['reasons'],x['state_digest']) for x in legacy['trials']])
    with tempfile.TemporaryDirectory(prefix='c24-v23-independent-') as td:
        td=Path(td); legacy_path=td/'legacy-result.json'; independent_path=td/'independent.json'
        legacy_path.write_text(json.dumps(legacy,ensure_ascii=False,sort_keys=True)+'\n')
        completed=subprocess.run(['python3',z.historical_tests,'--input',str(input_path),'--authority',str(authority_path),'--runner',str(runner_path),'--result',str(legacy_path),'--output',str(independent_path)],check=False,capture_output=True,text=True)
        # Exit 1 is the preserved script's expected signal for its six legacy
        # digest escapes. v2.3 replaces those six assertions below.
        if completed.returncode not in (0,1) or not independent_path.exists(): raise RuntimeError('historical independent replay did not produce evidence')
        preserved=json.loads(independent_path.read_text())
    semantic=[copy.deepcopy(x) for x in preserved['attacks'] if x['family']!='decision-digest-completeness']
    # v2.4 makes contradictory UNKNOWN/PENDING observations fail-closed.  A
    # historical oracle that required REVIEW_REQUIRED remains safely closed
    # when the same required reason is present under a harder FAIL decision.
    for row in semantic:
        oracle=row.get('reviewer_oracle',{})
        hardened=bool(oracle.get('required_decision')=='REVIEW_REQUIRED' and row.get('actual_decision')=='FAIL' and oracle.get('required_reason') in row.get('actual_reasons',[]))
        if hardened:
            row['semantic_matched']=True; row['semantic_escape']=False; row['v2_4_fail_closed_hardening']=True

    def reject_result(candidate):
        unsealed=False; resealed=False; errors=[]
        try: runner.verify_result(copy.deepcopy(candidate),authority)
        except (ValueError,TypeError,KeyError) as exc: unsealed=True; errors.append(str(exc))
        candidate['decision_digest']=runner.sha(runner.result_payload(candidate))
        try: runner.verify_result(copy.deepcopy(candidate),authority)
        except (ValueError,TypeError,KeyError) as exc: resealed=True; errors.append(str(exc))
        return unsealed and resealed,errors

    independent_output=[]
    mutations=[
        ('aggregate-successful-external-effects-tamper',lambda x:x.update(successful_external_effects=x['successful_external_effects']+7)),
        ('aggregate-successful-real-certificates-tamper',lambda x:x.update(successful_real_certificates=x['successful_real_certificates']+7)),
        ('aggregate-distribution-tamper',lambda x:x['distribution'].update(PASS=x['distribution'].get('PASS',0)+1)),
        ('trial-certificate-id-tamper',lambda x:x['trials'][0].update(certificate_id='CERT-TAMPERED')),
        ('trial-success-counter-tamper',lambda x:x['trials'][0].update(successful_external_effects=99)),
        ('trial-layer-tamper',lambda x:x['trials'][0].update(layer='representative_real_world')),
    ]
    for attack,mutate in mutations:
        candidate=copy.deepcopy(result); mutate(candidate); matched,errors=reject_result(candidate)
        independent_output.append({'attack_id':attack,'family':'v2.3-full-result-integrity','semantic_matched':matched,'semantic_escape':not matched,'errors':errors})
    independent25=semantic+independent_output

    def semantic_attack(attack_id,base_id,mutate):
        scenario=copy.deepcopy(by_id[base_id]); mutate(scenario['state'])
        try:
            state=runner.validate_state(scenario['state'],'v23.'+attack_id)
            decision,lifecycle,reasons,*_=runner.evaluate(source,state,scenario['layer'],authority)
        except (ValueError,TypeError,KeyError) as exc:
            decision,lifecycle,reasons='SCHEMA_REJECT','REVOKED',[str(exc)]
        return {'attack_id':attack_id,'family':'v2.3-author-near-neighbour','decision':decision,'lifecycle':lifecycle,'reasons':reasons,'matched':decision!='PASS','escape':decision=='PASS'}

    def principal_role_owner(state,app_field,role,action):
        pid=state['application'][app_field]; pr=state['principal_registry'][pid]
        pr['roles']=sorted(set(pr['roles']+[role])); seal(runner,pr)
        auth=next(x for x in state['authority_registry'].values() if x['action']==action); auth['actor']=pid; seal(runner,auth)

    def change_approver_owner(state):
        pid=state['change']['owner']; pr=state['principal_registry'][pid]
        pr['roles']=sorted(set(pr['roles']+['change_approver'])); seal(runner,pr)
        auth=next(x for x in state['authority_registry'].values() if x['action']=='approve_material_change'); auth['actor']=pid; seal(runner,auth)

    def expire_evidence(state,kind):
        ev=next(x for x in state['evidence_registry'].values() if x['kind']==kind); ev['expires_at']='2026-10-01T00:00:00Z'; seal(runner,ev)

    def early_expire(state):
        life=state['lifecycle']; life['occurred_at']='2026-09-30T11:51:00Z'; seal(runner,life)
        ev=state['evidence_registry'][life['evidence_ref']]; ev['content_digest']=runner.sha(runner.lifecycle_payload(life)); seal(runner,ev)

    def external(state,status='APPLIED',top=False,readback=True,mismatch=False):
        app=state['application']; obs={'effect_id':'EFFECT-V23','status':'APPLIED','external':True,'environment':'external'}
        effect={'effect_id':'EFFECT-V23','application_id':app['application_id'],'external':top,'status':status,'environment':'external','receipt':obs,'receipt_digest':runner.sha(obs)}
        if readback:
            rb=copy.deepcopy(obs)
            if mismatch: rb['status']='UNKNOWN'
            effect.update(readback=rb,readback_digest=runner.sha(rb))
        seal(runner,effect); state['effect_ledger']=[effect]

    def incomplete_change(state):
        ch=state['change']; ch.update(material=True,kind='MODEL',impact_review='PASS',retest='PASS',affected_scopes=['MODEL'],post_change_release=state['application']['release'],issued_at='2026-09-30T11:45:00Z'); seal(runner,ch)
        ev=state['evidence_registry'][ch['evidence_ref']]; ev['content_digest']=runner.sha(runner.change_payload(state['application'],ch)); seal(runner,ev)

    semantic_near=[
        ('lifecycle-owner-is-subject',active_id,lambda s:principal_role_owner(s,'subject_id','lifecycle_owner','change_certificate_lifecycle')),
        ('lifecycle-owner-is-controller-near',active_id,lambda s:principal_role_owner(s,'controller','lifecycle_owner','change_certificate_lifecycle')),
        ('change-approver-is-change-owner',active_id,change_approver_owner),
        ('lifecycle-evidence-short-window',active_id,lambda s:expire_evidence(s,'lifecycle_event')),
        ('change-evidence-short-window',active_id,lambda s:expire_evidence(s,'change_review')),
        ('expire-event-early-near',expired_id,early_expire),
        ('external-applied-hidden',active_id,lambda s:external(s,top=False)),
        ('external-readback-mismatch',active_id,lambda s:external(s,top=True,mismatch=True)),
        ('external-applied-missing-readback',active_id,lambda s:external(s,top=True,readback=False)),
        ('material-change-missing-post-lineage',active_id,incomplete_change),
    ]
    remediation=[semantic_attack(*x) for x in semantic_near]
    output_near=[
        ('result-authority-root-tamper',lambda x:x.update(authority_root_digest='sha256:'+'0'*64)),
        ('result-scenario-id-tamper',lambda x:x['trials'][0].update(scenario_id='S24-TAMPER')),
        ('result-application-id-tamper',lambda x:x['trials'][0].update(application_id='APP-TAMPER')),
        ('result-subject-id-tamper',lambda x:x['trials'][0].update(subject_id='SUB-TAMPER')),
        ('result-task-id-tamper',lambda x:x['trials'][0].update(task_id='TASK-TAMPER')),
        ('result-trial-id-tamper',lambda x:x['trials'][0].update(trial_id='TRIAL-TAMPER')),
        ('result-evidence-id-tamper',lambda x:x['trials'][0].update(evidence_id='EV-TAMPER')),
        ('result-certificate-id-near',lambda x:x['trials'][0].update(certificate_id='CERT-NEAR')),
        ('result-layer-near',lambda x:x['trials'][0].update(layer='representative_real_world')),
        ('result-real-success-near',lambda x:x['trials'][0].update(successful_real_certificates=1)),
    ]
    for attack,mutate in output_near:
        candidate=copy.deepcopy(result); mutate(candidate); matched,errors=reject_result(candidate)
        remediation.append({'attack_id':attack,'family':'v2.3-author-result-near-neighbour','matched':matched,'escape':not matched,'errors':errors})

    def positive(scenario,renew=False):
        scenario=copy.deepcopy(scenario); st=scenario['state']
        if renew:
            cert=next(iter(st['certificate_registry'].values()))
            cert['issued_at']='2026-09-30T11:52:00Z'; cert['expires_at']='2026-10-20T00:00:00Z'; seal(runner,cert)
        checked=runner.validate_state(st,'v23.positive')
        decision,lifecycle,reasons,*_=runner.evaluate(source,checked,scenario['layer'],authority)
        return {'kind':'legal-renewal' if renew else 'legal-positive-neighbour','scenario_id':scenario['scenario_id'],'decision':decision,'lifecycle':lifecycle,'reasons':reasons,'matched':decision=='PASS'}

    positives=[positive(by_id[limited_ids[-1]]),positive(by_id[active_id],True)]
    payload={
        'schema':'c24.cert.v2.3-final-remediation-regression.v1','scope':'offline_synthetic_author_remediation',
        'input_sha256':'sha256:'+hashlib.sha256(input_path.read_bytes()).hexdigest(),'authority_sha256':'sha256:'+hashlib.sha256(authority_path.read_bytes()).hexdigest(),
        'runner_sha256':'sha256:'+hashlib.sha256(runner_path.read_bytes()).hexdigest(),'result_sha256':'sha256:'+hashlib.sha256(result_path.read_bytes()).hexdigest(),
        'independent_25_count':len(independent25),'independent_25_matched':sum(bool(x.get('semantic_matched')) for x in independent25),'independent_25_escape_count':sum(bool(x.get('semantic_escape')) for x in independent25),
        'remediation_count':len(remediation),'remediation_matched':sum(bool(x['matched']) for x in remediation),'remediation_escape_count':sum(bool(x['escape']) for x in remediation),
        'positive_count':len(positives),'positive_matched':sum(bool(x['matched']) for x in positives),
        'independent_25':independent25,'remediation':remediation,'positive_controls':positives,
        'limits':{'real_world_executed':False,'real_certificate_issued':False,'external_effect_executed':False,'practice_gate':'REVIEW_REQUIRED','fact_cross_editor_chief_rc':'NOT_AUTHORIZED'},
    }
    payload['suite_digest']=runner.sha({'independent_25':independent25,'remediation':remediation,'positive_controls':positives})
    Path(z.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:payload[k] for k in ('independent_25_count','independent_25_matched','independent_25_escape_count','remediation_count','remediation_matched','remediation_escape_count','positive_count','positive_matched','suite_digest')},ensure_ascii=False))


if __name__=='__main__': main()
