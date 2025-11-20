#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试DataPreprocessingAgent
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.data_preprocessing_agent import preprocess_wos_data

def test_data_preprocessing():
    """测试数据预处理功能"""
    
    print("="*70)
    print("🧪 测试DataPreprocessingAgent")
    print("="*70)
    
    # 测试1: 处理现有的CSV文件
    print("\n【测试1】处理现有CSV文件")
    try:
        result = preprocess_wos_data(
            input_source='data/文献关键信息_全部.csv',
            output_dir='data', 
            output_filename='test_processed.csv'
        )
        
        if result['success']:
            print(f"  ✅ 处理成功")
            print(f"  📁 输出文件: {result['output_file']}")
            print(f"  📊 处理记录: {result['total_records']}")
            print(f"  📋 数据列: {result['data_columns']}")
        else:
            print(f"  ❌ 处理失败: {result['error']}")
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
    
    # 测试2: 自动检测模式（如果有WOS分段文件）
    print("\n【测试2】自动检测模式")
    wos_files = ['0-1000.xls', '1001-2000.xls', '2001-3000.xls', '3000-3674.xls']
    has_wos_files = any(Path(f).exists() for f in wos_files)
    
    if has_wos_files:
        try:
            result = preprocess_wos_data(
                input_source='auto',
                output_dir='data',
                output_filename='auto_processed.csv'
            )
            
            if result['success']:
                print(f"  ✅ 自动检测成功")
                print(f"  📁 输出文件: {result['output_file']}")
                print(f"  📊 处理记录: {result['total_records']}")
            else:
                print(f"  ❌ 自动检测失败: {result['error']}")
                
        except Exception as e:
            print(f"  ❌ 自动检测失败: {e}")
    else:
        print("  ⚠️  未找到WOS分段文件，跳过自动检测测试")
    
    print("\n" + "="*70)
    print("🎉 测试完成！")
    print("="*70)

if __name__ == '__main__':
    test_data_preprocessing()