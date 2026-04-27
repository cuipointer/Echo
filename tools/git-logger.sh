#!/bin/bash

# Echo Git Logger - 工程日志 Git 集成工具
# 自动提交日志文件到 Git 仓库

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: $0 <日志文件路径> [提交消息]"
    echo ""
    echo "示例:"
    echo "  $0 logs/daily/2026-04-21.md"
    echo "  $0 logs/daily/2026-04-21.md 'docs: 更新日志 - 15:00 Desense分析 完成排查'"
    exit 1
fi

LOG_FILE="$1"
COMMIT_MSG="$2"

# 检查日志文件是否存在
if [ ! -f "$LOG_FILE" ]; then
    log_error "日志文件不存在: $LOG_FILE"
    exit 1
fi

# 检查是否为 Git 仓库
if [ ! -d ".git" ]; then
    log_error "当前目录不是 Git 仓库"
    exit 1
fi

# 获取当前分支
CURRENT_BRANCH=$(git branch --show-current)
log_info "当前分支: $CURRENT_BRANCH"

# 检查分支策略
if [ "$CURRENT_BRANCH" = "master" ]; then
    log_warning "在主分支 (master) 上，禁止自动提交"
    log_info "建议切换到 echo-dev 分支: git checkout echo-dev"
    exit 1
fi

if [ "$CURRENT_BRANCH" != "echo-dev" ]; then
    log_warning "当前分支不是 echo-dev ($CURRENT_BRANCH)"
    read -p "是否继续提交？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "已取消提交"
        exit 0
    fi
fi

# 提取日志信息用于提交消息
if [ -z "$COMMIT_MSG" ]; then
    # 从日志文件提取最新活动
    LATEST_ENTRY=$(tail -n 20 "$LOG_FILE" | grep -E '^\| [0-9]{2}:[0-9]{2} \|' | tail -n 1 | sed 's/|/ /g' | awk '{$1=$1;print}')
    
    if [ -n "$LATEST_ENTRY" ]; then
        # 提取时间、模块和摘要
        TIME=$(echo "$LATEST_ENTRY" | awk '{print $1}')
        MODULE=$(echo "$LATEST_ENTRY" | awk '{print $2}')
        SUMMARY=$(echo "$LATEST_ENTRY" | awk '{$1=$2=""; print $0}' | sed 's/^ *//' | sed 's/ ✅ 完成//')
        
        COMMIT_MSG="docs: 更新日志 - $TIME $MODULE $SUMMARY"
    else
        COMMIT_MSG="docs: 更新工程日志"
    fi
fi

log_info "提交消息: $COMMIT_MSG"

# 检查是否有变更
if git diff --quiet "$LOG_FILE"; then
    log_warning "日志文件没有变更，跳过提交"
    exit 0
fi

# 执行 Git 操作
log_info "添加日志文件到暂存区..."
git add "$LOG_FILE"

log_info "提交变更..."
git commit -m "$COMMIT_MSG"

log_success "日志已成功提交到 Git"

# 显示提交信息
log_info "提交哈希: $(git log -1 --pretty=format:%H)"
log_info "提交时间: $(git log -1 --pretty=format:%cd)"

# 更新日志文件中的统计信息（可选）
if grep -q "提交次数" "$LOG_FILE"; then
    # 获取今日提交次数
    TODAY=$(date +%Y-%m-%d)
    COMMIT_COUNT=$(git log --since="$TODAY 00:00:00" --until="$TODAY 23:59:59" --oneline | wc -l)
    
    # 更新统计信息（简化处理，实际使用可能需要更复杂的 sed 操作）
    log_info "今日提交次数: $COMMIT_COUNT"
fi