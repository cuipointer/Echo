---
title: O11 WiFi 2.4G chain1 Normal 信道平坦度 6.2 dB(CPU 屏蔽罩泄露)
date: 2026-05-06
status: 已闭环(硬件整改)
source_case: EMC 2024 A.2(从 EMC-2024-Desense-triage.md 拆出的独立案例)
sop_refs: [W24-09]
---

# 案例:O11 WiFi 2.4G chain1 Normal 平坦度 6.2 dB — CPU 屏蔽罩泄露

**机型**:O11
**阶段**:P1
**现象**:2.4G WiFi **chain1** Normal 信道间平坦度最差 **6.2 dB**(全频段宽带劣化)
**持续天数**:13 天

---

## 分析流程(Echo 框架)

| Step | 动作 | 输出 |
|:---:|---|---|
| 1. 参数解析 | 受扰体 `W24` / 场景 `normal` / "chain1 信道平坦度 6.2 dB" | 参数完整 |
| 2. Normal 优先 | 自身即 Normal 基准 | 基线 = 测试自身 |
| 3. **宽窄带判别** | **信道间平坦度差** → **全频段宽带特征**(对照 A.1 的单频点) | ✓ 保留:平台泄露 / 电源 SSN / 屏蔽不良;✗ 排除:窄带谐波 |
| 4. 决策树 + 矩阵 | `W24` + 宽带 → 候选源 `SHIELD_LEAK / PMIC / DDR`;chain1 靠近 CPU 位置 → **H1:CPU 屏蔽罩泄露**;矩阵中原缺 `SHIELD_LEAK → W24`,Sprint 1 已补 `W24-09` | H1:CPU 屏蔽泄露 |
| 5. 三要素结论 | 见下方 | — |
| 6. 后续动作 | 软件不可解 → 硬件整改(屏蔽罩密封加强) | 直达硬件层 |

---

## 三要素分析

| 要素 | 内容 |
|---|---|
| **干扰源** | CPU 屏蔽罩内部的宽带噪声(DDR / 主芯片综合底噪) |
| **受扰体** | WiFi 2.4G(2412-2484 MHz 全频段,chain1 天线靠近 CPU 位置) |
| **耦合路径** | **辐射** —— 屏蔽罩密封不良,内部噪声向外泄露到 chain1 天线区域 |

---

## 根因

**CPU 屏蔽罩内部噪声从密封不良处辐射泄露**,chain1 天线因物理靠近 CPU 位置,受影响显著(chain0 受影响小,形成双链路差)。

---

## 解决方案

### 硬件措施(最终方案)

- P2 阶段回归验证**屏蔽罩加固**(屏蔽罩与中框贴合处优化、接地点密度提升)

### 长期措施

1. **设计查阅必查项**:屏蔽罩设计需要和天线 layout 做 overlay 检查,任何靠近天线的屏蔽罩都要有 chain 级灵敏度对比数据
2. **matrix.yaml 固化**:Sprint 1 已新增 `SHIELD_LEAK → W24 = W24-09` 映射

---

## 架构启示

1. **信道间平坦度差是 Normal Desense 的宽带干扰判据**,与 A.1(单频点)形成对照 —— 已固化进 [bandwidth-discrimination.md](../methodology/bandwidth-discrimination.md) 的"信道平坦度 ≥ 3 dB → 宽带平台泄露"判据
2. **chain 间差异是定位利器**:双链路(chain0/chain1)独立测试时,若只有一条链路恶化,应立即怀疑"天线位置临近的泄露源",而非全局干扰
3. **Echo 方法论补充**:Normal 优先原则下,应增加"信道平坦度 ≥ N dB"作为宽带 Normal Desense 的自动触发判据(已实现)

---

## 反哺 SOP

- **SOP-W24-09(SHIELD_LEAK → WiFi 2.4G,新建)**:本案例是该 SOP 的首个闭环样本,驱动:
  - Section 二·理论预判:增加"chain 间差异"作为宽带屏蔽泄露的典型特征
  - Section 四·硬件排查:把"屏蔽罩密封性检查 → 接地点密度优化"作为主路径
  - Section 五·结论模板:强调"天线 physical location vs CPU 屏蔽罩"作为必查项

---

## 参考

- 原始案例汇总:[EMC-2024-Desense-triage.md](EMC-2024-Desense-triage.md#a2)
- SOP W24-09:[../sops/W24/W24-09.md](../sops/W24/W24-09.md)
- 方法论:[../methodology/bandwidth-discrimination.md](../methodology/bandwidth-discrimination.md)
- 矩阵:[../matrix/matrix.yaml](../matrix/matrix.yaml)(`SHIELD_LEAK → W24 = W24-09` v2.1.0 新增)
