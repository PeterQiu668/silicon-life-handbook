# C15 离线运行说明

运行 `python3 run-drift-harness.py`。固定输入对 D20 五类漂移逐项扩展 15 个基础测试，共 75 个唯一 trial；覆盖正常、边界、异常、对抗与恢复。runner 从 baseline/observed bundle、独立 run/trace、dataset access、grader hash、candidate exact diff、稳定主体、批准记录、当前 target、shadow ledger、effect ledger 和完整 rollback manifest 推导裁决，不消费调用方自报的“已漂移、已批准、已回滚”布尔量。

D22 的规范数据层仍只有 `training / regression / holdout / representative_real_world` 四层，但本夹具实际只执行前三层，真实任务计数强制为 0；三个基础测试展开成十五条 `synthetic_shadow`，只表示未来拟映射到真实任务层。security/red-team 为横切非补偿切片。环境纯合成、无网络、无真实凭证、无外部写；runner 会硬拒绝重复基础 test ID、展开 ID 冲突、synthetic 冒充真实层、真实层缺 source/run/evidence ID、非法 shadow 或 executed/count 不一致，并从 effect ledger 派生外部效果数。作者运行只验证状态化规则夹具可重复，不证明真实平台、影子、canary、回滚或固化。
