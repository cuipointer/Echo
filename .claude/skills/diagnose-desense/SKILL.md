---
name: diagnose-desense
description: 识别用户的 Desense 诊断需求并触发 /diagnose slash 命令执行。触发:用户报告 Desense / 灵敏度恶化 / 场景(LCD/Camera/RC/VIDEO 等) × 频段(WiFi/LTE/GNSS)的干扰问题,或提供受扰频段 + 测试场景 + 干扰幅度。
---

# Diagnose Desense Skill(触发器)

## 职责

本 skill **不定义诊断流程**,只负责识别自然语言中的 Desense 诊断需求,转交给 `/diagnose` slash 命令执行。

诊断流程、决策树、矩阵查询、输出模板的**唯一真相源**是 [`.claude/commands/diagnose.md`](../../commands/diagnose.md)。

## 触发条件

以下自然语言表达触发本 skill:

- "XX 机型 XX 场景 XX 频段 Desense"(例如 "AS2 RC WiFi 2.4G ch1-13 4~7 dB")
- "灵敏度恶化 / 灵敏度下降 / sensitivity degradation"
- 明确给出"受扰频段 + 测试场景"两者中至少一项
- 用户主动要求"诊断 / debug / 排查 Desense 问题"

## 动作

1. **解析自然语言**,提取:
   - 受扰频段 → 映射到 `W24 / W5 / LLB / LHB / GL1 / GL5`
   - 测试场景 → 映射到 `normal / lcd / ddr / video / vib / fc / rc`
   - 干扰描述 → 自由文本
2. **转交 `/diagnose`**:以"调用 /diagnose 命令,参数为 `<频段> <场景> <描述>`"的形式推进。
3. **Normal 优先检查**:若用户未提 Normal 基线,在转交前提示用户确认,避免在基准未对齐的情况下进入场景诊断。

## 与其他模块的关系

| 模块 | 关系 |
|---|---|
| `/diagnose` 命令 | **本 skill 的执行后端**。流程、输出模板、SOP 引用全部由命令文件定义。 |
| `echo` agent | 提供 Desense 专家人格和方法论语境。本 skill 识别到需求后可在 echo 语境下转交 `/diagnose`。 |
| `harmonic-calc` skill | 若诊断过程中需谐波计算,由 `/diagnose` 工作流调用。 |
| `sop-executor` skill | 诊断输出 SOP 编号后,由 `/diagnose` 建议用户调用本 skill 按 SOP 执行。 |

## 不做什么

- ❌ 不重复定义 5 步诊断流程
- ❌ 不重复定义输出模板
- ❌ 不直接读决策树 / 矩阵表(由 `/diagnose` 统一读)

---

**设计备注**:本 skill 原本包含完整工作流和输出模板,与 `/diagnose` 命令和 `echo` agent 重复。经架构审计后(2026-04-27)折叠为纯触发器,单一真相源归 `/diagnose`。
