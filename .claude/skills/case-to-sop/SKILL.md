---
name: case-to-sop
description: 案例驱动 SOP 沉淀。从新增 knowledge/cases/*.md 的 frontmatter sop_refs 出发,自动规划每个被引用 SOP 应该做的更新(stub→v0.9 全量重写 / v0.9→追加案例 / 正式版→仅追加 Section 六)。触发:"案例沉淀"、"驱动 SOP"、"反哺 SOP"、"/case-to-sop"、用户新增或修改 knowledge/cases/*.md 并要求更新对应 SOP。
metadata:
  audience: developers
  workflow: knowledge-curation
  category: sop-lifecycle
---

# case-to-sop

## 职责

当一个新的案例文件(`knowledge/cases/*.md`)写完后,把案例中的经验**反哺**到对应的 SOP(`knowledge/sops/<band>/*.md`)。本 skill 负责:

1. 读案例 frontmatter 中的 `sop_refs: [SOP-ID, ...]`
2. 对每个 SOP 判断当前状态:**stub**(v0.1 placeholder)/ **v0.9**(方法论版)/ **formal**(v1.0+ 正式版)
3. 给出**具体的更新动作**(全量重写 / 追加反哺 / 追加案例)
4. 由 Claude 按计划执行 Read / Edit / Write 落盘

本 skill 是 **Planner + Executor** —— 规划来自脚本,实际落盘由 Claude 在语境中完成。

## 触发条件

满足以下任一:

1. 用户输入 `/case-to-sop` 或 slash 命令等价形式
2. 用户说"案例沉淀"、"反哺 SOP"、"驱动 SOP 更新"、"把这个案例的结论写回 SOP"
3. 用户刚新建或刚修改 `knowledge/cases/*.md`,并希望同步更新 SOP
4. 用户引用具体案例文件路径并要求"更新对应 SOP"

## 实现绑定

| 调用路径 | 实现 | 责任 |
|---|---|---|
| **主路径(规划)** | `tools/case_to_sop.py` | 解析案例 frontmatter + 状态检测 + 输出更新计划 |
| **执行(落盘)** | Claude(Read / Edit / Write) | 按计划实际修改 SOP 文件 |
| **状态检测逻辑共享** | 与 `tools/check-architecture-consistency.py` L51-58 对齐 | 保持"stub / v0.9 / formal"判定单一真相源 |

## 工作流程

### 1. 参数解析

从用户输入中提取 **案例文件路径**(形如 `knowledge/cases/<name>.md`)。
如果用户只提案例名未提路径,先在 `knowledge/cases/` 中匹配。

### 2. 规划(调用脚本)

```bash
python3 tools/case_to_sop.py <case-file.md>
```

输出内容结构:

- **案例元信息**:title / 机型阶段 / 现象 / source_case
- **sop_refs** 列表
- **关键案例要点**(脚本自动抽取的 5 条 bullets)
- **逐 SOP 行动计划**:每个 SOP 一个 `=== SOP-X-YY ===` 区段,含 State / Template / Proposed action
- **后续执行提示**

### 3. 状态 → 动作映射(Claude 执行依据)

| State | 动作 | 关键产物 |
|---|---|---|
| `stub`(v0.1 placeholder)| **Full v0.9 rewrite**(基于案例 + 兄弟 SOP 结构)| 完整 8 章节方法论版,版本 v0.9.0,标注"方法论版(待现场复测)" |
| `v0.9`(方法论版)| **追加 Section 六 + 更新反哺引用** | 案例追加到典型案例章节,更新附录引用与更新记录,版本 v0.9.x→v0.9.(x+1) |
| `formal`(v1.0+ 正式版)| **仅追加 Section 六 典型案例** | 只动第六章,版本 v1.x.y→v1.x.(y+1) |
| `missing` | 提示先跑 `tools/gen_sop_stubs.py` 生成 placeholder | — |

### 4. 执行(Claude 落盘)

按计划对每个 SOP:

1. Read 目标 SOP 全文
2. **stub** → 参照脚本给出的 sibling 模板,Write 全量新版(含本案例作首源案例 + 教训反思)
3. **v0.9 / formal** → Edit 追加 Section 六 案例块,更新版本号 / 日期 / 更新记录表

### 5. 校验

落盘后运行:

```bash
python3 tools/check-architecture-consistency.py
```

重点关注:SOP 行数阈值(v0.9: 180-500 / formal: 180-300)、必备章节、版本号格式。

### 6. 日志

调用 `engineering-logger` 技能追加日志,记录:

- 案例文件
- 更新到的 SOP 列表(含版本号变动)
- 是否触发 matrix.yaml 变更(通常不会,除非案例引入了新的源×受扰体映射)

## 输出契约

Claude 在执行计划后给用户的回复应包含:

```markdown
## 案例反哺结果

**案例**:`knowledge/cases/<name>.md`

### SOP 变更清单
| SOP | Before | After | 动作 |
|---|---|---|---|
| SOP-X-YY | v0.9.0 | v0.9.1 | 追加 Section 六 案例 |
| ... | ... | ... | ... |

### 关键反哺点
- <从案例抽取的 1-3 条方法论级教训>

### 后续建议
- 是否需要更新 matrix.yaml(仅当案例引入新 source × victim 组合)
- 是否需要更新 bandwidth-discrimination.md(仅当案例纠正了宽窄带判别反例)
```

## 与其他 skill / 命令的关系

| 模块 | 关系 |
|---|---|
| `engineering-logger` | 落盘后调用以记录日志 |
| `sop-executor` | 本 skill 负责 SOP "写入",后者负责 SOP "执行" —— 正交关系 |
| `/diagnose` | 诊断完成 → 用户写案例 → 本 skill 把案例反哺回 SOP |
| `/formal` | 正式报告生成后,若报告伴随新案例,可链式触发本 skill |
| `tools/check-architecture-consistency.py` | 状态检测逻辑共享;落盘后用于校验 |
| `tools/gen_sop_stubs.py` | 若 sop_refs 命中不存在的 SOP,提示先跑此脚本 |

## 不做什么

- 不自动修改 matrix.yaml(矩阵变更需用户显式决策,本 skill 只提示)
- 不自动修改 methodology/ 方法论文档(同上)
- 不 commit(提交由 engineering-logger 或用户手动完成)
- 不在用户未确认的前提下对 formal(v1.0+) SOP 做结构性修改 —— 只追加 Section 六

## 设计备注

本 skill 把 Sprint 2 手动编排的 "Agent prompt pattern" 固化下来:Sprint 2 的每个 v0.9 SOP 都是以 **(案例 + 兄弟 SOP 模板 + Echo 方法论)** 三要素由 Agent 生成。`tools/case_to_sop.py` 把这三者的定位自动化(通过 frontmatter sop_refs + 同 band 最强兄弟 SOP + 共享的状态检测逻辑),Claude 只负责在语境中按计划落盘,避免每次都要手动挑模板、手动判版本。

---

**版本**:v1.0.0(2026-05-06)
