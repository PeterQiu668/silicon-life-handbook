# C07 作者合成基线运行包

本目录保存第 7 章作者为验证数据合同而执行的离线合成基线。它不是 OpenClaw、Hermes 或 Muse 产品基准，也不是独立实践门签核。

运行命令：

```bash
python3 run-synthetic-baseline.py
```

输入为 `synthetic-input.yaml`。该文件使用 JSON 语法，因此同时是合法 YAML，脚本只依赖 Python 标准库。输出为 `synthetic-baseline-results.yaml` 和 `synthetic-baseline-summary.md`；重复运行时，除 `generated_at` 固定为测试合同日期外，字节级结果应保持一致。

运行边界：无网络、无凭证、无外部工具调用、无真实用户数据、无生产写入。`model`、`human`、`expert` grader 都是预先标记的合成夹具，仅用于验证校准表与争议路由，不能解释为真实裁判已完成校准。

## X-C07-02 合成裁判红队

`run-grader-calibration.py` 是在首次独立实践评审指出缺口后新增的机器可执行练习包。它覆盖八个预注册变体：顺序反转、等义长短、身份可见/盲化、裁判提示注入、正确答案/错误轨迹、错误 gold、缺证和 grader/rubric 版本漂移。

为避免覆盖保存证据，独立复跑应指定新输出目录：

```bash
python3 run-grader-calibration.py --output-dir /path/to/fresh-output
```

默认输出为 `grader-calibration-results.yaml` 和 `grader-calibration-summary.md`。输入使用 JSON 语法，因此同时是合法 YAML；脚本只依赖 Python 标准库，并对 Schema、八类覆盖和唯一 ID 做 fail-fast 检查。

这个运行包只验证机器控制能否识别预先植入的偏差并安全路由。它没有调用真实 model grader，也没有真实 human/expert 参加；因此机器控制门可以 PASS，X-C07-02 完整门仍必须保持 `REVIEW_REQUIRED`。后续独立复跑者不得把合成标签写成真实校准成绩。
