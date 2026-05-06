---
title: O2 WiFi 2.4G Display Desense Fail 20 dB(NFC 谐波干扰)
date: 2026-05-06
status: 已闭环
source_case: EMC 2024 B.2(从 EMC-2024-Desense-triage.md 拆出的独立案例)
sop_refs: [W24-08]
---

# 案例:O2 WiFi 2.4G Display Desense Fail 20 dB — NFC 谐波干扰

**机型**:O2
**阶段**:P1
**现象**:
- 2.4G WiFi Desense Display/Touch on **Fail 20 dB**
- Video/Display 场景 Fail 18 dB

**持续天数**:33 天

---

## 分析流程(Echo 框架)

| Step | 动作 | 输出 |
|:---:|---|---|
| 1. 参数解析 | 受扰体 `W24` / 场景 `lcd`(Display/Touch on)/ "Fail 20 dB" | 参数完整 |
| 2. Normal 优先 | 强制检查(假设 Normal ≤ 1 dB 达标) | 基线达标 |
| 3. **宽窄带判别** | **单场景 20 dB** + Display 触发 → 两个候选模型:①Display 相关窄带(MIPI)②场景下共存干扰激活 | 需进入 Step 4 验证 |
| 4. 决策树 + 矩阵 | 首选 H1:`LCD_MIPI → W24 = W24-01`(Display 场景标配假设);但 33 天未解决说明 H1 不命中 → 回到 Step 3 重新枚举 → **H2:NFC 谐波**(NFC 载波 13.56 MHz × 177 ≈ 2400 MHz) | H2:NFC 共存干扰 |
| 5. 三要素结论 | 见下方 | — |
| 6. 后续动作 | 软件无效 → 硬件 PCB 改版 + 滤波网络 | 设计级硬件修改 |

---

## 三要素分析

| 要素 | 内容 |
|---|---|
| **干扰源** | NFC(Near Field Communication,载波 13.56 MHz) |
| **受扰体** | WiFi 2.4G(2412-2484 MHz,Display/Touch 场景下激活 NFC 工作) |
| **耦合路径** | **传导 + 辐射** —— NFC 天线/电路噪声经射频通路耦合到 WiFi 前端 |

---

## 排查过程

| 步骤 | 操作 | 结果 |
|:---:|---|---|
| 1 | 复现 Display 场景 2.4G 20 dB Desense | 稳定复现 |
| 2 | 假设 LCD MIPI 时钟谐波(H1)- 尝试软件规避 | **无改善**(~33 天消耗) |
| 3 | 重新枚举候选源:Display 场景激活的其他硬件(NFC / Touch / Display) | 识别 NFC 作为新假设 |
| 4 | 关闭 NFC 功能验证 | **干扰改善,H2 命中** |
| 5 | 频谱确认:NFC 13.56 MHz × 177 ≈ 2400 MHz | 高次谐波命中 |
| 6 | 硬件 PCB 改版 + 射频通路滤波网络 | 彻底解决 |

---

## 解决方案

### 硬件措施(最终方案)

1. **PCB 改版**:在 WiFi 2.4G 射频通路增加**滤波网络**,抑制 NFC 谐波进入 WiFi 前端
2. **布局**(若将来可调整):NFC 天线与 WiFi 天线最小距离约束

### 长期措施

1. **矩阵新增 NFC 源**:matrix.yaml 增加 NFC source + NFC→W24 映射(对应 SOP W24-08)
2. **Echo 方法论补充**:场景 Desense 排查时,"**同频段共存源**"应作为一个独立检查项,不应假设场景激活的唯一新源是"场景自身的时钟"
3. **设计查阅必查项新增**:Display/Touch 场景下的所有共存设备(NFC / Touch IC / Sensor 等)高次谐波与 WiFi 2.4G 的命中关系

---

## 架构启示

1. **33 天耗时的根因是假设锁死**:团队一开始默认"Display 场景恶化 = LCD MIPI 干扰",没有把 NFC(Display 场景下常态工作)作为平行假设枚举
2. **Echo 框架的修正**:`/diagnose` Step 4 决策树 + 矩阵应**同时输出多个候选假设**,而非锁定 H1;若 H1 3~5 天无进展应强制回到 Step 3 重新枚举
3. **共存源分类**:传统 matrix.yaml 按"时钟/电源/射频/显示/存储/摄像"分类,缺少"**共存类**"分类。本次反哺补上 NFC,未来可能还需补 Touch IC / UWB / 蓝牙 等

---

## 反哺 SOP

- **SOP-W24-08(NFC → WiFi 2.4G,新建)**:本案例将作为该 SOP 的唯一源案例,确立"关闭 NFC 验证"作为步骤 2.5 标配动作
- **SOP-W24-01(LCD_MIPI → W24)**:补充"若 H1 不命中,优先考虑共存类(NFC 等)"提示
- **Echo 方法论**:宽窄带判别文档新增"反例 3:场景激活带来放大效应"(已落地)

---

## 参考

- 原始案例汇总:[EMC-2024-Desense-triage.md](EMC-2024-Desense-triage.md#b2)
- SOP W24-08(新):[../sops/W24/W24-08.md](../sops/W24/W24-08.md)(本 Sprint 后生成 placeholder)
- 方法论:[../methodology/bandwidth-discrimination.md](../methodology/bandwidth-discrimination.md)
- 矩阵:[../matrix/matrix.yaml](../matrix/matrix.yaml) v2.1.0(新增 NFC 源)
