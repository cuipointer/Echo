#!/usr/bin/env python3
"""
工程日志管理系统
提供正确的时间处理和日志记录功能
"""

import os
import sys
import datetime
import re
from pathlib import Path

class EngineeringLogger:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.logs_dir = self.project_root / "logs"
        self.daily_dir = self.logs_dir / "daily"
        self.templates_dir = self.logs_dir / "templates"
        
        # 确保目录存在
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
    
    def get_current_time_info(self):
        """获取当前时间信息"""
        now = datetime.datetime.now()
        return {
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M'),
            'datetime': now,
            'iso': now.isoformat()
        }
    
    def get_daily_log_path(self, date=None):
        """获取每日日志文件路径"""
        if date is None:
            date = self.get_current_time_info()['date']
        return self.daily_dir / f"{date}.md"
    
    def ensure_template_exists(self):
        """确保模板文件存在"""
        template_file = self.templates_dir / "daily-template.md"
        
        if not template_file.exists():
            template_content = """# 工程开发日志

**日期**：{{DATE}}
**项目**：Echo

---

## 今日活动

| 时间 | 模块 | 活动摘要 | 状态 |
|------|------|----------|------|
| | | | |

---

## 详细记录

（复杂任务的详细记录追加在此处）

---

## 今日统计

- **提交次数**：0
- **新建文件**：0
- **修改文件**：0
- **Git 分支**：
- **最后提交**：

---

## 明日计划

1.

---

## 备注
"""
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(template_content)
    
    def create_daily_log(self, date=None):
        """创建每日日志文件"""
        self.ensure_template_exists()
        
        time_info = self.get_current_time_info()
        if date is None:
            date = time_info['date']
        
        log_file = self.get_daily_log_path(date)
        
        # 如果文件已存在，不覆盖
        if log_file.exists():
            return log_file
        
        # 读取模板
        template_file = self.templates_dir / "daily-template.md"
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # 替换占位符
        content = template.replace("{{DATE}}", date)
        
        # 写入日志文件
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"创建日志文件: {log_file}")
        return log_file
    
    def log_activity(self, module, summary, status="✅ 完成", detailed_record=None):
        """记录活动"""
        time_info = self.get_current_time_info()
        
        # 确保日志文件存在
        log_file = self.create_daily_log()
        
        # 读取现有内容
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在活动表格中添加新行
        activity_line = f"| {time_info['time']} | {module} | {summary} | {status} |"
        
        # 找到活动表格的插入位置
        table_start = content.find("## 今日活动")
        table_end = content.find("---", table_start)
        
        if table_start != -1 and table_end != -1:
            table_content = content[table_start:table_end]
            
            # 找到表格的最后一行（空行）
            lines = table_content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() == "| | | | |":
                    # 在空行前插入新行
                    lines[i] = activity_line + '\n' + line
                    break
            else:
                # 如果没有空行，在表格末尾添加
                lines.append(activity_line)
            
            # 更新内容
            new_table_content = '\n'.join(lines)
            content = content[:table_start] + new_table_content + content[table_end:]
        
        # 如果有详细记录，添加到详细记录部分
        if detailed_record:
            detailed_section = f"""
### [{time_info['time']}] {summary}

- **模块**：{module}
- **任务**：{detailed_record.get('task', '')}
- **关键产出**：{detailed_record.get('output', '')}
- **备注**：{detailed_record.get('notes', '')}
"""
            
            # 找到详细记录部分的插入位置
            detailed_start = content.find("## 详细记录")
            if detailed_start != -1:
                # 在详细记录部分的开头插入
                insert_pos = content.find("（复杂任务的详细记录追加在此处）", detailed_start)
                if insert_pos != -1:
                    content = content[:insert_pos] + detailed_section + '\n' + content[insert_pos:]
        
        # 更新统计信息
        content = self.update_statistics(content)
        
        # 写回文件
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"活动已记录: {time_info['time']} - {module} - {summary}")
        return log_file
    
    def update_statistics(self, content):
        """更新统计信息"""
        # 获取Git信息
        git_branch = self.get_git_branch()
        latest_commit = self.get_latest_commit()
        
        # 更新分支信息
        content = re.sub(r'- \*\*Git 分支\*\*：.*', 
                        f"- **Git 分支**：{git_branch}", content)
        
        # 更新提交信息
        content = re.sub(r'- \*\*最后提交\*\*：.*', 
                        f"- **最后提交**：{latest_commit}", content)
        
        return content
    
    def get_git_branch(self):
        """获取当前Git分支"""
        try:
            import subprocess
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "unknown"
    
    def get_latest_commit(self):
        """获取最新Git提交"""
        try:
            import subprocess
            result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %s'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "unknown"
    
    def commit_log_changes(self):
        """提交日志变更到Git"""
        try:
            import subprocess
            time_info = self.get_current_time_info()
            log_file = self.get_daily_log_path()
            
            # 添加文件
            result = subprocess.run(['git', 'add', str(log_file)], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            # 提交
            commit_msg = f"docs: 更新日志 - {time_info['time']}"
            result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                print(f"Git提交成功: {commit_msg}")
                return True
            else:
                print(f"Git提交失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"Git操作异常: {e}")
            return False

def main():
    """测试函数"""
    logger = EngineeringLogger()
    
    # 测试日志记录
    logger.log_activity(
        module="时间修复",
        summary="修复工程日志时间处理bug",
        detailed_record={
            "task": "修复日期占位符替换和时间戳生成逻辑",
            "output": "创建了logger.py工具脚本",
            "notes": "解决了年份不一致和硬编码时间戳问题"
        }
    )
    
    # 提交到Git
    logger.commit_log_changes()

if __name__ == "__main__":
    main()