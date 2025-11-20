#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度分析Agent - 综合PDF、OCR、深度分析
"""

import pandas as pd
import json
from pathlib import Path
from typing import List, Dict
from core.agent import Agent
from tools.pdf_process_tool import PDFProcessTool
from tools.ocr_tool import DeepSeekOCRTool
from tools.deep_analysis_tool import DeepAnalysisTool


class DeepAnalysisAgent(Agent):
    """深度分析智能体 - PDF全文深度挖掘"""
    
    def __init__(
        self,
        llm,
        pdf_dir: str = "./pdfs",
        image_dir: str = "./pdf_images",
        **kwargs
    ):
        super().__init__(
            name="深度分析Agent",
            llm=llm,
            **kwargs
        )
        
        self.pdf_dir = Path(pdf_dir)
        self.pdf_process_tool = PDFProcessTool(output_dir=image_dir)
        self.ocr_tool = DeepSeekOCRTool()
        self.analysis_tool = DeepAnalysisTool(llm)
    
    def _default_system_prompt(self) -> str:
        return """你是一个深度文献分析专家。
你的任务是从PDF全文中提取表格、图像、数据集等关键信息，
并进行综合分析和总结。"""
    
    def run(
        self,
        download_results: Dict,
        max_papers: int = 10
    ) -> pd.DataFrame:
        """
        深度分析PDF文献
        
        Parameters:
        -----------
        download_results : Dict
            PDF下载结果
        max_papers : int
            最多分析的文献数量
            
        Returns:
        --------
        DataFrame : 深度分析结果
        """
        print(f"\n{'='*70}")
        print(f"🔍 {self.name} 开始工作")
        print(f"{'='*70}")
        
        # 获取成功下载的PDF
        pdf_files = []
        for doi, result in download_results.get('results', {}).items():
            if result['status'] in ['success', 'exists'] and result.get('path'):
                pdf_files.append({
                    'doi': doi,
                    'path': Path(result['path'])
                })
        
        if not pdf_files:
            print("⚠️  没有可分析的PDF文件")
            return pd.DataFrame()
        
        # 限制数量
        if len(pdf_files) > max_papers:
            print(f"⚠️  PDF数量过多，只分析前{max_papers}篇")
            pdf_files = pdf_files[:max_papers]
        
        print(f"待分析PDF: {len(pdf_files)} 篇\n")
        
        analysis_results = []
        
        for idx, pdf_info in enumerate(pdf_files, 1):
            print(f"【{idx}/{len(pdf_files)}】{pdf_info['path'].stem}")
            
            try:
                # Step 1: PDF转图片
                print("  📄 转换PDF...", end=" ")
                image_paths = self.pdf_process_tool.convert_pdf_to_images(
                    pdf_info['path'],
                    dpi=200  # 降低DPI加快速度
                )
                print(f"{len(image_paths)} 页")
                
                if not image_paths:
                    print("  ❌ PDF转换失败")
                    continue
                
                # Step 2: OCR识别（只处理前10页，避免超时）
                print("  👁️  OCR识别...", end=" ")
                ocr_results_list = []
                
                for img_path in image_paths[:10]:
                    ocr_result = self.ocr_tool.extract_from_image(
                        str(img_path),
                        extract_tables=True,
                        extract_figures=True
                    )
                    ocr_results_list.append(ocr_result)
                
                print(f"✅ {len(ocr_results_list)} 页")
                
                # Step 3: 深度分析
                print("  🔍 深度分析...", end=" ")
                analysis = self.analysis_tool.analyze_paper_content(
                    paper_title=pdf_info['path'].stem,
                    ocr_results=ocr_results_list,
                    doi=pdf_info['doi']
                )
                print("✅")
                
                # 整理结果
                result_record = {
                    'DOI': pdf_info['doi'],
                    'PDF_Path': str(pdf_info['path']),
                    'Pages_Analyzed': len(ocr_results_list),
                    'Tables_Count': len(analysis.get('tables_summary', [])),
                    'Figures_Count': len(analysis.get('figures_summary', [])),
                    'Tables_Summary': json.dumps(analysis.get('tables_summary', []), ensure_ascii=False),
                    'Figures_Summary': json.dumps(analysis.get('figures_summary', []), ensure_ascii=False),
                    'Data_Availability': json.dumps(analysis.get('data_availability', {}), ensure_ascii=False),
                    'Key_Datasets': json.dumps(analysis.get('key_datasets', []), ensure_ascii=False),
                    'Methods': json.dumps(analysis.get('methods', {}), ensure_ascii=False)
                }
                
                analysis_results.append(result_record)
                
                print()  # 换行
                
            except Exception as e:
                print(f"  ❌ 分析失败: {e}\n")
                continue
        
        # 转为DataFrame
        if analysis_results:
            df = pd.DataFrame(analysis_results)
            
            # 保存结果
            output_file = 'deep_analysis_results.xlsx'
            df.to_excel(output_file, index=False)
            print(f"\n💾 深度分析结果已保存: {output_file}")
            
            # 保存详细的JSON结果
            json_file = 'deep_analysis_results.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, ensure_ascii=False, indent=2)
            print(f"💾 JSON结果已保存: {json_file}")
            
            return df
        else:
            print("❌ 没有成功分析的文献")
            return pd.DataFrame()
