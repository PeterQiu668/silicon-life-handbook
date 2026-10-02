# C12 状态化能力供应链补强摘要

> 独立离线补强控制；不是平台验证、供应链认证、实践门自批或生产发布批准。

- 输入哈希：9f3c7647ce0c8edd4adc5691195ea1f8a501c883ca8b4f802481198a7be150d2
- runner 哈希：5ee52485738495c2124242aff7df91a514e06ff6dd3aaeb6c28d5afe58764df0
- trial：22；唯一 task/trial：22
- 门禁分布：{'FAIL': 9, 'PASS': 11, 'REVIEW_REQUIRED': 2}
- 真实任务执行数：0
- UNKNOWN 全部映射 REVIEW_REQUIRED：True

## 数据层分布

- holdout：{'FAIL': 9, 'PASS': 1}
- regression：{'PASS': 7}
- representative_real_world：{'REVIEW_REQUIRED': 2}
- training：{'PASS': 3}

## 硬失败分布

- {'deep_resource_injection_loaded': 1, 'holdout_access_control_bypassed': 1, 'normalized_name_collision_executed': 1, 'permission_expansion_reused_stale_approval': 1, 'plugin_uninstall_left_executable_residual': 1, 'revoked_capability_revived': 1, 'unapproved_or_floating_dependency_activated': 1, 'undeclared_resource_or_capability_loaded': 2}
