#!/usr/bin/env python3
"""C23 v2.7 non-author final attacks on the alleged single replay entrypoint."""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,json,subprocess,tempfile
from collections import Counter
from pathlib import Path

def load(path):
    spec=importlib.util.spec_from_file_location('c23_v27_independent',path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def file_sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--authority-root',required=True); p.add_argument('--result',required=True); p.add_argument('--runner',required=True); p.add_argument('--verifier',required=True); p.add_argument('--output',required=True); a=p.parse_args()
    r=load(Path(a.runner)); source_text=Path(a.input).read_text(); root_text=Path(a.authority_root).read_text(); result_text=Path(a.result).read_text()
    source=r.strict_json_loads(source_text); root=r.strict_json_loads(root_text); persisted=r.strict_json_loads(result_text); r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root),copy.deepcopy(source))
    fail_row=next(x for x in persisted['trials'] if x['derived']['verdict']=='FAIL'); rr_row=next(x for x in persisted['trials'] if x['derived']['verdict']=='REVIEW_REQUIRED'); pass_row=next(x for x in persisted['trials'] if x['derived']['verdict']=='PASS')
    attacks=[]; controls=[]
    def resign(result):
        result['distribution']=dict(sorted(Counter(x['derived']['verdict'] for x in result['trials']).items())); result['accepted_real_claim_count']=sum(x['derived']['accepted_real_claim_count'] for x in result['trials']); result['external_effect_count']=sum(x['derived']['external_effect_count'] for x in result['trials']); result['decision_digest']=r.digest({k:v for k,v in result.items() if k!='decision_digest'})
    def row(result,sid): return next(x for x in result['trials'] if x['scenario_id']==sid)
    def add(test_id,family,fn,secure={'REJECT'}):
        observed='ACCEPTED'; message=''
        try: fn()
        except Exception as exc: observed='REJECT'; message=f'{type(exc).__name__}: {exc}'
        ok=observed in secure; attacks.append({'test_id':test_id,'family':family,'observed':observed,'secure_expected_outcomes':sorted(secure),'secure_contract_passed':ok,'escape':not ok,'message':message})
    def candidate_change(sid,**values):
        c=copy.deepcopy(persisted); row(c,sid)['derived'].update(values); resign(c); return c

    # The leading underscore is a Python convention, not an access-control boundary.
    add('U01_PRIVATE_ENVELOPE_ACCEPTS_FAIL_TO_PASS','entrypoint-bypass',lambda:r._verify_result_envelope(candidate_change(fail_row['scenario_id'],verdict='PASS',reasons=[]),root))
    add('U02_PRIVATE_ENVELOPE_ACCEPTS_RR_TO_PASS','entrypoint-bypass',lambda:r._verify_result_envelope(candidate_change(rr_row['scenario_id'],verdict='PASS',reasons=[]),root))
    add('U03_PUBLIC_SOURCE_ARGUMENT_OMITTED','entrypoint-arity',lambda:r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root)))
    add('U04_PUBLIC_SOURCE_NONE','entrypoint-arity',lambda:r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root),None))
    add('U05_PUBLIC_ROOT_NONE','entrypoint-arity',lambda:r.verify_result(copy.deepcopy(persisted),None,copy.deepcopy(source)))
    add('U06_PUBLIC_ROOT_SOURCE_SWAPPED','entrypoint-arity',lambda:r.verify_result(copy.deepcopy(persisted),copy.deepcopy(source),copy.deepcopy(root)))
    add('U07_PUBLIC_EMPTY_SOURCE','entrypoint-arity',lambda:r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root),{}))

    add('U08_RESULT_FAIL_TO_PASS_FULL_RESEAL','persisted-vs-replay',lambda:r.verify_result(candidate_change(fail_row['scenario_id'],verdict='PASS',reasons=[]),root,source))
    add('U09_RESULT_RR_TO_PASS_FULL_RESEAL','persisted-vs-replay',lambda:r.verify_result(candidate_change(rr_row['scenario_id'],verdict='PASS',reasons=[]),root,source))
    add('U10_RESULT_REASON_REWRITE_FULL_RESEAL','persisted-vs-replay',lambda:r.verify_result(candidate_change(fail_row['scenario_id'],reasons=['FORGED.INDEPENDENT']),root,source))
    add('U11_RESULT_COUNT_REWRITE_FULL_RESEAL','persisted-vs-replay',lambda:r.verify_result(candidate_change(pass_row['scenario_id'],external_effect_count=1),root,source))
    def reorder_result():
        c=copy.deepcopy(persisted); c['trials'][0],c['trials'][1]=c['trials'][1],c['trials'][0]; resign(c); r.verify_result(c,root,source)
    add('U12_RESULT_ORDER_REWRITE','persisted-vs-replay',reorder_result)
    def transplant_result():
        c=copy.deepcopy(persisted); c['trials'][0].update({k:c['trials'][1][k] for k in ('case_record_id','task_id','trial_id','run_id','evidence_id')}); resign(c); r.verify_result(c,root,source)
    add('U13_RESULT_IDENTITY_TRANSPLANT','combination-transplant',transplant_result)
    def provenance_result(field,value):
        c=copy.deepcopy(persisted); c['provenance'][field]=value; resign(c); r.verify_result(c,root,source)
    add('U14_RESULT_MANIFEST_DIGEST_REBOUND','combination-transplant',lambda:provenance_result('scenario_manifest_digest','0'*64))
    add('U15_RESULT_AUTHORITY_DIGEST_REBOUND','combination-transplant',lambda:provenance_result('authority_root_digest','1'*64))

    def source_mut(mut):
        d=copy.deepcopy(source); mut(d); r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root),d)
    add('U16_SOURCE_SCENARIO_REMOVED','source-transplant',lambda:source_mut(lambda d:d['scenarios'].pop()))
    add('U17_SOURCE_SCENARIOS_REORDERED','source-transplant',lambda:source_mut(lambda d:d['scenarios'].__setitem__(slice(0,2),[d['scenarios'][1],d['scenarios'][0]])))
    add('U18_SOURCE_REGISTRY_ORDER_REVERSED','source-normalization',lambda:source_mut(lambda d:d['registries']['source_registry'].reverse()))
    add('U19_SOURCE_BUILD_ID_REPLACED','source-transplant',lambda:source_mut(lambda d:d['suite'].update(build_id='BUILD.C23.FORGED')))
    def source_semantic_reseal():
        d=copy.deepcopy(source); rec=d['registries']['source_registry'][0]; rec['private_content']={'private_case':'FORGED'}; rec['private_content_digest']=r.digest(rec['private_content']); rec['record_digest']=r.digest({k:v for k,v in rec.items() if k!='record_digest'}); r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root),d)
    add('U20_SOURCE_CONTENT_RESEALED_WITH_OLD_ROOT','source-transplant',source_semantic_reseal)

    def root_mut(mut,reseal=True):
        q=copy.deepcopy(root); mut(q)
        if reseal:q['root_digest']=r.digest(r.root_payload(q))
        r.verify_result(copy.deepcopy(persisted),q,copy.deepcopy(source))
    add('U21_ROOT_REGISTRY_ORDER_REVERSED_RESEALED','root-transplant',lambda:root_mut(lambda q:q['registries']['source_registry'].reverse()))
    add('U22_ROOT_BUILD_ID_REPLACED_RESEALED','root-transplant',lambda:root_mut(lambda q:q['suite_manifest'].update(build_id='BUILD.C23.FORGED')))
    add('U23_ROOT_MANIFEST_DIGEST_REPLACED','root-transplant',lambda:root_mut(lambda q:q['suite_manifest'].update(scenario_manifest_digest='2'*64),False))

    def strict_attack(test_id,family,text,kind,needle,replacement):
        def run():
            parsed=r.strict_json_loads(text.replace(needle,replacement,1))
            if kind=='source':r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root),parsed)
            elif kind=='root':r.verify_result(copy.deepcopy(persisted),parsed,copy.deepcopy(source))
            else:r.verify_result(parsed,copy.deepcopy(root),copy.deepcopy(source))
        add(test_id,family,run)
    strict_attack('U24_SOURCE_DUPLICATE_TOP','duplicate-json',source_text,'source','{','{\n  "schema_version": "FORGED",')
    strict_attack('U25_SOURCE_DUPLICATE_NESTED','duplicate-json',source_text,'source','"case_version": 1','"case_version": 99,\n        "case_version": 1')
    strict_attack('U26_ROOT_DUPLICATE_TOP','duplicate-json',root_text,'root','{','{\n  "root_digest": "'+'0'*64+'",')
    strict_attack('U27_ROOT_DUPLICATE_NESTED','duplicate-json',root_text,'root','"status": "ACTIVE"','"status": "REVOKED",\n        "status": "ACTIVE"')
    strict_attack('U28_RESULT_DUPLICATE_TOP','duplicate-json',result_text,'result','{','{\n  "trial_count": 999,')
    strict_attack('U29_RESULT_DUPLICATE_NESTED','duplicate-json',result_text,'result','"verdict": "PASS"','"verdict": "FAIL",\n        "verdict": "PASS"')
    strict_attack('U30_SOURCE_NAN_NUMERIC','nonfinite-json',source_text,'source','"model_usd": 10','"model_usd": NaN')
    strict_attack('U31_SOURCE_INFINITY_NUMERIC','nonfinite-json',source_text,'source','"model_usd": 10','"model_usd": Infinity')

    def cli_forged():
        c=candidate_change(fail_row['scenario_id'],verdict='PASS',reasons=[])
        with tempfile.TemporaryDirectory(prefix='c23-v27-independent-cli-') as td:
            path=Path(td)/'forged.json'; path.write_text(json.dumps(c,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
            proc=subprocess.run(['python3',a.verifier,'--result',str(path),'--authority-root',a.authority_root,'--input',a.input],capture_output=True,text=True)
            if proc.returncode==0: return
            raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])
    add('U32_VERIFIER_CLI_FORGED_RESULT','cli-entrypoint',cli_forged)

    def control(test_id,fn):
        observed='PASS'; message=''
        try:fn()
        except Exception as exc:observed='REJECT'; message=f'{type(exc).__name__}: {exc}'
        controls.append({'test_id':test_id,'observed':observed,'expected':'PASS','passed':observed=='PASS','message':message})
    control('C01_PERSISTED_PUBLIC_VERIFY',lambda:r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root),copy.deepcopy(source)))
    control('C02_DETERMINISTIC_REPLAY',lambda:r.verify_result(r.evaluate(copy.deepcopy(source),copy.deepcopy(root)),copy.deepcopy(root),copy.deepcopy(source)))
    control('C03_SOURCE_WHITESPACE_KEY_ORDER_EQUIVALENT',lambda:r.verify_result(copy.deepcopy(persisted),copy.deepcopy(root),r.strict_json_loads(json.dumps(source,ensure_ascii=True,sort_keys=False,indent=7))))
    control('C04_RESULT_WHITESPACE_KEY_ORDER_EQUIVALENT',lambda:r.verify_result(r.strict_json_loads(json.dumps(persisted,ensure_ascii=True,sort_keys=False,indent=5)),copy.deepcopy(root),copy.deepcopy(source)))

    def legal_repin():
        doc,new_root=copy.deepcopy(source),copy.deepcopy(root); target=next(x for x in persisted['trials'] if x['derived']['verdict']=='PASS'); scenario=next(x for x in doc['scenarios'] if x['scenario_id']==target['scenario_id']); raw=scenario['raw_state']
        task=next(x for x in doc['registries']['task_authority_registry'] if x['task_authority_id']==raw['task_authority_ref']); spec=dict(task['task_spec']); spec['clarification']='LEGAL.INDEPENDENT.REPIN'; task['task_spec']=spec; task['task_digest']=r.digest(spec); task['record_digest']=r.digest({k:v for k,v in task.items() if k!='record_digest'})
        contract_keys=('case_record_id','case_version','task_id','run_id','side','task_authority_ref','input_authority_ref','permission_authority_ref','dataset_authority_ref','grader_authority_ref','task_digest','input_digest','risk','permissions_digest','data_digest','eval_digest','model_usd','tool_usd','compute_usd','human_minutes','human_usd','elapsed_seconds','total_usd'); budgets=[]
        for ref in (raw['baseline_budget_ref'],raw['candidate_budget_ref']):
            budget=next(x for x in doc['registries']['budget_registry'] if x['budget_id']==ref); budget['task_spec']=copy.deepcopy(spec); budget['task_digest']=task['task_digest']; budget['contract_digest']=r.digest({k:budget[k] for k in contract_keys}); budget['record_digest']=r.digest({k:v for k,v in budget.items() if k!='record_digest'}); budgets.append(budget)
        migration=next(x for x in doc['registries']['migration_registry'] if x['migration_id']==raw['migration_ref'])
        for side,budget in zip(('baseline_contract','candidate_contract'),budgets): migration[side]['task_digest']=task['task_digest']; migration[side]['budget_contract_digest']=budget['contract_digest']
        migration['record_digest']=r.digest({k:v for k,v in migration.items() if k!='record_digest'}); new_root['registries']=copy.deepcopy(doc['registries']); new_root['suite_manifest']=r.suite_manifest(doc['suite'],doc['scenarios']); new_root['root_digest']=r.digest(r.root_payload(new_root)); return doc,new_root
    def legal_repin_control():
        doc,new_root=legal_repin(); old=r.PINNED_AUTHORITY_ROOT_DIGEST
        try:r.PINNED_AUTHORITY_ROOT_DIGEST=new_root['root_digest']; result=r.evaluate(doc,new_root); r.verify_result(result,new_root,doc)
        finally:r.PINNED_AUTHORITY_ROOT_DIGEST=old
    control('C05_LEGAL_NEW_ROOT_REPIN',legal_repin_control)
    def unpinned_new_root():
        doc,new_root=legal_repin(); new_result=copy.deepcopy(persisted); new_result['authority_root_digest']=new_root['root_digest']; new_result['provenance']['authority_root_digest']=new_root['root_digest']; new_result['provenance']['scenario_manifest_digest']=new_root['suite_manifest']['scenario_manifest_digest']; resign(new_result); r.verify_result(new_result,new_root,doc)
    add('U33_COHERENT_NEW_TRIO_WITHOUT_PIN','combination-transplant',unpinned_new_root)
    def repinned_new_root_semantically_equivalent_result():
        doc,new_root=legal_repin(); old=r.PINNED_AUTHORITY_ROOT_DIGEST
        try:r.PINNED_AUTHORITY_ROOT_DIGEST=new_root['root_digest']; c=copy.deepcopy(persisted); c['authority_root_digest']=new_root['root_digest']; c['provenance']['authority_root_digest']=new_root['root_digest']; c['provenance']['scenario_manifest_digest']=new_root['suite_manifest']['scenario_manifest_digest']; resign(c); r.verify_result(c,new_root,doc)
        finally:r.PINNED_AUTHORITY_ROOT_DIGEST=old
    control('C06_LEGAL_REPIN_EQUIVALENT_RESULT_REBOUND',repinned_new_root_semantically_equivalent_result)

    escapes=[x for x in attacks if x['escape']]
    payload={'schema_version':'c23.v2.7-independent-final-negative.v1','review_role':'non_author','oracle':'public semantic replay and non-bypassable verification boundary','input_sha256':file_sha(a.input),'authority_root_sha256':file_sha(a.authority_root),'result_sha256':file_sha(a.result),'runner_sha256':file_sha(a.runner),'verifier_sha256':file_sha(a.verifier),'baseline_distribution':persisted['distribution'],'baseline_decision_digest':persisted['decision_digest'],'attack_count':len(attacks),'secure_attack_count':len(attacks)-len(escapes),'escape_count':len(escapes),'escape_ids':[x['test_id'] for x in escapes],'positive_control_count':len(controls),'positive_control_pass_count':sum(x['passed'] for x in controls),'attacks':attacks,'positive_controls':controls,'limits':{'real_case_executed':False,'real_runtime_migration_executed':False,'external_effect_executed':False,'practice_gate':'REVIEW_REQUIRED','chief_editor_rc':'NOT_AUTHORIZED'}}
    payload['suite_digest']=r.digest([(x['test_id'],x['observed'],x['message'],x['secure_contract_passed']) for x in attacks]+[(x['test_id'],x['observed'],x['message'],x['passed']) for x in controls]); Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({k:payload[k] for k in ('attack_count','secure_attack_count','escape_count','escape_ids','positive_control_count','positive_control_pass_count','suite_digest')},ensure_ascii=False)); return 0 if not escapes and payload['positive_control_pass_count']==len(controls) else 1

if __name__=='__main__': raise SystemExit(main())
