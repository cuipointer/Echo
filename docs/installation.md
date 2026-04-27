# 安装指南

## 系统要求

- **操作系统**：Linux / macOS / Windows (WSL)
- **Python**：3.7 或更高版本
- **Git**：2.0 或更高版本

## 快速安装

### 1. 克隆项目

```bash
git clone https://github.com/your-username/echo-desense.git
cd echo-desense
```

### 2. 运行安装脚本

```bash
./install.sh
```

安装脚本将完成以下操作：
- 初始化 Git 仓库
- 配置 Git 参数
- 创建 README.md 和 CHANGELOG.md
- 设置脚本权限

### 3. 验证安装

```bash
# 检查目录结构
ls -la

# 检查 Git 仓库
git status

# 检查工具脚本
python3 tools/harmonic_calc.py --help
```

## 手动安装

如果安装脚本无法运行，可以手动安装：

### 1. 创建目录结构

```bash
# 基础目录
mkdir -p .claude/agents
mkdir -p .claude/skills/{diagnose-desense,harmonic-calc,sop-executor,engineering-logger}
mkdir -p .claude/commands
mkdir -p knowledge/{methodology,matrix,sops,cases}
mkdir -p tools
mkdir -p docs
mkdir -p logs/{daily,debug,weekly,templates}
mkdir -p playground/{sessions,outputs,prompts,scratchpad}
mkdir -p extensions/{RSE,Camera}
mkdir -p .github/{ISSUE_TEMPLATE,workflows}
```

### 2. 复制配置文件

复制以下文件到项目根目录:
- `.gitignore`
- `LICENSE`
- `CLAUDE.md`

### 3. 设置权限

```bash
chmod +x install.sh uninstall.sh
chmod +x tools/*.py tools/*.sh
```

## 配置 Git

### 设置用户信息

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 设置默认分支

```bash
git config init.defaultBranch main
```

## 验证安装

### 检查目录结构

```bash
tree -L 2
```

预期输出:
```
.
├── .github
├── .gitignore
├── .claude
├── CLAUDE.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── docs
├── extensions
├── knowledge
├── logs
├── playground
└── tools
    ├── install.sh
    ├── uninstall.sh
    └── ...
```

### 检查工具脚本

```bash
# 谐波计算工具
python3 tools/harmonic_calc.py 400 4 1561 1606

# 链路预算工具
python3 tools/link_budget.py margin -30 80 -140
```

### 检查 Git 仓库

```bash
git status
git log --oneline
```

## 下一步

安装完成后，可以：

1. **阅读文档**：查看 `docs/` 目录了解使用方法
2. **了解方法论**：查看 `knowledge/methodology/` 目录
3. **开始使用**:在 Claude Code 中打开本目录,输入 `/diagnose` 启动诊断流程

## 常见问题

### Q: 安装脚本无法运行
A: 检查文件权限：`chmod +x install.sh`

### Q: Git 初始化失败
A: 确保当前目录不是 Git 仓库的子目录

### Q: Python 工具无法运行
A: 检查 Python 版本：`python3 --version`

### Q: 目录结构不完整
A: 手动创建缺失的目录，或重新运行安装脚本
