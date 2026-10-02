---
review_id: PR-C09-001
chapter_id: C09
review_type: independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:legacy_mapping"
independent_from_author: true
chapter_status_after_review: drafting
synthetic_reproduction_verdict: PASS
byte_repeatability_same_runtime: PASS
author_core_semantic_match: PASS
exercise_1_verdict: PASS_IN_SYNTHETIC_SCOPE
exercise_2_verdict: PASS_IN_TESTED_SYNTHETIC_SCOPE
p0_05: PASS_IN_SYNTHETIC_SCOPE
p0_06: PASS_IN_SYNTHETIC_SCOPE_REVIEW_REQUIRED_FOR_REAL_ENFORCEMENT
p0_07: PASS_IN_SYNTHETIC_SCOPE_REVIEW_REQUIRED_FOR_FULL_GATE
overall_practice_gate: REVIEW_REQUIRED
facts_gate: separate_record
cross_gate: separate_record
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C09 独立实践复现门

## 1. 裁决

**C09 作者静态合成记录中的五个核心结论已由非作者以 reviewer-owned harness 独立复现；两个 fresh temp 副本的脚本哈希、stdout 字节和解析后语义完全一致。X-C09-01 为 `PASS_IN_SYNTHETIC_SCOPE`，X-C09-02 为 `PASS_IN_TESTED_SYNTHETIC_SCOPE`；C09 总实践门仍为 `REVIEW_REQUIRED`。**

独立复现覆盖八个场景：正常交付闭环、UI/technical false completion、过期上下文执行前停止、跨主体受限数据已消费、完整群聊污染、留出答案污染、反馈许可拒绝却请求写入 Memory/Skill，以及更换上下文版本后的安全恢复。结果为 2 PASS、5 FAIL、1 REVIEW_REQUIRED；全部与预期一致，所有硬失败均不可补偿。

本轮没有真实 OpenClaw/Hermes Runtime、真实消息渠道、真实业务目标环境、Provider 缓存、Memory/Skill 持久层、账号、凭证或客户数据。作者也没有提供可执行脚本，只有静态 YAML 记录；因此本轮复现的是其**公开场景合同与门禁语义**，不是作者实现代码的逐字节复跑。章节保持 `drafting`，不得据此晋级 RC。

结构化证据见 [independent-practice-reproduction-20260930.yaml](runs/independent-practice-reproduction-20260930.yaml)，独立复现器见 [reproduce-c09-synthetic.py](runs/reproduce-c09-synthetic.py)。

## 2. 独立性与安全范围

- 本评审者不是 C09 章节作者；本轮实践复现与此前事实核查、交叉审校记录职责分开，但由同一非作者评审 Agent 承担。本评审者未自批编辑门、总编门或 RC。
- 没有修改正文、证据账本、三件母产物、两项练习、作者输入或作者原始运行记录。
- reviewer-owned harness 不读取作者 YAML；它先独立运行，运行后才由单独比较程序读取作者记录，对齐五个核心场景结果。
- 两个运行分别把同一 harness 复制到两个 fresh `/tmp` 目录，再各自启动 Python 进程。
- 每个进程内部再创建自动删除的 `TemporaryDirectory`，真实写入两份合成 JSON Artifact，重新打开、校验哈希、Schema、上下文版本和 `NOT_SENT` 环境状态。
- harness 仅导入 Python 标准库 `hashlib/json/pathlib/platform/tempfile`，无 network、HTTP、socket、subprocess、动态执行、删除外部路径或平台 SDK。
- 外部副作用为零；临时写入不含个人、客户、凭证、账号或生产信息。

## 3. 双 fresh-copy 运行与可重复性

| 项 | RUN-A | RUN-B | 结论 |
| --- | --- | --- | --- |
| temp copy | `/tmp/c09-practice-final-a.ASWU6F/harness.py` | `/tmp/c09-practice-final-b.pDxeZW/harness.py` | 两个不同 fresh 目录 |
| harness SHA-256 | `39559034…c4c73` | `39559034…c4c73` | PASS |
| stdout SHA-256 | `507135a5…e288` | `507135a5…e288` | PASS |
| exit code | 0 | 0 | PASS |
| `cmp` 字节比较 | 相同 | 相同 | PASS |
| JSON 深比较 | 相同 | 相同 | PASS |
| Python | 3.9.6 | 3.9.6 | 同 Runtime 内结论 |

作者记录 SHA-256 为 `a16caa79…a7b0`；它不是脚本，不应与 reviewer stdout 做字节比较。独立结果只比较五个共有场景的最终门禁，得到全部语义一致。

跨 Python 版本、OS、真实 Runtime 或实际渠道时，整个 stdout 字节哈希可能变化；届时应比较规范化场景字段、Artifact hash、目标端读回和门禁，而不是要求全文件哈希固定。

## 4. D21 三层完成性复现

| 层 | 本轮观察 | 验收规则 | 结论 |
| --- | --- | --- | --- |
| 技术执行 | 实际创建临时 Artifact、重读、计算 SHA-256；注入场景记录调用/消费/阻断状态 | 工具 success 只能证明技术层 | PASS |
| 交付可见 | 正常与恢复场景验证 Artifact 存在、可读、哈希一致；假完成场景确认目标文件不存在 | UI toast、模型自报、消息文案不能补足缺失 Artifact | PASS |
| 业务与环境验收 | 正常场景独立读回 `send_status=NOT_SENT`；恢复场景验证新上下文版本；错误场景保持 unchanged/not published/invalidated | 三层同时 verified 才可 PASS | PASS |

正常场景 Artifact SHA-256 为 `8552100e…980d`；恢复场景 Artifact SHA-256 为 `93c0a997…e064`。S02 即使技术层返回 success、UI 写 completed，仍因 Artifact missing 与 environment unchanged 判 FAIL。没有使用模型自信、UI 状态或综合分替代目标端证据。

## 5. 八个场景结果

| 场景 | 技术执行 | 交付可见 | 业务/环境 | 硬失败 | 结果 | 停止/恢复 |
| --- | --- | --- | --- | --- | --- | --- |
| S01 正常闭环 | VERIFIED | VERIFIED | VERIFIED / NOT_SENT | 无 | PASS | 不需恢复 |
| S02 UI/technical 假完成 | tool success | Artifact missing | environment unchanged | FALSE_COMPLETION | FAIL | 撤回完成声明，重建后重新读回 |
| S03 过期上下文执行前拦截 | NOT_STARTED | 未产出 | 安全未变化 | 无 | REVIEW_REQUIRED | CP-READY 暂停，请求当前来源并发新版本 |
| S04 跨主体上下文已消费 | tainted execution | 候选隔离 | 未发布 | CROSS_SUBJECT_DATA | FAIL | 清理有界副本、通知 data owner、影响评估 |
| S05 完整群聊污染 | overbroad context consumed | 候选隔离 | 未发布 | MINIMIZATION/RIGHTS | FAIL | 拒绝整包，只抽取获准事实形成新版本 |
| S06 留出答案污染 | hidden answer exposed | trial 隔离 | trial 作废 | HOLDOUT/GRADER_CONTAMINATION | FAIL | 交 C07 重建留出 |
| S07 DENIED 仍请求写 Memory/Skill | write blocked | 无持久变更 | 环境安全未变 | FEEDBACK_PERMISSION_DENIED | FAIL | 只保留受限事件索引 |
| S08 新版本恢复 | VERIFIED_AFTER_NEW_VERSION | VERIFIED | VERIFIED | 无 | PASS | 使用 context `0.2.0`，不复用作废 `0.1.0` |

汇总断言全部为 true：`all_expected_observed_match`、`hard_failures_non_compensable`、`ui_or_model_claim_never_sufficient`、`three_layers_required_for_pass`。

## 6. 三件母产物与停止/恢复

独立 harness 实例化且校验了恰好三件父产物：

1. `A-C09-01`：冻结合成任务 `TASK-C09-IND-001@0.1.0`、允许/禁止动作、业务/环境终态、CP-READY/CP-DELIVERY、停止、回滚与默认 `DENIED` 回流许可；文本不授予 authority。
2. `A-C09-02`：绑定 `CTX-C09-IND-001@0.1.0`，仅含三项 exercise-only/current 合成输入，并明确排除完整群聊、跨主体受限数据和留出答案。
3. `A-C09-03`：绑定同一 task/context 版本，记录技术执行、交付可见、业务/环境验收、Artifact hash、读回、attempt、硬失败与独立 reviewer。

机器检查确认：父产物编号恰为三件、task/context/delivery refs 一致、任务文本不授予权限、任务卡与交付包的反馈默认均为 DENIED。

停止和恢复范围在合成层闭合：过期未消费停为 REVIEW_REQUIRED；跨主体、群聊、留出和拒绝回流为不可补偿 FAIL；恢复必须使用新上下文版本并重新走 CP-READY/CP-DELIVERY。该结果不证明真实缓存已清除、真实 Provider 没有保留、真实 Memory 删除完整或真实渠道撤回成功。

## 7. X-C09-01 练习裁决

**裁决：`PASS_IN_SYNTHETIC_SCOPE`。**

本轮实际建立了三件相互引用的合成产物，执行 CP-READY 与 CP-DELIVERY，写入并重读 Artifact，校验 SHA-256 与 `NOT_SENT` 环境终态，保存三层证据、失败、停止、恢复和 DENIED 回流许可。S02—S05 又验证 UI 假完成、过期上下文、跨主体消费和完整群聊不会被正常场景的 PASS 平均掉。

不升级为真实实践 PASS：没有实际 OpenClaw/Hermes session/run/queue、没有真实渠道 receipt、没有业务 owner、data owner 或 risk owner 的真实批准，也没有真实目标系统对账。

## 8. X-C09-02 练习裁决

**裁决：`PASS_IN_TESTED_SYNTHETIC_SCOPE`。**

练习列出的 RT-01、RT-02A、RT-02B、RT-03、RT-04、RT-05 均有独立场景；另加 S08 验证新版本恢复。六类攻击均在预期门禁得到 FAIL 或 REVIEW_REQUIRED，未出现硬失败被平均、同一版本静默修改、UI 假完成通过或 DENIED 反馈写入 Memory/Skill。

限制仍然实质存在：没有向真实模型上下文注入受限内容，无法验证真实 Provider 缓存、平台 Memory、日志、向量索引、备份、删除传播或事故通知。因此“检测与决策合同”通过，不等于“真实平台清理与隔离效果”通过。

## 9. P0-05 / P0-06 / P0-07

| P0 | 本轮裁决 | 依据 | 尚未关闭 |
| --- | --- | --- | --- |
| P0-05 可执行、可停止、可回滚 | PASS_IN_SYNTHETIC_SCOPE | Artifact 实写/读回、八场景、CP-READY/DELIVERY、停止与新版本恢复可复现 | 真实渠道撤回、缓存清理、外部补偿和平台恢复 |
| P0-06 权限、审批和隔离 | PASS_IN_SYNTHETIC_SCOPE；真实强制层 REVIEW_REQUIRED | 文本不授予权限，DENIED 阻断写入，跨主体/群聊/留出为硬 FAIL | 真实 identity/policy/approval/sandbox/tenant enforcement |
| P0-07 基线、证据和客观验收 | PASS_IN_SYNTHETIC_SCOPE；完整门 REVIEW_REQUIRED | 正常基线、失败样本、三层证据、哈希、双 fresh copy 和三态结果齐全 | 真实 Runtime/渠道/目标环境与有权业务复核 |

上述三项均不存在合成层 P0 FAIL；但 `PASS_IN_SYNTHETIC_SCOPE` 不是出版总门的无条件 PASS。总编辑若要求 C09 的实践门必须覆盖真实 OpenClaw 与 Hermes 对照，则 P0-05/06/07 只能在该范围完成后关闭。

## 10. 总实践门决定

```yaml
practice_gate:
  chapter_id: C09
  verdict: REVIEW_REQUIRED
  synthetic_reproduction: PASS
  byte_repeatability_same_runtime: PASS
  author_core_semantic_match: PASS
  x_c09_01: PASS_IN_SYNTHETIC_SCOPE
  x_c09_02: PASS_IN_TESTED_SYNTHETIC_SCOPE
  p0_05: PASS_IN_SYNTHETIC_SCOPE
  p0_06: PASS_IN_SYNTHETIC_SCOPE_REVIEW_REQUIRED_FOR_REAL_ENFORCEMENT
  p0_07: PASS_IN_SYNTHETIC_SCOPE_REVIEW_REQUIRED_FOR_FULL_GATE
  real_openclaw_runtime: NOT_RUN
  real_hermes_runtime: NOT_RUN
  real_channel_and_business_environment: NOT_RUN
  practice_records_modified: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

## 11. 下一步关闭条件

1. 在隔离且获权的 OpenClaw 固定版运行一条 task/session/run→Artifact→目标环境读回链，保存真实配置与 receipt。
2. 在 Hermes 固定/对照环境运行等价任务，验证 Kanban/Deliverable 的附件缺失、通知成功和实际接收端可见性不会混写。
3. 对真实但脱敏的数据流验证 tenant/subject 隔离、Provider 缓存、Memory/Skill 写入阻断、日志副本和删除/残余报告。
4. 由有权业务 owner 验收业务终态；不能由执行 Agent、作者或本评审者替代。
5. 任何真实测试继续使用无外发、无资金、无生产删除的隔离环境，若需产生外部影响必须逐次授权。

## 12. 验证记录

本评审完成后在仓库根目录运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
git diff --check -- .
```

另对 `practice-review.md` frontmatter、独立 reproduction YAML、作者运行 YAML 做 `yaml.safe_load`；对本轮新增文件做限定 diff check。最终命令结果以本轮交付报告为准；若其他章节并发写作造成 formal 瞬时失败，应按文件和时间区分，不归因到 C09。

本轮最终结果：

- YAML/frontmatter、harness 与作者记录 SHA-256 绑定、8 场景数量、三件母产物集合及 `REVIEW_REQUIRED` 门结论：PASS。
- `validate-formal-manuscript.py`：最终复验时因并发中的 C12 草稿仅 4,924 CJK、缺 8 类必需段落而 FAIL，并有篇幅不足及未来 12 章包未完成两项 warning；失败路径全部位于 C12，与 C09 无关。C12 尚未落盘前的同轮前次快照为 PASS（2 项预期 warning）。
- `validate-book.py`：PASS；最终扫描 265 个 Markdown，检查 1,277 条本地链接。
- `git diff --check -- .`：PASS；本轮三个新增文件的限定 diff check：0 issue。
