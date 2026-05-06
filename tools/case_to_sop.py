#!/usr/bin/env python3
"""case_to_sop.py — 案例驱动 SOP 更新规划器(MVP, planner only).

输入:knowledge/cases/*.md 中的一个案例文件路径
输出:Markdown 形式的更新计划(stdout),针对 frontmatter sop_refs 里的
      每一个 SOP,识别其当前状态(stub / v0.9 / formal)并给出建议动作。

本工具只"规划",不修改任何 SOP 文件 —— 由 Claude(case-to-sop skill)在
读取本脚本输出后,使用 Write/Edit 工具执行实际的 SOP 更新。

用法:
    python3 tools/case_to_sop.py knowledge/cases/O2-NFC-W24.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False


# --------------------------------------------------------------------------- #
# Frontmatter & field extraction                                              #
# --------------------------------------------------------------------------- #

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    if HAS_YAML:
        try:
            data = yaml.safe_load(block) or {}
            if isinstance(data, dict):
                return data
        except yaml.YAMLError:
            pass
    # regex fallback
    data: dict = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            items = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
            data[k] = items
        else:
            data[k] = v.strip("'\"")
    return data


MACHINE_RE = re.compile(r"\*\*机型\*\*[:：]\s*([^\n*]+)")
PHASE_RE = re.compile(r"\*\*阶段\*\*[:：]\s*([^\n*]+)")
PHENOMENON_RE = re.compile(r"\*\*现象\*\*[:：]\s*([^\n]+)")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$", re.MULTILINE)


def extract_case_fields(text: str, fm: dict) -> dict:
    body = FM_RE.sub("", text, count=1)
    fields = {
        "title": fm.get("title", ""),
        "status": fm.get("status", ""),
        "sop_refs": fm.get("sop_refs", []) or [],
        "source_case": fm.get("source_case", ""),
        "machine": "",
        "phase": "",
        "phenomenon": "",
        "bullets": [],
    }
    if m := MACHINE_RE.search(body):
        fields["machine"] = m.group(1).strip()
    if m := PHASE_RE.search(body):
        fields["phase"] = m.group(1).strip()
    if m := PHENOMENON_RE.search(body):
        fields["phenomenon"] = m.group(1).strip()
    # grab first few bullets from the body (skip empty / navigation lines)
    bullets = BULLET_RE.findall(body)
    fields["bullets"] = [b for b in bullets if len(b) > 4][:8]
    return fields


# --------------------------------------------------------------------------- #
# SOP state detection (mirrors tools/check-architecture-consistency.py)        #
# --------------------------------------------------------------------------- #

def sop_path(base: Path, sop_id: str) -> Path:
    band = sop_id.split("-", 1)[0]
    if band == "NORMAL":
        return base / f"knowledge/sops/NORMAL/SOP-{sop_id}.md"
    return base / f"knowledge/sops/{band}/{sop_id}.md"


def detect_sop_state(content: str) -> str:
    head = content[:600]
    if ("**状态**:**待编写**" in content
            or "**状态**：待编写" in content
            or "**待编写**" in head):
        return "stub"
    if "方法论版" in head:
        return "v0.9"
    return "formal"


# --------------------------------------------------------------------------- #
# Sibling template selection                                                  #
# --------------------------------------------------------------------------- #

def pick_sibling_template(base: Path, sop_id: str) -> Path | None:
    """Pick the most authoritative sibling SOP in the same band to serve as
    a structural template when rewriting a stub.

    Preference: formal (v1.x) > v0.9 methodology > any other > None.
    """
    band = sop_id.split("-", 1)[0]
    if band == "NORMAL":
        sop_dir = base / "knowledge/sops/NORMAL"
    else:
        sop_dir = base / f"knowledge/sops/{band}"
    if not sop_dir.is_dir():
        return None

    formal: list[Path] = []
    methodology: list[Path] = []
    for p in sorted(sop_dir.glob("*.md")):
        if p.name == "_template.md":
            continue
        if sop_id in p.name:
            continue
        state = detect_sop_state(p.read_text(encoding="utf-8", errors="ignore"))
        if state == "formal":
            formal.append(p)
        elif state == "v0.9":
            methodology.append(p)
    if formal:
        return formal[0]
    if methodology:
        return methodology[0]
    return None


# --------------------------------------------------------------------------- #
# Plan rendering                                                              #
# --------------------------------------------------------------------------- #

def render_plan(case_path: Path, base: Path) -> str:
    text = case_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    fields = extract_case_fields(text, fm)
    out: list[str] = []
    rel_case = case_path.resolve().relative_to(base.resolve())

    out.append(f"# case-to-sop 更新计划")
    out.append("")
    out.append(f"**案例文件**:`{rel_case}`")
    if fields["title"]:
        out.append(f"**标题**:{fields['title']}")
    if fields["machine"] or fields["phase"]:
        out.append(f"**机型/阶段**:{fields['machine']} / {fields['phase']}")
    if fields["phenomenon"]:
        out.append(f"**现象**:{fields['phenomenon']}")
    if fields["source_case"]:
        out.append(f"**源**:{fields['source_case']}")
    out.append(f"**sop_refs**:{', '.join(fields['sop_refs']) if fields['sop_refs'] else '(空)'}")
    out.append("")

    if not fields["sop_refs"]:
        out.append("> [WARN] frontmatter 未声明 `sop_refs`,无法规划 SOP 更新。")
        out.append("> 请先在案例 frontmatter 填写 `sop_refs: [SOP-ID, ...]`,再重跑本脚本。")
        return "\n".join(out)

    out.append("## 关键案例要点(供 SOP 反哺参考)")
    out.append("")
    for b in fields["bullets"][:5]:
        out.append(f"- {b}")
    if not fields["bullets"]:
        out.append("- (未抽取到可用要点,Claude 需自行从案例正文提炼)")
    out.append("")

    out.append("## 逐 SOP 行动计划")
    out.append("")

    for sop_id in fields["sop_refs"]:
        sop_id = sop_id.strip()
        if not sop_id:
            continue
        out.append(f"### === SOP-{sop_id} ===")
        sp = sop_path(base, sop_id)
        if not sp.exists():
            out.append(f"- **State**: missing (文件不存在: `{sp.relative_to(base)}`)")
            out.append(f"- **Proposed action**: 先运行 `python3 tools/gen_sop_stubs.py` 生成 placeholder,再重跑本脚本")
            out.append("")
            continue
        state = detect_sop_state(sp.read_text(encoding="utf-8"))
        sibling = pick_sibling_template(base, sop_id)
        sibling_rel = sibling.relative_to(base) if sibling else "(同 band 无可用模板)"

        out.append(f"- **File**: `{sp.relative_to(base)}`")
        out.append(f"- **State**: `{state}`")
        out.append(f"- **Template (sibling)**: `{sibling_rel}`")

        if state == "stub":
            out.append("- **Proposed action**: **Full v0.9 rewrite** — 基于案例 + 兄弟 SOP 结构")
            out.append("  - 替换 v0.1 placeholder 为完整方法论版(8 大章节)")
            out.append("  - 头部标注 `**状态**:**方法论版(待现场复测)**`,版本置 v0.9.0")
            out.append("  - Section 一/二:从案例抽取干扰源、受扰体、耦合路径、谐波命中表")
            out.append("  - Section 三/四:参照 sibling 的软件/硬件步骤骨架,按案例调整黄金动作")
            out.append("  - Section 六:本案例作为首源案例完整写入,含教训反思")
            out.append("  - Section 八:交叉引用 matrix.yaml / bandwidth-discrimination / sibling SOP")
        elif state == "v0.9":
            out.append("- **Proposed action**: **追加 Section 六 案例 + 更新反哺引用**")
            out.append("  - 在「六、典型案例」追加本案例(机型、持续天数、根因、最终方案、教训)")
            out.append("  - 检查并更新「八、附录·参考文档」与「更新记录」表")
            out.append("  - 若本案例暴露新的排查步骤,追加到 Section 三/四(标注反哺版本号)")
            out.append("  - 版本号 v0.9.x → v0.9.(x+1),日期更新")
        else:  # formal
            out.append("- **Proposed action**: **仅追加 Section 六 典型案例**")
            out.append("  - 正式 SOP 骨架稳定,只在「六、典型案例」末尾追加本案例")
            out.append("  - 不动 Section 一 ~ 五、七、八")
            out.append("  - 版本号 v1.x.y → v1.x.(y+1) 作为 case addition 版本")

        out.append("")

    out.append("## 后续(Claude 执行)")
    out.append("")
    out.append("1. 按上述每条 Proposed action 使用 Read 读取 SOP 当前内容")
    out.append("2. 使用 Edit(小改动) 或 Write(全量重写 stub) 落盘")
    out.append("3. 完成后由 `engineering-logger` 技能记录日志")
    out.append("4. 运行 `python3 tools/check-architecture-consistency.py` 校验行数/章节/版本号")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Main                                                                        #
# --------------------------------------------------------------------------- #

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 tools/case_to_sop.py <case-file.md>", file=sys.stderr)
        return 2
    case_path = Path(sys.argv[1]).resolve()
    if not case_path.exists():
        print(f"error: case file not found: {case_path}", file=sys.stderr)
        return 2
    # repo root = this script's parent's parent
    base = Path(__file__).resolve().parent.parent
    print(render_plan(case_path, base))
    return 0


if __name__ == "__main__":
    sys.exit(main())
