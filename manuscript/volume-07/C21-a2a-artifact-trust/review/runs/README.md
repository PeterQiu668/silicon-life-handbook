# C18 状态化离线夹具

夹具仅使用合成 key material、`.invalid` 端点和内存对象，不访问网络、不含真实凭证、不产生外部副作用。输入给出原始 Card 模板、缓存、事件序列、Task 快照、effect、Artifact、digest/signature字段、authority store 与 trust evidence；runner 先物化原始对象，再从字节、字段、顺序和证据推导三态，不读取预裁决布尔值。`build-synthetic-a2a-input.py` 是冻结输入的唯一生成器；先重建输入，再运行裁判。

```bash
PYTHONPYCACHEPREFIX=/tmp/c18-pycache python3 build-synthetic-a2a-input.py
PYTHONPYCACHEPREFIX=/tmp/c18-pycache python3 run-a2a-harness.py --input synthetic-a2a-input.yaml --output synthetic-a2a-results.yaml
```

D22 四层显式记录，`representative_real_world=0`；`security_red_team` 是横切属性。v3.1 离线 harness 不接受同一输入内自签的 representative-real-world manifest，真实层一律移交外部独立证据门。冻结 v3.1 为18 trial、`3 PASS / 9 FAIL / 6 REVIEW_REQUIRED`、decision digest `8d671fbdfaad6fc523e404a268d59bf4b151c6b26aa321238241fc5f50d71ca4`；三条 synthetic shadow、零外部副作用。这些数值只证明离线合成机器控制，不批准两项真实实践练习。

冻结文件 SHA-256：builder `f2ee5d44f17bf2508038f1e92603a46eaa0f90cc50b24416e62495aa2203b020`；runner `8501dcb9d485e2064e7b41b9f49217280c2f2b3634498140a2a28633e00213a5`；input `d61672da179f0668e302a4fa11ab4c15190f3be3a212d454bd8052bbad9410b1`；result `51b1919ef32bac3356be069ace559afb79ee752b03b4aceb07f5a8c2fc6ebd2e`；summary `49f98783673681224d1fc9eebc7d650f6317f99bdc487001380afffe2aa437f9`。
