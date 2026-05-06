---
description: 启动 Desense 问题诊断流程(三要素模型 + 决策树 + 宽窄带判别 v2.1)
argument-hint: <受扰频段> <测试场景> [现象描述]
---

# /diagnose

用户输入:`$ARGUMENTS`

**本命令是 Desense 诊断工作流的单一真相源**。`echo` agent 提供分析风格,`diagnose-desense` skill 负责触发识别,但实际流程和输出模板由本文件定义。

按以下 6 步完成标准化诊断,输出三要素结论 + 可疑 SOP 编号 + 可执行的零成本验证路径。

---

## Step 1. 解析参数

从 `$ARGUMENTS` 中提取:

| 字段 | 可选值 | 说明 |
|---|---|---|
| **受扰频段** | `W24` / `W5` / `LLB` / `LHB` / `GL1` / `GL5` | 见 [knowledge/methodology/three-elements.md](../../knowledge/methodology/three-elements.md) 受扰体清单 |
| **测试场景** | `normal` / `lcd` / `ddr` / `video` / `vib` / `fc` / `rc` | 对应前摄/后摄/录像/振动/充电等 |
| **现象描述** | 自由文本 | 如"灵敏度恶化 10 dB"、"全频段 ch1-13" |

参数缺失或歧义时:用一次性问题向用户索取,不强行推断。

## Step 2. Normal 优先检查

遵循 **Normal 优先原则**([knowledge/methodology/scene-priority.md](../../knowledge/methodology/scene-priority.md)):

- **未测 Normal** → 建议用户先做 Normal 基准测试,暂停诊断
- **Normal > 1 dB** → 告知"Normal 是基准线,需要先解决才能准确评估场景干扰",转入 Normal 排查(查 [knowledge/sops/NORMAL/](../../knowledge/sops/NORMAL/))
- **Normal ≤ 1 dB** → 计算`场景额外干扰 = 场景实测干扰 − Normal Desense`,继续 Step 3

## Step 3. 宽窄带判别(架构级筛选)

根据"现象描述"中的受扰带宽特征先做大类筛选,避免后续做无效分析。

**完整方法论**:[knowledge/methodology/bandwidth-discrimination.md](../../knowledge/methodology/bandwidth-discrimination.md) v1.0.0(自动判据 + 3 个反例 + 援引案例)

**自动判据速查**:

| 特征 | 判据 | ✓ 保留 | ✗ 排除 |
|---|---|---|---|
| 单频点 / 单信道 ≥ **10 dB** | 窄带谐波强命中 | 时钟类(OSC/MIPI/MCLK/DDR 高次谐波) | 宽带 EMI |
| 多信道平坦度差 ≥ **3 dB** | 宽带平台泄露 | 屏蔽不良 / 电源 SSN / Driver IC / FPC 辐射 | 窄带谐波 |
| 干扰频率随 MIPI 配置变化 | MIPI 相关 | LCD_MIPI / Camera_MIPI | 固定时钟源 |
| 场景激活即恶化,关闭即恢复 | 场景设备自身 / 共存 | 场景模块 / NFC / Speaker 等 | 常态辐射源 |
| 低频段主分集同步偏低 | 低频电源传导 | PMIC / Charger / 无线充电源 | 高频时钟 |

**反例提醒**:判据是启发式,可能误判的三种场景:
1. 多干扰源叠加(表面单频命中但有宽带底噪 → 用步骤 2.6 多源叠加排查法)
2. 密集谐波(形式宽带本质谐波 → 仍按窄带路径查)
3. 场景激活放大既有源(非激活了新源 → 关场景看恢复)

## Step 4. 决策树 + 矩阵查询

1. 读取 [knowledge/decision-tree.md](../../knowledge/decision-tree.md),按受扰频段 + 测试场景收敛到"干扰源大类"
2. 结合 Step 3 的带宽判别,**过滤**出符合特征的干扰源子类
3. 读取 [knowledge/matrix/matrix-table.md](../../knowledge/matrix/matrix-table.md),按"干扰源 × 受扰体"查 SOP 编号
4. 若矩阵声明 SOP 但文件不存在 → 明确告知用户"矩阵声明 SOP-XXX 但尚未落盘,建议参考模板 [_template.md](../../knowledge/sops/_template.md) 现场创建"
5. 若无对应组合 → 记录为新组合,建议补充矩阵和 SOP

## Step 5. 输出三要素结论

按以下模板输出(**本模板是所有 Desense 诊断输出的唯一格式**):

```markdown
## 诊断结果

### 问题信息
- 受扰频段:[频段]
- 测试场景:[场景]
- 干扰现象:[现象 + 带宽特征]
- Normal 基线:[≤1 dB ✓ / >1 dB ✗]

### 干扰特征判别
- 带宽类型:[宽带 / 窄带 / 随配置变化]
- 架构含义:[排除窄带谐波 / 排除宽带 EMI / 锁定 MIPI]

### 干扰源假设(按优先级排序)
| 优先级 | 假设 | 架构依据 | 验证方式 |
|:---:|---|---|---|
| H1 | [主假设] | [依据] | [零成本操作] |
| H2 | [次假设] | [依据] | [验证动作] |
| ... | | | |

### 受扰体分析
- 频段:[具体频段]
- 敏感度要求:[dBm 值]

### 耦合路径分析
- 主假设:[传导/辐射/串扰/地弹]
- 机制:[具体机制]

### SOP 编号
- 主推:[编号]:[组合描述]
- 备选:[编号]:[其他组合]

### 零成本验证路径(SOP-{受扰体}-{源}-xx 步骤 2.5 风格)
| 操作 | 预期现象 → 命中假设 |
|---|---|
| 关闭 [子功能 1] | 改善 → 锁定 H1 |
| 关闭 [子功能 2] | 改善 → 锁定 H2 |
| ... | |

### 下一步建议
1. [建议 1 — 通常是执行零成本验证]
2. [建议 2 — 若验证命中则进入 SOP 整改]
3. [建议 3 — 若未命中则扩展假设]
```

## Step 6. 后续动作路由

根据用户响应分发到相应能力模块:

- 用户同意执行 SOP → 调用 `sop-executor` skill 按编号引导排查
- 用户需要谐波命中计算 → 调用 `harmonic-calc` skill
- 排查完毕要写报告 → 建议 `/formal` 命令
- 发现新案例 → 引导用户在 `knowledge/cases/` 沉淀,并更新对应 SOP

---

## 四条工作原则(贯穿全流程)

| 原则 | 在哪一步生效 |
|---|---|
| **Normal 优先** | Step 2 强制检查 |
| **宽窄带判别** | Step 3 架构级筛选 |
| **软件优先** | Step 5 的"零成本验证路径"必须先于硬件整改 |
| **设计查阅** | Step 4 查阅相关 SOP 的"设计审查必查项"段 |

## 知识库依赖

| 文件 | 用途 |
|---|---|
| [knowledge/decision-tree.md](../../knowledge/decision-tree.md) | Step 4 大类收敛 |
| [knowledge/matrix/matrix-table.md](../../knowledge/matrix/matrix-table.md) | Step 4 SOP 编号查找 |
| [knowledge/sops/](../../knowledge/sops/) | Step 6 执行路由 |
| [knowledge/domain/](../../knowledge/domain/) | Step 3 带宽判别的领域依据(camera/display/normal) |
| [knowledge/cases/](../../knowledge/cases/) | Step 4 案例回溯,避免重复排查 |

---

## 参考:原 OpenCode CLI 参数(历史对照,已迁移)

| 原 CLI 参数 | 对应值 |
|---|---|
| `-f, --freq` | W24 / W5 / LLB / LHB / GL1 / GL5 |
| `-s, --scene` | normal / lcd / ddr / video / vib / fc / rc |
| `-d, --desc` | 自由文本 |

---

**版本**:v2.1(2026-05-06 更新,Step 3 引用 bandwidth-discrimination.md 方法论文档 + 自动判据速查表 + 反例提醒)

## 版本历史

| 版本 | 日期 | 更新 |
|---|---|---|
| v2.1 | 2026-05-06 | Step 3 宽窄带判别从表格升级到引用方法论文档 + 自动判据速查 + 反例提醒(EMC 2024 9 案例反哺) |
| v2.0 | 2026-04-27 | 架构审计后重写,新增 Step 3 宽窄带判别、假设优先级排序、零成本验证路径表;巩固单一真相源地位 |
