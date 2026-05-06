---
title: O11U GPS L1 DDR Desense 3 dB(PMIC 屏蔽罩顶部开窗泄露)
date: 2026-05-06
status: 已闭环(设计级改版)
source_case: EMC 2024 C.3(从 EMC-2024-Desense-triage.md 拆出的独立案例)
sop_refs: [GL1-03, GL1-04]
---

# 案例:O11U GPS L1 DDR Desense 3 dB — PMIC 屏蔽罩顶部开窗(设计缺陷)

**机型**:O11U
**阶段**:P0.1
**现象**:GPS L1 DDR 场景 Desense **~3 dB**(L1 频段 1561-1606 MHz)
**持续天数**:**42 天(设计级改版耗时代表)**

> **看起来 3 dB 数字小,但 GPS L1 敏感度 -140 ~ -150 dBm,3 dB 恶化足以显著影响定位成功率 / TTFF / 低信号场景可用性**

---

## 分析流程(Echo 框架)

| Step | 动作 | 输出 |
|:---:|---|---|
| 1. 参数解析 | 受扰体 `GL1`(1561-1606 MHz,敏感度 -140 dBm 量级)/ 场景 `ddr` / "3 dB" | **GPS 敏感度极高,3 dB 即严重** |
| 2. Normal 优先 | 强制检查;GPS Normal 特别要求(通常 ≤ 3 dB) | 假设基线达标 |
| 3. **宽窄带判别** | **GPS 单频段 3 dB + DDR 场景** → 宽带噪声经结构路径耦合 | ✓ 保留:平台泄露 / 屏蔽不良 |
| 4. 决策树 + 矩阵 | `GL1` + `ddr` → **多重命中**:`DDR → GL1 = GL1-03` + `PMIC → GL1 = GL1-04` + `SHIELD_LEAK → NORMAL = NORMAL-07`;定位到 **H1:BOT 面 PMIC 屏蔽罩顶部开窗(设计级缺陷)** | H1:屏蔽罩设计开窗 |
| 5. 三要素结论 | 见下方 | — |
| 6. 后续动作 | 软件无解 + 普通硬件修补无效(42 天)→ **设计级改版**:PMIC 屏蔽罩取消顶部开窗,切换积水铜箔 | 设计级(最高成本) |

---

## 三要素分析

| 要素 | 内容 |
|---|---|
| **干扰源** | BOT 面 PMIC 屏蔽罩内噪声(DDR 相关宽带底噪) |
| **受扰体** | **GNSS L1(1561-1606 MHz,敏感度 -140 ~ -150 dBm)** |
| **耦合路径** | **辐射** —— 屏蔽罩顶部开窗泄露 → PCB 另一面 → GPS 天线 |

---

## 根因

**BOT 面 PMIC 屏蔽罩顶部有开窗(为其他工艺便利)**,噪声从开窗处辐射,通过 PCB 另一面耦合到 GPS 天线。属于**设计级缺陷**,非装配 / 物料问题,所以常规整改无效。

---

## 解决方案

### 设计级措施(最终方案)

- **PMIC 屏蔽罩顶部开窗取消,切换为积水铜箔**(完全封闭屏蔽)

### 长期措施

1. **设计查阅必查项新增**:所有屏蔽罩**"设计级开窗"**(为工艺便利而开)必须在 RF 协同 review 时标注 → 评估对敏感接收机(特别是 GPS / BDS / 远信号场景 LTE LB)的影响
2. **matrix.yaml**:本案例是 `DDR → GL1 = GL1-03` + `PMIC → GL1 = GL1-04` 两条映射的综合样本,两 SOP 都需引用

---

## 架构启示

1. **GPS L1 的 3 dB ≠ WiFi 的 3 dB**:GPS 敏感度 -140 ~ -150 dBm,任何小幅恶化都严重影响定位质量,特别是弱信号场景(地库 / 峡谷)。**GPS SOP 的阈值应比 WiFi / LTE 更严**
2. **"设计级开窗"是隐蔽缺陷**:普通 SOP 的"屏蔽罩密封性检查"通常查装配,但**设计级开窗是"合规装配但设计本身不合规"** —— 必须在 PCB / 屏蔽罩设计 review 阶段标注
3. **多源矩阵命中时需要综合诊断**:GL1-03 + GL1-04 + NORMAL-07 三条映射都命中,说明**"干扰源识别"要允许一个案例触发多条 SOP 路径**,SOP 间需相互引用
4. **42 天耗时分析**:常规修补 30 天无效(屏蔽罩加胶 / 接地 / 铜箔等)→ 最终设计改版 → 提示**普通整改 > 3 周无进展 → 强制升级到设计级 review**,这是**时间护栏**应写进诊断流程

---

## 反哺 SOP

- **SOP-GL1-03(DDR → GNSS L1)**:本案例是该 SOP 的首选闭环样本:
  - Section 二·理论预判:DDR 宽带底噪在 GPS L1 附近的频谱分布
  - Section 四·硬件排查:将"屏蔽罩顶部开窗"作为必检项(与"屏蔽罩贴合 / 接地"并列)
  - Section 六·典型案例:本案例 + 3 dB 严重性说明
- **SOP-GL1-04(PMIC → GNSS L1)**:本案例驱动:
  - Section 二·设计审查:必查"BOT 面 PMIC 屏蔽罩设计"专项
  - Section 五·结论模板:新增"开窗检查"条目
- **SOP-NORMAL-07(SHIELD_LEAK → NORMAL)**:本案例作为屏蔽罩设计缺陷的典型引用

---

## 参考

- 原始案例汇总:[EMC-2024-Desense-triage.md](EMC-2024-Desense-triage.md#c3)
- SOP GL1-03:[../sops/GL1/GL1-03.md](../sops/GL1/GL1-03.md)
- SOP GL1-04:[../sops/GL1/GL1-04.md](../sops/GL1/GL1-04.md)
- SOP NORMAL-07:[../sops/NORMAL/SOP-NORMAL-07.md](../sops/NORMAL/SOP-NORMAL-07.md)
- 方法论:[../methodology/bandwidth-discrimination.md](../methodology/bandwidth-discrimination.md)
- 矩阵:[../matrix/matrix.yaml](../matrix/matrix.yaml)(`DDR → GL1 = GL1-03` / `PMIC → GL1 = GL1-04`)
