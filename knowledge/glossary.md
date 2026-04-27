# 术语词典

**版本**:v1.0.0
**更新日期**:2026-04-27

> 本文件是 Echo·Desense 项目术语的**单一真相源**。SOP / 文档中的术语定义应引用本文件,不再重复定义。

---

## 核心概念

| 术语 | 中文 | 定义 |
|---|---|---|
| **Desense** | 灵敏度恶化 | De-sensitization。接收机灵敏度相对基准的恶化程度(dB)。 |
| **Normal Desense** | 基准灵敏度恶化 | 无特定场景激活时的 Desense 基线,必须先确认 ≤ 1 dB 才能进入场景诊断。 |
| **三要素模型** | Source / Victim / Path | 所有 Desense 问题的分析框架:干扰源 + 受扰体 + 耦合路径。 |
| **SOP** | 标准作业程序 | Standard Operating Procedure。针对特定(干扰源, 受扰体)组合的标准化排查步骤。 |

---

## 干扰源相关

| 术语 | 含义 | 补充 |
|---|---|---|
| **MIPI** | Mobile Industry Processor Interface | 移动设备处理器接口,分为 DSI(显示)和 CSI(摄像) |
| **D-PHY / C-PHY** | MIPI 物理层 | D-PHY 是差分信号,C-PHY 是三线差分(见 [camera/mipi-dphy-cphy.md](domain/camera/mipi-dphy-cphy.md)) |
| **CSI** | Camera Serial Interface | MIPI 摄像模组接口 |
| **DSI** | Display Serial Interface | MIPI 显示接口 |
| **MCLK** | Master Clock | 摄像模组主时钟(24 / 27 MHz 典型) |
| **DDR** | Double Data Rate | 内存接口,时钟 200-933 MHz |
| **PMIC** | Power Management IC | 电源管理芯片,含多路 DCDC(1-4 MHz 开关频率) |
| **VCM** | Voice Coil Motor | 音圈马达,用于 AF 驱动 |
| **OIS** | Optical Image Stabilization | 光学防抖,由 Driver IC 驱动 |
| **AF** | Auto Focus | 自动对焦,由 VCM 驱动 |
| **Buck / Boost** | DCDC 拓扑 | Buck 降压 / Boost 升压开关变换器 |
| **SSN** | Simultaneous Switching Noise | 同步开关噪声,多 I/O 同时切换引起 |
| **Class-D** | 数字功放 | 扬声器 PA 的数字功放拓扑,开关频率 300-600 kHz |

---

## 受扰体相关

| 术语 | 含义 | 频率 |
|---|---|---|
| **WiFi 2.4G** | IEEE 802.11 b/g/n | 2412-2484 MHz |
| **WiFi 5G** | IEEE 802.11 a/n/ac/ax | 5150-5850 MHz |
| **LTE LB** | LTE 低频段 | 700-960 MHz(B5/8/12/20/26/28) |
| **LTE HB** | LTE 高频段 | 2300-3700 MHz(B7/40/41/42/48) |
| **GNSS L1** | 全球导航卫星 L1 | 1561-1606 MHz(GPS/BDS/GLONASS) |
| **GNSS L5** | 全球导航卫星 L5 | 1176 MHz(GPS L5 / BDS B2a) |
| **RSSI** | Received Signal Strength Indication | 接收信号强度指示 |
| **PER** | Packet Error Rate | 包错误率 |
| **Throughput** | 吞吐量 | 数据传输速率 |

---

## 耦合路径相关

| 术语 | 含义 | 典型改善措施 |
|---|---|---|
| **传导耦合** | 通过 PCB 走线/电源平面传播 | 滤波 / 隔离 / 分割电源 |
| **辐射耦合** | 通过空间电磁场传播 | 屏蔽 / 拉远距离 / 吸波材料 |
| **串扰** | 通过相邻走线耦合 | 包地 / 增加间距 / 差分走线 |
| **地弹** | 通过公共地阻抗耦合 | 分割地 / 加强接地 / 星型接地 |
| **共模噪声** | Common Mode Noise | 共模滤波器抑制 |
| **PIM** | Passive Intermodulation | 无源互调,非线性器件/接触产生 |

---

## 排查措施相关

| 术语 | 含义 | 适用 |
|---|---|---|
| **SSC** | Spread Spectrum Clocking | 展频时钟,通过频率调制降低离散谐波功率 |
| **SSC 调制深度** | 频率摆动幅度 | 典型 1-2%,深度越大抑制效果越好但需验证兼容性 |
| **滤波** | Filtering | 串磁珠 / 并电容 / π 型网络 / 共模扼流圈 |
| **屏蔽罩** | Shielding Can | 金属屏蔽盒,降低辐射 |
| **包地** | Ground Shielding | 敏感走线周围包围地走线 |
| **多点接地** | Multi-point Grounding | FPC / 屏蔽罩多处接地降低阻抗 |

---

## 流程与方法论

| 术语 | 含义 | 参考 |
|---|---|---|
| **Normal 优先原则** | 场景诊断前先解决 Normal | [methodology/scene-priority.md](methodology/scene-priority.md) |
| **软件优先原则** | 拆机前穷尽软件措施 | [methodology/software-first.md](methodology/software-first.md) |
| **设计查阅原则** | 分析前先查设计资料 | [methodology/design-review.md](methodology/design-review.md) |
| **宽窄带判别** | 根据受扰带宽筛选干扰源大类 | /diagnose Step 3 |
| **零成本验证** | 纯软件操作的排查步骤 | SOP 步骤 2.5 |
| **步骤 2.5** | 模组子功能逐项排查 | 见 [sops/W24/W24-02.md](sops/W24/W24-02.md) |
| **三要素结论** | 标准输出格式 | /diagnose Step 5 / [methodology/three-elements.md](methodology/three-elements.md) |

---

## 限值与标准

| 标准 | 限值 | 适用 |
|---|---|---|
| Class 2 | ≤ 3 dB | GPS 要求 |
| Class 3 | ≤ 6 dB | 其他制式(企标) |
| 研发内部 | ≤ 4 dB | 所有频段 |

---

## 使用约定

- **SOP 和文档附录中的"术语表"**应仅列出该文档特有的术语;通用术语链接到本文件
- **新术语**:若要新增,先在本文件添加定义,再在其他文档中使用
- **缩写展开**:首次出现时用"全称(缩写)"格式,后续直接用缩写
