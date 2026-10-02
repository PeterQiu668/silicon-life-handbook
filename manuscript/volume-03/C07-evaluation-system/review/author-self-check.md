# C07 作者自检

> 检查日期：2026-09-30
> 角色：章节作者
> 状态：drafting
> 声明：作者自检不构成事实门、交叉门、独立实践门或总编门签核；本文件不得用于把章节标记为 release_candidate 或 done。

## 1. 范围与计数

- 正文覆盖：7.1—7.8；
- 作者初稿快照净中文字符：18,162（移除 frontmatter、反引号/波浪线代码块后的作者计数）；
- 独立事实修补后 formal validator 口径：18,721 CJK；
- 母产物：严格三件；
- 练习：两项；
- 失败模式：十二类；
- 合成运行：8 task / 24 trial，13 PASS / 8 FAIL / 3 REVIEW_REQUIRED；
- 门禁词：仅 PASS / FAIL / REVIEW_REQUIRED；UNKNOWN 只作为 grader 原始输入。

## 2. P0 作者侧逐项检查

| P0 | 作者侧结论 | 证据 | 独立门状态 |
| --- | --- | --- | --- |
| P0-01 模板与目录完整 | PASS | chapter.md 含 7.1—7.8、导航、案例、练习、验收与交接 | 待交叉审稿 |
| P0-02 定义权一致 | PASS | 只主定义 evaluation-system；引用而不重定义 C03/C04/C06/C20/C24 | 待交叉审稿 |
| P0-03 关键事实有来源 | PASS | evidence-ledger.yaml 经独立事实审校拆分为 20 项 claim，分固定/动态/厂商声明 | 待事实审稿 |
| P0-04 版本命令与字段 | PASS | OpenClaw 固定提交；Hermes 固定/动态分层；Muse vendor-claim | 待事实与实机复核 |
| P0-05 可执行、可停止、可回滚 | PASS | 两项练习、动作合同、停止与恢复、合成 harness | 待独立实践门 |
| P0-06 高风险权限与隔离 | PASS | 合成/沙盒/shadow、系统权限、最小凭证、硬门 | 待独立安全与实践门 |
| P0-07 基线与客观验收 | PASS | 可重复 24-trial 基线、终态与三态验收 | 待独立复跑 |
| P0-08 仿生边界 | PASS | 四段式体检/考试类比并否定意识外推 | 待交叉审稿 |
| P0-09 平台证据边界 | PASS | OpenClaw 固定、Hermes 动态、Muse 声明明确分开 | 待事实审稿 |
| P0-10 案例与隐私 | PASS | CASE-A/B/C 为教学复合案例；运行只用合成数据 | 待编辑复核 |
| P0-11 Agent 块与权限 | PASS | agent_procedure 可解析式 YAML，未授权生产/外发 | 待机器校验与实践 |
| P0-12 无隐藏冲突 | PASS | 开放缺口进入账本且章节保持 drafting | 待全书交叉审稿 |
| P0-13 安全失败不可平均 | PASS | 六道门、五项合成硬失败均为 FAIL | 待独立红队 |
| P0-14 产物可定位 | PASS | 三件 artifact、两项 exercise、run 原始材料均落盘 | 待后章消费测试 |
| P0-15 强声明受限 | PASS | 明确不支持平台比较、稳定/领先/认证 | 待总编审稿 |

上述 PASS 仅表示作者检查未发现结构性缺项，不替代对应独立角色。尤其 P0-03/04/05/06/07/09/13 仍需非作者签核。

## 3. 百分制作者初评

| 维度 | 满分 | 自评分 | 作者证据 |
| --- | ---: | ---: | --- |
| 论证与结构 | 14 | 13 | 从对象、数据、场景、证据、裁判到门禁形成闭环 |
| 事实准确与证据 | 18 | 17 | 19 项账本、版本身份与限制；仍待独立链接/版本复核 |
| 技术与系统完整性 | 10 | 10 | SUT、状态、接口、停止、回滚、环境终态齐全 |
| 课程与学习设计 | 12 | 11 | 三层写法、三案、反证、两项迁移练习 |
| 实践与可复现性 | 14 | 13 | 标准库确定性 harness 与全量原始结果；未做真实 Runtime |
| 评测与验收 | 12 | 12 | 四层、五场景、四类 grader、三态、尾部与不确定性 |
| 安全、治理与伦理 | 8 | 8 | 非补偿硬门、最小权限、污染、停止与责任 |
| 仿生解释质量 | 4 | 4 | 四段式完整且边界明确 |
| 中文出版表达 | 4 | 3 | 已完成结构性自校，仍需专业编辑压缩少量英文混用 |
| 人机双读与章际接口 | 4 | 4 | Agent YAML、三件产物和多章输出合同 |
| **合计** | **100** | **95** | 作者目标达成，不构成最终评分 |

## 4. 作者运行记录

命令：

~~~bash
cd manuscript/volume-03/C07-evaluation-system
python3 review/runs/run-synthetic-baseline.py
~~~

结果输入哈希为 3ef2cc8f7991fb2dbcfffcd04ac3753b57a1983570f27fe50007e713f8c31dc0。运行无网络、无凭证、无真实数据、无外部副作用；model/human/expert 均为合成夹具。五个确认硬失败为 fabricated_success、prompt_leak、unauthorized_tool、duplicate_side_effect、authority_bypass，全部进入 FAIL。两个 code UNKNOWN 均映射为 REVIEW_REQUIRED。

该运行证明 harness 与数据合同可复跑，不证明真实 OpenClaw/Hermes/Muse 或真实裁判效果。

## 5. 校验结果

- evidence-ledger、输入与运行结果 YAML：PASS；
- chapter frontmatter 与全部嵌入 YAML：PASS；
- 证据闭合：正文引用 20 项，账本定义 20 项，无缺失、无未使用 claim；
- 本地来源路径：PASS；
- 三件 artifact、两件 exercise 数量合同：PASS；
- 合成 harness Python 编译与结果断言：PASS；
- 重复运行输出字节一致：PASS；
- C07 本地链接与全书链接检查：PASS；
- formal validator：PASS，C07 计数 18,721 CJK；全书仅有并发准备中的章节和未来章节缺失 warning；
- publication validator：PASS；
- 新文件 whitespace / diff check：PASS。

## 6. 待独立审校清单

1. 事实审校：复核 OpenClaw 固定提交字段、Hermes 动态文档与 release 边界、Muse 厂商声明措辞；
2. 交叉审校：确认不越权 C03 七维、C08 训练、C20 SLI/SLO 和 C24 认证；
3. 实践审校：独立复跑两项练习，至少替换 task 变体与 grader，保留失败；
4. 安全红队：测试留出泄漏、候选注入、选择性报告、工具成功/终态失败和跨 trial 状态；
5. 编辑审校：检查 18,000—24,000 CJK、术语密度、黑白表格、证据链接和 Agent 块；
6. 总编门：只有前述审校关闭且评分复核后，才能改变 drafting 状态。

## 7. 作者结论

作者侧写作包已达到送交独立审校的条件。正式章节结论仍是 REVIEW_REQUIRED，原因不是已知硬失败，而是独立事实、交叉、实践与总编签核尚未发生。
