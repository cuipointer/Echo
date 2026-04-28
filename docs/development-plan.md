# Echo·Desense 开发计划

**版本**:v1.0.0
**创建日期**:2026-04-28
**项目状态**:活跃开发中

---

## 愿景

把"射频 Desense 排查"从依赖个人经验的**零散 Debug 行为**,演进为可积累、可复用、可自动化检验的**标准化专家系统**。

核心主张:

1. **知识结构化**:方法论 + 矩阵 + SOP + 案例分层,每层都有单一真相源
2. **流程可执行**:Claude Code harness(agents / commands / skills)把知识变成可调用工作流
3. **闭环沉淀**:每个现场案例反哺 SOP 和矩阵,SOP 改进推动架构迭代
4. **自动守护**:linter + 生成器避免知识漂移

---

## 路线图

### Phase 1 — 基础建设(2026-04,已完成)

**目标**:从 OpenCode 迁移到 Claude Code,建立单一真相源架构

| 里程碑 | 状态 | 交付件 |
|---|:---:|---|
| OpenCode → Claude Code 迁移 | ✅ | `.claude/{agents,commands,skills}/`、`CLAUDE.md` |
| harness 层折叠 | ✅ | `/diagnose` v2.0 单一真相源 + skill 触发器 + agent 人格 |
| 矩阵结构化 | ✅ | `matrix.yaml` + `gen_matrix_views.py` 生成器 |
| SOP 覆盖补齐 | ✅ | `gen_sop_stubs.py` + 26 个 placeholder |
| 架构一致性检查 v2 | ✅ | `check-architecture-consistency.py` 9 项检查,0 错 0 警 |
| 术语与变更记录 | ✅ | `glossary.md` + `CHANGELOG.md` |

详见 [CHANGELOG.md](../CHANGELOG.md) v2.0.0。

---

### Phase 2 — 内容填充(2026-05)

**目标**:把 27 个 stub SOP 填充为可执行的内容,建立案例库

| 里程碑 | 优先级 | 预期工时 | 依赖 |
|---|:---:|:---:|---|
| **P0 高频 SOP 填充**(LLB-07 充电器→LTE LB, W24-03 DDR→WiFi 2.4G, LHB-04 USB3→LTE HB) | P0 | 6 人天 | 需现场实测数据 |
| P1 中频 SOP 填充(NORMAL-05~08 RF 类、W24-04~07 等) | P1 | 10 人天 | 现场 + 方法论提炼 |
| 案例库扩充(每月至少 2 个闭环案例沉淀) | P1 | 持续 | 实际排查工作 |
| 历史案例回溯(从 logs/ 反查未沉淀的经验) | P2 | 3 人天 | 逐日日志 |

**成功标准**:27 个 stub 中至少 15 个转为"已完成"状态(含 3 个 P0),案例库达到 ≥ 8 个。

---

### Phase 3 — 自动化(2026-06)

**目标**:把手工动作自动化,让知识沉淀不依赖人工勤奋

| 任务 | 设计 | 收益 |
|---|---|---|
| **架构 linter 接入 hook** | `.claude/settings.json` PostToolUse hook,改 .md 后自动触发 | 阻止提交级漂移 |
| **case → SOP 自动化沉淀 skill** | 新 skill:检测到 `knowledge/cases/` 新文件 → 解析"教训"段 → 匹配 matrix → 提议 SOP 版本更新 diff | AS2→W24-02 那类闭环标准化 |
| **矩阵覆盖度报告** | `tools/matrix_coverage.py`:生成"每个(源,体)组合的 SOP 完成度 + 案例数量"报告 | 暴露知识盲点 |
| **决策树 ↔ 矩阵一致性校验** | linter 扩展:决策树到达的每个"干扰源类别"必须在 matrix.yaml 中可达 | 避免引导到空路径 |
| **周报/月报自动聚合** | 扫描 `logs/daily/*.md` → 聚合到 `logs/weekly/YYYY-Www.md` | 报告工作量降低 |

**成功标准**:新加一个现场案例从提交到 SOP 更新草案生成,纯自动化 ≤ 5 分钟。

---

### Phase 4 — 横向扩展(2026-Q3~Q4)

**目标**:把 Echo 框架复用到其他测试大类(按需启动,决策点见下)

决策点:当射频接口人手册中的其他方向(EMC / RSE / OTA / SAR)有明确推广意愿时启动。

候选扩展:

| 扩展 | 目录 | 预期方法论差异 | 启动条件 |
|---|---|---|---|
| **RSE**(辐射杂散发射) | `extensions/RSE/` | 输出方向(设备→外部)而非接收方向,限值标准不同 | 团队决策启动 |
| **EMC**(电磁兼容) | `extensions/EMC/`(暂无) | 侧重抗扰度 + 发射 | 团队决策启动 |
| **Camera 横向** | `extensions/Camera/` | 跨 Desense/EMC/SAR 的 Camera 通用策略 | 出现跨大类 Camera 问题时 |

**不扩展的默认姿态**:半年内无启动 → `extensions/` 收敛删除,避免架构空壳。详见 [extensions/README.md](../extensions/README.md)。

---

### Phase 5 — 工具链成熟(2026-Q4~2027-Q1)

**目标**:把知识库变成团队级平台

候选特性(按团队需求排序):

- **Web UI**:矩阵表 / SOP 库的在线查询界面(而非 Markdown 浏览)
- **测量工具集成**:把仪表数据接入 `playground/`,自动填充 SOP 检查表字段
- **跨项目对比**:多机型 Desense 数据库,"A 机型 SOP-X 改善 5dB,B 机型改善 2dB,差异归因"
- **知识图谱**:把 sources / victims / 案例 / SOP 映射为图数据库,支持反向查询(如"GL1-01 被哪些案例引用")

---

## 技术决策记录 (ADR)

### ADR-1:单一真相源架构

- **决定**:每层知识设立一个源文件,其他视图均从它生成或引用
- **体现**:`matrix.yaml`(映射源)、`glossary.md`(术语源)、`/diagnose`(工作流源)、`decision-tree.md`(决策源)
- **理由**:消除多份 Markdown 之间漂移的根因。一致性交给 linter 和生成器,不依赖人工记忆。
- **代价**:修改需要经过"改源 → 跑生成器 → commit 二者"的流程,比直接改视图多一步

### ADR-2:Placeholder 优于悬空

- **决定**:矩阵声明但未实施的 SOP 全部生成 `v0.1.0 待编写` 的 placeholder
- **理由**:悬空引用会让用户走到空路径,placeholder 至少能引导到"本 SOP 尚未实施"的明确信息
- **代价**:目录看起来"完成度"高但实际很多是 stub——状态字段必须清晰

### ADR-3:Harness 层职责单一

- **决定**:`/diagnose` 命令 = 工作流,skill = 触发器,agent = 人格;三者不重叠
- **理由**:避免三处同时定义同一流程导致漂移
- **代价**:修改诊断流程必须改 `/diagnose` 一个文件,触发和人格配合

### ADR-4:案例优先反哺 SOP

- **决定**:现场案例沉淀到 `knowledge/cases/` 后,必须评估是否更新对应 SOP
- **体现**:AS2-RC-WiFi24 案例 → W24-02 v2.0 → v2.1(新增步骤 2.5)
- **理由**:SOP 的价值在于固化经验,案例是 SOP 演进的原材料

---

## 贡献指南摘要

详见 [docs/contributing.md](contributing.md)。要点:

- **新 SOP**:先改 `matrix.yaml`(声明) → `gen_sop_stubs.py`(生成 stub) → 填充内容 → 状态改为已完成
- **新案例**:写到 `knowledge/cases/<机型>-<场景>-<频段>-<关键词>.md`,在末尾引用对应 SOP,并提议 SOP 更新
- **改方法论**:直接改 `methodology/` 下文件,版本号+1,在 `CHANGELOG.md` 记录
- **改矩阵**:只改 `matrix.yaml`,跑 `gen_matrix_views.py`,commit 二者

---

## 成功指标(北极星)

| 指标 | 当前 | 6 个月目标 | 12 个月目标 |
|---|:---:|:---:|:---:|
| 已完成 SOP 数 | 14 | 30 | 41 + 扩展 |
| 案例库 | 1 | 15 | 40 |
| 架构 linter 检查项 | 9 | 12 | 15(含 CI 集成) |
| 平均排查周期(新案例 → 闭环) | — | 5 天 | 3 天 |
| 知识漂移次数(月)| — | 0 | 0 |
| 新接口人上手时间 | — | 2 周 | 1 周 |

---

## 参考

- [CLAUDE.md](../CLAUDE.md) — 项目级行为规范
- [CHANGELOG.md](../CHANGELOG.md) — 历次架构变更记录
- [knowledge/glossary.md](../knowledge/glossary.md) — 术语词典
- [tools/check-architecture-consistency.py](../tools/check-architecture-consistency.py) — 架构一致性守护
- 原始参考文档:[射频天线项目接口人工作手册](https://mi.feishu.cn/docx/DUKIdPkSGoH6UkxGRWwc5p84n7f)

---

**维护者**:射频天线团队 / Echo 项目接口人
**欢迎贡献**:见 [docs/contributing.md](contributing.md)
