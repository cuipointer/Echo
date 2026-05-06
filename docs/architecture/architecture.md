# Echo·Desense 架构与工作流

**当前版本**:v2.1.0(2026-05-06 Sprint 1 完成)

## 1. 系统架构：多 Agent 协作

```mermaid
flowchart TB
    User([工程师自然语言输入<br/>"RC 场景 WiFi 2.4G 灵敏度恶化 5dB"])

    subgraph Harness["Claude Code / Claude Agent SDK"]
        direction TB
        Skills["Skills (自动触发)"]
        Commands["Slash Commands (工作流)"]
        Subagent["Subagent (人格/上下文隔离)"]
    end

    subgraph SK["Skills 层"]
        DD[diagnose-desense<br/>意图识别]
        HC[harmonic-calc<br/>谐波命中计算]
        SE[sop-executor<br/>SOP 引导]
        EL[engineering-logger<br/>日志归档]
    end

    subgraph CMD["Commands 层"]
        Diag["/diagnose<br/>诊断主流程"]
        Mat["/matrix<br/>矩阵查表"]
        Form["/formal<br/>正式报告"]
        Play["/playground<br/>临时调试"]
    end

    subgraph AG["Subagent 层"]
        Echo["echo<br/>Desense 专家人格<br/>三要素 + 四原则"]
    end

    subgraph KB["知识库 (83 文档)"]
        Meth[methodology/<br/>方法论 5 篇]
        Mtx[matrix/<br/>matrix.yaml + 3 视图<br/>16 源 × 7 体 × 49 映射]
        SOPs[sops/<br/>43 个 SOP<br/>17 正式 + 26 stub]
        Case[cases/<br/>4 个闭环案例]
    end

    subgraph Tools["Python / Shell 工具"]
        HCpy[harmonic_calc.py]
        LB[link_budget.py]
        Chk[check-architecture<br/>-consistency.py]
        Log[logger.py]
    end

    User --> DD
    DD --> Diag
    Diag --> Echo
    Echo --> Mat
    Mat --> SOPs
    Diag --> HC
    HC --> HCpy
    SOPs --> SE
    SE --> User
    User --> EL
    EL --> Log
    User --> Form
    Form --> Case
    Echo -.读.-> Meth
    Mat -.读.-> Mtx
```

## 2. 核心链路：一次 Desense 诊断的长链推理

```mermaid
sequenceDiagram
    autonumber
    participant U as 工程师
    participant S as diagnose-desense<br/>(Skill)
    participant E as echo<br/>(Subagent)
    participant D as /diagnose<br/>(Command)
    participant M as /matrix
    participant H as harmonic-calc
    participant X as sop-executor
    participant L as engineering-logger

    U->>S: "RC 场景 WiFi24 恶化 5dB"
    Note over S: 意图识别:<br/>受扰频段 + 场景 + 幅度
    S->>E: 注入 Desense 专家上下文
    E->>D: 调用诊断主流程

    Note over D: Step1 Normal 优先判定
    D->>U: "Normal Desense 测过吗?"
    U-->>D: "Normal ≤ 1dB"

    Note over D: Step2 宽窄带判别 (v2.1)
    D->>D: 单频 ≥10dB → 窄带谐波<br/>平坦度 ≥3dB → 宽带平台<br/>随 MIPI → FPC/BTB 辐射<br/>场景激活 → 共存/模块自身

    Note over D: Step3 决策树收敛
    D->>M: 干扰源×受扰体 查表
    M-->>D: 返回 SOP 编号 W24-02

    opt 窄带命中
        D->>H: 基频 × 谐波次数
        H-->>D: 命中 WiFi 2.4G 第 N 次谐波
    end

    D->>X: 按 SOP 引导现场测量
    X->>U: Step-by-step 测量指令
    U-->>X: 测量数据回传
    X-->>E: 生成三要素结论

    E-->>U: 输出干扰源/受扰体/<br/>耦合路径 + 改善措施

    U->>L: 任务完成
    L->>L: 写入 logs/daily/YYYY-MM-DD.md
```

## 3. 关键设计原则

| 层级 | 关注点 | 好处 |
|---|---|---|
| **Skill 层** | 自然语言意图识别、自动触发 | 用户零学习成本 |
| **Command 层** | 标准化工作流、可复用 | 流程一致、可审计 |
| **Subagent 层** | 人格与上下文隔离 | 长上下文不污染主会话 |
| **知识库** | 文档即配置 | 工程师可直接维护，无需改代码 |
| **Tools** | Python 脚本兜底计算 | 谐波命中、链路预算等精确运算 |

## 4. 项目数据(v2.1.0,2026-05-06 更新)

- Slash Commands: **4** (`/diagnose` v2.1 / `/matrix` / `/formal` / `/playground`)
- Skills: **4** (diagnose-desense / harmonic-calc / sop-executor / engineering-logger)
- Subagents: **1** (echo,四条工作原则:Normal 优先 / 软件优先 / 设计查阅 / **宽窄带判别**)
- 方法论文档: **5** 篇(三要素 / Normal 优先 / 软件优先 / 设计查阅 / **宽窄带判别 v1.0**)
- 标准化 SOP: **43**(**17 正式** + 26 stub,覆盖 W24/W5/GL1/GL5/LHB/LLB/Normal 七大频段族)
  - Phase 2 Sprint 1 新增:LLB-07(Charger)/ W24-03(DDR)/ LHB-04(USB3)/ W24-08(NFC)/ W24-09(SHIELD)
- 矩阵:**16 源 × 7 受扰体 × 49 映射**(单一真相源 `matrix.yaml` v2.1.0)
- 案例库:**4 个闭环案例**(AS2-RC-WiFi24-OIS / EMC-2024-triage / O11-DDR-LLB-aperture / O2-NFC-W24)
- 知识库文档总量:**83 篇 / 14,247 行** + `.claude/` harness 层 9 个 md + `docs/` 8 篇
- 工具脚本:**12** 个(Python + Shell,含 matrix 生成器 / SOP stub 生成器 / 一致性 linter)
- 已归档工作日志:**5+** 篇
- Git:10+ 次结构化 commit,2 个 tag(`v2.0.0` Phase 1 / `v2.1.0` Phase 2 Sprint 1)
- 远端:GitHub `cuipointer/Echo`

## 5. 为什么选 Claude Agent SDK

1. **原生支持多 Agent 协作**：Subagent 机制天然契合"专家人格 + 工作流"解耦
2. **Skill 自动触发**：无需显式调用，工程师用自然语言就能进入标准流程
3. **文档即配置**：`.md` 即可定义 agent/command/skill，团队维护门槛极低
4. **长上下文 + 文件系统记忆**：14K+ 行知识库可随时索引，不受单次对话窗口限制

## 6. 单一真相源架构(v2.1.0 固化)

Echo 的**核心设计决策**是为每一类知识建立**单一真相源**，所有视图文件由生成器/引用派生，消除漂移风险:

| 层 | 真相源 | 派生视图 |
|---|---|---|
| 诊断工作流 | [.claude/commands/diagnose.md](../../.claude/commands/diagnose.md) v2.1 | echo agent 引用、diagnose-desense skill 转交 |
| 矩阵 | [knowledge/matrix/matrix.yaml](../../knowledge/matrix/matrix.yaml) v2.1.0 | `matrix-table.md` / `source-list.md` / `victim-list.md`(由 `tools/gen_matrix_views.py` 生成) |
| 术语 | [knowledge/glossary.md](../../knowledge/glossary.md) | 各 SOP 附录引用 |
| 方法论 | [knowledge/methodology/](../../knowledge/methodology/) | `/diagnose` Step 3 引用 `bandwidth-discrimination.md`;echo agent 引用四原则文档 |
| 变更记录 | [CHANGELOG.md](../../CHANGELOG.md) | 各 SOP / 文件自带 `**版本**` 字段 |

守护由 [tools/check-architecture-consistency.py](../../tools/check-architecture-consistency.py) v2 执行(9 项自动检查，当前 0 错 0 警)。

## 7. Phase 2 Sprint 1 反哺路径(2026-05-06)

```
EMC 2024 案例分析(9 案例)  ──→  6 条架构建议
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        matrix.yaml v2.1   bandwidth-       SOP 模板步骤 2.6
        +NFC 共存源        discrimination    多源叠加排查法
        +SHIELD→W24        .md v1.0
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                       /diagnose v2.0 → v2.1
                       (Step 3 自动判据 + 反例提醒)
                               │
                               ▼
                       3 个 P0 SOP v0.9 方法论版
                       LLB-07 / W24-03 / LHB-04
```

详见 [CHANGELOG.md](../../CHANGELOG.md) v2.1.0 + [docs/phase2-sprint-plan.md](phase2-sprint-plan.md)。
