#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第二阶段主程序 - PDF深度分析流程

流程：
1. 读取第一阶段筛选结果
2. 使用手动下载的PDF文件（跳过自动下载）
3. PDF转图片
4. DeepSeek-OCR识别
5. Qwen深度分析
6. 汇总表格、图像、数据集
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from core.llm import LiteratureLLM
# from agents.pdf_download_agent import PDFDownloadAgent  # 已禁用自动下载
from agents.deep_analysis_agent import DeepAnalysisAgent

load_dotenv()


def main():
    print("="*70)
    print("🔬 文献深度分析系统 - Stage 2 (手动下载模式)")
    print("   使用手动下载的PDF → OCR识别 → 深度分析")
    print("   统一使用硅基流动API")
    print("="*70)
    
    # 初始化LLM（Qwen用于深度分析，DeepSeek-OCR用于识别）
    # 都使用相同的硅基流动API配置
    llm = LiteratureLLM(
        model=os.getenv("LLM_MODEL", "Qwen/Qwen3-Omni-30B-A3B-Instruct"),
        temperature=0.1
    )
    
    # 初始化分析Agent（不需要下载Agent）
    analysis_agent = DeepAnalysisAgent(
        llm,
        pdf_dir="./pdfs",
        image_dir="./pdf_images"
    )
    
    print("\n✅ 系统初始化完成")
    print("📁 PDF目录: ./pdfs/")
    print("💡 请将手动下载的PDF文件放入 ./pdfs/ 目录\n")
    
    # 读取第一阶段结果
    try:
        screening_file = 'literature_screening_results.xlsx'
        df = pd.read_excel(screening_file)
        print(f"📁 读取筛选结果: {len(df)} 篇文献")
        
        passed = (df['LLM_Decision'] == 'accept').sum()
        print(f"   通过筛选: {passed} 篇")
        
    except FileNotFoundError:
        print(f"❌ 未找到筛选结果文件: {screening_file}")
        print("   请先运行 main.py 完成第一阶段筛选")
        return
    
    # ========== STAGE 2: 深度分析 ==========
    
    # Step 1: 扫描手动下载的PDF文件
    print("\n" + "="*70)
    print("【STAGE 2.1】扫描PDF文件")
    print("="*70)
    
    pdf_dir = Path("./pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    print(f"\n📂 在 ./pdfs/ 目录中找到 {len(pdf_files)} 个PDF文件")
    
    if len(pdf_files) == 0:
        print("\n❌ 未找到任何PDF文件！")
        print("\n请按以下步骤操作：")
        print("1. 手动下载需要分析的文献PDF")
        print("2. 将PDF文件放入 ./pdfs/ 目录")
        print("3. 重新运行本程序")
        print("\n💡 提示：文件名可以是任意格式（如：paper1.pdf, 10.1016_xxx.pdf等）")
        return
    
    # 显示找到的PDF文件
    print("\n找到的PDF文件：")
    for i, pdf_file in enumerate(pdf_files[:10], 1):  # 只显示前10个
        size_mb = pdf_file.stat().st_size / 1024 / 1024
        print(f"  {i}. {pdf_file.name} ({size_mb:.2f} MB)")
    
    if len(pdf_files) > 10:
        print(f"  ... 还有 {len(pdf_files) - 10} 个文件")
    
    # 用户选择要分析的数量
    print("\n请选择要分析的文献数量：")
    print(f"1. 测试模式（分析3篇文献）")
    print(f"2. 小批量模式（10篇）")
    print(f"3. 全部文献（{len(pdf_files)} 篇）")
    
    choice = input("\n请输入选择 (1-3, 默认1): ").strip() or "1"
    
    if choice == "1":
        max_papers = 3
        print(f"\n🔬 测试模式: 处理 {min(max_papers, len(pdf_files))} 篇")
    elif choice == "2":
        max_papers = 10
        print(f"\n🔬 小批量模式: 处理 {min(max_papers, len(pdf_files))} 篇")
    else:
        max_papers = len(pdf_files)
        print(f"\n🔬 完整模式: 处理全部 {len(pdf_files)} 篇")
    
    # 构造模拟的download_results（用于分析Agent）
    download_results = {
        'downloaded': min(max_papers, len(pdf_files)),
        'failed': 0,
        'total': len(pdf_files),
        'results': {}
    }
    
    # 为每个PDF文件创建结果条目
    for pdf_file in pdf_files[:max_papers]:
        # 尝试从文件名提取DOI（如果文件名是DOI格式）
        doi = pdf_file.stem.replace('_', '/')
        download_results['results'][doi] = {
            'status': 'exists',
            'path': str(pdf_file),
            'source': 'manual'
        }
    
    print(f"✅ 准备分析 {download_results['downloaded']} 篇文献\n")
    
    # Step 2: 深度分析
    print("\n" + "="*70)
    print("【STAGE 2.2】深度分析 (PDF→OCR→分析)")
    print("="*70)
    
    analysis_df = analysis_agent.run(
        download_results=download_results,
        max_papers=max_papers or 1000
    )
    
    # 最终总结
    print("\n" + "="*70)
    print("📊 第二阶段完成统计")
    print("="*70)
    
    print(f"\nPDF文件:")
    print(f"  本地文件: {download_results.get('downloaded', 0)} 篇")
    
    if not analysis_df.empty:
        print(f"\n深度分析:")
        print(f"  成功分析: {len(analysis_df)} 篇")
        print(f"  提取表格: {analysis_df['Tables_Count'].sum()} 个")
        print(f"  提取图表: {analysis_df['Figures_Count'].sum()} 个")
        
        # 统计有数据集的文献
        has_datasets = sum(1 for x in analysis_df['Key_Datasets'] 
                          if x and x != '[]')
        print(f"  包含数据集: {has_datasets} 篇")
    
    print(f"\n生成文件:")
    print(f"  1. deep_analysis_results.xlsx - 深度分析结果")
    print(f"  2. deep_analysis_results.json - 详细JSON结果")
    print(f"  3. ./pdfs/ - 源PDF文件")
    print(f"  4. ./pdf_images/ - PDF转换的图片")
    
    print("\n" + "="*70)
    print("✅ 第二阶段分析全部完成！")
    print("="*70)


if __name__ == "__main__":
    main()
