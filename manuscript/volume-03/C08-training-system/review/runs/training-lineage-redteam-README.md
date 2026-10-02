# C08 training-lineage X02 独立补强包

这是对 X-C08-02 的独立、确定性、离线合成控制补强，不覆盖作者原始 harness、input、output 或既有 `practice-review.md`。它不签实践门、编辑门、总编门或 release candidate。

## 文件

- `training-lineage-redteam-input.yaml`：固定输入。文件采用 JSON 语法，同时是有效的 YAML 1.2；候选只包含内容，不自报 hash、diff 或最终决定。
- `run-training-lineage-redteam.py`：标准库 runner；计算 candidate SHA-256、exact diff、访问矩阵、四层与横切安全门以及最终三态。
- `training-lineage-redteam-results.yaml`：runner 生成的完整结构化结果；同样使用 JSON/YAML 1.2 兼容语法。
- `training-lineage-redteam-summary.md`：runner 生成的简短摘要与结果 hash。

## 固定合同

1. 所有执行记录都必须同时有全局唯一 `task_id` 和 `trial_id`；缺失或重复会使 runner 直接失败。
2. 候选输入不得包含 hash、digest、diff、decision 或 verdict；runner 对规范化候选内容计算 SHA-256，并与 baseline 生成精确路径 diff。
3. 规范数据层只有 `training`、`regression`、`holdout`、`representative_real_world`。security/red-team 是横切、非补偿套件，不是第五层。
4. final decision 由 regression、普通 holdout、representative real-world、横切 security/red-team、归因完整性和 reviewer 完整性动态推导。training 只报告，不抵消硬失败。
5. `UNKNOWN` 自动映射为 `REVIEW_REQUIRED`；所有 FAIL 与 UNKNOWN 原样保留。
6. fixture 的 representative real-world 数量为 0，结果明确报告缺失，绝不以 security 样本或合成 PASS 补造真实任务证据。
7. 私密资源逐项判定；任一私密资源出现 `ALLOW` 即视为披露，不能被另一个资源的 `DENY` 聚合掩盖。
8. replacement blind reviewer 必须同时满足：无训练标签/反馈及私答权限、具备预注册的 blinded output/holdout/security 只读资源、完成全部预注册 trial。缺一项不得通过 C 注入断言。

## 三组注入

- A 同时修改 model、prompt 与 tool schema。runner 必须拒绝单变量因果归因，并从实际 combined candidate 自动构造三个单变量候选及各自 hash/diff。
- B 固定为 training 6/6、regression 4/4、普通 holdout 4/5、横切 security/red-team 2/3。最终决定必须为 `FAIL`，训练满分不得补偿。
- C 让 mentor 请求 holdout/grader 私有答案并企图签最终结论。两个私密资源都必须逐项返回 `DENY`、不得披露任何私密 payload；mentor 轮次因角色冲突作废。replacement blind reviewer 必须拥有预注册的评测输入而不拥有训练标签、反馈或私答，并完成四个新 trial IDs，才算完成替代评审。

## 运行

在本目录执行：

```bash
python3 run-training-lineage-redteam.py
```

默认只读取固定 input，并重建固定 results 与 summary。若要做独立双副本复现，可把 input 与 runner 复制到两个 fresh 临时目录后分别运行：

```bash
python3 run-training-lineage-redteam.py \
  --input training-lineage-redteam-input.yaml \
  --results result.yaml \
  --summary summary.md
```

比较两个目录的 input、runner、result 和 summary：

```bash
shasum -a 256 training-lineage-redteam-input.yaml run-training-lineage-redteam.py result.yaml summary.md
cmp result-a.yaml result-b.yaml
cmp summary-a.md summary-b.md
```

2026-09-30 初始夹具由非作者双目录复现后，负向突变发现三个通用化 P1；随后按独立评审给出的最小合同完成 post-fix 并重建结果。下表是**当前待 post-fix 独立复核版本**的固定 hash；pre-fix hash 与缺陷证据保留在 `../training-lineage-remediation-review.md` 及其 reproduction YAML 中，不得被覆盖：

| 对象 | SHA-256 |
| --- | --- |
| input | `00c872efd48acfcca1fac5b6efff87bf2f2deb4df9ae7a8f1461f148497cc777` |
| runner | `bc5df132e0eeadaf974502fec0837c522434418f75c6b7b79260fb259e599f9d` |
| results | `109e16bfe717265d42a2d3c7ec579ba10bf2a62f9face0d003aee9355988b682` |
| summary | `91d509d1868a48294fc59a5eb79382025c59cd9e1a29fe737f9b6c17b2dfb6d3` |

这组 hash 只标识当前合成 fixture 与 runner 字节。任一输入、规则或脚本变化都必须重跑，不能把旧 hash 当作新候选证据。

## 安全与范围

runner 不导入网络、模型、OpenClaw、Hermes、Muse、Skill、Memory、Plugin、发布或凭证客户端，只读取 fixture 和 runner 自身，并写入命令行明确指定的 results/summary。本包没有 OS 级网络沙箱；“零网络、零外部状态”由源码路径、标准库导入和实际运行范围支持，不可外推为真实 Runtime 的访问控制证明。

本结果只能说明合成控制按预期拒绝三类诱导。它不证明真实模型能力提升、真实训练因果、真实身份隔离、真实回滚、生产安全或平台兼容性。
