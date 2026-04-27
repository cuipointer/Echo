#!/usr/bin/env python3
"""
工程日志时间修复工具
修复日志文件中的日期和时间戳问题
"""

import os
import sys
import datetime
import re
from pathlib import Path

def get_current_datetime():
    """获取当前日期和时间"""
    now = datetime.datetime.now()
    return {
        'date': now.strftime('%Y-%m-%d'),
        'time': now.strftime('%H:%M'),
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute
    }

def fix_daily_log():
    """修复今日日志文件的时间问题"""
    current = get_current_datetime()
    log_dir = Path("logs/daily")
    
    # 检查今日日志文件是否存在
    log_file = log_dir / f"{current['date']}.md"
    
    if not log_file.exists():
        print(f"今日日志文件不存在: {log_file}")
        return False
    
    # 读取日志文件内容
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查日期是否正确
    if current['date'] not in content:
        # 替换日期占位符
        content = re.sub(r'\*\*日期\*\*：.*', f"**日期**：{current['date']}", content)
        print(f"已修复日期: {current['date']}")
    
    # 检查是否需要更新时间戳
    # 查找最后一个时间戳
    time_pattern = r'\| (\d{2}:\d{2}) \|'
    times = re.findall(time_pattern, content)
    
    if times:
        last_time = times[-1]
        # 如果最后一个时间戳比当前时间晚，可能需要修复
        last_hour, last_minute = map(int, last_time.split(':'))
        current_hour, current_minute = current['hour'], current['minute']
        
        # 如果最后一个时间戳比当前时间晚，说明时间戳有问题
        if last_hour > current_hour or (last_hour == current_hour and last_minute > current_minute):
            print(f"检测到异常时间戳: {last_time} (当前时间: {current['time']})")
            # 这里可以添加时间戳修复逻辑
    
    # 检查统计信息中的Git提交信息
    git_pattern = r'- \*\*最后提交\*\*：.*'
    git_commits = re.findall(git_pattern, content)
    
    # 获取最新的Git提交信息
    try:
        import subprocess
        result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %s'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            latest_commit = result.stdout.strip()
            content = re.sub(git_pattern, f"- **最后提交**：{latest_commit}", content)
            print(f"已更新Git提交信息: {latest_commit}")
    except Exception as e:
        print(f"获取Git信息失败: {e}")
    
    # 写回文件
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"日志文件已修复: {log_file}")
    return True

def create_daily_log_template():
    """创建正确的每日日志模板"""
    current = get_current_datetime()
    template_file = Path("logs/templates/daily-template.md")
    
    template_content = f"""# 工程开发日志

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
    
    # 如果模板文件不存在，创建它
    template_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"模板文件已创建: {template_file}")

def main():
    """主函数"""
    print("=== 工程日志时间修复工具 ===")
    print(f"当前时间: {get_current_datetime()['date']} {get_current_datetime()['time']}")
    
    # 确保模板文件存在
    create_daily_log_template()
    
    # 修复今日日志
    if fix_daily_log():
        print("时间修复完成")
    else:
        print("时间修复失败")

if __name__ == "__main__":
    main()