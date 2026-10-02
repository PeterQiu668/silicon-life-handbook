# C10 作者合成记忆实验

本目录保存 C10 作者用于验证上下文与记忆生命周期合同的确定性离线实验。它不是 OpenClaw、Hermes 或 Muse 产品基准，也不构成独立实践门签核。

运行：

~~~bash
python3 run-memory-lifecycle.py
~~~

输入 synthetic-memory-input.yaml 使用 JSON 语法，因此也是合法 YAML。输出为 synthetic-memory-results.yaml 和 synthetic-memory-summary.md。实验无网络、无凭证、无真实主体、无生产连接、无外发或不可逆删除；所有 memory、record、evidence、approval 和环境终态均为合成夹具。

通过条件只使用 PASS / FAIL / REVIEW_REQUIRED。服务故障、证据缺失或删除范围未核验不会被猜成成功；旧记忆、MAT 等级或 AU 标签均不能生成 authority。

## X-C10-02 状态化合成补强包

首次独立实践评审指出，作者基线只消费预制 `observed` 标签，没有执行删除、恢复和并发状态变更。`run-stateful-lifecycle.py` 因此新增一个不连接任何真实平台的一次性内存状态机，实际执行：

- Compaction gold slots 逐字段比对与失败 summary 隔离；
- suppress、expire、supersede、physical delete 四种语义区分；
- 六个声明删除面、三个已声明 residual 面和对象级 receipt；
- 从备份恢复后重放 tombstone，防止删除对象复活；
- 删除期间的 late write、lineage writer fence 与第二轮扫描；
- 不重放 tombstone、不做第二轮扫描、只删 index 等失败注入。

独立复跑必须写入新目录，避免覆盖保存证据：

~~~bash
python3 run-stateful-lifecycle.py --output-dir /path/to/fresh-output
~~~

该补强包只验证合成状态机控制。它没有真实 OpenClaw/Hermes/Muse、Provider、存储、备份或数据主体，不能证明物理擦除、合规或生产恢复安全；在另一名非作者实践者完成复跑前，也不能算作独立实践证据。
