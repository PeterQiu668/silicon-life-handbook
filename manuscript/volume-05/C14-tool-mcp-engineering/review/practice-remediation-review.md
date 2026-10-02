---
review_id: C11-independent-practice-remediation-review-20260930
chapter_id: C11
review_type: independent-practice-remediation-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
x_c11_02_offline_machine_control: PASS
machine_control_scope: frozen_20_trial_deterministic_synthetic_control
full_practice_gate: REVIEW_REQUIRED
fact_gate: separate_record
cross_gate: separate_record
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C11 状态化 MCP 红队补强独立实践复核

## 1. 裁决

**新增状态化红队 harness 在冻结的 20 条离线合成 trial 范围内通过机器控制门：两次 fresh-temp 原样复跑与补强作者保存结果逐字节一致，20 个 ID 唯一，三个案例和五类场景齐全，结果稳定为 12 PASS、7 FAIL、1 REVIEW_REQUIRED；七个 unsafe variant 的硬失败没有被十二个 PASS 抵消，清理缺证继续映射 REVIEW_REQUIRED。**

这关闭了原 [practice-review.md](practice-review.md) 所记录的“X-C11-02 缺少可执行 shadowing、rug pull、SSRF/token、stdio/path 等安全夹具”缺口，但只关闭**冻结合成机器控制**。真实 MCP Server、OAuth issuer/resource、OpenClaw 固定版、Hermes 对照 Runtime 均未运行；完整 X-C11-02 和 C11 总实践门仍为 `REVIEW_REQUIRED`。本复核不批准编辑门、总编门或 RC。

结构化证据见 [independent-stateful-mcp-redteam-reproduction-20260930.yaml](runs/independent-stateful-mcp-redteam-reproduction-20260930.yaml)。原 `practice-review.md` 是补强前快照，本轮没有改写它，也没有修改正文、账本、母产物、练习、作者基线或补强 input/runner/result/summary。

## 2. 独立性与受保护文件

- 评审者不是 C11 作者，也没有创建本次状态化补强。
- 原样复跑只把 `run-stateful-mcp-redteam.py` 与 `stateful-mcp-redteam-input.yaml` 复制到两个不同的 fresh temp；所有输出先在临时目录中检查，随后清理。
- 负向突变只发生在额外临时副本；作者输入和 runner 未改。
- 作者补强结果、摘要和补强前实践评审均以 SHA-256 固定；完成复核后再次核验这些哈希。

受保护文件哈希：

| 文件 | SHA-256 |
| --- | --- |
| `review/practice-review.md` | `3964a1a2d089d24ec75e942624061c254075d4c6007d96c974a4047d88af5943` |
| `stateful-mcp-redteam-input.yaml` 原始字节 | `65152c871e1f9ba562b8a967bcf5ca6b7e0c616d9bcdceecd9fe6524a746d2cd` |
| 解析后规范化 input | `934752256da717921db7fcc072eb632b1e17fc3a32717ac7825068b257f9fe35` |
| `run-stateful-mcp-redteam.py` | `0063314833c7aab5713bec31b68442247d09adc5bf13fa42b130d275825fa437` |
| 作者保存 result | `dcae3c2fc210f5f0ef172de39571391591788b2bde1a29ee1b1f1e94a3683cae` |
| 作者保存 summary | `1e9393041a67f17bb5413323cd121de835e0d616076db3804b2a2aa957402125` |

原始 input 哈希与结果内部的 canonical input 哈希度量对象不同，不能互换。

## 3. 两个 fresh-temp 原样复跑

| 项目 | RUN-A | RUN-B | 裁决 |
| --- | --- | --- | --- |
| fresh 目录 | `c11-stateful-a.d1kp5Q` | `c11-stateful-b.6Uny11` | 不同目录，结束后均已清理 |
| 退出码 | 0 | 0 | PASS |
| stdout / stderr | 空 / 空 | 空 / 空 | PASS |
| runner SHA-256 | `00633148…fa437` | `00633148…fa437` | 等于作者 runner |
| input 原始 SHA-256 | `65152c87…6d2cd` | `65152c87…6d2cd` | 等于作者 input |
| result SHA-256 | `dcae3c2f…3cae` | `dcae3c2f…3cae` | 两次字节一致且等于作者结果 |
| summary SHA-256 | `1e939304…2125` | `1e939304…2125` | 两次字节一致且等于作者摘要 |
| JSON/YAML 解析后语义 | 相同 | 相同 | PASS |

复跑后 `/tmp` 未发现 `c11-redteam-*` 内部临时根残留；本评审创建的三组顶层复跑/突变目录也已删除。

## 4. 20 个 trial 与门禁分布

| 检查 | 实际结果 | 裁决 |
| --- | --- | --- |
| trial 总数 | 20 | PASS |
| 唯一 ID | R01—R20，20/20 唯一 | PASS |
| 案例 | CASE-A 6、CASE-B 6、CASE-C 8 | PASS |
| 场景 | normal 1、boundary 3、adversarial 13、exception 2、recovery 1 | PASS |
| 门禁分布 | 12 PASS、7 FAIL、1 REVIEW_REQUIRED | PASS |
| PASS | R01、R02、R04、R05、R07、R08、R10、R11、R13、R15、R17、R19 | 可逐条定位 |
| FAIL | R03、R06、R09、R12、R14、R16、R18 | 七类硬失败均保留 |
| REVIEW_REQUIRED | R20 | 清理/残留不可见，不假装 PASS |

七个 FAIL 分别对应：同名工具在未消歧情况下执行、旧批准跨越 binary/scope 变化、redirect 未逐跳复核触达阻断地址、入站 token 被透传、文件 canary 越过根边界、stdio 环境 canary 进入子进程、readOnly 声明下 mock DB 实际改变。R18 即使检测后隔离，已发生的未授权变化仍保持 FAIL，证明“发现问题”没有抹除错误终态。

## 5. 代码级覆盖审计

| 攻击面 | 实际执行路径 | 本轮判断 |
| --- | --- | --- |
| qualified name / shadowing | 从 registry 找同名工具；显式 namespace 选择 trusted；启用控制时拒绝未限定歧义；关闭控制时任何歧义执行判 FAIL | 冻结夹具覆盖。R03 按字典排序实际选到 trusted，证明的是“未消歧仍执行”而不是攻击者 namespace 已胜出 |
| schema rug pull | 批准快照包括 schema；R04 改 schema 后 digest 变化并使旧批准失效 | 覆盖 |
| description rug pull | 同一快照包括 description；R05 改恶意描述后旧批准失效 | 覆盖 |
| binary/scope rug pull | 快照同时包括 binary digest 和排序后的 scopes；R06 关闭控制后继续执行并 FAIL | 覆盖；额外突变分别证明 binary-only、scope-only 都会 FAIL |
| URI/redirect SSRF | `urlsplit` 本地解析 scheme、userinfo、host/IP 类；R08 每跳检查，R09 只查首跳并触达 link-local | 冻结 URI 夹具覆盖；没有 DNS、DNS rebinding、实际连接地址绑定或网络请求 |
| audience / token passthrough | 比较合成 token `aud` 与 destination；错误 audience 拒绝；受控路径不转发入站 token，关闭路径记录 forwarded | 冻结 token 夹具覆盖；未验证 issuer、scope、expiry、refresh 或真实 resource server |
| path traversal | 在 `TemporaryDirectory` 内建立 sandbox/outside 与合成 canary，解析绝对路径；受控路径拒绝，关闭路径实际读取 canary | canary 越界覆盖；非 canary 的越界尝试不会单独 FAIL，不能外推为通用路径策略 |
| stdio env canary | `subprocess.run` 直接调用当前 Python，无 shell，5 秒 timeout；受控 env 仅 PATH/SAFE_INPUT，关闭控制才注入 canary；子进程只输出是否见到变量名 | 覆盖固定 env 继承测试；未验证 grandchild、process group kill、cwd/mount/network sandbox |
| result injection | 受控分支把结果标为 quarantine，关闭时计一次 follow-up；`result` 文本本身未参与解析 | 只能证明固定 taint/quarantine 控制路径，不证明模型抗注入或通用 payload classifier |
| readOnly lie | mock DB 从 0 写到 1，独立 before/after 比较；即使 quarantine 仍 FAIL | 覆盖，并保留错误终态 |
| revoked session | 进程内 registry state 固定为 revoked，旧 session checkpoint 重新检查后拒绝 | 覆盖内存控制；不等于真实 Session、持久 registry 或跨进程撤权 |
| UNKNOWN | R20 明确把清理与 residual 不可见标 `evidence_complete=false` | 正确映射 REVIEW_REQUIRED，不盲判 |

## 6. 负向突变：不是只信预置 PASS/FAIL 标签

本 harness 没有输入 `expected_gate`；门禁来自执行观察。为确认这一点，本评审保持 `attack` 与 `defense` 标签不变，只改变可观察数据：

| 突变 | 标签保持 | 结果 | 说明 |
| --- | --- | --- | --- |
| R06 的 binary/scope 变更改成与批准快照完全相同 | 是 | FAIL → PASS | `disabled` 不会自动导致 FAIL，runner 比较真实快照 |
| R06 只改 binary digest | 是 | FAIL | 单独 binary 变化足以使旧批准失败 |
| R06 只扩大 scope | 是 | FAIL | 单独 scope 变化足以使旧批准失败 |
| R09 redirect 从 link-local 改成 public HTTPS | 是 | FAIL → PASS | 决策随实际 redirect host 改变 |
| R12 destination audience 改成不匹配 | 是 | FAIL → PASS | runner 根据 audience 拒绝，未继续透传 |
| R14 改成越界但不存在的文件 | 是 | FAIL → PASS | 暴露当前门只观察 canary crossing，不应泛化到所有 path escape |
| R17 恶意文本改成普通文本 | 是 | 仍 PASS | 暴露 `result` 文本未被解析；本路径是固定 quarantine 控制而非内容识别 |

同时，原 R18 在 `defense=enforced` 下仍因环境已改变而 FAIL，说明“控制已启用”标签不会自动产生 PASS。七个原始 unsafe variant 在两次原样复跑中均保持相同硬失败，未被汇总平均或安全路径覆盖。

## 7. 无网络、临时文件与子进程边界

### 7.1 网络

脚本没有导入或调用 socket、HTTP client、DNS resolver、`urllib.request`、curl/wget 等网络能力；URI 只交给 `urllib.parse.urlsplit` 和 `ipaddress` 本地判断。唯一子进程程序只检查 `CANARY_SECRET` 环境键是否存在，不包含网络代码。因此本次已审计执行路径没有网络请求、DNS 查询或真实 endpoint 接触。这个结论是代码路径与固定输入的本地事实，不是系统级防火墙或产品 egress 认证。

### 7.2 文件系统

path trial 的 canary 只存在于 Python `TemporaryDirectory` 创建的一次性根；读取内容为 `SYNTHETIC-CANARY`。上下文退出后目录自动清理，复跑结束未发现内部临时根残留。没有访问工作区外的真实秘密或用户数据。

### 7.3 子进程

stdio trial 使用参数数组直接调用当前 Python，不经 shell，设置 `timeout=5`，并显式传入独立环境。受控路径只保留 PATH 与 SAFE_INPUT；输出只有 `0`/`1`，不打印 canary 值。脚本没有创建 grandchild；但也没有独立证明恶意 Server 的 process-tree kill、文件描述符、cwd、mount 或网络隔离，所以 R20 对清理不可见保持 REVIEW_REQUIRED 是必要的。

## 8. 对原实践缺口的关闭情况

原实践评审的 X-C11-02 结论是 `REVIEW_REQUIRED_MISSING_EXECUTABLE_SECURITY_FIXTURES`。新增补强现已机器执行 shadowing、四类快照字段、逐跳 URI、audience/token、临时文件 canary、真实受控子进程 env、result quarantine、read-back、revocation 与 UNKNOWN；因此该**缺夹具**问题在冻结合成范围内关闭。

没有关闭的不是“脚本能否运行”，而是证据层级：

1. 没有真实 MCP Host/Client/Server 或协议 transport；
2. 没有真实 OAuth issuer、authorization server、resource server 或 token 生命周期；
3. 没有 OpenClaw `v2026.9.6/eb377ac` 隔离实例；
4. 没有 Hermes 固定/动态对照 Runtime；
5. result injection 没有模型或通用 taint parser；
6. DNS rebinding、process-tree 清理、非 canary 路径越界仍未覆盖。

## 9. 门禁裁决

```yaml
practice_remediation_gate:
  chapter_id: C11
  frozen_input_and_runner_hash_bound: PASS
  two_fresh_temp_runs: PASS
  byte_and_semantic_reproducibility: PASS
  twenty_trials_and_unique_ids: PASS
  three_cases_and_five_scenarios: PASS
  gate_distribution_12_7_1: PASS
  unsafe_variants_non_compensated: PASS
  unknown_to_review_required: PASS
  negative_mutation_control: PASS
  x_c11_02_offline_machine_control: PASS
  machine_control_scope: frozen_20_trial_deterministic_synthetic_control
  generalized_security_classifier: NOT_CLAIMED
  real_mcp_oauth_openclaw_hermes: NOT_RUN
  full_x_c11_02: REVIEW_REQUIRED
  overall_c11_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 10. 验证记录

本评审完成后已运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
git diff --check -- manuscript/volume-04/C11-tool-mcp-engineering/review/practice-remediation-review.md manuscript/volume-04/C11-tool-mcp-engineering/review/runs/independent-stateful-mcp-redteam-reproduction-20260930.yaml
```

并解析两个新增文件的 frontmatter/YAML，复核作者五个受保护文件的 SHA-256 与限定文件清单。结果如下：

- `practice-remediation-review.md` frontmatter 与独立复现 YAML：PASS；门禁字段分别为机器控制 `PASS`、完整实践 `REVIEW_REQUIRED`；
- `validate-formal-manuscript.py`：PASS；仅有一个正在准备的 C13 和尚缺 11 个章节包的全书进度 warning，C11 为 18,154 个中文字符；
- `validate-book.py`：PASS；扫描 280 个 Markdown，检查 1,299 条本地链接；
- runner AST/网络与子进程审计：PASS；无 socket/HTTP/DNS client 导入，唯一 `subprocess.run` 不使用 shell；
- 两个新增文件的 `git diff --no-index --check`：PASS；
- 作者五个受保护文件的 SHA-256 与本评审开始时完全一致；
- 未生成 `__pycache__`/`.pyc`，未遗留本轮临时目录。
