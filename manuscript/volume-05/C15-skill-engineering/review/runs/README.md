# C12 作者离线 Skill 供应链实验

本目录保存 C12 作者用于验证候选审计、影子测试、恶意版本隔离、撤回传播和替代发布合同的确定性实验。

运行：

~~~bash
python3 run-skill-supply-chain.py
~~~

输入 synthetic-skill-input.yaml 使用 JSON 语法，因此也是合法 YAML。脚本只使用 Python 标准库；没有网络、真实凭证、真实 Plugin 安装、生产 Gateway、外发或不可逆删除。所有 Skill、Plugin、签名、SBOM、session、Node、Worker 和结果均为合成夹具。

PASS 只证明 fixture 按合同路由，不构成 Agent Skills、OpenClaw、Hermes、Muse、SLSA、Sigstore 或 SBOM 认证。未知传播范围映射 REVIEW_REQUIRED；恶意资源生效、权限扩大、依赖漂移、自发布和撤回失败为硬 FAIL。

## 独立状态化补强

作者基线经独立实践审校后，另增以下机器控制：

~~~bash
python3 run-stateful-supply-chain.py
~~~

`stateful-supply-chain-input.yaml` 与 `run-stateful-supply-chain.py` 不替换作者基线，也不自批实践门。它们在无网络、无真实 Plugin/Registry/凭证的前提下，实际创建一次性文件树和生命周期状态，检查 Unicode 归一化名称冲突、深层资源扫描、未声明 network/path/secret、typosquatting/浮动依赖、manifest 低报、holdout 访问隔离、自发布、权限暗增、旧 Worker/cache 复活、卸载可执行残余和替代发布链。

每条记录带显式 `task_id/trial_id`，并使用 D22 的四个规范数据层；`security` 只作为横切非补偿套件。`representative_real_world` 两条记录明确不执行真实任务并保持 REVIEW_REQUIRED。该控制的 PASS 只适用于固定离线合成路径，必须再由非作者在 fresh temp 中独立复跑；它不能证明真实签名、SBOM、平台隔离、跨 Runtime 撤回或供应链安全。
