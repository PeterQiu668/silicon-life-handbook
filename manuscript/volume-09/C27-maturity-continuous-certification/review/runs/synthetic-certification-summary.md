# C24 离线认证状态机摘要

- trials: `60`
- distribution: `{'FAIL': 52, 'PASS': 6, 'REVIEW_REQUIRED': 2}`
- lifecycle: `{'ACTIVE': 3, 'EXPIRED': 1, 'LIMITED': 2, 'REVOKED': 52, 'SUSPENDED': 2}`
- representative real-world attempts: `1`
- real certificate attempts: `1`
- external effect attempts: `1`
- observed external effects: `1`
- validated successful real certificates: `0`
- validated successful external effects: `0`
- input semantic digest: `sha256:a68baf11441ff9738cb616744e855daf9ce32cba2dd133d8c7f5100f3ff64e0a`
- authority semantic digest: `sha256:6da041cac0ab70d39769636811be9656130b8373788b898fa2a861e3c024ccac`
- authority root digest: `sha256:1c768968e30d39195369e517394c3c218829b175d64d219a6e5ff159062fb6ad`
- decision digest: `sha256:4645332ab3e0e1aa16ac5a435a3105a422c17eeefea3e0f8ef1a84a53e27e5f4`

`attempted_*`、`observed_*`与`successful_*`严格分离；冻结主体图、事件DAG与authority canonical projection共同绑定，任何可信verify入口均强制source+root语义重放。
