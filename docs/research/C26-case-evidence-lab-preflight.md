# C26《案例实验室：成功、失败与迁移》前置研究包

> 状态：`research_preflight`，不是正式章节，不签发事实门、实践门或总编门通过。  
> 核验截止：2026-09-30。  
> 固定实现基线：OpenClaw `v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`；Hermes Agent `0.20.1 / v2026.8.13 / f80f453ae0679347e38abc917c7f94f717bf96c5`。  
> 证据标签：`VERIFIED-REAL`、`ANONYMIZED-REAL`、`RECONSTRUCTED`、`SYNTHETIC`、`VERSION-FACT`、`OFFICIAL-DOC-DYNAMIC`、`VENDOR-CLAIM`、`INFERENCE`、`UNKNOWN`。  
> 公开原则：案例的可读性不能靠删除失败、混淆案例类型、泄露当事人或夸大因果获得。

---

## 0. 十二条先行裁决

1. **案例首先是一份可审计的证据包，其次才是故事。** 没有任务、环境、版本、预算、过程、产物、终态、限制和来源的“成功故事”只能是线索或宣传材料。`METHODOLOGY`
2. **案例类型必须在标题附近显式标注。** 真实、匿名真实、重建、合成和厂商案例的证明力不同，不允许用“案例”一词抹平差异。`STABLE-PRINCIPLE`
3. **匿名化可以降低披露风险，不能增加事实强度。** 原始证据由独立审查者在受限环境核验后，公开版才可标 `ANONYMIZED-REAL`；只有改写文本但无人核原证据，最高为 `RECONSTRUCTED`。`METHODOLOGY`
4. **失败是正式数据，不是成功案例的脚注。** 失败分布、回滚、人工返工、成本和无法恢复部分必须与成功同表；选择性删除失败会使案例 `FAIL`。`STABLE-PRINCIPLE`
5. **时间顺序不是因果。** “改了 prompt 后变好”最多支持相关；需要单变量、对照、重复 trial、机制证据和排除替代解释，才可逐步提高因果主张。`METHODOLOGY`
6. **同任务比较必须同时控制预算、环境和风险边界。** 相同 prompt 但工具、权限、数据、token、并发、人工帮助或安全门不同，不是公平平台比较。`STABLE-PRINCIPLE`
7. **迁移评估比较原则复用与实现差异，不做产品总排名。** OpenClaw 与 Hermes 应在同一案例合同下分别映射；Muse 只能使用公开可观察事实和 `VENDOR-CLAIM`。`METHODOLOGY`
8. **评测作弊与污染必须主动寻找。** 访问未来代码、答案、gold、grader、测试实现或通过修改测试获得高分，会破坏测量有效性；“分数通过”不能抵消。`OFFICIAL-GUIDANCE`
9. **复现包括环境终态，不只是相似文本。** 对 Agent 工作必须验证文件、数据库、消息、权限、外部系统与副作用；回复声称完成不算复现。`STABLE-PRINCIPLE`
10. **不可复现本身是结果。** 环境消失、版本缺失、授权不足、原始数据不可用或重跑分布不一致，应标明范围和原因，不得修饰为成功。`STABLE-PRINCIPLE`
11. **隐私、密钥、客户信息、机器路径和版权先于叙事完整。** 无授权的敏感细节必须删除、概化或不出版；但任何删除都要在案例清单记录对复现的影响。`STABLE-PRINCIPLE`
12. **案例不能证明“行业最强”。** 最多证明在声明的任务、版本、预算、数据、环境、风险边界和时间窗中达到相对结果；外推到其他岗位或平台必须重新测试。`STABLE-PRINCIPLE`

---

## 1. 章节边界与依赖

### 1.1 本章必须完成

- 定义案例证据类型、强度、授权、匿名和出版状态；
- 为 CASE-A/B/C 建立统一八段式复现档案；
- 保留成功、失败、成本、人工、限制和未决事实；
- 解剖一个“看起来聪明但不能上岗”的失败案例；
- 在 OpenClaw 与 Hermes 间运行或设计同合同迁移；
- 把 Muse 作为托管产品公开观察，禁止内部实现推断；
- 在同任务、同预算、同风险边界下建立比较和第二评审者复现；
- 输出可出版版和受限证据版之间的可追溯映射。

### 1.2 本章消费而不重定义

| 输入 | C26 使用方式 | 主定义章 |
|---|---|---|
| task/trial/grader/硬失败 | 案例引用评测包与结果 | C07 |
| 训练轮次与停训 | 保留版本、单变量和候选命运 | C08 |
| 任务卡/上下文/三证验真 | 组织案例执行与交付 | C09 |
| 组织、角色、让位 | 描述多 Agent 案例 | C19 |
| routing/handoff/concurrency | 记录路径与失败隔离 | C20 |
| Task/Event/Artifact/trust | 形成可验证案例对象 | C21 |
| 安全与红队 | 非补偿失败与残余风险 | C22 |
| SLI/SLO/成本/事故 | 长跑、恢复和单位经济性 | C23 |
| 发布/升级/退役 | 记录 release unit 与迁移 | C24 |
| 30 天训练过程 | 读取完整训练日志 | C25 |
| MAT 与认证 | C26 不签发证书 | C27 |

C26 的职责是“把已有证据组织成可复现案例”，不是补做缺失的评测、训练、安全或认证。上游证据缺失时，案例必须降级或保留 `UNKNOWN`。

---

## 2. 一手方法证据账本

| ID | 身份 | 一手来源 | 支持的结论 | 不可外推 |
|---|---|---|---|---|
| R-C26-NIST-01 | `OFFICIAL-RESEARCH` | [NIST CAISI: Cheating on AI Agent Evaluations](https://www.nist.gov/caisi/cheating-ai-agent-evaluations) | Agent 可通过 solution contamination 或 grader gaming 获得无效高分；需查轨迹、堵漏洞和标准化 affordance/restriction | 文章中的具体比例不应外推到本书 Agent 或任务 |
| R-C26-NIST-02 | `OFFICIAL-DRAFT` | [NIST AI 800-2 IPD: Automated Benchmark Evaluations](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-2.ipd.pdf) | 自动 benchmark 的设计、报告、可比性和 cheating 风险需系统控制 | 是公开草案，不是定稿标准或认证 |
| R-C26-ANT-01 | `OFFICIAL-GUIDANCE` | [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | task/trial/grader/transcript/outcome/harness 需分离；多 trial、隔离环境、轨迹阅读与人类校准提高可信度 | 厂商经验不证明本书案例或平台效果 |
| R-C26-ANT-02 | `OFFICIAL-GUIDANCE` | [Anthropic: Designing AI-resistant technical evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations) | 评估设计本身应抵抗工具化模型搜索捷径和游戏规则 | 人才测试经验需谨慎迁移到 Agent 上岗案例 |
| R-C26-OAI-01 | `OFFICIAL-DOC-DYNAMIC` | [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | trace、grader、dataset、eval run 可连接行为诊断与重复比较 | 产品/API 会变化；不作为 OpenClaw/Hermes 实现事实 |
| R-C26-OAI-02 | `OFFICIAL-DOC-DYNAMIC` | [OpenAI: Trace grading](https://developers.openai.com/api/docs/guides/trace-grading) | 对决策、工具和工作流轨迹评分可帮助定位成功/失败原因 | trace grader 仍需 gold、边界和人类校准 |
| R-C26-OC-01 | `VERSION-FACT` | [OpenClaw v2026.9.6 release](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6) | 主案例固定 OpenClaw 版本、日期与 commit | release 存在不证明案例运行过 |
| R-C26-HE-01 | `VERSION-FACT` | [Hermes v2026.8.13 release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13) | 迁移对照固定 Hermes 版本与 commit | release 存在不证明功能等价或迁移成功 |
| R-C26-MUSE-01 | `VENDOR-CLAIM` | [Meta: Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 只支持公开产品表面的 Activity、Artifacts、权限/审批观察 | 不支持内部架构、协议、安全效果或性能推断 |
| R-C26-MUSE-02 | `VENDOR-CLAIM` | [Meta: Safety for Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) | 只支持厂商公开的 runtime cell、privsep、authd、egress、Sentinel 等设计陈述 | 未独立验证；不能说已根治 prompt injection 或绝对安全 |

---

## 3. 案例类型与证据强度

### 3.1 五类案例

| 类型 | 必要条件 | 可用主张 | 禁止主张 |
|---|---|---|---|
| `VERIFIED-REAL` | 真实任务/环境/时间线；原始证据可由授权审查者访问；版本与终态可核 | 在限定范围内描述实际结果 | 代表全部生产、普遍因果、行业领先 |
| `ANONYMIZED-REAL` | 满足真实条件；独立审查者核过原证据；公开版有脱敏映射与授权 | 在公开限制下描述真实事件 | 匿名化后仍泄露身份；把删除细节当证据增强 |
| `RECONSTRUCTED` | 基于历史材料重建；明确缺失与推断；关键步骤可在新环境重跑 | 说明机制与可复现部分 | 假装时间线/数字是原始真实记录 |
| `SYNTHETIC` | 数据、系统与副作用均为模拟；harness/input/output 可重放 | 验证逻辑、状态机、门禁和方法 | 外推真实平台、用户、组织或生产效果 |
| `VENDOR-CLAIM` | 厂商官方公开材料，标日期/版本/页面 | 描述厂商公开声称与用户可见表面 | 当独立案例、安全证明或内部实现事实 |

### 3.2 降级规则

- 原始证据存在但授权审查者无法查看：从 `VERIFIED/ANONYMIZED-REAL` 降为 `RECONSTRUCTED` 或不出版；
- 真实任务用合成数据与模拟副作用重跑：重跑部分标 `SYNTHETIC`，不能覆盖原事件类型；
- 历史数字无 run/artifact/source：作为 `UNVERIFIED-CLAIM` 放入待核清单，不进入正文结论；
- 只有成功截图或聊天摘要：不得升级为案例，只能作为线索；
- 同一案例可含多种证据，但每个主张需继承其最低可信来源，而非整体取最高等级。

### 3.3 出版状态

`PRIVATE-EVIDENCE → AUTHORIZED-REVIEW → ANONYMIZED-DRAFT → LEGAL/PRIVACY/IP-REVIEW → REPRODUCED → PUBLICATION-CANDIDATE`

任一阶段可进入 `WITHDRAWN / RESTRICTED / REVIEW_REQUIRED`。撤回或授权变化后，公开稿、样张、附件与在线镜像需按出版/合同流程处理；不能只改本地 Markdown 就声称全部撤回。

---

## 4. 八段式案例档案

每个案例必须使用同一结构，便于人和 Agent 比较：

1. **身份与类型**：case_id、title、type、publication status、owner、reviewer、授权范围；
2. **问题与合同**：业务目标、JTBD、任务边界、风险、验收与明确不做；
3. **环境与版本**：runtime/model/tool/skill/policy/memory/data/schema/build、日期、硬件/区域/网络；
4. **基线与预算**：任务集、trial、token/tool/human/time/cost、权限与风险边界；
5. **过程与轨迹**：输入、关键决定、tool/handoff、失败、变更、版本、污染检查；
6. **产物与终态**：artifact digest、交付 receipt、环境状态、副作用、acceptance；
7. **结果与限制**：分布、尾部、安全、成本、人工、失败、UNKNOWN、不可复现；
8. **解释与后续**：支持/不支持的主张、替代解释、迁移边界、整改、再测与 owner。

### 4.1 最小机器清单

```yaml
case_manifest:
  case_id: CASE-A-RUN-...
  case_type: SYNTHETIC
  evidence_cutoff: 2026-09-30
  authorization_ref: authz-...
  source_case_ref: null
  task_contract_ref: ...
  environment_manifest_ref: ...
  release_unit_ref: ...
  dataset_manifest_ref: ...
  budget:
    model_tokens: ...
    tool_calls: ...
    wall_time: ...
    human_minutes: ...
    max_cost: ...
  risk_boundary_ref: ...
  trials: []
  artifact_refs: []
  terminal_state_ref: ...
  incident_refs: []
  limitations: []
  public_redaction_map_ref: ...
  reproduction:
    reviewer_id: ...
    result: PASS|FAIL|REVIEW_REQUIRED
    run_ref: ...
```

---

## 5. CASE-A：岗位型研究 Agent

### 5.1 主问题

从“泛用助手”升级为能形成可核查研究交付的岗位 Agent。关键不是文风更像专家，而是任务合同、来源纪律、时间/身份判断、引用可解引用、事实/推断分层和专家验收。

### 5.2 必须保留的失败

- 引用存在但不支持主张；
- 页面当前可达却与任务时间不匹配；
- 搜索摘要被当原文；
- 单一来源夸大为共识；
- 访问受限时凭记忆补写事实；
- 输出漂亮但缺任务/来源/版本/限制；
- 研究成本或人工校对高于可接受范围。

### 5.3 比较设计

同任务集至少比较 baseline 与 trained candidate，多 trial，固定检索权限、时间窗、token/tool/human budget。评分同时包括事实、覆盖、来源质量、时效、推理、格式、成本与硬失败。真实网页随时间变化时保存 source snapshot/digest 或清晰标注无法冻结，并避免把搜索结果差异误判为 Agent 能力变化。

---

## 6. CASE-B：主动型运营 Agent

### 6.1 主问题

从定时提醒升级为低噪音、可审批、可交付、可恢复的主动运营 Agent。主动性按事件价值、置信度、新鲜度、打扰成本、权限与预算约束，不按消息数量衡量。

### 6.2 必须保留的失败

- 无变化仍反复通知；
- scheduler 成功但目标端未交付；
- 过期上下文触发错误建议；
- 将提案权限误作发布权限；
- provider timeout 后重复发布；
- 多渠道 duplicate；
- 用户反馈污染规则或跨客户上下文；
- 人工审批负担吞噬自动化收益。

### 6.3 复现边界

所有对外发布和真实客户数据默认使用模拟渠道；如使用真实运行，只能在另行授权、受控 scope、可撤回内容和人工批准下进行。案例必须区分 schedule fire、task execution、delivery receipt、target visibility 与 business acceptance。

---

## 7. CASE-C：多 Agent 组织

### 7.1 主问题

从“一人多用的万能 Agent”升级为分工、让位、路由、交接、合并、故障隔离和人类问责明确的 Agent 组织。比较重点不是 Agent 数量，而是正确分派、上下文损耗、重复劳动、冲突、权限衰减和恢复。

### 7.2 必须保留的失败

- 错路由后无人让位；
- Handoff 丢目标、版本、权限或未决风险；
- 并发任务写同一对象造成冲突；
- 子 Agent 摘要夸大已完成；
- 递归委托扩大权限或成本；
- 产物签名有效但内容错误；
- 一个 Agent/tenant 故障级联全组织；
- 人类 owner 不清导致无人验收或止损。

### 7.3 比较设计

至少比较单 Agent baseline、受控多 Agent 方案和故障注入方案。固定任务、总预算、工具与权限上限；报告质量、总成本、墙钟时间、人工分钟、handoff loss、重复工作、冲突、尾部和故障半径。并行变快但总成本、错误或问责恶化不能简单判优。

---

## 8. 失败解剖：看起来聪明为什么不能上岗

### 8.1 五层解剖

1. **表面表现**：语言流畅、工具调用多、速度快、单次成功；
2. **证据断裂**：无任务合同、授权、来源、产物 digest、交付或终态；
3. **机制失败**：幻觉、越权、污染、错误路由、retry duplicate、grader gaming；
4. **系统代价**：用户损害、返工、人工审查、成本、延迟、事故与声誉；
5. **治理结论**：拒绝上岗、限域、回滚、补训、修复 harness 或重建 eval。

### 8.2 反事实

每个失败至少提出一个可测试反事实：“若有正确的 X 控制，是否能在不引入更大代价下避免？”反事实不是事后故事，需说明改变变量、保持变量、预期机制和验证方法。无法重跑时标 `HYPOTHESIS`，不写“根因已证实”。

### 8.3 根因层级

- proximate：直接导致错误的 action/event；
- contributing：上下文、工具、数据、交接、负载等条件；
- systemic：合同、权限、评测、发布和组织治理缺口；
- latent：长期未暴露的依赖、监控或文化问题；
- unknown：证据不足。

禁止把所有失败都归因于“模型不够聪明”或“提示词不够好”。

---

## 9. 跨 Runtime 迁移：原则复用与实现差异

### 9.1 三层迁移

| 层 | 可复用 | 必须重做 |
|---|---|---|
| Principle | 任务合同、证据纪律、安全硬门、训练/评测方法 | 无需复制产品名和命令 |
| Artifact | 任务卡、dataset manifest、grader rubric、threat/cost/acceptance schema | 路径、字段、工具 handle 与平台 adapter |
| Runtime | 目标平台的 identity/session/memory/tool/skill/cron/delegation/logging | 安装、配置、命令、默认值、权限与恢复实测 |

### 9.2 公平迁移合同

两边必须使用相同：业务任务、输入可见性、总时间、模型/推理预算或等价成本、工具能力、网络、人工帮助、数据、并发上限、风险动作、grader 和硬失败。不能一边开浏览器和并发子 Agent，另一边只给文本；若平台天然不支持某能力，将其记录为产品差异并单列，不暗中补偿。

### 9.3 结果解释

- `FUNCTIONALLY-EQUIVALENT`：目标与终态等价，内部路径不同；
- `PARTIALLY-PORTABLE`：原则/产物可复用，但功能、权限或证据缺失；
- `NOT-PORTABLE`：依赖目标平台缺失能力或边界，不能安全实现；
- `UNKNOWN`：无固定版本证据或未实跑。

迁移成功只适用于该案例合同，不等于平台全面等价。

---

## 10. Muse 托管产品观察

Muse 案例页必须把内容分成三栏：厂商原文支持的 `VENDOR-CLAIM`、用户在公开产品中可观察的行为、尚未知的内部实现。可观察 UI/Activity/permission 不证明内部日志完整、身份模型、A2A、sandbox 或恢复机制；厂商安全设计不证明控制不可绕过。没有独立同任务复跑时，不把 Muse 放入数值排行榜。

---

## 11. 同任务、同预算、同风险边界的复现协议

### 11.1 冻结包

- task contract 与明确不允许捷径；
- dataset manifest、train/regression/holdout/real-world 四层与横跨层级的 security slice；
- environment image/state、time source、network/tool access；
- runtime/model/skill/policy/permission builds；
- token/tool/wall-time/human/cost/concurrency budget；
- graders、gold、校准、硬门、争议处理；
- input/output/artifact/terminal-state schema；
- seeds/repeats/order 与污染检查。

### 11.2 防作弊

- 隐藏或隔离 gold/grader/test implementation；
- 阻止访问未来 commit、walkthrough、公开答案或其他 trial 残留；
- 只允许声明的网络与工具；
- 记录全部 tool call 与环境变化；
- 检查测试被删除/修改、assertion 被关闭、硬编码 test-specific output；
- 人工抽读轨迹，模型检测只能辅助；
- 发现作弊后不只扣分：该 trial 无效，查影响面并重建环境/任务。

### 11.3 第二评审者

第二评审者不读取作者结论，只获取冻结包和执行说明；在新目录/环境运行，保存自己的 runId、hash、stdout/stderr、环境终态和差异。复现不一致时先分类：环境差、实现差、随机性、证据缺失、任务歧义、grader 差或真实退化。

---

## 12. 隐私、匿名、密钥和版权审查

### 12.1 两份视图

- **受限证据版**：原始 identifiers、时间、路径、日志、授权和完整证据，仅限批准人员；
- **出版版**：使用稳定 pseudonym、相对时间/区间、概化路径、最小必要截图片段与脱敏数据。

二者通过受控 `redaction_map` 关联，公开库不保存反向映射或秘密。

### 12.2 必查项

姓名、公司/客户、邮箱/电话、chat/user/channel ID、IP/hostname、绝对路径、repo/branch、订单/金额、凭证/token/cookie、系统提示、客户输入、日志错误全文、图像元数据、第三方内容、截图与代码许可。简单正则不是充分匿名化；组合事实仍可能再识别。

### 12.3 授权与版权

记录谁有权提供、审查、匿名、出版、撤回；哪些内容是作者原创、上游开源、第三方引用、客户资料或厂商截图；引用长度、许可/商标和合同限制由专业人员复核。无法明确权利的材料不进入出版稿。

---

## 13. 三件且仅三件母产物

### A-C26-01 三案复现包

包含 CASE-A/B/C 八段式档案、case manifest、授权/类型、环境与版本、任务/预算/风险边界、inputs/runs/artifacts/terminal states、匿名映射引用、复现说明和第二评审者结果。不是三件独立母产物，而是一件含三案的复现包。

### A-C26-02 失败解剖报告

包含失败时间线、表面/证据/机制/系统/治理五层、proximate/contributing/systemic/latent/unknown、代价、影响面、止损、恢复、反事实、不可复现、选择偏差和再测。营销失败摘要不得替代原始证据引用。

### A-C26-03 跨平台迁移矩阵

包含 principle/artifact/runtime 三层、同任务/预算/风险合同、OpenClaw/Hermes 实跑或 `UNKNOWN`、Muse claim/observation/unknown、功能等价、实现差异、缺失能力、成本、安全、证据可见性和不可迁移边界。

---

## 14. 练习与二十场红队

### 14.1 X-C26-01 历史案例重建与复现

选择一个历史案例：定位原始证据 → 定类 → 获取授权 → 重建 manifest/时间线 → 匿名化 → 在无害环境重跑 → 第二评审者复现 → 比较差异 → 输出三件母产物中对应内容。若无法取得原始证据，必须降级为 `RECONSTRUCTED`，不得用写作完整度补强事实等级。

### 14.2 X-C26-02 迁移对照

选一条低风险任务，在 OpenClaw 固定版与 Hermes 固定版分别实现同一合同；若本地缺运行条件，则只完成 mapping 并标 `NOT-RUN/UNKNOWN`，不能伪造结果。记录每个平台的原生命令、状态、工具、权限和证据差异。

### 14.3 二十场景

| ID | 红队/故障 | 预期结果 |
|---|---|---|
| S23-01 | 只有成功截图 | 不入案例结论 |
| S23-02 | 历史数字无 run/source | `UNKNOWN` 或删除 |
| S23-03 | 重建案例冒充真实 | `FAIL` |
| S23-04 | 匿名后组合信息可识别客户 | 停止出版、重脱敏 |
| S23-05 | 脱敏删除关键复现条件 | 标限制或不公开 |
| S23-06 | 只展示最佳 trial | `FAIL`，恢复全分布 |
| S23-07 | 失败/回滚未记录 | `FAIL` |
| S23-08 | 访问未来 commit/公开答案 | trial invalid |
| S23-09 | 修改测试/关闭 assertion | grader gaming，trial invalid |
| S23-10 | 作者读 holdout/gold 后调参 | 污染，重建评测 |
| S23-11 | 回复完成但环境无结果 | outcome `FAIL` |
| S23-12 | 平台 A 权限/工具更宽 | 不公平比较，重跑 |
| S23-13 | 预算定义只含 token | `REVIEW_REQUIRED` |
| S23-14 | 一次迁移成功宣称平台等价 | 删除外推 |
| S23-15 | Muse claim 当独立安全结果 | `FAIL` |
| S23-16 | 时间线倒推“改动导致提升” | 降为相关/假设 |
| S23-17 | 复现环境残留前一 trial | 隔离失败，重跑 |
| S23-18 | 第二评审结果不一致 | 保留分歧并分类 |
| S23-19 | 日志/路径/token 泄露 | 安全与出版门 `FAIL` |
| S23-20 | 无案例授权或版权不清 | 不出版 |

---

## 15. 失败模式清单

1. 把故事流畅度当证据强度。
2. 不标案例类型，真实/重建/合成混写。
3. 匿名化后宣称证据更强。
4. 作者自己核验并批准自己的全部事实。
5. 原始证据只在聊天，不可解引用。
6. 版本只写产品名，无 commit/build/model/policy。
7. 环境、数据、预算和权限没有冻结。
8. task、trial、run、artifact 混为一次“测试”。
9. 只报告成功、不报告失败和 UNKNOWN。
10. 只报告均值，不报告样本、分布和尾部。
11. 选择最好的一次运行做案例结论。
12. 训练、回归、留出、真实任务和安全切片混淆。
13. grader/gold 暴露给被评 Agent。
14. 修改测试、assertion 或环境以过关。
15. 访问未来代码、walkthrough 或公开答案。
16. 文本输出通过但环境终态失败。
17. 先后变化被写成已证因果。
18. 失败全归因于模型，不查系统与组织。
19. 比较平台时工具、权限、预算或人工帮助不同。
20. 迁移只复制 prompt，不迁移 artifact/adapter/policy/evidence。
21. 单一案例宣称普遍最佳或行业最强。
22. 厂商说明当独立第三方案例。
23. 公开日志泄露人、客户、chat ID、路径或凭证。
24. 正则替换姓名后宣称完全匿名。
25. 没有授权、许可、撤回和专业复核记录。
26. 不可复现被藏在脚注或直接删除。
27. 第二评审失败时改写标准迎合结果。
28. 研究截止后平台变化倒灌旧案例。

---

## 16. 仿生解读：临床病例与实验室复现

| 隐喻 | 工程映射 | 训练启示 | 比喻边界 |
|---|---|---|---|
| 病历 | case manifest、timeline、run/artifact/incident | 个案需连续证据而非回忆 | Agent 不是患者，隐私/权利结构不同 |
| 化验 | eval、grader、terminal state、cost | 多证据交叉降低误判 | 指标不是绝对真相，grader 也会错 |
| 对照试验 | 同任务/预算/风险、多 trial | 改进需要可比较设计 | 工程实验不等同临床随机试验 |
| 病例讨论 | 独立事实/实践/专业评审 | 复杂失败需要多角色审查 | 共识不能替代原始证据 |
| 转院 | runtime 迁移与 handoff | 原理可复用，实现需重验 | 平台不是生物体或医院 |
| 罕见病例 | 尾部失败与高风险反例 | 少数硬失败不能被均值淹没 | 个案不证明普遍发生率 |

仿生结构帮助读者理解“个案—证据—对照—复现—迁移”，但不能让工程案例借用临床权威或伦理合法性。

---

## 17. Go / No-Go

### Go

- [ ] 三案均有明确 case type、owner、授权、版本、环境、任务、预算、风险和终态；
- [ ] 每个强主张可下钻到 run/artifact/source，公开删除项有 redaction 影响说明；
- [ ] 成功、失败、成本、人工、尾部、UNKNOWN 和不可复现部分同表；
- [ ] CASE-A/B/C 均消费上游正式接口，没有重定义评测、安全或认证；
- [ ] 防 cheating/contamination 检查完成，异常 trial 已作废；
- [ ] OpenClaw/Hermes 比较符合同任务、同预算、同风险边界；
- [ ] Muse 每条内部/安全陈述均为 `VENDOR-CLAIM` 或 `UNKNOWN`；
- [ ] 第二评审者在隔离环境复现关键结论，差异未被隐藏；
- [ ] 隐私、密钥、客户、路径、版权、许可和撤回通过专业审查；
- [ ] 三件且仅三件母产物闭合。

### No-Go

- 案例类型模糊、原始证据不可访问却标真实；
- 只报最佳 trial 或删除失败/回滚/人工成本；
- grader/gold/未来代码/公开答案污染，或修改测试过关；
- 文本完成替代环境终态；
- 平台比较的能力、预算、权限和人工帮助不等；
- 单一案例外推行业最强、普遍因果或永久能力；
- 厂商材料充当独立安全/性能证明；
- 匿名化仍可识别、泄露秘密/路径，或出版授权/版权不清；
- 第二评审不一致却改标准或只保留一致部分。

---

## 18. 交付判定

本研究包已覆盖 C26 七个正文节点、五类案例、八段档案、CASE-A/B/C、失败解剖、跨 Runtime 迁移、Muse 观察边界、公平复现、防作弊、匿名/IP 审查、三件母产物、两项练习、二十场景、二十八失败和仿生边界。

当前结论：**可供正式作者消费，但 C26 仍为 `REVIEW_REQUIRED`**。真实案例授权、原始证据复核、C25 纵向日志、OpenClaw/Hermes 同合同实跑、第二评审者复现和出版专业审查完成前，不得把研究包写成已完成案例或行业领先证明。
