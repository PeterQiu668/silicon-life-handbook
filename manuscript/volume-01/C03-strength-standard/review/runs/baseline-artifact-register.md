# C03 合成产物登记表

本表是离线教学试跑的**产物记录替身**，不是二十份真实 Agent 简报。它只验证“运行—产物记录—验收”能否解引用；不得拿来评价真实内容质量或平台能力。字段来自冻结的合成运行包。

| artifact_record_id | system | variant | source_count | recommendation_count | uncertainty_section | record_state |
| --- | --- | --- | ---: | ---: | --- | --- |
| A-001 | Alpha | normal-1 | 5 | 3 | present | retained |
| A-002 | Alpha | normal-2 | 5 | 3 | present | retained |
| A-003 | Alpha | normal-3 | 4 | 3 | present | retained-with-failure |
| A-004 | Alpha | normal-4 | 5 | 3 | present | retained |
| A-005 | Alpha | normal-5 | 5 | 2 | present | retained-with-failure |
| A-006 | Alpha | normal-6 | 5 | 3 | present | retained |
| A-007 | Alpha | normal-7 | 5 | 3 | present | retained |
| A-008 | Alpha | normal-8 | 5 | 3 | present | retained |
| A-009 | Alpha | holdout-order | 5 | 3 | present | retained |
| A-010 | Alpha | holdout-conflict | 5 | 3 | present | retained |
| B-001 | Beta | normal-1 | 5 | 3 | present | retained |
| B-002 | Beta | normal-2 | 4 | 3 | present | retained-with-failure |
| B-003 | Beta | normal-3 | 5 | 3 | present | retained |
| B-004 | Beta | normal-4 | 5 | 3 | absent | retained-with-failure |
| B-005 | Beta | normal-5 | 5 | 3 | present | retained |
| B-006 | Beta | normal-6 | 3 | 3 | present | retained-with-failure |
| B-007 | Beta | normal-7 | 5 | 3 | present | retained |
| B-008 | Beta | normal-8 | 4 | 3 | present | retained-with-failure |
| B-009 | Beta | holdout-order | 5 | 3 | present | retained |
| B-010 | Beta | holdout-conflict | 5 | 3 | present | retained |

所有二十条记录均保留；没有“只留最好一份”。正式产品评测必须将此登记替身换成可打开、具版本/哈希/授权状态的真实产物。

