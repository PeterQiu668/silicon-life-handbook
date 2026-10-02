# C04 实践运行结构化校验报告

> 校验时间：2026-09-30T15:39:19+08:00  
> 校验对象：`c04-synthetic-input-pack.yaml`、`c04-role-swap-run-set.yaml`  
> 方法：Ruby YAML 解析后执行预注册的覆盖、完整性、门禁和外部状态断言。

## 1. 岗位互换运行集

```json
{
  "total_runs": true,
  "unique_ids": true,
  "role_coverage": true,
  "two_core_each": true,
  "migration_failure_present": true,
  "prohibited_blocked": true,
  "no_external_change": true,
  "failures_preserved": true,
  "review_state_present": true,
  "recoveries_present": true
}
```

断言含义：运行总数为 22 且 ID 唯一；每个岗位覆盖 core/variant/boundary/risk/recovery/handoff，且至少两个核心任务；误迁移失败被保留；所有禁止尝试都有 `denied-*` 控制裁决；没有真实外部状态变化；失败、复核态和三个岗位的恢复记录均存在。

## 2. 输入包

```json
{
  "frozen": true,
  "synthetic": true,
  "external_denied": true,
  "five_samples": true,
  "swap_roles": true
}
```

断言含义：输入已冻结并标记为匿名合成；外部状态和生产变更被禁用；成功、失败、拒绝、人工接管、边界争议五类样本齐全；存在两个互换对照岗位。

## 3. 解释边界

机器校验只能证明结构化材料满足所列断言，不能证明记录对应真实 Runtime 或生产行为。本报告必须与人工检查、失败报告和零外部状态声明一起读取；不得据此批准真实上线或认证。

## 4. 包内与全书只读回归

- 两个运行 YAML：解析通过；
- `review/` 下 Markdown frontmatter 和 fenced YAML：解析通过；
- 实践与并发评审共 13 个文件：检查 15 个本地链接，缺失 0；
- `validate-formal-manuscript.py`：通过，当前快照 C04 为 16,492 CJK；唯一警告为全书尚缺 20 个章节包；
- `validate-book.py`：通过，扫描 151 个 Markdown、1,008 个本地链接；
- 校验发生在并发证据/交叉审校文件已经出现之后。结果只代表 2026-09-30T15:39+08:00 附近的当前共享工作区快照；后续并发修改需要重跑。
