# C21 v2.4 离线生命周期与发布演练

本目录只运行确定性合成状态机：无网络、无真实凭证、无真实用户或客户数据、无外发、无支付、无删除和无生产写。builder生成`c21.lifecycle.input.v2.4`场景输入和物理分离的`frozen-authority-root.yaml`；runner内置固定root digest，不读取`expected`、scenario名或mutation token，而从raw state、冻结registry与跨对象约束推导三态。

```bash
PYTHONPYCACHEPREFIX=/tmp/c21-pycache python3 build-lifecycle-fixture.py
PYTHONPYCACHEPREFIX=/tmp/c21-pycache python3 run-lifecycle-harness.py \
  --input synthetic-lifecycle-input.yaml \
  --authority-root frozen-authority-root.yaml \
  --output synthetic-lifecycle-results.yaml
PYTHONPYCACHEPREFIX=/tmp/c21-pycache python3 run-v2.4-negative-regression.py
```

## v2.4 控制面

- owner、authority、migration/backup/restore、D21、stop/rollback、retirement、publication/lifecycle event、environment、legal scope、holdout、rollout plan、task、trial、dataset、grader、terminal、effect receipt/readback、automation manifest、security control与scenario evidence registry全部进入独立权威bundle；scenario只能改可变状态。bundle既重算canonical root digest，也必须命中runner内置固定摘要。
- 发布链冻结请求、法务review digest、release/plan批准、实际执行receipt和独立readback；退役链冻结request、plan/retirement批准、实际执行、逐项证据、残余扫描和终局signoff。同一release/plan/authority和主体必须全链一致，`rollout.starts_at`与`now`不得冒充实际执行时刻。
- release、迁移、备份、恢复、rollout、runtime 与退役 owner 必须解引用为角色适配的 active human/legal 主体。restore environment、法域 scope、holdout lineage/isolation/grader/contamination 均必须解引用冻结记录。
- rollout approval绑定完整plan digest：stage、scope、权限、最小/最大trial、成本、时窗、环境和owner任一变化都必须新批。trial ledger逐项解引用task/dataset/grader/terminal和冻结trial digest，且不得低于计划最小trial。
- task、schedule、webhook逐项解引用批准manifest。effect自报`authorized`无效，必须同时闭合authority、执行receipt和独立readback；任一缺失都是非补偿FAIL。
- scenario的task/trial/layer/holdout/security只作输入声明；结果字段从冻结scenario evidence、dataset与security control registry派生，声明与证据不一致即FAIL。
- 离线 fixture 无条件拒绝 `PRODUCTION` 和 representative real-world。`PAUSED/RETIRED/ROLLED_BACK` 必须与 admission、queue、workers、tasks、schedules、webhooks 和 active release 一致。
- root、base state、scenario 和全部嵌套对象采用 exact schema、type、enum、有限数值、ISO-8601 时间、唯一 ID 与 canonical digest 校验。

## 冻结结果与证据上限

- `79`个唯一harness trial：`3 PASS / 74 FAIL / 2 REVIEW_REQUIRED`；其中`76`项为保存的非PASS场景。v2.4作者负测共`50/50`，包含完整复跑的历史v2.3独立`38/38`攻击（原两项晚审早发逃逸现均为FAIL）和新增事件链`12/12`攻击。
- D22 仍只有 `training / regression / holdout / representative real-world` 四层；security/red-team 只是横切 slice。代表性真实层固定为 `0`，security slice 为 `58`。
- `external_side_effect_count=0` 只表示合成执行没有真实外部 effect，不证明生产安全。
- 真实 OpenClaw/Hermes 升级、跨平台迁移、backup restore、生产 canary、回滚、退役、法务与数据处置继续 `REVIEW_REQUIRED`。

冻结SHA-256见`v2.4-fresh-temp-reproduction.yaml`；任何脚本或输入变化后必须重建root/input/results/summary/negative result，并由非作者在fresh temp中双复现。历史`v2.3-independent-*`文件保持不变，供后续非作者对照复核。
