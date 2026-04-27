# Display 与 Camera 干扰特性对比

| 维度 | Display | Camera |
|:---|:---|:---|
| **MIPI 方向** | CPU → Display IC | Camera → CPU |
| **时钟来源** | Display IC 内部 OSC | CPU 提供 MCLK |
| **主要时钟** | MIPI DSI Clock、OSC | MIPI CSI Clock、MCLK |
| **电源特点** | ELVDD/ELVSS 大电流 | AVDD 模拟敏感 |
| **典型场景** | 亮屏常亮 | 预览/录像 |
| **内部限值** | ≤ 3dB | ≤ 4dB |
| **最高频干扰** | MIPI 谐波、OSC 谐波 | MIPI 谐波、MCLK 谐波 |

## 排查优先级差异

| 场景 | Display 优先查 | Camera 优先查 |
|:---|:---|:---|
| 固定频率干扰 | OSC | MCLK |
| 随内容变化 | MIPI 时钟 | MIPI 时钟 |
| 随亮度变化 | 背光 PWM | — |
| 对焦时 | — | VCM |
| 触摸时 | TP | — |