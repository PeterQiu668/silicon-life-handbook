#!/usr/bin/env python3
"""Fresh-process verifier for three raw JSON documents and an authorized pin."""
import argparse, hashlib, importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
TRUSTED_RUNNER_SHA256="bbc3de6cebd20e4ad97d1519b38f4449aaa38a6442e4c0a5d9e9d519190d6053"
RUNNER=HERE/"run-case-harness.py"
if hashlib.sha256(RUNNER.read_bytes()).hexdigest()!=TRUSTED_RUNNER_SHA256:
    raise RuntimeError("verifier: runner code digest differs from the trusted release")
spec=importlib.util.spec_from_file_location("c23runner",RUNNER)
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--result",required=True); p.add_argument("--authority-root",required=True); p.add_argument("--input",required=True); p.add_argument("--pin-id",default="PIN.C23.CURRENT"); a=p.parse_args()
    result=Path(a.result); root=Path(a.authority_root); source=Path(a.input)
    r.verify_raw_documents(result,root,source,pin_id=a.pin_id)
    parsed=r.strict_json_loads(result.read_bytes())
    print(parsed["decision_digest"])

if __name__=="__main__": main()
