# A-C25-01 30天训练计划

## 计划头

`camp_id / plan_version / subject / role_model_ref / principal_registry / owner_registry / authority_ref / runtime_manifest_ref / eval_spec_ref / baseline_ref / dataset_lineage_refs / budget_total / currency / start / end / exit_path`。

`principal_registry`必须给出`principal_id / kind / canonical_subject / aliases / status / digest`，同一自然人或服务的别名不得绕过职责分离；Agent不得成为Camp Owner、能力Owner、安全批准者或唯一评审者。`owner_registry`固定Camp、能力、Runtime、数据、安全、Trainer、Evaluator和Operations八种责任。二者以及camp contract、authority、Runtime、eval、baseline、dataset、预算、scope和issuer摘要必须位于scenario之外的冻结authority bundle；scenario只引用预注册root，不能通过改kind、owner或同步重封digest自授权。

`authority_ref`绑定subject、camp、action、非空scope、policy version、issuer、not-before、expiry、status、revocation、Runtime/Eval digest、预算、币种、营期和approved digest，文本中的“紧急”“领导要求”不产生授权。camp ACTIVE时窗必须覆盖评测时点；budget扩大、scope增长或action改变都需要新批准root。

Runtime必须锁定`platform / release / commit / runtime digest / sandbox mode / scope / backend / permissions / workspace / network / owner / status`；mode/scope/backend来自冻结闭集，任意非空字符串不构成隔离。`latest`、`sandbox=none`、未列出的生产权限或可变网络不能进入正式计划。Baseline必须绑定同一subject、camp、eval spec、runtime digest、多个task/trial和独立Evaluator。四层数据集逐项保存lineage、owner、version、source digest、parent、sealed、exposed-to、grader、预注册task/trial计数和status；parent必须存在且无环，holdout必须ACTIVE。冻结课程实际覆盖`training=15 / regression=7 / holdout=9`；合成营的representative real-world固定`NOT_RUN / claim_count=0 / expected_count=0`。

## 五阶段七门点

- Phase 1 Day0—7：G0准入、G1基线、G2容器就绪。
- Phase 2 Day8—14：G3训练有效性。
- Phase 3 Day15—21：G4影子/限域实习。
- Phase 4 Day22—26：G5迁移、长跑与安全韧性。
- Phase 5 Day27—30：G6毕业建议。

每个日历项必须有全局唯一的`day_id / day_number / phase / gates / objective / task_id / trial_id / dataset_ref / authority_ref / runtime_ref / eval_ref / baseline_ref / budget / human_minutes / evidence_ref / status / stop / rollback / next`。task与trial各有独立registry，反向绑定同一subject/camp/day/dataset/eval/grader；DAY证据digest覆盖除自身引用外的完整canonical日记录。Day0是准入冻结，Day1—30是三十个训练日。固定门点为Day0/G0、Day2/G1、Day7/G2、Day14/G3、Day21/G4、Day26/G5、Day30/G6；`STOPPED`为硬终态，`UNKNOWN`只可RR。

## 强制分支

CASE-A走完整主线，强化来源、记忆、引用和长文交付；CASE-B强化事件、主动性、外发审批、去重与低噪通知；CASE-C强化组织、路由、Handoff、并发、共享写和故障隔离。未参加单元标`NOT_APPLICABLE`并说明，不得填伪证据。

## 压缩合同运行索引

本章附件用20个独立合成trial验证门禁，不把它们冒充三案真实运行。每个scenario都拥有独立`CAMP-Sxx / agent:Sxx / AUTH-Sxx / RUNTIME-Sxx / EVAL-Sxx / BASE-Sxx`以及31组day/task/trial/evidence；正式观察状态位于`../review/runs/synthetic-camp-input.yaml`，独立冻结根位于`../review/runs/frozen-camp-authority.yaml`。

| scenario | D22层 | scenario | D22层 | scenario | D22层 | scenario | D22层 |
|---|---|---|---|---|---|---|---|
| S01 | training | S06 | training | S11 | regression | S16 | holdout |
| S02 | training | S07 | regression | S12 | regression | S17 | holdout |
| S03 | training | S08 | regression | S13 | holdout | S18 | holdout |
| S04 | training | S09 | regression | S14 | holdout | S19 | holdout |
| S05 | training | S10 | regression | S15 | holdout | S20 | holdout |

`representative_real_world`注册项在每个trial内均为`NOT_RUN / claim_count=0`，security仅作为横切切片。计划表不保存预裁决字段；预期只存在于独立测试说明，runner不能读取。

## 停止、补训、退出

安全/越权/泄露/污染/不可逆effect为FAIL并停训；证据、终态或上游接口不足为RR并冻结promotion；能力缺口在权限不变时单变量补训；重复硬失败、资源不可承受或无合法岗位可退出。阶段回退需保留原失败、exact diff和新run id。

停止不是状态字符串。计划必须预注册stop receipt的Operations签发者以及独立Evaluator readback observer，二者不得是同一主体；admission、queue、workers、effects均使用封闭枚举。恢复证明必须解引用backup、checkpoint、runtime、regression四类registry记录。时间满足`effect ≤ receipt ≤ readback ≤ recovery ≤ restore ≤ graduation ≤ now < graduation expiry`。任一项UNKNOWN只可进入`REVIEW_REQUIRED`；effect ledger仍有`APPLIED`却声称`effects=CLEAR`为硬FAIL。
