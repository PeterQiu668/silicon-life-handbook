---
review_id: C23-v2.9-independent-final-20261001
chapter_id: C23
role: non_author_final_reviewer
status: completed_with_p0
reviewed_on: "2026-10-01"
fact_gate: REVIEW_REQUIRED
cross_gate: REVIEW_REQUIRED
synthetic_machine_gate: REVIEW_REQUIRED
practice_gate: REVIEW_REQUIRED
editor_gate: NOT_REVIEWED
chief_editor_gate: NOT_AUTHORIZED
release_candidate_authorized: false
---

# C23 v2.9 非作者最终事实、交叉与合成机器终审

## 终审结论

C23 v2.9尚不能通过事实门、交叉门或synthetic machine gate。独立45项未预告组合攻击中，43项安全拒绝，发现2项同进程普通module-global重绑逃逸；它们不需要修改closure cell、runner文件、解释器或内核，因此落在正文和README自己声明已覆盖的边界内：

1. `F24_PATCH_TRANSITIVE_CANONICAL`：将module-global `canonical`替换为只对result对象返回固定值的函数，重封后的FAIL→PASS结果被`verify_raw_documents`接受。
2. `F25_PATCH_TRANSITIVE_ROOT_VALIDATOR`：将module-global `validate_authority_root`替换为空函数，未进入pin registry但内部自洽的source/root/result三元组在`PIN.C23.CURRENT`下被接受。

根因是：闭包捕获了`_evaluate_with_pin`函数对象，却没有捕获或校验该函数运行时解析的传递依赖；最终结果比较也直接从module global查找`canonical`。因此“捕获evaluator函数对象”不等于“冻结完整验证语义”。[chapter.md](../chapter.md)第387行关于“普通global monkeypatch不影响已捕获核心”的读者主张，以及E-C23-044当前证据上限，均需在修复和独立回归前降级。

六项合法正控全部可达，包括raw text、bytes、Path、fresh CLI以及预授权repin的raw/CLI路径。两项直接修改closure cell的攻击也能接受伪造结果，但这需要任意同进程对象写能力，符合作者明示的out-of-scope边界；本审查将其单列为边界示范，不把它们混入上述两项P0。

真实案例、真实授权与版权、真实OpenClaw—Hermes迁移、真实外部effect均未执行，实践门保持`REVIEW_REQUIRED`。本审查不批准编辑、总编或RC。

## 独立重建

两个fresh temp从builder开始重建固定input、authority root、result、作者v2.9套件与独立套件，五类输出逐字节一致：

- 固定32 trial：`2 PASS / 24 FAIL / 6 REVIEW_REQUIRED`；
- authority root逻辑摘要：`18b6e3b04b574fd170eb2d746b1cf0d6271877098bec9116cea5fed2e43734d0`；
- decision digest：`7293a070771b55f59428898c802f40eaf85c658839e005932911b8721d924e2c`；
- 作者v2.9输出SHA-256：`d0f2220b...8ce48`；
- 独立终审输出SHA-256：`858000ce...289c1`；独立suite digest：`d9b2fda9...a6bd5b`。

复现明细见[independent-final-v2.9-reproduction-20261001.yaml](independent-final-v2.9-reproduction-20261001.yaml)，逐项攻击见[independent-final-v2.9-negative-results.yaml](independent-final-v2.9-negative-results.yaml)。

## 攻击覆盖

45项in-scope攻击覆盖：

- result/root/source的raw text、bytes、Path边界，以及dict、list、bytearray和旧对象API拒绝；
- 三文档任意嵌套重复键、尾随文档、NaN、Infinity、无效UTF-8和字符串路径歧义；
- public/internal evaluator名、strict parser、pin摘要、历史pin、pin reader、最终canonical、root validator与public verifier名的module-global重绑；
- 未知/空/PENDING pin、pin_id与root错配、未授权但内部自洽三元组、FAIL/RR结果重封；
- fresh CLI缺参、重复键、runner digest篡改、pin registry摘要篡改、fresh import/reload和低参数反射入口；
- v2.8独立终审I30—34五条历史逃逸意图。

v2.8原脚本在v2.9会因对象级`verify_result(dict,dict,dict)`已删除而提前退出，不能作为新接口的完整回归结果。本审查逐项迁移其原始攻击意图：I30—32的宽松私有parser入口不存在且raw重复键拒绝；I33重绑public evaluator仍拒绝；I34把历史pin global设为`PENDING`仍拒绝，五项均安全。

## 历史套件

- 作者79、v2.3的30、v2.4的23、v2.5的25、v2.6的24项原样通过。
- v2.7攻击`24/24`安全，但三个对象API正控均因协议退役失败；不构成新安全逃逸。
- v2.8作者与独立脚本均在旧对象API处停止；攻击意图已迁移到raw终审，但不能写成“旧脚本原样通过”。
- 作者v2.9为`30/30`安全、`8/8`正控通过；本次新增传递global依赖攻击说明作者套件覆盖不足，而非否定其保存结果。

## P0与关闭合同

### P0-C23-V29-01：最终比较依赖可变module-global canonical

当前`verify_raw_documents`闭包内部最终调用module-global `canonical`。关闭条件：最终比较使用闭包捕获且不可由普通module rebinding替换的规范化函数，或更直接地比较由闭包内严格parser与固定算法产生的canonical bytes；新增FAIL→PASS和RR→PASS两类定向攻击，patch public/private `canonical`、`digest`、`json.dumps`后仍拒绝，同时合法固定结果和合法repin继续通过。

### P0-C23-V29-02：捕获的evaluator仍动态读取可变传递依赖

`_evaluate_with_pin`函数对象虽被捕获，但调用时仍从module globals解析`validate_authority_root`、`validate_document`、`digest`等依赖。关闭条件可二选一：

- 构造真正自包含的trusted evaluator closure，将全部裁决依赖作为闭包参数捕获，并对传递依赖做定向monkeypatch回归；或
- 将唯一可信验收入口收缩为固定verifier与runner摘要的fresh subprocess CLI，明确把同进程Python函数降级为非可信测试helper，不再宣称它抵抗普通global patch。

无论选择哪条，都必须至少覆盖`validate_authority_root / validate_document / canonical / digest / root_payload / exact`的普通global重绑，并证明未授权自洽三元组不能借`PIN.C23.CURRENT`通过。

## P1与出版清理

1. `evidence-ledger.yaml`有三个未被任何claim消费的source：`LOCAL-V28-NOTE`、`LOCAL-V28-REMEDIATION`、`LOCAL-V28-REPRO`。应删除孤立source或明确绑定仍需保留的历史claim。
2. [A-C26-02-failure-analysis-report.md](../artifacts/A-C26-02-failure-analysis-report.md)第20行仍以“作者79项、v2.3整改、上一轮独立36项、作者侧合成控制”等生产日志口径面向读者。应把版本化执行清单迁至review source index，母产物只保留当前失败分布、回归合同与证据上限。

## 事实、结构与来源

- 正文44/44 evidence IDs闭合，无未知claim引用；44个source中41个被claim消费。
- 五个外部一手URL均返回HTTP 200；OpenClaw、Hermes固定版本和Muse `VENDOR-CLAIM`边界没有发现新的错配。
- frontmatter为`formal_candidate`、`content_candidate_only`、`real_world_practice: REVIEW_REQUIRED`；正文只有23.1—23.7七个正式H2。
- 正文主体没有内部review路径或整改标题；主要出版污染位于A-C26-02，而不是正式chapter主线。
- formal strict、YAML/JSON、Python编译、本地链接和diff check均通过。`validate-book.py`唯一失败为合订稿stale；按任务要求未构建。

## 门禁裁决

| 门 | 裁决 | 理由 |
|---|---|---|
| fact | REVIEW_REQUIRED | 正文global-monkeypatch主张被两项P0反证 |
| cross | REVIEW_REQUIRED | trusted verifier边界与实现不一致 |
| synthetic machine | REVIEW_REQUIRED | 45项中2项in-scope escape；虽有6/6合法正控，仍不满足零逃逸 |
| practice | REVIEW_REQUIRED | 真实案例、授权、迁移和effect未执行 |
| editor / chief / RC | NOT AUTHORIZED | 本审查无批准权限 |

## 可复现命令

```bash
cd manuscript/volume-08/C23-case-evidence-lab
python3 review/independent-final-v2.9-negative-tests.py \
  --input review/runs/synthetic-case-input.yaml \
  --authority-root review/runs/frozen-evidence-root.yaml \
  --result review/runs/synthetic-case-results.yaml \
  --runner review/runs/run-case-harness.py \
  --verifier review/runs/verify-case-result.py \
  --output review/independent-final-v2.9-negative-results.yaml
```
