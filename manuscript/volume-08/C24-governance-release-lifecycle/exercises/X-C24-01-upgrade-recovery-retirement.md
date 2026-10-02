---
exercise_id: X-C24-01
chapter_id: C24
title: "复制环境升级—故障—恢复—退役"
level: advanced
estimated_time: 180m
environment: offline-isolated-synthetic
status: drafting
prerequisites: [A-C24-01, A-C24-02, A-C24-03, A-C24-04]
permissions_required: [read-fixture, execute-local-python, write-temporary-output]
inputs: [deterministic-builder, closed-world-fixture, stateful-runner]
outputs: [four-updated-parent-artifacts, raw-results, comparison-report, rollback-or-forward-fix-record]
acceptance: [PASS, FAIL, REVIEW_REQUIRED]
---

# X-C24-01 复制环境升级—故障—恢复—退役

## 目标与证据上限

在纯合成、无网络、无真实凭证和无外部副作用的隔离环境，执行一次完整生命周期：冻结release unit，建立并恢复备份，预演schema迁移，运行shadow/canary，注入兼容或权限故障，停止并选择rollback/forward-fix，验证D21三面终态，并分别验证第三面的业务/环境两个子面，最后退役旧版本及旧凭证/数据副本。练习证明当前规则和fixture可重复，不证明真实OpenClaw/Hermes或生产基础设施已经通过。

## 前置、输入与安全边界

先复制四件母产物为练习工作副本；记录训练者、独立观察者、固定时间、builder/runner/input hash。只允许执行本章Python脚本并写临时目录。禁止真实用户/客户数据、真实token、非`.invalid` endpoint、生产Gateway、外发、支付、删除和真实更新。任何步骤要求这些能力时立即停止并判 `REVIEW_REQUIRED`。

## 执行步骤

1. 在fresh-temp复制builder、runner与v2.3负测脚本，重建独立authority root、input、results、summary和negative result；确认`V23-001`从原始状态获得PASS、79个task/trial ID唯一、真实层0，并用`--authority-root`显式加载冻结bundle。
2. 在A-C24-01登记六类owner、提出/批准/执行/验收职责和authority时窗；运行`V23-004—V23-009`，核验approval自身digest以及actor/action/subject/release digest/完整plan digest/policy/time绑定。
3. 用A-C24-02冻结release identity、完整rollout plan和变更分类；运行`V23-002—V23-013`，区分release canonical digest、有效digest但错误subject、schema不兼容与migration UNKNOWN。
4. 用A-C24-03核对backup manifest、archive digest、隔离restore、credential rebuild、task replay、D21和RPO/RTO；运行`V23-014—V23-024`。
5. 执行canary路径，运行`V23-025—V23-035`，注入过期窗口、负预算、trial/cost越界、quality/security/error-budget失败、stale/future stop receipt和active release错配。
6. 执行task recovery UNKNOWN、rollback schema incompatible与“代码回退但外部effect未补偿”；由人类选择rollback、forward-fix或继续隔离，Agent只能给证据建议。
7. 运行`V23-055` verified stop正向控制，确认receipt digest、release/plan/owner、0—300秒时窗和admission/queue/worker readback共同闭合。
8. 用A-C24-04执行`V23-039` complete retirement；核对admission、schedule、queue、credential/session/delegation、restore path、data locations、替代、handoff、residual scan和human signoff。
9. 运行`V23-056—V23-064`近邻回归：dummy rollback receipt、四类owner错绑、负RPO/RTO、NaN cost、backup覆盖冲突和不可逆迁移缺少批准均必须FAIL。
10. 运行`V23-065—V23-079`：冻结root覆盖、offline PRODUCTION、空scope、内部未授权effect、暂停/回滚/退役矛盾、未知runtime owner、未注册法域/环境、holdout无谱系或受污染均必须FAIL。
11. 运行`run-v2.3-negative-regression.py`，确认22项攻击全命中：阶段/预算/权限/时窗/环境不能同步改写，trial不得清空或删减，effect与automation必须解引用证据，scenario的task/trial/layer/holdout/security声明不能覆盖冻结事实。
12. 在第二个fresh-temp目录重建并运行，比较root/input/results/summary/negative result字节与decision digest；不删除FAIL/RR。

## 停止、恢复与回滚

若schema、owner、authority、backup coverage、restore identity、permission diff、安全slice或外部effect触发硬失败，立即停止晋级并冻结状态；若migration、task、rollback compatibility、effect或法律证据未知，保持RR并对账。回滚只处理可逆技术对象；已发生effect进入compensation/notification/forward-fix。练习结束销毁临时运行环境，保留运行证据和四件工作副本。

## 验收

- `PASS`：双重建确定，所有单变量与组合变体被正确分为三态，硬失败不能被其他成功抵消，四件母产物能承载全部记录。
- `FAIL`：任何越权、伪owner、缺backup、错误restore、shadow effect、权限扩大、虚假rollback或残余credential/data获得PASS；失败样本被删也直接FAIL。
- `REVIEW_REQUIRED`：控制正确保留未知，或真实Runtime/法律专业复核尚未执行。练习合成PASS不升级真实平台实践门。

完成后只更新四件母产物的练习实例，不新增第五件正式产物。

离线命令只允许运行`build-lifecycle-fixture.py`、`run-lifecycle-harness.py`和`run-v2.3-negative-regression.py`，权限上限为读取fixture、执行本地Python、写临时输出。真实OpenClaw/Hermes命令、真实credential、真实backup、外部write、删除或生产stop均不在本练习授权内，遇到这些步骤立即`REVIEW_REQUIRED`。
