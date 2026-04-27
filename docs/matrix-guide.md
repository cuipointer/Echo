# 矩阵使用指南

## 矩阵简介

矩阵表用于快速定位 (干扰源, 受扰体) 组合对应的 SOP 编号。

## 矩阵结构

### 干扰源 ↓ \ 受扰体 →

| 干扰源 | WiFi 2.4G | WiFi 5G | LTE LB | LTE HB | GNSS L1 | GNSS L5 |
|--------|-----------|---------|--------|--------|---------|---------|
| **LCD MIPI** | W24-01 | W5-01 | LLB-01 | LHB-01 | **GL1-01** | GL5-01 |
| **Camera MIPI** | W24-02 | W5-02 | LLB-02 | LHB-02 | GL1-02 | GL5-02 |
| **DDR** | W24-03 | W5-03 | LLB-03 | LHB-03 | GL1-03 | GL5-03 |
| **PMIC Buck** | W24-04 | — | **LLB-04** | — | GL1-04 | GL5-04 |
| **VIB Motor** | — | — | LLB-05 | — | **GL1-05** | — |
| **Speaker PA** | W24-05 | — | LLB-06 | — | GL1-06 | — |
| **Charger** | W24-06 | — | **LLB-07** | — | GL1-07 | — |
| **USB 3.0** | W24-07 | **W5-04** | — | **LHB-04** | — | — |

**标注**：
- **加粗** = 高频问题，优先编写 SOP
- `—` = 频率域无直接交叠（仍需检查谐波）

## SOP 编号规则

### 格式：`{受扰体}-{干扰源}-{序号}`

- **受扰体**：2 字母代码
  - W24: WiFi 2.4G
  - W5: WiFi 5G
  - LLB: LTE LB
  - LHB: LTE HB
  - GL1: GNSS L1
  - GL5: GNSS L5

- **干扰源**：2 字母代码
  - LC: LCD MIPI
  - CA: Camera MIPI
  - DD: DDR
  - PM: PMIC Buck
  - VB: VIB Motor
  - SP: Speaker PA
  - CH: Charger
  - U3: USB 3.0

- **序号**：2 位数字（01-99）

### 示例
- **W24-01**: WiFi 2.4G 受 LCD MIPI 干扰
- **GL1-01**: GNSS L1 受 LCD MIPI 干扰
- **LLB-04**: LTE LB 受 PMIC Buck 干扰

## 使用方法

### 1. 定位组合
- 确定受扰体频段
- 确定干扰源模块
- 查找矩阵表对应位置

### 2. 获取 SOP 编号
- 读取矩阵表中的 SOP 编号
- 如为 `—`，检查谐波命中
- 如为加粗，优先排查

### 3. 执行 SOP
- 按 SOP 编号查找文档
- 按标准化步骤执行
- 记录排查结果

### 4. 更新矩阵
- 如发现新组合，记录并反馈
- 如 SOP 过时，更新矩阵表
- 持续优化矩阵结构

## 查询工具

### Slash 命令查询
```
/matrix LCD GL1
```

### 手动查询
1. 打开 `knowledge/matrix/matrix-table.md`
2. 查找干扰源行
3. 查找受扰体列
4. 读取 SOP 编号

## 高频问题

### P0 高频问题（优先编写 SOP）

| 序号 | SOP 编号 | 组合 | 原因 |
|------|----------|------|------|
| 1 | SOP-GL1-01 | LCD MIPI → GNSS L1 | 谐波命中概率极高 |
| 2 | SOP-W24-01 | LCD MIPI → WiFi 2.4G | 最常见干扰组合 |
| 3 | SOP-LLB-04 | PMIC → LTE LB | 低频开关噪声直接命中 |
| 4 | SOP-GL1-05 | VIB Motor → GNSS L1 | 马达 PWM 谐波密集 |
| 5 | SOP-W5-04 | USB 3.0 → WiFi 5G | 5Gbps 信号直接干扰 |

### P1 中频问题（后续补充）

| 序号 | SOP 编号 | 组合 | 原因 |
|------|----------|------|------|
| 6 | SOP-W24-02 | Camera MIPI → WiFi 2.4G | 相机场景常见 |
| 7 | SOP-LLB-07 | Charger → LTE LB | 充电场景干扰 |
| 8 | SOP-GL1-02 | Camera MIPI → GNSS L1 | 录像场景干扰 |
| 9 | SOP-W24-03 | DDR → WiFi 2.4G | 下载/跑分干扰 |
| 10 | SOP-LHB-04 | USB 3.0 → LTE HB | 高频段干扰 |

## 矩阵优化

### 持续更新
- 收集新问题案例
- 更新矩阵表结构
- 优化 SOP 编号

### 经验固化
- 走通一次决策树 → 沉淀为矩阵中的一个格子
- SOP 执行结果 → 反馈优化矩阵
- 形成闭环优化

## 常见问题

### Q: 如何查询 SOP 编号?
A: 使用 `/matrix` slash 命令或手动查询矩阵表。

### Q: 矩阵表中 `—` 表示什么？
A: 表示频率域无直接交叠，但仍需检查谐波命中。

### Q: 如何更新矩阵表？
A: 编辑 `knowledge/matrix/matrix-table.md`，提交 PR。

### Q: 如何发现新组合？
A: 记录排查过程中的新组合，反馈到项目。

## 参考文档

- `knowledge/matrix/matrix-table.md`：矩阵表
- `knowledge/matrix/source-list.md`：干扰源清单
- `knowledge/matrix/victim-list.md`：受扰体清单
- `knowledge/decision-tree.md`：决策树
