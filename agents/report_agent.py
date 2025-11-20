#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成Agent - 参考Report Writer
"""

import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime
from core.agent import Agent


class LiteratureReportAgent(Agent):
    """文献报告生成智能体 - 负责整合所有分析结果生成综合报告"""
    
    def __init__(self, llm, **kwargs):
        super().__init__(
            name="报告生成Agent",
            llm=llm,
            **kwargs
        )
    
    def _default_system_prompt(self) -> str:
        return """你是一个专业的科学报告撰写专家，专注于土壤科学领域。
你的任务是整合文献分析结果，生成结构化、逻辑清晰的研究报告。
报告应该包含研究概览、主要发现、数据特征、研究趋势等部分。"""
    
    def generate_comprehensive_report(
        self,
        df: pd.DataFrame,
        research_topic: str = "土壤有机碳研究",
        include_summaries: bool = True
    ) -> str:
        """
        生成综合研究报告
        
        Parameters:
        -----------
        df : DataFrame
            分析后的文献数据
        research_topic : str
            研究主题
        include_summaries : bool
            是否包含文献摘要
            
        Returns:
        --------
        str : Markdown格式的报告
        """
        print(f"\n{'='*70}")
        print(f"📄 {self.name} 开始工作")
        print(f"{'='*70}\n")
        
        # 准备统计信息
        stats = self._calculate_statistics(df)
        
        # 准备文献摘要
        summaries = ""
        if include_summaries:
            summaries = self._prepare_literature_summaries(df)
        
        # 构建Prompt
        prompt = self._build_report_prompt(
            research_topic, stats, summaries
        )
        
        try:
            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=3000
            )
            
            # 添加报告头部和尾部
            report = self._format_report(response, stats, df)
            
            print(f"✅ 报告生成完成 ({len(report)} 字符)\n")
            
            return report
            
        except Exception as e:
            print(f"❌ 报告生成失败: {e}")
            return self._generate_fallback_report(stats)
    
    def _calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """计算统计信息"""
        total = len(df)
        passed = (df.get('LLM_Decision', pd.Series()) == 'accept').sum()
        analyzed = df.get('Summary', pd.Series()).notna().sum()
        
        stats = {
            'total_papers': total,
            'passed_screening': passed,
            'deeply_analyzed': analyzed,
            'screening_rate': f"{passed/total*100:.1f}%" if total > 0 else "N/A",
            'analysis_rate': f"{analyzed/total*100:.1f}%" if total > 0 else "N/A"
        }
        
        # 提取额外信息
        if 'Publication Year' in df.columns:
            years = df['Publication Year'].dropna()
            if len(years) > 0:
                stats['year_range'] = f"{int(years.min())}-{int(years.max())}"
                stats['most_common_year'] = int(years.mode()[0]) if len(years.mode()) > 0 else "N/A"
        
        return stats
    
    def _prepare_literature_summaries(
        self,
        df: pd.DataFrame,
        max_papers: int = 30
    ) -> str:
        """准备文献摘要"""
        passed_df = df[df.get('LLM_Decision', pd.Series()) == 'accept']
        
        summaries = []
        for idx, row in passed_df.head(max_papers).iterrows():
            title = row.get('Article Title', f'文献{idx+1}')
            year = row.get('Publication Year', 'N/A')
            summary = row.get('Summary', '')
            
            if pd.notna(summary) and summary:
                summaries.append(f"**[{idx+1}] {title}** ({year})\n   {summary}")
            else:
                summaries.append(f"**[{idx+1}] {title}** ({year})")
        
        return "\n\n".join(summaries) if summaries else "无可用摘要"
    
    def _build_report_prompt(
        self,
        research_topic: str,
        stats: Dict,
        summaries: str
    ) -> str:
        """构建报告生成提示词"""
        prompt = f"""请基于以下文献分析结果，生成一份专业的研究报告。

**研究主题：** {research_topic}

**数据统计：**
- 总文献数: {stats['total_papers']} 篇
- 通过筛选: {stats['passed_screening']} 篇 ({stats['screening_rate']})
- 深度分析: {stats['deeply_analyzed']} 篇 ({stats['analysis_rate']})
{f"- 年份范围: {stats.get('year_range', 'N/A')}" if 'year_range' in stats else ""}

**文献摘要：**
{summaries[:3000]}  

**报告要求：**

1. **格式要求**
   - 使用Markdown格式
   - 包含清晰的章节标题
   - 使用列表、表格等增强可读性

2. **内容要求**
   - **研究概览**：总体介绍研究范围和数据来源
   - **主要发现**：归纳关键发现和研究结论（3-5点）
   - **数据特征**：分析数据的分布特点、研究热点
   - **研究趋势**：识别研究的时间趋势和主题演变
   - **方法论分析**：总结常用的研究方法（如果有）
   - **研究建议**：基于分析提出未来研究方向（2-3点）

3. **写作风格**
   - 学术严谨，逻辑清晰
   - 数据支撑，有理有据
   - 突出关键发现
   - 总字数800-1200字

请生成报告（仅返回报告内容，不要额外说明）：
"""
        return prompt
    
    def _format_report(
        self,
        content: str,
        stats: Dict,
        df: pd.DataFrame
    ) -> str:
        """格式化完整报告"""
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        report = f"""# 土壤有机碳文献研究报告

**生成时间：** {current_time}  
**分析文献：** {stats['total_papers']} 篇  
**有效文献：** {stats['passed_screening']} 篇

---

{content}

---

## 附录：数据统计

| 指标 | 数值 |
|------|------|
| 总文献数 | {stats['total_papers']} 篇 |
| 通过筛选 | {stats['passed_screening']} 篇 ({stats['screening_rate']}) |
| 深度分析 | {stats['deeply_analyzed']} 篇 ({stats['analysis_rate']}) |
"""
        
        if 'year_range' in stats:
            report += f"| 年份范围 | {stats['year_range']} |\n"
            report += f"| 高频年份 | {stats.get('most_common_year', 'N/A')} |\n"
        
        report += f"\n**报告生成：** {self.name} @ Literature Research System\n"
        
        return report
    
    def _generate_fallback_report(self, stats: Dict) -> str:
        """生成备用报告（当LLM失败时）"""
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        return f"""# 土壤有机碳文献研究报告

**生成时间：** {current_time}  
**生成状态：** 备用报告（LLM生成失败）

## 数据统计

- **总文献数：** {stats['total_papers']} 篇
- **通过筛选：** {stats['passed_screening']} 篇 ({stats['screening_rate']})
- **深度分析：** {stats['deeply_analyzed']} 篇

## 说明

报告生成过程中遇到错误，以上为基础统计信息。
请查看详细的Excel文件获取完整分析结果。
"""
    
    def run(self, df: pd.DataFrame, **kwargs) -> str:
        """实现基类的run方法"""
        research_topic = kwargs.get('research_topic', '土壤有机碳研究')
        include_summaries = kwargs.get('include_summaries', True)
        return self.generate_comprehensive_report(df, research_topic, include_summaries)
