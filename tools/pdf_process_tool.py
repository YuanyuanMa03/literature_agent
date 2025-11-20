#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF处理工具 - 将PDF转换为图片供OCR识别
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from pdf2image import convert_from_path
from PIL import Image


class PDFProcessTool:
    """PDF处理工具 - 转换PDF为图片"""
    
    def __init__(self, output_dir: str = "./pdf_images"):
        """
        初始化PDF处理工具
        
        Parameters:
        -----------
        output_dir : str
            图片输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def convert_pdf_to_images(
        self,
        pdf_path: str,
        dpi: int = 300,
        fmt: str = 'PNG'
    ) -> List[Path]:
        """
        将PDF转换为图片
        
        Parameters:
        -----------
        pdf_path : str
            PDF文件路径
        dpi : int
            图片分辨率（DPI）
        fmt : str
            输出格式（PNG/JPEG）
            
        Returns:
        --------
        List[Path] : 生成的图片路径列表
        """
        pdf_path = Path(pdf_path)
        
        # 为每个PDF创建子目录
        pdf_name = pdf_path.stem
        image_dir = self.output_dir / pdf_name
        image_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 转换PDF为图片
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                fmt=fmt,
                thread_count=4,
                use_pdftocairo=True  # 更好的渲染质量
            )
            
            image_paths = []
            for i, image in enumerate(images, 1):
                image_path = image_dir / f"page_{i:03d}.{fmt.lower()}"
                image.save(image_path, fmt)
                image_paths.append(image_path)
            
            print(f"✅ {pdf_name}: {len(image_paths)} 页")
            return image_paths
            
        except Exception as e:
            print(f"❌ {pdf_name}: {e}")
            return []
    
    def batch_convert(
        self,
        pdf_paths: List[Path],
        dpi: int = 300
    ) -> Dict[str, List[Path]]:
        """
        批量转换PDF
        
        Parameters:
        -----------
        pdf_paths : List[Path]
            PDF文件路径列表
        dpi : int
            图片分辨率
            
        Returns:
        --------
        Dict : {pdf_name: [image_paths]}
        """
        results = {}
        total = len(pdf_paths)
        
        print(f"\n📄 开始转换 {total} 个PDF...")
        
        for idx, pdf_path in enumerate(pdf_paths, 1):
            print(f"[{idx}/{total}] ", end="")
            
            image_paths = self.convert_pdf_to_images(pdf_path, dpi=dpi)
            if image_paths:
                results[pdf_path.stem] = image_paths
        
        success = len(results)
        print(f"\n📊 转换完成: {success}/{total} 成功")
        
        return results
    
    def extract_images_from_pdf(
        self,
        pdf_path: str,
        min_width: int = 100,
        min_height: int = 100
    ) -> List[Path]:
        """
        从PDF中提取嵌入的图片（如表格、图表）
        
        Parameters:
        -----------
        pdf_path : str
            PDF文件路径
        min_width : int
            最小图片宽度
        min_height : int
            最小图片高度
            
        Returns:
        --------
        List[Path] : 提取的图片路径
        """
        import fitz  # PyMuPDF
        
        pdf_path = Path(pdf_path)
        pdf_name = pdf_path.stem
        image_dir = self.output_dir / pdf_name / "extracted_images"
        image_dir.mkdir(parents=True, exist_ok=True)
        
        image_paths = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                images = page.get_images()
                
                for img_idx, img in enumerate(images):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # 保存图片
                    img_path = image_dir / f"page_{page_num+1}_img_{img_idx+1}.png"
                    
                    with open(img_path, "wb") as f:
                        f.write(image_bytes)
                    
                    # 检查尺寸
                    img = Image.open(img_path)
                    if img.width >= min_width and img.height >= min_height:
                        image_paths.append(img_path)
                    else:
                        img_path.unlink()  # 删除过小的图片
            
            doc.close()
            print(f"✅ {pdf_name}: 提取 {len(image_paths)} 张图片")
            
        except Exception as e:
            print(f"❌ {pdf_name}: {e}")
        
        return image_paths
