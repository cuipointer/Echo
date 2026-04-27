---
description: 进入临时调试缓冲区(playground/),记录临时分析不写入知识库
argument-hint: [会话名]
---

# /playground

用户输入:`$ARGUMENTS`(可选会话名)

引导用户进入临时调试区 [playground/](playground/),用于 prompt 实验、输出预览、临时笔记——**不入 Git、不进知识库**。

## 1. 解析参数

- 若提供会话名 → 在 `playground/sessions/<会话名>/` 下创建 `prompt.md` / `output.md` / `notes.md` 三个空文件(如已存在则复用)。
- 若未提供 → 指向 `playground/scratchpad/`,并让用户自由记录。

## 2. 目录约定

```
playground/
├── sessions/<会话名>/
│   ├── prompt.md      # Prompt 草稿
│   ├── output.md      # 输出预览
│   └── notes.md       # 临时笔记
├── outputs/            # 批量输出
├── prompts/            # Prompt 草稿池
└── scratchpad/         # 自由草稿
```

## 3. 核心规则

1. **不持久化**:playground 目录在 `.gitignore` 中,内容不会进 Git。
2. **重要发现要搬家**:如果草稿中出现值得保留的结论或 SOP,**必须**迁移到 `knowledge/` 相应子目录;否则过期即清理。
3. **清理建议**:完成一轮实验后,建议删除过期会话。

## 4. 后续动作

- 从 playground 形成正式结论 → 调用 `/formal` 生成正式报告。
- 发现的新矩阵组合 → 手动补充到 `knowledge/matrix/`。
