#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度分析工具 - 使用Qwen分析OCR提取的内容
"""

import json
from typing import List, Dict, Optional
from core.llm import LiteratureLLM


class DeepAnalysisTool:
    """深度分析工具 - 分析文献全文内容"""
    
    def __init__(self, llm: LiteratureLLM):
        """
        初始化深度分析工具
        
        Parameters:
        -----------
        llm : LiteratureLLM
            LLM客户端
        """
        self.llm = llm
    
    def analyze_paper_content(
        self,
        paper_title: str,
        ocr_results: List[Dict],
        doi: str = ""
    ) -> Dict:
        """
        分析单篇文献的OCR结果
        
        Parameters:
        -----------
        paper_title : str
            文献标题
        ocr_results : List[Dict]
            OCR识别结果列表
        doi : str
            DOI号
            
        Returns:
        --------
        Dict : {
            'tables_summary': 表格汇总,
            'figures_summary': 图表汇总,
            'data_availability': 数据可用性,
            'key_datasets': 关键数据集,
            'methods': 方法总结
        }
        """
        # 整合所有OCR结果
        all_text = self._merge_ocr_results(ocr_results)
        all_tables = self._extract_all_tables(ocr_results)
        all_figures = self._extract_all_figures(ocr_results)
        data_availability = self._extract_data_availability(ocr_results)
        
        # 构建分析prompt
        prompt = self._build_analysis_prompt(
            paper_title,
            all_text,
            all_tables,
            all_figures,
            data_availability
        )
        
        try:
            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=3000,
                json_mode=True
            )
            
            result = json.loads(response)
            result['doi'] = doi
            
            return result
            
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            return {
                'error': str(e),
                'tables_summary': [],
                'figures_summary': [],
                'data_availability': data_availability,
                'key_datasets': []
            }
    
    def _merge_ocr_results(self, ocr_results: List[Dict]) -> str:
        """合并所有OCR文本"""
        texts = []
        for result in ocr_results:
            if result.get('text'):
                texts.append(result['text'])
        return "\n\n".join(texts)
    
    def _extract_all_tables(self, ocr_results: List[Dict]) -> List[Dict]:
        """提取所有表格"""
        tables = []
        for page_idx, result in enumerate(ocr_results):
            if result.get('tables'):
                for table in result['tables']:
                    table['page'] = page_idx + 1
                    tables.append(table)
        return tables
    
    def _extract_all_figures(self, ocr_results: List[Dict]) -> List[Dict]:
        """提取所有图表"""
        figures = []
        for page_idx, result in enumerate(ocr_results):
            if result.get('figures'):
                for figure in result['figures']:
                    figure['page'] = page_idx + 1
                    figures.append(figure)
        return figures
    
    def _extract_data_availability(self, ocr_results: List[Dict]) -> Optional[str]:
        """提取数据可用性信息"""
        for result in ocr_results:
            if result.get('data_availability'):
                return result['data_availability']
        return None
    
    def _build_analysis_prompt(
        self,
        title: str,
        text: str,
        tables: List[Dict],
        figures: List[Dict],
        data_availability: Optional[str]
    ) -> str:
        """构建深度分析prompt"""
        prompt = f"""请深度分析以下文献的全文内容，提取关键信息。

**文献标题：** {title}

**文献内容：**
{text[:5000]}  # 限制长度避免超token

**表格数量：** {len(tables)}
**图表数量：** {len(figures)}
**数据可用性：** {data_availability or "未找到"}

---

**分析任务：**

1. **表格总结**：
   - 列出所有表格的标题和主要内容
   - 标注关键数据（如SOC含量、土壤类型、处理方式等）
   - 注明表格所在页码

2. **图表总结**：
   - 列出所有图表的类型和主要发现
   - 描述趋势和关键结论
   - 注明图表所在页码

3. **数据集提取**：
   - 提取文中提到的所有数据集名称
   - 提取数据仓库链接（如Zenodo、Figshare、GitHub等）
   - 提取补充材料链接

4. **方法总结**：
   - 总结主要研究方法
   - 总结数据采集和分析方法

**输出格式（JSON）：**
```json
{{
  "tables_summary": [
    {{
      "page": 页码,
      "title": "表格标题",
      "key_data": "关键数据描述",
      "variables": ["变量1", "变量2"]
    }}
  ],
  "figures_summary": [
    {{
      "page": 页码,
      "type": "图表类型",
      "finding": "主要发现"
    }}
  ],
  "data_availability": {{
    "statement": "数据可用性声明",
    "repositories": ["仓库链接1", "仓库链接2"],
    "datasets": ["数据集名称1", "数据集名称2"]
  }},
  "key_datasets": [
    {{
      "name": "数据集名称",
      "source": "来源",
      "url": "链接（如果有）"
    }}
  ],
  "methods": {{
    "sampling": "采样方法",
    "analysis": "分析方法",
    "instruments": ["使用的仪器"]
  }}
}}
```

请仅返回JSON，不要其他文字。
"""
        return prompt
