#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献筛选工具
"""

import pandas as pd
import json
import time
from typing import Dict, List
from pathlib import Path
from core.llm import LiteratureLLM


class LiteratureScreeningTool:
    """文献智能筛选工具"""
    
    def __init__(self, llm: LiteratureLLM):
        self.llm = llm
        self.name = "文献筛选工具"
    
    def screen_paper(self, title: str, abstract: str) -> Dict:
        """
        筛选单篇文献
        
        Parameters:
        -----------
        title : str
            文献标题
        abstract : str
            文献摘要
            
        Returns:
        --------
        dict : 筛选结果
        """
        if pd.isna(abstract) or str(abstract).strip() == "":
            return {
                "decision": "reject",
                "has_soc": False,
                "has_data": False,
                "is_review": False,
                "reason": "无摘要",
                "confidence": 1.0
            }
        
        prompt = f"""请判断以下文献是否包含土壤有机碳(SOC)的数据或测量结果。

**判断标准：**
1. 摘要中提到了SOC相关术语（如SOC、soil organic carbon、soil carbon等）
2. 摘要中提到有数据、测量、分析或量化结果

**文献信息：**
标题: {title}
摘要: {abstract}

**重要：只返回纯JSON格式，不要任何额外文字。**

返回格式：
{{"decision": "accept或reject", "has_soc": true/false, "has_data": true/false, "is_review": true/false, "reason": "判断理由", "confidence": 0-1的数值}}
"""
        
        try:
            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500,
                json_mode=True
            )
            
            result = json.loads(response)
            return result
            
        except Exception as e:
            print(f"⚠️  筛选失败: {e}")
            return {
                "decision": "error",
                "has_soc": False,
                "has_data": False,
                "is_review": False,
                "reason": f"处理失败: {str(e)}",
                "confidence": 0.0
            }
    
    def batch_screen(
        self,
        df: pd.DataFrame,
        start_idx: int = 0,
        save_interval: int = 10
    ) -> pd.DataFrame:
        """
        批量筛选文献
        
        Parameters:
        -----------
        df : DataFrame
            文献数据
        start_idx : int
            开始索引
        save_interval : int
            保存间隔
            
        Returns:
        --------
        DataFrame : 添加了筛选结果的数据框
        """
        print(f"\n开始批量筛选 {len(df)-start_idx} 篇文献...")
        
        # 初始化结果列
        if 'LLM_Decision' not in df.columns:
            df['LLM_Decision'] = None
            df['LLM_Has_SOC'] = None
            df['LLM_Has_Data'] = None
            df['LLM_Is_Review'] = None
            df['LLM_Reason'] = None
            df['LLM_Confidence'] = None
        
        for idx in range(start_idx, len(df)):
            row = df.iloc[idx]
            
            print(f"[{idx+1}/{len(df)}] 处理中...", end='\r')
            
            # 筛选
            result = self.screen_paper(
                title=row.get('Article Title', ''),
                abstract=row.get('Abstract', '')
            )
            
            # 保存结果
            df.at[idx, 'LLM_Decision'] = result.get('decision', 'error')
            df.at[idx, 'LLM_Has_SOC'] = result.get('has_soc', False)
            df.at[idx, 'LLM_Has_Data'] = result.get('has_data', False)
            df.at[idx, 'LLM_Is_Review'] = result.get('is_review', False)
            df.at[idx, 'LLM_Reason'] = result.get('reason', '')
            df.at[idx, 'LLM_Confidence'] = result.get('confidence', 0.0)
            
            # 定期保存
            if (idx + 1) % save_interval == 0:
                checkpoint_file = 'checkpoint_screening.csv'
                df.to_csv(checkpoint_file, index=False)
                print(f"\n💾 已保存checkpoint: {idx+1}/{len(df)}")
            
            # 避免API限流
            time.sleep(5)
        
        print(f"\n✅ 筛选完成！")
        return df
