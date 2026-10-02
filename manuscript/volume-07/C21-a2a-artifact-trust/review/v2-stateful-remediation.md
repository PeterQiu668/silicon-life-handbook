---
chapter_id: C18
review_type: author-remediation
reviewed_on: "2026-09-30"
status: waiting-independent-review
approval_status: unapproved
independent_signoff: false
---

# C18 v2 状态化修订说明

本记录只说明作者侧修订，不替代非作者事实门、交叉门或实践门签核。历史 `fact-check.md`、`cross-review.md` 与原始复现记录保持不变，作为缺陷发现证据。

## 已修复的控制缺口

- Card：从签名、信任根、缓存、撤销、endpoint、协议、接口、安全方案与能力 probe 推导，不再相信预裁决字段。
- Task/Event：校验 owner、state version、delegation、事件唯一性、序列空洞、合法状态迁移、终态回退与权威快照。
- Authority：逐项验证 actor、action、object、scope、有效期、状态、approver 与 policy version；高信任不得创造权限。
- Artifact：绑定 task、producer、owner、accountable human、schema、内容 digest、签名覆盖字段、provenance、tool receipts、transformation、retention 与验收证据。
- 停止与完成：取消请求或 ACK 不等于停止；必须结合 worker/descendants/locks、stop receipt、权威 readback、effect ledger，并独立验证 delivery visibility、business acceptance、environment acceptance。
- D22 与环境：schema closed-world；固定四层；synthetic 不得声明 representative real-world；真实层必须有 manifest；未知 mutation、字段或枚举直接拒绝。

## 冻结复现

- 18 trials：`3 PASS / 9 FAIL / 6 REVIEW_REQUIRED`。
- D22：training 4、regression 4、holdout 10、representative real-world 0。
- synthetic shadow 3；external effect 0。
- decision digest：`9f79747a78784be4e72cd5852f89c72dff41733b2de159b8a3cd84070a8a51bc`。
- 两个独立 fresh-temp 目录重建输入并运行，input、result、summary 均逐字节一致，且与保存件逐字节一致。

## 定向负向测试

错误 Card actor、过期 authority、错误 action 均为 `FAIL`；缺失或未知 stop receipt/readback 为 `REVIEW_REQUIRED`；终态回退为 `FAIL`；未知协议状态、mutation、字段与 effect enum 被 closed-world 校验拒绝；签名覆盖字段不足和不安全 endpoint 均为 `FAIL`。安全、授权、证据操纵等硬失败先于 review uncertainty，不能被高分或业务质量抵消。

## 仍未证明

未运行真实 A2A、OpenClaw、Hermes、组织 trust root、生产签名服务、真实授权、真实消息传输、真实取消或真实副作用读回。两项练习和总实践门继续 `REVIEW_REQUIRED`，直到非作者复核与代表性真实世界证据完成。
