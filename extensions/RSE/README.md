# Extension:RSE(占位)

**状态**:**未落地**(placeholder)

## 预期范围

RSE(Radiated Spurious Emission,辐射杂散发射)测试大类。射频接口人手册中 RSE 是与 EMC 并列的独立测试方向。

## 与 core 的关系

RSE 与 Desense 互为镜像(Desense 管"接收机被干扰",RSE 管"设备向外辐射超标"),共享部分方法论(三要素模型的"干扰源"和"耦合路径"概念)。未来落地时应:

- 复用 core 的 `/diagnose` 流程框架
- 独立建立 RSE 限值标准和测试矩阵
- 沉淀 RSE 特有的 SOP

## 不填充的理由(2026-04-27)

当前 RSE 知识未成熟,团队也未明确启动此扩展。保留目录作为**架构扩展点标记**,避免未来再次讨论"RSE 放哪里"。
