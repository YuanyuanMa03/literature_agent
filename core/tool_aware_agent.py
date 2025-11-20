#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToolAwareAgent - 支持工具调用监听的Agent
"""

from typing import Optional, Callable, Dict, Any
from .agent import Agent


class ToolAwareAgent(Agent):
    """
    工具感知Agent - 可以监听和记录工具调用
    
    增加工具调用的可观测性
    """
    
    def __init__(
        self,
        name: str,
        llm,
        system_prompt: Optional[str] = None,
        tool_call_listener: Optional[Callable] = None
    ):
        """
        初始化ToolAwareAgent
        
        Parameters:
        -----------
        name : str
            Agent名称
        llm : LiteratureLLM
            LLM实例
        system_prompt : str, optional
            系统提示词
        tool_call_listener : Callable, optional
            工具调用监听器，签名为 func(call_info: Dict)
        """
        super().__init__(name, llm, system_prompt)
        self._tool_call_listener = tool_call_listener
        self._tool_call_count = 0
    
    def _notify_tool_call(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        result: Any,
        success: bool = True,
        error: Optional[str] = None
    ):
        """
        通知工具调用监听器
        
        Parameters:
        -----------
        tool_name : str
            工具名称
        parameters : Dict
            工具参数
        result : Any
            执行结果
        success : bool
            是否成功
        error : str, optional
            错误信息
        """
        if self._tool_call_listener is None:
            return
        
        self._tool_call_count += 1
        
        call_info = {
            'agent_name': self.name,
            'tool_name': tool_name,
            'parameters': parameters,
            'result': result,
            'success': success,
            'error': error,
            'call_number': self._tool_call_count
        }
        
        try:
            self._tool_call_listener(call_info)
        except Exception as e:
            print(f"⚠️  工具调用监听器错误: {e}")
    
    def get_tool_call_count(self) -> int:
        """获取工具调用次数"""
        return self._tool_call_count
    
    def reset_tool_call_count(self):
        """重置工具调用计数"""
        self._tool_call_count = 0
