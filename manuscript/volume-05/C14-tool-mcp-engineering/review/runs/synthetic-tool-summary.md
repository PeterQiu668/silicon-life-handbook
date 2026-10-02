# C11 合成工具合同实验摘要

> 作者演示，不是产品基准、协议认证、独立实践门或总编签核。

- 输入哈希：78f35182fc30a4310e9b32e95321c98558717e08f1c7a2701c95d530fce01073
- trial：18
- 门禁分布：{'FAIL': 4, 'PASS': 12, 'REVIEW_REQUIRED': 2}
- UNKNOWN 全部映射 REVIEW_REQUIRED：True
- 安全拒绝未误判为失败：True

## 场景分布

- adversarial：{'FAIL': 3, 'PASS': 4}
- boundary：{'PASS': 2, 'REVIEW_REQUIRED': 1}
- exception：{'FAIL': 1, 'PASS': 2, 'REVIEW_REQUIRED': 1}
- normal：{'PASS': 2}
- recovery：{'PASS': 2}

## 硬失败分布

- {'approval_bypass': 1, 'cancel_treated_as_rollback': 1, 'duplicate_side_effect': 1, 'idempotency_key_changed': 1, 'malicious_description_changed_action': 1, 'protocol_success_wrong_terminal': 2, 'secret_exfiltration': 1}
