# C24 离线持续认证 harness

本目录只运行纯合成、断网、零真实凭证、零生产写的认证控制；不签发真实证书。Builder生成60个完整raw-state场景、两个预注册合法正控计划与独立冻结authority root。正式输入没有`mutation`、`case`或`expected`字段；runner只从pinned authority、可信时钟和closed-world registry推导三态与五态生命周期。

生产—消费关系进入pinned root中的closed-world事件DAG：authority、签名、manifest preregistration、holdout、grader和namespace先于trial input，input严格早于completion与output，Artifact/failure/cost/D21/环境终态/七维证据、change及change evidence先于pre-certificate manifest和review，review/appeal先于certificate，随后才允许public claim与lifecycle。sequence连续唯一，直接前驱形成严格hash-chain，相同timestamp不能证明先后。pre-certificate manifest排除未来claim/lifecycle evidence，避免摘要因果环。

principal的canonical ID、role、status、alias与时窗和所有authority/event投影一起进入冻结root；尾随空白、Unicode兼容字符、alias碰撞/循环、本地UNKNOWN补录或REVOKED主体复活均不能改变历史授权语义。`verify_result(result, authority, source)`三个参数均必需，并强制source重放；没有无根接受路径。重大变化仍必须绑定training/regression/holdout三层、安全切片、pre/post release和独立review。input、authority、result解析前递归拒绝重复JSON键。

```bash
python3 build-certification-fixture.py --output synthetic-certification-input.yaml --authority-output frozen-certification-authority.yaml --positive-contract-output v2.7-positive-control-contracts.yaml
python3 run-certification-harness.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --output synthetic-certification-results.yaml
python3 run-certification-negative-regression.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --output certification-negative-regression-results.yaml
python3 run-v22-remediation-regression.py --runs-dir . --historical-tests ../v2.1-independent-negative-tests.py --output v2.2-remediation-regression-results.yaml
python3 run-v23-final-remediation-regression.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --historical-tests ../v2.2-independent-final-negative-tests.py --output v2.3-final-remediation-regression-results.yaml
python3 ../v2.3-independent-final-negative-tests.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --output v2.4-replay-independent-21.yaml
python3 run-v24-remediation-regression.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --output v2.4-remediation-regression-results.yaml
python3 run-v25-remediation-regression.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --output v2.5-remediation-regression-results.yaml
python3 ../v2.4-independent-final-negative-tests.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --output v2.5-replay-v2.4-independent-29.yaml
python3 run-v26-remediation-regression.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --output v2.6-remediation-regression-results.yaml
python3 ../v2.5-independent-final-negative-tests.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --output v2.6-replay-v2.5-independent-36.yaml
python3 run-v27-positive-control-regression.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --contracts v2.7-positive-control-contracts.yaml --output v2.7-positive-control-regression-results.yaml
python3 ../v2.6-independent-final-negative-tests.py --input synthetic-certification-input.yaml --authority frozen-certification-authority.yaml --runner run-certification-harness.py --result synthetic-certification-results.yaml --output v2.7-replay-v2.6-independent-46.yaml
```

冻结结果为`6 PASS / 52 FAIL / 2 REVIEW_REQUIRED`；五态分布为`ACTIVE=3 / LIMITED=2 / SUSPENDED=2 / REVOKED=52 / EXPIRED=1`。新增ACTIVE正控分别为合法续证与重大变化后三层再认证；20项相邻攻击为`20/20`拒绝，两个完整正控`2/2 PASS`。既有43项作者攻击和46项非作者组合攻击原样回放仍全部非PASS，其原正控也全部通过。历史审校文件保持原样；这些结果只描述列明的离线套件，不外推未枚举攻击。

固定authority root为`sha256:1c768968e30d39195369e517394c3c218829b175d64d219a6e5ff159062fb6ad`，decision digest为`sha256:4645332ab3e0e1aa16ac5a435a3105a422c17eeefea3e0f8ef1a84a53e27e5f4`，正控回归suite digest为`sha256:668fa04d4dd8f05a7fb6879202e7b943cabb3055c07190e0a9ee0fe85497d89e`。双临时目录重建、完整hash与历史兼容限制见`v2.7-fresh-temp-reproduction.yaml`。

真实OpenClaw/Hermes部署、代表性生产任务、外部认证机构、法域和高风险专业认证全部保持`REVIEW_REQUIRED`。本目录的PASS只证明合成控制路径闭合，不代表真实系统或组织通过认证。
