---
title: O2 WiFi 5G 5765 Normal Desense Fail 20 dB(时钟 spur)
date: 2026-05-06
status: 已闭环(软件解)
source_case: EMC 2024 A.1(从 EMC-2024-Desense-triage.md 拆出的独立案例)
sop_refs: [W5-01]
---

# 案例:O2 WiFi 5G 5765 Normal Desense Fail 20 dB — 时钟 Spur

**机型**:O2
**阶段**:P1
**现象**:5G WiFi **5765 MHz** Normal Desense 最差值 **Fail 20 dB**(单频点)
**持续天数**:21 天

---

## 分析流程(Echo 框架)

| Step | 动作 | 输出 |
|:---:|---|---|
| 1. 参数解析 | 受扰体 `W5` / 场景 `normal` / "5765 单频点 Fail 20 dB" | 参数完整 |
| 2. Normal 优先 | 本身即 Normal 场景,无需检查基线 | 基线 = 测试自身 |
| 3. **宽窄带判别** | **单频点 20 dB** → **强窄带特征** | ✓ 保留:时钟谐波类源;✗ 排除:宽带 EMI / 电源 SSN |
| 4. 决策树 + 矩阵 | `W5` + 窄带 → 候选源 `OSC / MIPI`;Normal 场景无显示/摄像激活 → **H1:OSC 倍频**(首选);对应 `W5-01` | 主假设 H1:OSC 倍频命中 |
| 5. 三要素结论 | 见下方 | — |
| 6. 后续动作 | **零成本验证**:数字滤波器 NV 调参(无需改板)→ 成功 | 软件优先原则命中 |

---

## 三要素分析

| 要素 | 内容 |
|---|---|
| **干扰源** | 系统时钟(XO/OSC)的倍频产生的 spur,落在 5765 MHz |
| **受扰体** | WiFi 5G 5765 MHz(单频点,窄带干扰特征) |
| **耦合路径** | 传导 + 辐射混合 —— 噪声沿电源 / 地平面进入接收前端 |

---

## 根因

5765 MHz 有**时钟倍频产生的 spur**。系统时钟的某个倍频(需结合实际时钟频率反推)恰好落在 WiFi 5G 信道内,形成 CW spur 压制接收。

---

## 解决方案

### 软件措施(最终方案)

- 导入**数字滤波器措施**(NV 配置级,非硬件改板)。

### 长期措施

1. **SOP W5-01 补强**:把"数字滤波器 NV 调参"作为软件首选措施写进 Section 三·软件排查步骤
2. **设计查阅**:量产前的时钟规划 review 需要对照 WiFi 5G 所有可能信道(非单一默认信道),避免 spur 落点遗漏

---

## 架构启示

1. **单频点 20 dB 恶化是窄带谐波命中典型特征**,完全匹配 Echo 方法论 [bandwidth-discrimination.md](../methodology/bandwidth-discrimination.md) 的"单频 ≥10 dB → 窄带谐波"判据
2. **软件优先原则有效样本**:无需拆机 / 改板,21 天完成(相比 A.2 的 13 天硬件改版更低成本,但从发现到定位到软件方案的路径效率决定总耗时)
3. **NV 调参不属于"用户可感"的软件,不冲突稳定性**:这是工厂阶段的参数导入,客户无感

---

## 反哺 SOP

- **SOP-W5-01(OSC/LCD_MIPI → WiFi 5G)**:本案例是该 SOP 的首个闭环样本,驱动 Section 三·步骤 2(软件规避)明确写"数字滤波器 NV 调参";并把"时钟倍频谐波命中信道"作为 Section 二·理论预判的主要假设

---

## 参考

- 原始案例汇总:[EMC-2024-Desense-triage.md](EMC-2024-Desense-triage.md#a1)
- SOP W5-01:[../sops/W5/W5-01.md](../sops/W5/W5-01.md)
- 方法论:[../methodology/bandwidth-discrimination.md](../methodology/bandwidth-discrimination.md)
- 矩阵:[../matrix/matrix.yaml](../matrix/matrix.yaml)(`OSC → W5` 映射)
