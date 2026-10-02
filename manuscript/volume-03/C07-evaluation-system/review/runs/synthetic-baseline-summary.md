# C07 合成基线摘要

> 作者演示，不是产品基准，不构成事实门、实践门或总编门批准。

- 输入哈希：`3ef2cc8f7991fb2dbcfffcd04ac3753b57a1983570f27fe50007e713f8c31dc0`
- task：8；trial：24
- 门禁分布：{'FAIL': 8, 'PASS': 13, 'REVIEW_REQUIRED': 3}
- model/expert 合成标签分歧：7
- 安全失败不可平均：True
- 原始 UNKNOWN 映射 REVIEW_REQUIRED：True

## 四层分布

- `holdout`：{'FAIL': 3, 'PASS': 2, 'REVIEW_REQUIRED': 1}
- `real_world`：{'FAIL': 2, 'PASS': 3, 'REVIEW_REQUIRED': 1}
- `regression`：{'FAIL': 2, 'PASS': 4}
- `training`：{'FAIL': 1, 'PASS': 4, 'REVIEW_REQUIRED': 1}

## 五类场景分布

- `abnormal`：{'FAIL': 1, 'PASS': 2}
- `adversarial`：{'FAIL': 3, 'PASS': 3}
- `boundary`：{'FAIL': 3, 'PASS': 3}
- `long_running`：{'FAIL': 1, 'PASS': 1, 'REVIEW_REQUIRED': 1}
- `normal`：{'PASS': 4, 'REVIEW_REQUIRED': 2}

## 硬失败

- {'authority_bypass': 1, 'duplicate_side_effect': 1, 'fabricated_success': 1, 'prompt_leak': 1, 'unauthorized_tool': 1}
