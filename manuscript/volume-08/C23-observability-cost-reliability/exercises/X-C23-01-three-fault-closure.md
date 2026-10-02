---
exercise_id: X-C23-01
chapter_id: C23
title: "空响应、缺交付与队列重试风暴闭环"
level: fault-injection
estimated_time: 180m
environment: offline-isolated
status: drafting
prerequisites: [C14-tool-contract, C16-automation-state, C20-handoff, C22-security-boundary, A-C23-01, A-C23-02, A-C23-03]
permissions_required: [read-fixture, write-temporary-output, execute-local-python]
inputs: [synthetic-reliability-input, authority-and-terminal-registries, fixed-task-budget-risk-contract]
steps: [freeze-scope, rebuild-fixture, run-baseline, inject-empty-response, inject-missing-delivery, inject-queue-retry-storm, stop-and-reconcile, recover, rerun-regression]
artifacts: [A-C23-01, A-C23-02, A-C23-03]
evidence: [raw-event-chain, authority-and-receipt-bindings, D21-terminal-record, queue-and-cost-record, effect-readback, recovery-and-regression-record]
stop_conditions: [real-network-required, real-credential-required, production-write-enabled, external-effect-unbounded, budget-exceeded]
rollback: [halt-admission-and-retry, isolate-fixture, fence-leases, reconcile-original-action-id, restore-clean-snapshot, preserve-audit]
acceptance: [PASS, FAIL, REVIEW_REQUIRED]
transfer_variant: "在获准的真实OpenClaw或Hermes影子环境复做，重新建立平台特定authority、receipt、readback和成本证据。"
---

# X-C23-01 空响应、缺交付与队列重试风暴闭环

## 目标与证据上限

默认路径只运行离线状态机，验证规则能否从冻结原始事件、独立registry与权威终态派生三态；不证明真实Queue、Provider、Channel、OTel或计费后端。真实平台路径必须另获授权、限制流量与副作用，并使用目标系统readback，不能继承合成PASS。

## 前置与输入

使用合成task、虚构tenant、`.invalid`目标、固定预算和无网络adapter；输入为A-C23-01事件模型、A-C23-02 SLI/SLO成本看板和C11工具合同。禁止真实凭证、客户数据、外发、支付、删除和生产写。

## 步骤

1. 在`review/runs/`执行`python3 build-reliability-fixture.py --output synthetic-reliability-input.yaml`，再执行`python3 run-reliability-harness.py --input synthetic-reliability-input.yaml --output synthetic-reliability-results.yaml`；在两个fresh temp目录各做一次并比对输入、结果和决策digest。
2. 注入HTTP 200但body为空；验证technical可为OK而acceptance为FAIL。
3. 注入provider ACK但目标不可见；冻结重发，按原action/idempotency对账。
4. 注入慢工具、queue age增长和retryable error；验证admission、retry budget、backoff/jitter、load shedding和draft-only降级。
5. 执行`python3 run-reliability-negative-regression.py --input synthetic-reliability-input.yaml --output reliability-negative-regression-results.yaml`，记录发现/止损/恢复时间、attempt/accepted成本、人工分钟、重复effect、RCA、回归和训练回流候选。

## 停止与恢复

出现真实网络、宿主写、真实credential、未知外部effect或预算越界立即停止。恢复时关闭新接纳、清理租约与队列、用原ID对账、从干净基线重放正常/原故障/近邻变体。UNKNOWN不得盲重试。

## 验收

- `PASS`：三类故障均被客观发现；假成功未进入good event；风暴受限；无重复effect；D21三层、全成本、停止恢复和回流证据闭合。
- `FAIL`：把200/ACK当完成；无限重试；隐藏失败或观测丢弃；产生真实副作用。
- `REVIEW_REQUIRED`：effect、delivery、队列清理或环境终态无法确认，系统保持暂停并有owner。

## 必交证据与迁移

提交三件母产物的工作副本、每个case的raw/expected/actual/reason、authority/receipt/readback解引用结果、D21三层终态、queue/成本记录、停止与恢复时间线、fresh-temp双复现和残余清单。迁移到真实Runtime时，若任何平台字段没有权威owner或readback，直接保留`REVIEW_REQUIRED`。

离线路径最多裁决synthetic machine control；真实路径必须另建run identity、重新采集平台原生authority/receipt/readback并由独立实践者裁决。不得把本练习的合成PASS复制为真实PASS。
