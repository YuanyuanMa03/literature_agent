#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据预处理Agent独立使用脚本
演示如何使用DataPreprocessingAgent处理WOS数据
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.data_preprocessing_agent import DataPreprocessingAgent, preprocess_wos_data
from core.llm import LiteratureLLM
import os
from dotenv import load_dotenv

load_dotenv()


def demo_data_preprocessing():
    """演示数据预处理Agent的使用"""
    
    print("="*80)
    print("🔧 数据预处理Agent - 使用演示")
    print("="*80)
    
    # 创建LLM实例
    print("\n📝 初始化LLM...")
    llm = LiteratureLLM(
        model=os.getenv("LLM_MODEL", "Qwen/Qwen3-Omni-30B-A3B-Instruct"),
        temperature=0.1
    )
    
    # 创建数据预处理Agent
    print("🤖 初始化数据预处理Agent...")
    agent = DataPreprocessingAgent(llm)
    
    print("\n" + "="*50)
    print("选择处理模式：")
    print("1. 自动检测WOS分段文件")
    print("2. 处理现有CSV文件")
    print("3. 处理指定文件")
    print("="*50)
    
    choice = input("\n请选择模式 (1-3, 默认2): ").strip() or "2"
    
    if choice == "1":
        # 自动检测模式
        print("\n🔍 使用自动检测模式...")
        result = agent.run(
            input_source="auto",
            output_dir="data",
            output_filename="auto_preprocessed_literature.csv"
        )
        
    elif choice == "2":
        # 处理现有CSV文件
        csv_file = "data/文献关键信息_全部.csv"
        if Path(csv_file).exists():
            print(f"\n📊 处理现有CSV文件: {csv_file}")
            result = agent.run(
                input_source=csv_file,
                output_dir="data",
                output_filename="preprocessed_literature.csv"
            )
        else:
            print(f"❌ 文件不存在: {csv_file}")
            return
            
    elif choice == "3":
        # 处理指定文件
        file_path = input("\n请输入文件路径: ").strip()
        if Path(file_path).exists():
            print(f"\n📊 处理指定文件: {file_path}")
            result = agent.run(
                input_source=file_path,
                output_dir="data",
                output_filename="custom_preprocessed.csv"
            )
        else:
            print(f"❌ 文件不存在: {file_path}")
            return
    else:
        print("❌ 无效选择")
        return
    
    # 显示结果
    print("\n" + "="*80)
    print("📊 处理结果")
    print("="*80)
    
    if result["success"]:
        print(f"✅ 处理成功！")
        print(f"📁 输出文件: {result['output_file']}")
        print(f"📊 处理记录: {result['total_records']} 篇")
        
        print(f"\n📋 数据列:")
        for i, col in enumerate(result['data_columns'], 1):
            print(f"  {i}. {col}")
        
        print(f"\n📈 统计信息:")
        stats = result['statistics']
        print(f"  - 总文献数: {stats['total_records']}")
        if 'year_range' in stats:
            print(f"  - 年份范围: {stats['year_range']}")
        if 'doi_count' in stats:
            print(f"  - 有DOI的文献: {stats['doi_count']} 篇 ({stats['doi_percentage']}%)")
        if 'abstract_count' in stats:
            print(f"  - 有摘要的文献: {stats['abstract_count']} 篇 ({stats['abstract_percentage']}%)")
        
        print(f"\n👀 数据预览 (前3篇):")
        for i, record in enumerate(result['preview'], 1):
            print(f"\n{i}. {record.get('authors', 'N/A')} ({record.get('year', 'N/A')})")
            title = str(record.get('title', 'N/A'))
            print(f"   {title[:80]}{'...' if len(title) > 80 else ''}")
            
            if 'abstract' in record and record['abstract']:
                abstract = str(record['abstract'])
                print(f"   摘要: {abstract[:100]}{'...' if len(abstract) > 100 else ''}")
            
            doi = record.get('doi', 'N/A')
            print(f"   DOI: {doi if doi else 'N/A'}")
        
        print(f"\n💾 生成的文件:")
        output_path = Path(result['output_file'])
        print(f"  - CSV: {output_path}")
        print(f"  - Excel: {output_path.with_suffix('.xlsx')}")
        
    else:
        print(f"❌ 处理失败: {result['error']}")
    
    print("\n" + "="*80)
    print("🎉 演示完成！")
    print("="*80)


def demo_convenience_function():
    """演示便捷函数的使用"""
    
    print("\n" + "="*80)
    print("⚡ 便捷函数演示")
    print("="*80)
    
    print("\n使用preprocess_wos_data()便捷函数:")
    
    try:
        result = preprocess_wos_data(
            input_source="data/文献关键信息_全部.csv",
            output_dir="data",
            output_filename="convenience_function_demo.csv"
        )
        
        if result["success"]:
            print(f"✅ 便捷函数执行成功！")
            print(f"📁 输出文件: {result['output_file']}")
            print(f"📊 处理记录: {result['total_records']} 篇")
        else:
            print(f"❌ 便捷函数执行失败: {result['error']}")
            
    except Exception as e:
        print(f"❌ 便捷函数演示失败: {e}")


if __name__ == '__main__':
    try:
        # 主演示
        demo_data_preprocessing()
        
        # 便捷函数演示
        demo_convenience_function()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断执行")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()