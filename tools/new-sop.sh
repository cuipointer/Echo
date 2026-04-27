#!/bin/bash

# SOP 快速创建脚本

set -e

echo "========================================"
echo "SOP 快速创建脚本"
echo "========================================"

# 检查运行目录
if [ ! -f "CLAUDE.md" ]; then
    echo "错误：请在项目根目录运行此脚本"
    exit 1
fi

# 输入参数
read -p "请输入受扰体代码 (W24/W5/LLB/LHB/GL1/GL5): " victim
read -p "请输入干扰源代码 (LC/CA/DD/PM/VB/SP/CH/U3): " source
read -p "请输入 SOP 序号 (01-99): " number

# 验证输入
if [[ ! "$victim" =~ ^(W24|W5|LLB|LHB|GL1|GL5)$ ]]; then
    echo "错误：受扰体代码无效"
    exit 1
fi

if [[ ! "$source" =~ ^(LC|CA|DD|PM|VB|SP|CH|U3)$ ]]; then
    echo "错误：干扰源代码无效"
    exit 1
fi

if [[ ! "$number" =~ ^[0-9]{2}$ ]]; then
    echo "错误：序号必须是两位数字"
    exit 1
fi

# SOP 编号
sop_id="${victim}-${source}-${number}"

# 目标目录
target_dir="knowledge/sops/${victim}"
target_file="${target_dir}/SOP-${sop_id}.md"

# 检查是否已存在
if [ -f "$target_file" ]; then
    echo "警告：SOP 文件已存在：$target_file"
    read -p "是否覆盖？(y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 0
    fi
fi

# 创建 SOP 文件
echo "创建 SOP 文件：$target_file"

# 复制模板
cp knowledge/sops/_template.md "$target_file"

# 替换占位符
sed -i "s/{受扰体}/{受扰体}/g" "$target_file"
sed -i "s/{干扰源}/{干扰源}/g" "$target_file"
sed -i "s/{序号}/${number}/g" "$target_file"

# 设置标题
title="# SOP-${sop_id}"
sed -i "1s/.*/${title}/" "$target_file"

echo ""
echo "========================================"
echo "SOP 创建完成！"
echo "========================================"
echo ""
echo "文件位置：$target_file"
echo ""
echo "下一步："
echo "1. 编辑文件，填写完整 SOP 内容"
echo "2. 更新矩阵表：knowledge/matrix/matrix-table.md"
echo "3. 提交到 Git 仓库"
echo ""
