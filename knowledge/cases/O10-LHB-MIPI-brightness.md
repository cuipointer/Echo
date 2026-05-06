---
title: O10 N77 亮屏场景 Desense 11 dB(屏 MIPI CLK 高频噪声)
date: 2026-05-06
status: 已闭环(硬件串感)
source_case: EMC 2024 B.3(从 EMC-2024-Desense-triage.md 拆出的独立案例)
sop_refs: [LHB-01]
---

# 案例:O10 N77 亮屏 Desense 11 dB — 屏 MIPI CLK 高频噪声

**机型**:O10
**阶段**:P1
**现象**:N77 亮屏场景 Desense 最大值 **11 dB**(N77 = 3300-4200 MHz)
**持续天数**:**6 天(熟路快速闭环)**

---

## 分析流程(Echo 框架)

| Step | 动作 | 输出 |
|:---:|---|---|
| 1. 参数解析 | 受扰体 `LHB`(N77 3300-4200 MHz)/ 场景 `lcd`(亮屏)/ "11 dB" | 参数完整 |
| 2. Normal 优先 | 强制检查(假设达标) | 假设基线达标 |
| 3. **宽窄带判别** | **单频段 11 dB + 亮屏触发** → 窄带谐波强命中 | ✓ 保留:MIPI 时钟谐波;✗ 排除:宽带 |
| 4. 决策树 + 矩阵 | `LHB` + `lcd` 场景 → `LCD_MIPI → LHB = LHB-01`(矩阵首命中);**6 天闭环**说明 H1 直接命中,无需多假设枚举 | H1:LCD MIPI 高频谐波 |
| 5. 三要素结论 | 见下方 | — |
| 6. 后续动作 | 硬件:**MIPI 通路串 10 nH 电感**(成本低 / 验证快) | 硬件层(低成本) |

---

## 三要素分析

| 要素 | 内容 |
|---|---|
| **干扰源** | 屏 MIPI CLK 高频噪声(CLK 频率的高次谐波) |
| **受扰体** | 5G NR N77(3300-4200 MHz,亮屏场景触发 MIPI 工作) |
| **耦合路径** | **辐射** —— MIPI 信号高频谐波从屏 BTB / FPC 辐射到天线 |

---

## 根因

**亮屏时 MIPI CLK 线高频噪声辐射**,通过屏 BTB / FPC 传播到 N77 天线区域。MIPI CLK 的高次谐波密度在 3~4 GHz 区间较大。

---

## 解决方案

### 硬件措施(最终方案)

- **MIPI 通路串 10 nH 电感**(抑制高频噪声;电感选择需兼顾 MIPI 数据完整性,10 nH 是实测权衡后的最优值)

### 长期措施

1. **SOP LHB-01 补强**:"MIPI 串电感 / 磁珠"作为**优先硬件措施**(成本极低、验证快,应优于改结构件)
2. **设计查阅**:MIPI 通路是否预留串电感 / 磁珠封装位,应作为 DFX 规范条目

---

## 架构启示

1. **6 天快速闭环是"熟路问题"标杆**:标准 SOP 覆盖充分时,亮屏 + 高频段 Desense 可以秒杀。对比 C.2 的 42 天,说明**SOP 覆盖度和耗时成强反比**
2. **"MIPI 串 10 nH 电感"**是 LHB-01 应固化的首选硬件动作(对比其他更重的硬件方案如屏蔽罩改版 / 铜箔 / 导电泡棉)
3. **亮屏场景对应的 MIPI CLK 谐波模型**:
   - MIPI CLK 基频 ~900 MHz / 1 GHz(跟 panel / 码率相关)
   - 3~5 次谐波覆盖 3~5 GHz,正好命中 N77 / N79 / WiFi 5G
   - `harmonic-calc` skill 可快速计算

---

## 反哺 SOP

- **SOP-LHB-01(OSC/LCD_MIPI → LHB)**:本案例是该 SOP 的首选快速闭环样本:
  - Section 二·理论预判:列出 MIPI CLK 基频 × N 次 → N77 / N79 / WiFi 5G 命中表
  - Section 四·硬件排查:**首推 10 nH 串电感**(附完整物料选型:阻抗 / 电流 / 封装),其次才是改 PCB / 改屏蔽
  - Section 七·检查表:增加"MIPI 通路是否串电感"作为设计必检项

---

## 参考

- 原始案例汇总:[EMC-2024-Desense-triage.md](EMC-2024-Desense-triage.md#b3)
- SOP LHB-01:[../sops/LHB/LHB-01.md](../sops/LHB/LHB-01.md)
- 方法论:[../methodology/bandwidth-discrimination.md](../methodology/bandwidth-discrimination.md)
- 谐波工具:`python3 tools/harmonic_calc.py <MIPI_CLK_freq> 4 3300 4200` 验证命中
- 矩阵:[../matrix/matrix.yaml](../matrix/matrix.yaml)(`LCD_MIPI → LHB = LHB-01`)
