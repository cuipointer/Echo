---
description: 启动 Desense 问题诊断流程(三要素模型 + 决策树)
argument-hint: <受扰频段> <测试场景> [现象描述]
---

# /diagnose

用户输入:`$ARGUMENTS`

按以下流程对 Desense 问题做标准化诊断,输出三要素结论和可疑 SOP 编号。

## 1. 解析参数

从 `$ARGUMENTS` 中提取:
- **受扰频段**:W24 / W5 / LLB / LHB / GL1 / GL5
- **测试场景**:normal / lcd / ddr / video / vib / fc / rc
- **现象描述**(可选):如"灵敏度恶化 10 dB"

若参数缺失或歧义,用一次性问题向用户索取。

## 2. Normal 优先检查

先确认用户是否已测 Normal Desense:

- 未测 → 建议用户先做 Normal 基准测试
- Normal > 1 dB → 引导进入 Normal 排查,告知"Normal 是基准线,需要先解决才能准确评估场景干扰"
- Normal ≤ 1 dB → 计算`场景额外干扰 = 场景实测干扰 - Normal Desense`,继续下一步

## 3. 决策树 + 矩阵查询

- 读取 [knowledge/decision-tree.md](knowledge/decision-tree.md),根据受扰频段 + 测试场景收敛到"干扰源类别"
- 读取 [knowledge/matrix/](knowledge/matrix/) 下的矩阵表,根据"干扰源 × 受扰体"组合查 SOP 编号
- 若无对应 SOP,记录为新组合并提示需要补充 SOP

## 4. 输出格式

```markdown
## 诊断结果

### 问题信息
- 受扰频段:[频段]
- 测试场景:[场景]
- 干扰现象:[现象]

### 干扰源分析
- 可疑模块:[模块列表]
- 优先级:[高/中/低]

### 受扰体分析
- 频段:[频段]
- 敏感度要求:[dBm 值]

### 耦合路径分析
- 可能类型:[传导/辐射/串扰/地弹]

### SOP 编号
- [编号]:[组合描述]

### 下一步建议
1. [建议 1]
2. [建议 2]
```

## 5. 后续动作

- 若用户同意执行 SOP,调用 `sop-executor` skill 按编号引导排查
- 若需要计算谐波,调用 `harmonic-calc` skill
- 排查完毕生成报告时,建议用户使用 `/formal`

---

## 参考:原 OpenCode CLI 参数(仅供对照,已迁移到 Claude Code)

| 原 CLI 参数 | 对应值 |
|---|---|
| `-f, --freq` | W24 / W5 / LLB / LHB / GL1 / GL5 |
| `-s, --scene` | normal / lcd / ddr / video / vib / fc / rc |
| `-d, --desc` | 自由文本 |
