#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究规划Agent - 参考TODO驱动范式
"""

import json
import re
from typing import List, Dict
from datetime import datetime
from core.agent import Agent


class ResearchPlanningAgent(Agent):
    """研究规划智能体 - 负责将研究需求分解为具体任务"""
    
    def __init__(self, llm, **kwargs):
        super().__init__(
            name="研究规划Agent",
            llm=llm,
            **kwargs
        )
    
    def _default_system_prompt(self) -> str:
        return """你是一个专业的土壤科学研究规划专家。
你的任务是将复杂的文献研究需求分解为清晰的子任务（TODO列表）。
每个子任务应该有明确的目标、可执行的步骤和预期产出。"""
    
    def plan_research_tasks(
        self,
        research_topic: str,
        total_papers: int,
        context: str = ""
    ) -> List[Dict]:
        """
        规划研究任务
        
        Parameters:
        -----------
        research_topic : str
            研究主题（如"土壤有机碳饱和机制"）
        total_papers : int
            文献总数
        context : str
            额外上下文信息
            
        Returns:
        --------
        List[Dict] : 任务列表
        """
        print(f"\n{'='*70}")
        print(f"📋 {self.name} 开始工作")
        print(f"{'='*70}\n")
        
        prompt = self._build_planning_prompt(research_topic, total_papers, context)
        
        try:
            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500,
                json_mode=True
            )
            
            tasks = self._extract_tasks(response)
            
            print(f"✅ 规划完成，生成 {len(tasks)} 个研究任务\n")
            
            for idx, task in enumerate(tasks, 1):
                print(f"{idx}. {task['title']}")
                print(f"   目标: {task['goal']}")
                print(f"   预期产出: {task['output']}\n")
            
            return tasks
            
        except Exception as e:
            print(f"❌ 规划失败: {e}")
            # 返回默认任务列表
            return self._get_default_tasks()
    
    def _build_planning_prompt(
        self,
        research_topic: str,
        total_papers: int,
        context: str
    ) -> str:
        """构建规划提示词"""
        current_date = datetime.now().strftime("%Y年%m月%d日")
        
        prompt = f"""你是一个研究规划专家。请为以下文献研究项目制定执行计划。

**研究主题：** {research_topic}
**文献总数：** {total_papers} 篇
**当前日期：** {current_date}
{f"**额外信息：** {context}" if context else ""}

**任务：** 将研究流程分解为4-6个清晰的子任务（TODO）。

每个任务应包含：
- title: 任务名称（简洁明了）
- goal: 任务目标（要达成什么）
- steps: 执行步骤（具体怎么做）
- output: 预期产出（生成什么结果）
- priority: 优先级（high/medium/low）

**示例输出格式：**
```json
{{
  "tasks": [
    {{
      "title": "文献数据加载与预处理",
      "goal": "加载所有文献数据并进行初步清洗",
      "steps": [
        "读取Excel文件",
        "合并多个数据源",
        "检查数据完整性"
      ],
      "output": "包含{total_papers}篇文献的清洗后DataFrame",
      "priority": "high"
    }},
    {{
      "title": "智能筛选相关文献",
      "goal": "使用LLM筛选出包含SOC数据的文献",
      "steps": [
        "调用ScreeningAgent",
        "判断SOC数据相关性",
        "保存筛选结果"
      ],
      "output": "筛选后的文献列表和判断理由",
      "priority": "high"
    }}
  ]
}}
```

**重要要求：**
1. 任务数量：4-6个
2. 任务之间应有逻辑顺序
3. 每个任务的目标和产出要明确
4. 返回纯JSON，不要额外文字

请生成研究计划：
"""
        return prompt
    
    def _extract_tasks(self, response: str) -> List[Dict]:
        """从响应中提取任务列表"""
        try:
            # 尝试提取JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                if 'tasks' in data:
                    return data['tasks']
                return [data]  # 单个任务
            
            # 直接解析
            data = json.loads(response)
            if 'tasks' in data:
                return data['tasks']
            return [data]
            
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON解析失败: {e}")
            print(f"响应内容: {response[:200]}...")
            return self._get_default_tasks()
    
    def _get_default_tasks(self) -> List[Dict]:
        """获取默认任务列表"""
        return [
            {
                "title": "文献数据加载",
                "goal": "加载并合并所有文献数据",
                "steps": ["读取Excel文件", "合并数据", "验证完整性"],
                "output": "完整的文献DataFrame",
                "priority": "high"
            },
            {
                "title": "智能筛选文献",
                "goal": "筛选包含SOC数据的相关文献",
                "steps": ["调用ScreeningAgent", "判断相关性", "保存结果"],
                "output": "筛选后的文献列表",
                "priority": "high"
            },
            {
                "title": "深度数据提取",
                "goal": "从通过筛选的文献中提取关键数据",
                "steps": ["调用AnalysisAgent", "提取SOC数据", "生成摘要"],
                "output": "结构化的数据和摘要",
                "priority": "medium"
            },
            {
                "title": "生成研究报告",
                "goal": "整合所有分析结果生成综合报告",
                "steps": ["整合数据", "生成Markdown报告", "保存文件"],
                "output": "完整的研究报告文档",
                "priority": "high"
            }
        ]
    
    def run(self, research_topic: str, total_papers: int = 0, **kwargs):
        """实现基类的run方法"""
        return self.plan_research_tasks(research_topic, total_papers, kwargs.get('context', ''))
