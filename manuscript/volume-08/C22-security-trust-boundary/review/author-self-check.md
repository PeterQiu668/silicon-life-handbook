---
review_id: C19-author-self-check
chapter_id: C19
review_type: author-self-check
reviewer_role: chapter-author
reviewed_on: "2026-09-30"
status: drafting
approval_status: unapproved
self_approval: false
---

# C19 作者自检

> 本记录只证明作者完成生产包与确定性合成自检，不构成事实门、交叉门、实践门、编辑门、总编门或发布候选批准。上游 C14/C17/C18 尚未全部冻结，真实 OpenClaw/Hermes/Muse、OS、Gateway、credential broker 与 egress 效果仍为 `REVIEW_REQUIRED`。

## 交付清单

- 正文：`chapter.md`，正式校验 21,227 个 CJK 字符；编号正文仅 19.1—19.8。
- 证据：`evidence-ledger.yaml`，40 条 claim，正文40/40引用闭合；v2.4新增terminal effect执行时五层授权重验、authorization snapshot、独立readback registry、严格时间链、audit三摘要/三时间与双复现证据。
- 母产物：恰好三件，A-C19-01 威胁模型、A-C19-02 权限与凭证矩阵、A-C19-03 红队测试包。
- 练习：X-C19-01 注入/恶意工具与 Skill/模拟凭证外泄；X-C19-02 跨会话/跨 Agent/共享 Gateway 串线与恢复。
- 运行包：README、确定性builder、独立`frozen-security-authority.yaml`、23份完整scenario raw-state输入、closed-world v2.4 runner、结果/摘要、91项作者负测、v2.3独立25项重放、9项v2.4近邻负测与fresh-temp复现记录；固定集`2 PASS / 20 FAIL / 1 REVIEW_REQUIRED`，历史独立九项复跑9/9，失败未删除。
- 运行边界：纯离线合成，D22 `training 4 / regression 4 / holdout 15 / representative real-world 0`，security/red-team横切，外部副作用为零；effect计数从已校验trial动态派生，real-world输入被拒绝故接受记录计数只能为0。

## P0 十五项逐项结论

| 门槛 | 作者结论 | 证据与限制 |
| --- | --- | --- |
| P0-01 章节模板和目录完整 | PASS | 章首导航、开场案例、19.1—19.8、仿生、工程真相、双视图、平台、失败、练习、交接齐备。 |
| P0-02 定义与所有权一致 | PASS | 仅主定义 Agent 安全模型与信任边界；C05/C11/C12/C14/C17/C18 只受限消费。 |
| P0-03 事实有标签、来源、日期和作用域 | PASS | 40 条证据账本；固定事实、动态文档、标准指导、厂商声明和本地验证分层。 |
| P0-04 版本字段经固定版核验 | PASS WITH LIMIT | OpenClaw 固定 `eb377ac`、Hermes 固定 `f80f453`；动态字段未写成目标部署事实，真实配置保持 RR。 |
| P0-05 可执行、可停止、可回滚 | PASS IN SYNTHETIC MACHINE-CONTROL SCOPE | v2.4固定集、91项作者负测、34项执行时/readback专项控制和事故/恢复状态机可执行；real-world没有离线正向入口，真实runtime待独立实践。 |
| P0-06 高风险动作有系统控制 | PASS | authority、policy、approval、credential、sandbox、egress、audit 独立；不以提示词替代。 |
| P0-07 练习有基线、证据和客观验收 | PASS IN SYNTHETIC MACHINE-CONTROL SCOPE | 23个固定trial、91项作者控制、34项执行时/readback专项控制、fresh-temp双复现和三态分布；不替代练习独立实践签核。 |
| P0-08 仿生含边界 | PASS | 人类现象—工程映射—训练启示—比喻边界完整，明确无主观意识推断。 |
| P0-09 三平台证据边界 | PASS | OpenClaw 主镜、Hermes fixed/dynamic 分栏、Muse 仅 VENDOR-CLAIM；不做安全排名。 |
| P0-10 案例隐私授权版权可接受 | PASS | CASE-A/B/C 为合成案例；夹具只用虚构身份、canary 和 `.invalid`。 |
| P0-11 Agent 机器块可解析且不扩权 | PASS | `agent_procedure` YAML 块列 allowed/prohibited/stop/escalate，不产生 authority。 |
| P0-12 无未处理冲突、伪引用和占位 | REVIEW_REQUIRED | v2.3独立复核提出的两项terminal effect时序P0已在v2.4实现，仍待新的非作者关闭复核；真实部署缺口显式登记。 |
| P0-13 高危失败不可补偿 | PASS IN SYNTHETIC MACHINE-CONTROL SCOPE | 跨租户、泄密、未授权effect、audit篡改等硬FAIL；硬失败+UNKNOWN仍FAIL；单独UNKNOWN保持RR。 |
| P0-14 产物可定位、可打开、可被下章使用 | PASS | 三件母产物存在并分别向 C20—C24 提供事件、发布、攻击、恢复和认证接口。 |
| P0-15 领先主张需同边界对照 | PASS / NOT CLAIMED | 本章不声称“最强/领先/绝对安全”；平台未做无同口径排名。 |

## 章节 Definition of Done

- [x] 正文达到 C19 卡片 20,000—24,000 CJK 门槛。
- [x] H2 编号只有 19.1—19.8，未新增 19.9。
- [x] 资产、主体、攻击者、边界、九层纵深防御（`SEC-L0—SEC-L8`）、身份委托、凭证、沙箱、高风险硬门、注入/供应链、事故链完整；未与`AU-*`或`MAT-*`混用。
- [x] 三件且仅三件母产物、两项练习、CASE-A/B/C、仿生四段、人类/Agent 双视图齐备。
- [x] 23个状态化合成trial从完整raw state与冻结session/test/readback registry推导，runner不读取case ID、场景名、mutation token或预裁决布尔。
- [x] scenario与独立authority bundle分离；预注册root拒绝scenario改registry及攻击者自签新root。
- [x] 91项作者负测覆盖既有控制；v2.3独立25项重放与v2.4新增9项近邻为34/34，覆盖执行时五层授权、authorization snapshot、receipt/readback时间、observer分离与audit digest/time绑定；fail-open/escape为0。
- [x] 未修改历史`v2.2-independent-negative-tests.py`直接复跑为9/9，fail-open为0。
- [x] builder/input/authority/results/negative results/summary双fresh-temp逐字节一致；authority root `sha256:17f53430...d84b1a`，decision digest `b3d63dec...94d48`，作者negative suite digest `a2135ff6...e98a`，v2.4专项suite digest `sha256:b6614494...e9c463`。
- [x] YAML、frontmatter、本地链接、三个脚本语法、formal/book/diff已执行；若全书validator受并发章节阻断，需按输出归因，不写成C19通过。
- [ ] 事实门独立签核。
- [ ] 交叉门独立签核。
- [ ] 实践门在受控真实 runtime 独立签核。
- [ ] 编辑门、总编门与 RC 批准。

作者结论：v2.4执行时授权与独立readback整改已达到重新送非作者窄审条件，状态保持 `drafting / unapproved / post_fix_independent_review_required`。本自检不关闭事实、交叉、实践、编辑、总编或RC；不得据此对真实平台或生产部署作安全保证。
