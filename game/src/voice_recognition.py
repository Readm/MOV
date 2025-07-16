import threading
import queue
import time
import pygame
from typing import Optional

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("语音识别库未安装，使用键盘模拟模式")

class VoiceRecognition:
    """语音识别模块"""
    
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
        
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                # 调整识别器设置
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                print("语音识别初始化完成")
            except Exception as e:
                print(f"语音识别初始化失败: {e}")
                print("使用键盘模拟模式 (1-5键)")
        else:
            print("使用键盘模拟语音模式 (1-5键对应咒语)")
    
    def start_listening(self):
        """开始监听语音"""
        if SPEECH_RECOGNITION_AVAILABLE and hasattr(self, 'recognizer'):
            if not self.is_listening:
                self.is_listening = True
                self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
                self.listen_thread.start()
                print("开始语音识别...")
        else:
            print("语音识别不可用，请使用键盘模式 (1-5键)")
    
    def stop_listening(self):
        """停止监听语音"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=1.0)
        print("停止语音识别")
    
    def _listen_loop(self):
        """语音监听循环"""
        if not SPEECH_RECOGNITION_AVAILABLE or not hasattr(self, 'recognizer'):
            return
            
        while self.is_listening:
            try:
                with self.microphone as source:
                    # 监听音频，超时设置
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                try:
                    # 使用Google Web Speech API识别
                    command = self.recognizer.recognize_google(audio, language='zh-CN')
                    print(f"识别到语音: {command}")
                    self.command_queue.put(command)
                    
                except sr.UnknownValueError:
                    # 无法识别语音
                    pass
                except sr.RequestError as e:
                    print(f"语音识别服务错误: {e}")
                    
            except sr.WaitTimeoutError:
                # 超时，继续监听
                pass
            except Exception as e:
                print(f"语音识别错误: {e}")
                time.sleep(0.1)
    
    def get_command(self) -> Optional[str]:
        """获取识别到的命令"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None
    
    def handle_key_test(self, key):
        """处理键盘测试输入"""
        if key in self.test_commands:
            command = self.test_commands[key]
            print(f"模拟语音命令: {command}")
            self.command_queue.put(command)
    
    def stop(self):
        """停止语音识别"""
        self.stop_listening()

