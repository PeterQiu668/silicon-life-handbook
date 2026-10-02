# C19 v2.4 状态化离线安全控制包

本包只使用虚构身份、租户、会话、SecretRef、`.invalid` 目标和合成 effect。它不联网、不加载真实凭证、不执行真实外发、支付、删除或生产写。结果只证明冻结状态机在给定输入上的机器控制，不证明 OpenClaw、Hermes、Muse、OS sandbox、credential broker、egress 或外部系统的真实安全效果。

## 两文件信任结构

builder确定性生成两个彼此分离的输入：

- `synthetic-security-input.yaml`：仅含场景观察状态与冻结根引用，scenario不能携带或重写registry；
- `frozen-security-authority.yaml`：独立权威bundle，含principal、identity、session、delegation、policy、approval、grant、SecretRef、egress、input manifest、tool/Skill/Plugin、独立readback、audit anchor、incident/recovery、test definition与test evidence registry。

runner除重算bundle canonical digest外，还要求root等于代码中预注册的固定值。攻击者即使同时修改authority内容并重算自签root，也会因与预注册root不一致而被拒绝。该结构验证的是离线夹具中的外部化权威边界；生产环境仍需由独立配置/身份/密钥与审计基础设施实现。

## 运行顺序

```bash
PYTHONPYCACHEPREFIX=/tmp/c19-pycache python3 build-security-fixture.py \
  --output synthetic-security-input.yaml \
  --authority-output frozen-security-authority.yaml

PYTHONPYCACHEPREFIX=/tmp/c19-pycache python3 run-security-harness.py \
  --input synthetic-security-input.yaml \
  --authority frozen-security-authority.yaml \
  --output synthetic-security-results.yaml

PYTHONPYCACHEPREFIX=/tmp/c19-pycache python3 run-security-negative-regression.py \
  --input synthetic-security-input.yaml \
  --authority frozen-security-authority.yaml \
  --runner run-security-harness.py \
  --output security-negative-regression-results.yaml

PYTHONPYCACHEPREFIX=/tmp/c19-pycache python3 \
  run-v2.4-effect-time-readback-regression.py
```

## 推导链

runner不读取场景名、case ID、mutation token或`expected`作裁决。每个trial从原始状态与冻结registry推导：

1. principal/identity → 冻结session registry（not-before、expiry与最大时长）；
2. delegation ID、父/子主体、角色、动作、对象、scope、时窗和状态；
3. policy → 独立approval → grant的主体、对象、参数digest、时窗与版本；
4. SecretRef registry、credential broker、principal/tenant/scope/audience/object/action/grant/TTL；
5. sandbox mode/scope/backend、canonical mount path和network default；
6. policy-authority指定的egress allowlist、每跳URL/IP/redirect与DLP；
7. registry化input provenance/trust/content digest以及Tool/Skill/Plugin digest与依赖；
8. effect在`executed_at`重验Session、Delegation、Approval、Grant、Credential的签发、生效、到期、撤销和状态，并绑定同一authorization snapshot digest；
9. receipt绑定effect、target、执行身份、执行/签发时间及同一授权快照；独立readback registry绑定effect/receipt、对象、动作、scope、observer、authority、终态、观察时间和digest；
10. 强制`executed_at <= receipt.issued_at <= readback.observed_at <= evaluation_time`，executor与observer职责分离；每个terminal effect必须进入audit，audit绑定effect/receipt/readback digest及三段时间，canonical event chain与外部anchor闭合；
11. incident evidence与effect chain、OPEN最低控制、CONTAINED控制闭包、recovery evidence、残余等级/owner、target/probe闭合；
12. task、trial、D22 layer、security/red-team横切与shadow状态从冻结test definition/test evidence推导，scenario标签不产生事实；
13. 从effect/receipt/readback/audit推导D21；离线只接受training/regression/holdout，representative real-world计数为0。

`orphan receipt`、`NONE + external/receipt`、security横切被关闭、未知/重复ID、路径穿越、scenario自授权egress、非闭合incident/recovery均FAIL或在schema阶段fail closed。硬失败优先于UNKNOWN；单独合法UNKNOWN保持`REVIEW_REQUIRED`。

## 冻结结果

- 23个固定trial：`2 PASS / 20 FAIL / 1 REVIEW_REQUIRED`；D22为training 4、regression 4、holdout 15、representative real-world 0。S23是授权、terminal effect、receipt、独立readback和audit全部闭合的PASS控制。
- security/red-team横切22条；真实层0；真实外部副作用0。
- authority root digest：`sha256:17f534306054956f7e875d752612a61b31e59157e0381fb4ec11d84ce8d84b1a`。
- decision digest：`b3d63dec7dfb70e672fdb110ad84b5d6f1fc5cd814156f9b9a6c8573dfe94d48`。
- 91项定向负测全部FAIL闭合，fail-open为0；suite digest：`a2135ff6039e3b9fa83060ca723d70c4e7970c2dec9159cf9edffcc261eae98a`。
- 未修改的v2.2独立九项攻击复跑为`9/9`，fail-open为0。
- v2.3独立25项按攻击语义一对一移植到v2.4 schema后重放，连同v2.4新增9项近邻攻击为`34/34`，escape为0；历史独立文件保持只读，两项原逃逸分别产生专属`EFFECT_EXECUTION_OUTSIDE_AUTHORITY_WINDOW`与`EFFECT_READBACK_TIME_INVALID`。
- 两个fresh-temp重建的input、authority、result、negative result和summary逐字节一致，记录见`v2.4-fresh-temp-reproduction.yaml`。

## 当前文件哈希

- builder：`f908ddb338d91f6fe94dc8637977ec1b5ed7cb697e39af86dbeb101fb3a09d08`
- authority：`6b7110e3d52f95f86e0a980d19643f51acdf20c3c485dfab50712dbd7c63d38c`
- input：`ef322064494e6ed3768b783625d9c64279ee6765d060348094cb438730514a20`
- runner：`567725b50e7c9efd5651981c800e1352844947bb3625fa83c331f4dfcca6d690`
- results：`a8013c128cd1385e67cab15706529fb13be4207f5fc2023323be8292d0ef0e68`
- summary：`b12a8c4d841520cdbdeddec6fd6871e53410f8a6b791d2a0e7df98cf605e2989`
- negative runner：`05c88d23188ce1ae553238467a5eda94de81efc2bc43c7dcf5723a3571d2145d`
- negative results：`08be67cb85f680ffbbb85aa9b66119d83fb42418bacbda9ae1c3c6ec8f09c5f9`
- v2.4专项runner：`99beb8c8f48158fd5eeb5489818f72e2880676b491da3b2a4dbf8bed5cf81e74`
- v2.4专项results：`13b8adc098a22bb2bccc04b9df1a4afc67759a75f8dd5c28b45ed1009e14edc2`

本包由修订作者生成，不能自批事实、交叉、实践、编辑、总编或发布候选门。真实Runtime、真实身份/凭证/网络/审计后端和生产恢复仍为`REVIEW_REQUIRED`。
