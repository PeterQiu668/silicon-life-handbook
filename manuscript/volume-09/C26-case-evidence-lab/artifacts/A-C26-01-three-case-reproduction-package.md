# A-C26-01 三案复现包

本母产物为三案共用的唯一事实入口；A-C26-02与A-C26-03只能引用这里的对象ID，不得另造事实。每案八段：身份/授权；问题岗位；环境版本；任务对照；过程轨迹；Artifact/D21；结果/失败/成本；限制/复现。

## 必填登记与绑定

| 八段 | 权威对象 | 必须绑定 | 缺失处置 |
|---|---|---|---|
| 身份/授权 | identity、authorization、source | subject、case、version、principal、scope、time、status、revocation、source digest | 离线真实身份直接拒绝；其他硬缺失FAIL |
| 问题岗位 | task/input authority + comparison contract | task与input各自authority、case/task/run、data/risk/permissions/eval digest | 同时改写基线与候选也不得绕过外部authority |
| 环境版本 | environment、release | manifest digest、mode、version、固定commit | 浮动版或未版本化FAIL |
| 任务对照 | baseline/candidate budget | case/task/run/side、五类authority ref、model/tool/compute/human/time与total、contract digest | 跨scenario互换、分项不闭合或不等FAIL |
| 过程轨迹 | task/trial/run/evidence ID、trial/failure registry | 全局唯一并贯穿全部对象；分布动态聚合 | 错绑、伪计数或删失败FAIL |
| Artifact/D21 | artifact、D21 registry | 六字段evidence payload；kind/source/time/content digest在Artifact信封；technical/delivery/business evidence | FAIL硬失败，UNKNOWN为RR；FAILURE_LOG晚于D21/评审/公开为FAIL |
| 结果/成本 | derived result | 三态、原因、动态real/effect计数 | 禁止手填统计 |
| 限制/复现 | reviewer、publication、redaction、migration | 独立principal/alias、private/public/mapping digest、预算总额与模型/工具/计算/人时/人工/权限/数据/评测构成 | 自评、错映射或资源构成不等FAIL |

## CASE-A/B/C冻结入口

CASE-A研究Agent、CASE-B主动运营Agent与CASE-C多Agent组织均复用上述对象模型。正式离线夹具以`S01—S32`作为控制与故障切片，而不是把scenario名称当案例结论。每个scenario携带完整raw state，并由冻结suite manifest精确绑定有序inventory、全部raw refs、author assignment及Artifact/effect/trial/failure投影；raw state没有`expected`、mutation或叙事标签。

## 当前复现记录

- 固定集：32 trial；2 PASS、24 FAIL、6 REVIEW_REQUIRED。
- 复现时必须同时取得完整source、冻结authority root和result的原始JSON文件，并通过fresh subprocess CLI选择`frozen-pin-registry.json`中已授权的具体`pin_id`。verifier在内部严格解析三份原始文档，使用私有冻结globals中的canonical、digest、authority/document校验与完整evaluator函数图重放语义，再比较完整结果；已经被宽松解析成`dict`的对象、只校验摘要/聚合/digest、修改公开module global pin/validator/canonical或使用`PENDING`都不能构成接受。当前固定夹具的authority root逻辑摘要为`18b6e3b04b574fd170eb2d746b1cf0d6271877098bec9116cea5fed2e43734d0`，decision digest为`7293a070771b55f59428898c802f40eaf85c658839e005932911b8721d924e2c`。复现者还应核对runner、verifier与pin registry的release摘要；任一输入或可信代码变化都要生成新版本。直接改写closure cell属于任意同进程代码执行，不在本地控制证明范围。
- real-case manifest为空；动态接受真实主张0；动态外部effect 0。
- 限制：只证明离线合成证据合同，不证明真实案例、公开授权或跨Runtime效果。

读者需要复现时，应向维护者取得同一版本的冻结复现包与发布清单，先核对source、authority root、result、verifier和pin registry的摘要，再通过维护者提供的公开校验入口提交三份原始JSON文档及已登记`pin_id`。公开入口必须在fresh process中执行严格解析、冻结root授权与完整语义重放；若维护者尚未提供公开入口，读者只能把材料标记为“待复现”，不能自行把预解析对象或摘要比对视为验收。

合法repin不是运行时改global，而是由独立authority把新root精确摘要加入冻结registry，再以新release代码摘要启动fresh CLI。对象级`evaluate`只生成作者候选结果，不签发接受结论。
