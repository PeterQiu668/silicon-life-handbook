#!/usr/bin/env python3
"""Insert the 2026.10 original Mermaid figure program into canonical sources."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = ROOT / ".figure-program-2026-10.done"


def figure(number: str, title: str, mermaid: str, explanation: str) -> str:
    return (
        f"**图 {number}　{title}（本书绘制）**\n\n"
        f"```mermaid\n{mermaid}\n```\n\n"
        f"图 {number} {explanation}"
    )


INSERTIONS: list[tuple[str, str, str]] = [
    ("part-I-getting-started/00-formal-volume-zero.md", "## 0.1 这一小时要得到什么", figure("0-1", "卷零最小闭环", "flowchart LR\n  A[任务卡] --> B[本地运行]\n  B --> C[保存产物]\n  C --> D[独立读回]\n  D --> E{PASS / FAIL / REVIEW_REQUIRED}", "展示第一次运行也必须经历任务、行动、产物、读回与裁决；聊天返回只处在链条中间。")),
    ("part-I-getting-started/00-formal-volume-zero.md", "## 0.8 从这里进入全书", figure("0-2", "卷零到九卷的学习路线", "flowchart TD\n  V0[卷零 跑通] --> V1[卷一至三 定义与训练]\n  V1 --> V4[卷四 执行技法]\n  V4 --> V5[卷五至八 能力与治理]\n  V5 --> V9[卷九 实战与认证]", "把全书阅读顺序压缩为五个阶段；读者可以按角色跳转，但执行技法位于能力基础设施之前。")),

    ("manuscript/volume-01/C01-agent-system/chapter.md", "## 1.1 ", figure("1-1", "Agent 系统能力乘积", "flowchart LR\n  M[模型] --> S[Agent 系统表现]\n  R[运行时] --> S\n  T[工具与环境] --> S\n  X[状态与反馈] --> S\n  G[授权与治理] --> S", "说明模型只是系统表现的一项输入；任一关键环节接近零，都可能使整体失效。")),
    ("manuscript/volume-01/C02-training-paradigm/chapter.md", "## 2.1 ", figure("2-1", "训练闭环与生产闭环", "flowchart LR\n  A[评测失败] --> B[训练干预]\n  B --> C[回归与留出]\n  C --> D[受控上岗]\n  D --> E[生产反馈]\n  E --> A", "把能力改变和真实工作连接起来；生产反馈只能成为候选，必须重新进入评测与治理。")),
    ("manuscript/volume-01/C03-strength-standard/chapter.md", "## 3.1 ", figure("3-1", "七维强者剖面", "mindmap\n  root((胜任力))\n    质量\n    泛化\n    安全\n    稳定\n    效率\n    协作\n    可治理", "用七个不可互相替代的维度描述强；安全硬失败不能由其他维度的高分抵消。")),
    ("manuscript/volume-02/C04-role-capability-model/chapter.md", "## 4.1 ", figure("4-1", "从岗位到训练门禁", "flowchart LR\n  J[岗位/JTBD] --> T[任务域]\n  T --> C[能力树]\n  C --> R[风险与NFR]\n  R --> E[评测]\n  E --> G[毕业门禁]", "展示岗位语言如何逐步变成可观察能力、风险控制和毕业条件。")),
    ("manuscript/volume-02/C05-life-contracts/chapter.md", "## 5.1 ", figure("5-1", "七大生命契约关系", "flowchart TD\n  U[USER] --> I[IDENTITY]\n  S[SOUL] --> A[AGENTS]\n  A --> T[TOOLS]\n  H[HEARTBEAT] --> A\n  M[MEMORY] --> A\n  I --> A", "说明七类契约各有职责；人格和操作承诺最终仍要由运行时权限执行。")),
    ("manuscript/volume-02/C06-runtime-architecture/chapter.md", "## 6.1 ", figure("6-1", "六层系统总图", "flowchart TB\n  L1[控制层 Gateway / RPC] --> L2[认知执行层 Agent Loop / Model]\n  L2 --> L3[状态层 Workspace / Session / Memory]\n  L3 --> L4[消息层 Channel / Binding / Queue]\n  L4 --> L5[行动层 Tools / Browser / Nodes / Workers]\n  L5 --> L6[治理层 Identity / Policy / Approval / Audit]\n  L6 -.约束.-> L2", "给出本书的 OpenClaw 主实现观察框架。六层是责任分区，不表示所有请求都按单一方向流动。")),
    ("manuscript/volume-02/C06-runtime-architecture/chapter.md", "## 6.4 ", figure("6-2", "消息到环境终态的数据流", "sequenceDiagram\n  participant U as 用户/通道\n  participant G as Gateway\n  participant A as Agent Runtime\n  participant T as Tool/Node\n  participant E as Environment\n  U->>G: 请求\n  G->>A: 路由+会话\n  A->>T: 已授权动作\n  T->>E: 改变/读取\n  E-->>A: 终态证据", "把消息成功、模型输出、工具调用和环境终态分开，避免把中间返回当作业务完成。")),
    ("manuscript/volume-02/C06-runtime-architecture/chapter.md", "## 6.7 ", figure("6-3", "治理横切六层", "flowchart LR\n  I[Identity] --> P[Policy]\n  P --> A[Approval]\n  A --> S[Sandbox]\n  S --> O[Audit]\n  O --> R[Recovery]\n  R -.反馈.-> P", "展示身份、策略、审批、隔离、审计和恢复如何横切系统，而不是集中在一个安全提示词中。")),
    ("manuscript/volume-02/C06-runtime-architecture/chapter.md", "## 6.8 ", figure("6-4", "最小可训单体边界", "flowchart TD\n  Q[固定任务与评测] --> A[单一 Agent Runtime]\n  A --> W[隔离 Workspace]\n  A --> T[最小工具集]\n  A --> L[日志与检查点]\n  T --> V[可读回环境]\n  V --> Q", "定义开始训练前的最小闭环：任务、隔离执行、有限工具、观测和环境验证同时存在。")),
    ("manuscript/volume-03/C07-evaluation-system/chapter.md", "## 7.1 ", figure("7-1", "D22 四层评测与横切安全", "flowchart TB\n  T[training] --> R[regression]\n  R --> H[holdout]\n  H --> W[representative_real_world]\n  S[security red-team] -.横切.-> T\n  S -.横切.-> R\n  S -.横切.-> H\n  S -.横切.-> W", "强调安全红队是横切切片，不是可以用平均分补偿的第五层数据集。")),
    ("manuscript/volume-03/C08-training-system/chapter.md", "## 8.1 ", figure("8-1", "受控训练轮次", "flowchart LR\n  F[可重放失败] --> H[根因假设]\n  H --> C[单变量候选]\n  C --> T[训练]\n  T --> R[回归/留出/安全]\n  R --> D{并入/限域/停训/回滚}", "把训练定义为受控能力变更链；训练集提分只是中间信号。")),
    ("manuscript/volume-03/C09-interaction-system/chapter.md", "## 9.1 ", figure("9-1", "任务完成四轴", "flowchart LR\n  T[任务状态] --> G{完成判定}\n  M[消息状态] --> G\n  A[Artifact状态] --> G\n  E[环境终态] --> G\n  G --> D[三面完成]", "展示四类状态必须分别记录；任一轴的绿色标记都不能单独证明业务完成。")),
    ("manuscript/volume-04/C10-task-decomposition-planning/chapter.md", "## 10.1 ", figure("10-1", "任务图与滚动重规划", "flowchart LR\n  O[可验证终态] --> D[任务图]\n  D --> Q[READY 队列]\n  Q --> A[行动]\n  A --> V[环境读回]\n  V --> R{触发重规划?}\n  R -- 是 --> D\n  R -- 否 --> Q", "说明计划不是一次生成的步骤表，而是根据环境证据持续更新的执行状态机。")),
    ("manuscript/volume-04/C11-externalized-working-memory/chapter.md", "## 11.1 ", figure("11-1", "外部化工作记忆栈", "flowchart TB\n  T[任务卡] --> P[PLAN]\n  P --> Q[TODO]\n  Q --> C[CHECKPOINT]\n  S[SCRATCHPAD] --> E[EVIDENCE]\n  E --> C\n  C --> R[恢复/交接]", "区分承诺、动作队列、临时探索、证据和恢复快照，避免一份摘要承担所有职责。")),
    ("manuscript/volume-04/C12-self-verification-recovery-delegation/chapter.md", "## 12.1 ", figure("12-1", "稳健执行六步循环", "flowchart LR\n  C[声明] --> V[独立验证]\n  V --> X[反例]\n  X --> D{死胡同?}\n  D -- 是 --> R[回退/重规划]\n  D -- 否 --> P[并行探索]\n  P --> S[预注册收敛]\n  S --> C", "把怀疑、反例、停止、回退与收敛变成可执行步骤；任何一步都不授予自我批准权。")),
    ("manuscript/volume-05/C13-context-memory/chapter.md", "## 13.1 ", figure("13-1", "记忆生命周期总图", "flowchart LR\n  O[观察/候选] --> W{写入准入}\n  W --> S[存储+来源]\n  S --> R{检索授权}\n  R --> U[使用]\n  U --> C[纠错/更新]\n  C --> A[归档/过期/删除]\n  A -.残余验证.-> S", "展示记忆从候选到删除验证的完整生命周期；写入价值与保存权利是两道不同的门。")),
    ("manuscript/volume-05/C13-context-memory/chapter.md", "## 13.4 ", figure("13-2", "压缩与保真检查", "flowchart TD\n  C[原上下文] --> F[冻结不变量]\n  F --> P[压缩/摘要]\n  P --> D[差异检查]\n  D --> V{目标/边界/授权/否定事实完整?}\n  V -- 否 --> R[失效并恢复]\n  V -- 是 --> N[新窗口]", "把压缩视为有损转换；只有不可丢字段验证通过，压缩产物才可继续使用。")),
    ("manuscript/volume-05/C13-context-memory/chapter.md", "## 13.6 ", figure("13-3", "纠错与删除传播", "flowchart LR\n  S[原始来源] --> M1[记忆条目]\n  M1 --> M2[摘要/索引]\n  M2 --> O[输出/产物]\n  X[更正或删除请求] --> M1\n  M1 -.传播.-> M2\n  M2 -.传播.-> O\n  O --> R[残余报告]", "说明更正和删除必须沿派生链传播，并报告备份、已发布产物等无法即时消除的残余。")),
    ("manuscript/volume-05/C14-tool-mcp-engineering/chapter.md", "## 14.1 ", figure("14-1", "工具风险与控制梯度", "flowchart LR\n  R[只读] --> W[内部写入]\n  W --> X[对外发送]\n  X --> P[资金/身份/生产]\n  P --> D[删除/破坏]\n  R -.控制增强.-> D", "随着影响、不可逆性和敏感性上升，审批、隔离、读回与恢复要求同步增强。")),
    ("manuscript/volume-05/C15-skill-engineering/chapter.md", "## 15.1 ", figure("15-1", "能力供应链", "flowchart LR\n  S[来源] --> V[版本/签名]\n  V --> T[测试/权限审查]\n  T --> R[Registry]\n  R --> L[渐进加载]\n  L --> O[运行观测]\n  O --> X[撤回/替代]", "把 Skill 和 Plugin 当作有来源、版本、权限、测试与撤回责任的供应链对象。")),
    ("manuscript/volume-06/C16-proactivity-automation/chapter.md", "## 16.1 ", figure("16-1", "信号到安静策略", "flowchart LR\n  S[信号] --> D{有意义变化?}\n  D -- 否 --> Q[保持安静]\n  D -- 是 --> P[提案]\n  P --> A{授权允许?}\n  A -- 否 --> E[升级/等待]\n  A -- 是 --> X[受控执行]", "说明主动性起点是变化判断；没有新信息或没有授权时，正确动作可以是安静和等待。")),
    ("manuscript/volume-06/C17-autonomy-authorization/chapter.md", "## 17.1 ", figure("17-1", "AU 自主阶梯与影响边界", "flowchart LR\n  L0[AU-L0 回答] --> L1[AU-L1 发现]\n  L1 --> L2[AU-L2 提案]\n  L2 --> L3[AU-L3 准备]\n  L3 --> L4[AU-L4 受控执行]\n  L4 -.不自动产生.-> O[组织责任]", "展示自主等级描述可行动范围，不代表成熟度，也不会自动转移人类责任。")),
    ("manuscript/volume-06/C17-autonomy-authorization/chapter.md", "## 17.4 ", figure("17-2", "授权状态机与收缩路径", "stateDiagram-v2\n  [*] --> 未授权\n  未授权 --> 待审批: 提交对象/动作/内容/影响\n  待审批 --> 已授权: scope+期限+主体绑定\n  已授权 --> 已执行: 动作+读回\n  已授权 --> 已收缩: 风险/不确定性上升\n  已收缩 --> 已撤销\n  已执行 --> 已过期\n  已撤销 --> [*]", "给出授权从申请到过期的状态机。任何身份、范围、时效或风险变化都优先走收缩路径。")),
    ("manuscript/volume-06/C17-autonomy-authorization/chapter.md", "## 17.7 ", figure("17-3", "授权升级与降级门", "flowchart TD\n  E[评测与生产证据] --> G{硬门全过?}\n  G -- 否 --> D[降级/暂停/撤销]\n  G -- 是 --> H[人类批准精确 scope]\n  H --> T[限时试运行]\n  T --> R{复核}\n  R -- 失败 --> D\n  R -- 通过 --> K[维持或小步扩大]", "说明能力证据只能支持授权决策，不能由 Agent 自行把高分兑换成更高权限。")),
    ("manuscript/volume-06/C18-drift-improvement-governance/chapter.md", "## 18.1 ", figure("18-1", "受控改进回路", "flowchart LR\n  O[观察] --> H[假设]\n  H --> E[隔离实验]\n  E --> V[评估]\n  V --> D{固化/回滚/停训}\n  D --> B[新基线]\n  B --> O", "把自我改进限制为提出候选和运行实验；目标、权限和发布仍由外部治理决定。")),
    ("manuscript/volume-07/C19-multi-agent-organization/chapter.md", "## 19.1 ", figure("19-1", "最小多 Agent 组织", "flowchart TD\n  M[主理 Agent] --> R[研究 Agent]\n  M --> X[执行 Agent]\n  R --> A[Artifact 仓]\n  X --> A\n  A --> V[独立评审 Agent]\n  V --> M", "展示最小组织的角色、产物和评审路径；多 Agent 价值来自边界清楚，而非数量。")),
    ("manuscript/volume-07/C20-routing-handoff-concurrency/chapter.md", "## 20.1 ", figure("20-1", "路由与让位决策", "flowchart TD\n  T[任务] --> C{能力+权限+负载+数据位置}\n  C --> S[胜任者]\n  C --> Y[让位/求助]\n  S --> E[执行]\n  Y --> H[交接]", "说明路由必须同时考虑胜任力和权限；找不到合适执行者时，让位优于伪装胜任。")),
    ("manuscript/volume-07/C20-routing-handoff-concurrency/chapter.md", "## 20.4 ", figure("20-2", "Handoff 时序", "sequenceDiagram\n  participant A as 交出方\n  participant S as 状态/产物库\n  participant B as 接收方\n  participant O as 任务Owner\n  A->>S: 冻结版本+已完成/未完成/风险\n  A->>B: handoff_id+最小上下文\n  B->>S: 读取并验证\n  B-->>A: ACK / REJECT / ASK\n  B-->>O: 接管范围与剩余风险", "规定交出、冻结、读取、确认和责任接管的顺序；没有 ACK 的发送不等于交接完成。")),
    ("manuscript/volume-07/C20-routing-handoff-concurrency/chapter.md", "## 20.5 ", figure("20-3", "并发分支与合并点", "flowchart LR\n  P[父任务] --> A[隔离分支A]\n  P --> B[隔离分支B]\n  P --> C[隔离分支C]\n  A --> M{预注册合并}\n  B --> M\n  C --> M\n  M --> V[冲突/证据/终态验证]", "展示并行必须有隔离工作区、统一 Schema 和显式合并点；共享写入未经控制会扩大失败面。")),
    ("manuscript/volume-07/C21-a2a-artifact-trust/chapter.md", "## 21.1 ", figure("21-1", "A2A 对象与信任链", "flowchart LR\n  C[Agent Card] --> T[Task]\n  T --> M[Message/Event]\n  T --> A[Artifact]\n  I[身份/签名/策略] -.验证.-> C\n  I -.验证.-> A\n  A --> V[运行验收]", "区分发现、任务、消息、事件和产物；签名证明来源，不证明内容正确或业务完成。")),
    ("manuscript/volume-08/C22-security-trust-boundary/chapter.md", "## 22.1 ", figure("22-1", "SEC-L0—SEC-L8 九层防御与攻击面", "flowchart TB\n  L0[SEC-L0 资产与目标] --> L1[SEC-L1 身份]\n  L1 --> L2[SEC-L2 数据]\n  L2 --> L3[SEC-L3 模型与上下文]\n  L3 --> L4[SEC-L4 工具与协议]\n  L4 --> L5[SEC-L5 执行隔离]\n  L5 --> L6[SEC-L6 审批与策略]\n  L6 --> L7[SEC-L7 观测与响应]\n  L7 --> L8[SEC-L8 恢复与问责]", "给出九层防御主图；攻击者可从内容、身份、工具、供应链和恢复面跨层移动，因此单点防护不足。")),
    ("manuscript/volume-08/C22-security-trust-boundary/chapter.md", "## 22.4 ", figure("22-2", "执行位置与信任边界", "flowchart LR\n  A[Agent Runtime] --> S[Sandbox]\n  S --> H[Host]\n  S --> N[Node/Worker]\n  N --> X[外部服务]\n  P[Policy/Approval] -.约束.-> S\n  E[Egress] -.过滤.-> X", "说明 Sandbox mode、scope 和 backend 共同决定实际边界；工具描述不会自动形成隔离。")),
    ("manuscript/volume-08/C22-security-trust-boundary/chapter.md", "## 22.6 ", figure("22-3", "间接注入攻击路径", "flowchart LR\n  U[不可信网页/邮件] --> C[上下文]\n  C --> M[模型决策]\n  M --> T[工具调用]\n  T --> D[数据/凭证/外发]\n  G[taint+最小权限+审批+读回] -.阻断.-> T", "展示外部内容如何经上下文影响工具；防御需要来源标记、最小权限、确定性门和终态验证共同作用。")),
    ("manuscript/volume-08/C23-observability-cost-reliability/chapter.md", "## 23.1 ", figure("23-1", "业务承诺到 SLO", "flowchart LR\n  B[业务承诺] --> S[SLI]\n  S --> O[SLO]\n  O --> E[错误预算]\n  E --> A[告警/降级/停机]", "把可观测指标锚定到业务承诺；组件绿色不等于客户结果已经实现。")),
    ("manuscript/volume-08/C23-observability-cost-reliability/chapter.md", "## 23.2 ", figure("23-2", "最小事件链", "flowchart LR\n  T[task.created] --> A[authorization.checked]\n  A --> R[routing.decided]\n  R --> M[model.called]\n  M --> X[tool.executed]\n  X --> H[handoff.acked]\n  H --> E[environment.verified]\n  E --> D[delivery.accepted]", "定义从任务创建到业务接受的最小事件链，每个事件都可关联 task、actor、版本、证据和成本。")),
    ("manuscript/volume-08/C23-observability-cost-reliability/chapter.md", "## 23.6 ", figure("23-3", "可靠性恢复阶梯", "flowchart TD\n  F[故障] --> T{可安全重试?}\n  T -- 是 --> I[幂等重试]\n  T -- 否 --> C[取消/隔离]\n  I --> V{终态正确?}\n  V -- 否 --> P[补偿/回退]\n  P --> D[降级/人工接管]\n  V -- 是 --> R[恢复]", "给出重试、取消、补偿、回退和降级的选择顺序，防止把所有故障都交给重试。")),
    ("manuscript/volume-08/C24-governance-release-lifecycle/chapter.md", "## 24.1 ", figure("24-1", "发布与全生命周期责任链", "flowchart LR\n  D[定义] --> B[构建]\n  B --> V[验证]\n  V --> R[发布]\n  R --> O[运行]\n  O --> U[升级/回滚]\n  U --> X[退役/数据处置]\n  G[业务/数据/安全/风险Owner] -.签字.-> R", "展示从定义到退役的连续责任；发布批准不能替代运行、升级和数据处置责任。")),
    ("manuscript/volume-09/C25-thirty-day-training-camp/chapter.md", "## 25.1 ", figure("25-1", "30天训练营甘特图", "gantt\n  title 30天训虾训练营\n  dateFormat  X\n  axisFormat 第%d天\n  section 定义与基线\n  岗位/风险/基线 :0, 4\n  section 契约与容器\n  契约/权限/工具 :4, 4\n  section 训练与真实任务\n  集中训练/回归 :8, 7\n  真实任务/记忆/主动性 :15, 7\n  section 压力与认证\n  迁移/故障/红队 :22, 5\n  留出/毕业 :27, 4", "按天展示四阶段训练节奏；甘特条只表示最早安排，不绕过每日硬门与失败退出。")),
    ("manuscript/volume-09/C25-thirty-day-training-camp/chapter.md", "## 25.3 ", figure("25-2", "训练营每日证据回路", "flowchart LR\n  P[当日计划] --> T[训练/任务]\n  T --> E[证据包]\n  E --> R[晚间复盘]\n  R --> G{继续/回归/停训}\n  G --> P", "说明每天都要形成可保存的计划、运行、证据与决定，而不是到第 30 天一次性补材料。")),
    ("manuscript/volume-09/C25-thirty-day-training-camp/chapter.md", "## 25.6 ", figure("25-3", "毕业门禁", "flowchart TD\n  H[holdout] --> G{七维+硬门}\n  W[representative_real_world] --> G\n  S[security red-team] --> G\n  C[成本/恢复] --> G\n  G -- 全过 --> P[限域上岗]\n  G -- 可补证 --> R[REVIEW_REQUIRED]\n  G -- 硬失败 --> F[FAIL/停训]", "把毕业结论连接到留出、代表性真实任务、安全、成本和恢复，任何硬失败都不能用总分抵消。")),
    ("manuscript/volume-09/C26-case-evidence-lab/chapter.md", "## 26.1 ", figure("26-1", "贯穿案例证据包", "flowchart LR\n  B[基线] --> I[干预]\n  I --> T[轨迹]\n  T --> A[Artifact]\n  A --> O[环境终态]\n  O --> F[失败分布]\n  F --> M[迁移限制]", "规定澄明、潮生和北辰都用同一证据结构呈现，避免只展示成功故事。")),
    ("manuscript/volume-09/C27-maturity-continuous-certification/chapter.md", "## 27.1 ", figure("27-1", "成熟度与持续认证", "flowchart LR\n  L0[MAT-L0 工具] --> L1[MAT-L1 可用助手]\n  L1 --> L2[MAT-L2 稳定岗位]\n  L2 --> L3[MAT-L3 受控自主]\n  L3 --> L4[MAT-L4 可治理组织]\n  L4 --> L5[MAT-L5 持续认证生态]\n  X[重大变更] -.触发重测.-> L0", "展示成熟度是组织能力阶梯；重大变更触发针对性重测，而非永久保留原等级。")),

    ("manuscript/appendices/G-evaluation-certification-baseline-library.md", "## ", figure("90-1", "公开基准能力覆盖地图", "flowchart LR\n  S[SWE-bench 软件变更] --> D[七维/D22校准]\n  T[τ-bench 对话工具策略] --> D\n  W[WebArena 网页环境] --> D\n  G[GAIA 通用助手] --> D\n  D --> L[本地岗位与风险评测]", "说明四个公开基准只能提供局部外部参照，最终仍需映射到本地任务、预算、风险和四层数据。")),
    ("manuscript/appendices/G-evaluation-certification-baseline-library.md", "## ", figure("90-2", "公开分数到胜任力的校准路径", "flowchart LR\n  P[公开分数] --> R[复现版本/脚手架/成本]\n  R --> M[七维映射]\n  M --> D[D22 四层缺口]\n  D --> J[岗位任务补测]\n  J --> V[有限范围结论]", "把公开分数转成可审计的有限结论；跳过复现、映射和补测时，不得宣称岗位胜任。")),
    ("manuscript/appendices/H-security-operations-incident-handbook.md", "## ", figure("91-1", "中国法规适用性分流", "flowchart TD\n  A[Agent项目] --> P{处理个人信息?}\n  P -- 是 --> PIPL[个人信息保护检查]\n  A --> D{开展数据处理?}\n  D -- 是 --> DSL[数据安全检查]\n  A --> G{向境内公众提供生成式AI服务?}\n  G -- 是 --> GEN[暂行办法/安全评估/备案评估]\n  A --> ALG{具有规定的算法服务属性?}\n  ALG -- 是 --> FIL[算法/深度合成/模型备案评估]", "用于触发合规评估而非给出法律结论；实际适用性必须由组织法务和主管机关口径复核。")),
    ("manuscript/appendices/H-security-operations-incident-handbook.md", "## ", figure("91-2", "安全事件处置时序", "sequenceDiagram\n  participant A as Agent/监控\n  participant S as 安全Owner\n  participant O as 业务/数据Owner\n  participant E as 外部环境\n  A->>S: 检测+证据\n  S->>E: 隔离/停止\n  S->>O: 影响与法定义务评估\n  O->>E: 修复/通知/补偿\n  E-->>S: 恢复验证", "把检测、止损、责任评估、修复和恢复验证串联，避免只修技术错误而遗漏主体通知与数据责任。")),
    ("manuscript/appendices/I-terms-sources-rights-versioning.md", "## ", figure("92-1", "外部术语到本书术语的桥", "flowchart LR\n  E[外部术语] --> M[语义核对]\n  M --> B[本书受控术语]\n  B --> O[定义Owner章节]\n  O --> A[产物/评测/治理]\n  A -.差异说明.-> E", "说明词汇对照不是简单翻译；每个外部术语都要经过适用范围和差异说明后进入本书体系。")),
    ("manuscript/appendices/I-terms-sources-rights-versioning.md", "## ", figure("92-2", "来源权利与事实双门", "flowchart TD\n  S[候选材料] --> F{事实可核验?}\n  F -- 否 --> X[排除/待核]\n  F -- 是 --> R{有使用权/可合理引用?}\n  R -- 否 --> B[RIGHTS-BLOCKED]\n  R -- 是 --> C[进入正文并标来源身份]\n  B --> I[独立重构方法/替代一手来源]", "把事实可信与使用权分成两道门；课程页面即使提供启发，未获授权也不能成为全书中枢架构的唯一来源。")),
]


def main() -> int:
    if MARKER.exists():
        print("SKIP figure program already inserted")
        return 0
    for relative, anchor, block in INSERTIONS:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        number_line = block.splitlines()[0]
        if number_line in text:
            continue
        if anchor not in text:
            raise RuntimeError(f"anchor not found in {relative}: {anchor!r}")
        text = text.replace(anchor, block + "\n\n" + anchor, 1)
        path.write_text(text, encoding="utf-8")
    MARKER.write_text("2026-10-01\n", encoding="utf-8")
    print(f"PASS inserted {len(INSERTIONS)} formal figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
