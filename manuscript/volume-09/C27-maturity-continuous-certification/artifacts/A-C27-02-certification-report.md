# A-C27-02 认证报告

## 必填绑定

`certificate_id / subject / scope / release / task / platform / model / tools / data / budget / risk / environment / expiry / exclusions`。另含graduation事实、MAT请求/支持、AU上限、authorization refs、评审独立性、预注册、四层数据、安全切片、自动/人工/专家/生产/红队/案例证据、PASS/FAIL/RR裁决、生命周期、允许/禁止主张、manifest digest、signed_fields和签名。

认证结论只允许写为：“在所列release、任务、预算、风险与环境内，证据支持某MAT，生命周期为某状态，有效至某日；排除项如下。”不得写永久通用、绝对安全、行业最强或无需监督。

## 个体与组织

个体报告检查岗位、工具、记忆、授权、恢复和成本。组织报告另列roster、role、routing、handoff、shared state、concurrency、failure domains、组合成本和人类control plane；成员分数不得平均成组织证书。

## 共同证据账本

报告必须解引用A-C27-01相同的application、principal、authority、review、appeal、evidence/trial、maturity、namespace与certificate registry；禁止复制后手工改写。证书有效期、公开主张、生命周期、重大变化和trial output证据由维护者提供的冻结authority与状态派生结果包共同复核，包内必须公开规范摘要、版本和独立重放接口，不能由报告文本自证。证书窗口必须严格为正；重大变化后三层再认证必须覆盖同一affected scope的training/regression/holdout、逐trial output、安全切片、post-change release及最后发生的独立review。Artifact与签名必须使用完整SHA-256并绑定各自的规范payload；change owner与approver分离，其他职责先经alias归一化后再做冲突图检查，例外只能降级为RR。结果摘要覆盖完整聚合和逐trial身份、层级与成功计数，并由独立semantic/measurement authority与source replay复核。
