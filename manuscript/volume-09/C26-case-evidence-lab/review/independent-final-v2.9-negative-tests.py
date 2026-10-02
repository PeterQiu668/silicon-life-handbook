#!/usr/bin/env python3
"""Non-author final attacks for the C23 v2.9 raw verifier boundary."""
from __future__ import annotations
import argparse, copy, functools, hashlib, importlib.util, inspect, json, shutil, subprocess, tempfile
from collections import Counter
from pathlib import Path

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def fsha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    for flag in ('input','authority-root','result','runner','verifier','output'): p.add_argument('--'+flag,required=True)
    a=p.parse_args(); runner=Path(a.runner); verifier=Path(a.verifier); r=load(runner,'c23_v29_independent')
    source_text=Path(a.input).read_text(); root_text=Path(a.authority_root).read_text(); result_text=Path(a.result).read_text()
    source=r.strict_json_loads(source_text); root=r.strict_json_loads(root_text); result=r.strict_json_loads(result_text); r.verify_raw_documents(result_text,root_text,source_text)
    attacks=[]; controls=[]; boundary=[]
    def resign(candidate):
        candidate['distribution']=dict(sorted(Counter(x['derived']['verdict'] for x in candidate['trials']).items())); candidate['accepted_real_claim_count']=sum(x['derived']['accepted_real_claim_count'] for x in candidate['trials']); candidate['external_effect_count']=sum(x['derived']['external_effect_count'] for x in candidate['trials']); candidate['decision_digest']=r.digest({k:v for k,v in candidate.items() if k!='decision_digest'})
    forged=copy.deepcopy(result); failrow=next(x for x in forged['trials'] if x['derived']['verdict']=='FAIL'); failrow['derived'].update(verdict='PASS',reasons=[]); resign(forged); forged_text=json.dumps(forged,ensure_ascii=False,sort_keys=True)
    rrforged=copy.deepcopy(result); rrrow=next(x for x in rrforged['trials'] if x['derived']['verdict']=='REVIEW_REQUIRED'); rrrow['derived'].update(verdict='PASS',reasons=[]); resign(rrforged); rr_text=json.dumps(rrforged,ensure_ascii=False,sort_keys=True)
    def trio(build):
        s=copy.deepcopy(source); s['suite']['build_id']=build; q=copy.deepcopy(root); q['suite_manifest']['build_id']=build; q['root_digest']=r.digest(r.root_payload(q)); z=r.evaluate(copy.deepcopy(s),copy.deepcopy(q)); return tuple(json.dumps(x,ensure_ascii=False,sort_keys=True) for x in (s,q,z))
    unauthorized=trio('BUILD.C23.20261001.INDEPENDENT.UNAUTHORIZED'); repin=trio('BUILD.C23.20261001.V29.REPIN')
    def run_case(test_id,family,fn,scope='in_scope'):
        observed='ACCEPTED'; message=''
        try: fn()
        except Exception as exc: observed='REJECT'; message=f'{type(exc).__name__}: {exc}'
        row={'test_id':test_id,'family':family,'scope':scope,'observed':observed,'expected':'REJECT','secure':observed=='REJECT','escape':observed!='REJECT','message':message}
        (boundary if scope!='in_scope' else attacks).append(row)
    def control(test_id,family,fn):
        observed='PASS'; message=''
        try: fn()
        except Exception as exc: observed='REJECT'; message=f'{type(exc).__name__}: {exc}'
        controls.append({'test_id':test_id,'family':family,'observed':observed,'expected':'PASS','passed':observed=='PASS','message':message})
    def patched(name,value,fn):
        marker=object(); old=getattr(r,name,marker); setattr(r,name,value)
        try: return fn()
        finally:
            if old is marker: delattr(r,name)
            else: setattr(r,name,old)
    def cli(result_path=a.result,root_path=a.authority_root,input_path=a.input,pin='PIN.C23.CURRENT',program=verifier):
        proc=subprocess.run(['python3',str(program),'--result',str(result_path),'--authority-root',str(root_path),'--input',str(input_path),'--pin-id',pin],capture_output=True,text=True)
        if proc.returncode: raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    # Serialized provenance and strict parser.
    run_case('F01_RESULT_DICT','raw-boundary',lambda:r.verify_raw_documents(result,root_text,source_text)); run_case('F02_ROOT_DICT','raw-boundary',lambda:r.verify_raw_documents(result_text,root,source_text)); run_case('F03_SOURCE_DICT','raw-boundary',lambda:r.verify_raw_documents(result_text,root_text,source)); run_case('F04_ALL_DICT','raw-boundary',lambda:r.verify_raw_documents(result,root,source)); run_case('F05_LIST_OLD_API','raw-boundary',lambda:r.verify_raw_documents([],root_text,source_text)); run_case('F06_BYTEARRAY','raw-boundary',lambda:r.verify_raw_documents(bytearray(result_text.encode()),root_text,source_text)); run_case('F07_OLD_VERIFY_RESULT','retired-api',lambda:getattr(r,'verify_result')(result,root,source)); run_case('F08_PERMISSIVE_ALIAS','retired-parser',lambda:getattr(r,'_ORIGINAL_JSON_LOADS')(result_text))
    dup_result=result_text.replace('"verdict": "FAIL"','"verdict": "PASS",\n        "verdict": "FAIL"',1); dup_source=source_text.replace('"case_version": 1','"case_version": 2, "case_version": 1',1); dup_root=root_text.replace('"suite_id":','"suite_id": "FORGED", "suite_id":',1)
    run_case('F09_DUP_RESULT_NESTED','strict-parser',lambda:r.verify_raw_documents(dup_result,root_text,source_text)); run_case('F10_DUP_SOURCE_NESTED','strict-parser',lambda:r.verify_raw_documents(result_text,root_text,dup_source)); run_case('F11_DUP_ROOT_NESTED','strict-parser',lambda:r.verify_raw_documents(result_text,dup_root,source_text)); run_case('F12_TRAILING_RESULT','strict-parser',lambda:r.verify_raw_documents(result_text+'{}',root_text,source_text)); run_case('F13_TRAILING_SOURCE','strict-parser',lambda:r.verify_raw_documents(result_text,root_text,source_text+'[]')); run_case('F14_NAN_RESULT','strict-parser',lambda:r.verify_raw_documents(result_text.replace('"trial_count": 32','"trial_count": NaN',1),root_text,source_text)); run_case('F15_INFINITY_SOURCE','strict-parser',lambda:r.verify_raw_documents(result_text,root_text,source_text.replace('"trial_count": 3','"trial_count": Infinity',1))); run_case('F16_INVALID_UTF8','strict-parser',lambda:r.verify_raw_documents(b'\xff',root_text,source_text)); run_case('F17_STRING_PATH_IS_NOT_PATH','strict-parser',lambda:r.verify_raw_documents(str(Path(a.result)),root_text,source_text))

    # Simple module-global monkeypatches claimed to be closed by v2.9.
    run_case('F18_PATCH_PUBLIC_EVALUATE','module-global',lambda:patched('evaluate',lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    run_case('F19_PATCH_INTERNAL_EVALUATOR_NAME','module-global',lambda:patched('_evaluate_with_pin',lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    run_case('F20_PATCH_PUBLIC_PARSER','module-global',lambda:patched('strict_json_loads',json.loads,lambda:r.verify_raw_documents(dup_result,root_text,source_text)))
    run_case('F21_PATCH_PIN_DIGEST','module-global',lambda:patched('PIN_REGISTRY_SHA256','PENDING',lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    run_case('F22_PATCH_RETIRED_PIN','module-global',lambda:patched('PINNED_AUTHORITY_ROOT_DIGEST',root['root_digest'],lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    run_case('F23_PATCH_PIN_READER','module-global',lambda:patched('_read_pin_registry',lambda:[('PIN.C23.CURRENT',r.strict_json_loads(unauthorized[1])['root_digest'])],lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    original_canonical=r.canonical
    def result_only_constant(value):
        if isinstance(value,dict) and value.get('schema_version')==r.RESULT_SCHEMA and 'trials' in value: return 'C23-FORGED-EQUALITY'
        return original_canonical(value)
    run_case('F24_PATCH_TRANSITIVE_CANONICAL','module-global',lambda:patched('canonical',result_only_constant,lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    run_case('F25_PATCH_TRANSITIVE_ROOT_VALIDATOR','module-global',lambda:patched('validate_authority_root',lambda *_:None,lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    saved=r.verify_raw_documents
    run_case('F26_SAVED_CORE_AFTER_PUBLIC_REBIND','module-global',lambda:patched('verify_raw_documents',lambda *_a,**_k:True,lambda:saved(forged_text,root_text,source_text)))

    # Pin/root/registry combinations and semantic replay.
    run_case('F27_UNKNOWN_PIN','pin-registry',lambda:r.verify_raw_documents(result_text,root_text,source_text,pin_id='PIN.C23.UNKNOWN')); run_case('F28_PENDING_PIN','pin-registry',lambda:r.verify_raw_documents(result_text,root_text,source_text,pin_id='PENDING')); run_case('F29_REPIN_ID_CURRENT_ROOT','pin-registry',lambda:r.verify_raw_documents(result_text,root_text,source_text,pin_id='PIN.C23.V29.REPIN')); run_case('F30_CURRENT_ID_REPIN_ROOT','pin-registry',lambda:r.verify_raw_documents(repin[2],repin[1],repin[0],pin_id='PIN.C23.CURRENT')); run_case('F31_UNAUTHORIZED_SELF_CONSISTENT_TRIO','pin-registry',lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])); run_case('F32_FORGED_FAIL_RESEALED','semantic-replay',lambda:r.verify_raw_documents(forged_text,root_text,source_text)); run_case('F33_FORGED_RR_RESEALED','semantic-replay',lambda:r.verify_raw_documents(rr_text,root_text,source_text))

    # Direct intent replay of the five v2.8 final escapes.  The historical
    # script itself aborts because its dict verifier API was intentionally
    # retired, so these preserve the exact attack intent at the new raw API.
    run_case('H-I30_PRIVATE_PERMISSIVE_RESULT','v2.8-I30-replay',lambda:getattr(r,'_ORIGINAL_JSON_LOADS')(dup_result))
    run_case('H-I31_PRIVATE_PERMISSIVE_SOURCE','v2.8-I31-replay',lambda:getattr(r,'_ORIGINAL_JSON_LOADS')(dup_source))
    run_case('H-I32_PRIVATE_PERMISSIVE_ROOT','v2.8-I32-replay',lambda:getattr(r,'_ORIGINAL_JSON_LOADS')(dup_root))
    run_case('H-I33_MONKEYPATCH_EVALUATOR','v2.8-I33-replay',lambda:patched('evaluate',lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    run_case('H-I34_MONKEYPATCH_PIN_PENDING','v2.8-I34-replay',lambda:patched('PINNED_AUTHORITY_ROOT_DIGEST','PENDING',lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))

    with tempfile.TemporaryDirectory(prefix='c23-v29-independent-') as td:
        td=Path(td); fr=td/'forged.json'; fr.write_text(forged_text); dr=td/'dup.json'; dr.write_text(dup_result); rp_s=td/'repin-source.json'; rp_q=td/'repin-root.json'; rp_z=td/'repin-result.json'; rp_s.write_text(repin[0]); rp_q.write_text(repin[1]); rp_z.write_text(repin[2])
        run_case('F34_CLI_FORGED','fresh-cli',lambda:cli(fr)); run_case('F35_CLI_DUPLICATE','fresh-cli',lambda:cli(dr))
        def cli_missing_source():
            proc=subprocess.run(['python3',str(verifier),'--result',a.result,'--authority-root',a.authority_root],capture_output=True,text=True)
            if proc.returncode: raise ValueError('CLI missing source rejected')
        run_case('F36_CLI_MISSING_SOURCE','fresh-cli',cli_missing_source)
        def tamper_runner():
            for name in ('verify-case-result.py','run-case-harness.py','frozen-pin-registry.json'): shutil.copy(verifier.parent/name,td/name)
            with (td/'run-case-harness.py').open('a') as f: f.write('\n# independent tamper\n')
            cli(program=td/'verify-case-result.py')
        run_case('F37_CLI_RUNNER_DIGEST','fresh-cli',tamper_runner)
        def tamper_registry():
            for name in ('verify-case-result.py','run-case-harness.py','frozen-pin-registry.json'): shutil.copy(verifier.parent/name,td/name)
            data=json.loads((td/'frozen-pin-registry.json').read_text()); data['pins'][0]['authority_root_digest']=r.strict_json_loads(unauthorized[1])['root_digest']; (td/'frozen-pin-registry.json').write_text(json.dumps(data))
            cli(program=td/'verify-case-result.py')
        run_case('F38_CLI_PIN_REGISTRY_DIGEST','fresh-cli',tamper_registry)
        fresh=load(runner,'c23_v29_independent_reload'); run_case('F39_FRESH_IMPORT_FORGED','import-reload',lambda:fresh.verify_raw_documents(forged_text,root_text,source_text))
        run_case('F40_REFLECTED_LOW_ARITY','reflection',lambda:next(obj for name,obj in vars(r).items() if callable(obj) and any(t in name.lower() for t in ('verify','accept')) and _binds(obj,result_text,root_text))(result_text,root_text))

        control('P01_RAW_TEXT','raw-positive',lambda:r.verify_raw_documents(result_text,root_text,source_text)); control('P02_RAW_BYTES','raw-positive',lambda:r.verify_raw_documents(result_text.encode(),root_text.encode(),source_text.encode())); control('P03_RAW_PATH','raw-positive',lambda:r.verify_raw_documents(Path(a.result),Path(a.authority_root),Path(a.input))); control('P04_FRESH_CLI','fresh-cli',lambda:cli()); control('P05_LEGAL_REPIN_RAW','authorized-repin',lambda:r.verify_raw_documents(repin[2],repin[1],repin[0],pin_id='PIN.C23.V29.REPIN')); control('P06_LEGAL_REPIN_CLI','authorized-repin',lambda:cli(rp_z,rp_q,rp_s,'PIN.C23.V29.REPIN'))

    # Explicitly demonstrate the stated arbitrary-same-process boundary.  These
    # are reported, not counted as in-scope escapes.
    freevars=dict(zip(r.verify_raw_documents.__code__.co_freevars,r.verify_raw_documents.__closure__ or ()))
    def cell_patch(name,value,fn):
        cell=freevars[name]; old=cell.cell_contents; cell.cell_contents=value
        try: return fn()
        finally: cell.cell_contents=old
    run_case('B01_MUTATE_EVALUATOR_CELL','arbitrary-same-process',lambda:cell_patch('evaluator_fn',lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)),scope='out_of_scope_demonstration')
    run_case('B02_MUTATE_PIN_CELL','arbitrary-same-process',lambda:cell_patch('captured_pins',(('PIN.C23.CURRENT',r.strict_json_loads(unauthorized[1])['root_digest']),),lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])),scope='out_of_scope_demonstration')

    escapes=[x for x in attacks if x['escape']]; payload={'schema_version':'c23.v2.9-independent-final.v1','role':'non_author','attack_count':len(attacks),'secure_attack_count':len(attacks)-len(escapes),'escape_count':len(escapes),'escape_ids':[x['test_id'] for x in escapes],'boundary_demonstration_count':len(boundary),'boundary_accept_count':sum(x['observed']=='ACCEPTED' for x in boundary),'positive_control_count':len(controls),'positive_control_pass_count':sum(x['passed'] for x in controls),'baseline_distribution':result['distribution'],'baseline_decision_digest':result['decision_digest'],'input_sha256':fsha(a.input),'root_sha256':fsha(a.authority_root),'result_sha256':fsha(a.result),'runner_sha256':fsha(a.runner),'verifier_sha256':fsha(a.verifier),'pin_registry_sha256':fsha(runner.parent/'frozen-pin-registry.json'),'attacks':attacks,'boundary_demonstrations':boundary,'positive_controls':controls,'limits':{'real_case_executed':False,'real_authorization_reviewed':False,'real_runtime_migration_executed':False,'real_external_effect_executed':False,'practice_gate':'REVIEW_REQUIRED','chief_rc':'NOT_AUTHORIZED'}}
    payload['suite_digest']=r.digest([(x['test_id'],x['observed'],x['message'],x.get('secure',x.get('passed'))) for x in attacks+boundary+controls]); Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({k:payload[k] for k in ('attack_count','secure_attack_count','escape_count','escape_ids','boundary_accept_count','positive_control_count','positive_control_pass_count','suite_digest')},ensure_ascii=False)); return 0 if not escapes and payload['positive_control_pass_count']==len(controls) else 1

def _binds(obj,*args):
    try: inspect.signature(obj).bind(*args); return True
    except (TypeError,ValueError): return False

if __name__=='__main__': raise SystemExit(main())
