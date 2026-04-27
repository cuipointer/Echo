# 领域知识库

领域知识库包含各模块的深度技术知识，用于支撑三要素模型的分析和SOP的执行。

## 目录结构

```
knowledge/domain/
├── display/          # Display领域知识
│   ├── overview.md              # 屏幕工作原理总览
│   ├── lcd-power.md             # LCD电源规格
│   ├── oled-power.md            # OLED电源规格
│   ├── tp-basics.md             # TP工作原理
│   ├── interference-sources.md  # 10类亮屏干扰源
│   ├── analysis-flow.md         # 亮屏Desense分析思路
│   └── limits.md                # 干扰限值定义
├── camera/           # Camera领域知识
│   ├── overview.md              # Camera工作原理总览
│   ├── circuit-power.md         # Camera电路与电源规格
│   ├── mipi-dphy-cphy.md        # MIPI D-PHY/C-PHY对比
│   ├── mipi-frequency.md        # MIPI频率计算公式
│   ├── interference-sources.md  # 8类Camera干扰源
│   ├── analysis-flow.md         # Camera Desense分析思路
│   └── limits.md                 # 干扰限值定义
├── comparison-display-camera.md # Display与Camera对比
└── rse/              # RSE领域知识（预留）
```

## 使用方法

1. **问题分析阶段**：查阅相关领域知识，理解干扰源特性
2. **SOP执行阶段**：参考领域知识进行针对性排查
3. **方案制定阶段**：基于领域知识制定有效改善措施

## 知识更新流程

- 收集新的案例和经验
- 更新对应领域知识文件
- 同步更新相关SOP文件
- 验证知识有效性