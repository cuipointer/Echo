# Git 分支与协作规范

**版本**:v1.0.0
**生效日期**:2026-04-28
**适用范围**:Echo·Desense 仓库

---

## 设计原则

本仓库的特殊性:

- **单人维护**(至少近期),但需要 review 流程防止自己犯错
- **内容项目**(SOP / 案例 / 方法论)多于功能开发
- **有严格一致性守护**(`tools/check-architecture-consistency.py` linter)
- **非部署型**(没有生产环境,"稳定"意味着可作为知识库快照被任何人任何时候取用)

由此推导出的原则:

1. **分支即意图**:分支名明确说明"这次改动要做什么"
2. **双保险**:linter 挡机械问题,冷却期 self-review 挡判断问题
3. **main 是快照**:main 上每个 commit 都应该能作为"当下最稳定的知识库"被任何人取用
4. **tag 记里程碑**:重要节点打 tag,形成可回溯的版本历史

---

## 分支模型全景

```
   tag v2.0.0        tag v2.1.0         tag v2.2.0
       │                 │                   │
       ▼                 ▼                   ▼
───○───○─────────○───────○─────────○─────── main (稳定,受保护)
        ╲       ╱        ╲        ╱
         ○─────○           ○──────○         develop (集成)
         ╱   ╲            ╱    ╲
     ○──○   ○──○       ○─○   ○─○           feature/* sop/* case/* ...
```

### 三层结构

| 层级 | 分支 | 稳定度 | 受保护 | 变更来源 |
|:---:|---|:---:|:---:|---|
| **稳定层** | `main` | 最稳定,linter 全绿 + self-review 过 | ✅ 受保护 | 只接受从 `develop` 合入 + `hotfix/*` |
| **集成层** | `develop` | 日常工作主干,linter 基本全绿,允许短暂不完美 | ⚠️ 软保护 | 接受所有 `feature/*` / `sop/*` / `case/*` / ... 合入 |
| **开发层** | `<type>/<slug>` | 工作中,可能有 broken 中间态 | ❌ 不保护 | 本地开发,完成后合并回 `develop` |

---

## 分支命名规范

### 主分支

| 分支 | 含义 |
|---|---|
| `main` | 稳定快照,每个 commit 可用。受保护,不能直接 push |
| `develop` | 集成分支,累积 feature 变更。review 后合入 `main` |

### 工作分支(按变更性质命名)

| 前缀 | 用途 | 示例 |
|---|---|---|
| `feature/<slug>` | 新增功能 / 工具链 / 架构改进 | `feature/hook-linter-integration` |
| `sop/<编号>` | 填充或更新单个 SOP(强对应矩阵编号) | `sop/llb-07`, `sop/w24-03` |
| `case/<机型-场景-频段>` | 新案例沉淀 | `case/as2-rc-w24`, `case/ms1-video-gl1` |
| `refactor/<slug>` | 架构级重构(不改内容) | `refactor/matrix-yaml-schema` |
| `docs/<slug>` | 纯文档变更(README / glossary / CHANGELOG 等) | `docs/development-plan-v2` |
| `fix/<slug>` | 非紧急 bug 修复 | `fix/broken-matrix-link` |
| `hotfix/<slug>` | 紧急修复,从 `main` 拉出直接打回 `main` | `hotfix/sop-version-mismatch` |
| `experimental/<slug>` | 实验,不一定合入 | `experimental/web-ui` |

**命名约束**:

- slug 全小写,用连字符分隔(`fix/broken-link` 而非 `fix/BrokenLink`)
- SOP 编号用小写(`sop/llb-07` 而非 `sop/LLB-07`)
- 长度 ≤ 40 字符(避免 shell 尾部截断)

---

## 标签(Tag)策略

### 版本号遵循 SemVer

```
v<major>.<minor>.<patch>
```

- **major**:架构级变更,可能影响知识层或 harness 层的组织方式
- **minor**:新增知识内容(SOP / 案例 / 方法论新章节)里程碑
- **patch**:修正 / broken link / 小澄清

### 打 tag 的时机

| 类型 | 触发条件 | 示例 |
|---|---|---|
| **major** | Phase 完成(见 [development-plan.md](development-plan.md)) | `v2.0.0` Phase 1 完成(2026-04-27) |
| **minor** | 重要里程碑(例如"27 个 stub 全部填充完毕") | `v2.1.0` Phase 2 完成 |
| **patch** | 累积若干修复后对外发布稳定版 | `v2.0.1`, `v2.0.2` |

### Tag 消息规范

```
v2.1.0 - Phase 2 内容填充完成

亮点:
- 27 个 stub SOP 全部转为正式 (v1.0.0+)
- 案例库扩充到 15 个
- Phase 3 自动化启动

详细变更见 CHANGELOG.md
```

---

## 典型工作流

### Workflow 1:填充新 SOP

```bash
# 从 develop 拉分支
git checkout develop
git pull
git checkout -b sop/llb-07

# 编辑 knowledge/sops/LLB/LLB-07.md
# 从 **状态**: 待编写 改为 **状态**: 进行中
# 填充八章节内容...
# 验证
python3 tools/check-architecture-consistency.py

# 完成后改状态为 已完成,版本 v1.0.0
git add knowledge/sops/LLB/LLB-07.md
git commit -m "feat(sop): 填充 LLB-07 充电器→LTE LB v1.0

- 新增理论预判(基频 500 kHz~2 MHz 谐波命中 700-960 MHz)
- 三、软件排查步骤(拔充电器 + 调整充电功率 + 关闭快充)
- 案例 1 引用 knowledge/cases/<机型>-<场景>-LLB.md"

# 推到远端 / 或保持本地
git push -u origin sop/llb-07

# self-review(可用 Claude /review 辅助)
# 合并到 develop(保留历史)
git checkout develop
git merge --no-ff sop/llb-07 -m "Merge sop/llb-07 into develop"
git branch -d sop/llb-07
```

### Workflow 2:案例沉淀 + SOP 更新(闭环)

```bash
git checkout develop
git checkout -b case/ms1-video-gl1

# 写 knowledge/cases/MS1-video-GL1-<关键词>.md
git add knowledge/cases/MS1-video-GL1-*.md
git commit -m "docs(case): MS1 录像 GL1 Desense 闭环"

# 评估是否更新 SOP-GL1-02(Camera → GL1)
# 若有更新:
vim knowledge/sops/GL1/GL1-02.md  # 版本 v1.0 → v1.1,新增步骤或整改
git add knowledge/sops/GL1/GL1-02.md
git commit -m "feat(sop): GL1-02 v1.0 → v1.1 基于 MS1 案例更新

- 新增步骤 2.5 录像模式专项排查
- 案例 4 引用 MS1-video-GL1"

# 冷却 + 合并
git checkout develop
git merge --no-ff case/ms1-video-gl1
```

### Workflow 3:架构级重构

```bash
git checkout develop
git checkout -b refactor/<名称>

# 多次提交(细粒度)
git commit -m "refactor: 第 1 步 XXX"
git commit -m "refactor: 第 2 步 YYY"
git commit -m "refactor: 第 3 步 ZZZ + linter 验证"

# 重构完成后合入 develop
git checkout develop
git merge --no-ff refactor/<名称>
```

### Workflow 4:develop → main(定期,冷却后)

**建议节奏**:每周或每完成一个 feature batch。必须经过"冷却期 self-review"。

```bash
# 冷却 24h 后
git checkout main
git pull

# 确认 develop 通过 linter
git checkout develop
python3 tools/check-architecture-consistency.py
# 0 错 0 警才继续

# 合入 main(推荐 --no-ff 保留 develop 合入痕迹)
git checkout main
git merge --no-ff develop -m "Merge develop: <简述本次合入的集合>"

# 若达到 minor/patch 里程碑,打 tag
git tag -a v2.0.1 -m "v2.0.1 - <简述>

详细变更见 CHANGELOG.md"

# 推到远端
git push origin main --tags

# develop 保持跟主干同步
git checkout develop
git merge main
git push
```

### Workflow 5:紧急修复(hotfix)

```bash
# 紧急问题直接从 main 拉
git checkout main
git checkout -b hotfix/critical-link-broken

# 快速修复
git commit -m "fix: <简述>"

# linter 必须过
python3 tools/check-architecture-consistency.py

# 直接合回 main 并打 patch tag
git checkout main
git merge --no-ff hotfix/critical-link-broken
git tag -a v2.0.2 -m "v2.0.2 - hotfix: <简述>"
git push origin main --tags

# 回灌 develop
git checkout develop
git merge main
git push

# 清理
git branch -d hotfix/critical-link-broken
```

---

## 提交信息规范(Conventional Commits)

### 格式

```
<type>(<scope>): <短描述>

<可选正文:为什么改,关键细节>

<可选脚注:Co-Authored-By / 关联 issue / BREAKING CHANGE>
```

### type 取值

| type | 含义 |
|---|---|
| `feat` | 新功能 / 新内容(新 SOP / 新 skill / 新工具) |
| `fix` | bug 修复 / broken link 修复 |
| `refactor` | 重构,不改功能不改内容 |
| `docs` | 纯文档(README / CHANGELOG / glossary / case) |
| `test` | 测试相关 |
| `chore` | 构建 / 工具链 / git 配置等 |
| `perf` | 性能优化 |

### scope 取值(本仓库)

| scope | 对应 |
|---|---|
| `sop` | `knowledge/sops/` 下变更 |
| `case` | `knowledge/cases/` 下变更 |
| `matrix` | `knowledge/matrix/` 下变更 |
| `methodology` | `knowledge/methodology/` 下变更 |
| `harness` | `.claude/` 下变更 |
| `linter` | `tools/check-architecture-consistency.py` 相关 |
| `tools` | `tools/` 其他脚本 |
| `docs` | `docs/` 或根目录文档 |

### 示例

```
feat(sop): 填充 LLB-07 充电器→LTE LB v1.0
fix(matrix): 修正 GL5-04 频段范围
refactor(harness): 折叠 diagnose 三重定义为单一真相源
docs(case): AS2 后摄 Wide WiFi 2.4G Desense 闭环案例
chore: 升级 PyYAML 到 6.0.1
```

---

## 分支保护规则(未来多人时启用)

当团队扩展到多人时,启用以下保护规则(GitHub / GitLab 均支持):

### `main` 分支

- ❌ 禁止直接 push
- ✅ 要求 PR 合入
- ✅ 要求 linter CI 通过(`python3 tools/check-architecture-consistency.py`)
- ✅ 要求至少 1 个 reviewer approval(单人时可跳过)
- ✅ 禁止 force push
- ✅ Merge 策略:**Merge commit**(保留分支合入历史)

### `develop` 分支

- ⚠️ 软保护:允许直接 push,但推荐通过分支合入
- ✅ CI 跑 linter(可失败,但有提醒)
- ❌ 禁止 force push

---

## 本地工具建议

### pre-commit hook(可选)

在 `.git/hooks/pre-commit` 放:

```bash
#!/bin/bash
# 每次 commit 前自动跑 linter
cd "$(git rev-parse --show-toplevel)"
python3 tools/check-architecture-consistency.py > /dev/null 2>&1
status=$?
if [ $status -ne 0 ]; then
  echo "❌ linter 未通过,拒绝提交。运行 python3 tools/check-architecture-consistency.py 查看详情"
  exit 1
fi
```

### git 配置建议

```bash
# 每次 merge 都保留合入痕迹
git config merge.ff false

# pull 默认 rebase,避免无意义的 merge commit
git config pull.rebase true

# 撤销 / 暂存友好
git config rerere.enabled true
```

---

## 决策树:该用哪个分支?

```
需要做变更
   │
   ▼
是紧急 bug(影响立即取用的 main)吗?
   ├── 是 → hotfix/<slug> (从 main 拉)
   └── 否
         │
         ▼
    变更性质?
         ├── 填 SOP  → sop/<编号>
         ├── 写案例  → case/<机型-场景-频段>
         ├── 改架构  → refactor/<slug>
         ├── 修 bug  → fix/<slug>
         ├── 纯文档  → docs/<slug>
         ├── 新功能  → feature/<slug>
         └── 搞实验  → experimental/<slug>
         │
         ▼
    (从 develop 拉,开发完成后合回 develop)
```

---

## Self-Review 检查清单(单人 review 必过)

合入 `develop` 前:

- [ ] `python3 tools/check-architecture-consistency.py` 0 错 0 警
- [ ] `git diff main..HEAD` 扫一遍,没有误提交的文件(如 `.env`、本地 tmp)
- [ ] Commit 消息遵循 Conventional Commits
- [ ] 新增 SOP 文件改了状态字段,版本号合理
- [ ] 新增案例引用了对应 SOP,考虑了是否要升级 SOP 版本
- [ ] 如果改 `matrix.yaml`,跑了 `python3 tools/gen_matrix_views.py`

合入 `main` 前(额外):

- [ ] 冷却 ≥ 24 小时,自己回看一遍 `git log develop..main`
- [ ] 如果是里程碑,更新 `CHANGELOG.md`
- [ ] 如果打 tag,tag 消息清晰

---

## 常见问题

### Q:单人项目为什么还要 develop 和 feature 分支?

A:为了保住 `main` 的稳定性。`main` 每个 commit 都该是"当下最稳定的知识库快照",方便任何时间任何人(包括未来加入的成员)取用。`develop` 作为集成缓冲,允许工作中的"不完美中间态"。

### Q:冷却期是什么意思?必须 24h 吗?

A:写完立刻回看容易忽略问题(自我确认偏误)。隔一段时间再看,相当于用"陌生人视角"审视自己的改动。24h 是经验值,可根据 commit 复杂度调整——小改 4~8h 足够,大改最好 > 24h。

### Q:如果急着上线,能绕过 review 吗?

A:可以,但需明确标记。一般只有 hotfix 类场景允许绕过 develop 直接打回 main;其他类型建议走完流程,免得踩坑后悔。

### Q:tag 了以后发现问题怎么办?

A:**不要删除或修改已 push 的 tag**。打一个新 tag(比如 v2.1.1)作为修正版本,CHANGELOG 里说明 "v2.1.0 已弃用,请使用 v2.1.1"。

---

## 未来演进

当团队扩展到 2+ 人时,以下规则升级:

1. **启用分支保护**:如上面"分支保护规则"章节
2. **引入 CODEOWNERS**:指定不同目录的 owner(例如 `knowledge/sops/W24/*` 由 WiFi 接口人 review)
3. **CI 自动化**:GitHub Actions / GitLab CI 跑 linter,失败时阻止合入
4. **PR 模板**:统一 PR 描述格式(做了什么 / 为什么 / 如何测试)
5. **issue / discussion**:用 GitHub Issues 跟踪 SOP 填充进度,不再手工在 CHANGELOG 跟踪

---

## 参考

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- 本仓库:[CHANGELOG.md](../CHANGELOG.md) / [development-plan.md](development-plan.md)
