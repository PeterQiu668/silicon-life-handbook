---
review_id: C11-author-self-check-20260930
chapter_id: C11
review_type: author-self-check
status: drafting
reviewer: "chapter-author-agent:c11"
reviewed_on: "2026-09-30"
approval_scope: author-preflight-only
independent_approval: false
editorial_approval: false
---

# C11 作者自检

> 本记录只证明作者完成生产前自检，不构成事实门、交叉门、独立实践门或总编门签核。章节保持 drafting。

## 包清单

- chapter.md；
- evidence-ledger.yaml；
- A-C11-01 工具目录与风险清单；
- A-C11-02 工具合同；
- A-C11-03 MCP 安全检查表；
- X-C11-01 读写工具合同、幂等与故障注入；
- X-C11-02 MCP 能力、授权与 Server 信任红队；
- review/runs 下的输入、harness、逐 trial 与摘要。

正式母产物严格三件。风险分级、合同测试、异常演练和能力/授权边界均作为三件产物的嵌入字段，没有创建第四件。

## 15 项 P0 作者侧结论

| 门槛 | 结论 | 证据位置 | 说明 |
| --- | --- | --- | --- |
| P0-01 模板与目录 | PASS | chapter.md 11.1—11.8、章首、章末 | 案例、双视图、练习、交接、证据和变更完整 |
| P0-02 定义权一致 | PASS | 11.1、11.8.1、章首边界 | C11 主定义 Tool/MCP 工程，不重定义 C12/C14/C19/C20 |
| P0-03 事实与证据 | PASS | evidence-ledger.yaml、E-C11-001—025 | 标准、固定、动态、厂商、方法与本地验证分层 |
| P0-04 版本核验 | PASS | 11.4、11.8.2—11.8.4 | MCP 2026-07-28、OpenClaw 固定提交；无未核验命令 |
| P0-05 可执行可恢复 | PASS | 11.6、11.7、A-C11-02 | 幂等、timeout、retry、cancel、补偿、下线和恢复证明完整 |
| P0-06 权限与隔离 | PASS | 11.5、A-C11-03 | schema、授权、Policy、Approval、Sandbox 分开 |
| P0-07 练习与验收 | PASS | X-C11-01/02、review/runs | 五类场景、环境终态、失败分布和三态门 |
| P0-08 仿生边界 | PASS | 11.8.6 | 人类现象、工程映射、训练启示、比喻边界四段完整 |
| P0-09 平台证据边界 | PASS | 11.8.2—11.8.5 | OpenClaw fixed、Hermes fixed/dynamic、Muse VENDOR-CLAIM |
| P0-10 案例合规 | PASS | 开场案例、11.7.12—11.7.14 | 三案例均为合成，无真实客户、凭证或外发 |
| P0-11 机器块 | PASS | 11.2.8、章末 Agent 验收、三产物 | YAML 可解析，不新增授权 |
| P0-12 冲突与缺口 | PASS | ledger open_issues、11.8 | 未实机项显式 REVIEW_REQUIRED，未标完成 |
| P0-13 硬失败不可抵消 | PASS | 11.3.7、11.7.7、运行结果 | 越权、泄密、SSRF、重复副作用、错误终态直接 FAIL |
| P0-14 产物可消费 | PASS | artifacts/ 与 11.8.10 | 三件产物可定位，C12/C13/C14/C17/C19/C20/C21/C22 接口明确 |
| P0-15 领先/提升主张 | PASS | 11.7、运行限制 | 无产品领先主张；合成结果不外推平台 |

以上 PASS 仅表示作者未发现结构性 P0 阻断；独立评审可以推翻。

## 作者侧百分制预评

| 维度 | 满分 | 作者预评 | 说明 |
| --- | ---: | ---: | --- |
| 论证与结构 | 14 | 14 | 从边界、接口、风险、协议、授权、运行语义到测试连续 |
| 事实准确与证据 | 18 | 17 | 25 项证据闭合；真实 Server/平台仍需独立复核 |
| 技术与系统完整性 | 10 | 10 | discovery、schema、auth、execution、receipt、terminal、recovery 完整 |
| 课程与学习设计 | 12 | 11 | 三案例与双练习有梯度；尚需真实读者试教 |
| 实践与可复现性 | 14 | 13 | 两次确定性运行一致；未做真实 Runtime/MCP |
| 评测与验收 | 12 | 12 | 五场景、硬门、完整分布、三态和独立终态 |
| 安全、治理与伦理 | 8 | 8 | SSRF/token/secret/approval/sandbox/stop/revoke 完整 |
| 仿生解释质量 | 4 | 4 | 四段式边界清楚 |
| 中文出版表达 | 4 | 4 | 术语稳定，无口号或伪最强 |
| 人机双读与章际接口 | 4 | 4 | Agent YAML 可解析，接口可交接 |
| 合计 | 100 | 97 | 作者预评，不构成独立评分或候选资格 |

## 确定性合成运行

环境：Python 标准库、离线 JSON/YAML 夹具、内存模拟状态；无网络、真实身份、真实凭证、外发、资金、生产或破坏性操作。

连续运行两次，输出字节哈希一致：

- synthetic-tool-results.yaml：cf927f93c1847a919e272a4cf0ed1f75edc561db2de865ad560acee596870245；
- synthetic-tool-summary.md：84b91608898b7d8aea6d23e8953de9826c987a6184cc8598141e218b4b6f74f8；
- 输入内容哈希：78f35182fc30a4310e9b32e95321c98558717e08f1c7a2701c95d530fce01073。

结果：18 trial；12 PASS、4 FAIL、2 REVIEW_REQUIRED。安全拒绝被正确判 PASS，所有 UNKNOWN 证据映射 REVIEW_REQUIRED。FAIL 保留审批绕过、恶意描述改变动作、重复副作用、幂等键变化、Cancel 冒充回滚、秘密外泄企图和协议成功但错误终态。

## 开放项

1. OpenClaw 目标部署实际 MCP Servers、tool profile、Approval、Sandbox、Browser 与 Secrets 配置尚未实机探测：REVIEW_REQUIRED；
2. Hermes 动态 MCP/Security/Code Execution 页面尚未逐项固定到 v0.20.1 源码：REVIEW_REQUIRED；
3. Muse 内部 connector schema、幂等、补偿与凭证实现未知：REVIEW_REQUIRED；
4. 真实 Provider 的 receipt、幂等、取消、补偿、日志和保留需逐供应商核验：REVIEW_REQUIRED；
5. 作者实验不构成 MCP 协议认证、产品安全评测或真实删除/外发证明。

## 作者结论

作者侧生产门完成，未发现需立即阻断移交的 P0 缺陷。正式候选资格仍取决于独立事实、交叉、实践和总编四门；作者不批准任何一门。
