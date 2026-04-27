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

在 Claude Code 中打开本目录,使用以下 slash 命令:

1.  启动诊断流程:`/diagnose`
2.  查询矩阵表:`/matrix`
3.  临时调试:`/playground`
4.  生成报告:`/formal`

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
