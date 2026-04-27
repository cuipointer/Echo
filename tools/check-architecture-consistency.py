#!/usr/bin/env python3
"""
Echo 知识库架构一致性检查工具

检查 SOP 文件格式、文档结构、术语一致性等
"""

import os
import re
import sys
from pathlib import Path

class ArchitectureChecker:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        
    def check_sop_format(self):
        """检查 SOP 文件格式一致性"""
        print("\n=== 检查 SOP 文件格式 ===")
        
        sop_files = list(self.base_path.glob("knowledge/sops/**/*.md"))
        template_file = self.base_path / "knowledge/sops/_template.md"
        
        # 读取模板结构
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # 提取模板章节
        template_sections = re.findall(r'## [^\n]+', template_content)
        
        for sop_file in sop_files:
            if sop_file.name == "_template.md":
                continue
                
            print(f"\n检查文件: {sop_file.relative_to(self.base_path)}")
            
            with open(sop_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查文件长度
            line_count = len(content.split('\n'))
            if line_count < 180:
                self.warnings.append(f"{sop_file.name}: 文件过短 ({line_count}行)，建议180-220行")
            elif line_count > 250:
                self.warnings.append(f"{sop_file.name}: 文件过长 ({line_count}行)，建议精简")
            
            # 检查章节结构（忽略案例的具体标题格式）
            file_sections = re.findall(r'## [^\n]+', content)
            
            # 标准化章节名称进行比较
            template_sections_clean = [s.replace("[案例名称]", "").strip() for s in template_sections]
            file_sections_clean = [s.replace("[案例名称]", "").strip() for s in file_sections]
            
            # 检查主要章节是否存在
            required_sections = [
                "一、组合信息", "二、理论预判", "三、软件排查步骤", 
                "四、硬件排查步骤", "五、结论模板", "六、典型案例",
                "七、检查表", "八、附录"
            ]
            
            missing_sections = []
            for section in required_sections:
                if not any(section in s for s in file_sections_clean):
                    missing_sections.append(section)
            
            if missing_sections:
                self.errors.append(f"{sop_file.name}: 缺失章节: {', '.join(missing_sections)}")
            
            # 检查版本号格式
            version_match = re.search(r'\*\*版本\*\*：v(\d+)\.(\d+)\.(\d+)', content)
            if not version_match:
                self.errors.append(f"{sop_file.name}: 版本号格式错误或缺失")
            
            # 检查检查表
            if "## 七、检查表" not in content:
                self.errors.append(f"{sop_file.name}: 缺失检查表章节")
            
            # 检查典型案例
            if "## 六、典型案例" not in content:
                self.warnings.append(f"{sop_file.name}: 缺失典型案例章节")
    
    def check_document_structure(self):
        """检查文档结构完整性"""
        print("\n=== 检查文档结构 ===")
        
        # 检查领域知识目录 README
        domain_dirs = ["display", "camera"]
        for domain in domain_dirs:
            readme_file = self.base_path / f"knowledge/domain/{domain}/README.md"
            if not readme_file.exists():
                self.errors.append(f"缺失 {domain} 领域 README 文件")
            else:
                print(f"✓ {domain} README 存在")
    
    def check_decision_tree_balance(self):
        """检查决策树内容平衡性"""
        print("\n=== 检查决策树平衡性 ===")
        
        dt_file = self.base_path / "knowledge/decision-tree.md"
        with open(dt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查 Camera 分支详细程度
        camera_section = re.search(r'## Camera 专用分支[^#]+', content, re.DOTALL)
        if camera_section:
            camera_content = camera_section.group(0)
            camera_lines = len(camera_content.split('\n'))
            
            # 检查是否包含标准步骤
            required_elements = [
                "第一步：干扰源初步定位",
                "第二步：频率分析", 
                "谐波命中计算",
                "参考SOP"
            ]
            
            for element in required_elements:
                if element not in camera_content:
                    self.warnings.append(f"决策树 Camera 分支缺失: {element}")
        
        print(f"✓ 决策树 Camera 分支检查完成")
    
    def check_terminology_consistency(self):
        """检查术语一致性"""
        print("\n=== 检查术语一致性 ===")
        
        # 定义标准术语
        standard_terms = {
            "Desense": "灵敏度恶化",
            "SSC": "展频时钟", 
            "MIPI": "移动行业处理器接口",
            "谐波": "谐波",
            "耦合路径": "耦合路径"
        }
        
        # 检查关键文件中的术语使用
        key_files = [
            "knowledge/sops/GL1/GL1-01.md",
            "knowledge/sops/GL1/GL1-02.md",
            "knowledge/domain/display/overview.md",
            "knowledge/domain/camera/overview.md"
        ]
        
        for file_path in key_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查标准术语使用
                for term, definition in standard_terms.items():
                    if term in content:
                        print(f"✓ {file_path}: 使用标准术语 '{term}'")
    
    def generate_report(self):
        """生成检查报告"""
        print("\n" + "="*60)
        print("架构一致性检查报告")
        print("="*60)
        
        if self.errors:
            print("\n❌ 错误项:")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✅ 无严重错误")
        
        if self.warnings:
            print("\n⚠️ 警告项:")
            for warning in self.warnings:
                print(f"  - {warning}")
        else:
            print("\n✅ 无警告项")
        
        # 总体评估
        total_issues = len(self.errors) + len(self.warnings)
        if total_issues == 0:
            print("\n🎉 架构一致性优秀!")
        elif len(self.errors) == 0:
            print(f"\n📊 架构一致性良好，有 {len(self.warnings)} 项可优化")
        else:
            print(f"\n🔧 需要修复 {len(self.errors)} 项错误和 {len(self.warnings)} 项警告")
        
        return len(self.errors) == 0

def main():
    """主函数"""
    base_path = Path(__file__).parent.parent
    checker = ArchitectureChecker(base_path)
    
    print("开始 Echo 知识库架构一致性检查...")
    
    # 执行各项检查
    checker.check_sop_format()
    checker.check_document_structure()
    checker.check_decision_tree_balance()
    checker.check_terminology_consistency()
    
    # 生成报告
    success = checker.generate_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()