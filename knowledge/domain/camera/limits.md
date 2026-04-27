# Camera 干扰限值定义

## 定义

Camera Desense 主要指**前摄或后摄打开的状况下**相对于传导接收灵敏度的干扰值。

## 测试场景

| 场景 | 说明 |
|:---|:---|
| FC (Front Camera) | 前摄预览 |
| RC (Rear Camera) | 后摄预览 |
| Video | 录像模式（MIPI 持续传输） |

## 限值表

| 等级 | 限值 | 适用制式 |
|:---|:---|:---|
| Class 2 | ≤ 3dB | GPS（强制） |
| Class 3 | ≤ 6dB | WiFi / LTE（企标） |
| 研发内部 | ≤ 4dB | 所有制式 |

## 与亮屏限值对比

| 场景 | GPS 限值 | 其他制式 |
|:---|:---|:---|
| 亮屏 | ≤ 3dB | ≤ 3dB（内部） |
| Camera | ≤ 3dB | ≤ 4dB（内部） |

> Camera 内部要求略宽松于亮屏（4dB vs 3dB）。