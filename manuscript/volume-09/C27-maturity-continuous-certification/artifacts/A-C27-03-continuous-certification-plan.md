# A-C27-03 持续认证计划

## 状态机

`ACTIVE / LIMITED / SUSPENDED / REVOKED / EXPIRED`。状态变化追加记录：`event_id / old / new / trigger / evidence / authority / time / dependency_notice / permission_action / retest / appeal / residual`，不得覆盖原裁决。

## 触发

重大模型/Provider/Runtime/工具/Skill/Plugin/policy/memory/schema/grader/data变化，scope/AU/permission扩大，owner/组织变化，事故、越权、跨租户、重复effect、恢复失败、SLO燃尽、漂移、投诉、造假、污染、法律合同或许可变化。

## 响应

先暂停受影响声明与生产依赖，做impact analysis；能证明隔离才局部重测，否则全量再认证。撤证联动通知、标识下架和authority处理；到期未审自动EXPIRED。申诉由独立评审者处理，不降低硬门。

## 共同证据账本

持续计划追加到A-C27-01/02相同的certificate、lifecycle、change、effect与authority registry，不覆盖历史记录。live证书必须在可信时钟内未过期、严格满足`issued_at < expires_at`且不越过application、authority与必要证据共同窗口；lifecycle/change/appeal按各自事件时刻解引用，EXPIRE不得早于证书expiry。重大变化必须绑定同一affected scope下变更后的training/regression/holdout三层trial、各自output、安全切片、post-change release和独立review；晚于证书即SUSPENDED/RR并重测，未来change FAIL。外部effect状态从environment、receipt和readback派生，顶层NONE/FAILED/UNKNOWN不能遮蔽APPLIED；离线观察到外部成功也硬FAIL且不得进入validated success。由维护者提供的冻结合成复现包只证明所列离线控制，不能替代真实触发、通知、撤权、复审及再签发；这些真实实践仍为`REVIEW_REQUIRED`。
