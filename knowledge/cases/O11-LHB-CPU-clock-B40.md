---
title: O11 B40 DIV FrontCam 场景 Desense 16 dB(CPU 768M 三次倍频命中)
date: 2026-05-06
status: 已闭环(硬件屏蔽)
source_case: EMC 2024 B.1(从 EMC-2024-Desense-triage.md 拆出的独立案例)
sop_refs: [LHB-01]
---

# 案例:O11 B40 DIV FrontCam 场景 16 dB — CPU 768M 三次倍频

**机型**:O11
**阶段**:P1
**现象**:B40 DIV **FrontCam 场景** Desense 最大值 **16 dB**(B40 DIV = 2300-2400 MHz)
**持续天数**:17 天

---

## 分析流程(Echo 框架)

| Step | 动作 | 输出 |
|:---:|---|---|
| 1. 参数解析 | 受扰体 `LHB`(B40 2300-2400 MHz)/ 场景 `rc`(前摄)/ "DIV 16 dB" | 参数完整 |
| 2. Normal 优先 | 强制检查(假设 ≤ 1 dB 达标) | 假设基线达标 |
| 3. **宽窄带判别** | **单频段 16 dB** → **窄带谐波强命中** | ✓ 保留:时钟类谐波;✗ 排除:电源宽带 |
| 4. 决策树 + 矩阵 | 谐波计算:**CPU 768 MHz × 3 = 2304 MHz**,正中 B40 低端;查矩阵 `OSC → LHB = LHB-01`(可考虑新增 `CPU_CLOCK → LHB`);FrontCam 场景激活 → 放大辐射路径 | H1:CPU 768M×3 命中 B40 |
| 5. 三要素结论 | 见下方 | — |
| 6. 后续动作 | 软件不可调 CPU 时钟 → 硬件:**全方位导电泡棉屏蔽**(包围性) | 硬件层 |

---

## 三要素分析

| 要素 | 内容 |
|---|---|
| **干扰源** | CPU 时钟 768 MHz 的**三次倍频 = 2304 MHz** |
| **受扰体** | LTE B40 DIV(2300-2400 MHz,DIV 链路对弱信号敏感) |
| **耦合路径** | **辐射** —— CPU 屏蔽罩泄露 + FrontCam 场景激活放大辐射路径 |

---

## 根因

**CPU 768 MHz 时钟的三次谐波(2304 MHz)正好落在 B40 低端**。FrontCam 场景激活时,前摄 FPC / 接口的有效辐射面增大,放大了原本隐蔽的 CPU 屏蔽泄露。

---

## 解决方案

### 硬件措施(最终方案)

- **中框增加全方位导电泡棉屏蔽**(包围性屏蔽增强 CPU 区域密封性,阻断辐射泄露)

### 长期措施

1. **设计查阅必查项**:时钟规划 review 需要覆盖**所有整数倍谐波**与 LTE HB 各 Band 的命中关系,768 MHz / 1024 MHz / 其他主时钟的 2~5 次谐波都应做命中表
2. **SOP LHB-01 补强**:把"FrontCam 场景放大效应"作为典型场景入 Section 六·典型案例

---

## 架构启示

1. **16 dB 单场景恶化是极严重水平**(B40 典型灵敏度 -94~-102 dBm),会直接影响通话/数据质量
2. **关键诊断点**:CPU 768M × 3 = 2304 MHz 的谐波计算 —— `/diagnose` Step 3 宽窄带判别 + 谐波命中组合能秒杀的案例;`harmonic-calc` skill 可验证命中
3. **FrontCam 场景放大辐射**:场景激活不仅激活新干扰源,**也可能放大既有源的辐射路径**(通过改变物理结构 / 激活 FPC 弯折 / 放大天线耦合面)—— 这是场景 Desense 的一个关键机制
4. **矩阵考虑**:是否把 `CPU_CLOCK(768M)` 作为独立源,还是归并到 `OSC`?结论:归并到 `OSC` 即可(SOP LHB-01 已覆盖),矩阵细分到具体频率会过度膨胀

---

## 反哺 SOP

- **SOP-LHB-01(OSC/LCD_MIPI → LHB)**:本案例是该 SOP 的重点闭环样本:
  - Section 二·理论预判:增加"CPU 主时钟 × N 次谐波 → LTE HB 各 Band 命中表"
  - Section 三·软件排查:强调"**FrontCam 场景对比 Normal**"作为验证"场景放大辐射"假设的零成本步骤
  - Section 四·硬件排查:主路径强调"全方位导电泡棉 / CPU 屏蔽加强"

---

## 参考

- 原始案例汇总:[EMC-2024-Desense-triage.md](EMC-2024-Desense-triage.md#b1)
- SOP LHB-01:[../sops/LHB/LHB-01.md](../sops/LHB/LHB-01.md)
- 方法论:[../methodology/bandwidth-discrimination.md](../methodology/bandwidth-discrimination.md)
- 谐波工具:`python3 tools/harmonic_calc.py 768 3 2300 2400` → 命中 B40 ✓
- 矩阵:[../matrix/matrix.yaml](../matrix/matrix.yaml)(`OSC → LHB = LHB-01`)
