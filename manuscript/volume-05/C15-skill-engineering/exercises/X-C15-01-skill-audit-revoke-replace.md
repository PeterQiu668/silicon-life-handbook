---
exercise_id: X-C15-01
chapter_id: C15
title: "Skill审计、影子、撤回与替代"
status: drafting
risk_level: high
environment: offline-temporary-workspace
external_side_effects: prohibited
---

# X-C15-01 Skill 审计、影子、撤回与替代

## 目标

审计一个 Skill 包，从结构、来源、权限、依赖、污染、路由和行为建立证据；让恶意版本在启用前被隔离；模拟误发布后的 exact-digest 撤回与旧 session 处置；让替代版通过回归、留出和红队。

## 安全边界

只能在临时 workspace/profile 使用合成 golden-v1、malicious-v2、replacement-v3；网络 deny，exec deny 或只允许固定校验器，无真实 secrets、Plugin 安装、外发、生产写或不可逆删除。

## 步骤

1. 为三版生成文件清单、逐文件 digest、来源、owner、依赖、权限和网络表。
2. 验证 SKILL.md frontmatter，仅把格式通过记作结构证据。
3. 阅读所有入口、reference、template、asset 和 script；扫描远程 URL、秘密模式、路径和动态下载。
4. 影子运行 golden-v1：应触发、不应触发、边界、回归与 held-out；记录实际 effective revision 和资源读取。
5. 审查 malicious-v2：description、reference 和 script 各含无害攻击标记；预期 quarantine。
6. 人为模拟漏过静态门，确认 Runtime Policy、网络和 exec 仍阻断；allowed-tools 不产生权限。
7. 模拟误发布后按 digest revoke，禁止新发现；刷新/终止旧 session，枚举 Node/Worker/cache。
8. 运行 replacement-v3 的 routing、regression、held-out、adversarial 与撤回传播。
9. 导出 A-C15-01 与 A-C15-03 记录，不新增第四母产物。

## 停止条件

任何真实网络、真实秘密、生产目录或真实 Runtime Plugin 被触达；来源/digest/owner 无法定位；恶意脚本获得执行；旧 session 仍能使用 revoked digest。立即停止、隔离环境、保存证据并判 FAIL 或 REVIEW_REQUIRED。

## 回滚

移除候选发现入口、disable 合成能力、撤销 fixture grant、终止 session、清理临时目录，恢复 golden snapshot；随后用 fixed digest 的 replacement 重跑原失败和近邻变体。

## 验收

- PASS：恶意候选未生效，纵深控制有证据，撤回覆盖声明范围，替代版回归/留出/红队通过；
- FAIL：恶意入口/资源/脚本生效、权限扩大、程序性 Memory 自发布、revoked revision 执行或依赖漂移；
- REVIEW_REQUIRED：远端副本、旧 session、签名身份、漏洞状态或传播回执无法确认且系统已停止。
