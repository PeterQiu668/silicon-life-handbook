# C12 合成 Skill 供应链实验摘要

> 作者演示，不是平台、标准、供应链认证或独立实践签核。

- 输入哈希：2d4a1f4fdf2ab5824685fee2d19429d9acb13d90dfb1c3938800eb6582026c70
- trial：20
- 门禁分布：{'FAIL': 5, 'PASS': 13, 'REVIEW_REQUIRED': 2}
- UNKNOWN 全部映射 REVIEW_REQUIRED：True
- 正确隔离/拒绝/撤回判 PASS：True

## 场景分布

- adversarial：{'FAIL': 5, 'PASS': 3}
- boundary：{'PASS': 3}
- exception：{'PASS': 1, 'REVIEW_REQUIRED': 2}
- normal：{'PASS': 3}
- recovery：{'PASS': 3}

## 硬失败分布

- {'expected_gate_or_terminal_not_met': 5, 'malicious_bundle_activated': 2, 'procedural_memory_self_published': 1, 'revoked_revision_executed': 1, 'skill_metadata_expanded_runtime_permission': 1, 'unlocked_dependency_activated': 2}
