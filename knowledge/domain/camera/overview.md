# Camera 基本工作原理

## 1. 成像流程

```
外界景物
    │
    ▼
Lens（镜头）→ 光学图像
    │
    ▼
IR Filter（红外滤波）
    │
    ▼
Sensor（图像传感器）→ 模拟电信号
    │
    ▼
A/D 转换 → 数字图像信号
    │
    ▼
CPU 处理
    │
    ▼
Display 显示
```

## 2. 关键组件

| 组件 | 功能 | 备注 |
|:---|:---|:---|
| **Lens** | 聚光成像 | 多片镜片组成 |
| **IR Filter** | 滤除红外光 | 保证色彩还原 |
| **Sensor** | 光电转换 | CMOS/CCD |
| **VCM** | 音圈马达，控制对焦 | Z 向微移 |
| **OIS Driver** | 光学防抖 | 水平微移补偿抖动 |
| **PCB/FPC** | 电气连接 | 传输电源和信号 |

## 3. 信号流向关键认知

- **MIPI 驱动端**：Camera 模组
- **MIPI 接收端**：CPU
- **MCLK 驱动端**：CPU
- **MCLK 接收端**：Camera 模组

> ⚠️ **与 Display 相反**：Display 是 CPU 发 MIPI，Camera 是 Camera 发 MIPI 给 CPU。