# 执行记录

## 2026-09-30 · 出版级主干重构

### 结果

- 新增 18,129 字符、1,062 行的连续出版主稿，按 Agent 生命周期组织为九篇。
- 新增 Agent 渐进读取入口，避免一次性加载约 8.8 万行资料。
- 新增机器可读 `BOOK-MANIFEST.yaml`，明确正式书目、稳定基线、深度层、操作层和出版排除项。
- 新增 `SOURCES.md`，记录三门课程、OpenClaw、MCP、A2A、Agent Skills、OpenAI Evals 与 Anthropic Agent 工程资料的来源边界。
- 新增编辑审计，完成初版八卷、三门课程和现代工程层的覆盖映射。
- 新增状态、关键决策、可复用经验和结构校验脚本。
- 修复 12 个主干深度章节指向根级 `_appendix-*` 的错误相对路径。
- 修复 `_appendix-api/README.md` 中因章节重编号产生的 11 组目录链接。
- 未删除、移动或改名旧版、现有深度章节、附录、备份与编辑底稿。

### 当前事实复核

- 本机 `openclaw --version`：`OpenClaw 2026.9.6 (eb377ac)`。
- npm `openclaw/latest`：`2026.9.6`。
- GitHub latest release：`v2026.9.6`，发布时间 2026-09-23。
- GitHub 存在 `v2026.9.7` tag，但复核时不属于 npm latest / GitHub latest release，因此只记入前沿观察。
- MCP latest release：`2026-07-28`。
- A2A latest release：`v1.0.1`。

### 验证

```text
python3 scripts/validate-book.py
OK canonical files: 5
OK markdown files scanned: 76
OK local links checked: 888
OK manuscript lines: 1062
OK manuscript chars: 18129
PASS publication layer is structurally valid
```

### Harness 收口

- 已运行全局 `doctor.mjs`，但全局 Harness 本身未通过：它在当前兼容入口下无法找到注册表中的多个 `Documents/Codex/projects/*` 项目，还报告 `clients/README.md`、`operations/README.md` 缺失及废弃 `js_repl` 开关。这些问题与本手册目录无关，本次未越权修改。
- 已尝试 `refresh.mjs`；该脚本会先调用同一个 doctor，因此被上述全局问题阻断，未完成索引刷新。
- 本手册自身的结构、链接、版本与章节闭环校验通过。

### 仍需后续完成

- 深度层逐章去重、更新 2026.9.4 旧基线和收敛绝对化主张。
- 用真实训练项目跑通 30 天路径并形成公开基准案例。
- 获得课程逐字稿或作者审定材料。
- 做第三方引用、商标、截图与代码片段的版权复核。
- 完成图表、排版、出版社体例和印前校对。

## 2026-09-30 · 正式出版版三级母架构

### 结果

- 将现有 `2026.9-RC1` 明确定位为候选内容底稿，不再视为可直接上线的正式版。
- 新建 `00-正式出版版-三级内容框架-v1.md`，形成 8 卷、24 章、146 个正文三级节点。
- 建立从“定义强者”到“实战与认证”的完整成长主线。
- 建立卷前、卷后、7 组附录、12 项章节写作合同和旧稿覆盖映射。
- 建立主动执行计划，将作者目录确认设为多 Agent 分章写作前的强制门禁。
- 未修改 `BOOK-MANIFEST.yaml`，未派发章节 Agent，未删除、移动或改名原有资料。

### 结构验证

```text
volume_count=8
chapter_count=24
body_section_count=146
```

```text
python3 scripts/validate-book.py
OK markdown files scanned: 79
OK local links checked: 888
PASS publication layer is structurally valid
```

### Harness 收口

- 已重新运行全局 `doctor.mjs`；它仍因 `Documents/Hummer` 兼容入口与注册项目实际路径不一致、`clients/README.md` 和 `operations/README.md` 缺失、废弃 `js_repl` 开关而不通过。
- 已尝试运行 `refresh.mjs`；因其前置 doctor 失败而终止，未刷新全局索引。
- 上述为全局 Harness 环境问题，本手册的结构和链接校验独立通过；本次未越权修改全局配置。

### 待作者确认

- 书名与副标题。
- 八卷主线和 24 章的取舍。
- “硅基生命”是核心学科概念还是管理隐喻。
- OpenClaw 是否保持在实现参考层。
- 是否接受七维可测领先标准。

## 2026-09-30 · 正式出版版进入多 Agent 生产

### 结果

- 作者确认八卷二十四章主线，要求保留硅基生命仿生解释，并把 OpenClaw、Hermes、Muse 与最新实践纳入正式手册。
- 建立 `00-正式出版版-三级内容框架-v2.md`：8 卷、24 章、178 个正文三级节、9 组附录。
- 建立 `docs/research/legacy-content-map.md`：逐章映射初版、9 月版、v4/v5 探索，标记保留、重写、降级和淘汰。
- 建立 `docs/research/platform-and-frontier-evidence.md`：24 章证据路由、三平台映射、51 个一手来源和禁写主张。
- 建立 `docs/editorial/BOOK-QUALITY-STANDARD.md`：15 项 P0、百分制评分、章节 DoD 和五道门禁。
- 建立 `docs/editorial/TERMINOLOGY-REGISTRY.yaml`：56 项受控术语和产品边界。
- 建立 `docs/editorial/CHAPTER-CARDS.md`：24 张章节卡、唯一概念所有权与无环依赖图。
- 建立 `manuscript/` 正式书稿区、卷前稿和专项结构校验脚本。
- 启动卷一第 1—3 章独立章节生产包写作；旧稿、RC1 和现有主稿均未覆盖。

### 当前验证

```text
framework volumes: 8
framework chapters: 24
framework body sections: 178
controlled terms: 56
chapter cards: 24
```

### 下一门禁

- 第 1—3 章完成初稿后进行循环交叉审校；
- 事实审校、练习试跑和总编审校通过前，章节状态不得标记为正式完成；
- 卷一稳定后再进入第 4—6 章，避免核心定义漂移。

## 2026-09-30 · 卷三初稿齐套与 C15—C20 风险预研

### 结果

- 卷一 C01—C03、卷二 C04—C06 已完成五门审校并保持 `release_candidate`；六章中文正文约 101,800 字符。
- C07—C09 由三个独立作者完成正式初稿生产包，分别为 18,632、16,391、15,157 个中文字符；每章均含正文、证据账本、严格限定的三件母产物、练习、作者自检与合成运行证据。
- C07 合成基线含 8 个任务、24 个试次，结果为 13 PASS、8 FAIL、3 REVIEW_REQUIRED；五类安全硬失败均未被综合分抵消。
- 非作者在两个全新临时目录独立复现 C07：任务数、试次数、门禁分布与两个输出 hash 均一致；X-C07-01 在合成范围通过，X-C07-02 与真实人类/专家校准保持 `REVIEW_REQUIRED`。
- C08 完成三轮单变量训练实验；训练集虽达 6/6，但留出集 4/5、安全集 2/3，最终正确裁决为 `STOP_AND_ROLLBACK_CANDIDATES`，没有伪称能力提升。
- C09 完成正常闭环、UI 假完成、过期上下文、跨客户污染和群聊污染五类合成场景；真实 Runtime 验证继续保留为缺口。
- 新增 C15、C17、C18、C19、C20 前置研究包；C05—C20 现均有研究底座。C20 研究包为 20,827 字符、490 行，18 个外部一手来源全部返回 HTTP 200。
- D19 冻结 `MAT-L0—MAT-L5` 与 `AU-L0—AU-L4` 两个命名空间；D20 冻结五类漂移并把记忆/上下文定义为跨类型状态与证据源。
- C10 已进入正式初稿生产；C07 正在进行非作者事实/交叉审校，C08 正在进行独立实践复现。

### 验证

```text
python3 scripts/validate-formal-manuscript.py
OK framework volumes: 8
OK framework chapters: 24
OK framework body sections: 178
OK controlled terms: 87
OK chapter packages present: 9
PASS 1 warning(s): 生产尚未完成，缺少 15 个后续章节包

python3 scripts/validate-book.py
OK markdown files scanned: 220
OK local links checked: 1250
PASS publication layer is structurally valid

git diff --check -- .
PASS
```

### 边界

- C07—C09 当前只通过初稿门；非作者四门未全部通过，不得并入正式 manifest。
- C07/C08/C09 的运行证据是确定性合成 harness，不是 OpenClaw、Hermes、Muse 的生产 Runtime 证明。
- C19/C20 为前置研究，不是正式章节，也不证明任一部署达到生产安全或 SLO。
- C20 的 OpenTelemetry、OpenAI、Hermes 动态文档仅作为核验日资料；固定实现事实与动态事实已分开标记。

## 2026-09-30 · 研究底座齐套、C10 独立审校与 C07 校准红队补强

### 结果

- C22 前置研究包完成；C05—C24 现均有逐章研究底座。C22 覆盖 Day 0—30、G0—G6、六类毕业证据、CASE-A/B/C 路径和 24 项红队/故障，33 个唯一一手来源链接本轮均返回 HTTP 200；合成、沙箱和真实 30 天运行仍明确为未执行。
- C10 非作者事实门与交叉门均以限制通过：24/24 claim 与 40/40 来源闭合，14 个本地源存在，26 个外链本轮均返回 HTTP 200；固定发布事实、动态文档和 Muse VENDOR-CLAIM 已分层。
- C10 非作者实践者在两个 fresh temp 目录复跑作者 harness；12 task / 24 trial、12 PASS / 10 FAIL / 2 REVIEW_REQUIRED 与作者保存输出逐字节一致。X-C10-01 在合成路由范围通过，X-C10-02 因未执行状态化删除、备份恢复不复活和并发 writer fence 继续为 REVIEW_REQUIRED。
- C07 新增 X-C07-02 八类机器可执行校准红队：顺序、冗长、身份、裁判注入、正确答案/错误轨迹、错误 gold、缺证和版本漂移。八个植入风险均被拦截，机器控制门通过；尚待另一名非作者复跑，真实人类/专家校准继续为 REVIEW_REQUIRED。
- C08 修补后的独立实践回归完成：两个 fresh temp 输出逐字节一致，四个规范数据层、横切安全套件、S01—S03=`holdout × adversarial`、真实任务样本为 0 与最终 `STOP_AND_ROLLBACK_CANDIDATES` 均复核；总实践门因真实训练/回滚未做保持 REVIEW_REQUIRED。C09 已派发非作者事实与交叉审校，C11 正式作者稿继续生产。

### 验证

```text
python3 scripts/validate-formal-manuscript.py
C01—C10 既有章节检查通过；全量命令因 C11 正在并发写作、尚未达到篇幅和必需段落而暂时 FAIL，待作者收口后重跑

python3 scripts/validate-book.py
PASS

git diff --check -- manuscript/volume-03/C07-evaluation-system/review/runs
PASS

git diff --check -- manuscript/volume-04/C10-context-memory/review
PASS
```

### 边界

- 前置研究不是正式章节；外链可访问不等于主张永久有效。
- 所有现有 C07—C10 运行仍是离线合成证据，不是 OpenClaw、Hermes 或 Muse 的真实生产比较。
- C07 真人/专家校准、C10 状态化删除恢复、C22 真实 30 天纵向训练和平台级沙箱演练均未获得本轮实践证据。

## 2026-09-30 · C07/C10 机器实践补强闭环与 C11 独立事实/交叉门

### 结果

- C07 X-C07-02 八类机器校准红队完成双 fresh temp 独立复跑；聚合停止理由遗漏经作者修补后再次独立回归，8 个非 PASS 变体与 8 个 stop reason 一一对应。机器控制门 PASS，真实 model/human/expert 校准和全章实践门仍为 REVIEW_REQUIRED。
- C10 X-C10-02 新增状态化内存实验并完成非作者复跑：9 个场景为 5 PASS / 4 FAIL；四种遗忘、声明删除面与 residual、restore+tombstone、late-write+二扫通过，Compaction 丢约束、无 tombstone 恢复、无二扫并发写入和只删 index 均被拦截。合成控制门 PASS，真实存储/备份/Provider 门仍为 REVIEW_REQUIRED。
- C11 正式作者包完成：正文 18,154 CJK，25 条 claim、三件母产物、两项练习和 18 trial 作者运行齐备。
- C11 非作者事实门与交叉门均带限制通过：25/25 claim 闭合，41/41 sources 使用，15/15 本地路径存在，26/26 外链本轮 HTTP 200；MCP fixed、OpenClaw fixed、Hermes fixed/dynamic、Muse VENDOR-CLAIM 分层通过。
- C11 章节卡补入 C09/C10 上游依赖与 C21 下游消费者，使实际 tool receipt、Memory taint 与退役撤权数据流和依赖图一致。
- C12 正式作者生产已启动。

### 验证

```text
C07 post-fix independent regression: PASS
C10 stateful independent reproduction: PASS_IN_SYNTHETIC_MACHINE_SCOPE
C11 evidence/frontmatter/source closure: PASS
python3 scripts/validate-book.py: PASS
git diff --check -- C07/C10/C11 affected paths: PASS
```

### 边界

- C07/C10 的机器门 PASS 都不能外推为真实 grader、物理删除、恢复或平台安全证明。
- C11 作者合成运行尚待独立实践复现；事实/交叉门不批准实践、编辑、总编或 RC。
- C12—C24 尚未形成全部正式章节，当前 full formal validator 的生产未完成提示不代表既有章节回归。

## 2026-09-30 · C09 三门独立审校完成

### 结果

- C09 非作者事实门与交叉门均带限制通过：14/14 claim 闭合，17/17 外链 HTTP 200，12/12 本地证据存在；OpenClaw/Hermes 固定锚点、A2A v1.0.1 固定规范与 Muse VENDOR-CLAIM 分层通过。
- 为 A2A 补入 v1.0.1 固定规范来源，动态 latest 只作核验日交叉检查；D21 的技术执行、交付可见、业务/环境验收三层和任务/消息/Artifact/环境四轴均保持。
- 非作者实践者建立 reviewer-owned harness，在两个 fresh temp 副本复现 8 个场景：2 PASS、5 FAIL、1 REVIEW_REQUIRED，字节与 JSON 语义一致。
- X-C09-01 在合成交付闭环范围通过，X-C09-02 在已测试的合成污染/权限范围通过；UI 假完成、跨主体、完整群聊、留出污染和 DENIED 回流均为非补偿失败。
- 全章实践门因真实 OpenClaw/Hermes、真实渠道、Provider 缓存、Memory/Skill 持久层和业务 owner 验收未执行而保持 REVIEW_REQUIRED。

### 验证与边界

- C09 YAML/frontmatter、哈希绑定、三件母产物和限定 diff：PASS；
- `validate-book.py`：PASS；
- full formal validator 的当前错误只来自并发中的 C12 未成稿，不归因于 C09；
- 同一非作者 Agent 承担 C09 事实/交叉与实践复现，但职责记录分开，未自批编辑、总编或 RC。

## 2026-09-30 · C08—C13 定义回归、实践补强与正式生产

### 结果

- C08 事实门通过；交叉门发现的两处下游定义冲突完成修补并由非作者回归关闭：训练/生产双闭环归 C02，C08 只拥有训练干预、轮次、双三角、停训和候选证据链；C22 只消费“目标—行为—反馈 / 任务—能力—证据”双三角。C08 事实/交叉门现均通过（带限制），真实训练实践仍为 REVIEW_REQUIRED。
- C11 作者路由基线由非作者双目录复现后，独立实践者指出 SSRF、token passthrough、shadowing、rug pull 与 stdio/path 仅为标签或缺失。随后新增状态化离线红队控制，并由另一位非作者双目录复现：20 trial，12 PASS / 7 FAIL / 1 REVIEW_REQUIRED。离线机器控制 PASS，真实 MCP/OAuth/OpenClaw/Hermes 仍为 REVIEW_REQUIRED。
- C12 正式作者包完成，正文 18,651 CJK；事实门 PASS，交叉门修补回归 PASS_WITH_LIMITATIONS。D22 四层、CISA public-comment draft 身份、C02/C09 依赖、D20—D23 显式绑定和 41/41 来源消费已闭合。
- C12 作者 20-trial 基线可重复，但独立实践发现缺显式 task_id、四层数据、状态化资源扫描、污染隔离、撤回传播与卸载残余。新增 22-trial 状态化能力供应链补强：11 PASS / 9 FAIL / 2 REVIEW_REQUIRED，真实任务执行数为 0；等待非作者复核，完整实践门不预先升级。
- C13 正式作者包完成，正文 18,418 CJK；只保留 13.1—13.8，恰好三件母产物与两项练习。30 trial 为 18 PASS / 6 FAIL / 6 REVIEW_REQUIRED；Heartbeat 使用 OpenClaw 固定版 system-owned automation 语义，没有复活退役 HEARTBEAT.md。
- C14 已沿 C13→C14 正式依赖链启动写作；章节卡中的旧“六级自主”问题已按 D19 更正为 AU-L0—AU-L4 五级。

### 验证

```text
python3 scripts/validate-formal-manuscript.py
OK framework volumes: 8
OK framework chapters: 24
OK framework body sections: 178
OK chapter packages present: 14
PASS（C14 preparing 与后续 10 章未完成为预期 warning）

python3 scripts/validate-book.py
PASS

git diff --check -- .
PASS
```

### 边界

- 状态化离线夹具能关闭“判分器只信预置标签”的机器控制缺口，仍不能证明真实平台、真实网络、真实身份、真实 Plugin 或跨 Runtime 撤回。
- C12 `representative_real_world` 两条只用于登记证据缺口，真实执行数为 0，结果保持 REVIEW_REQUIRED。
- C13 尚未通过非作者事实、交叉、实践、编辑或总编门；C14 仍在作者生产中。

## 2026-09-30 · C12 post-fix 独立复现与 C13 状态同步

### 结果

- C12 状态化能力供应链补强完成 post-fix 独立双目录复现：22 个唯一 task/trial，`11 PASS / 9 FAIL / 2 REVIEW_REQUIRED`，作者结果与 fresh-temp 输出字节一致。
- 七组负向突变均按预期工作：Cyrillic/Greek Tau 名称混淆、replacement 扩权、伪造真实世界执行、移除 security 覆盖、重复 task/trial 和非 D22 数据层均被正确拦截或降为待复核。
- C12 `machine-control` 升为 `PASS: post_fix_synthetic_invariant_control`；完整 X-C12-01/X-C12-02、P0-05/P0-06/P0-07 和总实践门仍为 `REVIEW_REQUIRED`，不外推到真实 Plugin、Registry、签名、SBOM 或跨 Runtime 撤回。
- C13 的 Standing Order 表述已改为两层：OpenClaw 固定文档的产品术语是 `permanent operating authority`；本书治理要求把这种持久授权约束为有范围、可撤销、可复核、可到期并由 C14 再认证。作者自检 claim 数同步为 27，C14/C22 前置研究的下游状态也已刷新。
- C13 已派发窄范围事实修复复核；C08 lineage 补强已派发另一名非作者做独立复现。

### 验证与边界

```text
C12 post-fix independent reproduction: PASS_IN_SYNTHETIC_MACHINE_SCOPE
C12 full practice gate: REVIEW_REQUIRED
python3 scripts/validate-formal-manuscript.py: PASS（未完成章节为预期 warning）
python3 scripts/validate-book.py: PASS
git diff --check -- .: PASS
```

- 离线状态化夹具证明的是控制逻辑与不变量能被执行，不是目标平台的安装、权限、网络、身份、供应链或生产安全已经通过。
- C13 的事实门只有在独立修复复核签署后才可从 `REVIEW_REQUIRED` 升级；正文修订本身不能自批。

### C13 事实修复复核收口

- 非作者窄范围复核已签 `PASS`：E-C13-014 现准确区分 OpenClaw 的 `permanent operating authority` 产品术语与本书的限域、可撤销、可复核、可到期、需 C14 再认证治理要求。
- 27/27 evidence ID 与正文引用闭合；作者自检、C14 前置研究和 C22 强依赖矩阵的状态均已同步。
- 该签署只关闭事实措辞、claim 计数与下游状态，不批准 C13 实践、编辑、总编或 RC。

## 2026-09-30 · C15 正式作者包完成并启动 C16

### 结果

- C15 正式正文完成并收口为 15.1—15.7，正式校验统计 18,377 CJK；此前中途草稿中的 preflight 式重复结构和陈旧状态已全部清理。
- C15 恰好交付漂移体检表、改进提案、影子测试与回滚计划三件母产物及两项练习；五类漂移、五步改进回路、人类定目标/批变更/担责任、不可自授权和三平台证据边界均进入正文。
- 作者离线夹具包含 75 个唯一 trial，分布为 `20 PASS / 45 FAIL / 10 REVIEW_REQUIRED`；零外部副作用，安全失败不可补偿。该结果尚未经过非作者实践复现。
- C16 前置研究依赖状态已刷新：C14 正式作者包可供受限消费，但独立门禁未完成前不得冻结授权接口。C16 正式作者生产已启动。

### 验证与边界

```text
python3 scripts/validate-formal-manuscript.py: PASS（仅缺 C16—C24 的预期 warning）
python3 scripts/validate-book.py: PASS
git diff --check -- .: PASS
```

- C15 仍为 `drafting / unapproved`，没有通过事实、交叉、实践、编辑、总编或 RC 门。
- C16 可以写作和受审，但不能抢 C17 的路由/Handoff/并发定义或 C18 的 A2A/信任定义，也不能把 C14 作者级合成结果写成生产授权事实。

## 2026-09-30 · C08 lineage post-fix 与 C14 D22 谱系修复

### 结果

- C08 X02 lineage 补强在首轮独立负测中暴露三项 P1：混合私密资源放行被聚合 DENY 掩盖、A 因果断言未绑定实际拒绝、C 替代评审未要求完成和必要资源。作者侧按最小合同修复后，非作者完成双目录复现与 11 组定向突变。
- C08 post-fix 结果保持 31 个唯一 task/trial；混合 `ALLOW + DENY` 现在产生 `PARTIAL` 与披露标记，A 关闭归因请求会失败，替代 reviewer 缺任何必要资源、增加任何禁止资源或缺 trial 都不能 PASS。合成不变量控制通过，完整实践仍为 `REVIEW_REQUIRED`。
- C14 事实门带限制通过；交叉门发现纯合成数据误标六条 `representative real-world`。修复后六条均为 `holdout + synthetic_shadow + intended_target_layer`，runner 强制真实任务计数为 0，并在离线合成环境拒绝伪 real-world 标记。
- C14 修复保持 28 trial 的 `11 PASS / 14 FAIL / 3 REVIEW_REQUIRED` 与零外部副作用；已派发非作者窄范围交叉修复复核。

### 边界

- C08/C14 的 post-fix 结论都只适用于离线合成不变量，不能证明真实模型训练、身份系统、授权服务、目标平台撤销传播、发布或回滚。
- D22 的 `representative_real_world` 表示样本来源和实际运行层，不是“看起来像真实业务”的场景标签；synthetic shadow 必须保持合成身份。

## 2026-09-30 · C15 交叉门修复与 C16 正式作者包

### 结果

- C15 事实门带限制通过；交叉门提出的两项 P1 已完成修复并由非作者回归关闭。正式硬依赖恢复为 C05/C07/C08/C10/C14，C12/C13 明示为补充接口；没有静默修改权威依赖图。
- C15 纯合成夹具的代表性真实任务计数已改为 0；三个基础测试展开的 15 条记录明确为 `holdout + synthetic_shadow + intended_target_layer`。runner 对合成冒充真实层和 executed/count 不一致硬失败，75 trial 仍为 `20 PASS / 45 FAIL / 10 REVIEW_REQUIRED`。
- C16 正式作者包完成：正文 18,059 CJK，只含 16.1—16.7；恰好三件母产物、两项练习、25 条 evidence。45 个作者 trial 为 `12 PASS / 27 FAIL / 6 REVIEW_REQUIRED`，零真实外部副作用。
- C17 前置研究已刷新 C14/C16 当前身份：两章作者包可供受限写作，但后续独立门禁完成前不得冻结为生产接口。C17 正式作者生产已启动。

### 边界

- C15 尚未通过非作者实践门；真实 drift、shadow、canary、外部固化和 bundle rollback 没有运行。
- C16 只是作者包，事实、交叉、实践、编辑、总编与 RC 尚未签署；作者夹具不能证明多 Agent 在真实任务上净收益为正。

## 2026-09-30 · C13 状态化实践补强完成独立回归

### 结果

- C13 首轮独立实践把作者夹具判为“固定复现 PASS、machine-control FAIL”，并提出信号/重放/时效、授权/停止、完成/通知/副作用、UNKNOWN/故障域/恢复、预算硬门五组 P1。
- 作者侧状态化改写后，首轮 post-fix 又暴露组合优先级问题：duplicate/pause/timezone 会掩盖共享故障域或 unsafe UNKNOWN，失效授权会把已有未知效果降成等待审批。第二次修复把已有未知效果、共享故障域和未确认 stop 置于早期路由之前。
- 非作者最终双目录复现及 22 项突变全部通过：30 trial 仍为 `18 PASS / 6 FAIL / 6 REVIEW_REQUIRED`，三触发各 `6/2/2`；共享故障域与 UNKNOWN 永不 PASS，未知效果无其他硬失败时进入 `REVIEW_REQUIRED`。
- `post_fix_synthetic_machine_control` 与硬失败不被掩盖均为 PASS；X-C13-01、X-C13-02 和总实践门仍为 `REVIEW_REQUIRED`。

### 边界

- 该结果证明离线状态化控制逻辑，不证明真实 OpenClaw/Hermes 的 scheduler、Webhook、Channel、停止、投递、恢复或 Sentinel 隔离。
- C13 仍未进入编辑门、总编门或 RC；真实 Runtime 证据未获授权时不得把完整实践门写成 PASS。

## 2026-09-30 · C15 v3.1 独立复验、C16 实践缺陷与 C17 D21/Schema 修补

### 结果

- C15 v3.1 由非作者在两个 fresh temp 中复现，75 trial 保持 `20 PASS / 45 FAIL / 10 REVIEW_REQUIRED`；原 23 项回归、rollback 优先级及 13 项 governance recertification 权威引用负测全部通过。离线状态化 machine-control 为 PASS，X01/X02 与总实践门仍为 `REVIEW_REQUIRED`。
- C16 冻结作者夹具双 fresh-temp 可重复，但独立实践判 machine-control FAIL：六项公平合同不生效，身份/授权/双写/同源/终态/预算/取消/凭证/effect ledger 仍由预裁决布尔代替；极小质量增益可补偿极端成本，dummy 真实层证据、零/负 trial 及外部效果汇总也存在 fail-open。状态化改写成为下一修补项。
- C17 事实门有限制通过；交叉门关闭固定来源、A2A 1.0、Hermes 来源粒度、上游状态、D22 四层和主要状态推导，但发现 D21 truthy 字符串可伪造完成、未知嵌套控制字段会被忽略。
- C17 作者侧升级为 v3：D21 改用三层 evidence registry 引用并核验来源、终态、digest、权威性和状态；控制对象采用 closed-world schema 与严格类型/枚举。固定 60 trial 保持 `12 PASS / 45 FAIL / 3 REVIEW_REQUIRED`，双 fresh-temp results/summary 逐字节一致。
- 全书质量标准的结构基线从陈旧的“146节/v1”校正为正式冻结的“178个正文三级节/v2”；未改变正文目录。
- C18 已进入独立事实/交叉审校；C19 继续受限写作。

### C17 v3 作者侧机器证据

```text
decision digest: cfd77c3eab68797600f4333c80fbc9900998bb93ec09996af72dd285270e4fe1
input sha256: 596e8420d68698f9b5cf5a02a32ab1e594352088610cd40e7e1ee106e0c771e1
runner sha256: dd991e1a48e1793c8917a51809eea3fbab55221917022d694c52f6fdeefcc479
results sha256: cf18124ca158b35202f134dbc55aff7590e3e566765a673fc7b15f4eb17bb1f8
summary sha256: f7ca824f58f0826a19e7887a7319490ecc3e4d76302ac36f45f48cf16c3fe272
```

### 边界

- C15/C17 的通过项只证明冻结离线合成控制可重复、负测不 fail-open；不证明真实平台、真实身份、真实渠道、代表性真实任务或生产副作用。
- C17 两项 P1 的关闭必须由非作者重新执行 `dummy`、未知 authority、缺字段/错类型、未知 schema、D21 缺失/错配/UNKNOWN 及组合负测后才能签署，作者修补不能自批交叉门。

## 2026-09-30 · C16—C20 状态化补强与正式稿推进

### 结果

- C16 v3 已从预裁决布尔改成状态推导；第二轮非作者窄复核又发现畸形时间、alias collision、未知 writer、同 base 双写、FACT 零来源、停止/取消缺回执、证据/effect UNKNOWN 和跨 run evidence ID 重用等近邻绕过。作者侧已逐项封闭，45 trial 保持 `12 PASS / 27 FAIL / 6 REVIEW_REQUIRED`，四个 synthetic-shadow 场景共12 trial，真实层与外部 effect 均为0；等待再次非作者复验。
- C17 v3.2 新增独立 capability evidence authority，observed 与 authority 必须在 capability、task version、permission snapshot、status、digest 五字段完全一致；14例定向回归为 `1 PASS / 13 FAIL`，主固定集保持60 trial、`12/45/3`，等待非作者窄复核。
- C18 v2 把 Card、Task/Event、authority/delegation、Artifact、stop receipt/readback、D21 三层验收、trust与D22改为 closed-world 状态推导。18 trial 修正为 `3 PASS / 9 FAIL / 6 REVIEW_REQUIRED`，decision digest `9f79747a78784be4e72cd5852f89c72dff41733b2de159b8a3cd84070a8a51bc`，双 fresh-temp 与保存件逐字节一致；等待非作者事实/交叉复验。
- C19 正式作者包完成后，独立事实/交叉门分别指出九层术语冲突和安全 runner fail-open。术语已统一为“九层纵深防御（第0—8层）”，三件母产物已实例化，两个练习已补齐质量标准练习卡并拆分合成/真实路径；closed-world stateful runner 正在重构。
- C20 正式作者包已完成：20,312 CJK、36 claims、三件母产物、两项练习、24 trial `4 PASS / 16 FAIL / 4 REVIEW_REQUIRED`；非作者事实/交叉审校中。

### 当前验证与边界

```text
python3 scripts/validate-formal-manuscript.py: PASS（仅缺C21—C24的预期warning）
python3 scripts/validate-book.py: PASS
git diff --check -- .: PASS
```

- C16—C20 的作者侧离线控制、事实门或交叉门状态各不相同；任何等待复验的章节都不得写成已批准。
- 所有 synthetic shadow、离线状态机与 `.invalid` 端点都不构成代表性真实世界证据；真实 OpenClaw/Hermes/A2A、身份/凭证、sandbox、egress、观测后端与生产恢复仍需独立实践。

## 2026-10-01 · 八卷二十四章正式内容候选完成

### 结果

- 完成8卷、24章、178个正文编号节点、A—I九附录、69件章节产物、49项练习与24份证据账本；章节正文合计438,443 CJK。
- C22重编为唯一的22.1—22.7主线；C23/C24移除历史源稿嵌入，正文均为单一H1与七个正式H2。
- C23 v3.0完成非作者终审：固定32 trial，69/69项未预告范围内攻击安全拒绝，9/9项正控通过，事实/交叉/离线机器门`PASS_WITH_LIMITATIONS`。
- C24 v2.7完成非作者终审：固定60场景，45/45项未预告攻击安全拒绝，8/8项正控通过，合法续证和重大变化后三层再认证均可达。
- 统一24章OpenClaw/Hermes/Muse嵌套基线、批准状态、真实实践状态和禁止自批字段；严格校验器不再豁免C22—C24。
- 清除正式正文与读者母产物中的本机路径、内部review路径、fresh-temp和整改流水；历史来源在C24账本中明确标记为非当前claim支持。
- 由规范源生成`manuscript/99-complete-manuscript.md`：20,241行、2,019,618字节，SHA-256 `0db96199b4aef72dacf50ce1f50493192d87277856248485e2254b07aff908d5`。
- 刷新STATUS、生产看板、最终一致性审计、出版就绪报告、manifest、README、决策与经验，并将书稿生产计划归档。

### 验证

```text
build-formal-book.py --check: PASS
validate-formal-manuscript.py --strict: PASS, 0 warnings
validate-book.py: PASS
YAML: 275/275 parse
JSON: 3/3 parse
Python py_compile: PASS
local links: 1,609 checked
external URLs: 234 2xx/3xx after retry; 2 access-control 403; 0 confirmed broken
git diff --check: PASS
formal source internal-path/production-log scan: 0 hits
```

### 边界

- 当前最高身份是`FORMAL_CONTENT_CANDIDATE_COMPLETE`，不是正式出版完成。
- 24章真实世界实践均为`REVIEW_REQUIRED`；真实OpenClaw/Hermes、真实30天训练、真实案例权利、真实认证机构和外部effect未由离线控制替代。
- 版权法律、专业编校、图表索引、版式、ISBN、印前样和作者签字仍需下一阶段完成。

### 全局Harness收口

- `doctor.mjs`与`refresh.mjs`文件未设置可执行位，改用`node <script>`运行。
- `refresh.mjs`已先刷新PROJECTS、LEARNING_INDEX、PORTFOLIO与KNOWLEDGE_INDEX，随后因全局doctor失败而返回非零。
- doctor失败均来自本书范围外的全局环境：注册的多个`~/Documents/Codex/projects/*`目录不存在、clients/operations缺README、旧`js_repl`配置、未登记`manuscript`目录和当前线程使用Hummer兼容入口。本轮未扩大权限去修复这些全局项目与配置。
- 项目自身构建、严格校验、链接、YAML/JSON、Python与diff验证不受上述全局Harness噪音影响，仍全部通过。

## 2026-10-01 · 训练学最佳实践结构升级

### 结果

- 正式纳入卷零，新增卷四与C10—C12；原C10—C24迁移为C13—C27，并建立章节ID迁移表。
- C10、C11、C12分别由独立章节Agent扩写到10,052、9,814、9,995个正文CJK字符，覆盖任务分解/重规划、外部化工作记忆、验证/反例/死胡同/回退、并行收敛和子Agent委派。
- 植入50幅正式Mermaid图；重点完成六层系统、记忆生命周期、授权状态机、Handoff时序、SEC九层攻击面、最小事件链和30天甘特，并将§4.5写入严格验证器。
- 为C09之外的23个原章新增合成现场切片，均包含数字、轨迹或失败日志；三条贯穿案例在前言中补齐样本量、失败分布和合成身份。
- 55个练习与核心20件模板由构建器装订进书，其余58件产物明确为在线配套资源；前言新增“本书不讲什么”。
- 附录G加入SWE-bench、tau-bench、WebArena、GAIA基准地图；附录H和C24.7加入中国个人信息、数据安全、生成式AI、算法/模型备案与内容标识触发器；附录I加入外部词汇对照。
- 新建8,023 CJK的管理者执行摘要分册，只讲七维、AU、D21、REVIEW_REQUIRED、签字点和五个问题。
- S01—S03统一标记RIGHTS-BLOCKED；C02三系统模型改为独立工程论证。
- 合订稿重建为27,421行、2,463,254字节，SHA-256 `355a3a9e91d7027316bfbf6666b675e01f9782158d028357f80156c7a5602fe1`。

### 验证

```text
build-formal-book.py --check: PASS
validate-formal-manuscript.py --strict: PASS, 0 warnings
validate-book.py: PASS
formal figures: 50
opening slices: 23
embedded exercises/core artifacts: 55/20
local links: 1,660
```

### 边界

- 本轮关闭的是结构、内容与构建门，不是现实效果、法律意见或出版社批准。
- 新C10—C12尚未完成授权真实环境实践和独立总编门；全书27章的真实实践继续为REVIEW_REQUIRED。
- 中国法规内容是适用性触发器，不替代具资质专业人员结合具体业务作判断。

### 全局 Harness 复核

- 再次运行 `node ~/.codex/harness/scripts/doctor.mjs` 与 `node ~/.codex/harness/scripts/refresh.mjs`；两者仍因本书范围外的全局注册表与环境项返回非零，包括已登记项目目录缺失、clients/operations 缺 README、旧 `js_repl` 配置、未登记目录及当前线程兼容入口。
- 本轮没有修改这些全局项目或配置；以下项目级构建、严格校验、语法解析、链接与 diff 检查作为本书交付依据。
