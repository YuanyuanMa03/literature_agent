#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据提取工具
"""

import json
from typing import Dict, Optional
from core.llm import LiteratureLLM


class DataExtractionTool:
    """SOC数据提取工具"""
    
    def __init__(self, llm: LiteratureLLM):
        self.llm = llm
        self.name = "数据提取工具"
    
    def extract_soc_data(self, title: str, abstract: str) -> Dict:
        """
        从摘要中提取SOC相关数据
        
        Parameters:
        -----------
        title : str
            文献标题
        abstract : str
            文献摘要
            
        Returns:
        --------
        dict : 提取的数据
        """
        prompt = f"""从以下文献摘要中提取土壤有机碳(SOC)相关的关键数据和信息。

**文献信息：**
标题: {title}
摘要: {abstract}

**需要提取的信息（如果有）：**
1. SOC含量范围或均值
2. 土壤深度信息
3. 土壤类型或质地
4. 研究地点/气候带
5. 土地利用类型
6. 是否提到POM/MAOM分组
7. 是否提到饱和相关概念
8. 关键发现或结论

**重要：只返回纯JSON格式。如果某项信息没有，填null。**

返回格式：
{{
    "soc_content": "SOC含量信息",
    "soil_depth": "土壤深度",
    "soil_type": "土壤类型",
    "location": "研究地点",
    "land_use": "土地利用",
    "has_fractionation": true/false,
    "has_saturation": true/false,
    "key_findings": "关键发现"
}}
"""
        
        try:
            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=800,
                json_mode=True
            )
            
            result = json.loads(response)
            return result
            
        except Exception as e:
            print(f"⚠️  数据提取失败: {e}")
            return {
                "soc_content": None,
                "soil_depth": None,
                "soil_type": None,
                "location": None,
                "land_use": None,
                "has_fractionation": False,
                "has_saturation": False,
                "key_findings": f"提取失败: {str(e)}"
            }
    
    def summarize_paper(self, title: str, abstract: str) -> str:
        """
        生成文献摘要总结
        
        Parameters:
        -----------
        title : str
            文献标题
        abstract : str
            文献摘要
            
        Returns:
        --------
        str : 总结文本
        """
        prompt = f"""请用中文简要总结以下SOC相关文献的核心内容（3-5句话）。

标题: {title}
摘要: {abstract}

总结要点：
1. 研究对象和方法
2. 主要发现
3. 数据特点
"""
        
        try:
            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            return response
            
        except Exception as e:
            return f"总结生成失败: {str(e)}"
