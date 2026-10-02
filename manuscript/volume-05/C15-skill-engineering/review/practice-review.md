---
review_id: C12-independent-practice-review-20260930
chapter_id: C12
review_type: independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
fresh_copy_reproduction: PASS
author_fixture_distribution: PASS
x_c12_01: REVIEW_REQUIRED
x_c12_02: REVIEW_REQUIRED
p0_05: REVIEW_REQUIRED
p0_06: REVIEW_REQUIRED
p0_07: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
fact_gate: not_reviewed
cross_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C12 独立实践门

## 1. 裁决

**作者离线 harness 的确定性路由结果已由非作者在两个 fresh temp 中逐字节复现：20 个 trial、13 PASS、5 FAIL、2 REVIEW_REQUIRED，三个案例与五类场景齐全，UNKNOWN 正确进入 REVIEW_REQUIRED，五个硬失败没有被十三个 PASS 抵消。这个结果只使“作者固定 fixture 可复现”通过；两项练习和 C12 总实践门仍为 `REVIEW_REQUIRED`。**

阻断原因不是脚本不能运行，而是它没有执行练习所要求的 Skill/Plugin/Registry 状态：`observed`、权限、撤回、旧 Session 与供应链风险主要由输入预置，runner 再做规则路由；没有 `task_id`、D22 四数据层、横切 safety/red-team、真实文件/资源扫描、依赖解析、Plugin 生命周期、撤回传播或替代部署。因此不得把清单写过、字段存在或 13/5/2 分布等同于练习跑通。

结构化证据见 [independent-practice-reproduction-20260930.yaml](runs/independent-practice-reproduction-20260930.yaml)。本评审没有修改正文、账本、母产物、练习、作者 input/runner/result/summary 或 C12 既有交叉审校，也不批准事实门、交叉门、编辑门、总编门或 RC。

## 2. 独立性与安全范围

- 本评审者不是 C12 作者，没有参与作者 harness 或两项练习的创建。
- 两次原样复跑只复制 runner 和 input 到不同 fresh temp；输出在临时目录检查后清理。
- 十组负向突变只发生在第三组临时副本；没有修改作者文件。
- 脚本只读取固定 JSON/YAML 输入并写 result/summary；没有 network、subprocess、installer、package manager、真实 secret、Plugin、Registry、Gateway 或生产副作用。
- “环境字段写 network=deny / exec=fixed-validator-only”是 fixture 声明，不是 OS sandbox 证明；本轮能确认的是 runner 代码本身没有网络或 exec 路径。

## 3. 双 fresh-temp 原样复跑

| 项目 | RUN-A | RUN-B | 裁决 |
| --- | --- | --- | --- |
| fresh 目录 | `c12-practice-a.ezOPxH` | `c12-practice-b.6WZdWa` | 不同目录，检查后均已清理 |
| 退出码 | 0 | 0 | PASS |
| stdout / stderr | 空 / 空 | 空 / 空 | PASS |
| runner SHA-256 | `5bbac6bf…cddd` | `5bbac6bf…cddd` | 等于作者 runner |
| input 原始 SHA-256 | `1468088d…401d` | `1468088d…401d` | 等于作者 input |
| result SHA-256 | `850f80df…5cf` | `850f80df…5cf` | 两次一致，等于作者结果 |
| summary SHA-256 | `73d69ab9…8cc1` | `73d69ab9…8cc1` | 两次一致，等于作者摘要 |
| 解析后结果 | 相同 | 相同 | PASS |

输入原始字节哈希为 `1468088d…401d`；结果内部 `input_sha256=2d4a1f4f…6c70` 是解析后对象的规范化哈希。两者度量对象不同，不能混用。

## 4. 记录完整性与分布

| 检查 | 实际 | 裁决 |
| --- | --- | --- |
| trial 数量 | 20 | PASS |
| trial ID | S01—S20，20/20 唯一 | PASS |
| task ID | 全部缺失 | REVIEW_REQUIRED |
| task/trial 配对 | 无法建立 | REVIEW_REQUIRED |
| CASE-A/B/C | 6 / 6 / 8 | PASS |
| 五类场景 | normal 3、boundary 3、exception 3、adversarial 8、recovery 3 | PASS |
| 门禁分布 | 13 PASS、5 FAIL、2 REVIEW_REQUIRED | PASS |
| UNKNOWN | S17、S18 均映射 REVIEW_REQUIRED | PASS |
| 硬失败 | S06、S08、S09、S11、S15 始终保留 | PASS |

五个 FAIL 分别保留了权限扩张并执行、恶意签名包激活、未锁依赖激活、程序性 Memory 自发布、撤回版在旧 Session 执行。安全隔离、拒绝或撤回按预期判 PASS 是正确语义，但这些结论只来自冻结 fixture 的路由，不是外部环境读回。

## 5. D22 数据层与横切安全

作者 input/result 没有 `data_layer`、dataset revision、访问历史或污染字段。唯一 `held_out` 是 S16 的 `phase` 名称；`adversarial` 是场景枚举。它们不能建立以下规范结构：

1. `training`；
2. `regression`；
3. `holdout`；
4. `representative real-world`；
5. 横跨四层、不可补偿的 security/red-team suite/slice。

因此当前 run 无法证明训练/留出隔离、留出未暴露、污染后结论失效或安全切片跨层执行。负向突变给 S16 加上 `holdout_contaminated=true` 和训练者访问字段后仍判 PASS，确认 runner 没有污染门。D22 实践接口为 `REVIEW_REQUIRED`。

## 6. 预置字段路由与状态化执行的区别

runner 的 `decide()` 实际只消费以下决策字段：

- trial：`expected`、`observed`、`runtime_permission_granted`、`self_publish`、`old_session_active`、`revoked_digest_loaded`、`evidence_complete`；
- release：`dependency_locked`、`malicious_entry`、`malicious_resource`、`malicious_script`。

以下 release 字段虽然被复制进输出，却不参与裁决：`digest`、`source_fixed`、`owner`、`manifest_valid`、`permission_delta`、`signed`、`provenance`、`sbom_complete`。脚本也没有读取 Skill 文件、递归资源、manifest、SBOM、签名、依赖图、Registry、Session、Worker、cache 或 Plugin 目录。

因此：

- `expected != observed` 可以正确保留预置终态冲突；
- 若若干硬布尔被置真，runner 可以正确保持 FAIL；
- 但它没有生成 `observed`，没有证明输入里的观察真实发生；
- phase 名称如 `shadow`、`signature`、`plugin_init`、`replacement`、`held_out`、`propagation_receipts` 只是标签，不会自动执行对应机制。

## 7. 攻击面代码级覆盖

| 攻击面 | 当前证据 | 实际等级 | 裁决 |
| --- | --- | --- | --- |
| 同名抢占 | S13 的 precedence 与 effective_hash_match 是预置字符串 | 路由标签 | REVIEW_REQUIRED |
| Unicode 混淆抢占 | 无标准化、confusable 或 namespace 代码 | 缺失 | REVIEW_REQUIRED |
| 深层 resource 注入 | `malicious_resource` 布尔仅在 `observed=active` 时触发 | 布尔标记，无递归资源图/内容扫描 | REVIEW_REQUIRED |
| 未声明 network/path/secret | 无行为字段、临时根、canary、egress 或 secret broker | 缺失 | REVIEW_REQUIRED |
| 浮动依赖 | `dependency_locked=false` 仅在 active 时触发 | 布尔标记 | REVIEW_REQUIRED |
| typosquatting | 无包名规范化、来源解析或依赖 resolver | 缺失 | REVIEW_REQUIRED |
| manifest 低报 | `manifest_valid`、`permission_delta` 不参与 decide | 仅输出快照 | REVIEW_REQUIRED |
| 更新扩权 | S06 预置 permission granted/executed | 终态布尔路由，无 old/new capability diff | REVIEW_REQUIRED |
| 训练/留出污染 | 无数据层和访问历史 | 缺失 | REVIEW_REQUIRED |
| 旧 Session 复活 | S15 的两个布尔被硬门捕获 | 预置布尔路由，无 Session 状态机 | REVIEW_REQUIRED |
| Worker/cache 复活 | 无字段或执行路径 | 缺失 | REVIEW_REQUIRED |
| Plugin 卸载残余 | 无 registry/process/config/grant/data 扫描 | 缺失 | REVIEW_REQUIRED |
| 程序性 Memory 自发布 | S11 `self_publish=true` 形成独立硬门 | 可复现的布尔硬门 | PASS，仅限规则控制 |
| Plugin 初始化隔离 | S10 `isolated→isolated` | 预置 expected/observed，无故障进程 | REVIEW_REQUIRED |
| 签名/provenance/SBOM | 字段存在但不参与裁决，也未调用验证器 | 快照展示 | REVIEW_REQUIRED |

清单和章节对这些风险写得完整，但实践门只认执行证据。上述 `REVIEW_REQUIRED` 不否定设计，而是拒绝把设计覆盖当成运行覆盖。

## 8. 负向突变

十组临时突变给出了两类结果。

### 8.1 确认存在的硬门

| 突变 | 结果 | 说明 |
| --- | --- | --- |
| S01 把 `self_publish` 改 true | FAIL | 自发布硬门独立生效 |
| S07 把 floating release 改成 active | FAIL | expected/observed 冲突与未锁依赖均保留 |
| S06 让 expected 与 executed 相同，仍保留 runtime permission granted | FAIL | 权限扩张硬门不依赖 expected mismatch |

### 8.2 暴露的空白路径

| 突变 | 结果 | 暴露边界 |
| --- | --- | --- |
| golden-v1 加 `malicious_resource=true`，但 observed 保持 eligible | PASS | 恶意资源只在 active 字符串下检查 |
| active replacement 改为来源未固定、manifest 无效、权限扩张、无签名/provenance/SBOM | PASS | 这些供应链字段不参与裁决 |
| S16 加留出污染和训练者访问 | PASS | 无数据污染门 |
| S19 加未声明网络、path escape、secret read | PASS | 无行为观察 |
| S20 加 Worker 活跃、cache 复活、可执行卸载残余 | PASS | 无撤回残余门 |
| S13 加 Unicode confusable 与 shadow selected | PASS | 无命名规范化或抢占解析 |
| S08 把 expected 改成 active，并移除恶意/依赖标记 | PASS | 不会独立检查 bundle 内容或行为 |

这证明 runner 不只是比较 expected/observed：少数硬布尔确实独立生效；同时也证明它不是状态化安全模拟器，许多练习要求的风险只要输入没有预置相应标记就不可见。

## 9. 停训、撤回与替代

### 停训

五个 FAIL 被保留在结果中，但 runner 在遇到硬失败后仍处理其余所有 trial，也没有输出 candidate aggregate gate、stop reason、freeze/quarantine 状态或重新准入条件。作为批量测试这并非错误，但它不能证明练习要求的停训/停止执行已经发生。

### 撤回

S14、S15、S20 分别声称新任务不可发现、旧 Session 执行失败、传播回执已撤回。三者是相互独立的输入行，没有共享 Registry revision、事件时间线、Session/Worker/cache 实体或重启验证。S15 的 FAIL 路由正确；S14/S20 的 PASS 仍只是预置观察一致。

### 替代

S12、S16、S19 分别标记 replacement、held_out 和 publish 通过，但没有相同 task/budget/risk contract、真实 regression/holdout 数据、candidate digest diff、部署目标或环境读回。不能据此证明 replacement-v3 已替代旧版。

## 10. X-C12-01 裁决

**`REVIEW_REQUIRED`。**

练习设计具备审计、影子、恶意版本、纵深防御、exact-digest 撤回、旧 Session、替代、停止和回滚要求。作者 fixture 可复现其门禁路由，并正确保留 S06/S11/S15 等硬失败。但它没有生成文件清单/digest、读取 entry/reference/script、运行正负路由、状态化撤回 Session/Worker/cache，也没有真实回归/留出/红队数据。X-C12-01 尚未达到完整可执行证据门。

## 11. X-C12-02 裁决

**`REVIEW_REQUIRED`。**

练习要求禁用态安装、注册面、初始化故障隔离、更新 capability diff、签名与语义分离、可变依赖/同名覆盖、SBOM/漏洞、disable/quarantine/uninstall residual 和 fixed-digest replacement。当前 runner 不创建 Plugin 实体、不运行初始化、不比较注册面、不验证签名/SBOM、不执行卸载或残余扫描。S08/S09 的失败只是 malicious/dependency 布尔加预置 active；S10 的隔离只是预置字符串。X-C12-02 不能以当前作者包判 PASS。

## 12. P0-05 / P0-06 / P0-07

| P0 | 裁决 | 已通过 | 未关闭 |
| --- | --- | --- | --- |
| P0-05 可执行、可停止、可回滚 | REVIEW_REQUIRED | runner 可执行、双复现；失败和 UNKNOWN 保留 | 无状态化 stop、rollback、revoke、replace、environment read-back |
| P0-06 权限、审批、隔离 | REVIEW_REQUIRED | 权限扩张和自发布布尔硬门可复现 | 无真实 Policy/Approval/Sandbox/identity/Plugin isolation；manifest/capability diff 不执行 |
| P0-07 基线、证据、客观验收 | REVIEW_REQUIRED | 输入/输出/hash、20 trial、三案例、五场景、13/5/2 可复现 | 无 task ID、四数据层、污染审计；大量观察预置，攻击覆盖不完整 |

没有确认真实越权或生产副作用，因此总门使用 `REVIEW_REQUIRED` 而非把缺证据写成 `FAIL`。作者 fixture 内的五个确认硬失败仍保持 FAIL，不能因总体门是 REVIEW_REQUIRED 而被抹除。

## 13. 真实平台与供应链边界

本轮没有运行：

- OpenClaw 固定版本的 Skill source、Workshop/self-learning、Plugin policy 或撤回传播；
- Hermes 固定/动态实现的 Skill/Plugin 生命周期；
- Muse 内部 Skill/Connector/custom tool；
- 真实 Plugin installer、Registry、签名根、SLSA provenance、SBOM、漏洞数据库；
- 真实 Session、Node、Worker、cache、credential、network、path、secret 或外部副作用。

因此任何“平台支持”“供应链安全”“撤回完成”“替代上线”结论都必须继续是 `REVIEW_REQUIRED` 或相应事实身份，不能由这 20 条 fixture 外推。

## 14. 总实践门

```yaml
practice_gate:
  chapter_id: C12
  fresh_copy_reproduction: PASS
  author_fixture_distribution_13_5_2: PASS
  unique_trial_ids: PASS
  task_trial_pairing: REVIEW_REQUIRED
  cases_and_five_scenarios: PASS
  d22_four_layers_and_cross_cutting_safety: REVIEW_REQUIRED
  unknown_mapping: PASS
  hard_failure_non_compensation: PASS
  stateful_execution: REVIEW_REQUIRED
  x_c12_01: REVIEW_REQUIRED
  x_c12_02: REVIEW_REQUIRED
  p0_05: REVIEW_REQUIRED
  p0_06: REVIEW_REQUIRED
  p0_07: REVIEW_REQUIRED
  real_platform_and_supply_chain: NOT_RUN
  overall: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  fact_gate: NOT_REVIEWED
  cross_gate: NOT_REVIEWED
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 15. 验证记录

完成本评审后已运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
git diff --no-index --check /dev/null manuscript/volume-04/C12-skill-engineering/review/practice-review.md
git diff --no-index --check /dev/null manuscript/volume-04/C12-skill-engineering/review/runs/independent-practice-reproduction-20260930.yaml
```

验证结果：

- 本文件 frontmatter、唯一 YAML 机器块、独立复现 YAML：PASS；
- `validate-formal-manuscript.py`：PASS；全书当前只剩“尚缺 11 个章节包”的进度 warning，C12 为 18,651 个中文字符；
- `validate-book.py`：PASS；扫描 285 个 Markdown，检查 1,318 条本地链接；
- 两个新增文件的 `git diff --no-index --check`：PASS；
- 两个练习与作者 runner/input/result/summary 的最终 SHA-256 与本轮开始时完全一致；
- 两次原样复跑和负向突变临时目录已清理，无本轮临时目录残留。
