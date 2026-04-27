---
name: harmonic-calc
description: 谐波计算工具,判断干扰源基频的谐波是否命中受扰体频段。触发:用户询问谐波计算、提供基频+谐波次数+受扰体频段,或分析干扰是否来自某模块的谐波。
---

# Harmonic Calc Skill

## 描述

调用谐波计算工具，判断干扰源谐波是否命中受扰体频段。

## 触发条件

- 用户询问谐波计算
- 用户提供基频、谐波次数、受扰体频段
- 用户要求验证频率命中关系

## 工作流程

### 1. 收集参数
- 干扰源基频 (MHz)
- 谐波次数
- 受扰体频段起始频率 (MHz)
- 受扰体频段结束频率 (MHz)

### 2. 调用工具
- 执行 `tools/harmonic_calc.py`
- 传入参数计算

### 3. 输出结果
- 谐波频率
- 是否命中
- 频偏（如未命中）

## 工具调用

```bash
python3 tools/harmonic_calc.py <base_freq> <harmonic_order> <victim_start> <victim_end>
```

## 输出格式

```markdown
## 谐波计算结果

### 输入参数
- 基频：[频率] MHz
- 谐波次数：[次数]
- 受扰体频段：[起始]-[结束] MHz

### 计算结果
- 谐波频率：[频率] MHz
- 是否命中：[是/否]
- 频偏：[偏移量] MHz（如未命中）

### 结论
[根据计算结果给出结论]
```

## 知识库引用

- `knowledge/matrix/source-list.md`：干扰源清单
- `knowledge/matrix/victim-list.md`：受扰体清单
