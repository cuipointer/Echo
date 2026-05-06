# Echo·Desense Phase 2 Sprint 计划

**Sprint 版本**:Sprint 1 of Phase 2
**起始日期**:2026-05-06
**计划工期**:10 个工作日(2 周)
**负责人**:射频天线项目接口人(Cuihan)

---

## 一、Sprint 目标

**10 天内交付 3 件大事**:

1. **技术债修复**:修复 `main/develop` 分支偏离,重建 git-workflow 执行节奏
2. **框架反哺**:把刚完成的 9 个 2024 EMC Desense 案例分析中识别的 6 条架构建议**落地到 matrix.yaml / 方法论 / SOP 模板**
3. **P0 SOP 填充**:把 3 个高频 P0 SOP(LLB-07 / W24-03 / LHB-04)从 placeholder(`v0.1 待编写`)升级到**方法论版 v0.9**(待现场复测)

**Sprint 里程碑**:打 `v2.1.0` tag,标记 Phase 2 第一轮交付完成。

---

## 二、当前状态快照(Sprint 起始)

### 分支与 tag

| 项 | 状态 |
|---|---|
| `main` | `c95cdb9`(领先 develop 3 commit,包含 EMC triage + 架构图材料) |
| `develop` | `65de8f9`(v2.0.0,**已落后 main 3 commit**) |
| `v2.0.0` tag | 打在 develop 上(应该在 main HEAD 更合理,但向前看不做迁移) |
| `case/emc-2024-triage` | 与 main HEAD 一致(已合并) |
| 远端 `origin` | GitHub `cuipointer/Echo` |

### 内容指标

| 指标 | 值 |
|---|:---:|
| Formal SOP 数 | **13** |
| Stub SOP 数 | 28 |
| 案例库 | 2(AS2-RC-WiFi24-OIS + EMC-2024-Desense-triage) |
| matrix.yaml sources | 15 |
| matrix.yaml mappings | 47 |
| `/diagnose` 版本 | v2.0 |
| linter 状态 | 0 错 0 警 ✅ |

### 待落地技术债(来自 EMC 案例分析)

1. `matrix.yaml` 缺 `NFC` 源(B.2 案例)
2. `matrix.yaml` 缺 `SHIELD_LEAK → W24` 映射(A.2 案例)
3. 方法论没沉淀"宽窄带判别自动判据"(已在 `/diagnose` Step 3 体现,但缺独立文档)
4. SOP 模板缺"步骤 2.6 多源叠加排查法"
5. 9 个 EMC 案例中的 C.1 / B.2 **两个高价值案例**嵌在 triage 文件里,未拆分为独立案例
6. 3 个 P0 SOP 仍是 placeholder(LLB-07 / W24-03 / LHB-04)

---

## 三、任务清单

### Week 1:技术债修复 + EMC 反哺(Day 1-5)

#### T1.1 — 分支同步(Day 1 上午,0.5 天)

- **分支**:无(直接 git 操作)
- **动作**:
  1. `git checkout develop && git merge main`(fast-forward)
  2. 决定 tag 策略:`v2.0.0` 保持在 65de8f9 不动(它确实是 Phase 1 本体);后续 Sprint 结束时在 main HEAD 打 `v2.1.0`
  3. `git push origin develop main` 同步远端
- **验收**:`git log main..develop --oneline` 和 `git log develop..main --oneline` 都为空
- **风险**:低(fast-forward 关系)

#### T1.2 — matrix.yaml 扩容(Day 1 下午,0.5 天)

- **分支**:`feature/echo-framework-feedback`(从 develop 拉)
- **动作**:
  1. 编辑 [knowledge/matrix/matrix.yaml](../knowledge/matrix/matrix.yaml):
     - 新增 source `NFC`(category: 共存;base_freq: 13.56 MHz;典型干扰:高次谐波命中 2.4G)
     - 新增 mapping `NFC → W24`(tier P1,typical_degradation: 10-20 dB,对应新 SOP `W24-08`)
     - 新增 source `CPU_SHIELD`(或扩展现有 `SHIELD_LEAK` 语义)→ `W24` 映射(tier P1,对应 `W24-09`)
  2. 更新 version 到 2.1.0 + changelog 条目
  3. 跑生成器:`python3 tools/gen_matrix_views.py`
  4. 验证生成的 matrix-table.md / source-list.md / victim-list.md
- **交付**:`matrix.yaml` + 3 个视图 md(自动生成)
- **复用**:[tools/gen_matrix_views.py](../tools/gen_matrix_views.py)
- **验收**:linter 0/0;运行 `python3 tools/gen_sop_stubs.py` 为 2 个新映射生成 stub(W24-08 / W24-09)

#### T1.3 — 方法论沉淀:宽窄带判别(Day 2,1 天)

- **分支**:同 `feature/echo-framework-feedback`
- **动作**:新建 `knowledge/methodology/bandwidth-discrimination.md`(将创建),内容:
  1. 为什么要做宽窄带判别(进入决策树前的架构级大类筛选)
  2. **自动判据**:
     - 单频点/单信道 ≥ 10 dB → 窄带谐波命中
     - 多信道平坦度差 ≥ 3 dB → 宽带平台泄露 / 电源 SSN / 屏蔽不良
     - 随 MIPI 配置变化 → MIPI Clock/Data 相关
     - 场景激活即恶化 → 场景设备自身或同频共存
  3. 3 个反例(帮助识别误判场景)
  4. 与三要素模型的关系
  5. 援引案例(AS2 案例 + 9 个 EMC 案例中的 A.1/A.2/B.1 等作为例证)
- **交付**:新文档 + `knowledge/methodology/README.md`(如存在)更新引用

#### T1.4 — SOP 模板 + /diagnose 更新(Day 3 上午,0.5 天)

- **分支**:同 `feature/echo-framework-feedback`
- **动作**:
  1. 在 [knowledge/sops/_template.md](../knowledge/sops/_template.md) "三、软件排查步骤" 新增 **步骤 2.6 多源叠加排查法**:
     - 触发条件:步骤 2.5 子功能排查后仍有显著 Desense;或现象表现为"多场景共同恶化但差异大"
     - 操作:逐一**隔离验证**每个可疑源的贡献(关 A 看改善 → 关 B 看改善 → 两者都关看总改善 → 推断是否叠加)
     - 决策逻辑表
  2. 在 [.claude/commands/diagnose.md](../.claude/commands/diagnose.md) Step 3 宽窄带判别章节引用新文档(`knowledge/methodology/bandwidth-discrimination.md`),版本升到 v2.1
- **交付**:`_template.md` 改动 + `diagnose.md` v2.1

#### T1.5 — 拆分 EMC 案例(Day 3 下午,0.5 天)

- **分支**:同 `feature/echo-framework-feedback`
- **动作**:
  1. 新建 `knowledge/cases/O11-DDR-LLB-aperture.md`(将创建):从 `EMC-2024-Desense-triage.md` C.1 段抽出,补充独立案例 frontmatter
  2. 新建 `knowledge/cases/O2-NFC-W24.md`(将创建):从 B.2 段抽出
  3. 在 `EMC-2024-Desense-triage.md` 的 C.1 / B.2 段末尾加引用"详见拆出的独立案例"
- **交付**:2 个新案例文件,案例库 2 → 4

#### T1.6 — Week 1 收尾(Day 4,0.5 天)+ 冷却合入 main(Day 5,0.5 天)

- **分支操作**:
  1. `python3 tools/check-architecture-consistency.py` 确认 0/0
  2. `feature/echo-framework-feedback` → `develop`(`git merge --no-ff`)
  3. 冷却 24 小时(Day 4 完 → Day 5 再看)
  4. self-review 清单过一遍 → `develop` → `main`(`git merge --no-ff`)
  5. `git push origin main develop` 同步远端
- **交付**:Week 1 所有变更已在 main,远端同步

---

### Week 2:P0 SOP 填充(Day 6-10)

**重要**:由于**无现场实测数据**,Week 2 的 SOP 填充为**方法论版 v0.9**,明确标记"待现场复测"。不直接升到 v1.0。

#### T2.1 — LLB-07(充电器 → LTE LB)(Day 6-7,1.5 天)

- **分支**:`sop/llb-07`(从 develop 拉)
- **关键文件**:[knowledge/sops/LLB/LLB-07.md](../knowledge/sops/LLB/LLB-07.md)
- **填充来源**:
  - 参考 EMC C.1(O11 B8/B5/B26 DDR,相近但不相同)
  - 参考 [LLB-04](../knowledge/sops/LLB/LLB-04.md)(PMIC Buck → LTE LB,同受扰体)
  - 结合 Charger IC 特性(500 kHz - 2 MHz 开关)
- **交付**:LLB-07 从 v0.1 → v0.9,含完整 8 章节;版本标记"方法论版待复测"
- **分支合并**:完成后 → develop

#### T2.2 — W24-03(DDR → WiFi 2.4G)(Day 8-9,1.5 天)

- **分支**:`sop/w24-03`
- **关键文件**:[knowledge/sops/W24/W24-03.md](../knowledge/sops/W24/W24-03.md)
- **填充来源**:
  - 参考 EMC C.1 / C.2 的 DDR 场景
  - 参考 [W24-01](../knowledge/sops/W24/W24-01.md) 已有的屏蔽罩/滤波 SOP 结构
  - 结合 DDR 频率(200-933 MHz)谐波命中 WiFi 2.4G 的计算
- **交付**:W24-03 v0.9
- **分支合并**:完成后 → develop

#### T2.3 — LHB-04(USB3 → LTE HB)(Day 10 上午,1 天)

- **分支**:`sop/lhb-04`
- **关键文件**:[knowledge/sops/LHB/LHB-04.md](../knowledge/sops/LHB/LHB-04.md)
- **填充来源**:
  - 参考 [W5-04](../knowledge/sops/W5/W5-04.md)(USB3 → WiFi 5G,同干扰源不同受扰体)—— 主要结构复用
  - USB 3.0 基频 2.5 GHz,LTE HB 2300-3700 MHz 有直接频率命中风险
- **交付**:LHB-04 v0.9
- **分支合并**:完成后 → develop

#### T2.4 — Sprint 收尾(Day 10 下午,1 天)

- **动作**:
  1. 更新 [CHANGELOG.md](../CHANGELOG.md) 加 **v2.1.0** 条目(EMC 反哺 + 3 P0 SOP 方法论版)
  2. `develop` → `main`(`git merge --no-ff`)
  3. 打 tag:`git tag -a v2.1.0 -m "v2.1.0 - Phase 2 Sprint 1 完成..."`
  4. `git push origin main develop v2.1.0` 全量推远端
  5. 更新 [logs/daily/](../logs/daily/) 写 Day 10 的收官日志
- **交付**:v2.1.0 tag + 远端同步

---

## 四、验收标准

Sprint 结束(Day 10 结束时)必须满足:

| 指标 | 现状 | 目标 |
|---|:---:|:---:|
| linter 错误/警告 | 0/0 | **0/0** 持续 |
| develop ↔ main 同步 | main 领先 3 | **完全同步 + v2.1.0 tagged** |
| Formal SOP 数(含 v0.9 方法论版) | 13 | **16**(+3 P0) |
| Stub SOP 数 | 28 | 27(少 3 个 P0)或 29(多 2 个 W24-08/09 stub) |
| 案例库 | 2 | **4** |
| matrix.yaml sources | 15 | **16+**(+NFC 至少) |
| matrix.yaml mappings | 47 | **49+**(+NFC→W24,+CPU_SHIELD→W24) |
| `/diagnose` 版本 | v2.0 | **v2.1** |
| 方法论文档 | 4 | **5**(+宽窄带判别) |
| CHANGELOG 最新版本 | v2.0.0 | **v2.1.0** |
| 远端 push | 部分 | **全分支 + tag 在远端** |

### 验证命令

```bash
cd /home/cuihan/workspace/workspace-claude

# 1. linter
python3 tools/check-architecture-consistency.py

# 2. 生成器幂等性
python3 tools/gen_matrix_views.py
python3 tools/gen_sop_stubs.py --dry-run  # 应显示无缺失

# 3. 分支同步
git log main..develop --oneline  # 应为空
git log develop..main --oneline  # 应为空

# 4. Tag
git tag -l | grep v2.1.0         # 应有

# 5. SOP 数量
find knowledge/sops -name '*.md' ! -name '_template.md' \
  | xargs grep -L '状态.*待编写' | wc -l  # 应 ≥ 16

# 6. 案例数
ls knowledge/cases/*.md | wc -l  # 应 ≥ 4

# 7. 远端同步
git log origin/main..main --oneline     # 应为空
git log origin/develop..develop --oneline  # 应为空
```

---

## 五、不做什么(明确 Scope)

以下不纳入本 Sprint,留给后续:

- ❌ **Phase 3 自动化**:linter 接入 PostToolUse hook、case→SOP 自动化 skill、决策树-矩阵一致性校验
- ❌ **Phase 4 扩展**:RSE / EMC / SAR 扩展进驻 extensions/
- ❌ **Phase 5 工具链**:Web UI / 测量工具集成 / 知识图谱
- ❌ **Token Plan 材料**(由独立流程跟进)
- ❌ **剩余 25 个 stub SOP 填充**(Sprint 2/3 任务)
- ❌ **现场实测复测**(本 Sprint 的 SOP 是方法论版 v0.9,待后续现场项目穿插复测升到 v1.0)
- ❌ **案例库扩充到 8 个**(Phase 2 长期目标,本 Sprint 只拆 2 个)

---

## 六、风险与应对

| 风险 | 等级 | 应对 |
|---|:---:|---|
| Week 2 无现场数据,SOP 内容质量不如实测 | 高 | 降级到 v0.9 方法论版;在文件 frontmatter 明确标注"待现场复测";写明"本 SOP 结构基于方法论推导,具体参数需项目复测确认" |
| 分支同步遇到冲突 | 低 | 当前是 fast-forward 关系,直接 merge |
| 远端 push 权限问题(新 GitHub 仓库) | 低 | T1.1 单独验证 push,若失败隔离为独立 task |
| 节奏从架构切到内容可能注意力丢失 | 中 | Week 1 与 Week 2 物理分隔,每天一个明确 DoD(Definition of Done) |
| EMC 反哺涉及多个文件同时改,破坏性大 | 中 | 都在同一个 feature 分支,冷却 24h 后再合 main,linter 全程守护 |

---

## 七、冷却期 & 合入节奏

遵循 [docs/git-workflow.md](git-workflow.md):

```
feature/echo-framework-feedback   ──┐
sop/llb-07                        ──┤
sop/w24-03                        ──┼──→ develop ──[冷却 24h]──→ main ──[tag v2.1.0]──→ origin
sop/lhb-04                        ──┘
```

每次合 develop 前:linter 0/0 + self-review clist 过
每次合 main 前:冷却 24h + 再扫一遍 `git log develop..main`

---

## 八、Sprint 结束后的下一步

完成 v2.1.0 后,根据结果决策 Sprint 2 内容:

- **如果有新项目现场可复测**:Sprint 2 优先把 v0.9 方法论版 SOP 升到 v1.0 实测版
- **如果现场不便**:Sprint 2 转向 **Phase 3 自动化序章**(先接 linter hook,降低未来维护成本)
- **如果发现新案例**:案例库补充,驱动新 SOP 反哺

Phase 3 启动条件:
- Formal SOP ≥ 20(超过本 Sprint 目标)
- 案例库 ≥ 8
- 手工沉淀成本过高(case→SOP 反哺 > 2 小时/案例)

---

## 参考

- 上游路线图:[docs/development-plan.md](development-plan.md)
- Git 工作流:[docs/git-workflow.md](git-workflow.md)
- 变更历史:[CHANGELOG.md](../CHANGELOG.md)
- EMC 案例分析源:[knowledge/cases/EMC-2024-Desense-triage.md](../knowledge/cases/EMC-2024-Desense-triage.md)
- 矩阵真相源:[knowledge/matrix/matrix.yaml](../knowledge/matrix/matrix.yaml)
- 架构守护:[tools/check-architecture-consistency.py](../tools/check-architecture-consistency.py)

---

**更新约定**:本 Sprint 计划在执行中若出现范围变更(加/减任务),必须在本文件末尾"更新记录"补一条,并同步到 CHANGELOG.md。

## 更新记录

| 日期 | 动作 | 备注 |
|---|---|---|
| 2026-05-06 | 创建 Sprint 1 计划 | 基于 4-27 Phase 1 完成后的 9 天停滞状态制定 |
