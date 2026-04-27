# 屏幕工作原理总览

## 1. 屏幕类型对比

| 类型 | 发光原理 | 背光需求 | 典型噪声 |
|:---|:---|:---|:---|
| **LCD** | 背光白光 + 滤光片 | 需要 LED 背光 | PWM 调光噪声、MIPI 时钟 |
| **OLED** | 自发光 RGB | 无需背光 | ELVDD/ELVSS 电源噪声、MIPI 时钟 |

## 2. 系统架构

```
CPU (MIPI 驱动端)
    │
    │ MIPI DSI (时钟 + 数据)
    ▼
Display Driver IC (MIPI 接收端)
    │
    ├── Source Driver → 灰度图像信息
    ├── Gate Driver → 逐行扫描控制
    ├── DC-DC Converter → 产生各级电压
    └── 内部 OSC → 产生所有 CLK
```

## 3. 关键认知

- **Display 所有 CLK 由内部晶振产生**
- **MIPI 驱动端为 CPU，Display 为接收端**
- **干扰可通过 MIPI 线缆传导或空间辐射**

## 4. 信号流向

```
CPU → MIPI 接口 → Display IC → RGB 数据 → Source Driver → 灰度图像
                              → Gate Driver → 逐行扫描
```