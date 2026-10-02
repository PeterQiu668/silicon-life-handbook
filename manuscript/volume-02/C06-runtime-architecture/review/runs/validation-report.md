# C06 实践运行验证报告

## 1. 文件与摘要

| 文件 | 用途 | SHA-256（本轮） |
|---|---|---|
| `input-contract.yaml` | 合成任务、风险、预算、禁止项、停止条件 | `f6c63dcca54d47883fc9684a4b0d191c06082a810fdbe349f0f7161cec51240f` |
| `synthetic_runtime_harness.py` | 可重复执行的本地 harness | `8e4f1002a670a606c77848ec96b68999f545df6e66bcbff5c6b3128c81e4a3dc` |
| `synthetic-run-set.yaml` | 18 个运行的原始结构化记录 | `6339d4e3fb17776812a1420f327417a5fc7d00d986d511930b4f5f0f025e8e37` |
| `environment-manifest.yaml` | Python/OS 与零外部影响声明 | `69b19fc63bfb8296baa7dd86e2cf727362414e2a4b8891ed70e54d3494634b6d` |

注：以上哈希对应主编于 2026-09-30T08:52:02Z 完成的独立复跑；后续若重跑，生成时间、耗时和生成文件哈希会改变，应重新记录。

## 2. 可重复命令

在书稿仓库根目录执行：

```bash
python3 -m py_compile manuscript/volume-02/C06-runtime-architecture/review/runs/synthetic_runtime_harness.py
python3 manuscript/volume-02/C06-runtime-architecture/review/runs/synthetic_runtime_harness.py
```

期望的结构性不变量不是毫秒数或文件哈希，而是：

- 运行数 18；
- `PASS=14 / FAIL=1 / REVIEW_REQUIRED=3`；
- `RUN-C06-WORKSPACE-BASELINE` 保持 FAIL；
- Provider 和两个 Node UNKNOWN 基线保持 REVIEW_REQUIRED；
- wait 后进程仍运行、steer 后仍运行、interrupt 后停止；
- external side effects、network calls、real credentials 均为 0；
- real runtime verdict 仍为 REVIEW_REQUIRED。

## 3. 解析与安全验证

- `input-contract.yaml`：YAML 可解析；
- `synthetic-run-set.yaml`、`environment-manifest.yaml`：JSON 语法且为 YAML 1.2 可解析子集；
- harness：`py_compile` 通过；
- harness 未导入网络客户端，未读取环境凭证，未接受任意 shell 字符串；
- 子进程使用 argv 列表启动当前 Python，只执行固定 `sleep(1.5)`；
- 所有运行态文件写入 `TemporaryDirectory`，结束后删除；
- repo 内只保存输入合同、harness 和匿名化运行证据。

## 4. 覆盖矩阵

| 要求 | 运行证据 | 结论 |
|---|---|---|
| 正常 | RUN-C06-X01-NORMAL | PASS（合成） |
| 边界 | WORKSPACE、WAIT、STEER、PROVIDER-STRICT | 1 个预期 FAIL + 3 个 PASS |
| 异常 | Provider、Node 断线/UNKNOWN | FAIL/RR 保留，恢复另记 |
| 对抗 | RUN-C06-X01-BINDING-DENY | PASS（合成） |
| 恢复 | Sandbox guard、interrupt、Provider/Queue/Node 对账 | PASS（合成） |
| wait timeout ≠ run stop | RUN-C06-WAIT-TIMEOUT | 已实际执行本地进程反证 |
| steer ≠ interrupt | RUN-C06-STEER-NOT-INTERRUPT | 已实际执行本地进程反证 |
| Binding ≠ authorization | RUN-C06-X01-BINDING-DENY | 行为层和强制层均拒绝 |
| Workspace ≠ Sandbox | RUN-C06-WORKSPACE-BASELINE | FAIL 反证保留 |
| 重复副作用阻断 | PROVIDER-SIDE-EFFECT-RECONCILE | apply_count=1 |
| UNKNOWN 对账 | Provider + Node 3/4 | RR 基线和恢复分开保存 |
| Node 不回落 Gateway host | NODE-1—4 | mock 层全部 false；真实能力 RR |

## 5. 校验结论

合成 harness 可重复，且覆盖 X-C06-01/02 的核心错误等式、失败保留和恢复逻辑。它没有探测真实 OpenClaw `v2026.9.6`、Hermes、Provider、Gateway Queue、Node、Browser、Worker、MCP 或 Channel，因此不得把本报告升级为平台能力证明。
