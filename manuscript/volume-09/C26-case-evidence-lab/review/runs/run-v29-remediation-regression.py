#!/usr/bin/env python3
"""C23 v2.9 raw-document, captured-verifier and fresh-CLI regression."""
from __future__ import annotations

import argparse, copy, hashlib, importlib.util, json, shutil, subprocess, tempfile
from collections import Counter
from pathlib import Path

def load(path: Path, name: str):
    spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec)
    assert spec.loader; spec.loader.exec_module(module); return module

def file_sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    for flag in ("input","authority-root","result","runner","verifier","output"): p.add_argument("--"+flag,required=True)
    a=p.parse_args(); runner=Path(a.runner); verifier=Path(a.verifier); r=load(runner,"c23_v29_author")
    source_text=Path(a.input).read_text(); root_text=Path(a.authority_root).read_text(); result_text=Path(a.result).read_text()
    source=r.strict_json_loads(source_text); root=r.strict_json_loads(root_text); result=r.strict_json_loads(result_text)
    r.verify_raw_documents(result_text,root_text,source_text)
    attacks=[]; controls=[]

    def resign(candidate):
        candidate["distribution"]=dict(sorted(Counter(x["derived"]["verdict"] for x in candidate["trials"]).items()))
        candidate["accepted_real_claim_count"]=sum(x["derived"]["accepted_real_claim_count"] for x in candidate["trials"])
        candidate["external_effect_count"]=sum(x["derived"]["external_effect_count"] for x in candidate["trials"])
        candidate["decision_digest"]=r.digest({k:v for k,v in candidate.items() if k!="decision_digest"})
    forged=copy.deepcopy(result); row=next(x for x in forged["trials"] if x["derived"]["verdict"]=="FAIL"); row["derived"].update(verdict="PASS",reasons=[]); resign(forged)
    forged_text=json.dumps(forged,ensure_ascii=False,sort_keys=True)
    def equivalent_trio(build_id):
        candidate_source=copy.deepcopy(source); candidate_source["suite"]["build_id"]=build_id
        candidate_root=copy.deepcopy(root); candidate_root["suite_manifest"]["build_id"]=build_id
        candidate_root["root_digest"]=r.digest(r.root_payload(candidate_root))
        candidate_result=r.evaluate(copy.deepcopy(candidate_source),copy.deepcopy(candidate_root))
        return tuple(json.dumps(x,ensure_ascii=False,sort_keys=True) for x in (candidate_source,candidate_root,candidate_result))
    unauthorized_source_text,unauthorized_root_text,unauthorized_result_text=equivalent_trio("BUILD.C23.20261001.V29.UNAUTHORIZED")

    def attack(test_id,family,fn):
        observed="ACCEPTED"; message=""
        try: fn()
        except Exception as exc: observed="REJECT"; message=f"{type(exc).__name__}: {exc}"
        attacks.append({"test_id":test_id,"family":family,"observed":observed,"expected":"REJECT","passed":observed=="REJECT","message":message})
    def control(test_id,family,fn):
        observed="PASS"; message=""
        try: fn()
        except Exception as exc: observed="REJECT"; message=f"{type(exc).__name__}: {exc}"
        controls.append({"test_id":test_id,"family":family,"observed":observed,"expected":"PASS","passed":observed=="PASS","message":message})
    def cli(result_path=a.result,root_path=a.authority_root,input_path=a.input,pin_id="PIN.C23.CURRENT",verifier_path=verifier):
        proc=subprocess.run(["python3",str(verifier_path),"--result",str(result_path),"--authority-root",str(root_path),"--input",str(input_path),"--pin-id",pin_id],capture_output=True,text=True)
        if proc.returncode: raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])

    # Lost serialization provenance is never accepted by the trusted entry.
    attack("V29-01_PARSED_RESULT_DICT","raw-only",lambda:r.verify_raw_documents(result,root_text,source_text))
    attack("V29-02_PARSED_ROOT_DICT","raw-only",lambda:r.verify_raw_documents(result_text,root,source_text))
    attack("V29-03_PARSED_SOURCE_DICT","raw-only",lambda:r.verify_raw_documents(result_text,root_text,source))
    attack("V29-04_ALL_PARSED_OBJECTS","raw-only",lambda:r.verify_raw_documents(result,root,source))
    attack("V29-05_OLD_OBJECT_API_ABSENT","retired-api",lambda:getattr(r,"verify_result")(result,root,source))
    attack("V29-06_PERMISSIVE_ALIAS_ABSENT","parser-surface",lambda:getattr(r,"_ORIGINAL_JSON_LOADS")(result_text))

    duplicate_result=result_text.replace('"verdict": "FAIL"','"verdict": "PASS",\n        "verdict": "FAIL"',1)
    duplicate_source=source_text.replace('"schema_version": "c23.case.input.v2.7"','"schema_version": "FORGED",\n  "schema_version": "c23.case.input.v2.7"',1)
    duplicate_root=root_text.replace('"root_digest":','"root_digest": "'+'0'*64+'",\n  "root_digest":',1)
    attack("V29-07_RAW_RESULT_DUPLICATE","duplicate-json",lambda:r.verify_raw_documents(duplicate_result,root_text,source_text))
    attack("V29-08_RAW_SOURCE_DUPLICATE","duplicate-json",lambda:r.verify_raw_documents(result_text,root_text,duplicate_source))
    attack("V29-09_RAW_ROOT_DUPLICATE","duplicate-json",lambda:r.verify_raw_documents(result_text,duplicate_root,source_text))

    # Captured references ignore simple module-global rebinding.
    def patched(name,value,fn):
        marker=object(); old=getattr(r,name,marker); setattr(r,name,value)
        try: return fn()
        finally:
            if old is marker: delattr(r,name)
            else: setattr(r,name,old)
    attack("V29-10_MONKEYPATCH_PUBLIC_EVALUATE","captured-core",lambda:patched("evaluate",lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V29-11_MONKEYPATCH_INTERNAL_EVALUATOR","captured-core",lambda:patched("_evaluate_with_pin",lambda *_:copy.deepcopy(forged),lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V29-12_MONKEYPATCH_STRICT_PARSER","captured-core",lambda:patched("strict_json_loads",json.loads,lambda:r.verify_raw_documents(duplicate_result,root_text,source_text)))
    attack("V29-13_MONKEYPATCH_PIN_DIGEST","captured-core",lambda:patched("PIN_REGISTRY_SHA256","PENDING",lambda:r.verify_raw_documents(forged_text,root_text,source_text)))
    attack("V29-14_INVENT_PIN_GLOBAL_PENDING","captured-core",lambda:patched("PINNED_AUTHORITY_ROOT_DIGEST","PENDING",lambda:r.verify_raw_documents(unauthorized_result_text,unauthorized_root_text,unauthorized_source_text)))
    saved=r.verify_raw_documents
    attack("V29-15_REBIND_PUBLIC_VERIFIER_SAVED_CORE","captured-core",lambda:patched("verify_raw_documents",lambda *_a,**_k:True,lambda:saved(forged_text,root_text,source_text)))

    attack("V29-16_PIN_PENDING","pin-authority",lambda:r.verify_raw_documents(result_text,root_text,source_text,pin_id="PENDING"))
    attack("V29-17_PIN_EMPTY","pin-authority",lambda:r.verify_raw_documents(result_text,root_text,source_text,pin_id=""))
    attack("V29-18_PIN_UNKNOWN","pin-authority",lambda:r.verify_raw_documents(result_text,root_text,source_text,pin_id="PIN.C23.UNAUTHORIZED"))
    attack("V29-19_WRONG_AUTHORIZED_PIN_FOR_CURRENT_ROOT","pin-authority",lambda:r.verify_raw_documents(result_text,root_text,source_text,pin_id="PIN.C23.V29.REPIN"))
    attack("V29-20_FORGED_RESULT_RESEALED","semantic-replay",lambda:r.verify_raw_documents(forged_text,root_text,source_text))
    changed_source=copy.deepcopy(source); changed_source["suite"]["build_id"]="BUILD.C23.FORGED"; changed_source_text=json.dumps(changed_source)
    attack("V29-21_SOURCE_CHANGED_ROOT_STALE","semantic-replay",lambda:r.verify_raw_documents(result_text,root_text,changed_source_text))

    with tempfile.TemporaryDirectory(prefix="c23-v29-author-") as td:
        td=Path(td)
        forged_path=td/"forged.json"; forged_path.write_text(forged_text)
        dup_result_path=td/"dup-result.json"; dup_result_path.write_text(duplicate_result)
        dup_source_path=td/"dup-source.json"; dup_source_path.write_text(duplicate_source)
        dup_root_path=td/"dup-root.json"; dup_root_path.write_text(duplicate_root)
        attack("V29-22_CLI_FORGED_RESULT","fresh-cli",lambda:cli(forged_path))
        attack("V29-23_CLI_DUP_RESULT","fresh-cli",lambda:cli(dup_result_path))
        attack("V29-24_CLI_DUP_SOURCE","fresh-cli",lambda:cli(input_path=dup_source_path))
        attack("V29-25_CLI_DUP_ROOT","fresh-cli",lambda:cli(root_path=dup_root_path))
        def cli_missing_source():
            proc=subprocess.run(["python3",str(verifier),"--result",a.result,"--authority-root",a.authority_root],capture_output=True,text=True)
            if proc.returncode: raise ValueError((proc.stderr or proc.stdout).strip().splitlines()[-1])
        attack("V29-26_CLI_MISSING_SOURCE","fresh-cli",cli_missing_source)
        def tampered_release():
            for name in ("verify-case-result.py","run-case-harness.py","frozen-pin-registry.json"):
                shutil.copy(verifier.parent/name,td/name)
            with (td/"run-case-harness.py").open("a") as f: f.write("\n# tampered\n")
            cli(verifier_path=td/"verify-case-result.py")
        attack("V29-27_CLI_RUNNER_DIGEST_TAMPER","code-digest",tampered_release)
        def caller_monkeypatch_cannot_cross_process():
            old=r.evaluate; r.evaluate=lambda *_:copy.deepcopy(forged)
            try: cli(forged_path)
            finally: r.evaluate=old
        attack("V29-28_CALLER_PATCH_CANNOT_CROSS_PROCESS","fresh-cli",caller_monkeypatch_cannot_cross_process)
        fresh=load(runner,"c23_v29_reload")
        attack("V29-29_FRESH_RELOAD_FORGED_RESULT","reload",lambda:fresh.verify_raw_documents(forged_text,root_text,source_text))
        attack("V29-30_RAW_TRAILING_DOCUMENT","parser-surface",lambda:r.verify_raw_documents(result_text+"{}",root_text,source_text))

        # Deterministic, authority-pre-registered repin positive.
        repin_source_text,repin_root_text,repin_result_text=equivalent_trio("BUILD.C23.20261001.V29.REPIN")
        rp_source=td/"repin-source.json"; rp_root=td/"repin-root.json"; rp_result=td/"repin-result.json"
        rp_source.write_text(repin_source_text); rp_root.write_text(repin_root_text); rp_result.write_text(repin_result_text)

        control("V29-C01_RAW_TEXT","raw-positive",lambda:r.verify_raw_documents(result_text,root_text,source_text))
        control("V29-C02_RAW_BYTES","raw-positive",lambda:r.verify_raw_documents(result_text.encode(),root_text.encode(),source_text.encode()))
        control("V29-C03_PATH_OBJECTS","raw-positive",lambda:r.verify_raw_documents(Path(a.result),Path(a.authority_root),Path(a.input)))
        control("V29-C04_FRESH_CLI","fresh-cli",lambda:cli())
        control("V29-C05_EQUIVALENT_FORMATTING","normalization",lambda:r.verify_raw_documents(json.dumps(result,ensure_ascii=True,indent=7),json.dumps(root,ensure_ascii=True,indent=5),json.dumps(source,ensure_ascii=True,indent=3)))
        control("V29-C06_AUTHORIZED_REPIN_RAW","authorized-repin",lambda:r.verify_raw_documents(repin_result_text,repin_root_text,repin_source_text,pin_id="PIN.C23.V29.REPIN"))
        control("V29-C07_AUTHORIZED_REPIN_CLI","authorized-repin",lambda:cli(rp_result,rp_root,rp_source,"PIN.C23.V29.REPIN"))
        control("V29-C08_GLOBAL_PATCH_LEGITIMATE_STILL_VERIFIES","captured-core",lambda:patched("evaluate",lambda *_:forged,lambda:r.verify_raw_documents(result_text,root_text,source_text)))

    escapes=[x for x in attacks if not x["passed"]]
    payload={"schema_version":"c23.v2.9.author-remediation-regression.v1","attack_count":len(attacks),"secure_attack_count":len(attacks)-len(escapes),"escape_count":len(escapes),"escape_ids":[x["test_id"] for x in escapes],"positive_control_count":len(controls),"positive_control_pass_count":sum(x["passed"] for x in controls),"baseline_distribution":result["distribution"],"baseline_decision_digest":result["decision_digest"],"input_sha256":file_sha(a.input),"authority_root_sha256":file_sha(a.authority_root),"result_sha256":file_sha(a.result),"runner_sha256":file_sha(a.runner),"verifier_sha256":file_sha(a.verifier),"pin_registry_sha256":file_sha(runner.parent/"frozen-pin-registry.json"),"attacks":attacks,"positive_controls":controls,"limits":{"trust_boundary":"fixed code digests plus fresh subprocess CLI","arbitrary_same_process_code_execution":"out_of_scope","real_case_executed":False,"real_runtime_migration_executed":False,"practice_gate":"REVIEW_REQUIRED"}}
    payload["suite_digest"]=r.digest([(x["test_id"],x["observed"],x["message"],x["passed"]) for x in attacks+controls])
    Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:payload[k] for k in ("attack_count","secure_attack_count","escape_count","positive_control_count","positive_control_pass_count","suite_digest")},ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"]==len(controls) else 1

if __name__=="__main__": raise SystemExit(main())
