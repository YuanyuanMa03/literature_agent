#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献分析Agent
"""

import pandas as pd
import time
from typing import List, Dict
from core.agent import Agent
from tools.extraction_tool import DataExtractionTool


class LiteratureAnalysisAgent(Agent):
    """文献分析智能体"""
    
    def __init__(self, llm, **kwargs):
        super().__init__(
            name="文献分析Agent",
            llm=llm,
            **kwargs
        )
        self.extraction_tool = DataExtractionTool(llm)
    
    def _default_system_prompt(self) -> str:
        return """你是一个专业的土壤科学文献分析助手。
你的任务是从文献中提取SOC相关的关键数据和信息，
包括SOC含量、土壤深度、土地利用类型等，并生成结构化的总结。"""
    
    def run(self, df: pd.DataFrame, max_papers: int = 50) -> pd.DataFrame:
        """
        分析通过筛选的文献
        
        Parameters:
        -----------
        df : DataFrame
            筛选后的文献数据
        max_papers : int
            最多分析的文献数量
            
        Returns:
        --------
        DataFrame : 添加了分析结果的数据框
        """
        print(f"\n{'='*70}")
        print(f"📊 {self.name} 开始工作")
        print(f"{'='*70}")
        
        # 只分析通过筛选的文献
        passed_df = df[df['LLM_Decision'] == 'accept'].copy()
        
        if len(passed_df) == 0:
            print("⚠️  没有通过筛选的文献")
            return df
        
        # 限制数量
        if len(passed_df) > max_papers:
            print(f"⚠️  文献数量过多，只分析前{max_papers}篇")
            passed_df = passed_df.head(max_papers)
        
        print(f"\n开始分析 {len(passed_df)} 篇文献...")
        
        # 初始化结果列
        df['Extracted_Data'] = None
        df['Summary'] = None
        
        for idx, row in passed_df.iterrows():
            print(f"[{idx+1}/{len(passed_df)}] 分析中...", end='\r')
            
            # 提取数据
            extracted = self.extraction_tool.extract_soc_data(
                title=row['Article Title'],
                abstract=row['Abstract']
            )
            
            # 生成总结
            summary = self.extraction_tool.summarize_paper(
                title=row['Article Title'],
                abstract=row['Abstract']
            )
            
            df.at[idx, 'Extracted_Data'] = str(extracted)
            df.at[idx, 'Summary'] = summary
            
            # 避免API限流（因为调用了两次API，所以等待时间更长）
            time.sleep(10)
        
        print(f"\n✅ 分析完成！")
        
        return df
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """
        生成综合分析报告
        
        Parameters:
        -----------
        df : DataFrame
            分析后的数据
            
        Returns:
        --------
        str : Markdown格式的报告
        """
        passed_df = df[df['LLM_Decision'] == 'accept']
        
        prompt = f"""基于以下{len(passed_df)}篇通过筛选的SOC文献，生成一份综合分析报告。

**要求：**
1. 使用Markdown格式
2. 包括：研究概览、主要发现、数据特征、研究趋势
3. 突出关键数据和发现
4. 长度控制在500-800字

**文献信息：**
{self._prepare_literature_summary(passed_df)}

请生成报告：
"""
        
        try:
            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            return response
        except Exception as e:
            return f"报告生成失败: {str(e)}"
    
    def _prepare_literature_summary(self, df: pd.DataFrame) -> str:
        """准备文献摘要"""
        summaries = []
        for idx, row in df.head(20).iterrows():  # 只使用前20篇
            summary = f"{idx+1}. {row['Article Title']} ({row.get('Publication Year', 'N/A')})"
            if 'Summary' in row and pd.notna(row['Summary']):
                summary += f"\n   {row['Summary']}"
            summaries.append(summary)
        
        return "\n\n".join(summaries)
