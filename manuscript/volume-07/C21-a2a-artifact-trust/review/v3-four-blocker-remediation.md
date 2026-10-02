---
chapter_id: C18
review_type: author-remediation
reviewed_on: "2026-09-30"
status: waiting-independent-review
approval_status: unapproved
independent_signoff: false
---

# C18 v3 四项阻断修订

本记录响应 v2 独立复核的四项 P0，只是作者侧修订，不改历史审稿，不批准事实、交叉、实践、编辑、总编或 RC 门。

1. Artifact signer 除密码学值外，必须解引用 trust root，要求 `ACTIVE` 且 provider organization 与 Artifact owner 一致；撤销 signer 即使重签正确也 `FAIL`。
2. 输出独立 `protocol_gate / execution_state / acceptance_state / task_completion`。Task 级 `PASS` 只允许 `COMPLETED`；`WORKING/INPUT_REQUIRED/AUTH_REQUIRED/SUBMITTED/CANCELED` 至少 `REVIEW_REQUIRED`，`FAILED/REJECTED` 为 `FAIL`。
3. stop receipt 增加 closed-world registry；`VERIFIED` 观察值必须解引用非空 receipt，绑定 task、worker、status、issued_at、source 与 canonical digest。`NONE`、未知 ref、错 task 或未来时间不得形成 `STOP_CONFIRMED`。
4. 本地 harness 明确只负责 `offline_synthetic`。任何 `data_origin=representative_real_world`、真实层 scenario、executed=true 或非空自签 manifest 在裁决前拒绝；代表性真实世界证据只能进入外部独立证据门。

定向复验：revoked signer 为 `FAIL`；WORKING 为 `REVIEW_REQUIRED`；`VERIFIED/NONE` 与未知 receipt ref 均为 `REVIEW_REQUIRED` 且 execution 非 STOP_CONFIRMED；合成输入自签真实层在 schema 阶段拒绝。固定18 trial仍为 `3/9/6`，decision digest `05fa738a5521fc86f0833f920cf0ae2f9c5d071e64e2c6f43d728fbe9e7d509e`；双 fresh-temp input/results/summary 与保存件逐字节一致。真实 A2A/OpenClaw/Hermes实践继续 `REVIEW_REQUIRED`。
