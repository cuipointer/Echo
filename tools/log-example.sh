#!/bin/bash

# Echo 日志系统使用示例
# 演示如何结合日志记录和 Git 提交

set -e

# 检查当前目录
if [ ! -f "CLAUDE.md" ]; then
    echo "错误：请在项目根目录运行此脚本"
    exit 1
fi

# 获取当前日期
TODAY=$(date +%Y-%m-%d)
LOG_FILE="logs/daily/$TODAY.md"

# 检查日志文件是否存在，不存在则创建
if [ ! -f "$LOG_FILE" ]; then
    echo "创建今日日志文件: $LOG_FILE"
    cp "logs/templates/daily-template.md" "$LOG_FILE"
    sed -i "s/{{DATE}}/$TODAY/g" "$LOG_FILE"
fi

# 添加示例日志条目
CURRENT_TIME=$(date +%H:%M)
LOG_ENTRY="| $CURRENT_TIME | 工具开发 | 实现 Git 日志集成功能 | ✅ 完成 |"

# 在今日活动表格中追加新条目
# 找到表格结束位置（第一个空行）并插入
awk -v entry="$LOG_ENTRY" '
/^\| [0-9]{2}:[0-9]{2} \|/ { found=1 }
/^$/ && found { print entry; found=0 }
{ print }
' "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"

echo "已添加日志条目: $LOG_ENTRY"

# 使用 Git 日志工具提交
if [ -f "tools/git-logger.sh" ]; then
    echo ""
    echo "=== 执行 Git 提交 ==="
    ./tools/git-logger.sh "$LOG_FILE"
else
    echo "Git 日志工具未找到: tools/git-logger.sh"
fi