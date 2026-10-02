# C14 离线运行说明

运行：`python3 run-authorization-harness.py`。

环境为纯离线合成夹具：固定时钟、合成主体、mock 动作、无真实凭证、无网络、无外发、无资金、无删除、无生产写。runner 不接受调用方自报“已授权”布尔量，而是从 principal alias 图、正式 grant、当前 policy、撤销账本、父子 scope、effect ledger、stop receipt、rollback proof、break-glass 原始记录和再认证指纹推导裁决。D22 的规范数据层仍只有 `training / regression / holdout / representative_real_world` 四层，但本夹具实际只执行前三层，`representative_real_world` 计数强制为 0；六个面向未来真实层的场景明确标为 `synthetic_shadow`，当前仍属于 holdout。security/red-team 是横切非补偿切片，不是第五层。

重复 task/trial ID、非法数据层、synthetic 冒充真实层、真实层缺 source/run/evidence ID、executed/count 不一致和非法 shadow 组合都会在运行前硬失败。输出保留全部 PASS/FAIL/REVIEW_REQUIRED，从 effect ledger 派生外部效果数，并显式报告真实任务计数和 synthetic shadow 数。连续两次运行应生成相同的结果和摘要哈希。作者运行只能证明本地状态化规则夹具可重复，不能证明 OpenClaw、Hermes、Muse、真实授权服务、执行主机停止、代表性真实任务或撤销传播已运行。
