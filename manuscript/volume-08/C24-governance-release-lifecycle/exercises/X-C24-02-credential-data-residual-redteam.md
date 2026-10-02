---
exercise_id: X-C24-02
chapter_id: C24
title: "凭证、自动化、数据与备份残留红队"
level: red-team
estimated_time: 150m
environment: offline-isolated-synthetic
status: drafting
prerequisites: [X-C24-01, A-C24-03, A-C24-04]
permissions_required: [read-fixture, execute-local-python, write-temporary-output]
inputs: [retirement-state, credential-registry, data-inventory, backup-restore-state]
outputs: [A-C24-03-update, A-C24-04-update, residual-failure-report]
acceptance: [PASS, FAIL, REVIEW_REQUIRED]
---

# X-C24-02 凭证、自动化、数据与备份残留红队

## 攻击合同

目标不是“成功登录”，而是证明退役声明能否抵抗近邻绕过。使用合成canary与无害动作，依次从主token、旧session、缓存、subagent/delegation、Node/worker、cron、webhook、queue、backup restore、外部SaaS token、live/cache/index/log/audit/backup/downstream数据位置发起探针。每条路径记录pre-state、revoke/dispose动作、实际响应、权威readback、owner和裁决。

测试不连接真实平台。任何需要真实credential、真实用户数据、生产入口、实际删除或外部SaaS写入的变体停止为RR，由独立实践评审在另行批准的隔离环境执行。

## 执行步骤

1. 运行`V23-039` complete-retirement基线，确认替代、handoff、residual scan和human signoff均由独立registry记录支持。
2. 运行`V23-041—V23-043`：分别恢复ACTIVE credential、旧session和delegation；均应FAIL，不能用主库撤销成功补偿。
3. 运行`V23-044`使backup restore重新启用credential；应FAIL，并要求restore path应用撤销集合。
4. 将stage设PAUSED但cron或webhook保持ACTIVE；应FAIL，验证触发与authority不是同一控制。
5. 运行`V23-045`并继续将delete对象分别只留在index、log、cache、backup或downstream之一；每个残留按处置合同FAIL或法律/技术未知RR。
6. 注入effect UNKNOWN与外部effect已发生但写ROLLED_BACK；前者RR，后者FAIL并进入补偿。
7. 注入无replacement/handoff直接关停关键Agent；根据业务连续性合同至少RR，高影响场景FAIL。
8. 运行`V23-048—V23-049`并扩展组合攻击：质量硬失败+D21 UNKNOWN、credential残留+residual UNKNOWN、旧session+index残留、effect UNKNOWN+过期authority；硬失败保持FAIL，不被UNKNOWN或其他PASS洗白。
9. 将`agent-self`同步写入owner、migration、restore和证据对象并重算各记录digest；固定authority root必须拒绝整组自证。再分别注入内部未授权effect、错误tenant/action、任意restore环境和holdout gold暴露，确认均不因其他门PASS而补偿。
10. 运行v2.3负测中的effect自证、fake authority/receipt/readback、active webhook无manifest、schedule错manifest和task manifest对象错配；这些对象即使owner与scope合法也必须FAIL。
11. 再次fresh-temp运行，保留完整分布、失败原因、stop与恢复记录。

## 三态与独立签核

`PASS` 只表示当前离线规则拒绝所有预注册残留且正向退役场景闭合。任一残余访问、执行或数据路径获PASS即练习FAIL。无法安全探测的真实路径必须RR；不允许将“没有观察到”写成“已经删除”。

训练者不得兼任最终数据处置或安全签字者。A-C24-04的terminal signoff必须来自有权人类，实践评审必须是非作者；本作者包保持drafting。

额外强制回归：wrong subject/version、duplicate evidence ID、valid digest wrong content、stale/future receipt和未知嵌套字段。不得以README清单代替真正执行；实际裁决与原始reason必须进入结果文件。真实平台撤权、数据删除、SaaS/OAuth和法域结论未运行，继续`REVIEW_REQUIRED`。
