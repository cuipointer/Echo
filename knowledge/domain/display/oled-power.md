# OLED 电源规格

| 电源名称 | 用途 | 常见电压 | 常见电流 | 噪声风险 |
|:---|:---|:---|:---|:---|
| **AVDD (VCLIN)** | Panel Gate Driver | 7.6V | ~15mA | 中 |
| **DVDD (VDDI)** | DDIC 数字电路供电 | 1.8V | 30-35mA | 低 |
| **VCI** | DC-DC Booster 输入 | 3V | 3-4mA | 低 |
| **ELVDD** | OLED 正极 | 4.6V | **~180mA** | **高（大电流开关）** |
| **ELVSS** | OLED 负极 | -3.1V | **~180mA** | **高（大电流开关）** |

## 排查要点

- ELVDD/ELVSS 电流大（~180mA），DC-DC 开关噪声强
- 关注 DC-DC 开关频率及其谐波
- OLED 无背光，但 ELVDD/ELVSS 是主要噪声源
- AMOLED Driver IC 与 TFT-LCD 功能相似，但有独立 RGB Gamma 发生器