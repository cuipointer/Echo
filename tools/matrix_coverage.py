#!/usr/bin/env python3
"""Echo·Desense 矩阵覆盖度报告.

扫描 knowledge/matrix/matrix.yaml 中每条 (source, victim) 映射,对每个 SOP 文件
分类为 formal / v0.9 / stub / missing 四种状态,并统计 knowledge/cases/*.md 中
指向每个 SOP 的引用次数。输出 Markdown 报告,揭示知识库盲点。

用法:
  python3 tools/matrix_coverage.py                    # 打印到 stdout
  python3 tools/matrix_coverage.py > report.md        # 重定向保存
  python3 tools/matrix_coverage.py --output report.md # 写入文件
  python3 tools/matrix_coverage.py --format json      # JSON 输出
  python3 tools/matrix_coverage.py --tier P0          # 仅 P0

退出码:
  0 = 正常
  1 = 存在"案例孤儿"(sop_refs 指向 missing 文件或 stub SOP 被案例引用)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("错误:需要 PyYAML。安装: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).parent.parent
MATRIX_YAML = ROOT / "knowledge/matrix/matrix.yaml"
SOPS_DIR = ROOT / "knowledge/sops"
CASES_DIR = ROOT / "knowledge/cases"

# 状态分类常量
STATE_FORMAL = "formal"
STATE_V09 = "v0.9"
STATE_STUB = "stub"
STATE_MISSING = "missing"
STATE_ORDER = [STATE_FORMAL, STATE_V09, STATE_STUB, STATE_MISSING]
STATE_ICON = {
    STATE_FORMAL: "OK",
    STATE_V09: "v0.9",
    STATE_STUB: "stub",
    STATE_MISSING: "MISS",
}
TIER_ORDER = ["P0", "P1", "P2"]

# victim 族排序(与 matrix.yaml victims 声明顺序一致)
VICTIM_ORDER = ["NORMAL", "W24", "W5", "LLB", "LHB", "GL1", "GL5"]


# --------------------------------------------------------------------------
# 数据加载
# --------------------------------------------------------------------------
def load_matrix() -> dict:
    """复用 gen_matrix_views.py 的解析逻辑。"""
    with open(MATRIX_YAML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def sop_path_for(sop_id: str) -> Path:
    """SOP 编号 → 磁盘路径。NORMAL 族文件名有 SOP- 前缀。"""
    victim_code = sop_id.split("-", 1)[0]
    if victim_code == "NORMAL":
        return SOPS_DIR / "NORMAL" / f"SOP-{sop_id}.md"
    return SOPS_DIR / victim_code / f"{sop_id}.md"


# --------------------------------------------------------------------------
# SOP 状态分类(参照 check-architecture-consistency.py 第 51-63 行)
# --------------------------------------------------------------------------
def classify_sop(path: Path) -> str:
    """读取 SOP 头部,分类为 formal / v0.9 / stub / missing。"""
    if not path.exists():
        return STATE_MISSING

    content = path.read_text(encoding="utf-8")
    head = content[:600]

    # 顺序关键:v0.9 方法论版可能在升级说明里提到 "placeholder",须先判定
    is_methodology = "方法论版" in head
    if is_methodology:
        return STATE_V09

    is_stub = (
        "**状态**:**待编写**" in content
        or "**状态**：待编写" in content
        or "**待编写**" in content[:500]
        or "(placeholder," in head  # gen_sop_stubs.py 生成器标记
    )
    if is_stub:
        return STATE_STUB

    # 正式版:含 **版本**:v1.x 或 **版本**:v1.x 且非方法论
    if re.search(r"\*\*版本\*\*[:：]v1\.", head):
        return STATE_FORMAL

    # 兜底:含版本号但非 v1 / v0.9 / stub → 视为 formal(极少见)
    if re.search(r"\*\*版本\*\*[:：]v\d+\.\d+", head):
        return STATE_FORMAL

    return STATE_FORMAL  # 存在且无明显 stub/方法论标记 → 默认 formal


# --------------------------------------------------------------------------
# 案例 sop_refs 扫描
# --------------------------------------------------------------------------
def scan_case_refs() -> tuple[Counter, dict[str, list[str]]]:
    """扫描 knowledge/cases/*.md 的 frontmatter sop_refs 字段。

    返回:
      counter: {sop_id: 引用次数}
      reverse: {sop_id: [case_filename, ...]}
    """
    counter: Counter = Counter()
    reverse: dict[str, list[str]] = defaultdict(list)

    if not CASES_DIR.exists():
        return counter, reverse

    fm_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

    for case_file in sorted(CASES_DIR.glob("*.md")):
        content = case_file.read_text(encoding="utf-8")
        m = fm_pattern.match(content)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        refs = fm.get("sop_refs") or []
        if not isinstance(refs, list):
            continue
        for sop_id in refs:
            sop_id = str(sop_id).strip()
            if not sop_id:
                continue
            counter[sop_id] += 1
            reverse[sop_id].append(case_file.name)

    return counter, reverse


# --------------------------------------------------------------------------
# 覆盖度计算
# --------------------------------------------------------------------------
def build_coverage(data: dict) -> list[dict]:
    """为每条 mapping 构建一个 coverage 记录。"""
    case_counts, _ = scan_case_refs()

    rows = []
    for m in data["mappings"]:
        sop_id = m["sop"]
        path = sop_path_for(sop_id)
        state = classify_sop(path)
        source_key = m["source"]
        victim_key = m["victim"]
        source = data["sources"].get(source_key, {})
        victim = data["victims"].get(victim_key, {})

        rows.append({
            "tier": m.get("tier", "?"),
            "source_key": source_key,
            "source_label": source.get("label", source_key),
            "victim_key": victim_key,
            "victim_label": victim.get("label", victim_key),
            "sop_id": sop_id,
            "sop_path": str(path.relative_to(ROOT)),
            "state": state,
            "cases": case_counts.get(sop_id, 0),
            "typical_degradation": m.get("typical_degradation", "-"),
            "high_priority": bool(m.get("high_priority", False)),
            "mechanism": m.get("mechanism", "-"),
        })
    return rows


def detect_orphans(data: dict) -> list[dict]:
    """检测案例孤儿:
    1) sop_refs 指向 matrix 中不存在 SOP(即该 sop_id 未出现在 mappings 中
       或对应 SOP 文件不存在)
    2) SOP state == stub,但被案例引用(有案例却无正式 SOP)
    """
    case_counts, reverse = scan_case_refs()
    known_sops = {m["sop"] for m in data["mappings"]}

    # 建立 sop_id → state 映射
    sop_states: dict[str, str] = {}
    for sop_id in known_sops:
        sop_states[sop_id] = classify_sop(sop_path_for(sop_id))

    orphans = []
    for sop_id, count in case_counts.items():
        cases = reverse.get(sop_id, [])
        if sop_id not in known_sops:
            orphans.append({
                "type": "案例引用了矩阵未声明的 SOP",
                "sop_id": sop_id,
                "count": count,
                "cases": cases,
            })
            continue
        state = sop_states.get(sop_id, STATE_MISSING)
        if state == STATE_MISSING:
            orphans.append({
                "type": "案例引用了文件缺失的 SOP",
                "sop_id": sop_id,
                "count": count,
                "cases": cases,
            })
        elif state == STATE_STUB:
            orphans.append({
                "type": "案例已沉淀但 SOP 仍为 stub",
                "sop_id": sop_id,
                "count": count,
                "cases": cases,
            })
    return orphans


# --------------------------------------------------------------------------
# Markdown 渲染
# --------------------------------------------------------------------------
def _victim_sort_key(v: str) -> int:
    try:
        return VICTIM_ORDER.index(v)
    except ValueError:
        return len(VICTIM_ORDER)


def _tier_sort_key(t: str) -> int:
    try:
        return TIER_ORDER.index(t)
    except ValueError:
        return len(TIER_ORDER)


def render_markdown(data: dict, rows: list[dict], orphans: list[dict],
                    tier_filter: str = "all") -> str:
    lines: list[str] = []

    if tier_filter != "all":
        rows = [r for r in rows if r["tier"] == tier_filter]

    # 排序:tier → victim 族 → sop_id
    rows_sorted = sorted(
        rows,
        key=lambda r: (_tier_sort_key(r["tier"]),
                       _victim_sort_key(r["victim_key"]),
                       r["sop_id"]),
    )

    # -------- 标题 --------
    lines.append("# Echo·Desense 矩阵覆盖度报告")
    lines.append("")
    lines.append(f"**数据源**:`knowledge/matrix/matrix.yaml` (v{data['version']}, {data['updated']})")
    lines.append(f"**映射总数**:{len(rows)}(tier filter = `{tier_filter}`)")
    lines.append("")
    lines.append("**状态定义**:")
    lines.append("- `formal` — 正式版 SOP(版本 v1.x,非方法论版)")
    lines.append("- `v0.9` — 方法论版(案例反哺,未经现场复测)")
    lines.append("- `stub` — 占位 SOP(待编写)")
    lines.append("- `missing` — matrix 声明了但文件不存在")
    lines.append("")
    lines.append("---")
    lines.append("")

    # -------- Section 1: 汇总 --------
    lines.append("## Section 1:汇总")
    lines.append("")

    # state 计数
    state_counter: Counter = Counter(r["state"] for r in rows_sorted)
    lines.append("### 状态计数")
    lines.append("")
    lines.append("| 状态 | 数量 | 占比 |")
    lines.append("|------|:----:|:----:|")
    total = max(1, len(rows_sorted))
    for s in STATE_ORDER:
        n = state_counter.get(s, 0)
        pct = n * 100.0 / total
        lines.append(f"| {s} | {n} | {pct:.1f}% |")
    lines.append(f"| **合计** | **{len(rows_sorted)}** | 100.0% |")
    lines.append("")

    # tier 分布
    lines.append("### Tier × 状态 分布")
    lines.append("")
    header = "| tier | " + " | ".join(STATE_ORDER) + " | 小计 |"
    sep = "|:----:|" + "|".join([":----:"] * len(STATE_ORDER)) + "|:----:|"
    lines.append(header)
    lines.append(sep)
    for tier in TIER_ORDER:
        tier_rows = [r for r in rows_sorted if r["tier"] == tier]
        if not tier_rows and tier_filter != "all":
            continue
        counts = Counter(r["state"] for r in tier_rows)
        cells = [str(counts.get(s, 0)) for s in STATE_ORDER]
        lines.append(f"| {tier} | " + " | ".join(cells) + f" | {len(tier_rows)} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # -------- Section 2: 详细覆盖度表 --------
    lines.append("## Section 2:详细覆盖度表")
    lines.append("")
    lines.append("_按 tier → victim 族 → SOP ID 排序_")
    lines.append("")
    lines.append("| tier | source | victim | SOP ID | state | cases | typical_degradation |")
    lines.append("|:----:|--------|--------|--------|:-----:|:-----:|---------------------|")
    for r in rows_sorted:
        lines.append(
            f"| {r['tier']} | {r['source_key']} | {r['victim_key']} | "
            f"{r['sop_id']} | {r['state']} | {r['cases']} | {r['typical_degradation']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # -------- Section 3: 盲点清单 --------
    lines.append("## Section 3:盲点清单(tier ∈ {P0, P1} 且 state ∈ {stub, missing})")
    lines.append("")
    blindspots = [
        r for r in rows_sorted
        if r["tier"] in ("P0", "P1") and r["state"] in (STATE_STUB, STATE_MISSING)
    ]
    if not blindspots:
        lines.append("_无盲点:P0 / P1 映射均已至少有 v0.9 版本 SOP。_")
    else:
        # P0 优先
        blindspots.sort(
            key=lambda r: (_tier_sort_key(r["tier"]),
                           0 if r["state"] == STATE_MISSING else 1,
                           _victim_sort_key(r["victim_key"]), r["sop_id"]),
        )
        lines.append("| 优先级 | tier | source | victim | SOP ID | state | cases | 机制 |")
        lines.append("|:------:|:----:|--------|--------|--------|:-----:|:-----:|------|")
        for i, r in enumerate(blindspots, 1):
            lines.append(
                f"| {i} | {r['tier']} | {r['source_key']} | {r['victim_key']} | "
                f"{r['sop_id']} | {r['state']} | {r['cases']} | {r['mechanism']} |"
            )
    lines.append("")
    lines.append("---")
    lines.append("")

    # -------- Section 4: 案例孤儿 --------
    lines.append("## Section 4:案例孤儿")
    lines.append("")
    lines.append("_sop_refs 指向不存在的 SOP,或 SOP 仍为 stub 却已被案例引用。_")
    lines.append("")
    if not orphans:
        lines.append("_未发现案例孤儿。_")
    else:
        lines.append("| 类型 | SOP ID | 引用次数 | 案例 |")
        lines.append("|------|--------|:--------:|------|")
        for o in orphans:
            cases_str = ", ".join(f"`{c}`" for c in o["cases"])
            lines.append(f"| {o['type']} | `{o['sop_id']}` | {o['count']} | {cases_str} |")
    lines.append("")

    return "\n".join(lines)


def render_json(data: dict, rows: list[dict], orphans: list[dict],
                tier_filter: str) -> str:
    if tier_filter != "all":
        rows = [r for r in rows if r["tier"] == tier_filter]
    rows_sorted = sorted(
        rows,
        key=lambda r: (_tier_sort_key(r["tier"]),
                       _victim_sort_key(r["victim_key"]),
                       r["sop_id"]),
    )
    state_counter = Counter(r["state"] for r in rows_sorted)
    tier_counter: dict = {}
    for tier in TIER_ORDER:
        tier_rows = [r for r in rows_sorted if r["tier"] == tier]
        tier_counter[tier] = {
            "total": len(tier_rows),
            "by_state": dict(Counter(r["state"] for r in tier_rows)),
        }
    return json.dumps({
        "matrix_version": data["version"],
        "matrix_updated": data["updated"],
        "tier_filter": tier_filter,
        "total_mappings": len(rows_sorted),
        "summary": {
            "by_state": dict(state_counter),
            "by_tier": tier_counter,
        },
        "mappings": rows_sorted,
        "orphans": orphans,
    }, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="生成 Echo·Desense 矩阵覆盖度报告(source × victim → SOP 状态 + 案例引用)。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--output", metavar="PATH",
                        help="写入文件路径(省略则输出到 stdout)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown",
                        help="输出格式(默认 markdown)")
    parser.add_argument("--tier", choices=["P0", "P1", "P2", "all"], default="all",
                        help="按 tier 过滤(默认 all)")
    args = parser.parse_args()

    data = load_matrix()
    rows = build_coverage(data)
    orphans = detect_orphans(data)

    if args.format == "json":
        out = render_json(data, rows, orphans, args.tier)
    else:
        out = render_markdown(data, rows, orphans, args.tier)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"✓ 报告已写入 {args.output}", file=sys.stderr)
    else:
        print(out)

    return 1 if orphans else 0


if __name__ == "__main__":
    sys.exit(main())
