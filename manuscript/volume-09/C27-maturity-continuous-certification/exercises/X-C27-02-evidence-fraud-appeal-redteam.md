# X-C27-02 证据伪造、裁判偏差与申诉红队

## 注入

运行builder保存的60个完整raw-state trial：覆盖授权主体、签发/事件时钟、digest与对象错绑，canonical alias自审、change owner自批、同人申诉，manifest/artifact/signature/holdout/grader/失败档案/cost造假，MAT前置与七维硬门，组织roster，多证书冲突，共同有效窗口、公开声明、生命周期、合法续证、重大变化后三层谱系、真实层/真实证书/外部effect以及hard+UNKNOWN。再运行25项基础回归、保留的历史与独立套件、当前46项组合攻击和20项续证/再认证近邻回归；重点核对因果偏序、root撤销shadow、D22逐层安全、result来源摘要不可互换，以及合法正控确实可达而不是“全拒绝”。

## 执行与验收

双fresh-temp从builder构建authority与input并运行，比较authority/input/result、root与decision digest、完整分布和生命周期；确认正式输入只有完整raw state且不存在case、expected或mutation字段。每项原semantic escape必须同时命中规定业务reason，篡改状态还必须由black-box冻结根拒绝。decision digest覆盖聚合、逐trial身份、layer和成功计数；独立semantic/measurement registry及source replay必须拒绝把FAIL、生命周期、reason、分布与digest一起重写的结果。input、authority和result的顶层及嵌套重复JSON键必须在解析前拒绝。离线real-world、real-certificate与已观察external effect动态计数并FAIL，validated success保持零。合法缩短expiry、合法续证与完整重大变化后三层再认证必须PASS，以证明不是全拒绝。真实平台、生产、外部认证效果保持RR。
