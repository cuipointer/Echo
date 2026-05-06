# 使用指南

## 快速开始

在 Claude Code 中打开本目录后,以下 slash 命令可用。

### 1. 启动诊断流程

```
/diagnose GL1 lcd 亮屏时 GNSS 灵敏度恶化
```

### 2. 查询矩阵表

```
/matrix LCD GL1
```

### 3. 临时调试

```
/playground
```

### 4. 生成报告

```
/formal debug logs/debug/DES-20260421-001.md
```

## 详细使用

### 诊断流程

#### 步骤 1：输入问题信息
- 受扰频段：WiFi 2.4G / WiFi 5G / LTE LB / LTE HB / GNSS L1 / GNSS L5
- 测试场景：Normal / LCD / DDR / VIDEO / VIB / FC / RC
- 干扰现象：描述灵敏度恶化情况

#### 步骤 2：执行决策树
根据受扰频段和测试场景，定位可疑干扰源。

#### 步骤 3：查询矩阵表
获取 (干扰源, 受扰体) 组合对应的 SOP 编号。

#### 步骤 4：执行 SOP
按标准化步骤执行排查，记录操作和结果。

#### 步骤 5：输出结论
生成三要素结论和改善措施。

### 矩阵表使用

#### 查询特定组合
```
/matrix LCD GL1
```

输出:
```
干扰源:LCD MIPI
受扰体:GNSS L1
SOP 编号:GL1-01
优先级:高
```

#### 查询完整矩阵
直接让 Claude 读取 `knowledge/matrix/matrix-table.md` 或在 `/matrix` 不带参数时输出完整概览。

### 工具脚本使用

#### 谐波计算
```bash
python3 tools/harmonic_calc.py <base_freq> <harmonic_order> <victim_start> <victim_end>
```

示例：
```bash
python3 tools/harmonic_calc.py 400 4 1561 1606
```

#### 链路预算
```bash
# 计算干扰裕量
python3 tools/link_budget.py margin <tx_power> <path_loss> <rx_sensitivity>

# 计算敏感度阈值
python3 tools/link_budget.py threshold <tx_power> <path_loss> <target_margin>
```

示例：
```bash
python3 tools/link_budget.py margin -30 80 -140
```

#### SOP 快速创建
```bash
./tools/new-sop.sh
```

按提示输入受扰体代码、干扰源代码和序号。

### 日志记录

#### 每日日志
编辑 `logs/daily/2026-04-21.md`，记录每日工作。

#### Debug 记录
编辑 `logs/debug/DES-20260421-001.md`，记录问题排查过程。

#### 周报
编辑 `logs/weekly/2026-04-21.md`，记录本周工作。

## 工作流程

### 标准排查流程

1. **问题输入**：收集受扰频段 + 测试场景
2. **宏观决策树**：从现象收敛到"干扰源类别"
3. **矩阵框架**：将组合映射到标准 SOP 编号
4. **SOP 执行**：按标准化步骤完成排查
5. **输出结论**：三要素结论 + 改善措施

### 三要素分析

#### 干扰源 (Source)
- 谁在产生噪声？
- 措施方向：展频 / 降频 / 关断
- 优先级：1（最有效）

#### 受扰体 (Victim)
- 哪个频段被干扰？
- 措施方向：滤波 / 避开频率 / 提高容限
- 优先级：3（最后手段）

#### 耦合路径 (Path)
- 怎么传过去的？
- 措施方向：屏蔽 / 隔离 / 接地
- 优先级：2

## 案例分析

### 案例 1：GNSS L1 受 LCD MIPI 干扰

#### 问题描述
- 受扰频段：GNSS L1 (1561-1606 MHz)
- 测试场景：亮屏常亮
- 干扰现象：灵敏度恶化 10dB

#### 排查过程
1. 使用决策树定位：亮屏 → LCD MIPI
2. 查询矩阵表：SOP-GL1-01
3. 执行 SOP：
   - 确认干扰源：LCD MIPI，基频 400MHz
   - 频率验证：400MHz × 4 = 1600MHz 命中 GNSS L1
   - 软件规避：SSC 展频，改善 3dB
   - 硬件整改：屏蔽罩接地优化，改善 8dB

#### 结论
- 干扰源：LCD MIPI，基频 400MHz
- 受扰体：GNSS L1，敏感度 -140dBm
- 耦合路径：辐射，空间电磁场耦合
- 改善措施：SSC + 屏蔽罩接地，总改善 11dB

## 常见问题

### Q: 如何确定干扰源？
A: 使用决策树根据受扰频段和测试场景定位。

### Q: 如何获取 SOP 编号？
A: 查询矩阵表，输入干扰源和受扰体。

### Q: 如何执行 SOP？
A: 按 SOP 文档的标准化步骤执行。

### Q: 如何记录排查过程？
A: 编辑 `logs/debug/` 目录下的 Debug 记录文件。

### Q: 如何生成报告?
A: 使用 `/formal` 命令生成正式报告。
