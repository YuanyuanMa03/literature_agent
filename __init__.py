"""
文献分析Agent系统
基于硅基流动API的智能文献分析框架
"""

__version__ = "1.0.0"
__author__ = "YYMa"

from .core.llm import LiteratureLLM
from .core.agent import Agent
from .core.message import Message
from .agents.screening_agent import LiteratureScreeningAgent
from .agents.analysis_agent import LiteratureAnalysisAgent

__all__ = [
    "LiteratureLLM",
    "Agent",
    "Message",
    "LiteratureScreeningAgent",
    "LiteratureAnalysisAgent",
]
