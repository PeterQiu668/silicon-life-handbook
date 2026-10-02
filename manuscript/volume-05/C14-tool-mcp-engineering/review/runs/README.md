# C11 作者合成工具合同与故障实验

本目录保存 C11 作者侧确定性离线实验。全部账户、token、域名、文件、邮件、工具、MCP Server、批准与环境终态均为合成对象；没有网络、真实凭证、真实外发、资金、生产系统或不可逆删除。

运行：

~~~bash
python3 run-tool-contract.py
~~~

输入 synthetic-tool-input.yaml 使用 JSON 语法，因此同时是合法 YAML。脚本只使用 Python 标准库，输出 synthetic-tool-results.yaml 与 synthetic-tool-summary.md。

实验验证的是工具合同与门禁路由，不是 OpenClaw、Hermes、Muse 或真实 MCP Server 的产品基准。协议原始状态 UNKNOWN 最终只能映射 REVIEW_REQUIRED；确认的越权、SSRF、token passthrough、重复副作用、错误终态或秘密暴露必须 FAIL。

## 独立状态化红队补强

`run-stateful-mcp-redteam.py` 与 `stateful-mcp-redteam-input.yaml` 是作者基线经独立实践审校发现覆盖缺口后新增的补强控制。运行：

~~~bash
python3 run-stateful-mcp-redteam.py
~~~

该控制不读取作者基线的预置 `ssrf_target`、`token_passthrough`、`effect` 或 `readback` 结论，而是在离线合成 Host/Client/Server 中实际完成以下观察：

- 解析限定名与同名工具冲突；
- 比较批准前后 schema、description、binary 与 scope 快照；
- 逐跳解析 URI，阻断非 HTTPS、loopback、private、link-local、reserved 等地址类；
- 检查 audience，并观察入站 token 是否被转发；
- 在一次性临时根中解析路径并读取合成 canary；
- 启动受控子进程，观察合成环境 canary 是否越界；
- 对工具结果注入、read-only 谎报、旧 Session 撤回与清理 UNKNOWN 保留独立状态。

所有 URI 均只做本地解析，不发出网络请求；token、文件内容与环境变量均为合成 canary。该补强连续运行输出应保持字节稳定，但仍不构成真实 MCP/OAuth、平台沙箱或产品安全认证。它必须由另一位非作者审校者在 fresh temp 中独立复跑后，才能改变实践门裁决。
