# Display 领域知识

## 知识结构

```
display/
├── overview.md              # Display 基本工作原理
├── lcd-power.md             # LCD 电源规格
├── oled-power.md            # OLED 电源规格
├── tp-basics.md             # TP 工作原理
├── interference-sources.md  # Display 干扰源 10 类
├── analysis-flow.md         # Display Desense 分析思路
├── limits.md                # 干扰限值定义
└── README.md               # 本文件
```

## 核心认知

### 1. 信号流向特性
- **MIPI 方向**：CPU → Display IC（与 Camera 相反）
- **时钟来源**：Display IC 内部 OSC 或外部时钟
- **数据流向**：图像数据从 CPU 传输到显示面板

### 2. 关键干扰源
- **最高优先级**：MIPI DSI Clock、内部 OSC 谐波
- **次优先级**：背光 PWM、TP 驱动噪声
- **电源相关**：ELVDD/ELVSS（OLED）、VSP/VSN（LCD）

### 3. 频率计算核心
```
MIPI Clock = Frame × Horizontal × Vertical × Pixel / Lane / 2
背光 PWM 频率 = 典型值 10-50kHz
TP 驱动频率 = 典型值 100-400kHz
```

### 4. 内部限值标准
- **GPS**：≤ 3dB（强制要求）
- **其他制式**：≤ 3dB（内部要求，比 Camera 严格）

## 与 Camera 对比

| 维度 | Display | Camera |
|:---|:---|:---|
| MIPI 方向 | CPU → Display IC | Camera → CPU |
| 时钟来源 | Display IC 内部 OSC | CPU 提供 MCLK |
| 典型场景 | 亮屏常亮 | 预览/录像 |
| 内部限值 | ≤ 3dB | ≤ 4dB |
| 主要干扰 | MIPI Clock、OSC | MIPI CSI Clock、MCLK |

## 相关 SOP

- **GL1-01**：Display MIPI → GNSS L1
- **W24-01**：Display MIPI → WiFi 2.4G  
- **W5-01**：Display MIPI → WiFi 5G
- **LLB-01**：Display MIPI → LTE Low Band
- **LHB-01**：Display MIPI → LTE High Band
- **GL5-01**：Display MIPI → GNSS L5

## 排查流程要点

1. **软件优先**：先验证灭屏测试确认 Display 相关
2. **干扰源定位**：亮度调节区分背光，TP开关区分触摸
3. **频率分析**：谐波计算验证命中关系
4. **路径确认**：FPC屏蔽和接地是关键

## 快速定位表

| 现象 | 最可能干扰源 |
|:---|:---|
| 灭屏干扰消失 | Display 相关确认 |
| 亮度变化干扰变化 | 背光 PWM 相关 |
| TP开关干扰变化 | 触摸驱动相关 |
| 固定频率干扰 | MIPI Clock 或 OSC 谐波 |
| 分辨率变化干扰变化 | MIPI 数据速率相关 |

## 技术特性差异

### LCD vs OLED
- **LCD**：背光系统（WLED）、液晶驱动、需要 VSP/VSN
- **OLED**：自发光、像素级控制、需要 ELVDD/ELVSS

### 干扰特性差异
- **LCD**：背光 PWM 是主要低频干扰源
- **OLED**：MIPI Clock 和内部 OSC 是主要干扰源
- **TP**：驱动频率和扫描方式影响干扰特性

## 设计审查要点

1. **MIPI 时钟规划**：避免谐波密集区，预留 SSC
2. **电源滤波设计**：背光/LCD/OLED 电源滤波充足
3. **屏蔽接地**：FPC 全程屏蔽，多点接地
4. **布局优化**：天线与显示区域足够距离
5. **TP 频率规划**：避免 Tx 频率谐波风险

## 典型案例模式

### 模式 1：亮屏 GPS 干扰
- **现象**：亮屏时 GPS 定位漂移
- **原因**：MIPI Clock 20次谐波命中 L1 频段
- **解决**：开启 SSC 或调整 MIPI 频率

### 模式 2：亮度调节 WiFi 干扰
- **现象**：亮度变化时 WiFi 性能波动
- **原因**：背光 PWM 高次谐波影响
- **解决**：优化背光频率或滤波

---

**最后更新**：2026-04-22  
**维护者**：Echo架构团队