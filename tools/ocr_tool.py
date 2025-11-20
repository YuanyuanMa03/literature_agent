#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR工具 - 使用DeepSeek-OCR识别图片中的文字、表格
"""

import os
import base64
import json
from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI


class DeepSeekOCRTool:
    """DeepSeek-OCR工具"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        初始化OCR工具
        
        Parameters:
        -----------
        api_key : str
            API Key（默认使用OPENAI_API_KEY）
        base_url : str
            API地址（默认使用OPENAI_API_BASE，即硅基流动）
        """
        # 统一使用硅基流动的配置
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('OPENAI_API_BASE', 'https://api.siliconflow.cn/v1')
        
        if not self.api_key:
            raise ValueError("需要提供API Key（OPENAI_API_KEY）")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # 硅基流动中的DeepSeek-OCR模型名称
        self.model = "deepseek-ai/DeepSeek-OCR"
    
    def extract_from_image(
        self,
        image_path: str,
        extract_tables: bool = True,
        extract_figures: bool = True
    ) -> Dict:
        """
        从图片中提取文字、表格、图表
        
        Parameters:
        -----------
        image_path : str
            图片路径
        extract_tables : bool
            是否提取表格
        extract_figures : bool
            是否提取图表
            
        Returns:
        --------
        Dict : {
            'text': 识别的文字,
            'tables': 表格数据列表,
            'figures': 图表描述列表,
            'metadata': 元数据
        }
        """
        # 读取并编码图片
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # 构建提示词
        prompt = self._build_prompt(extract_tables, extract_figures)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            # 解析结果
            result = self._parse_ocr_result(content)
            result['image_path'] = str(image_path)
            
            return result
            
        except Exception as e:
            print(f"❌ OCR失败: {e}")
            return {
                'text': '',
                'tables': [],
                'figures': [],
                'error': str(e)
            }
    
    def batch_extract(
        self,
        image_paths: List[Path],
        extract_tables: bool = True
    ) -> Dict[str, Dict]:
        """
        批量OCR识别
        
        Parameters:
        -----------
        image_paths : List[Path]
            图片路径列表
        extract_tables : bool
            是否提取表格
            
        Returns:
        --------
        Dict : {image_name: ocr_result}
        """
        results = {}
        total = len(image_paths)
        
        print(f"\n👁️  开始OCR识别 {total} 张图片...")
        
        for idx, image_path in enumerate(image_paths, 1):
            print(f"[{idx}/{total}] {image_path.name}...", end=" ")
            
            result = self.extract_from_image(
                str(image_path),
                extract_tables=extract_tables
            )
            
            if result.get('error'):
                print(f"❌")
            else:
                print(f"✅")
            
            results[image_path.name] = result
        
        print(f"\n📊 OCR完成: {len(results)} 张图片")
        
        return results
    
    def _build_prompt(
        self,
        extract_tables: bool,
        extract_figures: bool
    ) -> str:
        """构建OCR提示词"""
        prompt = """请仔细分析这张图片，提取以下信息：

1. **文字内容**：识别图片中的所有文字，保持原有格式和结构。

"""
        
        if extract_tables:
            prompt += """2. **表格数据**：如果图片中包含表格，请提取表格内容，以Markdown格式输出。
   - 保留表头
   - 保留所有数据行
   - 标注单位和说明

"""
        
        if extract_figures:
            prompt += """3. **图表信息**：如果图片中包含图表（如折线图、柱状图、散点图），请描述：
   - 图表类型
   - X轴和Y轴标签
   - 主要趋势或发现
   - 图例说明

"""
        
        prompt += """4. **数据可用性**：识别是否有 "Data Availability" 或相关的数据链接、仓库信息。

请以JSON格式返回结果：
```json
{
  "text": "识别的文字内容",
  "tables": [
    {"title": "表格标题", "content": "Markdown格式的表格"}
  ],
  "figures": [
    {"type": "图表类型", "description": "描述"}
  ],
  "data_availability": "数据可用性信息（如果有）"
}
```"""
        
        return prompt
    
    def _parse_ocr_result(self, content: str) -> Dict:
        """解析OCR结果"""
        try:
            # 尝试提取JSON
            import re
            json_match = re.search(r'```json\s*({.*})\s*```', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(1))
                return data
            
            # 尝试直接解析
            data = json.loads(content)
            return data
            
        except:
            # 如果解析失败，返回原始文本
            return {
                'text': content,
                'tables': [],
                'figures': [],
                'data_availability': None
            }
