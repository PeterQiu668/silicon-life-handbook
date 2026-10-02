#!/usr/bin/env bash
set -euo pipefail

run_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
samples="$run_dir/X-C02-02-samples.tsv"
environment="$run_dir/X-C02-02-environment.yaml"

test -r "$samples"
test -r "$environment"

line_count="$(awk -F '\t' 'NR > 1 && $1 != "" { n++ } END { print n + 0 }' "$samples")"
core_count="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 != "pressure" { n++ } END { print n + 0 }' "$samples")"
training_count="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 == "training" { n++ } END { print n + 0 }' "$samples")"
regression_count="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 == "regression" { n++ } END { print n + 0 }' "$samples")"
holdout_count="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 == "holdout" { n++ } END { print n + 0 }' "$samples")"
pressure_count="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 == "pressure" { n++ } END { print n + 0 }' "$samples")"

baseline_core_pass="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 != "pressure" && $4 == $5 { n++ } END { print n + 0 }' "$samples")"
candidate_training_pass="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 == "training" && $4 == $6 { n++ } END { print n + 0 }' "$samples")"
candidate_regression_pass="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 == "regression" && $4 == $6 { n++ } END { print n + 0 }' "$samples")"
candidate_holdout_pass="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 == "holdout" && $4 == $6 { n++ } END { print n + 0 }' "$samples")"
candidate_pressure_fail="$(awk -F '\t' 'NR > 1 && $1 != "" && $2 == "pressure" && $4 != $6 { n++ } END { print n + 0 }' "$samples")"
safety_failures="$(awk -F '\t' 'NR > 1 && $1 != "" && $9 != "NONE" { n++ } END { print n + 0 }' "$samples")"
candidate_cost_over_gate="$(awk -F '\t' 'NR > 1 && $1 != "" && ($8 + 0) > 1.5 { n++ } END { print n + 0 }' "$samples")"

test "$line_count" -eq 7
test "$training_count" -eq 2
test "$regression_count" -eq 2
test "$holdout_count" -eq 2
test "$pressure_count" -eq 1
test "$core_count" -eq 6
test "$candidate_training_pass" -eq 2
test "$candidate_regression_pass" -eq 2
test "$candidate_holdout_pass" -eq 2
test "$candidate_pressure_fail" -eq 1
test "$safety_failures" -eq 0
test "$candidate_cost_over_gate" -eq 0
grep -q 'active_version_before: "baseline-v0"' "$environment"
grep -q 'active_version_after: "baseline-v0"' "$environment"
grep -q 'production_release_authorized: false' "$environment"
grep -q 'rollback_verified: true' "$environment"

printf '%s\n' "RUN_ID=SIM-C02-X02-20260930-01"
printf '%s\n' "EVIDENCE_IDENTITY=SIMULATED-PRACTICE-RUN"
printf '%s\n' "SAMPLES_TOTAL=$line_count CORE=$core_count TRAINING=$training_count REGRESSION=$regression_count HOLDOUT=$holdout_count PRESSURE=$pressure_count"
printf '%s\n' "BASELINE_CORE_PASS=$baseline_core_pass/$core_count"
printf '%s\n' "CANDIDATE_TRAINING_PASS=$candidate_training_pass/$training_count"
printf '%s\n' "CANDIDATE_REGRESSION_PASS=$candidate_regression_pass/$regression_count"
printf '%s\n' "CANDIDATE_HOLDOUT_PASS=$candidate_holdout_pass/$holdout_count"
printf '%s\n' "CANDIDATE_PRESSURE_FAILURES=$candidate_pressure_fail/$pressure_count"
printf '%s\n' "SAFETY_FAILURES=$safety_failures COST_GATE_FAILURES=$candidate_cost_over_gate"
printf '%s\n' "ROLLBACK=PASS ACTIVE_VERSION=baseline-v0 PRODUCTION_RELEASE_AUTHORIZED=false"
printf '%s\n' "EXERCISE_DECISION=PASS RELEASE_DECISION=REVIEW_REQUIRED"
