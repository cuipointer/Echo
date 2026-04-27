# Normal 领域知识库

**版本**：v1.0.0  
**更新日期**：2026-04-22  
**更新内容**：创建Normal领域知识库概述文档

---

## 概述

**Normal Desense** 是手机在**灭屏且其他功能全部关闭**状态下的射频灵敏度恶化问题，是所有场景的**基准线**，具有最高优先级。

## 核心概念

### 定义
- **Normal场景**：灭屏 + 所有功能关闭的基准状态
- **Normal Desense**：辐射灵敏度相对于传导灵敏度的恶化值
- **基准线作用**：其他场景干扰都是在Normal基础上叠加

### 重要性
> ⚠️ **任何Desense问题排查的第一步永远是确认Normal是否达标（≤1dB）**

## 知识结构

### 核心文档

| 文档 | 内容概述 | 关键要点 |
|------|----------|----------|
| [概述](overview.md) | Normal定义、重要性、技术特点 | 基准线概念、排查铁律 |
| [干扰源分类](interference-sources.md) | 8类干扰源详细分析 | 优先级排序、快速定位 |
| [分析流程](analysis-flow.md) | 标准化排查步骤 | 传导确认、大小功率检查 |
| [限值定义](limits.md) | 企标要求、设计目标 | 场景叠加计算公式 |

### 相关SOP

| SOP编号 | 干扰源 | 受扰体 | 说明 |
|---------|--------|--------|------|
| [NORMAL-01](../../sops/NORMAL/SOP-NORMAL-01.md) | 系统电源 | Normal | PMIC开关噪声 |
| [NORMAL-02](../../sops/NORMAL/SOP-NORMAL-02.md) | 系统时钟 | Normal | 时钟谐波干扰 |
| [NORMAL-03](../../sops/NORMAL/SOP-NORMAL-03.md) | 射频电源 | Normal | PA供电噪声 |
| [NORMAL-04](../../sops/NORMAL/SOP-NORMAL-04.md) | 非线性器件 | Normal | 交调干扰 |
| [NORMAL-05](../../sops/NORMAL/SOP-NORMAL-05.md) | PA匹配 | Normal | 阻抗失配 |
| [NORMAL-06](../../sops/NORMAL/SOP-NORMAL-06.md) | 天线Tuner | Normal | 控制噪声 |
| [NORMAL-07](../../sops/NORMAL/SOP-NORMAL-07.md) | 屏蔽泄露 | Normal | 辐射泄露 |
| [NORMAL-08](../../sops/NORMAL/SOP-NORMAL-08.md) | 电连接不良 | Normal | 接触非线性 |

## 排查流程

### 标准排查顺序
```
1. 传导测试确认
2. 大小功率一致性检查  
3. 交调问题排查
4. 电源和时钟排查
5. 屏蔽与接地排查
6. 解决方案导入
```

### 关键检查点
- **传导正常**：排除器件本身问题
- **大小功率一致**：判断非线性干扰
- **电源时钟**：系统级噪声源
- **屏蔽接地**：辐射泄露路径

## 限值标准

### 核心限值
| 标准等级 | 限值要求 | 适用场景 |
|:---|:---|:---|
| **企标要求** | ≤ 1.5dB | 产品认证 |
| **研发内部** | ≤ 1dB | 研发目标 |
| **设计目标** | ≤ 0.5dB | 理想设计 |

### 场景叠加公式
```
场景总干扰 = Normal Desense + 场景额外干扰
```

## 与其他领域关系

### Display领域
- **关系**：LCD干扰叠加在Normal基础上
- **限值对比**：Normal ≤1dB vs LCD ≤3dB
- **排查顺序**：先Normal后LCD

### Camera领域  
- **关系**：Camera干扰叠加在Normal基础上
- **限值对比**：Normal ≤1dB vs Camera ≤4dB
- **排查顺序**：先Normal后Camera

## 快速参考

### 排查优先级
1. **系统电源噪声**（PMIC Buck）
2. **时钟谐波**（系统时钟）
3. **非线性器件**（天线周围）
4. **屏蔽泄露**（结构问题）

### 典型问题模式
- **宽带恶化** → 电源/屏蔽问题
- **特定频段** → 时钟谐波问题  
- **大小功率差异** → 非线性问题

## 相关链接

### 方法论
- [场景优先级规则](../../methodology/scene-priority.md)
- [决策树](../../decision-tree.md)
- [矩阵表](../../matrix/matrix-table.md)

### 工具
- [架构一致性检查](../../tools/check-architecture-consistency.py)
- [SOP编写标准](../../docs/sop-writing-standard.md)

## 更新记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-22 | 创建Normal领域知识库 |