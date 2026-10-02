# C20 v2.1 状态化离线故障注入夹具

本夹具只使用合成任务、虚构租户、虚构回执和零价值 canary；无网络、无真实凭证、无真实外发、支付、删除或生产写。`build-reliability-fixture.py`确定性生成24个逐场景完整raw-state；runner只消费root authority registries与原始状态，不用case名、recipe或`expected_decision`裁决。离线runner无条件拒绝`representative_real_world`和同文件自填manifest，合成PASS不能迁移为生产证明。

```bash
PYTHONPYCACHEPREFIX=/tmp/c20-pycache python3 build-reliability-fixture.py \
  --output synthetic-reliability-input.yaml
PYTHONPYCACHEPREFIX=/tmp/c20-pycache python3 run-reliability-harness.py \
  --input synthetic-reliability-input.yaml \
  --output synthetic-reliability-results.yaml \
  --summary synthetic-reliability-summary.md
PYTHONPYCACHEPREFIX=/tmp/c20-pycache python3 run-reliability-negative-regression.py \
  --input synthetic-reliability-input.yaml \
  --output reliability-negative-regression-results.yaml
```

D22四层中`representative real-world`动态派生为0；security/red-team是横切属性而非第五层。保存结果为`4 PASS / 16 FAIL / 4 REVIEW_REQUIRED`、外部副作用0。46项负向控制覆盖closed-world schema、类型/枚举/版本、ID、D21/recovery显式失败、D22、authority/policy、receipt/readback、事件digest/chain/time/seq、evidence唯一性、非负/有限/range、外部effect、UNKNOWN与硬失败非补偿；46/46通过。

这是作者侧synthetic invariant control，尚待非作者复核。真实OpenClaw/Hermes、OTel collector、Prometheus、Queue、Provider、Channel、授权服务、成本后端与恢复路径均未运行，完整实践门保持`REVIEW_REQUIRED`。
