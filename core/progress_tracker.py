#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度追踪器 - 参考第十四章SSE进度推送设计
"""

from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ProgressTracker:
    """
    进度追踪器
    
    用于追踪和记录研究流程的进度
    """
    
    def __init__(self, event_listener: Optional[Callable] = None):
        """
        初始化进度追踪器
        
        Parameters:
        -----------
        event_listener : Callable, optional
            事件监听器，签名为 func(event: Dict)
        """
        self._event_listener = event_listener or self._default_listener
        self._events: List[Dict] = []
        self._tasks: Dict[str, Dict] = {}
        self._start_time = None
        self._end_time = None
    
    def start_tracking(self):
        """开始追踪"""
        self._start_time = datetime.now()
        self._emit_event({
            'type': 'tracking_started',
            'timestamp': self._start_time.isoformat(),
            'message': '开始研究流程追踪'
        })
    
    def end_tracking(self):
        """结束追踪"""
        self._end_time = datetime.now()
        duration = (self._end_time - self._start_time).total_seconds()
        
        self._emit_event({
            'type': 'tracking_ended',
            'timestamp': self._end_time.isoformat(),
            'duration': duration,
            'message': f'研究流程完成，耗时 {duration:.1f} 秒'
        })
    
    def add_task(self, task_id: str, task_info: Dict):
        """
        添加任务
        
        Parameters:
        -----------
        task_id : str
            任务ID
        task_info : Dict
            任务信息（title, goal, priority等）
        """
        self._tasks[task_id] = {
            **task_info,
            'status': TaskStatus.PENDING,
            'start_time': None,
            'end_time': None,
            'progress': 0
        }
        
        self._emit_event({
            'type': 'task_added',
            'task_id': task_id,
            'task': self._tasks[task_id]
        })
    
    def start_task(self, task_id: str):
        """开始任务"""
        if task_id not in self._tasks:
            return
        
        self._tasks[task_id]['status'] = TaskStatus.IN_PROGRESS
        self._tasks[task_id]['start_time'] = datetime.now()
        
        self._emit_event({
            'type': 'task_started',
            'task_id': task_id,
            'message': f"开始任务: {self._tasks[task_id].get('title', task_id)}"
        })
    
    def update_task_progress(self, task_id: str, progress: int, message: str = ""):
        """
        更新任务进度
        
        Parameters:
        -----------
        task_id : str
            任务ID
        progress : int
            进度百分比 (0-100)
        message : str
            进度消息
        """
        if task_id not in self._tasks:
            return
        
        self._tasks[task_id]['progress'] = progress
        
        self._emit_event({
            'type': 'task_progress',
            'task_id': task_id,
            'progress': progress,
            'message': message
        })
    
    def complete_task(self, task_id: str, result: Any = None):
        """完成任务"""
        if task_id not in self._tasks:
            return
        
        self._tasks[task_id]['status'] = TaskStatus.COMPLETED
        self._tasks[task_id]['end_time'] = datetime.now()
        self._tasks[task_id]['progress'] = 100
        
        if result is not None:
            self._tasks[task_id]['result'] = result
        
        duration = (
            self._tasks[task_id]['end_time'] - 
            self._tasks[task_id]['start_time']
        ).total_seconds()
        
        self._emit_event({
            'type': 'task_completed',
            'task_id': task_id,
            'duration': duration,
            'message': f"任务完成: {self._tasks[task_id].get('title', task_id)} ({duration:.1f}秒)"
        })
    
    def fail_task(self, task_id: str, error: str):
        """任务失败"""
        if task_id not in self._tasks:
            return
        
        self._tasks[task_id]['status'] = TaskStatus.FAILED
        self._tasks[task_id]['end_time'] = datetime.now()
        self._tasks[task_id]['error'] = error
        
        self._emit_event({
            'type': 'task_failed',
            'task_id': task_id,
            'error': error,
            'message': f"任务失败: {self._tasks[task_id].get('title', task_id)}"
        })
    
    def log_status(self, message: str, level: str = "info"):
        """
        记录状态日志
        
        Parameters:
        -----------
        message : str
            日志消息
        level : str
            日志级别 (info, warning, error)
        """
        self._emit_event({
            'type': 'status',
            'level': level,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_tool_call(self, call_info: Dict):
        """记录工具调用"""
        self._emit_event({
            'type': 'tool_call',
            **call_info,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_summary(self) -> Dict:
        """获取追踪摘要"""
        if not self._start_time:
            return {'status': 'not_started'}
        
        duration = (
            (self._end_time or datetime.now()) - self._start_time
        ).total_seconds()
        
        completed = sum(
            1 for t in self._tasks.values() 
            if t['status'] == TaskStatus.COMPLETED
        )
        failed = sum(
            1 for t in self._tasks.values() 
            if t['status'] == TaskStatus.FAILED
        )
        total = len(self._tasks)
        
        return {
            'total_tasks': total,
            'completed': completed,
            'failed': failed,
            'in_progress': total - completed - failed,
            'duration': duration,
            'total_events': len(self._events)
        }
    
    def _emit_event(self, event: Dict):
        """发送事件"""
        event['timestamp'] = event.get('timestamp', datetime.now().isoformat())
        self._events.append(event)
        self._event_listener(event)
    
    def _default_listener(self, event: Dict):
        """默认事件监听器（打印到控制台）"""
        event_type = event.get('type', 'unknown')
        message = event.get('message', '')
        
        if event_type == 'status':
            level = event.get('level', 'info')
            if level == 'error':
                print(f"❌ {message}")
            elif level == 'warning':
                print(f"⚠️  {message}")
            else:
                print(f"ℹ️  {message}")
        
        elif event_type in ['task_started', 'task_completed']:
            print(f"✓ {message}")
        
        elif event_type == 'task_failed':
            error = event.get('error', '')
            print(f"✗ {message}: {error}")
        
        elif event_type == 'task_progress':
            progress = event.get('progress', 0)
            print(f"  [{progress}%] {message}")
