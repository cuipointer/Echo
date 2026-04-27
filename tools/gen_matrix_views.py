#!/usr/bin/env python3
"""从 knowledge/matrix/matrix.yaml 生成三个 Markdown 视图。

视图:
  - matrix-table.md   (源 × 受扰体 SOP 矩阵)
  - source-list.md    (干扰源清单,按 category 分组)
  - victim-list.md    (受扰体清单)

用法:
  python3 tools/gen_matrix_views.py

matrix.yaml 是唯一真相源,手动修改生成的 .md 会在下次运行时被覆盖。
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("错误:需要 PyYAML。安装: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).parent.parent
MATRIX_YAML = ROOT / "knowledge/matrix/matrix.yaml"
OUT_MATRIX = ROOT / "knowledge/matrix/matrix-table.md"
OUT_SOURCES = ROOT / "knowledge/matrix/source-list.md"
OUT_VICTIMS = ROOT / "knowledge/matrix/victim-list.md"

GENERATED_BANNER = "<!-- 由 tools/gen_matrix_views.py 从 matrix.yaml 生成,手改无效 -->"


def load():
    with open(MATRIX_YAML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_mapping_lookup(data):
    """{(source_key, victim_key): mapping}"""
    lookup = {}
    for m in data["mappings"]:
        lookup[(m["source"], m["victim"])] = m
    return lookup


def gen_matrix_table(data):
    lines = []
    lines.append(GENERATED_BANNER)
    lines.append("")
    lines.append("# 核心矩阵表")
    lines.append("")
    lines.append(f"**版本**:{data['version']}")
    lines.append(f"**更新日期**:{data['updated']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 矩阵结构")
    lines.append("")
    lines.append("矩阵表用于快速定位 (干扰源, 受扰体) 组合对应的 SOP 编号。")
    lines.append("")
    lines.append("**使用流程**:决策树定位干扰源 → 矩阵表查询 SOP → 执行标准化排查")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 完整矩阵")
    lines.append("")
    lines.append("### 干扰源 ↓ \\ 受扰体 →")
    lines.append("")

    victims_order = list(data["victims"].keys())
    sources_order = list(data["sources"].keys())
    lookup = build_mapping_lookup(data)

    header_cells = ["干扰源"]
    align_cells = ["--------"]
    for vk in victims_order:
        v = data["victims"][vk]
        if v.get("is_baseline"):
            header_cells.append(f"**{v['label']}**")
            align_cells.append(":----------:")
        else:
            header_cells.append(v["label"])
            align_cells.append("-----------")
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("|" + "|".join(align_cells) + "|")

    for sk in sources_order:
        s = data["sources"][sk]
        row = [f"**{s['label']}**"]
        for vk in victims_order:
            m = lookup.get((sk, vk))
            if m is None:
                row.append("—")
            else:
                cell = m["sop"]
                # Normal 列整体加粗(基准场景优先),或 high_priority → 加粗一次,不重复
                if vk == "NORMAL" or m.get("high_priority"):
                    cell = f"**{cell}**"
                row.append(cell)
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("### 标注说明")
    lines.append("- **加粗** = 高频问题,优先编写 SOP")
    lines.append("- `—` = 频率域无直接交叠(仍需检查谐波)")
    lines.append("- **Normal 列** = 基准场景,所有排查前置条件")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 干扰源详细信息")
    lines.append("")
    for sk in sources_order:
        s = data["sources"][sk]
        lines.append(f"### {s['label']}")
        lines.append(f"- **基频范围**:{s['base_freq_range']}")
        lines.append(f"- **噪声来源**:{s['noise_source']}")
        lines.append(f"- **典型干扰**:{s['typical_interference']}")
        if s.get("normal_impact"):
            lines.append(f"- **Normal 影响**:{s['normal_impact']}")
        lines.append(f"- **排查优先级**:{s['priority']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 受扰体详细信息")
    lines.append("")
    for vk in victims_order:
        v = data["victims"][vk]
        lines.append(f"### {v['label']}")
        if v.get("is_baseline"):
            lines.append(f"- **说明**:{v['description']}")
        else:
            fr = v["freq_range_mhz"]
            lines.append(f"- **频率范围**:{fr[0]}-{fr[1]} MHz")
            sens = v["sensitivity_dbm"]
            lines.append(f"- **敏感度要求**:{sens[0]} ~ {sens[1]} dBm")
            if v.get("notes"):
                lines.append(f"- **备注**:{v['notes']}")
        lines.append(f"- **优先级**:{v['priority']}")
        lines.append("")

    # 按 tier 分组
    lines.append("---")
    lines.append("")
    lines.append("## 组合详情(按优先级)")
    lines.append("")
    for tier, tier_label in [("P0", "P0 高频问题(必备 SOP)"),
                             ("P1", "P1 中频问题(应编写)"),
                             ("P2", "P2 低频问题(按需)")]:
        tier_maps = [m for m in data["mappings"] if m.get("tier") == tier]
        if not tier_maps:
            continue
        lines.append(f"### {tier_label}")
        lines.append("")
        lines.append("| SOP 编号 | 干扰源 | 受扰体 | 机制 | 典型恶化 | 诊断提示 |")
        lines.append("|---------|--------|--------|------|----------|----------|")
        for m in tier_maps:
            s = data["sources"][m["source"]]
            v = data["victims"][m["victim"]]
            sop = m["sop"]
            if m.get("high_priority"):
                sop = f"**{sop}**"
            lines.append(f"| {sop} | {s['label']} | {v['label']} | {m.get('mechanism', '-')} | {m.get('typical_degradation', '-')} | {m.get('diagnosis_hint', '-')} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## SOP 编号规则")
    lines.append("")
    lines.append(f"**格式**:`{data['sop_numbering']['format']}`")
    lines.append(f"- {data['sop_numbering']['note']}")
    lines.append("")
    lines.append("### 受扰体代码")
    lines.append("| 代码 | 频段 |")
    lines.append("|------|------|")
    for vk in victims_order:
        v = data["victims"][vk]
        lines.append(f"| {v['code']} | {v['label']} |")
    lines.append("")
    lines.append("### 干扰源代码")
    lines.append("| 代码 | 模块 |")
    lines.append("|------|------|")
    for sk in sources_order:
        s = data["sources"][sk]
        lines.append(f"| {s['code']} | {s['label']} |")
    lines.append("")

    # 谐波参考
    if data.get("harmonic_reference"):
        lines.append("---")
        lines.append("")
        lines.append("## 谐波分析参考")
        lines.append("")
        lines.append("### 常见谐波命中")
        lines.append("| 干扰源基频 | 受扰体 | 谐波次数 | 命中频点 |")
        lines.append("|------------|--------|----------|----------|")
        for h in data["harmonic_reference"]:
            lines.append(f"| {h['source']} | {h['victim']} | {h['order']} | {h['hit']} |")
        lines.append("")
        lines.append("### 谐波计算公式")
        lines.append("```")
        lines.append("干扰频率 = 基频 × N")
        lines.append("命中判断:受扰体频率范围是否包含干扰频率")
        lines.append("```")
        lines.append("")

    # 更新记录
    lines.append("---")
    lines.append("")
    lines.append("## 更新记录")
    lines.append("")
    lines.append("| 版本 | 日期 | 更新内容 |")
    lines.append("|------|------|----------|")
    for c in data.get("changelog", []):
        lines.append(f"| {c['version']} | {c['date']} | {c['notes']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 相关文档")
    lines.append("- 真相源:`knowledge/matrix/matrix.yaml`")
    lines.append("- 决策树:[knowledge/decision-tree.md](../decision-tree.md)")
    lines.append("- SOP 模板:[knowledge/sops/_template.md](../sops/_template.md)")
    lines.append("- 干扰源清单:[source-list.md](source-list.md)(生成)")
    lines.append("- 受扰体清单:[victim-list.md](victim-list.md)(生成)")
    lines.append("")

    return "\n".join(lines)


def gen_source_list(data):
    lines = []
    lines.append(GENERATED_BANNER)
    lines.append("")
    lines.append("# 干扰源清单")
    lines.append("")
    lines.append(f"**版本**:{data['version']}")
    lines.append(f"**更新日期**:{data['updated']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 总表(按类别)")
    lines.append("")
    lines.append("| 大类 | 干扰源 | 代码 | 基频范围 | 优先级 |")
    lines.append("|------|--------|------|----------|--------|")
    by_cat = {}
    for sk, s in data["sources"].items():
        by_cat.setdefault(s["category"], []).append((sk, s))
    for cat, items in by_cat.items():
        first = True
        for sk, s in items:
            cat_col = cat if first else ""
            first = False
            lines.append(f"| {cat_col} | {s['label']} | {s['code']} | {s['base_freq_range']} | {s['priority']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 详细说明")
    lines.append("")
    for sk, s in data["sources"].items():
        lines.append(f"### {s['label']}")
        lines.append(f"- **分类**:{s['category']}")
        lines.append(f"- **代码**:{s['code']}")
        lines.append(f"- **基频范围**:{s['base_freq_range']}")
        lines.append(f"- **噪声来源**:{s['noise_source']}")
        lines.append(f"- **典型干扰**:{s['typical_interference']}")
        if s.get("normal_impact"):
            lines.append(f"- **Normal 影响**:{s['normal_impact']}")
        lines.append(f"- **排查优先级**:{s['priority']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 真相源")
    lines.append("- 本文件由 `tools/gen_matrix_views.py` 从 `knowledge/matrix/matrix.yaml` 自动生成")
    lines.append("- 新增/修改干扰源请改 YAML,然后重新运行生成器")
    lines.append("")
    return "\n".join(lines)


def gen_victim_list(data):
    lines = []
    lines.append(GENERATED_BANNER)
    lines.append("")
    lines.append("# 受扰体清单")
    lines.append("")
    lines.append(f"**版本**:{data['version']}")
    lines.append(f"**更新日期**:{data['updated']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 总表")
    lines.append("")
    lines.append("| 受扰体 | 代码 | 频率范围 | 敏感度要求 | 优先级 |")
    lines.append("|--------|------|----------|------------|--------|")
    for vk, v in data["victims"].items():
        if v.get("is_baseline"):
            lines.append(f"| {v['label']} | {v['code']} | (基准场景) | — | {v['priority']} |")
            continue
        fr = v["freq_range_mhz"]
        sens = v["sensitivity_dbm"]
        freq_str = f"{fr[0]}-{fr[1]} MHz" if fr[0] != fr[1] else f"{fr[0]} MHz"
        lines.append(f"| {v['label']} | {v['code']} | {freq_str} | {sens[0]} ~ {sens[1]} dBm | {v['priority']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 详细说明")
    lines.append("")
    for vk, v in data["victims"].items():
        lines.append(f"### {v['label']}")
        if v.get("is_baseline"):
            lines.append(f"- **说明**:{v['description']}")
        else:
            fr = v["freq_range_mhz"]
            freq_str = f"{fr[0]}-{fr[1]} MHz" if fr[0] != fr[1] else f"{fr[0]} MHz"
            sens = v["sensitivity_dbm"]
            lines.append(f"- **频率范围**:{freq_str}")
            lines.append(f"- **敏感度要求**:{sens[0]} ~ {sens[1]} dBm")
            if v.get("notes"):
                lines.append(f"- **备注**:{v['notes']}")
        lines.append(f"- **优先级**:{v['priority']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 敏感度分级")
    lines.append("")
    lines.append("| 量级 | 受扰体 | 排查难度 |")
    lines.append("|------|--------|----------|")
    lines.append("| 极高 (-140 ~ -150 dBm) | GNSS L1 / GNSS L5 | 微弱干扰即影响性能 |")
    lines.append("| 高 (-94 ~ -102 dBm) | LTE LB / LTE HB | 常见干扰,需重点排查 |")
    lines.append("| 中 (-82 ~ -90 dBm) | WiFi 2.4G / WiFi 5G | 噪声边际较大 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 真相源")
    lines.append("- 本文件由 `tools/gen_matrix_views.py` 从 `knowledge/matrix/matrix.yaml` 自动生成")
    lines.append("- 新增/修改受扰体请改 YAML,然后重新运行生成器")
    lines.append("")
    return "\n".join(lines)


def main():
    data = load()
    OUT_MATRIX.write_text(gen_matrix_table(data), encoding="utf-8")
    OUT_SOURCES.write_text(gen_source_list(data), encoding="utf-8")
    OUT_VICTIMS.write_text(gen_victim_list(data), encoding="utf-8")

    print(f"✓ 生成 {OUT_MATRIX.relative_to(ROOT)}")
    print(f"✓ 生成 {OUT_SOURCES.relative_to(ROOT)}")
    print(f"✓ 生成 {OUT_VICTIMS.relative_to(ROOT)}")
    print(f"  数据源:{MATRIX_YAML.relative_to(ROOT)} (v{data['version']})")
    print(f"  sources: {len(data['sources'])}  victims: {len(data['victims'])}  mappings: {len(data['mappings'])}")


if __name__ == "__main__":
    main()
