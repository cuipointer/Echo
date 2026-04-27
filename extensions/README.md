# Extensions — 领域扩展点

**版本**:v1.0.0
**日期**:2026-04-27

本目录是 Echo·Desense 架构的**领域扩展点**。Echo 的核心(`knowledge/`)聚焦射频 Desense 问题;当要复用 Echo 的方法论 + harness 层框架到其他领域(EMC / SAR / OTA / 短距等)时,扩展进驻本目录。

## 已注册扩展

| 扩展 | 目的 | 状态 |
|---|---|:---:|
| [Camera/](Camera/) | Camera 横向领域知识(跨 Desense / EMC / SAR) | 占位(**尚未落地**) |
| [RSE/](RSE/) | RSE(Radiated Spurious Emission)独立领域 | 占位(**尚未落地**) |

## 扩展结构约定

每个扩展应遵循与 core `knowledge/` 相似的分层:

```
extensions/<NAME>/
├── README.md           ← 扩展介绍 + 范围 + 与 core 的关系
├── methodology/        ← 扩展特有的方法论(可引用 core methodology)
├── domain/             ← 扩展特有的领域知识
├── matrix/             ← 扩展的矩阵(如适用,YAML + 生成器)
├── sops/               ← 扩展的 SOP 库
└── cases/              ← 扩展的案例库
```

Harness 层(`.claude/{agents,commands,skills}/`)由 core 统一提供,扩展可:
- 在自己的 README / methodology 中声明何时触发
- 贡献额外的 skill(放到 `.claude/skills/<extension>-*/`)
- 扩展不应重新定义 `/diagnose` 流程——而是通过 methodology + matrix 数据让 `/diagnose` 能覆盖到

## 现状(2026-04-27)

**Camera/ 和 RSE/ 目前都是空目录,作为占位不做内容填充**。原因:

1. Camera 知识已经在 [knowledge/domain/camera/](../knowledge/domain/camera/) 中,Camera/ 扩展本身缺乏清晰的"与 core 区分"的边界。未来若发展出跨 Desense/EMC/SAR 的 Camera 通用策略,再迁移进来。
2. RSE 是独立测试大类(同团队射频接口人职责之一,见飞书接口人手册),但目前没有落地 SOP 或方法论内容。

**下一步**(视需求决定):
- **路线 A(收敛)**:若半年内没有 EMC/RSE/SAR 场景需要扩展,**删除** `extensions/`(避免架构空壳)
- **路线 B(扩展)**:当团队决定把 RSE 知识纳入 Echo 复用框架时,在本目录下落地第一个完整扩展

## 参考

- [CLAUDE.md](../CLAUDE.md) — 项目级指南
- [knowledge/methodology/](../knowledge/methodology/) — 核心方法论
- [CHANGELOG.md](../CHANGELOG.md) — 架构变更记录
