# Camera 领域知识

## 知识结构

```
camera/
├── overview.md              # Camera 基本工作原理
├── circuit-power.md         # Camera 电路与电源规格
├── mipi-dphy-cphy.md        # MIPI D-PHY / C-PHY 对比
├── mipi-frequency.md        # MIPI 频率计算公式
├── interference-sources.md  # Camera 干扰源 8 类
├── analysis-flow.md         # Camera Desense 分析思路
├── limits.md                # 干扰限值定义
└── README.md               # 本文件
```

## 核心认知

### 1. 信号流向特殊性
- **MIPI 方向相反**：Camera 是 Camera 发 MIPI 给 CPU，Display 是 CPU 发 MIPI
- **MCLK 来源**：CPU 提供 MCLK 给 Camera

### 2. 关键干扰源
- **最高优先级**：MIPI CSI 时钟/数据谐波
- **次优先级**：MCLK 谐波、AVDD 电源 SSN
- **辅助干扰**：VCM 驱动、Flash LED

### 3. 频率计算核心公式
```
MIPI Clock = Frame × Horizontal × Vertical × Pixel / Lane / 2
```

### 4. 内部限值差异
- **GPS**：≤ 3dB（强制要求）
- **其他制式**：≤ 4dB（内部要求）

## 与 Display 对比

| 维度 | Display | Camera |
|:---|:---|:---|
| MIPI 方向 | CPU → Display IC | Camera → CPU |
| 时钟来源 | Display IC 内部 OSC | CPU 提供 MCLK |
| 典型场景 | 亮屏常亮 | 预览/录像 |
| 内部限值 | ≤ 3dB | ≤ 4dB |

## 相关 SOP

- **GL1-02**：Camera MIPI → GNSS L1
- **W24-02**：Camera MIPI → WiFi 2.4G  
- **W5-02**：Camera MIPI → WiFi 5G
- **LLB-02**：Camera MIPI → LTE Low Band
- **LHB-02**：Camera MIPI → LTE High Band
- **GL5-02**：Camera MIPI → GNSS L5

## 排查流程要点

1. **软件优先**：先验证 MIPI SSC、频率调整
2. **频率计算**：确认谐波命中关系
3. **路径确认**：FPC/B2B 屏蔽接地是关键
4. **电源排查**：AVDD 纹波直接影响模拟性能

## 快速定位表

| 现象 | 最可能干扰源 |
|:---|:---|
| 分辨率/帧率变化 → 干扰变化 | MIPI 相关 |
| 固定频率干扰 | MCLK 谐波 |
| 对焦时加重 | VCM 驱动 |
| 闪光灯开启时干扰 | Flash LED |
| 前后摄差异明显 | 模组/FPC 布局问题 |