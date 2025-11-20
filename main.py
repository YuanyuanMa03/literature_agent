#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献分析Agent系统 - 增强版主程序
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv 

from core.llm import LiteratureLLM # 导入LLM模型
from core.progress_tracker import ProgressTracker # 导入进度追踪器
from agents.planning_agent import ResearchPlanningAgent # 导入规划Agent
from agents.data_preprocessing_agent import DataPreprocessingAgent # 导入数据预处理Agent
from agents.screening_agent import LiteratureScreeningAgent # 导入筛选Agent
from agents.analysis_agent import LiteratureAnalysisAgent # 导入分析Agent
from agents.report_agent import LiteratureReportAgent # 导入报告Agent

load_dotenv()


class LiteratureResearchSystem:
    """
    文献研究系统 - TODO驱动的研究范式（增强版）
    
    - 数据预处理Agent：处理原始WOS数据，生成标准格式
    - 规划Agent：分解研究任务
    - 筛选Agent：智能筛选文献
    - 分析Agent：深度提取数据
    - 报告Agent：生成综合报告
    - 进度追踪：实时监控流程
    """
    
    def __init__(self, enable_progress_tracking: bool = True):
        """
        初始化系统
        
        Parameters:
        -----------
        enable_progress_tracking : bool
            是否启用进度追踪
        """
        print("="*70)
        print("🔬 文献分析Agent系统 - Enhanced Edition")
        print("="*70)
        
        # 初始化LLM
        self.llm = LiteratureLLM(
            model=os.getenv("LLM_MODEL", "Qwen/Qwen3-Omni-30B-A3B-Instruct"),
            temperature=0.1
        )
        
        # 初始化进度追踪器
        self.progress = ProgressTracker() if enable_progress_tracking else None
        
        # 初始化Agents
        self.preprocessing_agent = DataPreprocessingAgent(self.llm)
        self.planning_agent = ResearchPlanningAgent(self.llm)
        self.screening_agent = LiteratureScreeningAgent(self.llm)
        self.analysis_agent = LiteratureAnalysisAgent(self.llm)
        self.report_agent = LiteratureReportAgent(self.llm)
        
        print("\n✅ 系统初始化完成（包含5个专业Agent）\n")
    
    def load_literature(
        self,
        file_pattern: str = "*",
        task_id: str = "load"
    ) -> pd.DataFrame:
        """
        加载文献数据（支持 .xls, .xlsx, .csv 格式）
        
        Parameters:
        -----------
        file_pattern : str
            文件模式（默认匹配所有文献文件）
        task_id : str
            任务ID（用于进度追踪）
            
        Returns:
        --------
        DataFrame : 合并后的文献数据（列名已标准化）
        """
        if self.progress:
            self.progress.start_task(task_id)
        
        print("📁 加载文献数据...")
        
        # 支持多种文献数据格式
        supported_extensions = ['.xls', '.xlsx', '.csv']
        all_files = []
        
        for ext in supported_extensions:
            pattern = file_pattern if file_pattern.endswith(ext) else f"{file_pattern}{ext}"
            all_files.extend(Path('.').glob(pattern))
        
        # 去重并排序
        files = sorted(set(all_files))
        
        if not files:
            error_msg = f"未找到匹配的文件: {file_pattern} (支持格式: {', '.join(supported_extensions)})"
            if self.progress:
                self.progress.fail_task(task_id, error_msg)
            raise FileNotFoundError(error_msg)
        
        dfs = []
        total_files = len(files)
        
        for idx, file in enumerate(files, 1):
            try:
                # 根据文件扩展名选择读取方法
                if file.suffix.lower() == '.csv':
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                # 标准化列名
                df = self._standardize_columns(df)
                
                dfs.append(df)
                print(f"   ✅ {file.name}: {len(df)} 篇")
                
                if self.progress:
                    progress = int((idx / total_files) * 100)
                    self.progress.update_task_progress(
                        task_id, progress,
                        f"已加载 {idx}/{total_files} 个文件"
                    )
            except Exception as e:
                print(f"   ❌ {file.name}: {e}")
        
        if not dfs:
            error_msg = "没有成功加载任何文件"
            if self.progress:
                self.progress.fail_task(task_id, error_msg)
            raise ValueError(error_msg)
        
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"\n📊 总计: {len(combined_df)} 篇文献\n")
        
        if self.progress:
            self.progress.complete_task(task_id, f"{len(combined_df)} 篇文献")
        
        return combined_df
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        标准化DataFrame列名
        
        支持中英文列名映射：
        - 标题/Title -> Article Title
        - 摘要/Abstract -> Abstract
        - 作者/Authors -> Authors
        - 年份/Year -> Publication Year
        - DOI -> DOI
        """
        column_mapping = {
            '标题/Title': 'Article Title',
            'Title': 'Article Title',
            '标题': 'Article Title',
            'title': 'Article Title',
            
            '摘要/Abstract': 'Abstract',
            'Abstract': 'Abstract',
            '摘要': 'Abstract',
            'abstract': 'Abstract',
            
            '作者/Authors': 'Authors',
            'Authors': 'Authors',
            '作者': 'Authors',
            'authors': 'Authors',
            
            '年份/Year': 'Publication Year',
            'Year': 'Publication Year',
            '年份': 'Publication Year',
            'year': 'Publication Year',
            
            'DOI': 'DOI',
            'doi': 'DOI'
        }
        
        # 重命名列
        df = df.rename(columns=column_mapping)
        
        # 确保必需列存在
        required_columns = ['Article Title', 'Abstract']
        for col in required_columns:
            if col not in df.columns:
                # 尝试从现有列中找到最接近的
                print(f"⚠️  警告: 未找到列 '{col}'，可用列: {list(df.columns)}")
        
        return df
    
    def run_research(
        self,
        research_topic: str = "土壤有机碳饱和机制",
        test_mode: bool = True,
        test_size: int = 10,
        analyze_top: int = 20,
        enable_planning: bool = True
    ):
        """
        运行完整的研究流程
        
        Parameters:
        -----------
        research_topic : str
            研究主题
        test_mode : bool
            是否为测试模式
        test_size : int
            测试模式下处理的文献数量
        analyze_top : int
            深度分析的文献数量
        enable_planning : bool
            是否启用规划Agent
        """
        print("\n" + "="*70)
        print("🚀 开始TODO驱动的文献研究流程")
        print("="*70)
        
        if self.progress:
            self.progress.start_tracking()
        
        # STEP 0: 数据预处理（新增）
        print("\n【STEP 0/5】数据预处理")
        if self.progress:
            self.progress.add_task('preprocessing', {
                'title': '数据预处理',
                'goal': '处理原始WOS数据，生成标准格式',
                'priority': 'high'
            })
            self.progress.start_task('preprocessing')
        
        try:
            # 检查是否已有处理好的数据
            processed_data_path = 'data/literature_data_processed.csv'
            if Path(processed_data_path).exists():
                print("  📁 发现已处理的数据，直接加载...")
                df = pd.read_csv(processed_data_path)
                print(f"  ✅ 加载完成: {len(df)} 篇文献")
            else:
                print("  🔧 开始数据预处理...")
                preprocessing_result = self.preprocessing_agent.run(
                    input_source="auto",
                    output_dir="data",
                    output_filename="literature_data_processed.csv"
                )
                
                if not preprocessing_result["success"]:
                    raise Exception(f"数据预处理失败: {preprocessing_result['error']}")
                
                df = pd.read_csv(preprocessing_result["output_file"])
                print(f"  ✅ 预处理完成: {len(df)} 篇文献")
            
            if self.progress:
                self.progress.complete_task('preprocessing', f"{len(df)} 篇文献")
        
        except Exception as e:
            print(f"❌ 数据预处理失败: {e}")
            if self.progress:
                self.progress.fail_task('preprocessing', str(e))
            raise
        
        # STEP 1: 规划研究任务（可选）
        if enable_planning:
            print("\n【STEP 0/4】研究规划")
            if self.progress:
                self.progress.add_task('planning', {
                    'title': '研究规划',
                    'goal': '分解研究任务',
                    'priority': 'high'
                })
                self.progress.start_task('planning')
            
            try:
                tasks = self.planning_agent.plan_research_tasks(
                    research_topic=research_topic,
                    total_papers=0,  # 暂时未知
                    context=f"测试模式: {test_mode}, 样本: {test_size if test_mode else '全部'}"
                )
                
                if self.progress:
                    self.progress.complete_task('planning', f"{len(tasks)} 个任务")
            
            except Exception as e:
                print(f"⚠️  规划失败，使用默认流程: {e}")
                if self.progress:
                    self.progress.fail_task('planning', str(e))
        
        # 应用测试模式（如果启用）
        if test_mode:
            print(f"\n⚠️  测试模式：只处理前 {test_size} 篇")
            df = df.head(test_size)
        
        # STEP 2: 筛选文献
        print("\n【STEP 2/5】智能筛选文献")
        if self.progress:
            self.progress.add_task('screening', {
                'title': '智能筛选文献',
                'goal': '筛选包含SOC数据的相关文献',
                'priority': 'high'
            })
            self.progress.start_task('screening')
        
        try:
            df = self.screening_agent.run(df)
            
            # 保存筛选结果
            output_file = 'literature_screening_results.xlsx'
            df.to_excel(output_file, index=False)
            print(f"\n💾 筛选结果已保存: {output_file}")
            
            if self.progress:
                passed = (df['LLM_Decision'] == 'accept').sum()
                self.progress.complete_task(
                    'screening',
                    f"{passed}/{len(df)} 篇通过筛选"
                )
        
        except Exception as e:
            print(f"❌ 筛选失败: {e}")
            if self.progress:
                self.progress.fail_task('screening', str(e))
            raise
        
        # STEP 3: 分析文献
        print("\n【STEP 3/5】深度分析文献")
        if self.progress:
            self.progress.add_task('analysis', {
                'title': '深度分析文献',
                'goal': '提取关键数据并生成摘要',
                'priority': 'medium'
            })
            self.progress.start_task('analysis')
        
        try:
            df = self.analysis_agent.run(df, max_papers=analyze_top)
            
            # 保存分析结果
            analysis_file = 'literature_analysis_results.xlsx'
            df.to_excel(analysis_file, index=False)
            print(f"\n💾 分析结果已保存: {analysis_file}")
            
            if self.progress:
                analyzed = df['Summary'].notna().sum() if 'Summary' in df.columns else 0
                self.progress.complete_task(
                    'analysis',
                    f"{analyzed} 篇深度分析完成"
                )
        
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            if self.progress:
                self.progress.fail_task('analysis', str(e))
            raise
        
        # STEP 4: 生成报告
        print("\n【STEP 4/5】生成研究报告")
        if self.progress:
            self.progress.add_task('report', {
                'title': '生成研究报告',
                'goal': '整合所有分析结果生成综合报告',
                'priority': 'high'
            })
            self.progress.start_task('report')
        
        try:
            report = self.report_agent.generate_comprehensive_report(
                df,
                research_topic=research_topic,
                include_summaries=True
            )
            
            # 保存报告
            report_file = 'literature_research_report.md'
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"\n💾 研究报告已保存: {report_file}")
            
            if self.progress:
                self.progress.complete_task('report', report_file)
        
        except Exception as e:
            print(f"❌ 报告生成失败: {e}")
            if self.progress:
                self.progress.fail_task('report', str(e))
            raise
        
        # 打印最终统计
        print("\n" + "="*70)
        print("📊 研究完成统计")
        print("="*70)
        
        total = len(df)
        passed = (df['LLM_Decision'] == 'accept').sum() if 'LLM_Decision' in df.columns else 0
        analyzed = df['Summary'].notna().sum() if 'Summary' in df.columns else 0
        
        print(f"\n总文献数: {total}")
        print(f"通过筛选: {passed} ({passed/total*100:.1f}%)")
        print(f"深度分析: {analyzed}")
        print(f"\n生成文件:")
        print(f"  1. literature_screening_results.xlsx - 筛选结果")
        print(f"  2. literature_analysis_results.xlsx - 分析结果")
        print(f"  3. literature_research_report.md - 研究报告")
        
        if self.progress:
            self.progress.end_tracking()
            summary = self.progress.get_summary()
            print(f"\n流程统计:")
            print(f"  总任务数: {summary['total_tasks']}")
            print(f"  已完成: {summary['completed']}")
            print(f"  失败: {summary['failed']}")
            print(f"  总耗时: {summary['duration']:.1f} 秒")
        
        print("\n" + "="*70)
        print("✅ 研究流程全部完成！")
        print("="*70)
        
        return df, report


def main():
    """主函数"""
    import sys
    
    # 创建系统
    system = LiteratureResearchSystem(enable_progress_tracking=True)
    
    # 询问模式
    print("请选择运行模式：")
    print("1. 测试模式（10篇文献，启用规划）")
    print("2. 小批量模式（50篇文献）")
    print("3. 完整模式（所有文献）")
    
    choice = input("\n请输入选择 (1-3, 默认1): ").strip() or "1"
    
    if choice == "1":
        test_mode = True
        test_size = 10
        enable_planning = True
    elif choice == "2":
        test_mode = True
        test_size = 50
        enable_planning = False
    elif choice == "3":
        test_mode = False
        test_size = 0
        enable_planning = False
    else:
        print("❌ 无效选择，使用测试模式")
        test_mode = True
        test_size = 10
        enable_planning = True
    
    # 运行研究
    try:
        df, report = system.run_research(
            research_topic="土壤有机碳饱和机制",
            test_mode=test_mode,
            test_size=test_size,
            analyze_top=20,
            enable_planning=enable_planning
        )
        
        # 显示部分报告
        print("\n" + "="*70)
        print("📄 报告预览")
        print("="*70)
        preview_len = min(600, len(report))
        print(report[:preview_len])
        if len(report) > preview_len:
            print("...\n（完整报告请查看生成的Markdown文件）")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
