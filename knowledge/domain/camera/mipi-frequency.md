# Camera MIPI 频率计算公式

## 1. 核心公式

| 公式 | 表达式 | 单位 |
|:---|:---|:---|
| **MIPI Data Rate** | Frame × Horizontal × Vertical × Pixel / Lane | bit/s |
| **MIPI Clock** | Frame × Horizontal × Vertical × Pixel / Lane / 2 | Hz |
| **Pixel Rate** | Frame × Horizontal × Vertical / Lane | pixel/s |
| **Packet Rate** | Frame × Horizontal × Vertical × Pixel / Lane / packet_size | packet/s |

## 2. 频谱特性关键认知

> **MIPI 传输数据时以 1 个 Packet 为单位，Packet Rate 决定了 MIPI 频谱的尖峰间隔。**

- Packet 所占位数由 Pixel 位数和传输格式决定
- 频谱表现为以 Packet Rate 为间隔的离散谱线
- 谐波可能落入任意射频频段

## 3. 频率计算示例

| 参数 | 典型值 |
|:---|:---|
| 分辨率 | 1920 × 1080 |
| 帧率 | 30 fps |
| Pixel 深度 | 10 bit |
| Lane 数 | 4 |

```
MIPI Clock = 30 × 1920 × 1080 × 10 / 4 / 2
           = 30 × 2,073,600 × 10 / 8
           = 77,760,000 Hz ≈ 77.76 MHz
```

**谐波风险**：
- 77.76 MHz × 20 = 1555.2 MHz（接近 GPS L1）
- 77.76 MHz × 31 = 2410.56 MHz（落入 WiFi 2.4G）

## 4. 摄像头频率树

Camera 内部时钟路径：
```
MCLK (外部输入)
    │
    ▼
PLL → 各模块时钟
    │
    ├── ADC Clock
    ├── Pipeline Clock
    ├── FIFO Clock
    └── MIPI Serializer Clock → CSI Clock/Data
```

> 多个分频/倍频路径，产生丰富的谐波组合。