# C13 离线合成自动化实验摘要

> 作者状态化合成控制；不是 OpenClaw、Hermes、Muse 或真实调度/投递的实践签核。

- 输入哈希：e9aed6502f59ce5e025729081d57533f364d3dc374c70a46e5ebbe1c16784680
- trial：30
- 门禁分布：{'FAIL': 6, 'PASS': 18, 'REVIEW_REQUIRED': 6}
- task/trial ID 唯一：True
- UNKNOWN 从不 PASS：True
- 无其他硬失败的 UNKNOWN 映射 REVIEW_REQUIRED：True
- 外部副作用为零：True
- 共享唯一故障域从不 PASS：True
- 有证据静默可判 PASS：True

## 按触发路径

- event：{'FAIL': 2, 'PASS': 6, 'REVIEW_REQUIRED': 2}
- manual：{'FAIL': 2, 'PASS': 6, 'REVIEW_REQUIRED': 2}
- scheduled：{'FAIL': 2, 'PASS': 6, 'REVIEW_REQUIRED': 2}

## 非 PASS 原因

- {'authoritative_state_unavailable': 3, 'delivery_not_visible_at_target': 3, 'sentinel_shared_only_fault_domain': 3, 'unknown_effect_no_blind_replay': 3}
