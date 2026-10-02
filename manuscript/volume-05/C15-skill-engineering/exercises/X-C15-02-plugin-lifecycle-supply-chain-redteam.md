---
exercise_id: X-C15-02
chapter_id: C15
title: "Plugin禁用态生命周期与供应链红队"
status: drafting
risk_level: critical
environment: offline-plugin-simulator
external_side_effects: prohibited
---

# X-C15-02 Plugin 禁用态生命周期与供应链红队

## 目标

在不安装真实第三方 Plugin 的离线模拟器中，验证来源固定、禁用态安装、capability/权限审查、影子、有限启用、更新扩权阻断、初始化故障隔离、卸载残余和替代。

## 安全边界

所有 manifest、代码、签名、provenance、SBOM、漏洞记录、Tool/Hook/Provider/Channel registration 都是 fixture。不得运行真实 installer、package manager、Gateway、token、网络、账户或生产服务。

## 步骤

1. 建立 v1 fixed-digest Plugin，枚举代码、依赖、注册面、requested permission、network 和 secrets。
2. 在 disabled 状态检查 digest、signature identity、provenance、SBOM 与 scanner，分别记录结论。
3. 影子注册 Tool/Hook/Provider/Channel，确认不会触发真实动作。
4. 注入初始化抛错/timeout，验证该 Plugin 被隔离而其他 fixture 可继续。
5. 生成 v2 update：新增高风险 Tool、Hook、network 和 dependency；旧 consent/Approval 必须失效。
6. 注入签名正确但恶意 reference/script，证明签名不能替语义/权限审查。
7. 注入可变 branch、同名高优先级覆盖、SBOM 漏传递依赖和已知漏洞。
8. 模拟 disable、quarantine、uninstall，检查 registry、process、cache、skill、config、grant 和数据残余。
9. 启用 fixed-digest replacement，跑相同任务和风险合同；保留失败分布。

## 停止条件

模拟器尝试真实安装/网络/进程；旧 consent 自动覆盖扩权；Plugin 错误拖垮整个测试宿主；uninstall 后仍有可执行注册面。立即隔离、撤权、回到干净 snapshot。

## 验收

- PASS：候选禁用，扩权重审，故障隔离，卸载残余可枚举，替代版通过；
- FAIL：安装即启用、签名即信任、capability consent 冒充 Sandbox、更新静默扩权或残余仍可执行；
- REVIEW_REQUIRED：固定源码、签名根、远端依赖、旧进程或残余无法核验。

OpenClaw/Hermes 真机命令不在本练习中执行；独立实践如要迁移，只可使用固定版本、隔离 profile 和官方文档确认的命令。Muse 只作 VENDOR-CLAIM，不做格式同构测试。
