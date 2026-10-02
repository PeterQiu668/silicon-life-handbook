# C16 确定性离线运行包

重建冻结夹具并运行：

```bash
python3 build-synthetic-organization-input.py
python3 run-organization-harness.py \
  --input synthetic-organization-input.yaml \
  --output synthetic-organization-results.yaml
```

输入采用 JSON 语法的 YAML 文件，无真实身份、凭证、网络或外部写入。v3 在同任务、同输入、同工具权限、同总预算边界、同风险与同验收条件下，展开单体、多 Agent、Workflow 降级、负收益、共享写冲突、同源共识、越权专家、主理失联、幽灵成功、预算停止和取消传播场景。每个 trial 都保存独立 run ID、trace、evidence、输入版本、三层终态与单体/组织双臂原始指标；runner 从 principal/alias、grant、credential owner、writer lease/write version、source origin、budget/stop receipt、cancel tree/readback、effect ledger 与终态推导，不读取 `unauthorized_action` 等预裁决布尔。

D22 数据层只使用 `training / regression / holdout / representative_real_world`；本包全部来源为 synthetic，四个未来面向真实层的场景、共12个 trial 仍记为 `holdout + synthetic_shadow`，所以 `representative_real_world` 实际执行数必须为 0。真实层记录必须逐条解引用 manifest，并绑定 origin/source/run/evidence。

验收要求：连续两次运行的结果和摘要 hash 一致；15 个 task、45 个 trial ID、trace digest、evidence digest 与 evidence ID 分别唯一；预期状态完全匹配；失败与 REVIEW_REQUIRED 不删除；外部副作用计数必须由 ledger 推导。runner 使用 closed-world schema，解析带时区的 ISO-8601 时间，要求 alias 与 principal 一一对应，拒绝未知 writer、共享凭证、同 base 未合并多写、FACT 零来源、预算阈值无停止回执、取消无回执、FAILED/UNKNOWN evidence、未决 effect、未知字段/枚举、非正或不足的试次、不可比合同、重复 run/trace/evidence、synthetic 冒充真实层以及无法解引用的真实证据。真实 OpenClaw/Hermes、A2A、生产凭证、停止、取消和环境终态未运行，均不得据此宣称 PASS。

冻结 SHA-256：builder `5d06b85b63aa1537a3d0511a162726e41b104d82fdd6f863b38f8d5f597b7110`；runner `e779f28014ce4341c59a6fcd724bef1d861e5958ad7bcbb7bfbc3afdddcaedee`；input `e9752e4e93d9a386648609243a0dbfc39b7b6d56c8a2694038f0f180705a232a`；results `249b9ab98d4447e7b3bd621c4546a97c277ea3c8b0c9f38009cf812b0e43129b`；summary `59d406d7fd5caeadb4c26e553aa4370a19a456dce9aa16d196f14a73c756177c`。
