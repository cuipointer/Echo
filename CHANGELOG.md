# Changelog

Echo·Desense 知识库与 harness 层的版本变更记录。

格式:参考 [Keep a Changelog](https://keepachangelog.com/)。日期 YYYY-MM-DD。

---

## [2.1.0] — 2026-05-06

### 本版本里程碑

Phase 2 Sprint 1 交付完成。10 天 Sprint 压缩为约 5 天(并行执行方式 A+B)。

### Added

**EMC 2024 案例反哺落地**:
- 新增 `knowledge/methodology/bandwidth-discrimination.md` v1.0(宽窄带判别独立方法论)
- 新增 `knowledge/cases/O11-DDR-LLB-aperture.md`(从 EMC C.1 拆出的独立案例)
- 新增 `knowledge/cases/O2-NFC-W24.md`(从 EMC B.2 拆出的独立案例)
- matrix.yaml v2.1.0:新增 source `NFC`(category: 共存)+ mapping `NFC → W24 = W24-08` 和 `SHIELD_LEAK → W24 = W24-09`
- source_codes 增加 `NF`;自动生成 W24-08 / W24-09 placeholder
- SOP 模板新增**步骤 2.6 多源叠加排查法**(从 W24-02 v2.1 的 2.5 延伸)

**P0 SOP 填充(v0.9 方法论版)**:
- `knowledge/sops/LLB/LLB-07.md` — Charger → LTE LB(参照 LLB-04 + EMC A.3/C.1)
- `knowledge/sops/W24/W24-03.md` — DDR → WiFi 2.4G(参照 W24-01 + EMC C.1/C.2)
- `knowledge/sops/LHB/LHB-04.md` — USB 3.0 → LTE HB(参照 W5-04 + EMC O81)
- 状态标记 `v0.9.0 方法论版(待现场复测)`,等待首次项目落地后升 v1.0

**计划文档**:
- `docs/architecture/phase2-sprint-plan.md` Sprint 1 计划 + 第九章并行执行方案(DAG/3 种并行方式/时间压缩)

### Changed

- `.claude/commands/diagnose.md` v2.0 → v2.1:Step 3 宽窄带判别引用独立方法论文档 + 自动判据速查表 + 反例提醒

### Infrastructure

- Week 1 所有变更集中在 `feature/echo-framework-feedback` 分支,分 3 个 commit 对应 T1.2/T1.3/T1.5
- Week 2 每个 SOP 独立分支(`sop/llb-07` / `sop/w24-03` / `sop/lhb-04`),按 git-workflow 规范合入
- develop 同步回 main 前完成加速 self-review(linter 0/0 + diff 扫描)

### 指标达成

| 指标 | v2.0.0 | v2.1.0 | 目标 |
|---|:---:|:---:|:---:|
| Formal SOP 数 | 13 | **16** | 16 ✓ |
| 案例库 | 2 | **4** | 4 ✓ |
| matrix.yaml sources | 15 | **16** | 16+ ✓ |
| matrix.yaml mappings | 47 | **49** | 49+ ✓ |
| 方法论文档 | 4 | **5** | 5 ✓ |
| `/diagnose` 版本 | v2.0 | **v2.1** | v2.1 ✓ |
| linter 状态 | 0/0 | **0/0** | 0/0 ✓ |

---

## [2.0.0] — 2026-04-27

### Added

**架构结构化(Sprint 2b)**:
- 新增 `knowledge/matrix/matrix.yaml` 作为干扰源 × 受扰体 × SOP 映射的**单一真相源**
- 新增 `tools/gen_matrix_views.py` 从 matrix.yaml 生成 `matrix-table.md` / `source-list.md` / `victim-list.md`

**补齐悬空 SOP(Sprint 3)**:
- 新增 `tools/gen_sop_stubs.py` 为矩阵声明但未落盘的 SOP 生成 placeholder
- 为 26 个悬空 SOP 生成占位文件(状态 `待编写`),涵盖 NORMAL-04~08 / W24-03~07 / W5-01/03 / LLB-01/03/05/06/07 / LHB-01/03/04 / GL1-03/04/06/07 / GL5-01/03/04

**规范沉淀(Sprint 4)**:
- 新增 `knowledge/glossary.md` 术语单一来源
- 新增本 `CHANGELOG.md` 知识库级变更记录

### Changed

**Harness 层折叠(Sprint 1)**:
- `/diagnose` 命令升级到 v2.0,成为 Desense 诊断工作流的**单一真相源**
- 新增 Step 3 宽窄带判别(架构级筛选)、假设优先级排序表、零成本验证路径表
- `diagnose-desense` skill 降级为触发器,不再重复工作流定义
- `echo` agent 保留方法论和人格,移除 5 步流程

**Linter 扩展(Sprint 2a)**:
- `tools/check-architecture-consistency.py` v2:
  - 新增 matrix.yaml ↔ SOP 文件存在性校验
  - 新增跨文件引用完整性校验
  - 新增 source-list/victim-list 自动生成标记检查
  - 新增 harness 层完整性和 frontmatter 校验
  - 新增 normal 域 README 检查(原只查 camera/display)
  - 自适应 SOP 行数阈值(stub / 正式 SOP 不同)

### Fixed

- 修正 `knowledge/domain/normal/README.md` 指向 `tools/` 和 `docs/` 的相对路径错误(../../ → ../../../)
- 修正 `.claude/commands/matrix.md` 对 `knowledge/matrix/` 的路径
- 重建 `knowledge/sops/NORMAL/SOP-NORMAL-04.md`(原 42 行残次版,重建为 8 章节完整 stub)

### Infrastructure

- 修复 `.gitignore`:移除 `logs/` 整目录忽略(与 engineering-logger skill 契约矛盾),仅保留 `*.log` 忽略
- 从 OpenCode 环境完整迁移到 Claude Code 环境:`.opencode/` → `.claude/`,`AGENTS.md` → `CLAUDE.md`,全 harness 适配

---

## [1.1.0] — 2026-04-22(Echo 版历史)

### Added
- 矩阵表新增 Normal 场景列
- NORMAL SOP 系列(NORMAL-01~04)
- `knowledge/methodology/scene-priority.md` 场景优先级规则
- `knowledge/domain/normal/` Normal 领域知识

### Changed
- 决策树新增 Normal 优先检查分支
- `echo` agent 加入 Normal 优先原则

---

## [1.0.0] — 2026-04-21(Echo 版历史)

### Added
- 项目初始化
- 三要素模型框架
- 宏观决策树(`knowledge/decision-tree.md`)
- 核心矩阵表 v1.0(`knowledge/matrix/matrix-table.md`)
- P0 高频 SOP:GL1-01 / GL1-02 / GL1-05 / W24-01 / W24-02 / W5-02 / W5-04 / LLB-02 / LLB-04 / LHB-02 / GL5-02
- 谐波计算工具 `tools/harmonic_calc.py`
- 链路预算工具 `tools/link_budget.py`
- 日志工具 `tools/logger.py`
- 架构一致性检查 `tools/check-architecture-consistency.py` v1

### Changed
- 基于 OpenCode 架构的初始能力模块布局
- AGENTS.md 定义 Echo agent 行为规范

---

## 版本约定

- **主版本号(Major)**:架构层面变更,可能影响 harness 层或知识层的组织方式(如 2.0.0 引入 matrix.yaml 重构)
- **次版本号(Minor)**:新增知识内容(SOP / 案例 / 方法论新章节)
- **补丁版本号(Patch)**:修正 / 小幅澄清 / broken link 修复

各单独 SOP 和方法论文档维护自己的 `**版本**` 字段;本 CHANGELOG 汇总知识库层面的变化。
