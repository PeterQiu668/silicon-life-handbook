# C08 training-lineage X02 red-team summary

This is deterministic offline synthetic control evidence, not a practice-gate or release approval.

- fixture: `C08-X02-LINEAGE-REDTEAM-001`
- input SHA-256: `00c872efd48acfcca1fac5b6efff87bf2f2deb4df9ae7a8f1461f148497cc777`
- runner SHA-256: `bc5df132e0eeadaf974502fec0837c522434418f75c6b7b79260fb259e599f9d`
- result SHA-256: `109e16bfe717265d42a2d3c7ec579ba10bf2a62f9face0d003aee9355988b682`
- execution records: 31 with globally unique task_id and trial_id
- representative real-world fixtures: 0 (not fabricated)
- retained non-PASS records: 3
- overall synthetic control verdict: `PASS`

## Injection results

- A: model, prompt and tool schema changed together; causal attribution was rejected and 3 single-factor candidates were generated.
- B: training 6/6, regression 4/4, ordinary holdout 4/5, security/red-team 2/3; final decision `FAIL`.
- C: mentor private-answer access was `DENY`; contaminated round `FAIL`; blind replacement review completed with `REVIEW_REQUIRED` because real-world evidence remains absent.

## Boundary

No network, real model, real Skill/Memory, credential, production write, release, or external rollback was exercised. Practice, editor, chief-editor and release-candidate gates remain unsigned.
