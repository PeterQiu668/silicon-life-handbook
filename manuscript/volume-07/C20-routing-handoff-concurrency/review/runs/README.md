# C17 离线确定性夹具

本目录只使用合成任务、伪标识和内存状态，不包含真实凭证，不调用网络，不写生产系统。输入固定风险、预算、权限与版本；20 个场景各运行 3 次，保留全部 `PASS / FAIL / REVIEW_REQUIRED`。runner 从任务与授权版本、能力证据、负载/预算/数据位置、Handoff/ACK/owner CAS、writer lease、effect ledger、cancel 状态、wait-for graph、进度、必需分支、receipt read-back 与 D21 三层证据对象推导裁决，不再按预分类 fault 或调用方自报的完成布尔查表。

D22 只使用 `training / regression / holdout / representative_real_world` 四层；本包真实层显式为 0，四个未来真实层候选只作为 `holdout + synthetic_shadow`。security/red-team 是横切非补偿切片。顶层与 route/yield/handoff/writer/effect/cancel/progress/branches/receipt/d21 等控制对象执行闭世界 schema；重复 scenario/task/trial ID、缺字段、错类型、未知字段/枚举、common contract 失效、synthetic 冒充真实层或真实层证据无法解引用都会在生成结果前硬失败。

运行：

```bash
PYTHONPYCACHEPREFIX=/tmp/c17-pycache python3 run-routing-harness.py \
  --input synthetic-routing-input.yaml \
  --output synthetic-routing-results.yaml
```

连续运行两次，`decision_digest` 必须一致。路由能力引用必须解到 capability evidence registry，并绑定能力类型、任务版本、权限快照、状态和 digest。D21 的技术执行、交付可见、业务/环境验收分别引用 observed registry 记录，再与独立 authority registry 的层级、来源和对象 digest 对照，同时核验终态、权威性和状态；缺失、错配、失败或未知不得由 truthy 字符串伪造完成。`receipt=UNKNOWN` 且权威读回仍未知时不能被自动改写为成功或失败；`REVIEW_REQUIRED` 是安全的未知终态。作者试跑不构成独立实践签核。

能力证据摘要不是“格式像 SHA-256 就可信”。`capability_evidence_registry` 的观察记录必须与独立 `capability_evidence_authority` 对同一 evidence ref 的能力类型、任务版本、权限快照、状态和 `evidence_digest` 逐字段精确一致。格式合法但内容错误的观察 digest、格式合法但错误的权威 digest、权威记录缺失以及版本/权限/状态错配都会进入 `FAIL / capability_evidence_authority_mismatch`。

定向回归：

```bash
PYTHONPYCACHEPREFIX=/tmp/c17-pycache python3 run-capability-digest-regression.py \
  --input synthetic-routing-input.yaml \
  --runner run-routing-harness.py \
  --output capability-digest-regression-results.yaml
```

该回归共 14 例：精确绑定基线 1 例应 `PASS`；dummy/缺失 observed record、observed 撤销/未知/能力错配/版本错配/权限错配、错误 observed digest、错误 authority digest、缺少 authority record、authority 版本/权限/状态错配 13 例均应 `FAIL`。它保留 v3.1 独立审校的全部能力证据负测，并新增 authority/digest 定向负测；它仍是冻结合成证据控制，不替代真实能力测评、真实 Registry 或平台实践门。
