---
description: 生成正式的 Desense 分析报告(debug / weekly / summary)
argument-hint: [报告类型: debug|weekly|summary] [输入文件]
---

# /formal

用户输入:`$ARGUMENTS`

按指定模板生成正式报告,输出到 [playground/outputs/](playground/outputs/) 或用户指定路径。

## 1. 解析参数

- **报告类型**(默认 `debug`):
  - `debug`:单个问题的排查报告
  - `weekly`:周报
  - `summary`:总结报告
- **输入文件**(可选):已有的排查记录 / 日志文件路径
- **输出文件**(可选):默认 `playground/outputs/<类型>-YYYYMMDD.md`

## 2. 选择模板

| 报告类型 | 模板路径 |
|---|---|
| debug | `logs/templates/debug-template.md`(若不存在则查 `logs/templates/` 下的等价模板) |
| weekly | `logs/templates/weekly-template.md` |
| summary | `knowledge/report-template.md` 或现场生成 |

先 `Read` 模板文件,确认结构后再写报告;若模板不存在,采用以下默认骨架。

## 3. 默认骨架

### Debug 报告

1. **标题**:问题编号 + 日期
2. **问题描述**:现象 + 环境
3. **三要素分析**:干扰源 / 受扰体 / 耦合路径
4. **排查过程**:时间线 + 操作记录
5. **方案记录**:软件 / 硬件 / 长期措施
6. **结论**:最终状态 + 改善幅度
7. **附件**:相关文档和数据

### 周报

1. 本周成果
2. 问题汇总
3. 详细记录
4. 下周计划
5. 风险与阻塞

### 总结报告

1. 问题概述
2. 分析过程
3. 解决方案
4. 经验总结
5. 改进建议

## 4. 写入

将最终 Markdown 写到目标路径;若路径未指定,使用 `playground/outputs/<类型>-YYYYMMDD-<slug>.md`。写入后向用户返回文件路径和章节清单。

## 5. 后续动作

- 若报告需要入知识库(如典型案例) → 手动搬到 `knowledge/cases/`。
- 若是周报 → 建议同步到 `logs/weekly/`。
