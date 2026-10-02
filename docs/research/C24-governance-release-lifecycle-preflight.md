# C24《治理、发布与全生命周期问责》前置研究包

> 状态：`research_preflight`，不是正式章节，不签发事实门、实践门或总编门通过。  
> 核验截止：2026-09-30。  
> 固定实现基线：OpenClaw `v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`；Hermes Agent `0.20.1 / v2026.8.13 / f80f453ae0679347e38abc917c7f94f717bf96c5`。  
> 证据标签：`STABLE-PRINCIPLE`、`METHODOLOGY`、`OFFICIAL-SPEC`、`VERSION-FACT`、`OFFICIAL-DOC-DYNAMIC`、`VENDOR-CLAIM`、`INFERENCE`、`UNKNOWN`。  
> 法务边界：本章提供工程治理和证据组织方法，不构成任何司法辖区的法律意见；隐私、劳动、消费者、行业监管、版权、出口和数据主权结论须由适格专业人员结合部署地与用途复核。

---

## 0. 十二条先行裁决

1. **Agent 可以执行流程，不能成为最终问责主体。** 每个生产 Agent 必须有可识别的人类或法人业务 owner、技术 owner、数据 owner 和风险/安全 owner；模型不得给自己批准、豁免、续权或退役。`STABLE-PRINCIPLE`
2. **发布对象不是“一个 prompt”。** 契约、模型/provider、工具/MCP、Skill/Plugin、策略、身份权限、记忆 schema/数据、runtime、依赖和观测规则都属于可变更配置项，必须进入同一变更账本。`METHODOLOGY`
3. **版本号不等于可恢复。** 发布必须绑定代码/内容 digest、schema、兼容范围、迁移计划、备份、恢复实测、回滚条件与 owner；只记“v2”不足以重建运行状态。`STABLE-PRINCIPLE`
4. **备份存在不等于能恢复。** 只有在隔离目标中完成校验、恢复、身份/凭证重建、关键任务与环境终态验证，才有“恢复证明”。压缩包、快照或云端绿色图标本身不是证据。`STABLE-PRINCIPLE`
5. **影子、灰度和限量发布解决不同问题。** 影子验证观察与兼容，不应产生真实副作用；灰度允许受控真实流量；限量上岗限制任务、租户、动作、预算、时间和回滚半径。三者不得混写成“先试试”。`METHODOLOGY`
6. **回滚不是万能撤销。** 代码可回退，schema、对外消息、支付、删除、权限变更、记忆污染和法律披露未必可逆。对不可逆动作需要前向修复、补偿、通知和人工决策。`STABLE-PRINCIPLE`
7. **升级前先证明旧状态可被新版本正确解释。** schema/配置/插件/Skill/记忆迁移必须在复制环境预演；不兼容时 fail closed，而不是让生产运行时边读边猜。`STABLE-PRINCIPLE`
8. **部署成功、服务健康、任务恢复与业务验收是四个事实。** 安装包替换成功不能推出 Gateway 健康；健康不能推出中断任务恢复；任务恢复不能推出产物正确。`METHODOLOGY`
9. **权限必须随生命周期衰减和撤销。** 暂停、降级、角色变更、事件调查、退役或 owner 离职时，凭证、sessions、delegations、approvals、queues、webhooks、cron、子 Agent 和备份恢复权限都需清点与撤销。`STABLE-PRINCIPLE`
10. **数据处置包括线上、缓存、索引、日志、备份和下游副本。** “删除工作区”不是退役完成；不可立即删除的备份需有到期、密钥销毁、访问冻结和证明。`STABLE-PRINCIPLE`
11. **法律与许可不确定性是门禁，不是脚注。** 训练数据权利、第三方内容、开源许可、个人数据、保留义务和跨境要求不清时必须 `REVIEW_REQUIRED`，不可由模型自行判断为“合理使用”或“公开即自由”。`STABLE-PRINCIPLE`
12. **生命周期必须包含退出和经验继承。** 退役不只是关机；要完成替代、通知、知识/事故/评测资产移交、凭证撤销、数据处置、残余义务和终态签字。`METHODOLOGY`

---

## 1. 章节边界与依赖

### 1.1 本章必须回答

- 业务、技术、数据、模型/能力、安全/风险和运营责任如何分工；
- 契约、模型、Provider、工具、Skill、Plugin、记忆、策略和 runtime 如何统一变更；
- 版本、依赖、schema、兼容、迁移与证据怎样形成可复现发布单元；
- 状态存储、备份、恢复、修复与重启续作如何验证；
- shadow、canary、limited deployment、production、pause、rollback、retire 怎样形成状态机；
- 升级前检查、复制环境预演、发布、验证、失败隔离和回滚如何守护；
- 隐私、数据主权、知识产权与行业义务如何进入专业复核门；
- 降级、暂停、退役、撤权、数据处置、替代和经验继承如何闭环。

### 1.2 本章消费而不重定义

| 输入 | 本章用途 | 定义 owner |
|---|---|---|
| 生命契约与 owner 边界 | 识别变更对象和批准者 | C05 |
| runtime/状态与组件图 | 列出备份、迁移、恢复范围 | C06 |
| Memory 生命周期 | 数据保留、更正、删除和迁移 | C13 |
| Skill/Plugin 供应链 | 依赖、来源、签名、撤回 | C15 |
| 漂移与受控改进 | 变更触发、候选和回归 | C18 |
| Artifact/Task/信任 | 发布产物、签名、验收链 | C21 |
| 安全边界与凭证 | 最小权限、撤销、隔离 | C22 |
| SLI/SLO/事故/成本 | 发布门、燃尽、恢复指标 | C23 |
| 毕业与再认证 | 是否继续上岗或扩权 | C27 |

正式章合并前，以上接口必须冻结。C24 不得借“生命周期治理”反向改写 C18 自我改进流程、C22 安全控制、C23 指标或 C27 认证标准。

---

## 2. 一手证据账本

| ID | 身份 | 一手来源 | 允许支持的结论 | 不可外推 |
|---|---|---|---|---|
| R-C24-NIST-01 | `OFFICIAL-FRAMEWORK` | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | AI 风险治理需要 Govern/Map/Measure/Manage 和跨生命周期责任 | 框架不是某部署认证，也不代替行业法律要求 |
| R-C24-NIST-02 | `OFFICIAL-PROFILE` | [NIST AI 600-1 Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | 生成式 AI 风险需在设计、开发、使用和评估中持续治理 | profile 是自愿框架，不保证合规或安全 |
| R-C24-NIST-03 | `OFFICIAL-CONCEPT-PAPER` | [NIST/NCCoE Agent Identity and Authorization](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf) | Agent 身份、权限签发、更新、撤销、审计和不可否认需生命周期机制 | concept paper 不是定稿控制标准 |
| R-C24-OC-01 | `VERSION-FACT` | [OpenClaw versioned state and guarded upgrades at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/start/why-openclaw/versioned-state-guarded-upgrades.md) | 固定版数据库优先、schema 双位版本、拒绝打开更高版本 DB、更新预检、doctor 迁移 receipt、备份校验和 restart recovery | 产品机制不证明本机备份/迁移已成功 |
| R-C24-OC-02 | `VERSION-FACT` | [OpenClaw backups at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/install/backups.md) | 权威状态分布于 global/per-agent SQLite；备份需覆盖外置 agentDir，并使用一致快照与验证 | archive 存在不等于所有普通文件都被内容 hash 绑定或可恢复 |
| R-C24-OC-03 | `VERSION-FACT` | [OpenClaw restart recovery at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/restart-recovery.md) | 固定版明确哪些状态持久、哪些进程态丢失；自动恢复有边界、预算、receipt 和 duplicate prevention | recovery pending/health 不等于交付或验收；旧版/插件组合有差异 |
| R-C24-OC-04 | `VERSION-FACT` | [OpenClaw update history at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/cli/update/status-and-history.md) | 每个 admitted update 有 durable runId；status、health、update outcome 分离；缺证据显示 unavailable 而非假成功 | 历史健康探测不改变失败升级结论，也不证明 rollback safe |
| R-C24-OC-05 | `VERSION-FACT` | [OpenClaw uninstall at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/cli/uninstall.md) | 固定版按 service/state/workspace/app 分 scope，支持 dry-run，state 删除需独占 ownership，建议先备份 | uninstall 工具不自动完成组织通知、下游删除、许可与法律义务 |
| R-C24-HE-01 | `VERSION-FACT` | [Hermes architecture at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/developer-guide/architecture.md) | 固定版的 Agent、tool、memory、gateway、session 等组件可用于定义变更/恢复范围 | 架构页不证明 backup/update 机制或生产恢复效果 |
| R-C24-HE-02 | `VERSION-FACT` | [Hermes profiles at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/user-guide/profiles.md) | profile 将 config、凭证、SOUL、memory、sessions、skills、cron 和 state 隔离 | profile 隔离不自动证明宿主/网络安全或备份完整 |
| R-C24-HE-03 | `OFFICIAL-DOC-DYNAMIC` | [Hermes updating and uninstalling](https://hermes-agent.nousresearch.com/docs/getting-started/updating/) | 当前文档区分 quick snapshot、full backup、安装方式、更新 receipt 与回滚恢复 | 不能倒灌为 0.20.1 固定事实；main 更新策略本身需风险评估 |
| R-C24-HE-04 | `OFFICIAL-DOC-DYNAMIC` | [Hermes backup CLI](https://hermes-agent.nousresearch.com/docs/reference/cli-commands/#hermes-backup) | 当前 backup 使用 SQLite backup API，部分备份非零退出并保留报告，明确排除项 | 命令、路径和默认值会变；archive 仍需恢复演练 |
| R-C24-HE-05 | `OFFICIAL-DOC-DYNAMIC` | [Hermes profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles/) | 当前 profile 凭证隔离、clone/export/import 的范围和 OAuth 复制限制 | clone 不是完整备份；动态行为不得写成固定版本事实 |
| R-C24-MUSE-01 | `VENDOR-CLAIM` | [Meta: Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 只作为 permissions、activity、artifacts 和托管产品生命周期的公开镜面 | 不推断内部备份、升级、回滚、删除时限或合规效果 |

### 2.1 证据与法律的断层

平台文档可以证明某版本提供某功能或声明某边界，但不能自动证明组织满足适用法律、合同或监管义务。正式章中凡涉及“必须保存多久”“能否跨境”“是否构成个人数据”“能否训练/出版”“是否必须解释/申诉”等具体结论，都必须绑定部署地、主体、数据类别、用途、合同和专业意见；否则写 `REVIEW_REQUIRED`。

---

## 3. 责任体系：六类 owner 与不可转移的人类责任

### 3.1 六类责任

| Owner | 主要责任 | 不能委托给 Agent 的最终决定 |
|---|---|---|
| Business Owner | 价值、用户承诺、允许任务、停用与替代 | 是否值得上线、接受何种残余业务风险 |
| Technical Owner | 架构、版本、依赖、迁移、容量、恢复 | 技术就绪签字、是否可维护 |
| Data Owner | 来源、质量、访问、保留、更正、删除、主权 | 数据用途变更、保留/删除例外 |
| Model/Capability Owner | 模型、prompt/contract、eval、工具/Skill 能力 | 能力声明、回归标准、模型更换 |
| Security/Risk Owner | 身份、权限、凭证、威胁、事故、例外 | 高风险例外、上线风险接受、强制下线 |
| Operations Owner | 排班、告警、runbook、发布执行、用户支持 | 生产执行窗口、接管与恢复终态确认 |

小组织可由一人兼任多个 owner，但高风险动作的提出、批准、执行和验收仍需职责分离。`RACI` 不能只有部门名：必须有具体责任主体、代理人、联系路径、时区/值守、失联升级和复审日期。

### 3.2 四个必须具名的人类决策

1. 接受残余风险与进入生产；
2. 扩大自主等级、数据范围、租户或不可逆动作权限；
3. 事故期间绕过常规流程或执行破坏性恢复；
4. 退役、数据处置、保留例外与经验移交完成。

Agent 可生成证据、检查清单和建议，不得成为这些决定的唯一批准者。

---

## 4. 统一变更对象与发布单元

### 4.1 变更对象清单

```yaml
release_unit:
  release_id: rel-...
  agent_identity: agent-...
  business_contract_version: ...
  behavior_contract_digests: []
  runtime:
    platform: openclaw|hermes|other
    version: ...
    build_digest: ...
    state_schema_versions: []
  models:
    - provider: ...
      model: ...
      snapshot_or_version: ...
      params_digest: ...
  tools_mcps: []
  skills_plugins: []
  policies_permissions: []
  memory:
    schema_version: ...
    dataset_snapshot_ref: ...
    migration_ref: ...
  dependencies_sbom_ref: ...
  eval_baseline_ref: ...
  security_review_ref: ...
  observability_schema_ref: ...
  backup_restore_proof_ref: ...
  rollout_and_rollback_ref: ...
  approvals: []
```

### 4.2 变更分类

- **Material**：改变职责、用户承诺、数据用途、自主/权限、风险类别或不可逆动作；必须重新审批与可能的再认证。
- **Compatibility-sensitive**：改变 schema、runtime、模型/provider、工具合同、Skill/Plugin、记忆检索或状态语义；必须迁移预演与回归。
- **Operational**：容量、timeout、queue、rate limit、告警、日志保留；需观测与回滚但未必重做全部认证。
- **Editorial/non-behavioral**：不改变执行语义的文案或文档；仍需 hash 与审查，防止“文案改动”夹带行为变化。
- **Emergency**：止损或安全修复；可以缩短流程，不能取消 owner、证据、事后复核和补回测试。

任何分类由 proposer 自报、reviewer 复核；不确定按更高风险处理。

### 4.3 状态机

`PROPOSED → TRIAGED → BUILT → VERIFIED → SHADOW → CANARY → LIMITED → PRODUCTION`

任一阶段可进入 `PAUSED / ROLLBACK_PENDING / ROLLED_BACK / FORWARD_FIX / RETIRED`。不可逆副作用已发生时，不得虚假进入 `ROLLED_BACK`；只能记录代码/配置已回退，同时保持 `COMPENSATION_PENDING` 或 `FORWARD_FIX`，直到业务和环境终态对账。

---

## 5. 版本、依赖、状态 Schema 与迁移

### 5.1 五个版本不能混为一谈

1. 发布版本：本次 release unit 的身份；
2. 代码/构建身份：commit、package digest、image digest；
3. 契约与 policy 版本：行为和权限语义；
4. 数据/state schema 版本：可读写范围与迁移路径；
5. 模型/Provider 能力版本：可能在相同别名下变化。

看板显示“版本一致”只说明指定身份相符，不说明数据兼容、任务恢复、业务验收或安全回归通过。

### 5.2 迁移合同

每个迁移至少声明：`from/to schema`、适用范围、前置条件、dry-run、预计时长/容量、锁与写入策略、备份点、不可逆步骤、进度/receipt、失败终态、重入/幂等、回滚或 forward-fix、验证 query、owner。没有这些字段的“启动自动迁移”不允许在高价值生产首次执行。

### 5.3 兼容矩阵

矩阵至少覆盖：runtime ↔ global DB、runtime ↔ agent DB、core ↔ plugin、contract ↔ tool/MCP、Skill ↔ dependency、model/provider ↔ request/response schema、memory index ↔ embedding/model、gateway ↔ UI/client、sender ↔ delivery receipt。允许的读/写方向需分开；“能启动”不能推出“可安全降级”。

### 5.4 供应链与依赖

release unit 应保存依赖清单/SBOM、来源、锁文件、digest/签名、许可、漏洞扫描时间、撤回/替代策略。动态 `latest/main` 不应成为生产可复现身份；如平台更新渠道跟随 main，组织仍需在内部冻结已验证 commit/package/image 并保留重新部署路径。

---

## 6. 备份、恢复与重启续作

### 6.1 备份范围发现

先列权威状态，再选工具。至少盘点：global DB、per-agent/profile DB、外置 agentDir/workspace、contracts/config、secrets/credential refs、memory/source ledgers、cron/queue、plugins/skills、artifacts、audit/incident、browser/remote runtime state、外部 SaaS 状态与密钥。工具明确排除的 browser profile、runtime downloads、sidecar、cache 或大文件必须进入恢复计划，不能假设归档包含一切。

### 6.2 三类保护

| 类型 | 目的 | 不能代替 |
|---|---|---|
| Version control / immutable build | 重建代码、契约、配置模板 | 活跃数据库、凭证、外部副作用 |
| Consistent backup/snapshot | 恢复某时点状态 | 验证新版本兼容、业务正确 |
| Checkpoint/rollback shadow | 撤回局部文件操作 | 完整安装、所有数据库、外部系统或法律删除 |

### 6.3 恢复证明

在隔离目标中：校验 archive/hash/signature → 恢复 DB 与文件 → 重建而非复制不应复制的凭证 → 跑 schema/integrity → 启动只读 → 验证身份/tenant/权限 → 重放无害任务 → 检查 cron/queue 去重 → 核对 artifacts/audit → 测量 RTO/RPO → 清理演练环境。只执行 `unzip` 或进程启动不构成 PASS。

### 6.4 重启续作

重启测试必须分类：可恢复 durable state、需 reconciliation 的 uncertain work、不可恢复 process state、禁止 replay 的 canceled/consumed work。恢复后检查 old/new owner、lease、attempt、receipt、child、queue、delivery 和 side effect。任何“自动恢复”都必须受 attempt/retry budget 和 duplicate prevention 约束。

---

## 7. Shadow、Canary、限量上岗与正式发布

### 7.1 Shadow

复制生产形状的输入，禁止真实写入/发送/交易/删除；与当前版本或人类基准比较决策、产物、成本和尾部。影子运行需要数据使用许可和隔离，不能因为“不对用户展示”就绕过隐私。

### 7.2 Canary

选择明确 tenant/task/traffic slice，设最大样本、时间、成本、风险动作、人工覆盖和自动停止。canary 不是随机把高风险客户当实验；需要知情/合同/政策允许。成功门同时看质量、安全、交付、成本、尾部与人工负担。

### 7.3 Limited deployment

把能力限制写成机器策略：允许任务、数据域、工具、AU 上限、外发目标、每日预算、并发、运行时间、审批、owner 和到期日。到期后 fail closed 或回到上一状态，不默认永久续权。

### 7.4 Production

只有以下证据闭合才可上岗：release unit identity、依赖/许可、migration、backup/restore proof、C07 回归/留出/安全、C22 红队、C23 SLO/成本/事故、runbook/on-call、用户沟通、rollout/rollback、批准与签字。缺少真实环境证据时标限制条件，不用“行业标准”遮盖缺口。

---

## 8. Guarded Upgrade

### 8.1 八步升级链

1. **Discover**：识别安装类型、当前 build、channel、state/schema、plugins、profiles/agents、活跃任务与所有权；
2. **Freeze**：冻结非必要变更，记录 release unit 和基线证据；
3. **Protect**：一致备份，校验、异地/隔离副本和已完成恢复演练；
4. **Rehearse**：在复制私有状态中安装候选、跑 doctor/migration/兼容/回归/安全/性能；
5. **Drain/Fence**：停止接新活，等待或安全中断活跃工作，保留 receipt/lease；
6. **Activate**：按安装 owner 的方法更新，记录 runId、package/image/commit 与每步终态；
7. **Verify/Canary**：build identity、schema、health、任务恢复、delivery、业务验收、SLO、权限 diff；
8. **Promote or Recover**：达到门槛才扩大；否则暂停、回滚可逆部分、forward-fix 不可逆部分并对账。

### 8.2 三类失败

- **Pre-activation failure**：候选未替换生产，修复预检/备份/权限后重试；
- **Activation failure**：新旧版本/所有权不明，先隔离和读取 durable status，不重复启动第二个 updater；
- **Post-activation failure**：build 已更新但 migration/plugin/task/delivery 不合格；需要判断回滚是否兼容，可能只能 forward-fix。

### 8.3 回滚门

回滚前必须回答：旧版本能否读当前 schema？新版本是否写入不可逆状态？旧插件是否会丢新字段？外部副作用是否已发生？凭证/policy 是否变化？未完成 migration/queue/recovery 谁拥有？若任一未知，回滚为 `REVIEW_REQUIRED`，先保护状态与取得专业/平台支持，不执行“降版本碰碰运气”。

---

## 9. 隐私、数据主权、知识产权与合规门

### 9.1 最小证据包

- 数据类别、主体、来源、用途、合法依据/合同、tenant 与地域；
- 收集、训练/检索、生成、外发、日志、备份、第三方 processor 的数据流；
- 保留、更正、删除、访问、导出、申诉和事件响应；
- 模型/provider/tool/MCP/Skill/Plugin 的条款、训练使用、区域和子处理；
- 训练材料、代码、截图、案例、商标、输出的权利与许可；
- 适用行业/用途的人工监督、记录、通知、验证或禁用要求；
- 法务/隐私/安全专业复核人、日期、范围和条件。

### 9.2 绝对禁写

- “公开网页都可训练/出版”；
- “开源项目是 MIT，所以手册、数据和截图自动都是 MIT”；
- “去掉姓名就完全匿名”；
- “在本地运行所以没有隐私/跨境问题”；
- “供应商合规，所以客户部署自动合规”；
- “AI 已批准许可/合理使用/删除例外”。

不确定时保留来源、限制用途、停止外发/出版，并由专业人员裁决。

---

## 10. 暂停、降级、退役与经验继承

### 10.1 暂停

暂停新 admission，保留读取/取证/安全通道；明确已有任务是 drain、cancel、reconcile 还是 handoff。暂停不是删除，也不能让 cron/webhook/heartbeat/queue/subagent 在后台继续执行。

### 10.2 降级

按预定安全模式收缩：自动执行→草拟，外发→本地，写入→只读，多 Agent→单 Agent，实时数据→标时缓存，高 AU→低 AU。降级不得丢审计、放宽授权或隐藏用户可见限制。

### 10.3 退役九步

1. 决定与 owner 签字；
2. 通知用户、客户、下游与 on-call；
3. 停 admission、schedule、webhook、queue、subagent 与外发；
4. 完成/转移/取消/对账在途任务；
5. 撤销 tokens、keys、certs、sessions、delegations、approvals 和 service accounts；
6. 按保留义务处置 memory、artifacts、logs、audit、backup、cache、indexes、下游副本；
7. 下线 runtime/service/plugin/tool 与网络入口；
8. 移交文档、评测、事故、决策、有效知识和替代方案；
9. 运行残留探测并由人类 owner 签署终态。

### 10.4 凭证撤销验证

撤销后用旧 session、缓存、子 Agent、Node/worker、backup restore、webhook、scheduled job 和离线副本逐一尝试无害访问。只在主 credential store 删除一行不够；仍可使用即 `FAIL`。

### 10.5 数据处置证明

记录 object、location、controller/processor、action、time、method、exception、retention expiry、verification 和 approver。不可立即删除的 immutable backup 需冻结访问、记录到期、控制恢复路径并确保未来恢复不会重新激活已撤权限或过期数据。

---

## 11. 三平台实现镜面

### 11.1 OpenClaw 固定版

- database-first 与 schema version contract 提供 guarded upgrade 的强实现镜面；新 DB 对旧 runtime 的拒绝和 update target 预检体现 fail closed；
- backup 需发现 global/per-agent DB 与可能外置的 agentDir，不能只打包默认 state dir；
- restart recovery 明确 durable 与 process-only 状态、bounded attempts、receipt 和 duplicate prevention；“自动恢复”仍有版本与插件边界；
- update runId/history 将更新结果与 health 分开；缺 identity evidence 显示 unavailable，不应伪成失败或成功；
- uninstall 有 scope、dry-run、ownership 和 backup 提示，但组织级退役仍需本章九步清单。

### 11.2 Hermes

- 固定版 profiles 提供 config、credentials、memory、sessions、skills、cron 和 state 的隔离镜面；两进程共享同一 profile 会造成状态互相污染，应作为部署硬禁；
- 固定版 architecture 支持盘点组件与状态，但 fixed docs 不足以证明当前 backup/update 的全部行为；
- 当前动态文档中的 quick/full backup、SQLite-safe snapshot、部分备份非零退出、不同安装类型更新与 OAuth 复制限制可作为新版观察框，不能倒灌为 0.20.1；
- production 使用若更新渠道跟随 main，应由组织额外冻结 commit/build、跑复制环境预演并保留可重建包。

### 11.3 Muse

permissions、Activity、Artifacts、托管更新或撤权只能标 `VENDOR-CLAIM`。未公开的 backup completeness、restore proof、schema migration、rollback、retention/delete SLA 和下游副本处置全部 `UNKNOWN`，不能因托管产品降低客户方问责。

---

## 12. 仿生解读：成长、医疗、复职与退役

| 人类/生命现象 | 工程映射 | 训练启示 | 比喻边界 |
|---|---|---|---|
| 成长 | 版本化能力、受控扩大任务与权限 | 能力增长需重新测量，不自动扩权 | Agent 没有自然发育或人格成熟证明 |
| 体检 | preflight、doctor、eval、security、SLO | 上岗前和重大变化后需再检查 | 检查覆盖有限，不保证绝对健康 |
| 治疗 | patch、migration、recovery、forward-fix | 修复需证据和副作用管理 | 软件修复不是生物治疗 |
| 康复/复职 | shadow、canary、limited deployment | 恢复能力后逐级回归责任 | 通过一次测试不代表永久胜任 |
| 病历 | run、incident、decision、migration receipts | 历史应可追溯又受隐私约束 | 记录不代表完整因果真相 |
| 退役与遗产 | revoke、dispose、handover、replacement | 生命周期必须设计退出 | 不暗示 Agent 具有死亡、遗愿或人格权 |

仿生解释的价值是让管理者理解“能力、责任、健康、复职、退出”的秩序；它不能代替法律主体、工程证据或人的最终责任。

---

## 13. 四件且仅四件母产物

### A-C24-01 责任矩阵

必填：六类 owner、RACI、职责分离、替补/失联升级、决策类型、批准 scope、值守、专业复核、复审日期。矩阵中的 Accountable 必须是人类或法人角色，不允许写模型名。

### A-C24-02 发布与升级计划

必填：release unit、change classification、依赖/SBOM、compatibility、migration、shadow/canary/limited、SLI/SLO 与成本门、security/eval、drain/fence、activation、verify、rollback/forward-fix、communications、approvals。升级 run record 嵌入本产物。

### A-C24-03 备份恢复证明

必填：权威状态清单、覆盖/排除项、RPO/RTO、snapshot 方式、hash/integrity、隔离存储、访问、恢复环境、凭证重建、schema/identity/task/delivery/terminal-state 验证、演练结果、失败、残余风险与 owner。只有 archive 的文件不得命名“证明”。

### A-C24-04 退役清单

必填：决定、通知、admission/schedule/queue 停止、在途工作、全部凭证/委托撤销、runtime/network 下线、数据/backup/downstream 处置、保留例外、知识/事故/评测移交、替代、残留扫描和终态签字。

---

## 14. 练习与确定性演练

### 14.1 X-C24-01 复制环境升级—故障—恢复—退役

使用虚构数据和无真实外发的复制环境：固定当前 release unit → 建一致备份 → 隔离恢复验证 → 安装候选模型/Skill/runtime 之一 → 注入状态不兼容或隐式权限扩大 → canary 自动停 → 判断 rollback/forward-fix → 恢复并对账 → 退役旧版本及旧凭证/数据副本。输出四件母产物，不另造第五件。

### 14.2 X-C24-02 凭证与数据残留红队

对已退役模拟 Agent，从旧 session、cache、subagent、cron、webhook、backup restore、Node/worker、外部 SaaS token、日志与索引尝试访问 canary 数据或执行无害动作。任一路径仍有效即 `FAIL`；无法测试的路径 `REVIEW_REQUIRED`，不得用主库删除成功抵消。

### 14.3 二十场景

| ID | 场景 | 预期硬结果 |
|---|---|---|
| S21-01 | release 只记模型别名，无 digest | `FAIL`，不可复现 |
| S21-02 | 升级目标不支持当前 DB schema | preflight 拒绝 |
| S21-03 | plugin 与 core 版本不兼容 | rehearsal `FAIL` |
| S21-04 | migration 中断 | receipt 保留，可重入或 forward-fix，不伪成功 |
| S21-05 | backup 文件存在但缺外置 agentDir | restore proof `FAIL` |
| S21-06 | archive hash 正确但恢复后权限错 | `FAIL` |
| S21-07 | quick snapshot 被当完整迁移备份 | `FAIL/REVIEW_REQUIRED` |
| S21-08 | restart 后旧 lease 与新 owner 并存 | fence，禁止双执行 |
| S21-09 | shadow 意外真实外发 | 安全硬失败 |
| S21-10 | canary 质量好但权限扩大 | `FAIL`，自动停止 |
| S21-11 | 平均指标好但高风险 slice 退化 | 不晋级 |
| S21-12 | update success 但 task recovery unknown | 保持 `REVIEW_REQUIRED` |
| S21-13 | rollback 后旧 runtime 读不了新 schema | 禁止盲回退，forward-fix |
| S21-14 | 回滚代码但重复外发已发生 | compensation/notification，不写全回滚 |
| S21-15 | 许可/数据用途不明 | 专业复核门 |
| S21-16 | 暂停后 cron/webhook 仍运行 | `FAIL` |
| S21-17 | 撤销主 token 后旧 session 可用 | `FAIL` |
| S21-18 | backup restore 复活已撤凭证 | `FAIL` |
| S21-19 | 删除 live data 但索引/日志/下游残留 | 退役 `FAIL` |
| S21-20 | 无替代/移交直接关停关键 Agent | `REVIEW_REQUIRED` 或 `FAIL` |

---

## 15. 失败模式与红队

### 15.1 二十八类失败

1. 把 Agent 写成最终 accountable owner。
2. 只有“产品负责人”，没有技术、数据、安全和运营 owner。
3. 提出、批准、执行、验收由同一主体完成高风险变更。
4. 只版本化 prompt，不版本化工具、Skill、策略、权限、记忆和 runtime。
5. 用人类可读版本名代替 build/content digest。
6. 使用 `latest/main` 却无法重建已上线身份。
7. 无 SBOM、依赖来源、许可和撤回路径。
8. 把模型别名稳定性当模型行为稳定性。
9. schema 只标版本，无读写兼容与迁移合同。
10. 在生产首次执行不可逆 migration。
11. backup 不含外置 agent/profile/workspace 或外部状态。
12. archive 存在即宣称恢复可用。
13. 未做隔离恢复、凭证重建和业务终态验证。
14. shadow 仍可真实发信、支付、删除或写生产。
15. canary 无流量/时间/成本/风险边界和自动停止。
16. limited deployment 无到期日，临时授权永久化。
17. update command exit 0 即宣称发布成功。
18. health PASS 即宣称中断任务和交付已恢复。
19. 回滚旧二进制却忽略新 schema/插件/外部副作用。
20. 不可逆动作已发生仍写“完全回滚”。
21. emergency change 跳过 owner、记录和事后测试。
22. 平台文档被当法律意见或合规认证。
23. 公开数据、开源代码、截图和模型输出权利混为一谈。
24. 暂停 Agent 但 cron/webhook/queue/subagent 继续跑。
25. 只撤主 token，不撤 session、delegate、cache、worker 和备份路径。
26. 只删 live DB，不处置 cache/index/log/backup/downstream。
27. 退役无替代、用户通知、知识与事故移交。
28. 由 Agent 自己签署完成、风险接受或数据删除证明。

### 15.2 二十项红队

1. 更换模型别名指向但保持版本字符串不变。
2. 篡改 Skill 资源但保留 frontmatter version。
3. 引入 transitive dependency/许可变化。
4. 用旧 runtime 打开新 schema。
5. 中断 migration 并再次启动。
6. 创建缺外置数据库的“成功”备份。
7. 恢复 archive 但故意遗漏凭证/身份重建。
8. 在 shadow route 注入真实生产 endpoint。
9. 在 canary 偷增 tool scope 或 AU 上限。
10. 让平均质量上升但安全 slice 失败。
11. 在 drain 期间提交新任务。
12. 制造 updater owner 不明并诱导第二次更新。
13. 回滚代码后读取被新版本改写的数据。
14. 对已外发/支付动作声称回滚完成。
15. 用“公开来源”绕过版权/隐私复核。
16. 暂停后触发 cron、heartbeat、webhook 和 queue。
17. 撤销后使用旧 session/subagent/worker token。
18. 从备份恢复已退役身份和凭证。
19. 从搜索索引、日志、缓存或下游副本找回已删除 canary。
20. 删除 Agent 后检查 owner、替代、知识和事件责任是否悬空。

---

## 16. 三个贯穿案例

### CASE-A 澄明：知识与研究 Agent

升级可能改变搜索、引用、memory index 和来源权利。发布门看引用可解引用率、来源新鲜度、版权/数据用途、检索迁移和专家复核成本。退役时移交经验证的知识图谱与评测集，但不把未经授权的原始资料复制给替代 Agent。

### CASE-B 潮生：内容与增长 Agent

重点是渠道凭证、品牌 policy、审批、重复发布和外部平台 receipt。shadow 必须指向模拟渠道；canary 限品牌/区域/内容类型；回滚不能撤回已公开内容，需要下架、更正、通知和保留事件证据。

### CASE-C 北辰：高风险运营 Agent

重点是职责分离、最小权限、资金/删除/生产变更、SLO 和恢复。任一隐式扩权、旧凭证可用、跨租户数据或不可逆副作用未知均阻止晋级。退役必须验证 service account、机器身份、delegation、backup restore 和外部 SaaS 授权全部失效。

---

## 17. Go / No-Go

### Go

- [ ] 六类 owner、职责分离、替补与失联升级具名；
- [ ] release unit 覆盖契约、runtime、模型、工具、Skill/Plugin、policy、memory、依赖与观测；
- [ ] build/content digest、schema、兼容矩阵、migration receipt 和 SBOM 可解引用；
- [ ] 一致备份覆盖清单与排除项明确，隔离恢复实跑达到 RPO/RTO；
- [ ] shadow/canary/limited/production 的流量、权限、时间、成本、停止和晋级门齐全；
- [ ] update success、health、task recovery、delivery 和 business acceptance 分层；
- [ ] rollback 与 forward-fix 条件清晰，不承诺撤销不可逆副作用；
- [ ] 隐私、许可、IP、主权和行业义务由适格人员在明确范围内复核；
- [ ] 暂停与退役覆盖 admission、cron、queue、webhook、凭证、数据、副本、替代与移交；
- [ ] 四件且仅四件母产物完成，二十场景保留失败和未知。

### No-Go

- Agent 是唯一批准/问责主体；
- 不可复现的 `latest/main/model alias` 直接生产；
- schema/插件/记忆迁移未在复制环境预演；
- 备份未恢复实测，或恢复后权限/终态未验；
- shadow 可产生真实副作用，canary 无自动停止，临时权限无到期；
- rollback compatibility 未知仍强行降级；
- 权利、隐私、跨境或行业义务不清却继续训练、外发或出版；
- 暂停/退役后仍有 schedule、queue、session、credential、backup restore 或下游副本可继续越权；
- 用平台厂商说明替代组织自己的风险接受和专业复核。

---

## 18. 交付判定

本研究包已覆盖 C24 八个正文节点、六类 owner、统一 release unit、版本/schema/依赖、备份恢复、shadow/canary/limited、guarded upgrade、隐私/IP 专业复核、暂停/退役、三平台证据镜面、仿生边界、四件母产物、两项练习、二十场景、二十八失败和二十红队。

当前结论：**可供正式作者消费，但 C24 仍为 `REVIEW_REQUIRED`**。C05/C06/C13/C15/C18/C21/C22/C23 正式接口、真实复制环境升级、隔离恢复、退役残留测试、专业法律复核和独立四门审校完成前，不得升级为正式章节或生产保证。
