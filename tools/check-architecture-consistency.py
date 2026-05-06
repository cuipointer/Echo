#!/usr/bin/env python3
"""Echo 知识库架构一致性检查工具 (v2).

v2 扩展(2026-04-27):
  - matrix.yaml 与 SOP 文件存在性校验
  - 跨文件引用完整性校验(.md 中 knowledge/ 路径必须存在)
  - 自适应 SOP 行数阈值(待编写 stub / 正式 SOP 不同阈值)
  - 补 normal domain README 检查
  - source-list / victim-list 一致性(由 YAML 生成,只检查 banner)

v2.1 扩展(2026-05-06):
  - 新增决策树↔矩阵源一致性校验:确保 decision-tree.md 覆盖的干扰源
    与 matrix.yaml 中声明的 sources 相互对齐,
    支持 matrix source 标记 `decision_tree_bypass: true` 跳过反向可达性检查。
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
            # 判定是否为 v0.9 方法论版(比正式 SOP 允许更长,因含 EMC 案例反哺内容)
            is_methodology = "方法论版" in content[:600]

            # 自适应行数阈值
            if is_stub:
                # stub 模板大小:容忍 120-300
                if lines < 120 or lines > 320:
                    self.warnings.append(f"{rel}: stub 行数异常 ({lines} 行),模板预期 120-300")
            elif is_methodology:
                # v0.9 方法论版:180-500(含案例启示 / 多源叠加 / 双案例对比等扩展章节)
                if lines < 180:
                    self.warnings.append(f"{rel}: 方法论版过短 ({lines} 行),建议 ≥ 200")
                elif lines > 500:
                    self.warnings.append(f"{rel}: 方法论版过长 ({lines} 行),建议精简到 ≤ 450")
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

    # ----------------------- 决策树 ↔ matrix 源一致性 -----------------------
    def check_decision_tree_matrix_alignment(self):
        """验证 decision-tree.md 引导的"可疑干扰源"集合与 matrix.yaml 的 sources 集合一致。

        对齐策略:
          - 为每个 matrix source 生成"别名集"(source key + code + label 中的关键词),
            例如 LCD_MIPI → {"LCD_MIPI", "LCD MIPI", "LC"}; VIB_MOTOR → {"VIB_MOTOR", "VIB Motor", "VIB PWM", "VB"}
          - 若 matrix source 标记了 `decision_tree_bypass: true`,则不要求决策树提及,跳过正向缺口
          - 对决策树中提取到的 ALL_CAPS token(长度 ≥ 3),若无法匹配到任何 matrix source 的别名,记 warn(可能是拼写或孤立引用)

        仅使用 warn,避免过度误报阻塞 CI。
        """
        print("\n=== 检查决策树 ↔ matrix.yaml 源一致性 ===")
        if yaml is None:
            self.warnings.append("决策树↔矩阵源对齐检查跳过:未安装 PyYAML")
            return

        dt_path = self.base_path / "knowledge/decision-tree.md"
        matrix_path = self.base_path / "knowledge/matrix/matrix.yaml"
        if not dt_path.exists() or not matrix_path.exists():
            self.errors.append("决策树或 matrix.yaml 缺失,跳过一致性检查")
            return

        dt_content = dt_path.read_text(encoding="utf-8")
        data = self._matrix_data
        if data is None:
            data = yaml.safe_load(matrix_path.read_text(encoding="utf-8"))
            self._matrix_data = data

        sources = data.get("sources", {}) or {}

        # 为每个 source 构造别名集(覆盖中英文、代码、常见简称)
        def build_aliases(key: str, info: dict) -> set[str]:
            aliases: set[str] = set()
            aliases.add(key)
            aliases.add(key.replace("_", " "))
            code = info.get("code") or ""
            if code:
                aliases.add(code)
            label = info.get("label") or ""
            if label:
                # 原始 label
                aliases.add(label)
                # 去括号内容后的主名
                stripped = re.sub(r"\s*[\(（][^)）]*[\)）]\s*", "", label).strip()
                if stripped:
                    aliases.add(stripped)
                # 括号内的 token(如 "系统电源 (PMIC)" 中的 PMIC)
                for m in re.findall(r"[\(（]([^)）]+)[\)）]", label):
                    aliases.add(m.strip())
            # 手工扩展常见别名(决策树中习惯写法)
            extra = {
                "VIB_MOTOR": {"VIB PWM", "马达", "VIB"},
                "SPEAKER_PA": {"Speaker PA", "外放"},
                "USB3": {"USB 3.0", "USB3.0"},
                "LCD_MIPI": {"LCD MIPI", "MIPI"},
                "CAMERA_MIPI": {"Camera MIPI"},
                "NONLINEAR": {"非线性"},
                "PA_MATCH": {"PA 匹配", "匹配"},
                "SHIELD_LEAK": {"屏蔽"},
                "ANTENNA_TUNER": {"Tuner"},
                "BAD_CONNECTION": {"连接不良", "电连接"},
                "RF_POWER": {"射频电源"},
            }
            aliases.update(extra.get(key, set()))
            return {a for a in aliases if a}

        # 若决策树引用了 "NORMAL系列" / "NORMAL SOP",则视其为 Normal 分支的概括性入口,
        # 所有 mapping 到 NORMAL victim 的 source 都被视为"经 Normal 分支可达",放过缺口。
        normal_branch_referenced = bool(
            re.search(r"NORMAL\s*系列|NORMAL\s*SOP|NORMAL-0\d", dt_content)
        )
        sources_via_normal: set[str] = set()
        if normal_branch_referenced:
            for m in data.get("mappings", []) or []:
                if m.get("victim") == "NORMAL":
                    sources_via_normal.add(m.get("source"))

        matched_sources: list[str] = []
        missing_in_tree: list[str] = []
        for key, info in sources.items():
            if not isinstance(info, dict):
                continue
            if info.get("decision_tree_bypass") is True:
                continue
            aliases = build_aliases(key, info)
            hit = any(alias in dt_content for alias in aliases)
            if not hit and key in sources_via_normal:
                hit = True  # 经 Normal 分支可达
            if hit:
                matched_sources.append(key)
            else:
                missing_in_tree.append(key)

        # 反向:从决策树抽取 ALL_CAPS token(3+ 字符)
        dt_tokens = set(re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", dt_content))
        # 过滤掉明显非源的关键词(频段/受扰体代码/常见缩写)
        noise_tokens = {
            "SOP", "NORMAL", "MIPI", "PWM", "DDR",  # 部分是 source,这里按下面校验
            "WIFI", "GNSS", "LTE", "APP", "ADB", "CSI", "DSI",
            "MCLK", "AVDD", "DCDC", "VCM", "LED", "TP", "DDIC",
            "PIM", "EMC", "SSC", "SSN", "LB", "MB", "HB", "TVS", "ESD",
            "W24", "W5", "LLB", "LHB", "GL1", "GL5",
            "OFF", "ON", "OK",
            # 常见术语 / 非源缩写
            "CPU", "FPC", "LCD", "SPK", "USB", "PA", "RF",
            "B46",  # LTE-U 频段标签
        }
        # 收集 matrix 中所有已知 alias(用于判定 token 是否是源)
        all_aliases: set[str] = set()
        for key, info in sources.items():
            if isinstance(info, dict):
                all_aliases.update(build_aliases(key, info))
        unknown_tokens = []
        for tok in sorted(dt_tokens):
            if tok in noise_tokens:
                continue
            # 若 token 能匹配到 matrix 别名集任一元素,视为已对齐
            if tok in all_aliases:
                continue
            # 兼容大小写:是否与 source key 大写形式匹配
            if tok in sources:
                continue
            unknown_tokens.append(tok)

        # 报告
        if missing_in_tree:
            for key in missing_in_tree:
                label = sources[key].get("label", key)
                self.warnings.append(
                    f"matrix source `{key}` ({label}) 在 decision-tree.md 中未找到引用;"
                    f"若为有意不可达,请在 matrix.yaml 中为该源加 `decision_tree_bypass: true`"
                )

        if unknown_tokens:
            # 仅报 top-5,避免噪声
            shown = unknown_tokens[:5]
            self.warnings.append(
                f"decision-tree.md 含 {len(unknown_tokens)} 个疑似未知源 token(前 5): "
                f"{', '.join(shown)};请核查是否应纳入 matrix.yaml"
            )

        print(f"✓ matrix sources: {len(sources)} 个, 决策树匹配: {len(matched_sources)} 个, 缺口: {len(missing_in_tree)} 个")

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
    checker.check_decision_tree_matrix_alignment()

    ok = checker.generate_report()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
