---
review_id: C12-independent-stateful-remediation-review-20260930
chapter_id: C12
review_type: independent-practice-remediation-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_remediation_author: true
chapter_status_after_review: drafting
offline_stateful_machine_control: PASS
post_fix_regression: PASS
machine_control_scope: post_fix_synthetic_invariant_control
x_c12_01: REVIEW_REQUIRED
x_c12_02: REVIEW_REQUIRED
p0_05: REVIEW_REQUIRED
p0_06: REVIEW_REQUIRED
p0_07: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C12 状态化能力供应链补强独立复核

## 0. Post-fix 关闭复审（2026-09-30）

**当前最终版通过 post-fix synthetic invariant control。** 两个新的 fresh temp 原样复跑与作者当前保存结果逐字节一致；22 个唯一 task/trial 对、D22 四层、四层均有 security 横切覆盖、`11 PASS / 9 FAIL / 2 REVIEW_REQUIRED`、UNKNOWN→REVIEW_REQUIRED、九项硬失败不补偿及 `run_schema_invariants_pass=true` 均稳定复现。当前有效哈希为：

| 对象 | 当前 SHA-256 |
| --- | --- |
| input 原始字节 | `e2fd30d6e7a801cd75f832fc7019b4d147dc3deeebdca838ab80f63e8878db10` |
| runner | `5ee52485738495c2124242aff7df91a514e06ff6dd3aaeb6c28d5afe58764df0` |
| 作者 result | `40cf553c8e50f65a9a1ff9af6cb0c1efceeec289b5ed34ee5a1549f7bfdce444` |
| 作者 summary | `347bfeb2db91c21ef2ef3d1130cc7411d8e57bef67571ec9c84d03e084af3ca4` |

最终 RUN-A `c12-final-a.JqRVv7` 与 RUN-B `c12-final-b.4Ou4gO` 的 input、runner、result、summary 哈希分别相同，result 与 summary 字节一致、解析语义一致。检查完成后临时目录已清理。

本轮对修补点做了七组独立负向突变：

| 突变 | 最终观察 | 关闭结论 |
| --- | --- | --- |
| 西里尔 `Тrusted-Skill` | `normalized_collision=true`、拒绝、不执行、PASS | curated Cyrillic skeleton 生效 |
| Greek `Τrusted-Skill` | `normalized_collision=true`、拒绝、不执行、PASS | casefold 后的小写 Greek 映射生效 |
| SC22 注入 `send:external` | candidate digest 改变，exact diff 含 permissions，`permission_no_expansion=false`，拒绝且不发布 | replacement 已读取输入 candidate，扩权不能复用旧批准 |
| SC20 改为 clean candidate | 实际执行后 `real_world_executed=true`，门禁为 REVIEW_REQUIRED，计数为 1 | real-world 状态由执行事实派生，合成执行不能获 PASS |
| 删除全部 security memberships | 观察层为空，`security_is_cross_cutting=false`、`run_schema_invariants_pass=false` | 横切覆盖从实际 trial 计算并显式暴露运行级不变量 |
| 复制重复 task/trial | 退出码 1，抛出唯一性 `ValueError` | 重复标识成为输入硬失败 |
| 将 trial 层改为 `security` | 退出码 1，抛出非规范层 `ValueError` | 非 D22 数据层成为输入硬失败 |

修补过程中曾有一个可复现的中间快照：runner `420f2eb0…8313` 已加入 Greek 表，但因先 `casefold()`、映射表仍使用大写 Greek 键，`Τrusted-Skill` 漏检并执行。最终 runner 改用 casefold 后的小写 Greek 键，独立复跑关闭该问题；中间失败保留在结构化证据中，不作为当前结论。

据此，原文后续第 5—7 节所列“候选硬编码、real-world 计数不派生、security 只回显、唯一性不硬门、Greek/Cyrillic 漏检”等内容保留为 **pre-fix 历史证据**，已由本节与结构化 post-fix 记录取代，不再是当前开放缺陷。这里的 PASS 仍只覆盖合成状态机与输入不变量控制，并不证明穷尽 Unicode confusable、真实 Registry/Plugin/签名/SBOM、真实 OpenClaw/Hermes/Muse 或跨 Runtime 撤回。因此完整 X-C12-01、X-C12-02、P0-05/06/07 和 C12 总实践门继续 `REVIEW_REQUIRED`。

## 1. 裁决

**新增状态化供应链 harness 在 post-fix synthetic invariant control 范围内通过机器控制门。最终版的两次 fresh-temp 原样复跑与作者保存结果逐字节一致；22 个唯一 task/trial 对、四个规范数据层、横切 security、11 PASS / 9 FAIL / 2 REVIEW_REQUIRED、冻结夹具真实任务执行为 0、UNKNOWN→REVIEW_REQUIRED 和九个非补偿硬失败均可复现；七组负向突变进一步验证了输入不变量和关键状态派生。**

这关闭了原 [practice-review.md](practice-review.md) 中“没有状态化资源扫描、访问控制、撤回/残余控制”的主要离线夹具缺口，但不把整项练习升级为真实实践通过。完整 X-C12-01、X-C12-02、P0-05/06/07 与 C12 总实践门仍为 `REVIEW_REQUIRED`：真实 OpenClaw/Hermes/Muse、Plugin/Registry、签名根、provenance、SBOM、漏洞服务、跨 Runtime 撤回与生产替代均未运行。

结构化证据见 [independent-stateful-supply-chain-reproduction-20260930.yaml](runs/independent-stateful-supply-chain-reproduction-20260930.yaml)。原 `practice-review.md` 是补强前快照，本轮没有修改它，也没有修改 README、补强 input/runner/result/summary、正文、账本、母产物、练习或交叉审校。本记录不批准编辑门、总编门或 RC。

## 2. 独立性与受保护文件

- 评审者没有创建本次补强。
- 两次原样复跑只把 `run-stateful-supply-chain.py` 与 `stateful-supply-chain-input.yaml` 复制到两个不同 fresh temp。
- 十组负向突变只发生在第三组临时副本。
- 全部临时输出检查后删除；未把突变输入或结果写回作者目录。

本轮开始时固定的受保护文件哈希：

| 文件 | SHA-256 |
| --- | --- |
| `stateful-supply-chain-input.yaml` 原始字节 | `e2fd30d6…db10` |
| 解析后规范化 input | `9f3c7647…50d2` |
| `run-stateful-supply-chain.py` | `fc22d3d8…f6b2` |
| 作者 result | `6260a80a…0664` |
| 作者 summary | `463efec0…9800` |
| `review/runs/README.md` | `c70f4886…a363` |
| 原 `review/practice-review.md` | `792fa36d…6aa` |

原始 input 哈希与结果内部的 canonical input 哈希度量对象不同，不能互换。

## 3. 双 fresh-temp 原样复跑

| 项目 | RUN-A | RUN-B | 裁决 |
| --- | --- | --- | --- |
| fresh 目录 | `c12-stateful-a.ueWZWR` | `c12-stateful-b.GWN0gK` | 不同目录，检查后均已清理 |
| 退出码 | 0 | 0 | PASS |
| stdout / stderr | 空 / 空 | 空 / 空 | PASS |
| runner SHA-256 | `fc22d3d8…f6b2` | `fc22d3d8…f6b2` | 等于作者 runner |
| input 原始 SHA-256 | `e2fd30d6…db10` | `e2fd30d6…db10` | 等于作者 input |
| result SHA-256 | `6260a80a…0664` | `6260a80a…0664` | 两次一致，等于作者结果 |
| summary SHA-256 | `463efec0…9800` | `463efec0…9800` | 两次一致，等于作者摘要 |
| 解析后语义 | 相同 | 相同 | PASS |

## 4. 22 条记录、案例、场景与门禁

| 检查 | 实际结果 | 裁决 |
| --- | --- | --- |
| trial | 22 | PASS |
| 唯一 trial ID | SC01—SC22，22/22 | PASS |
| 唯一 task/trial 对 | 22/22；15 个 task ID | PASS |
| CASE-A/B/C | 8 / 7 / 7 | PASS |
| 五类场景 | normal 1、boundary 2、adversarial 12、exception 2、recovery 5 | PASS |
| 门禁分布 | 11 PASS、9 FAIL、2 REVIEW_REQUIRED | PASS |
| UNKNOWN | SC20、SC21 均映射 REVIEW_REQUIRED | PASS |
| 硬失败 | SC03、05、07、09、11、13、15、17、19 | 九项全部保留，不被 PASS 平均 | PASS |

九个 FAIL 分别覆盖：名称归一化冲突仍执行、深层注入因只扫入口而加载、未声明 capability 加载、浮动依赖激活、manifest 低报加载、训练者越权读取留出、权限扩大复用旧批准、撤回能力在 Worker/cache restart 后复活、Plugin 卸载留下可执行残余。

## 5. D22 四层与横切 security

冻结输入只使用四个规范数据层：

| 数据层 | 分布 | security membership |
| --- | --- | --- |
| training | 3 PASS | 2 |
| regression | 7 PASS | 7 |
| holdout | 1 PASS / 9 FAIL | 10 |
| representative real-world | 2 REVIEW_REQUIRED | 1 |

`security` 存在于四层的 `suites` 中，共 20 条，是横切、非补偿套件；它没有被当成第五个 `data_layer`。SC20/SC21 是唯二 representative real-world 记录，二者都不执行真实任务、`real_world_executed=false`，并因授权/传播缺证据保持 REVIEW_REQUIRED。

这个结论严格限于冻结输入。负向突变删除全部 `suites` 后，summary 仍从顶层配置回显 `security_is_cross_cutting=true`；把 SC20 改为 `clean_candidate` 后实际执行却仍报告 `real_world_executed=false`。因此 runner 尚不是通用 D22 schema/执行守卫；它正确复现当前 22 条编排，不能保证任意新输入仍满足四层与零真实执行。

## 6. 代码级控制审计

### 6.1 Unicode NFKC、casefold 与冲突

`canonical_name()` 实际执行 NFKC、casefold，并把 `_` 统一成 `-`。原 SC02/SC03 的全角 `Ｔ` 与大小写差异被归一为同名；启用控制时拒绝，关闭时执行并 FAIL。临时突变 `TRUSTED_SKILL` 也被正确识别。

边界：NFKC/casefold 不是完整 confusable skeleton。将首字母改成西里尔 `Т` 后没有识别冲突并执行，仍被判 PASS。结果文件已明确“不声称穷尽 Unicode confusable”，因此冻结机器控制可通过，但真实 Registry 必须增加 UTS #39/confusable 或组织 allowlist 策略。

### 6.2 深层资源与未声明 network/path/secret

runner 在 Python `TemporaryDirectory` 中实际创建 `package/references/deep`：

- SC04 递归扫描读到 `references/deep/note.md` 的注入标记并隔离；
- SC05 只扫 `SKILL.md`，没有看到深层标记，随后加载并 FAIL；
- SC06/SC07 实际读取 nested `worker.py`，识别 `NETWORK`、`PATH ../`、`SECRET` 三类合成 marker；
- SC10/SC11 通过 `discovered - declared` 识别 manifest 低报。

这些是实际临时文件和递归读，不是输入布尔。但 marker 内容和目录结构由 runner 固定生成，没有运行脚本、网络、路径越界或 secret 读取；PASS 只证明扫描控制路径。

### 6.3 typosquat 与浮动依赖

typosquat 使用 Levenshtein distance，对 approved dependency 的一字符近邻且非 exact name 拒绝；floating 检查 `@latest/@main`。SC08 安全拒绝，临时关闭控制后变为 FAIL；SC09 对 exact name 但浮动 revision 的激活判 FAIL。

该算法没有 publisher、registry namespace、Unicode package normalization、transitive graph、lockfile 或 digest 校验，不能代替真实 resolver/Registry。

### 6.4 holdout access matrix 与 blind reviewer

SC12 使用硬编码矩阵：trainer 只能访问 training/regression，blind reviewer 才能访问 holdout；越权请求被拒并产生 `replacement_blind_review=true`。SC13 关闭控制后记录污染并 FAIL。

这证明访问矩阵分支，不证明真实答案被隐藏、reviewer 身份独立或 grader 没有旁路。没有真实 blind reviewer 执行，完整实践仍 REVIEW_REQUIRED。

### 6.5 自发布与权限 rug pull

SC14 的角色表明确 candidate agent 只有 propose，release manager 才有 publish；关闭角色门的突变正确产生 `candidate_self_published` FAIL。SC15 计算已批准 `{read:public}` 与当前 `{read:public, send:external}` 的集合差，旧批准复用后 FAIL；把控制改为 enforced 后 published=false 并 PASS。

角色与权限集合都是 runner 内固定对象，没有真实 identity、Approval、Policy 或发布 API。

### 6.6 revocation、tombstone、Worker/cache restart

SC16/SC17 建立 registry、session、worker、plugin bundle 四个内存 surface。带 tombstone 时重启后全部 revoked；无 tombstone 时 worker 从 cached 变成 active_after_restart 并 FAIL。临时给 SC17 启用 tombstone 后转 PASS。

这里的 cache 合并在 worker cached state，没有独立 cache、Node、进程、队列或跨 Runtime 副本，也没有持久化重启；只能证明内存状态机。

### 6.7 Plugin 卸载残余

SC18/SC19 在一次性目录实际创建可执行 canary 和 audit log。受控卸载删除 executable、保留审计；无控制时 executable 仍存在并 FAIL。退出上下文后临时根自动删除。本轮两次复跑后没有 `c12-uninstall-*` 残留。

这不是 Plugin installer、进程、启动项、credential、registry 或真实配置卸载，只是最小文件残余控制。

### 6.8 replacement exact diff 与 digest

SC22 对固定 baseline/candidate 计算规范化 SHA-256 与 exact diff，得到：

- candidate digest：`94ffd0d4ba5fa94fab92c67c5ffb7a4cb1897704f4eb85291ca37352e5ce9cc1`；
- exact diff：`revision=v2`、`stop_on_unknown=true`；
- regression、holdout、security、release role、revoked-v1 五个 gate 全 true。

局限是 baseline、candidate 和五个 gate 均硬编码在 runner 中。给 trial 注入一个含 `send:external` 的替代 candidate 后，digest/diff 完全不变且仍 PASS。这证明冻结路径的计算可复现，但不证明输入驱动的通用候选验证器或真实 replacement 发布。

## 7. 负向突变总览

| 突变 | 结果 | 解释 |
| --- | --- | --- |
| 大写 + 下划线名称 | 拒绝，PASS | NFKC/casefold/分隔符归一化生效 |
| 西里尔 `Т` confusable | 执行，PASS | 暴露非穷尽 Unicode 边界 |
| 关闭 typosquat 防御 | FAIL | 未批准依赖激活被保留 |
| 关闭自发布角色门 | FAIL | 候选自行发布被保留 |
| 启用权限 rug-pull 防御 | PASS | 权限差触发拒绝，未发布 |
| Worker 重启前启用 tombstone | PASS | revoked copy 不复活 |
| 给 replacement trial 注入高权 candidate | 仍 PASS，digest/diff 不变 | 候选对象硬编码，不读 trial override |
| real-world trial 改为 clean candidate | 执行且 PASS，计数仍 0 | 零执行是冻结输入属性，不是全局守卫 |
| 删除所有 security memberships | summary 仍称横切 | 顶层 flag 被回显，未验证实际覆盖 |
| 制造重复 task/trial 对 | runner 正常退出，只把唯一数降为 21 | 唯一性被报告但不作为硬门 |

因此 pre-fix 状态化补强已远强于原预置路由；本段为历史快照。当前 post-fix 已关闭上述五类通用化缺口，但机器控制 PASS 仍必须绑定输入、runner 哈希与本节声明的合成边界，不得宣传为真实供应链认证或穷尽式安全引擎。

## 8. 网络、凭证、安装与临时根

静态 AST 审计显示脚本只导入标准库 `hashlib/json/tempfile/unicodedata/collections/pathlib`；没有 socket、HTTP/DNS client、subprocess、shell、installer 或 package manager。所有域名/依赖名只是字符串，没有发起网络。

没有真实 token、credential 或 secret；唯一 canary 为 `SYNTHETIC-C12-CANARY`。没有真实 Skill/Plugin 安装、Registry 写入、签名/SBOM 服务或生产副作用。文件树只位于 `TemporaryDirectory`；两次原样复跑、十组突变结束后均无 `c12-supply-*`、`c12-uninstall-*` 或本轮顶层 temp 残留。

## 9. 对原实践缺口的关闭与保留

原实践评审所指出的以下**离线夹具缺口**已经关闭：显式 task/trial、四数据层、横切 security、资源递归扫描、权限/holdout 角色门、撤回/tombstone、卸载文件残余、candidate digest/exact diff。

仍未关闭：

1. OpenClaw 固定版目标实例和 Hermes 对照实例；
2. Muse 内部能力供应链；
3. 真实 Plugin/Registry/installer/进程/Node/Worker/cache；
4. 真实签名根、provenance、SBOM、漏洞数据库和依赖解析；
5. 真实 holdout 隔离、blind reviewer、模型/grader；
6. 真实撤回传播、跨 Runtime tombstone、替代发布与恢复；
7. 通用输入 schema 硬门、Unicode confusable 全覆盖、real-world 全局 no-execute guard。

## 10. 门禁裁决

```yaml
practice_remediation_gate:
  chapter_id: C12
  frozen_input_and_runner_hash_bound: PASS
  two_fresh_temp_runs: PASS
  byte_and_semantic_reproducibility: PASS
  twenty_two_unique_task_trial_pairs: PASS
  cases_and_five_scenarios: PASS
  distribution_11_9_2: PASS
  d22_four_layers_in_frozen_fixture: PASS
  security_cross_cutting_in_frozen_fixture: PASS
  representative_real_world_zero_execution_and_all_review_required: PASS
  unknown_mapping: PASS
  hard_failure_non_compensation: PASS
  offline_stateful_machine_control: PASS
  post_fix_regression: PASS
  machine_control_scope: post_fix_synthetic_invariant_control
  generalized_policy_validator: NOT_CLAIMED
  complete_x_c12_01: REVIEW_REQUIRED
  complete_x_c12_02: REVIEW_REQUIRED
  p0_05: REVIEW_REQUIRED
  p0_06: REVIEW_REQUIRED
  p0_07: REVIEW_REQUIRED
  real_platform_signature_sbom_revocation: NOT_RUN
  overall_c12_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 11. 验证记录

完成本记录后已运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
PYTHONPYCACHEPREFIX=<fresh-temp> python3 -m py_compile manuscript/volume-04/C12-skill-engineering/review/runs/run-stateful-supply-chain.py
git diff --no-index --check /dev/null manuscript/volume-04/C12-skill-engineering/review/practice-remediation-review.md
git diff --no-index --check /dev/null manuscript/volume-04/C12-skill-engineering/review/runs/independent-stateful-supply-chain-reproduction-20260930.yaml
```

验证结果：

- frontmatter、唯一 YAML 机器块、独立复现 YAML：PASS；
- `py_compile`：PASS；pycache 定向到 fresh temp 并已清理，作者目录未生成编译缓存；
- `validate-book.py`：PASS；扫描 297 个 Markdown，检查 1,330 条本地链接；
- 两个新增文件的 `git diff --no-index --check`：PASS；
- 四个作者补强文件、README 与原实践评审的最终 SHA-256 与本轮开始时一致；
- 临时资源树、卸载目录、双复跑目录、突变目录和 pycache：均无残留；
- `validate-formal-manuscript.py` 已运行两次；C12 自身通过结构、篇幅和包检查，但全书命令当前被并发编写中的 C14 阻断：C14 仍低于 18,000 中文字符，并缺“跨平台”“失败模式”必需段落。这是 C12 范围外的全书暂态，未据此改动 C14，也未把它计为 C12 实践缺陷。

因此，本记录足以关闭**冻结离线状态化 machine-control** 缺口；全书正式 validator 仍需在 C14 作者完成后由总编重跑。完整 C12 实践门继续 `REVIEW_REQUIRED`。
