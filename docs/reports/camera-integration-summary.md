# Camera 技术资料融合方案总结

## 一、融合概览

### 1.1 架构更新

```
┌─────────────────────────────────────────────────────────────────┐
│                    Echo·Desense 知识体系                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  第一层：方法论（已有）                                            │
│  - 三要素模型 / 软件优先 / 设计先查                                │
│  - 决策树 + 矩阵框架                                              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  第二层：领域知识                                                  │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐   │
│  │  Display 领域        │  │  Camera 领域（本次融合）          │   │
│  │  - LCD/OLED 原理     │  │                                 │   │
│  │  - TP 原理           │  │  1. Camera 基本工作原理           │   │
│  │  - 亮屏干扰源 10 类  │  │  2. Camera 电路与电源             │   │
│  │  - 分析思路          │  │  3. MIPI D-PHY / C-PHY 分类      │   │
│  └─────────────────────┘  │  4. MIPI 频率计算公式             │   │
│                           │  5. Camera 干扰定义与限值          │   │
│                           │  6. Camera 干扰源 8 类             │   │
│                           │  7. Camera Desense 分析思路        │   │
│                           └─────────────────────────────────┘   │
│                                                                 │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  更新后的 SOP（Camera 相关）                               │   │
│  │  - W24-02 / W5-02 / LLB-02 / LHB-02 / GL1-02 / GL5-02   │   │
│  │  - 增加 MCLK/CSI 频率计算、电源 SSN 噪声排查等步骤         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 新增文件统计

| 类别 | 新增文件数 | 更新文件数 | 总计 |
|:---|:---|:---|:---|
| Camera 领域知识 | 7 个 | - | 7 |
| SOP 文件 | 6 个 | - | 6 |
| 决策树 | - | 1 个 | 1 |
| 对比文档 | 1 个 | - | 1 |
| **总计** | **14 个** | **1 个** | **15** |

## 二、核心知识文件

### 2.1 Camera 领域知识

| 文件 | 核心内容 | 关键认知 |
|:---|:---|:---|
| `overview.md` | Camera 成像流程、关键组件 | MIPI 方向与 Display 相反 |
| `circuit-power.md` | 7 种电源规格、信号线列表 | AVDD 模拟敏感，MCLK 关键 |
| `mipi-dphy-cphy.md` | D-PHY/C-PHY 对比 | 干扰特性差异大 |
| `mipi-frequency.md` | 频率计算公式 | Packet Rate 决定频谱间隔 |
| `interference-sources.md` | 8 类干扰源 | 时钟谐波优先级最高 |
| `analysis-flow.md` | 标准排查流程 | 软件优先，硬件辅助 |
| `limits.md` | 干扰限值定义 | 内部要求 4dB（比亮屏宽松） |

### 2.2 新增 SOP 文件

| SOP 编号 | 组合 | 关键排查点 |
|:---|:---|:---|
| **GL1-02** | Camera → GNSS L1 | MCLK 65 次谐波命中 1575MHz |
| **W24-02** | Camera → WiFi 2.4G | MCLK 100 次谐波命中 2400MHz |
| **W5-02** | Camera → WiFi 5G | MCLK 214 次谐波命中 5136MHz |
| **LLB-02** | Camera → LTE LB | MCLK 29 次谐波命中 696MHz |
| **LHB-02** | Camera → LTE HB | MCLK 71 次谐波命中 1704MHz |
| **GL5-02** | Camera → GNSS L5 | MCLK 49 次谐波命中 1176MHz |

### 2.3 决策树更新

- **新增 Camera 专用分支**：包含干扰源定位流程
- **更新谐波计算表**：添加 Camera MCLK 基频（24-27MHz）
- **完善附录**：添加 Camera 干扰源速查表

## 三、技术要点总结

### 3.1 Camera 特殊认知

1. **信号流向特殊**：Camera MIPI 方向与 Display 相反
2. **时钟关键**：MCLK 是 Camera 所有时钟的源头
3. **电源敏感**：AVDD 对模拟性能影响大，纹波控制关键
4. **内部限值宽松**：4dB（亮屏要求 3dB）

### 3.2 与 Display 对比

| 维度 | Display | Camera |
|:---|:---|:---|
| MIPI 方向 | CPU → Display IC | Camera → CPU |
| 时钟来源 | DDIC 内部 OSC | CPU 提供 MCLK |
| 主要干扰源 | MIPI Clock、OSC | MIPI CSI Clock、MCLK |
| 典型场景 | 亮屏常亮 | 预览/录像 |
| 内部限值 | ≤ 3dB | ≤ 4dB |

### 3.3 排查优先级

1. **软件措施**：MIPI SSC、频率调整、降低帧率
2. **频率计算**：确认谐波命中关系
3. **硬件措施**：FPC 屏蔽、MCLK 滤波、AVDD 滤波
4. **结构措施**：天线拉远、吸波材

## 四、Echo 调用路由

### 4.1 关键词识别

当用户输入包含以下关键词时，自动路由到 Camera 知识：
- "Camera"、"摄像头"、"前摄"、"后摄"
- "预览"、"录像"、"拍照"
- "MIPI CSI"、"MCLK"、"AVDD"

### 4.2 决策流程

```
用户输入 Camera 问题
    │
    ├── 关键词识别 → Camera 相关
    │
    ├── 加载 Camera 领域知识
    │   ├── overview.md
    │   ├── circuit-power.md
    │   └── ...
    │
    ├── 匹配受扰频段
    │   ├── GNSS L1 → GL1-02
    │   ├── WiFi 2.4G → W24-02
    │   └── ...
    │
    └── 按 SOP 步骤引导排查
```

## 五、文件清单

### 5.1 新增文件

```
knowledge/domain/camera/
├── overview.md
├── circuit-power.md
├── mipi-dphy-cphy.md
├── mipi-frequency.md
├── interference-sources.md
├── analysis-flow.md
├── limits.md
└── README.md

knowledge/domain/
└── comparison-display-camera.md

knowledge/sops/
├── GL1/GL1-02.md
├── W24/W24-02.md
├── W5/W5-02.md
├── LLB/LLB-02.md
├── LHB/LHB-02.md
└── GL5/GL5-02.md

docs/
└── camera-integration-summary.md
```

### 5.2 更新文件

```
knowledge/
├── decision-tree.md（新增 Camera 分支）
└── domain/README.md（更新目录结构）
```

## 六、验证要点

### 6.1 知识完整性

- [x] Camera 工作原理覆盖完整
- [x] 电路与电源规格详细
- [x] MIPI 频率计算准确
- [x] 干扰源分类合理
- [x] SOP 步骤可执行

### 6.2 与现有框架集成

- [x] 决策树新增 Camera 分支
- [x] 矩阵框架覆盖 Camera 组合
- [x] 三要素模型适配 Camera
- [x] 软件优先原则保持一致

### 6.3 技术准确性

- [x] MIPI 方向认知正确
- [x] 频率计算公式准确
- [x] 干扰限值合理
- [x] 排查优先级合理

---

**融合完成状态**：✅ 已完成
**更新时间**：2026-04-22
**下一步**：验证实际案例分析效果