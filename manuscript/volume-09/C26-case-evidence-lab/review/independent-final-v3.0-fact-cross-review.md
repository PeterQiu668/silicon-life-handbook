---
review_id: C23-v3.0-independent-final-20261001
chapter_id: C23
role: non_author_final_reviewer
status: completed_with_limitations
reviewed_on: "2026-10-01"
fact_gate: PASS_WITH_LIMITATIONS
cross_gate: PASS_WITH_LIMITATIONS
synthetic_machine_gate: PASS_WITH_LIMITATIONS
practice_gate: REVIEW_REQUIRED
editor_gate: NOT_AUTHORIZED
chief_editor_gate: NOT_AUTHORIZED
release_candidate_authorized: false
---

# C23 v3.0 非作者最终事实、交叉与合成机器终审

## 结论

C23 v3.0在列明的离线合成边界内通过事实门、跨章一致性门和synthetic machine gate，裁决为`PASS_WITH_LIMITATIONS`。两个全新临时目录均从builder开始重建固定32 trial、冻结authority root、result、作者v3.0套件、独立v3.0套件和v2.9独立套件，六类文件逐字节一致。新增69项未预告in-scope攻击全部安全拒绝，9项合法正控全部通过；没有发现普通module-global重绑、传递依赖组合patch、raw入口、pin/root、旧对象入口、别名/partial/getattr、reload或fresh CLI逃逸。

两项直接改写`verify_raw_documents.__closure__` cell的演示可改变裁决。这要求任意同进程对象写能力，符合章节明示的非目标边界，故单列为out-of-scope demonstration，不计入范围内逃逸。正式信任仍以固定runner、verifier、pin registry摘要和fresh subprocess CLI为边界。

真实案例、真实授权与版权、真实OpenClaw—Hermes迁移、真实外部effect均未执行，实践门保持`REVIEW_REQUIRED`。本审查不批准编辑门、总编门或RC。

## 双重建与固定结果

两个fresh temp分别为`/tmp/c23-v30-final-a.9DLH4m`与`/tmp/c23-v30-final-b.x1nPw3`。固定结果为：

- 32 trial：`2 PASS / 24 FAIL / 6 REVIEW_REQUIRED`；
- authority root逻辑摘要：`18b6e3b04b574fd170eb2d746b1cf0d6271877098bec9116cea5fed2e43734d0`；
- decision digest：`7293a070771b55f59428898c802f40eaf85c658839e005932911b8721d924e2c`；
- 动态接受真实主张：0；动态外部effect：0；
- 独立结果SHA-256：`4952845e14dd6523baf0439e25be022dc44895008df8d3697be16341cee9d9f6`；
- 独立suite digest：`ccebffdc30d75934e84c7a8add09b6c51538c3dee84ccba1bcef8e0f48fb75dc`。

完整文件哈希、历史套件摘要与限制见[独立复现记录](independent-final-v3.0-reproduction-20261001.yaml)，逐项结果见[独立攻击结果](independent-final-v3.0-negative-results.yaml)，可执行测试见[独立测试程序](independent-final-v3.0-negative-tests.py)。

## 未预告攻击覆盖

69项in-scope攻击覆盖以下路径：

1. result、root、source的raw text、bytes、Path边界；预解析dict、bytearray和旧对象验收入口拒绝。
2. 三份JSON的嵌套重复键、尾随文档、NaN、Infinity、无效UTF-8和字符串路径歧义。
3. 空、`PENDING`、未知、错配pin_id；CURRENT与repin互换；未授权但内部自洽的source/root/result三元组。
4. FAIL→PASS与RR→PASS重封结果，完整semantic replay仍拒绝。
5. `canonical / digest / strict_json_loads / validate_authority_root / validate_document / evaluate / _evaluate_with_pin / root_payload / exact / sha / validate_record / index_records / dt`逐项普通module-global重绑。
6. `json.dumps / hashlib.sha256 / math.isfinite`共享模块属性patch、schema常量、pin reader、pin digest、历史pin和伪造captured-pin名称。
7. canonical+root validator、parser+evaluator、authority+document、digest+exact+sha及六项公共语义同时patch。
8. 保存的旧core、getattr别名、`functools.partial`、module dictionary、fresh import/reload及函数默认pin改写。
9. fresh CLI伪结果、重复键、未授权三元组、缺source、runner摘要变化和pin-registry摘要变化。

测试并非“全拒绝”oracle。9项正控全部通过：当前root的raw text、bytes、Path、fresh CLI；registry预授权repin的raw与CLI；保存别名合法输入；fresh import合法输入；公共global被破坏时，冻结core仍能接受合法固定集。

## v2.9、I30—34与历史回放

v2.9非作者45项在v3.0上重放为`45/45`安全拒绝、`6/6`正控通过。历史I30—I32宽松私有parser入口不存在；I33公共evaluator重绑仍被完整重放拒绝；I34把历史pin global改为`PENDING`仍不能替代冻结registry，五项均拒绝。

作者历史语义套件本轮重新执行结果：原79项`79/79`、v2.3的30项`30/30`、v2.4的23项`23/23`、v2.5的25项`25/25`且正控`2/2`、v2.6的24项`24/24`且正控`2/2`。v2.7/v2.8旧对象验收正控属于已退役协议，不为使旧脚本变绿而重开丢失序列化来源的dict验收入口；其攻击意图已由当前raw与CLI套件覆盖。

## 事实、来源、结构与跨章一致性

- 正文引用44个Evidence ID，账本有44条claim，未知或未被正文引用的claim均为0。
- 账本44个source全部被当前claim消费，没有未知source引用或孤立source。
- Frontmatter为`formal_candidate / content_candidate_only / real_world_practice: REVIEW_REQUIRED / self_approval_allowed: false`。
- 正文仅一个H1和23.1—23.7七个正式H2；strict计数18,830 CJK，无本机绝对路径或正文内部review链接。
- OpenClaw固定`v2026.9.6 / eb377ac…`，Hermes固定`0.20.1 / f80f453…`，Muse保持`VENDOR-CLAIM`；未发现新的平台身份越界。
- 三件母产物保留三案八段、失败分布、迁移公平性、证据上限和真实未跑边界，没有重新引入“真实已验证”或“迁移成功”主张。

## 出版P1

`A-C23-01-three-case-reproduction-package.md`第32—36行仍直接展示`review/runs/...`内部命令路径。该问题不改变固定结果、事实引用或机器控制，因此不降级本轮fact/cross/synthetic裁决；但公开出版前应改成读者向“由维护者提供冻结source/root/result及可信验收器”的复现接口，把内部执行命令保留在prepublication source index或review证据。非作者审查员未修改母产物。

## 门禁裁决

| 门 | 裁决 | 边界 |
|---|---|---|
| fact | PASS_WITH_LIMITATIONS | 44/44 claim闭合；只证明固定合成schema及列明来源 |
| cross | PASS_WITH_LIMITATIONS | C07/C09/C18/D21接口一致；真实跨Runtime迁移仍未执行 |
| synthetic machine | PASS_WITH_LIMITATIONS | 69/69攻击拒绝、9/9正控通过；任意同进程代码执行不在证明范围 |
| practice | REVIEW_REQUIRED | 无真实案例、授权版权、迁移和外部effect |
| editor / chief / RC | NOT AUTHORIZED | 本审查不拥有这些批准权 |

## 验证

YAML/JSON解析、Python编译、formal strict、本地链接及`git diff --check`均通过。`validate-book.py`唯一错误为合订稿stale；本轮按约束未构建合订稿。

