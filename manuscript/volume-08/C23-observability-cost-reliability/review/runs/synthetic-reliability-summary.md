# C20 v2.1 合成可靠性运行摘要

- 输入：24个完整raw-state；training 4、regression 4、holdout 16、representative real-world 0；security/red-team横切7。
- 裁决：4 PASS、16 FAIL、4 REVIEW_REQUIRED；24/24冻结oracle匹配。
- 动态计数：外部副作用0；representative real-world证据0。
- 决策digest：`6af7d47b0874a7de639a4e7d085b023decbfe787d12da12d7a15d5e03fcf8bbf`。
- 负向回归：46/46通过；case名与expected不参与裁决。
- 范围：作者侧离线synthetic invariant control；非作者实践复核及真实Runtime验证仍为REVIEW_REQUIRED。
