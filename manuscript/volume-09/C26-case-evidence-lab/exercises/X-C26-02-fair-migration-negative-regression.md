# X-C26-02 公平迁移与负向回归

离线路径：运行builder，并以`--authority-root frozen-evidence-root.yaml`执行harness与回归。固定OpenClaw `v2026.9.6 / eb377ac…`和Hermes `0.20.1 / f80f453…`，逐项锁定suite manifest、scenario projection、author assignment、alias、release status、environment、五类task/input/permission/dataset/grader authority、budget case/task/run/side与成本构成、结构化adapter及运行分布。两个全新临时目录生成的input/root/result与语义重放回归必须逐字节一致；32 trial保持固定分布，全部历史与当前负测保留原始输出且不得有语义逃逸，真实claim和外部effect动态计数必须为0。

负测另需覆盖：删scenario、删FAIL trial、删effect、并行Artifact/principal/release/budget、跨案例作者替换、撤回或错版本assignment、FAILURE_LOG晚于D21/评审/公开、双边同改task/input、双边扩权或替换生产数据、作者自评grader、跨scenario预算成对互换、RECONSTRUCTED空限制、同总额不同成本构成、PUBLIC_CASE或厂商页伪装adapter证据、migration contract脱离budget registry、重复JSON键、effect回执与readback不一致、伪分布与未来publication。另设合法task和input authority重钉正邻，二者都应PASS；拒绝输入、FAIL与RR按合同区分。

真实路径：在另获权限后，分别于两个真实Runtime执行同合同并保存各自原生状态、权限、成本、D21与恢复证据；当前未执行，因此X02完整实践门仍为`REVIEW_REQUIRED`。任一不支持项必须RR或N/A，不能用质量总分补偿。
