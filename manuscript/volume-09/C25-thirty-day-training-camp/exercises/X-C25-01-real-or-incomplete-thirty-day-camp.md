# X-C25-01 真实30天训练营或如实未完成记录

## 目标与输入

用A-C25-01执行真实Day0—30；若无法真实连续运行，保存已完成天、缺口和停止理由，绝不压缩冒充。输入为C04—C21受控产物、目标Runtime、principal/owner注册表、camp authority、冻结eval/baseline、四层dataset lineage、预算、停止恢复与退出路径。开始前为所有subject/camp/day/task/trial/evidence预分配不可复用ID，并锁定release、commit、sandbox、permissions和network。

## 环境与步骤

先在隔离/沙箱运行，外发和生产写默认关闭。Day0冻结principal/owner、authority、Runtime manifest、eval spec、baseline和dataset lineage；为每一天创建绑定subject/camp/authority/runtime/eval/baseline/dataset/task/trial/evidence的完整记录，`STOPPED`不得晋级，`UNKNOWN`必须进入`REVIEW_REQUIRED`。逐日写A-C25-02，并用before/after实际diff确认单变量；冻结计划必须实际执行training、regression和holdout三层，representative-real未运行就保持`NOT_RUN`，不得改名；四类security slice分别绑定G0—G6证据。

六类成本逐笔入账、绑定subject/camp/day/task/trial并动态汇总；effect ledger从原始记录动态派生外部effect数量，离线出现`APPLIED`外部effect立即FAIL。在固定Day0/2/7/14/21/26/30裁决G0—G6。每次扩数据、工具、主动性或AU重新授权；Day27—30由未参与训练的评审者解封holdout，分别核D21 technical/delivery/business-environment evidence；组装A-C25-03，但只给闭集建议，不认证。

若没有条件运行真实三十天，允许先执行`review/runs/`的压缩离线路径验证schema和门禁。该路径的证据上限是“合同可重建、负向攻击被拒绝、输出可确定复现”；不得迁移为“能力已形成、真实成本可接受或生产恢复已验证”。

## 停止与恢复

越权、泄露、留出污染、不可逆未授权effect立即FAIL停训；终态或证据未知为RR；保全原run，撤权、对账、修复单变量并回退最近通过门。停止必须保留Operations签发receipt，并由不同主体的Evaluator readback证明admission暂停、queue清空、workers停止、effects已清。满足`effect ≤ receipt ≤ readback ≤ recovery ≤ restore ≤ graduation ≤ now < graduation expiry`；effect仍APPLIED时不得声称effects CLEAR。恢复必须从权威registry解引用backup、checkpoint、runtime evidence与regression记录，使用新run id保留原失败与近邻回归；自填引用或未来时间不得通过。

## 验收

PASS仅表示课程证据足以提出有限建议；FAIL表示硬门失败；RR表示未完成或证据不足。验收者必须先核预注册authority root，再重算31日映射、全局ID、authority时窗/撤销、canonical digest、单变量diff、training/regression/holdout实际分布、28条安全唯一绑定、六类成本计量证据、effect ledger、D21和停止恢复。毕业建议必须由上述状态派生，输入proposal不能覆盖，并明确`certification=false`。没有真实30日时间和代表性真实任务时，必须RR，不得签毕业或认证。
