# C23 离线案例证据 harness v3.0

这是纯合成、断网、零真实凭证和零外部副作用的作者整改包。builder 生成完整raw state、registry及独立`frozen-evidence-root.yaml`；runner通过`--authority-root`单独接收冻结root，重算并核对内置摘要。它不读取case名、`expected`、mutation token或叙事文本。

冻结root同时覆盖suite/build/evaluation time/schema、完整有序scenario manifest和registry。每个scenario精确绑定case/subject/task/trial/run/evidence、全部raw refs、case级单值registry、五类task/input/permission/dataset/grader authority、Artifact/effect/trial/failure投影与raw-state digest；release、budget、principal和全部case单值对象也必须被精确消费，语义键不得重复。预算绑定case/task/run/side、五类authority、成本构成与合同摘要，migration再绑定预算摘要。输入不能删减、重排、改名、保留并行真相或选择性披露。trial/failure分布和失败保存由registry动态聚合，而非相信自填整数或布尔值。

离线包拒绝`VERIFIED-REAL`、`ANONYMIZED-REAL`、非空真实manifest、真实外部effect和未冻结root。author/authority/reviewer/grader先经过principal、alias和assignment闭合；任何active共同作者或作者自评都会破坏独立性。runner重放authorization—assignment—trial—failure—FAILURE_LOG—effect—D21—review—publication—evaluation时钟，闭合FAIL三对象，按内容派生D21和effect，并以category×contract矩阵裁决adapter。生产权限和生产数据不能因两侧相同而通过；`RECONSTRUCTED`必须公开缺失与推断。

v3.0把正式验收与作者侧对象计算分开。可信入口只接收result、authority root、source三份原始JSON bytes/text/path和`frozen-pin-registry.json`中预授权的具体`pin_id`；预解析`dict`、空pin、`PENDING`和未登记root全部拒绝。strict parser与pin rows由闭包捕获；规范化、摘要、authority/root校验、document校验及全部裁决函数被重建到私有冻结globals中，因此普通module-global重绑不能改变既有核心。正式交付必须经fresh subprocess `verify-case-result.py`，并以release记录的runner/verifier/pin-registry摘要为信任边界。`evaluate(dict, dict)`只供builder和历史语义回归生成候选结果，不是验收API。直接改写closure cell属于明确不覆盖的任意同进程代码执行。

## 运行

```bash
python3 build-case-fixture.py
python3 run-case-harness.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --output synthetic-case-results.yaml
python3 run-negative-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --output negative-regression-results.yaml
python3 run-v23-remediation-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --output v2.3-remediation-regression-results.yaml
python3 run-v24-remediation-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --output v2.4-remediation-regression-results.yaml
python3 run-v25-remediation-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --runner run-case-harness.py \
  --output v2.5-remediation-regression-results.yaml
python3 run-v26-remediation-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --runner run-case-harness.py \
  --output v2.6-remediation-regression-results.yaml
python3 run-v27-remediation-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --result synthetic-case-results.yaml \
  --runner run-case-harness.py \
  --output v2.7-remediation-regression-results.yaml
python3 run-v28-remediation-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --result synthetic-case-results.yaml \
  --runner run-case-harness.py \
  --verifier verify-case-result.py \
  --output v2.8-remediation-regression-results.yaml
python3 verify-case-result.py \
  --input synthetic-case-input.yaml \
  --result synthetic-case-results.yaml \
  --authority-root frozen-evidence-root.yaml \
  --pin-id PIN.C23.CURRENT
python3 run-v29-remediation-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --result synthetic-case-results.yaml \
  --runner run-case-harness.py \
  --verifier verify-case-result.py \
  --output v2.9-remediation-regression-results.yaml
python3 run-v30-remediation-regression.py \
  --input synthetic-case-input.yaml \
  --authority-root frozen-evidence-root.yaml \
  --result synthetic-case-results.yaml \
  --runner run-case-harness.py \
  --verifier verify-case-result.py \
  --output v3.0-remediation-regression-results.yaml
```

固定集为32 trial：`2 PASS / 24 FAIL / 6 REVIEW_REQUIRED`。v3.0新增26项攻击覆盖result-only canonical、root validator、canonical/digest/root_payload/exact/document校验等传递依赖的逐项与组合重绑、旧core、reload、未授权换根和fresh CLI，`26/26`拒绝；七项正控全部通过，包括当前root和registry预授权的新root。两项直接closure-cell写入作为明确非目标边界单独保存，不计入in-scope escape。

历史语义套件的79、30、23、25、24与独立19/15/36/24仍原样通过；最早独立18项维持已知`17/18`旧oracle（I18实际被更严格REJECT）。v2.7/v2.8的对象级`verify_result(dict,dict,dict)`正控按安全设计退役，因此旧脚本不再作为v3.0接口通过条件；它们的攻击意图已迁移到raw/fresh-CLI回归，不能为“旧脚本全绿”重新开放丢失序列化来源的对象验收。

Authority root logical digest为`18b6e3b04b574fd170eb2d746b1cf0d6271877098bec9116cea5fed2e43734d0`，decision digest为`7293a070771b55f59428898c802f40eaf85c658839e005932911b8721d924e2c`。两个全新临时目录的input、root、result与v3.0 regression四类文件逐字节一致；全部文件sha和套件digest见v3.0作者复现记录。

`accepted_real_claim_count=0`与`external_effect_count=0`只证明当前离线合成运行边界。真实案例、真实公开授权、真实OpenClaw/Hermes迁移和真实平台副作用仍为`REVIEW_REQUIRED`。
