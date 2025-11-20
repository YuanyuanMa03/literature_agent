#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent基类
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from .message import Message
from .llm import LiteratureLLM


class Agent(ABC):
    """Agent抽象基类"""
    
    def __init__(
        self,
        name: str,
        llm: LiteratureLLM,
        system_prompt: Optional[str] = None
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt or self._default_system_prompt()
        self._history: list[Message] = []
        
        print(f"✅ {name} 初始化完成")
    
    @abstractmethod
    def _default_system_prompt(self) -> str:
        """默认系统提示词"""
        pass
    
    @abstractmethod
    def run(self, input_data: Any, **kwargs) -> Any:
        """运行Agent"""
        pass
    
    def add_message(self, message: Message):
        """添加消息到历史"""
        self._history.append(message)
    
    def clear_history(self):
        """清空历史"""
        self._history.clear()
    
    def get_history(self) -> list[Message]:
        """获取历史"""
        return self._history.copy()
    
    def _prepare_messages(self, user_input: str) -> list[Dict[str, str]]:
        """准备消息列表"""
        messages = []
        
        # 添加系统提示
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        
        # 添加历史消息
        for msg in self._history[-10:]:  # 只保留最近10条
            messages.append(msg.to_dict())
        
        # 添加当前用户输入
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        return messages
    
    def __str__(self) -> str:
        return f"Agent(name={self.name}, model={self.llm.model})"
