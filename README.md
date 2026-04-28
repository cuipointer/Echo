# Echo·Desense

基于三要素模型和矩阵框架的 Desense 分析助手

## 项目目标

建立 Desense 问题的标准化 Debug 流程系统，实现快速定位和解决问题。

## 核心方法论

### 三要素模型

所有 Desense 问题必须从三个维度分析：

1.  **干扰源 (Source)**：谁在产生噪声？
2.  **受扰体 (Victim)**：哪个频段被干扰？
3.  **耦合路径 (Path)**：怎么传过去的？

### 工作原则

1.  **软件优先**：拆机前验证所有软件措施
2.  **设计查阅**：分析前先查阅设计资料

## 快速开始

### 安装

```bash
./install.sh
```

### 使用

**启动方式**:在 Claude Code 中**以本目录为工作目录**启动(命令行:`cd` 到本目录再跑 `claude`;VSCode 扩展:File → Open Folder 指向本目录再打开 Claude Code)。Claude Code 启动时从当前工作目录的 `.claude/` 读取配置,因此**改完 `.claude/` 下文件后需要重启 Claude Code 会话**才能生效。

启动后可用以下 slash 命令(输入 `/` 会看到自动补全):

| 命令 | 用途 | 示例 |
|---|---|---|
| `/diagnose <频段> <场景> [描述]` | 启动诊断流程(三要素 + 决策树 + 宽窄带判别) | `/diagnose W24 rc AS2 全频段 4~7dB` |
| `/matrix <干扰源> <受扰体>` | 查矩阵表定位 SOP 编号 | `/matrix Camera_MIPI W24` |
| `/playground [会话名]` | 进入临时调试缓冲区 | `/playground ais2-test` |
| `/formal [debug\|weekly\|summary]` | 生成正式报告 | `/formal debug` |

配套 skill(由 Claude 在识别到需求时自动触发):

- `diagnose-desense` — 自然语言识别 Desense 问题 → 转交 `/diagnose`
- `harmonic-calc` — 谐波命中计算
- `sop-executor` — 按 SOP 编号引导现场排查
- `engineering-logger` — 任务完成后记录日志

完整能力结构见 [CLAUDE.md](CLAUDE.md)。

### 故障排除

**Q: 在 Claude Code 里 `/diagnose` 等命令不出现 / 不可用**

1. 确认工作目录是本仓库根:`pwd` 应为 `.../workspace-claude`
2. 确认 `.claude/commands/` 下有 `diagnose.md / matrix.md / formal.md / playground.md`
3. 若刚 git clone 或刚修改这些文件,**重启 Claude Code 会话**(退出后重新进入)
4. 运行 `python3 tools/check-architecture-consistency.py` 验证 harness 完整性

## 目录结构

- `.claude/` - Claude Code 能力模块(agents / commands / skills)
- `knowledge/` - 知识库（方法论、矩阵、SOP、案例）
- `tools/` - 工具脚本
- `docs/` - 使用文档
- `logs/` - 工作日志（不纳入 Git）
- `playground/` - 临时缓冲区（不纳入 Git）

## 开发计划

详见 [开发计划](docs/development-plan.md)

## 许可证

MIT License
