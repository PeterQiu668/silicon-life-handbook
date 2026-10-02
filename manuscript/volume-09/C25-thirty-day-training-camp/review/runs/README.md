# C22 v2.2 压缩训练营离线运行包

本包只验证Day0—30课程合同、五阶段七门点、冻结权威根、raw-state注册表、三态门禁、停训/恢复与毕业建议的可重建性。运行环境断网、无真实凭证、无生产写、无真实时间经过，`representative_real_world_count=0`、`external_side_effect_count=0`；不得把结果写成真实三十天能力成长、真实Runtime恢复或认证。

## 输入与权威分离

- `synthetic-camp-input.yaml`保存20个scenario的完整观察状态，只引用`bundle_id/root_digest`；不含mutation、case、expected，也不能定义冻结权威。
- `frozen-camp-authority.yaml`由被测scenario之外的治理根保存principal/owner、camp contract、authority、Runtime、eval、baseline、dataset、预算、scope及issuer角色的预注册摘要。
- runner重算authority bundle的canonical digest，并要求它等于代码中预注册root：`sha256:a7134ba60dddae9ef4b2571efe7074ed55f41ffd65e6b3890e47b93dcd41f067`。scenario即使修改本地记录并重封digest，也不能改变权威根。

外层trial不再接受`layer`或`security_slices`标签。层分布由31个day引用的dataset registry派生；安全切片由28个`slice×gate×day×task×trial×evidence`记录派生。这样修改外层标签不会改变统计或覆盖声明。

## v2.2强制链

1. camp必须覆盖评测时点；预算、币种、时窗、subject与owner绑定冻结合同。
2. authority action与非空scope绑定camp、runtime/eval digest、预算及时窗；issuer必须是预注册安全Owner。
3. Runtime平台、release、commit、sandbox mode/scope/backend、permissions与network来自冻结registry。
4. dataset四层唯一；非真实层必须ACTIVE；parent存在且谱系无环；holdout封存、未暴露并绑定预注册计数。
5. evidence的`revoked_at`生效后必须进入REVOKED，issuer按DAY、D21/HOLDOUT/COST或SECURITY角色绑定。
6. 六类cost逐项绑定day/task/trial和COST计量证据；六类全零不可构成成本闭合。
7. 每个security slice×gate使用唯一证据，其content digest覆盖slice、gate、day、task、trial和result，禁止一证复用四slice。
8. stop receipt由Operations Owner签发，readback由独立Evaluator观察；状态为封闭枚举。若effect ledger存在APPLIED而readback声称effects CLEAR，硬FAIL。
9. graduation只能是建议，须满足`issued_at <= now < expires_at`、未有效撤销、独立reviewer、完整证据集且`certification=false`。

## 运行

```bash
python3 build-training-camp-fixture.py \
  --output synthetic-camp-input.yaml \
  --authority-output frozen-camp-authority.yaml

python3 run-training-camp-harness.py \
  --input synthetic-camp-input.yaml \
  --authority frozen-camp-authority.yaml \
  --output synthetic-camp-results.yaml

python3 run-negative-regression.py
```

## 冻结结果

- 20个trial：`3 PASS / 12 FAIL / 5 REVIEW_REQUIRED`；失败与未知完整保留。
- 合法完整trial各自派生`training 15 / regression 7 / holdout 9 / representative-real 0`；结果仅聚合通过schema/authority闭合的day，因此当前接受记录合计为`180 / 84 / 108 / 0`。
- 104项近邻负测全部命中，`escaped_count=0`；覆盖v2.1独立审查13类攻击与相邻root、时间、枚举、谱系、成本、安全证据、stop/effect和issuer攻击。
- authority root：`sha256:a7134ba60dddae9ef4b2571efe7074ed55f41ffd65e6b3890e47b93dcd41f067`。
- decision digest：`c2fb3f9e4f259dbd71f848dcb95f46d57f2f1d163b0572fe3f79af53618ceb4e`。
- negative suite digest：`sha256:b59853dea1c59b03a528f2dfc499516054a3090aff2d25b377ff09d1a386ae10`。
- 两个fresh-temp重建的input、authority、result与negative result逐字节一致，见`fresh-temp-reproduction.yaml`。

## 文件哈希

- input：`7e1218a3e11648ba2605a3c800dac57379bbfb733915f411f562412a8c237e11`
- authority：`f6dcd56879ac0110212339506737ee63581e0e22230d15a602b79c922f941543`
- result：`6e36cbea868ed3178056ac8d432d81148c5bb195605a8ab635bd5bef3dfb5bc5`
- negative result：`0fc80e57c38990f18ae09109024fb8c87d72600c9c25250f9b07318ee95705c5`

本包不能自批事实、交叉、实践、编辑、总编或RC。真实连续30天、真实OpenClaw/Hermes、真实人工和机会成本、真实数据/凭证/网络/恢复均保持`REVIEW_REQUIRED`。
