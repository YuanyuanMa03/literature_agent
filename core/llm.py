#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义LLM客户端 - OpenAI兼容格式
"""

import os
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LiteratureLLM:
    """文献分析专用LLM客户端 - OpenAI兼容格式"""
    
    def __init__(
        self,
        model: str = "gemini-2.5-pro",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2000,
        timeout: int = 60
    ):
        """
        初始化LLM客户端
        
        Parameters:
        -----------
        model : str
            模型名称（如gemini-2.5-pro）
        api_key : str
            API密钥
        base_url : str
            API地址
        temperature : float
            温度参数（0-1）
        max_tokens : int
            最大生成token数
        timeout : int
            超时时间（秒）
        """
        self.model = model
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = (base_url or os.getenv('OPENAI_API_BASE')).rstrip('/') if (base_url or os.getenv('OPENAI_API_BASE')) else None
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError("需要提供API密钥")
        
        # 使用OpenAI客户端（兼容格式）
        if self.base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)
            print(f"✅ LLM初始化: {self.base_url}")
        else:
            self.client = OpenAI(api_key=self.api_key, timeout=self.timeout)
            print(f"✅ LLM初始化: OpenAI官方API")
        
        print(f"   模型: {self.model}")
    
    def chat(
        self,
        messages: list[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
        max_retries: int = 3
    ) -> str:
        """
        发送对话请求（带重试机制）- OpenAI兼容格式
        
        Parameters:
        -----------
        messages : list
            消息列表，格式：[{"role": "system/user/assistant", "content": "..."}]
        temperature : float
            本次请求的温度
        max_tokens : int
            本次请求的最大token数
        json_mode : bool
            是否要求返回JSON格式
        max_retries : int
            最大重试次数
            
        Returns:
        --------
        str : LLM的响应内容
        """
        import time
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 使用OpenAI标准格式调用
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature or self.temperature,
                    max_tokens=max_tokens or self.max_tokens,
                )
                
                content = response.choices[0].message.content
                if content is None:
                    content = ""
                
                # 如果要求JSON格式，尝试提取
                if json_mode:
                    content = self._extract_json(content)
                
                return content
                    
            except Exception as e:
                last_error = Exception(f"LLM调用失败: {e}")
                print(f"⚠️  尝试 {attempt+1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
        
        raise last_error or Exception("所有重试均失败")
    
    def _extract_json(self, text: str) -> str:
        """从响应中提取JSON"""
        import re
        
        # 尝试直接解析
        try:
            json.loads(text)
            return text
        except:
            pass
        
        # 提取```json```代码块
        json_match = re.search(r'```json\s*({.*?})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # 提取花括号内容
        json_match = re.search(r'({.*})', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        return text
    
    def __str__(self):
        return f"LiteratureLLM(model={self.model}, base={self.base_url})"
