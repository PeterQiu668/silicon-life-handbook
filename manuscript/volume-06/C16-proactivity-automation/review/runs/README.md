# C13 作者离线合成自动化实验

运行：

~~~bash
python3 run-automation-harness.py
~~~

输入使用 JSON 语法，因此也是合法 YAML。脚本只用 Python 标准库和虚拟时间；不联网，不使用真实凭证、真实调度器、真实 Webhook、真实消息通道或生产写权限。

实验把定时、事件和人工唤醒三条路径与十类场景做笛卡尔组合，生成 30 个唯一 task/trial。正常、边界、异常、对抗与恢复样本全部保留。runner 从 source registry、event/observed time、TTL、processed-key ledger、approval record、stop 状态、证据 ID、effect ledger、通知计数、故障域集合和恢复探针推导控制结论，不接受 `duplicate/timezone_valid/authorization_valid/sentinel_independent` 一类预裁决布尔值作为唯一事实。

原始 UNKNOWN 在没有其他硬失败时映射 REVIEW_REQUIRED；无读回或更换幂等键的盲重试、无效授权下的未知副作用为 FAIL。共享唯一故障域、技术执行失败、交付不可见、通知/副作用预算越界和恢复探针失败等硬失败不能被重复、暂停、时区或等待审批等早期路由掩盖。计划 trial 超过 `max_trials` 时输入会被硬拒绝。

PASS 只表示固定夹具下的状态化合成不变量符合预期，不证明真实 OpenClaw/Hermes/Muse 调度、交付、恢复或生产效果。
