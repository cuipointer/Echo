#!/bin/bash

# Echo·Desense (Claude Code 版) 安装脚本

set -e

echo "========================================"
echo "Echo·Desense 安装脚本 (Claude Code)"
echo "========================================"

# 检查运行目录
if [ ! -f "CLAUDE.md" ]; then
    echo "错误:请在项目根目录(包含 CLAUDE.md)运行此脚本"
    exit 1
fi

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "错误:未安装 Git"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误:未安装 Python3"
    exit 1
fi

# 可选:检查 Claude Code CLI(不强制)
if command -v claude &> /dev/null; then
    echo "检测到 Claude Code CLI: $(claude --version 2>/dev/null || echo '版本未知')"
else
    echo "提示:未检测到 Claude Code CLI,如需交互使用请安装"
fi

# 设置脚本权限
echo "设置脚本权限..."
chmod +x tools/*.sh 2>/dev/null || true
chmod +x tools/*.py 2>/dev/null || true

# 创建 CHANGELOG.md(若不存在)
if [ ! -f "CHANGELOG.md" ]; then
    echo "创建 CHANGELOG.md..."
    cat > CHANGELOG.md << 'EOF'
# Changelog

## v1.0.0 (Claude Code 版)

### Added
- 从 OpenCode 工作区适配到 Claude Code 环境
- `.claude/agents/echo.md` — echo subagent
- `.claude/commands/{diagnose,matrix,playground,formal}.md` — slash 命令
- `.claude/skills/{diagnose-desense,harmonic-calc,sop-executor,engineering-logger}/` — skills
- `CLAUDE.md` — 项目级指南(替代 AGENTS.md)
EOF
fi

echo ""
echo "========================================"
echo "安装完成!"
echo "========================================"
echo ""
echo "下一步:"
echo "1. 阅读 CLAUDE.md 了解项目规范"
echo "2. 在 Claude Code 中打开此目录"
echo "3. 输入 /diagnose 启动 Desense 诊断流程"
echo "4. 查看 knowledge/ 目录了解方法论"
echo ""
echo "常用 slash 命令:"
echo "  /diagnose   — 启动诊断"
echo "  /matrix     — 查询矩阵表"
echo "  /playground — 临时调试区"
echo "  /formal     — 生成正式报告"
echo ""
