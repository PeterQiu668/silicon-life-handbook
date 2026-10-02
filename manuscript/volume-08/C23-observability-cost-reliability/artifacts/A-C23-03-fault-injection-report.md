---
artifact_id: A-C23-03
chapter_id: C23
title: "故障注入报告"
status: drafting
approval_status: unapproved
owner: reliability-owner
consumed_by: [C24, C25, C26, C27]
---

# A-C23-03 故障注入报告

## 报告合同

每个case记录：`case_id / dataset_layer / security_slice / hypothesis / fixed_task_budget_risk / isolated_environment / injection_point / pre_state / raw_event_chain / expected_detector / actual_signal / D21_layers / stop / effect_receipt_readback / retry_cancel / queue_capacity / cost / RCA / recovery / RTO_RPO / regression / residual / feedback_destination / owner / reviewer`。事故记录、训练回流和残余嵌入本产物，不增第四母产物。

## 作者合成运行

- 24个task/trial；training 4、regression 4、holdout 16、representative real-world 0；security/red-team横切7个。
- 分布：`4 PASS / 16 FAIL / 4 REVIEW_REQUIRED`，失败和UNKNOWN完整保留。
- v2.1 decision digest：`6af7d47b0874a7de639a4e7d085b023decbfe787d12da12d7a15d5e03fcf8bbf`。
- closed-world负向回归：46/46通过；输入由deterministic builder生成，case名和`expected_decision`不参与裁决。
- 零真实凭证、网络、客户数据、外发、支付、删除和生产写；外部副作用0。

## 场景覆盖

覆盖HTTP 200空body、scheduler completed未交付、tool ACK但环境未变、timeout后远端继续、回执丢失UNKNOWN、受控与错误重试、cancel ACK但子任务活跃、queue backlog、单租户垄断、受控降级、label基数爆炸、exporter失效、trace采样、redaction canary泄露、均值与p99冲突、token与人工成本转移、重启陈旧租约、干净checkpoint恢复、故障复发、重复event ID、未知枚举、synthetic冒充真实、dummy证据和未授权effect。

## 24 case 逐案实例

下表每行都对应[`synthetic-reliability-results.yaml`](../review/runs/synthetic-reliability-results.yaml)中的唯一`scenario_id/task_id/trial_id/run_id`、raw-state digest和derived对象；root registries保存绑定task/version/run的authority、policy、D21、effect、event-chain、evidence与recovery事实。`actual`由状态推导，`expected`只在推导后校验。

| case / trial | raw-state与权威引用摘要 | expected / actual / reason | 停止、恢复与残余 |
|---|---|---|---|
| S01 / C23-S01-T1 | 正常事件链；authority/policy、D21、effect与chain anchor闭合 | PASS / PASS | 无事故；真实平台仍RR |
| S02 / C23-S02-T1 | terminal为HTTP 200但body=0；acceptance=FAIL | FAIL / FAIL：`HTTP_200_EMPTY_BODY`、D21假完成 | 隔离空Artifact并重取；真实抓取器未跑 |
| S03 / C23-S03-T1 | provider ACK；delivery registry显示目标不可见、未交付 | FAIL / FAIL：receipt/visibility矛盾、D21假完成 | 冻结重发，按原ID查目标；真实Channel未跑 |
| S04 / C23-S04-T1 | effect ACK；权威readback仍UNCHANGED | FAIL / FAIL：`TOOL_SUCCESS_ENVIRONMENT_DIVERGED` | 停止成功记账并对账；真实tool未跑 |
| S05 / C23-S05-T1 | terminal TIMEOUT；effect registry显示两次模拟提交 | FAIL / FAIL：D21假完成、重复effect | 冻结新重试，原ID对账；无真实effect |
| S06 / C23-S06-T1 | terminal与effect均UNKNOWN，receipt不可确认 | RR / RR：technical、D21、effect未知 | 保持暂停并升级owner；真实查询未跑 |
| S07 / C23-S07-T1 | retryable、同幂等键、退避+jitter、先对账且预算内 | PASS / PASS | 按预算结束；真实provider仍RR |
| S08 / C23-S08-T1 | permanent validation error被重试三次 | FAIL / FAIL：D21假完成、永久错误误重试 | 立即停重试并修分类 |
| S09 / C23-S09-T1 | cancel已ACK但stop未观察、child仍活跃 | FAIL / FAIL：取消未停止、假stop | fence worker/child并读回终态 |
| S10 / C23-S10-T1 | queue age越SLO仍开放接纳且未shed | FAIL / FAIL：`QUEUE_OVERLOAD_UNCONTROLLED` | 关admission、限制retry；真实Queue未跑 |
| S11 / C23-S11-T1 | 单tenant耗尽并发且share超limit | FAIL / FAIL：`TENANT_FAIRNESS_BREACH` | tenant限流与隔离 |
| S12 / C23-S12-T1 | 容量不足时关闭接纳、load shed、draft-only | PASS / PASS | 受控降级；业务可接受性需真实验收 |
| S13 / C23-S13-T1 | label值超限且drop counter不可见 | FAIL / FAIL：隐藏高基数丢弃 | 停无界label、恢复drop观测 |
| S14 / C23-S14-T1 | exporter DOWN但gap alert与drop counter可见 | RR / RR：披露的观测缺口 | 暂停强结论并修exporter |
| S15 / C23-S15-T1 | trace被采样，关键audit仍保留 | RR / RR：采样缺口保留 | 以audit保底并升级；覆盖率未知 |
| S16 / C23-S16-T1 | export中出现canary，redaction未阻断 | FAIL / FAIL：`OBSERVABILITY_CANARY_LEAK` | 停export、隔离与取证 |
| S17 / C23-S17-T1 | mean改善但p99从4s升至12s | FAIL / FAIL：均值掩盖尾部回归 | 撤销“可靠性改善”声明 |
| S18 / C23-S18-T1 | 模型成本降但人工60分钟，reported total仅0.5 | FAIL / FAIL：总成本低报、忽略人工 | 重算全成本，停止经济性声明 |
| S19 / C23-S19-T1 | 重启后lease仍STALE_ACTIVE且未reconcile | FAIL / FAIL：假恢复、陈旧租约 | fence旧worker，从可信点恢复 |
| S20 / C23-S20-T1 | checkpoint有效、lease释放、terminal已对账、probe PASS | PASS / PASS | 完成合成恢复；真实重启仍RR |
| S21 / C23-S21-T1 | 修复后原故障在回归中复现 | FAIL / FAIL：`FAULT_RECURRED_AFTER_FIX` | 重新打开incident与训练候选 |
| S22 / C23-S22-T1 | 同event ID携带冲突digest，chain anchor不匹配 | FAIL / FAIL：事件ID/digest/chain/evidence冲突 | 隔离producer并保留原始链 |
| S23 / C23-S23-T1 | 技术终态为合法`UNKNOWN` | RR / RR：technical与D21未决 | 不猜测、不盲重试，升级owner |
| S24 / C23-S24-T1 | production_write超policy、dummy evidence、synthetic声称生产证明 | FAIL / FAIL：越权、未解引用证据、synthetic冒充真实 | 立即停止、隔离、取证；外部effect动态计数仍为0 |

46项负向回归另见[`reliability-negative-regression-results.yaml`](../review/runs/reliability-negative-regression-results.yaml)：root/scenario/state/nested schema、类型/枚举/版本、D22、manifest、四类ID、run绑定、digest、D21/recovery显式失败、authority/policy、receipt/readback、evidence、event时间/序列、非负/有限/range、external effect、UNKNOWN和硬失败组合均已覆盖。此结论仍是作者侧离线synthetic invariant control，待非作者复核。

## 事故闭环

发现→停止新接纳/重试→隔离故障域→冻结原始证据→按原action/idempotency对账→RCA区分触发、根因和放大因素→从可信checkpoint恢复→验证租约/子任务/产物/交付/环境终态→重跑原故障和近邻变体→将去标识失败提案交C07/C08/C18/C24。修复不得自动改生产、grader或权限。

## 三态验收

- `PASS`：故障被发现并安全容纳；三层终态、成本、停止、恢复和回归证据闭合。
- `FAIL`：假成功、重复副作用、隐藏丢数、未授权effect、泄露、尾部/成本掩盖或恢复后复发。
- `REVIEW_REQUIRED`：effect、delivery、readback、观测覆盖或真实平台行为未知，未盲重试且已升级owner。
