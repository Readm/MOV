import threading
import queue
import time
import pygame
from typing import Optional
import json
import os
import sys
from datetime import datetime

class WebSpeechRecognition:
    """基于Web Speech API的语音识别模块"""
    
    def __init__(self):
        self.command_queue = queue.Queue()
        self.is_listening = False
        self.listen_thread = None
        
        # 键盘测试映射
        self.test_commands = {
            pygame.K_1: "fireball",
            pygame.K_2: "freeze", 
            pygame.K_3: "heal",
            pygame.K_4: "start",
            pygame.K_5: "menu"
        }
        
        print("Web语音识别模块初始化完成 (使用键盘模拟模式)")
    
    def start_listening(self):
        """开始语音识别"""
        print("Web语音识别不可用，请使用键盘模式 (1-5键)")
    
    def stop_listening(self):
        """停止语音识别"""
        self.is_listening = False
    
    def handle_key_test(self, key):
        """处理键盘测试输入"""
        if key in self.test_commands:
            command = self.test_commands[key]
            print(f"模拟语音命令: {command}")
            self.command_queue.put(command)
    
    def get_command(self) -> Optional[str]:
        """获取识别到的命令"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None
    
    def stop(self):
        """停止语音识别"""
        self.stop_listening()

class SimpleSpeechRecognition:
    """简化的语音识别模块，使用Google Speech-to-Text API"""
    
    def __init__(self):
        self.command_queue = queue.Queue()
        self.is_listening = False
        self.listen_thread = None
        
        # 键盘测试映射
        self.test_commands = {
            pygame.K_1: "fireball",
            pygame.K_2: "freeze", 
            pygame.K_3: "heal",
            pygame.K_4: "start",
            pygame.K_5: "menu"
        }
        
        # 预定义的语音命令关键词
        self.command_keywords = {
            'fire': ['fire', 'fireball', 'flame', 'burn', 'blaze', 'ignite', 'inferno', 
                    '火球', '火焰', '燃烧', 'fuego', 'feu', 'フィア', 'ファイア'],
            'ice': ['ice', 'freeze', 'cold', 'frost', 'chill', 'frozen', 'blizzard',
                   '冰冻', '冰', '寒冰', '霜冻', 'hielo', 'glace', 'アイス', 'フリーズ'],
            'heal': ['heal', 'cure', 'health', 'restore', 'recovery', 'mend', 'fix',
                    '治愈', '治疗', '恢复', '修复', 'sanar', 'guérir', 'ヒール', 'キュア'],
            'lightning': ['lightning', 'thunder', 'bolt', 'shock', 'electric', 'zap',
                         '闪电', '雷电', '电击', 'rayo', 'foudre', 'サンダー', 'ライトニング'],
            'shield': ['shield', 'protect', 'guard', 'defend', 'barrier', 'block',
                      '盾牌', '防护', '保护', 'escudo', 'bouclier', 'シールド', 'ガード'],
            'start': ['start', 'begin', 'play', 'go', 'new', 'game',
                     '开始', '开启', '游戏', 'empezar', 'commencer', 'スタート', '始める'],
            'menu': ['menu', 'back', 'return', 'home', 'main', 'exit',
                    '菜单', '返回', '主菜单', '退出', 'menú', 'メニュー', '戻る'],
            'quit': ['quit', 'exit', 'bye', 'close', 'end', 'stop',
                    '退出', '结束', '关闭', '停止', 'salir', 'quitter', '終了', 'やめる']
        }
        
        print("简化语音识别模块初始化完成")
    
    def _recognize_from_text(self, text: str) -> Optional[str]:
        """从文本中识别命令"""
        text_lower = text.lower()
        
        for command, keywords in self.command_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return command
        
        return None
    
    def simulate_voice_input(self, text: str):
        """模拟语音输入（用于测试）"""
        command = self._recognize_from_text(text)
        if command:
            print(f"识别到语音命令: {text} -> {command}")
            self.command_queue.put(command)
        else:
            print(f"未识别的语音: {text}")
    
    def start_listening(self):
        """开始语音识别"""
        print("语音识别已激活，可以说话了...")
        print("提示：说 'fire'、'ice'、'heal'、'start'、'menu' 等命令")
        print("或使用键盘模拟 (1-5键)")
    
    def stop_listening(self):
        """停止语音识别"""
        self.is_listening = False
        print("停止语音识别")
    
    def handle_key_test(self, key):
        """处理键盘测试输入"""
        if key in self.test_commands:
            command = self.test_commands[key]
            print(f"键盘模拟语音命令: {command}")
            self.command_queue.put(command)
    
    def handle_text_input(self, text: str):
        """处理文本输入（模拟语音）"""
        command = self._recognize_from_text(text)
        if command:
            print(f"文本识别命令: {text} -> {command}")
            self.command_queue.put(command)
    
    def get_command(self) -> Optional[str]:
        """获取识别到的命令"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None
    
    def stop(self):
        """停止语音识别"""
        self.stop_listening()

# 根据可用性选择语音识别实现
def create_voice_recognition():
    """创建语音识别实例"""
    try:
        # 尝试使用简化的语音识别
        return SimpleSpeechRecognition()
    except Exception as e:
        print(f"语音识别初始化失败: {e}")
        # 降级到键盘模拟
        return WebSpeechRecognition()