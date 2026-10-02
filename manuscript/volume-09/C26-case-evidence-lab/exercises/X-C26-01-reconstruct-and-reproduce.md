# X-C26-01 重建、匿名与独立复现

选择一个有授权的历史案例，回到原始任务、日志与Artifact，先在隔离副本完成八段档案和五类身份候选。登记subject/case/version、来源、处理与公开授权、版权、原始/公开digest、脱敏映射、环境manifest、预算分项、D21完成三面和撤回状态。作者不得把候选直接写成`VERIFIED-REAL / ANONYMIZED-REAL`；真实身份必须由外部事实门批准。

离线路径：先以`SYNTHETIC / RECONSTRUCTED`运行当前harness，至少三trial且保留失败；`RECONSTRUCTED`必须同时给出非空`missing_elements`与`inference_list`，并与source差异逐项一致。第二评审者单独取得冻结root与场景输入，核对root/suite-manifest digest、全部单值与集合projection、案例级author assignment、grader authority、alias归一化、角色/独立组，以及`trial <= failure <= FAILURE_LOG <= D21 <= reviewed_at <= released_at <= evaluation_time`因果链，不能与作者共享别名或grader私答。验证result时必须同时提供冻结source并重放语义；模块导入、函数别名、partial和CLI都不得提供省略source的接受路径。input、root与result须在解析前拒绝任意层级重复JSON键。受控真实路径仍需另获授权并使用真实环境；任何撤回、选择性删样、来源身份错配、公开时间倒置、D21失败或effect失账均FAIL。

停止条件：撤权、污染、secret/个人信息暴露、来源或版权失败、证据链断裂。回滚：冻结发布，撤下公开件，吊销授权和链接，保全原始证据，恢复合成稿。练习交付只能声明“离线合同通过”或“受控真实路径待审”，不得自批案例身份。
