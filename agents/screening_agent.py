#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献筛选Agent
"""

import pandas as pd
from typing import Dict
from core.agent import Agent
from core.message import Message
from tools.screening_tool import LiteratureScreeningTool


class LiteratureScreeningAgent(Agent):
    """文献筛选智能体"""
    
    def __init__(self, llm, **kwargs):
        super().__init__(
            name="文献筛选Agent",
            llm=llm,
            **kwargs
        )
        self.screening_tool = LiteratureScreeningTool(llm)
    
    def _default_system_prompt(self) -> str:
        return """你是一个专业的土壤科学文献筛选助手。
你的任务是判断文献是否包含土壤有机碳(SOC)的数据或测量结果。
你需要准确识别SOC相关术语，判断是否有数据支持，并给出清晰的理由。"""
    
    def run(self, df: pd.DataFrame, start_idx: int = 0) -> pd.DataFrame:
        """
        运行批量筛选
        
        Parameters:
        -----------
        df : DataFrame
            文献数据
        start_idx : int
            开始索引
            
        Returns:
        --------
        DataFrame : 筛选结果
        """
        print(f"\n{'='*70}")
        print(f"🔍 {self.name} 开始工作")
        print(f"{'='*70}")
        
        # 使用筛选工具
        result_df = self.screening_tool.batch_screen(df, start_idx=start_idx)
        
        # 统计结果
        accept_count = (result_df['LLM_Decision'] == 'accept').sum()
        reject_count = (result_df['LLM_Decision'] == 'reject').sum()
        error_count = (result_df['LLM_Decision'] == 'error').sum()
        
        print(f"\n📊 筛选统计：")
        print(f"   通过: {accept_count} 篇 ({accept_count/len(result_df)*100:.1f}%)")
        print(f"   未通过: {reject_count} 篇")
        print(f"   错误: {error_count} 篇")
        
        return result_df
