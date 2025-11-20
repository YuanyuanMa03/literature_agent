#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据预处理Agent - 将原始WOS文献数据处理成符合agent分析的标准格式
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Union
from core.agent import Agent
from core.message import Message
import os


class DataPreprocessingAgent(Agent):
    """数据预处理Agent"""
    
    def __init__(self, llm):
        """初始化数据预处理Agent"""
        super().__init__(
            name="数据预处理Agent",
            llm=llm,
            system_prompt=self._default_system_prompt()
        )
    
    def _default_system_prompt(self) -> str:
        """默认系统提示词"""
        return """你是一个专业的文献数据预处理专家。你的任务是：

1. 处理原始Web of Science (WOS)导出的文献数据
2. 提取关键信息：作者、年份、标题、摘要、DOI
3. 清理和标准化数据格式
4. 生成符合agent分析需求的标准CSV格式
5. 提供数据质量统计和预览

你需要确保数据的完整性、一致性和可用性。"""
    
    def run(
        self,
        input_source: Union[str, List[str], pd.DataFrame] = "auto",
        output_dir: str = "data",
        output_filename: str = "literature_data_processed.csv",
        auto_detect: bool = True
    ) -> Dict[str, any]:
        """
        运行数据预处理流程
        
        Parameters:
        -----------
        input_source : Union[str, List[str], pd.DataFrame]
            输入源：
            - "auto": 自动检测当前目录下的Excel文件
            - str: 单个文件路径
            - List[str]: 多个文件路径列表
            - pd.DataFrame: 直接输入DataFrame
        output_dir : str
            输出目录
        output_filename : str
            输出文件名
        auto_detect : bool
            是否自动检测WOS分段文件
            
        Returns:
        --------
        Dict[str, any]: 处理结果和统计信息
        """
        
        print("="*70)
        print("🔧 数据预处理Agent - 开始处理文献数据")
        print("="*70)
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        try:
            # STEP 1: 加载原始数据
            print("\n【STEP 1/4】加载原始数据")
            df = self._load_data(input_source, auto_detect)
            
            # STEP 2: 提取关键信息
            print("\n【STEP 2/4】提取关键信息")
            df_processed = self._extract_key_info(df)
            
            # STEP 3: 数据清理和标准化
            print("\n【STEP 3/4】数据清理和标准化")
            df_cleaned = self._clean_and_standardize(df_processed)
            
            # STEP 4: 保存结果
            print("\n【STEP 4/4】保存处理结果")
            output_file = self._save_results(
                df_cleaned,
                output_path / output_filename
            )
            
            # 生成统计报告
            stats = self._generate_statistics(df_cleaned)
            
            print("\n" + "="*70)
            print("✅ 数据预处理完成！")
            print("="*70)
            
            return {
                "success": True,
                "output_file": str(output_file),
                "total_records": len(df_cleaned),
                "statistics": stats,
                "data_columns": list(df_cleaned.columns),
                "preview": df_cleaned.head(3).to_dict('records') if len(df_cleaned) > 0 else []
            }
            
        except Exception as e:
            error_msg = f"数据预处理失败: {str(e)}"
            print(f"\n❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "output_file": None,
                "total_records": 0,
                "statistics": {},
                "data_columns": [],
                "preview": []
            }
    
    def _load_data(
        self,
        input_source: Union[str, List[str], pd.DataFrame],
        auto_detect: bool
    ) -> pd.DataFrame:
        """加载原始数据"""
        
        if isinstance(input_source, pd.DataFrame):
            print("  ✅ 直接使用输入的DataFrame")
            return input_source
        
        if input_source == "auto" and auto_detect:
            # 自动检测WOS分段文件
            wos_patterns = [
                '0-1000.xls', '1001-2000.xls', '2001-3000.xls', '3000-3674.xls',
                '0-1000.xlsx', '1001-2000.xlsx', '2001-3000.xlsx', '3000-3674.xlsx'
            ]
            
            found_files = []
            for pattern in wos_patterns:
                if Path(pattern).exists():
                    found_files.append(pattern)
            
            if found_files:
                print(f"  🔍 自动检测到 {len(found_files)} 个WOS分段文件:")
                for f in found_files:
                    print(f"    - {f}")
                input_files = found_files
            else:
                # 检测其他Excel文件
                excel_files = list(Path('.').glob('*.xls*'))
                if excel_files:
                    print(f"  🔍 检测到 {len(excel_files)} 个Excel文件:")
                    for f in excel_files:
                        print(f"    - {f}")
                    input_files = [str(f) for f in excel_files]
                else:
                    raise FileNotFoundError("未找到任何Excel文件")
        elif isinstance(input_source, str):
            input_files = [input_source]
        else:
            input_files = input_source
        
        # 读取并合并所有文件
        print(f"\n  📖 正在读取 {len(input_files)} 个文件...")
        dfs = []
        total_records = 0
        
        for input_file in input_files:
            try:
                print(f"    - 读取: {input_file}")
                if input_file.endswith('.csv'):
                    df_temp = pd.read_csv(input_file)
                else:
                    df_temp = pd.read_excel(input_file)
                
                dfs.append(df_temp)
                file_records = len(df_temp)
                total_records += file_records
                print(f"      ✅ {file_records} 篇文献")
                
            except Exception as e:
                print(f"      ❌ 读取失败: {e}")
                continue
        
        if not dfs:
            raise ValueError("没有成功读取任何文件")
        
        df = pd.concat(dfs, ignore_index=True)
        print(f"\n  ✅ 合并完成: 总计 {len(df)} 篇文献")
        
        return df
    
    def _extract_key_info(self, df: pd.DataFrame) -> pd.DataFrame:
        """提取关键信息"""
        
        print("  🔍 提取关键列...")
        
        # 定义关键列的多种可能名称
        column_mappings = {
            'authors': ['Authors', 'Author(s)', 'Author Full Names', '作者', '作者/Authors'],
            'year': ['Publication Year', 'Year', 'Publication Year', '年份', '年份/Year'],
            'title': ['Article Title', 'Title', 'Document Title', '标题', '标题/Title'],
            'abstract': ['Abstract', 'Abstract', '摘要', '摘要/Abstract'],
            'doi': ['DOI', 'DOI', 'DOI']
        }
        
        # 找到实际存在的列
        found_columns = {}
        for key, possible_names in column_mappings.items():
            for name in possible_names:
                if name in df.columns:
                    found_columns[key] = name
                    break
        
        if not found_columns:
            raise ValueError("未找到任何标准列，请检查数据格式")
        
        print(f"    ✅ 找到关键列: {list(found_columns.keys())}")
        
        # 提取关键列
        key_columns = list(found_columns.values())
        df_key = df[key_columns].copy()
        
        # 重命名为标准名称
        df_key.columns = list(found_columns.keys())
        
        return df_key
    
    def _clean_and_standardize(self, df: pd.DataFrame) -> pd.DataFrame:
        """清理和标准化数据"""
        
        print("  🧹 清理和标准化数据...")
        
        original_count = len(df)
        
        # 移除完全重复的行
        df = df.drop_duplicates()
        duplicate_count = original_count - len(df)
        if duplicate_count > 0:
            print(f"    - 移除重复文献: {duplicate_count} 篇")
        
        # 移除没有标题的记录
        if 'title' in df.columns:
            no_title_count = df['title'].isna().sum()
            if no_title_count > 0:
                df = df[df['title'].notna()]
                print(f"    - 移除无标题文献: {no_title_count} 篇")
        
        # 标准化年份格式
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
            invalid_year_count = df['year'].isna().sum()
            if invalid_year_count > 0:
                df = df[df['year'].notna()]
                print(f"    - 移除无效年份: {invalid_year_count} 篇")
        
        # 按年份降序排序（最新的在前）
        if 'year' in df.columns:
            df = df.sort_values('year', ascending=False)
        
        # 重置索引
        df = df.reset_index(drop=True)
        
        print(f"    ✅ 清理完成: 剩余 {len(df)} 篇文献")
        
        return df
    
    def _save_results(self, df: pd.DataFrame, output_file: Path) -> Path:
        """保存处理结果"""
        
        # 重命名为中英文对照格式（保持与原系统兼容）
        column_mapping = {
            'authors': '作者/Authors',
            'year': '年份/Year', 
            'title': '标题/Title',
            'abstract': '摘要/Abstract',
            'doi': 'DOI'
        }
        
        df_output = df.copy()
        df_output.columns = [column_mapping.get(col, col) for col in df.columns]
        
        # 保存为CSV（带序号）
        df_output.to_csv(
            output_file,
            index_label='序号',
            encoding='utf-8-sig'
        )
        
        # 同时保存为Excel格式
        excel_file = output_file.with_suffix('.xlsx')
        df_output.to_excel(excel_file, index=False)
        
        print(f"    ✅ CSV文件已保存: {output_file}")
        print(f"    ✅ Excel文件已保存: {excel_file}")
        
        return output_file
    
    def _generate_statistics(self, df: pd.DataFrame) -> Dict[str, any]:
        """生成统计信息"""
        
        print("  📊 生成统计信息...")
        
        stats = {
            "total_records": len(df),
            "columns": list(df.columns)
        }
        
        # 年份统计
        if 'year' in df.columns:
            year_range = f"{int(df['year'].min())} - {int(df['year'].max())}"
            stats["year_range"] = year_range
            
            # 年份分布（前10）
            year_counts = df['year'].value_counts().head(10).to_dict()
            stats["year_distribution"] = {int(k): v for k, v in year_counts.items()}
        
        # DOI统计
        if 'doi' in df.columns:
            doi_count = df['doi'].notna().sum()
            stats["doi_count"] = doi_count
            stats["doi_percentage"] = round(doi_count / len(df) * 100, 1)
        
        # 摘要统计
        if 'abstract' in df.columns:
            abstract_count = df['abstract'].notna().sum()
            stats["abstract_count"] = abstract_count
            stats["abstract_percentage"] = round(abstract_count / len(df) * 100, 1)
        
        # 显示统计信息
        print(f"\n  📈 【统计摘要】")
        print(f"    总文献数: {stats['total_records']}")
        if 'year_range' in stats:
            print(f"    年份范围: {stats['year_range']}")
        if 'doi_count' in stats:
            print(f"    有DOI的文献: {stats['doi_count']} 篇 ({stats['doi_percentage']}%)")
        if 'abstract_count' in stats:
            print(f"    有摘要的文献: {stats['abstract_count']} 篇 ({stats['abstract_percentage']}%)")
        
        return stats
    
    def preview_data(self, df: pd.DataFrame, n: int = 5) -> None:
        """预览数据"""
        
        print(f"\n  👀 【前{n}篇文献预览】")
        print("-" * 70)
        
        for i, row in df.head(n).iterrows():
            print(f"\n{i+1}. {row.get('authors', 'N/A')} ({int(row.get('year', 0))})")
            title = str(row.get('title', 'N/A'))
            print(f"   {title[:80]}{'...' if len(title) > 80 else ''}")
            
            if 'abstract' in row and pd.notna(row['abstract']):
                abstract = str(row['abstract'])
                print(f"   摘要: {abstract[:100]}{'...' if len(abstract) > 100 else ''}")
            
            doi = row.get('doi', 'N/A')
            print(f"   DOI: {doi if pd.notna(doi) else 'N/A'}")


# 便捷函数，保持与原脚本的兼容性
def preprocess_wos_data(
    input_source: Union[str, List[str], pd.DataFrame] = "auto",
    output_dir: str = "data",
    output_filename: str = "literature_data_processed.csv"
) -> Dict[str, any]:
    """
    便捷函数：预处理WOS数据
    
    Parameters:
    -----------
    input_source : Union[str, List[str], pd.DataFrame]
        输入源
    output_dir : str
        输出目录
    output_filename : str
        输出文件名
        
    Returns:
    --------
    Dict[str, any]: 处理结果
    """
    
    from core.llm import LiteratureLLM
    
    # 创建LLM实例
    llm = LiteratureLLM()
    
    # 创建数据预处理Agent
    agent = DataPreprocessingAgent(llm)
    
    # 运行预处理
    return agent.run(
        input_source=input_source,
        output_dir=output_dir,
        output_filename=output_filename
    )


if __name__ == '__main__':
    # 直接运行时的测试代码
    result = preprocess_wos_data()
    
    if result["success"]:
        print(f"\n🎉 预处理成功！")
        print(f"📁 输出文件: {result['output_file']}")
        print(f"📊 处理记录: {result['total_records']} 篇")
    else:
        print(f"\n❌ 预处理失败: {result['error']}")