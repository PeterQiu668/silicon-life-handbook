# C23 作者自检

> 日期：2026-10-01。状态：`drafting / unapproved`。作者不批准事实、实践、交叉、总编或RC门。

## 交付与运行

- 正文保持正式`23.1—23.7`，恰好三件母产物、两项练习。
- 证据账本44条claim，正文引用双向闭合。
- v3.0沿用固定集：32 trial，`2 PASS / 24 FAIL / 6 REVIEW_REQUIRED`；authority root与decision digest不漂移。
- 历史18项攻击原样复跑，旧10个缺口全部为`FAIL/REJECT`；I18旧脚本因更严格REJECT而记为17/18旧合同，结构化合法重钉root由新增R23—R30覆盖。
- 扩展负测：79/79；v2.3整改30/30；v2.4整改23/23；v2.5整改25/25；v2.6整改24/24；历史19/19；独立15/15、36/36、v2.6独立24/24。v2.9非作者45项在v3.0实现上为45/45安全；v3.0新增26/26攻击零逃逸、七个正控全部通过。所有记录均为作者侧回放，不替代新一轮独立终审。
- authority root logical digest：`18b6e3b0...34d0`；decision digest：`7293a070...e2c`；v3.0 suite digest见作者复现记录。
- accepted real claim与external effect动态计数均为0。

## v3.0传递依赖整改自检

- 已删除`_ORIGINAL_JSON_LOADS`及对共享`json.loads`的改写；strict parser捕获配置好的decoder，只接收原始UTF-8 bytes/text，并递归拒绝重复键和尾随文档。
- 可信`verify_raw_documents`拒绝已解析`dict`；闭包捕获原始parser、冻结canonical、不可变pin rows，以及重建在私有globals中的完整evaluator函数图。`validate_authority_root / validate_document / canonical / digest / root_payload / exact`等公开名称被普通重绑时，既有核心不再回查这些module globals。
- `verify-case-result.py`在fresh subprocess中先核对runner固定摘要，再读取三份原始JSON path并选择具体`pin_id`；`PENDING`、空pin、未知pin、当前root配错授权pin均拒绝。
- v3.0的26项攻击覆盖v2.9非作者发现的result-only canonical与root-validator两项P0、传递依赖逐项/组合patch、旧core、reload、CLI和未授权换根；零逃逸。七项正控覆盖raw text/bytes/path、fresh CLI与registry预授权repin。直接改写closure cell的两项攻击仍可改变同进程对象，已作为任意同进程代码执行的非目标边界保留，不虚称防住。
- A-C23-01读者段只描述冻结复现包、发布摘要和维护者提供的公开校验入口，不再暴露内部review路径或生产目录；内部执行命令仅保留在维护者运行说明中。

## v2.7及此前控制继续保留

- root物理分离、canonical重算并由runner固定摘要钉住；suite/build/time/schema、有序scenario manifest和精确projection均在冻结root内。
- release、budget、reviewer、effect、artifact、source、publication、migration等REVOKED为硬失败，UNKNOWN才可能RR。
- author、authority、reviewer先经alias registry归一；case级单值registry以及release、budget、principal实行exact projection和语义键唯一，任何active共同作者都会破坏reviewer独立性。
- effect kind唯一派生external并与authorized/status/receipt/readback/聚合计数一致；internal effect不豁免。
- scenario task/trial/run/evidence贯穿Artifact、D21、migration、effect、trial与failure；task/input/permission/dataset/grader五类authority各自独立，输入scenario集及全部projection必须与manifest精确相等。
- trial_count、failure_count、failures_preserved由trial/failure registry和FAILURE_LOG重算；PASS/UNKNOWN不得指active failure，FAIL trial、active failure与唯一FAILURE_LOG双向闭合。
- authorization—assignment—trial—failure—FAILURE_LOG—effect—D21—review—publication—evaluation按事件时间重放；所有日志和证据必须早于消费它的D21、review与publication。
- D21状态由三类closed evidence payload支持；adapter difference执行category×affected_contract×criticality×disposition允许矩阵，只接受同case/run/evidence的active技术证据，厂商公开页不能作为独立证据。
- 公平合同比较预算总额及模型、工具、计算、人时、人工成本、权限、数据和评测构成；预算绑定case/task/run/side、五类authority与contract digest，migration contract再绑定所选预算摘要。生产权限、生产数据、作者自评grader即使两侧相等也不得通过。
- `RECONSTRUCTED`要求identity/source都有相同且非空的missing elements与inference list；未披露或不一致为FAIL，合法重建保持RR。
- input、root与result在解析前递归拒绝任意层级重复JSON键；result采用closed schema与完整canonical digest，公共verifier还必须接收冻结source和root，重跑全部语义并逐字节比较结果。

## 验证与限制

两个全新临时目录从builder重建的input、root、result与v3.0 regression四类文件逐字节一致，并与提交文件逐字节一致；hash记录于`v3.0-author-reproduction-20261001.yaml`。formal/book、YAML/frontmatter、链接、py_compile和diff检查在交付前重新运行。

离线包在出结果前拒绝`VERIFIED-REAL / ANONYMIZED-REAL`与非空real-case manifest。真实案例、真实授权/版权、真实OpenClaw/Hermes同合同迁移、真实平台effect及Muse内部实现继续`REVIEW_REQUIRED`。作者只提交整改，不宣告P0、事实门或交叉门关闭。
