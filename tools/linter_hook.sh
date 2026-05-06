#!/usr/bin/env bash
# linter_hook.sh — PostToolUse hook 入口
#
# 在 Claude 做 Edit/Write/MultiEdit 后触发;仅在涉及知识库 / harness / 工具文件时
# 跑架构一致性 linter,输出简要状态回主会话。设计为"非阻塞反馈"——linter
# 发现错误只是提示,不阻止 Claude 继续;真阻塞交给后续 CI 或 pre-commit hook。
#
# Claude Code hooks 通过 stdin 传入 JSON payload(含 tool_input.file_path),
# 而不是环境变量。本脚本直接读 stdin JSON。
#
# 使用:
#   .claude/settings.json 里 PostToolUse 的 matcher = "Edit|Write|MultiEdit",
#   command = "bash tools/linter_hook.sh"

set -euo pipefail

cd "$(dirname "$0")/.."

# 读取 hook JSON payload(若无则降级为直接跑,兼容手工调用)
PAYLOAD=""
if [ ! -t 0 ]; then
  PAYLOAD="$(cat || true)"
fi

FP=""
if [ -n "$PAYLOAD" ] && command -v python3 >/dev/null 2>&1; then
  FP="$(printf '%s' "$PAYLOAD" | python3 -c 'import sys,json
try:
    d=json.load(sys.stdin)
    print((d.get("tool_input") or {}).get("file_path",""))
except Exception:
    print("")' 2>/dev/null || true)"
fi

# 命中范围判定:知识库 / harness / 工具 / 根级规范文档
case "$FP" in
  *knowledge/*.md|*knowledge/*.yaml|*knowledge/*.yml)
    IN_SCOPE=1 ;;
  *.claude/*.md|*.claude/*.json)
    IN_SCOPE=1 ;;
  *tools/*.py|*tools/*.sh)
    IN_SCOPE=1 ;;
  */CLAUDE.md|*/CHANGELOG.md|*/README.md)
    IN_SCOPE=1 ;;
  "")
    # 手工调用无 payload 时也跑一次
    IN_SCOPE=1 ;;
  *)
    IN_SCOPE=0 ;;
esac

if [ "$IN_SCOPE" -eq 0 ]; then
  exit 0
fi

# 跑 linter,截取结果尾部输出回主会话
OUT="$(python3 tools/check-architecture-consistency.py 2>&1 || true)"
SUMMARY="$(printf '%s' "$OUT" | tail -6)"

# 若实际存在严重错误或警告(非"无严重错误"之类的状态行),才反馈到 stderr
# 排除"✅ 无严重错误" / "✅ 无警告项" / "架构一致性优秀"这些正向摘要
if printf '%s' "$OUT" | grep -qE '(⚠️|❌|\[ERROR\]|\[WARN\])' \
   || printf '%s' "$OUT" | grep -qE '有 [0-9]+ 项可优化'; then
  {
    echo "[linter-hook] 架构一致性 linter 检出非 0 结果:"
    echo "$SUMMARY"
  } >&2
  # 非阻塞:即使有错也 exit 0,不拦 Claude
fi

exit 0
