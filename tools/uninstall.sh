#!/bin/bash

# Echo·Desense (Claude Code 版) 卸载脚本

set -e

echo "========================================"
echo "Echo·Desense 卸载脚本 (Claude Code)"
echo "========================================"

# 检查运行目录
if [ ! -f "CLAUDE.md" ]; then
    echo "错误:请在项目根目录(包含 CLAUDE.md)运行此脚本"
    exit 1
fi

# 确认卸载
read -p "确定要卸载 Echo·Desense 吗?(y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "已取消卸载"
    exit 0
fi

# 删除 Git 仓库
if [ -d ".git" ]; then
    echo "删除 Git 仓库..."
    rm -rf .git
fi

# 删除生成的文件
echo "删除生成的文件..."
rm -f CHANGELOG.md

# 保留的文件和目录
echo "保留以下文件和目录:"
echo "  - .claude/"
echo "  - knowledge/"
echo "  - tools/"
echo "  - docs/"
echo "  - logs/"
echo "  - playground/"
echo "  - extensions/"
echo "  - .gitignore"
echo "  - LICENSE"
echo "  - CLAUDE.md"
echo "  - README.md"
echo "  - install.sh"
echo "  - uninstall.sh"

echo ""
echo "========================================"
echo "卸载完成!"
echo "========================================"
echo ""
echo "注意:"
echo "  - logs/ 和 playground/ 目录未删除"
echo "  - 如需完全删除,请手动执行:"
echo "    rm -rf logs/ playground/"
echo ""
