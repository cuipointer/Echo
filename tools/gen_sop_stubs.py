#!/usr/bin/env python3
"""从 matrix.yaml 为缺失的 SOP 生成 placeholder 文件。

每个 placeholder 保留完整的 8 章节骨架(满足 linter),状态标记为 `待编写`,
在 "一、组合信息" 里从 yaml 填入源 / 受扰体 / 机制等,其他章节保留 TODO 占位。

用法:
  python3 tools/gen_sop_stubs.py [--dry-run]

--dry-run 只列出会生成哪些文件,不实际写入。
"""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("错误:需要 PyYAML", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).parent.parent
MATRIX_YAML = ROOT / "knowledge/matrix/matrix.yaml"
SOPS_DIR = ROOT / "knowledge/sops"


TEMPLATE = """
# SOP-{sop}:{source_label} → {victim_label}

**版本**:v0.1.0
**日期**:2026-04-27
**状态**:**待编写**(placeholder,由 `tools/gen_sop_stubs.py` 从 matrix.yaml 生成)

> **提醒**:本文件是占位 SOP,内容为模板骨架 + 矩阵数据回填,**没有实测验证**。
> 现场使用前请按 [_template.md](../_template.md) 补全各章节内容,并将状态改为 `进行中` 或 `已完成`。
> 对应 case 应沉淀到 `knowledge/cases/`。

---

## 一、组合信息

### 干扰源
- **模块**:{source_label}
- **代码**:{source_code}
- **分类**:{source_category}
- **基频范围**:{source_base_freq}
- **噪声来源**:{source_noise}
- **典型干扰**:{source_typical}

### 受扰体
- **频段**:{victim_label}
- **代码**:{victim_code}
- **频率范围**:{victim_freq}
- **敏感度要求**:{victim_sensitivity}

### 耦合路径
- **类型**:[待填:传导/辐射/串扰/地弹 — 参考 methodology/three-elements.md]
- **机制**:{mechanism}

### 矩阵元信息
- **优先级**:{tier} {priority_tag}
- **典型恶化量**:{degradation}
- **快速诊断提示**:{hint}

---

## 二、理论预判

### 谐波命中计算

[待填:根据干扰源基频计算谐波,验证是否落入受扰体频段]

示例格式:
- 基频:{source_base_freq}
- 受扰体频段:{victim_freq}
- 谐波:基频 × N = ___ MHz ✓/✗ 命中

可调用 `harmonic-calc` skill 或 `tools/harmonic_calc.py` 辅助计算。

### 设计审查必查项

[待填:从设计资料要查哪几项关键设计点,例如]
1. [干扰源时钟/电源规划]
2. [屏蔽设计完整性]
3. [滤波网络参数]
4. [天线与干扰源距离]

---

## 三、软件排查步骤

### 步骤 1:场景复现

**目标**:确认干扰现象可复现

**操作**:
1. 进入测试场景:[{hint}]
2. 测量受扰体灵敏度:记录 dBm 值
3. 记录干扰现象:描述恶化程度和稳定性

**预期结果**:干扰现象稳定复现,恶化 {degradation}

### 步骤 2:干扰源确认

**目标**:确认干扰源为 {source_label}

**操作**:
1. 关闭 {source_label} 对应功能,观察干扰是否消失
2. [其他排除性测试]

**预期结果**:确认干扰源模块

### 步骤 2.5:子功能逐项排查(零成本验证)

**目标**:[若干扰源有多个子功能,逐项关闭定位最强贡献者]

**操作**:[待填]

**预期结果**:[待填]

### 步骤 3:频率验证

**目标**:验证干扰频率与理论预判一致

**操作**:
1. 频谱仪观察 {victim_freq} 范围
2. 对比干扰源基频谐波

**预期结果**:频率关系与理论预判一致

### 步骤 4:软件规避尝试

**目标**:尝试软件措施改善干扰

**操作**:[根据干扰源类型填写]
1. [如时钟源 → 尝试 SSC 展频]
2. [如 Camera → 尝试降帧率/分辨率]
3. [如 Charger → 尝试不同充电功率]

**预期结果**:记录各项措施的改善 dB 值

---

## 四、硬件排查步骤

**触发条件**:软件措施无效或改善不足

### 步骤 1:路径确认

**目标**:确认耦合路径类型

**操作**:
1. 近场扫描:使用探头扫描干扰源区域
2. 屏蔽测试:临时屏蔽验证路径
3. [电源测量 / 天线隔离测试]

**预期结果**:确认主要耦合路径

### 步骤 2:硬件整改验证

**目标**:验证硬件整改措施

**操作**:[待填]
1. [屏蔽优化]
2. [滤波优化]
3. [布局调整]

**预期结果**:WiFi/LTE/GNSS 性能恢复到限值内

---

## 五、结论模板

### 问题分析

#### 干扰源
- **模块**:{source_label}
- **噪声来源**:{source_noise}
- **基频范围**:{source_base_freq}

#### 受扰体
- **频段**:{victim_label}
- **敏感度要求**:{victim_sensitivity}

#### 耦合路径
- **类型**:[传导/辐射/串扰/地弹]
- **机制**:{mechanism}

### 改善措施

#### 软件措施
1. [措施 1 — 改善 __ dB]
2. [措施 2]

#### 硬件措施
1. [措施 1 — 改善 __ dB]
2. [措施 2]

#### 长期措施
1. [设计规范]
2. [选型建议]

---

## 六、典型案例

### 案例 1:[待沉淀]

完成第一次实测后,将案例文件放到 `knowledge/cases/<机型>-<场景>-<频段>-<关键词>.md`,
并在此处引用:

- **问题描述**:[简要描述]
- **解决方案**:[关键措施]
- **参考链接**:[案例文件路径]

---

## 七、检查表

| 步骤 | 检查项 | 操作/填写内容 | 状态 |
|------|--------|---------------|------|
| 1.1 | 受扰频段确认 | {victim_label} | □ |
| 1.2 | 测试场景 | {hint} | □ |
| 2.1 | 谐波命中计算 | ____ MHz × ____ = ____ MHz | □ |
| 2.5 | 子功能排查 | [若适用] | □ |
| 3.1 | 频率验证 | 频谱仪截图 | □ |
| 4.1 | 软件规避尝试 | 措施 + 改善 dB | □ |
| 5.1 | 最终方案 | [填写最终采用的方案] | □ |

---

## 八、附录

### 术语表
- **Desense**:De-sensitization,灵敏度恶化
- **SSC**:Spread Spectrum Clocking,展频时钟
- **MIPI**:Mobile Industry Processor Interface

完整术语见 [knowledge/glossary.md](../../glossary.md)。

### 参考文档
- [矩阵表(源)](../../matrix/matrix.yaml)
- [三要素模型](../../methodology/three-elements.md)
- [决策树](../../decision-tree.md)
- [Camera 域](../../domain/camera/){{若适用}}
- [Display 域](../../domain/display/){{若适用}}
- [Normal 域](../../domain/normal/){{若适用}}
"""


def sop_to_path(sop: str) -> Path:
    """SOP 编号 → 文件路径。W24-01 → sops/W24/W24-01.md;NORMAL-01 → sops/NORMAL/SOP-NORMAL-01.md"""
    victim_code = sop.split("-", 1)[0]
    if victim_code == "NORMAL":
        return SOPS_DIR / "NORMAL" / f"SOP-{sop}.md"
    return SOPS_DIR / victim_code / f"{sop}.md"


def render_stub(m: dict, sources: dict, victims: dict) -> str:
    s = sources[m["source"]]
    v = victims[m["victim"]]
    if v.get("is_baseline"):
        freq = "(基准场景)"
        sens = "—"
    else:
        fr = v["freq_range_mhz"]
        freq = f"{fr[0]}-{fr[1]} MHz" if fr[0] != fr[1] else f"{fr[0]} MHz"
        sens_range = v["sensitivity_dbm"]
        sens = f"{sens_range[0]} ~ {sens_range[1]} dBm"

    return TEMPLATE.format(
        sop=m["sop"],
        source_label=s["label"],
        source_code=s["code"],
        source_category=s["category"],
        source_base_freq=s["base_freq_range"],
        source_noise=s["noise_source"],
        source_typical=s["typical_interference"],
        victim_label=v["label"],
        victim_code=v["code"],
        victim_freq=freq,
        victim_sensitivity=sens,
        mechanism=m.get("mechanism", "[待填]"),
        tier=m.get("tier", "P2"),
        priority_tag=("⭐ 高优先级" if m.get("high_priority") else ""),
        degradation=m.get("typical_degradation", "[待测]"),
        hint=m.get("diagnosis_hint", "[待填]"),
    ).lstrip()


def main():
    dry_run = "--dry-run" in sys.argv

    with open(MATRIX_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 按 SOP 编号去重(OSC 和 LCD_MIPI 可能共享 SOP),挑第一个映射作为代表
    unique_sops = {}
    for m in data["mappings"]:
        unique_sops.setdefault(m["sop"], m)

    missing = []
    existing = []
    for sop, m in unique_sops.items():
        path = sop_to_path(sop)
        if path.exists():
            existing.append((sop, path))
        else:
            missing.append((m, path))

    print(f"Matrix 声明(去重): {len(unique_sops)} 个唯一 SOP")
    print(f"已存在:              {len(existing)}")
    print(f"缺失:                {len(missing)}")

    if dry_run:
        print("\n=== dry-run,下列文件将被生成 ===")
        for m, p in missing:
            print(f"  {m['sop']:<12} → {p.relative_to(ROOT)}")
        return

    if not missing:
        print("无缺失,无需生成")
        return

    print(f"\n生成 {len(missing)} 个 placeholder...")
    for m, path in missing:
        path.parent.mkdir(parents=True, exist_ok=True)
        content = render_stub(m, data["sources"], data["victims"])
        path.write_text(content, encoding="utf-8")
        print(f"  ✓ {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
