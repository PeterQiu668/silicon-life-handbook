#!/usr/bin/env python3
"""C23 v3.0 regression for a transitively frozen trusted evaluator graph."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, subprocess, tempfile
from collections import Counter
from pathlib import Path

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    for flag in ("input","authority-root","result","runner","verifier","output"): p.add_argument("--"+flag,required=True)
    a=p.parse_args(); runner=Path(a.runner); verifier=Path(a.verifier); r=load(runner,"c23_v30_author")
    source_text=Path(a.input).read_text(); root_text=Path(a.authority_root).read_text(); result_text=Path(a.result).read_text()
    source=r.strict_json_loads(source_text); root=r.strict_json_loads(root_text); result=r.strict_json_loads(result_text); r.verify_raw_documents(result_text,root_text,source_text)
    attacks=[]; controls=[]; boundaries=[]
    def resign(candidate):
        candidate["distribution"]=dict(sorted(Counter(x["derived"]["verdict"] for x in candidate["trials"]).items())); candidate["accepted_real_claim_count"]=sum(x["derived"]["accepted_real_claim_count"] for x in candidate["trials"]); candidate["external_effect_count"]=sum(x["derived"]["external_effect_count"] for x in candidate["trials"]); candidate["decision_digest"]=r.digest({k:v for k,v in candidate.items() if k!="decision_digest"})
    forged=copy.deepcopy(result); frow=next(x for x in forged["trials"] if x["derived"]["verdict"]=="FAIL"); frow["derived"].update(verdict="PASS",reasons=[]); resign(forged); forged_text=json.dumps(forged,ensure_ascii=False,sort_keys=True)
    rr=copy.deepcopy(result); rrrow=next(x for x in rr["trials"] if x["derived"]["verdict"]=="REVIEW_REQUIRED"); rrrow["derived"].update(verdict="PASS",reasons=[]); resign(rr); rr_text=json.dumps(rr,ensure_ascii=False,sort_keys=True)
    def trio(build):
        s=copy.deepcopy(source); s["suite"]["build_id"]=build; q=copy.deepcopy(root); q["suite_manifest"]["build_id"]=build; q["root_digest"]=r.digest(r.root_payload(q)); z=r.evaluate(copy.deepcopy(s),copy.deepcopy(q)); return tuple(json.dumps(x,ensure_ascii=False,sort_keys=True) for x in (s,q,z))
    unauthorized=trio("BUILD.C23.20261001.V30.UNAUTHORIZED"); repin=trio("BUILD.C23.20261001.V29.REPIN")
    def patch(name,value,fn):
        marker=object(); old=getattr(r,name,marker); setattr(r,name,value)
        try: return fn()
        finally:
            if old is marker: delattr(r,name)
            else: setattr(r,name,old)
    def patch_attr(obj,name,value,fn):
        old=getattr(obj,name); setattr(obj,name,value)
        try: return fn()
        finally: setattr(obj,name,old)
    def attack(test_id,family,fn):
        observed="ACCEPTED"; message=""
        try: fn()
        except Exception as exc: observed="REJECT"; message=f"{type(exc).__name__}: {exc}"
        attacks.append({"test_id":test_id,"family":family,"observed":observed,"expected":"REJECT","passed":observed=="REJECT","escape":observed!="REJECT","message":message})
    def boundary(test_id,fn):
        observed="REJECT"; message=""
        try: fn(); observed="ACCEPTED"
        except Exception as exc: message=f"{type(exc).__name__}: {exc}"
        boundaries.append({"test_id":test_id,"scope":"out_of_scope_arbitrary_same_process","observed":observed,"message":message})
    def control(test_id,family,fn):
        observed="PASS"; message=""
        try: fn()
        except Exception as exc: observed="REJECT"; message=f"{type(exc).__name__}: {exc}"
        controls.append({"test_id":test_id,"family":family,"observed":observed,"expected":"PASS","passed":observed=="PASS","message":message})
    def cli(result_path=a.result,root_path=a.authority_root,input_path=a.input,pin="PIN.C23.CURRENT"):
        proc=subprocess.run(["python3",str(verifier),"--result",str(result_path),"--authority-root",str(root_path),"--input",str(input_path),"--pin-id",pin],capture_output=True,text=True)
        if proc.returncode: raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    original_canonical=r.canonical
    def result_constant(value):
        if isinstance(value,dict) and value.get("schema_version")==r.RESULT_SCHEMA and "trials" in value: return "FORGED.RESULT.EQUALITY"
        return original_canonical(value)
    # The two exact v2.9 P0 escapes.
    attack("V30-01_RESULT_ONLY_CANONICAL_FAIL","transitive-canonical",lambda:patch("canonical",result_constant,lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-02_RESULT_ONLY_CANONICAL_RR","transitive-canonical",lambda:patch("canonical",result_constant,lambda:r.verify_raw_documents(rr_text,root_text,source_text)))
    attack("V30-03_ROOT_VALIDATOR_NOOP","transitive-root",lambda:patch("validate_authority_root",lambda *_:None,lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))

    # Individual and combined transitive dependency rebinding.
    attack("V30-04_DIGEST_CONSTANT","transitive-dependency",lambda:patch("digest",lambda *_:"0"*64,lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-05_ROOT_PAYLOAD_FORGED","transitive-dependency",lambda:patch("root_payload",lambda *_:{},lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    attack("V30-06_EXACT_NOOP","transitive-dependency",lambda:patch("exact",lambda *_:None,lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-07_SHA_NOOP","transitive-dependency",lambda:patch("sha",lambda *_:None,lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    attack("V30-08_VALIDATE_DOCUMENT_FAKE","transitive-dependency",lambda:patch("validate_document",lambda *_:{},lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-09_VALIDATE_RECORD_NOOP","transitive-dependency",lambda:patch("validate_record",lambda *_:None,lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-10_INDEX_RECORDS_EMPTY","transitive-dependency",lambda:patch("index_records",lambda *_:{},lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-11_DT_CONSTANT","transitive-dependency",lambda:patch("dt",lambda *_:r.datetime.max.replace(tzinfo=r.datetime.now().astimezone().tzinfo),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-12_PUBLIC_EVALUATOR_FORGED","captured-evaluator",lambda:patch("evaluate",lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-13_PRIVATE_EVALUATOR_FORGED","captured-evaluator",lambda:patch("_evaluate_with_pin",lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-14_PUBLIC_PARSER_PERMISSIVE","captured-parser",lambda:patch("strict_json_loads",json.loads,lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-15_JSON_DUMPS_RESULT_CONSTANT","captured-canonical",lambda:patch_attr(r.json,"dumps",lambda *_a,**_k:"FORGED.RESULT.EQUALITY",lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-16_HASHLIB_SHA256_FAKE","captured-digest",lambda:patch_attr(r.hashlib,"sha256",lambda *_:type("H",(),{"hexdigest":lambda _s:"0"*64})(),lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    attack("V30-17_SCHEMA_GLOBALS_FORGED","captured-constants",lambda:patch("RESULT_SCHEMA","FORGED",lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V30-18_PIN_READER_FORGED","captured-pin",lambda:patch("_read_pin_registry",lambda:(("PIN.C23.CURRENT",r.strict_json_loads(unauthorized[1])["root_digest"]),),lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    attack("V30-19_PIN_ROWS_NAME_INVENTED","captured-pin",lambda:patch("_CAPTURED_PIN_ROWS",(("PIN.C23.CURRENT",r.strict_json_loads(unauthorized[1])["root_digest"]),),lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0])))
    attack("V30-20_CANONICAL_PLUS_ROOT_VALIDATOR","combined",lambda:patch("canonical",result_constant,lambda:patch("validate_authority_root",lambda *_:None,lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0]))))
    attack("V30-21_DIGEST_PLUS_EXACT","combined",lambda:patch("digest",lambda *_:"0"*64,lambda:patch("exact",lambda *_:None,lambda:r.verify_raw_documents(forged_text,root_text,source_text))))
    saved=r.verify_raw_documents
    attack("V30-22_SAVED_CORE_AFTER_PUBLIC_REBIND","old-core",lambda:patch("verify_raw_documents",lambda *_a,**_k:True,lambda:saved(forged_text,root_text,source_text)))
    fresh=load(runner,"c23_v30_reload")
    attack("V30-23_FRESH_RELOAD_FORGED","reload",lambda:fresh.verify_raw_documents(forged_text,root_text,source_text))
    attack("V30-24_UNAUTHORIZED_CURRENT_PIN","pin",lambda:r.verify_raw_documents(unauthorized[2],unauthorized[1],unauthorized[0]))
    attack("V30-25_WRONG_AUTHORIZED_PIN","pin",lambda:r.verify_raw_documents(result_text,root_text,source_text,pin_id="PIN.C23.V29.REPIN"))

    with tempfile.TemporaryDirectory(prefix="c23-v30-") as td:
        td=Path(td); fr=td/"forged.json"; fr.write_text(forged_text); rs=td/"repin-source.json"; rq=td/"repin-root.json"; rz=td/"repin-result.json"; rs.write_text(repin[0]); rq.write_text(repin[1]); rz.write_text(repin[2])
        attack("V30-26_CLI_FORGED","fresh-cli",lambda:cli(fr))
        control("V30-C01_RAW_TEXT","positive",lambda:r.verify_raw_documents(result_text,root_text,source_text))
        control("V30-C02_RAW_BYTES","positive",lambda:r.verify_raw_documents(result_text.encode(),root_text.encode(),source_text.encode()))
        control("V30-C03_RAW_PATH","positive",lambda:r.verify_raw_documents(Path(a.result),Path(a.authority_root),Path(a.input)))
        control("V30-C04_FRESH_CLI","positive",lambda:cli())
        control("V30-C05_REPIN_RAW","authorized-repin",lambda:r.verify_raw_documents(repin[2],repin[1],repin[0],pin_id="PIN.C23.V29.REPIN"))
        control("V30-C06_REPIN_CLI","authorized-repin",lambda:cli(rz,rq,rs,"PIN.C23.V29.REPIN"))
        control("V30-C07_GLOBALS_PATCHED_LEGAL","positive",lambda:patch("canonical",lambda *_:"BROKEN",lambda:patch("validate_authority_root",lambda *_:None,lambda:r.verify_raw_documents(result_text,root_text,source_text))))

    # Direct closure-cell writes are recorded as an explicit non-goal.
    freevars=dict(zip(r.verify_raw_documents.__code__.co_freevars,r.verify_raw_documents.__closure__ or ()))
    def mutate_cell(name,value,fn):
        cell=freevars[name]; old=cell.cell_contents; cell.cell_contents=value
        try: return fn()
        finally: cell.cell_contents=old
    boundary("V30-B01_DIRECT_CANONICAL_CELL",lambda:mutate_cell("canonical_fn",lambda *_:"EQUAL",lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    boundary("V30-B02_DIRECT_EVALUATOR_CELL",lambda:mutate_cell("evaluator_fn",lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))

    escapes=[x for x in attacks if x["escape"]]
    payload={"schema_version":"c23.v3.0.author-remediation-regression.v1","attack_count":len(attacks),"secure_attack_count":len(attacks)-len(escapes),"escape_count":len(escapes),"escape_ids":[x["test_id"] for x in escapes],"positive_control_count":len(controls),"positive_control_pass_count":sum(x["passed"] for x in controls),"boundary_demonstration_count":len(boundaries),"boundary_accept_count":sum(x["observed"]=="ACCEPTED" for x in boundaries),"baseline_distribution":result["distribution"],"baseline_decision_digest":result["decision_digest"],"runner_sha256":sha(a.runner),"verifier_sha256":sha(a.verifier),"pin_registry_sha256":sha(runner.parent/"frozen-pin-registry.json"),"attacks":attacks,"positive_controls":controls,"boundary_demonstrations":boundaries,"limits":{"ordinary_module_global_rebinding":"covered","direct_closure_cell_mutation":"out_of_scope_demonstrated","real_practice":"REVIEW_REQUIRED"}}
    payload["suite_digest"]=r.digest([(x["test_id"],x["observed"],x["message"],x.get("passed")) for x in attacks+controls+boundaries])
    Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:payload[k] for k in ("attack_count","secure_attack_count","escape_count","positive_control_count","positive_control_pass_count","boundary_accept_count","suite_digest")},ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"]==len(controls) else 1

if __name__=="__main__": raise SystemExit(main())
