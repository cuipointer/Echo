---
name: engineering-logger
description: 工程开发过程记录。任务完成后把工作摘要追加到 logs/daily/YYYY-MM-DD.md,可选提交到 Git。触发:用户完成一项具体任务(写代码/文档/执行 SOP/做分析)、用户明确要求记录日志、用户输入 "记录日志" 或 /log。
metadata:
  audience: developers
  workflow: software-development
  category: productivity
---

# engineering-logger

## 职责

把当天完成的工作事项追加到 `logs/daily/YYYY-MM-DD.md`,便于后续回溯和周报汇总。

## 实现绑定(重要)

本 skill **调用 `tools/logger.py` 的 Python 实现**作为主路径。`tools/git-logger.sh` 是 Python 实现的 git 提交辅助脚本(可在 CI 或交互式命令行中独立使用,本 skill 不直接调用)。

| 调用路径 | 实现 | 责任 |
|---|---|---|
| **主路径**(本 skill) | `tools/logger.py` | 读/写/追加 daily 日志;调用 git 子进程或由 Claude 直接 Bash git 命令 |
| 辅助路径 | `tools/git-logger.sh` | 命令行独立使用(非 skill 场景),带彩色输出 |

如需改变实现,以本 skill 为单一真相源。

## 触发条件

满足以下任一:

1. 用户刚完成一项具体任务(代码提交、SOP 编写、案例沉淀、架构变更)
2. 用户明确要求"记录日志"、"更新日志"、"写个工作总结"
3. 用户输入 `/log` 或 `/git-log`

## 执行步骤

### 1. 定位日志文件

- 路径:`logs/daily/YYYY-MM-DD.md`(YYYY-MM-DD 为今天日期)
- 若不存在:从 `logs/templates/daily-template.md` 创建

### 2. 追加「今日活动」表

一条任务一行,格式:

```markdown
| HH:MM | 模块 | 活动摘要 | 状态 |
```

字段说明:

- **HH:MM**:24h 格式当前时间
- **模块**:任务所属模块(Desense 分析 / SOP 系统 / 工具开发 / 知识库 / 架构 / 案例库 / Git 管理)
- **活动摘要**:一句话描述完成的工作,附带关键结果(改善 N dB / 新增 N 文件 / 修复 N bug 等)
- **状态**:✅ 完成

### 3. 追加「详细记录」(复杂任务)

复杂任务(如 SOP 编写、架构变更、问题排查闭环)在`## 详细记录`章节追加:

```markdown
### [HH:MM] 活动标题

- **模块**:模块名称
- **任务**:具体做了什么
- **关键产出**:创建/修改的文件(带路径)
- **备注**:需要注意的事项(可选)
```

### 4. Git 提交(视分支决策)

**分支策略**:

| 分支 | 策略 |
|---|---|
| `main` / `master` | 允许提交,但要求提交消息明确 |
| `echo-dev` | 允许自动提交(历史 Echo 习惯) |
| 其他分支 | 建议,让用户确认 |

提交消息格式:

```
docs: 更新日志 - YYYY-MM-DD <简要概括>
```

不再对主分支设硬性禁止(当前仓库主分支就是 `main`),由用户最终决定。

## 追加规则

1. **只追加,不覆盖**:已有内容不修改,只在末尾追加
2. **一条任务一条记录**:不合并
3. **简洁摘要**:每条 ≤ 2 行
4. **文件路径要带**:涉及文件时写出路径(相对仓库根)

## 示例

### 追加表格
```
| 14:30 | SOP 系统 | 创建 W24-02 v2.1,新增步骤 2.5 OIS 排查 | ✅ 完成 |
| 15:00 | 工具开发 | harmonic_calc.py 增加批量计算 | ✅ 完成 |
```

### 追加详细
```markdown
### [14:30] AS2 后摄 Wide WiFi 2.4G Desense 排查

- **模块**:Desense 分析 / SOP 系统
- **任务**:排查 AS2 RC 场景 WiFi 2.4G 全频段 4~7 dB,定位到 OIS Driver IC
- **关键产出**:
  - `knowledge/sops/W24/W24-02.md` v2.0 → v2.1(新增步骤 2.5)
  - `knowledge/cases/AS2-RC-WiFi24-OIS.md` 新建案例
- **经验教训**:子功能排查应前置于时钟/电源排查(零成本)
```

## 与其他模块的关系

| 模块 | 关系 |
|---|---|
| `tools/logger.py` | **主实现**,本 skill 的代码入口 |
| `tools/git-logger.sh` | 独立 CLI,不由 skill 调用 |
| `/diagnose` 命令 | 诊断完成后可触发本 skill 记录 |
| `/formal` 命令 | 生成正式报告后可触发本 skill 记录 |

## 设计备注

- v1(Echo 版)硬编码"仅 echo-dev 分支自动提交"。Claude Code 版(2026-04-27)放宽:允许 main/主分支提交,但由用户最终确认
- v1 未明确实现绑定(Python 还是 bash)。Claude Code 版明确:**主路径用 Python**,bash 工具仅供交互式独立使用

---

**版本**:v2.0(2026-04-27 架构审计后)
