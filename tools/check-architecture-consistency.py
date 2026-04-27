#!/usr/bin/env python3
"""Echo 知识库架构一致性检查工具 (v2).

v2 扩展(2026-04-27):
  - matrix.yaml 与 SOP 文件存在性校验
  - 跨文件引用完整性校验(.md 中 knowledge/ 路径必须存在)
  - 自适应 SOP 行数阈值(待编写 stub / 正式 SOP 不同阈值)
  - 补 normal domain README 检查
  - source-list / victim-list 一致性(由 YAML 生成,只检查 banner)
"""

import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

GENERATED_BANNER = "由 tools/gen_matrix_views.py"


class ArchitectureChecker:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self._matrix_data = None

    # ----------------------- SOP 格式 -----------------------
    def check_sop_format(self):
        print("\n=== 检查 SOP 文件格式 ===")

        sop_files = list(self.base_path.glob("knowledge/sops/**/*.md"))

        required_sections = [
            "一、组合信息", "二、理论预判", "三、软件排查步骤",
            "四、硬件排查步骤", "五、结论模板", "六、典型案例",
            "七、检查表", "八、附录",
        ]

        for sop_file in sop_files:
            if sop_file.name == "_template.md":
                continue
            rel = sop_file.relative_to(self.base_path)
            content = sop_file.read_text(encoding="utf-8")
            lines = len(content.split("\n"))

            # 判定是否为待编写 stub
            is_stub = ("**状态**:**待编写**" in content
                       or "**状态**：待编写" in content
                       or "**待编写**" in content[:500])

            # 自适应行数阈值
            if is_stub:
                # stub 模板大小:容忍 120-300
                if lines < 120 or lines > 320:
                    self.warnings.append(f"{rel}: stub 行数异常 ({lines} 行),模板预期 120-300")
            else:
                # 正式 SOP:180-300
                if lines < 180:
                    self.warnings.append(f"{rel}: 文件过短 ({lines} 行),建议 180-250")
                elif lines > 300:
                    self.warnings.append(f"{rel}: 文件过长 ({lines} 行),建议精简")

            # 必备章节
            file_sections = re.findall(r"## [^\n]+", content)
            missing = [s for s in required_sections if not any(s in x for x in file_sections)]
            if missing:
                self.errors.append(f"{rel}: 缺失章节: {', '.join(missing)}")

            # 版本号
            if not re.search(r"\*\*版本\*\*[:：]v(\d+)\.(\d+)\.(\d+)", content):
                self.errors.append(f"{rel}: 版本号格式错误或缺失")

    # ----------------------- Matrix ↔ SOP 存在性 -----------------------
    def check_matrix_sop_existence(self):
        print("\n=== 检查 matrix.yaml 声明的 SOP 是否都有文件 ===")
        if yaml is None:
            self.warnings.append("matrix.yaml 检查跳过:未安装 PyYAML")
            return

        matrix_yaml = self.base_path / "knowledge/matrix/matrix.yaml"
        if not matrix_yaml.exists():
            self.errors.append("knowledge/matrix/matrix.yaml 不存在")
            return

        data = yaml.safe_load(matrix_yaml.read_text(encoding="utf-8"))
        self._matrix_data = data

        missing = []
        for m in data.get("mappings", []):
            sop = m["sop"]
            victim_code = sop.split("-", 1)[0]
            if victim_code == "NORMAL":
                path = self.base_path / f"knowledge/sops/NORMAL/SOP-{sop}.md"
            else:
                path = self.base_path / f"knowledge/sops/{victim_code}/{sop}.md"
            if not path.exists():
                missing.append((sop, str(path.relative_to(self.base_path))))

        if missing:
            for sop, p in missing:
                self.errors.append(f"matrix 声明 SOP-{sop} 但文件不存在: {p}")
            self.errors.append(f"(共 {len(missing)} 个悬空 SOP,用 `python3 tools/gen_sop_stubs.py` 生成 placeholder)")
        else:
            print(f"✓ matrix.yaml 声明的 {len(data.get('mappings', []))} 个 SOP 文件全部存在")

    # ----------------------- source-list / victim-list 生成标记 -----------------------
    def check_generated_views(self):
        print("\n=== 检查 source-list/victim-list 是否由生成器产出 ===")
        for name in ["matrix-table.md", "source-list.md", "victim-list.md"]:
            f = self.base_path / "knowledge/matrix" / name
            if not f.exists():
                self.errors.append(f"{name} 不存在,运行 `python3 tools/gen_matrix_views.py`")
                continue
            head = f.read_text(encoding="utf-8").splitlines()[:1]
            if not head or GENERATED_BANNER not in head[0]:
                self.warnings.append(f"{name} 未标记为自动生成,可能被手改(应由 matrix.yaml 生成)")
            else:
                print(f"✓ {name} 来自 matrix.yaml")

    # ----------------------- 跨文件引用 -----------------------
    def check_cross_references(self):
        print("\n=== 检查 Markdown 中 knowledge/ 路径引用完整性 ===")

        pattern = re.compile(r"\]\(((?:\.\./)*(?:knowledge|\.claude|tools|logs|docs)/[^)#]+?)(?:#[^)]*)?\)")
        md_files = []
        for base in ["knowledge", ".claude", "docs", "CLAUDE.md"]:
            p = self.base_path / base
            if p.is_dir():
                md_files.extend(p.rglob("*.md"))
            elif p.is_file():
                md_files.append(p)

        broken = 0
        checked = 0
        for md in md_files:
            content = md.read_text(encoding="utf-8", errors="ignore")
            for match in pattern.finditer(content):
                ref = match.group(1)
                # 相对于当前 md 文件解析
                resolved = (md.parent / ref).resolve()
                checked += 1
                if not resolved.exists():
                    # 仅报告 knowledge/ / .claude/ / tools/ 路径下的
                    self.warnings.append(
                        f"{md.relative_to(self.base_path)}: 引用不存在 `{ref}`"
                    )
                    broken += 1
        print(f"✓ 扫描 {len(md_files)} 个文件,{checked} 处引用,{broken} 处 broken")

    # ----------------------- domain README -----------------------
    def check_domain_readmes(self):
        print("\n=== 检查 domain/ 子目录 README ===")
        for domain in ["display", "camera", "normal"]:
            readme = self.base_path / f"knowledge/domain/{domain}/README.md"
            if readme.exists():
                print(f"✓ {domain} README 存在")
            else:
                self.errors.append(f"缺失 {domain} 领域 README: knowledge/domain/{domain}/README.md")

    # ----------------------- 决策树 Camera 分支 -----------------------
    def check_decision_tree_balance(self):
        print("\n=== 检查决策树 Camera 分支 ===")
        dt = self.base_path / "knowledge/decision-tree.md"
        if not dt.exists():
            self.errors.append("knowledge/decision-tree.md 不存在")
            return
        content = dt.read_text(encoding="utf-8")
        camera_match = re.search(r"## Camera 专用分支[^#]+", content, re.DOTALL)
        if camera_match:
            required = ["第一步", "第二步", "谐波命中计算", "参考SOP"]
            for elem in required:
                if elem not in camera_match.group(0):
                    self.warnings.append(f"决策树 Camera 分支缺失: {elem}")
        print("✓ 决策树 Camera 分支检查完成")

    # ----------------------- 术语一致性 -----------------------
    def check_terminology_consistency(self):
        print("\n=== 检查术语一致性(抽样)===")
        # 术语统一来自 knowledge/glossary.md(如果存在)
        glossary = self.base_path / "knowledge/glossary.md"
        if glossary.exists():
            print(f"✓ glossary.md 存在(术语单一来源)")
        else:
            self.warnings.append("knowledge/glossary.md 未创建;术语只在各 SOP 附录中分散定义,有漂移风险")

        standard_terms = ["Desense", "SSC", "MIPI", "耦合路径"]
        key_files = [
            "knowledge/sops/GL1/GL1-01.md",
            "knowledge/sops/GL1/GL1-02.md",
            "knowledge/domain/display/overview.md",
            "knowledge/domain/camera/overview.md",
        ]
        for fp in key_files:
            full = self.base_path / fp
            if not full.exists():
                continue
            content = full.read_text(encoding="utf-8")
            present = [t for t in standard_terms if t in content]
            if present:
                print(f"✓ {fp}: 使用 {len(present)}/{len(standard_terms)} 个标准术语")

    # ----------------------- harness 层完整性 -----------------------
    def check_harness(self):
        print("\n=== 检查 .claude/ harness 完整性 ===")
        required = {
            ".claude/agents/echo.md": "echo subagent",
            ".claude/commands/diagnose.md": "/diagnose",
            ".claude/commands/matrix.md": "/matrix",
            ".claude/commands/formal.md": "/formal",
            ".claude/commands/playground.md": "/playground",
        }
        for rel, desc in required.items():
            p = self.base_path / rel
            if not p.exists():
                self.errors.append(f"harness 文件缺失: {rel} ({desc})")
                continue
            content = p.read_text(encoding="utf-8")
            if not content.startswith("---"):
                self.warnings.append(f"{rel}: 缺少 YAML frontmatter")

        # skills
        skills_dir = self.base_path / ".claude/skills"
        if skills_dir.exists():
            for skill_file in skills_dir.glob("*/SKILL.md"):
                content = skill_file.read_text(encoding="utf-8")
                if not content.startswith("---"):
                    self.warnings.append(f"{skill_file.relative_to(self.base_path)}: 缺少 YAML frontmatter")
                elif "compatibility: opencode" in content:
                    self.errors.append(f"{skill_file.relative_to(self.base_path)}: 仍含 `compatibility: opencode`,应清理")

    # ----------------------- 报告 -----------------------
    def generate_report(self):
        print("\n" + "=" * 60)
        print("架构一致性检查报告")
        print("=" * 60)

        if self.errors:
            print("\n❌ 错误项:")
            for e in self.errors:
                print(f"  - {e}")
        else:
            print("\n✅ 无严重错误")

        if self.warnings:
            print("\n⚠️  警告项:")
            for w in self.warnings:
                print(f"  - {w}")
        else:
            print("\n✅ 无警告项")

        total = len(self.errors) + len(self.warnings)
        if total == 0:
            print("\n🎉 架构一致性优秀!")
        elif not self.errors:
            print(f"\n📊 架构一致性良好,有 {len(self.warnings)} 项可优化")
        else:
            print(f"\n🔧 需要修复 {len(self.errors)} 项错误和 {len(self.warnings)} 项警告")
        return not self.errors


def main():
    base = Path(__file__).parent.parent
    checker = ArchitectureChecker(base)
    print("开始 Echo 知识库架构一致性检查 (v2)...")

    checker.check_sop_format()
    checker.check_matrix_sop_existence()
    checker.check_generated_views()
    checker.check_cross_references()
    checker.check_domain_readmes()
    checker.check_decision_tree_balance()
    checker.check_terminology_consistency()
    checker.check_harness()

    ok = checker.generate_report()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
