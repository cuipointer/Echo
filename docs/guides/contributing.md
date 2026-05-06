# 贡献指南

## 欢迎贡献

感谢您对 Echo·Desense 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 报告问题
- 提交功能请求
- 编写文档
- 提交代码
- 编写 SOP

## 如何贡献

### 1. 报告问题

如果您发现 Bug 或有功能建议，请通过 GitHub Issues 提交：

1. 访问 [Issues 页面](https://github.com/your-username/echo-desense/issues)
2. 点击 "New Issue"
3. 选择问题类型（Bug 报告 / 功能请求 / 新 SOP）
4. 填写详细信息

### 2. 提交代码

#### Fork 项目

1. Fork 项目到您的 GitHub 账户
2. 克隆您的 Fork：
   ```bash
   git clone https://github.com/your-username/echo-desense.git
   cd echo-desense
   ```

#### 创建分支

```bash
git checkout -b feature/your-feature-name
```

#### 提交更改

```bash
git add .
git commit -m "Add your feature description"
git push origin feature/your-feature-name
```

#### 创建 Pull Request

1. 访问您的 Fork 页面
2. 点击 "New Pull Request"
3. 填写 PR 描述
4. 等待审核

### 3. 编写文档

#### 文档位置
- `docs/`：使用文档
- `knowledge/`：知识库文档
- `logs/templates/`：日志模板

#### 文档规范
- 使用 Markdown 格式
- 保持结构清晰
- 使用一致的术语

### 4. 编写 SOP

#### SOP 位置
- `knowledge/sops/`：SOP 库
- 按频段分类：W24/W5/LLB/LHB/GL1/GL5

#### SOP 规范
- 使用 `_template.md` 作为模板
- 包含完整的三要素分析
- 记录排查步骤和结论

## 开发规范

### 代码风格

#### Python 脚本
- 使用 Python 3
- 遵循 PEP 8 规范
- 添加文档字符串
- 使用类型注解

#### Shell 脚本
- 使用 Bash
- 添加错误处理
- 添加注释说明

### 提交规范

#### Commit Message
```
<type>: <description>

[可选正文]

[可选脚注]
```

类型：
- `feat`：新功能
- `fix`：修复 Bug
- `docs`：文档更新
- `style`：代码格式
- `refactor`：重构
- `test`：测试
- `chore`：构建/工具

示例：
```
feat: 添加谐波计算工具

实现谐波频率计算功能
支持判断是否命中受扰体频段
```

### 分支规范

- `main`：主分支，稳定版本
- `develop`：开发分支
- `feature/*`：功能分支
- `bugfix/*`：修复分支
- `hotfix/*`：紧急修复

## 项目结构

```
echo-desense/
├── .github/              # GitHub 配置
├── .claude/              # Claude Code 能力模块(agents / commands / skills)
├── docs/                 # 使用文档
├── knowledge/            # 知识库
│   ├── methodology/      # 方法论
│   ├── matrix/           # 矩阵体系
│   ├── sops/             # SOP 库
│   └── cases/            # 案例库
├── logs/                 # 工作日志
├── playground/           # 临时缓冲区
├── tools/                # 工具脚本
└── extensions/           # 领域扩展
```

## 代码审查

### 审查清单

- [ ] 代码符合项目规范
- [ ] 文档已更新
- [ ] 测试已通过
- [ ] Commit Message 规范
- [ ] 无安全漏洞

### 审查流程

1. 提交 PR
2. 自动检查（CI）
3. 代码审查
4. 合并到主分支

## 社区规范

### 行为准则

- 尊重他人，友善交流
- 建设性反馈
- 包容多元观点
- 遵守项目规范

### 沟通方式

- GitHub Issues：问题报告和功能请求
- Pull Requests：代码贡献
- Discussions：讨论和建议

## 联系方式

- **项目主页**：https://github.com/your-username/echo-desense
- **问题反馈**：https://github.com/your-username/echo-desense/issues
- **讨论区**：https://github.com/your-username/echo-desense/discussions

## 感谢

感谢所有贡献者的支持！
