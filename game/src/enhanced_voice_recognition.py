import threading
import queue
import time
import pygame
from typing import Optional
import json
import os
import sys
from datetime import datetime

# 尝试导入语音识别相关库并记录状态
AUDIO_DEBUG = True  # 全局debug开关

def debug_log(message: str, level: str = "INFO"):
    """调试日志函数"""
    if AUDIO_DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] AUDIO-{level}: {message}")

def check_audio_dependencies():
    """检查音频依赖"""
    debug_log("开始检查音频依赖...")
    
    dependencies = {
        'speech_recognition': False,
        'pyaudio': False,
        'pydub': False
    }
    
    # 检查SpeechRecognition
    try:
        import speech_recognition as sr
        dependencies['speech_recognition'] = True
        debug_log("✅ SpeechRecognition库可用")
        
        # 检查麦克风
        try:
            mic_list = sr.Microphone.list_microphone_names()
            debug_log(f"找到 {len(mic_list)} 个麦克风设备:")
            for i, mic in enumerate(mic_list):
                debug_log(f"  麦克风 {i}: {mic}")
        except Exception as e:
            debug_log(f"⚠️ 枚举麦克风设备失败: {e}", "WARNING")
            
    except ImportError as e:
        debug_log(f"❌ SpeechRecognition库不可用: {e}", "ERROR")
    except Exception as e:
        debug_log(f"❌ SpeechRecognition库测试失败: {e}", "ERROR")
    
    # 检查PyAudio
    try:
        import pyaudio
        dependencies['pyaudio'] = True
        debug_log("✅ PyAudio库可用")
        
        # 检查音频设备
        try:
            pa = pyaudio.PyAudio()
            device_count = pa.get_device_count()
            debug_log(f"PyAudio检测到 {device_count} 个音频设备")
            
            input_devices = []
            for i in range(device_count):
                try:
                    device_info = pa.get_device_info_by_index(i)
                    if device_info['maxInputChannels'] > 0:
                        input_devices.append({
                            'index': i,
                            'name': device_info['name'],
                            'channels': device_info['maxInputChannels'],
                            'sample_rate': device_info['defaultSampleRate']
                        })
                        debug_log(f"  输入设备 {i}: {device_info['name']} "
                                f"({device_info['maxInputChannels']} 通道, "
                                f"{device_info['defaultSampleRate']} Hz)")
                except Exception as e:
                    debug_log(f"  设备 {i}: 获取信息失败 - {e}", "WARNING")
            
            if not input_devices:
                debug_log("❌ 未找到可用的音频输入设备", "ERROR")
            
            pa.terminate()
            
        except Exception as e:
            debug_log(f"⚠️ PyAudio设备枚举失败: {e}", "WARNING")
            
    except ImportError as e:
        debug_log(f"❌ PyAudio库不可用: {e}", "ERROR")
    except Exception as e:
        debug_log(f"❌ PyAudio库测试失败: {e}", "ERROR")
    
    # 检查Pydub
    try:
        import pydub
        dependencies['pydub'] = True
        debug_log("✅ Pydub库可用")
    except ImportError as e:
        debug_log(f"❌ Pydub库不可用: {e}", "ERROR")
    
    debug_log(f"依赖检查完成: {dependencies}")
    return dependencies

class EnhancedVoiceRecognition:
    """增强的语音识别模块，带详细调试信息"""
    
    def __init__(self):
        debug_log("初始化增强语音识别模块...")
        
        self.command_queue = queue.Queue()
        self.is_listening = False
        self.listen_thread = None
        self.audio_available = False
        
        # 键盘测试映射
        self.test_commands = {
            pygame.K_1: "fire",
            pygame.K_2: "ice", 
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
        
        # 检查音频依赖
        self.dependencies = check_audio_dependencies()
        
        # 尝试初始化真实语音识别
        self._init_real_speech_recognition()
        
        if not self.audio_available:
            debug_log("回退到键盘模拟模式", "WARNING")
        
        debug_log("增强语音识别模块初始化完成")
    
    def _init_real_speech_recognition(self):
        """初始化真实语音识别"""
        if not self.dependencies.get('speech_recognition') or not self.dependencies.get('pyaudio'):
            debug_log("缺少必要依赖，无法启用真实语音识别", "WARNING")
            return
        
        try:
            import speech_recognition as sr
            import pyaudio
            
            debug_log("尝试初始化SpeechRecognition...")
            self.recognizer = sr.Recognizer()
            
            # 测试麦克风
            debug_log("测试默认麦克风...")
            try:
                self.microphone = sr.Microphone()
                debug_log("✅ 默认麦克风创建成功")
                
                # 测试环境噪音调整
                debug_log("调整环境噪音基线...")
                with self.microphone as source:
                    debug_log("正在分析环境噪音... (1秒)")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    debug_log(f"环境噪音基线设置完成，能量阈值: {self.recognizer.energy_threshold}")
                
                self.audio_available = True
                debug_log("✅ 真实语音识别初始化成功")
                
            except Exception as e:
                debug_log(f"❌ 麦克风初始化失败: {e}", "ERROR")
                debug_log(f"错误类型: {type(e).__name__}", "DEBUG")
                
        except Exception as e:
            debug_log(f"❌ 语音识别库初始化失败: {e}", "ERROR")
    
    def start_listening(self):
        """开始语音识别"""
        debug_log("收到开始语音识别请求")
        
        if self.audio_available and not self.is_listening:
            debug_log("启动真实语音识别线程...")
            self.is_listening = True
            self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listen_thread.start()
            debug_log("✅ 语音识别线程已启动")
        else:
            if not self.audio_available:
                debug_log("音频不可用，使用键盘模拟模式", "WARNING")
                debug_log("提示：请使用1-5键模拟语音命令")
            else:
                debug_log("语音识别已在运行中", "INFO")
    
    def _listen_loop(self):
        """语音监听循环"""
        debug_log("进入语音监听循环")
        
        if not hasattr(self, 'recognizer') or not hasattr(self, 'microphone'):
            debug_log("语音识别组件未正确初始化", "ERROR")
            return
        
        listen_count = 0
        while self.is_listening:
            try:
                listen_count += 1
                debug_log(f"开始第 {listen_count} 次监听...")
                
                with self.microphone as source:
                    debug_log("等待语音输入... (超时: 2秒)")
                    # 监听音频，设置合理的超时
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    debug_log(f"捕获到音频数据，长度: {len(audio.frame_data)} 字节")
                
                try:
                    debug_log("正在识别语音...")
                    # 使用Google Web Speech API识别
                    command = self.recognizer.recognize_google(audio, language='zh-CN')
                    debug_log(f"✅ 语音识别成功: '{command}'")
                    
                    # 处理识别结果
                    processed_command = self._recognize_from_text(command)
                    if processed_command:
                        debug_log(f"✅ 命令匹配成功: '{command}' -> {processed_command}")
                        self.command_queue.put(processed_command)
                    else:
                        debug_log(f"⚠️ 未找到匹配的命令: '{command}'", "WARNING")
                    
                except sr.UnknownValueError:
                    debug_log("⚠️ 无法识别语音内容", "WARNING")
                except sr.RequestError as e:
                    debug_log(f"❌ 语音识别服务错误: {e}", "ERROR")
                    # 服务错误时暂停一段时间再重试
                    time.sleep(1)
                    
            except sr.WaitTimeoutError:
                debug_log("语音监听超时，继续等待...")
            except Exception as e:
                debug_log(f"❌ 语音监听循环错误: {e}", "ERROR")
                debug_log(f"错误类型: {type(e).__name__}", "DEBUG")
                time.sleep(0.5)  # 错误后短暂等待
        
        debug_log("语音监听循环结束")
    
    def stop_listening(self):
        """停止语音识别"""
        debug_log("停止语音识别...")
        self.is_listening = False
        if self.listen_thread and self.listen_thread.is_alive():
            debug_log("等待语音识别线程结束...")
            self.listen_thread.join(timeout=2.0)
            if self.listen_thread.is_alive():
                debug_log("语音识别线程未正常结束", "WARNING")
            else:
                debug_log("✅ 语音识别线程已结束")
    
    def _recognize_from_text(self, text: str) -> Optional[str]:
        """从文本中识别命令"""
        text_lower = text.lower()
        debug_log(f"分析文本命令: '{text_lower}'")
        
        for command, keywords in self.command_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    debug_log(f"找到匹配关键词: '{keyword}' -> {command}")
                    return command
        
        debug_log("未找到匹配的关键词")
        return None
    
    def simulate_voice_input(self, text: str):
        """模拟语音输入（用于测试）"""
        debug_log(f"模拟语音输入: '{text}'")
        command = self._recognize_from_text(text)
        if command:
            debug_log(f"✅ 模拟识别成功: {text} -> {command}")
            self.command_queue.put(command)
        else:
            debug_log(f"⚠️ 模拟识别失败: {text}")
    
    def handle_key_test(self, key):
        """处理键盘测试输入"""
        if key in self.test_commands:
            command = self.test_commands[key]
            debug_log(f"键盘模拟语音命令: 按键{key} -> {command}")
            self.command_queue.put(command)
        else:
            debug_log(f"未知的测试按键: {key}", "WARNING")
    
    def handle_text_input(self, text: str):
        """处理文本输入（模拟语音）"""
        debug_log(f"文本输入模拟语音: '{text}'")
        command = self._recognize_from_text(text)
        if command:
            debug_log(f"✅ 文本识别成功: {text} -> {command}")
            self.command_queue.put(command)
    
    def get_command(self) -> Optional[str]:
        """获取识别到的命令"""
        try:
            command = self.command_queue.get_nowait()
            debug_log(f"取出命令: {command}")
            return command
        except queue.Empty:
            return None
    
    def get_status(self) -> dict:
        """获取语音识别状态"""
        return {
            'audio_available': self.audio_available,
            'is_listening': self.is_listening,
            'dependencies': self.dependencies,
            'queue_size': self.command_queue.qsize()
        }
    
    def stop(self):
        """停止语音识别"""
        debug_log("语音识别模块关闭")
        self.stop_listening()

# 创建语音识别实例的工厂函数
def create_voice_recognition():
    """创建语音识别实例"""
    debug_log("创建语音识别实例...")
    try:
        return EnhancedVoiceRecognition()
    except Exception as e:
        debug_log(f"创建语音识别实例失败: {e}", "ERROR")
        # 降级到简单模式
        from web_speech_recognition import SimpleSpeechRecognition
        debug_log("降级到简单语音识别模式", "WARNING")
        return SimpleSpeechRecognition()