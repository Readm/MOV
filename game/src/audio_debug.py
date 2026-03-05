#!/usr/bin/env python3
"""
音频系统调试工具
"""
import os
import sys
import subprocess
import platform
from datetime import datetime

class AudioDebugger:
    """音频系统调试器"""
    
    def __init__(self):
        self.debug_info = []
        self.audio_devices = []
        
    def log(self, message: str, level: str = "INFO"):
        """记录调试信息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.debug_info.append(log_entry)
        print(log_entry)
    
    def check_system_info(self):
        """检查系统信息"""
        self.log("=== 系统信息检查 ===")
        self.log(f"操作系统: {platform.system()} {platform.release()}")
        self.log(f"Python版本: {sys.version}")
        self.log(f"当前用户: {os.getenv('USER', 'unknown')}")
        
        # 检查是否在WSL环境中
        if os.path.exists('/proc/version'):
            try:
                with open('/proc/version', 'r') as f:
                    version_info = f.read()
                    if 'Microsoft' in version_info or 'WSL' in version_info:
                        self.log("检测到WSL环境", "WARNING")
                        self.log(f"WSL版本信息: {version_info.strip()}")
            except Exception as e:
                self.log(f"读取/proc/version失败: {e}", "ERROR")
    
    def check_audio_packages(self):
        """检查音频相关包的安装状态"""
        self.log("=== 音频包检查 ===")
        
        packages_to_check = [
            'alsa-utils',
            'pulseaudio', 
            'portaudio19-dev',
            'python3-pyaudio',
            'libasound2-dev'
        ]
        
        for package in packages_to_check:
            try:
                result = subprocess.run(['dpkg', '-l', package], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.log(f"✅ {package}: 已安装")
                else:
                    self.log(f"❌ {package}: 未安装", "WARNING")
            except Exception as e:
                self.log(f"⚠️  {package}: 检查失败 - {e}", "ERROR")
    
    def check_audio_devices(self):
        """检查音频设备"""
        self.log("=== 音频设备检查 ===")
        
        # 检查ALSA设备
        try:
            result = subprocess.run(['aplay', '-l'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log("ALSA播放设备:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.log(f"  {line}")
            else:
                self.log("未找到ALSA播放设备", "WARNING")
                self.log(f"aplay错误: {result.stderr}", "ERROR")
        except Exception as e:
            self.log(f"检查ALSA播放设备失败: {e}", "ERROR")
        
        # 检查录音设备
        try:
            result = subprocess.run(['arecord', '-l'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log("ALSA录音设备:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.log(f"  {line}")
            else:
                self.log("未找到ALSA录音设备", "WARNING") 
                self.log(f"arecord错误: {result.stderr}", "ERROR")
        except Exception as e:
            self.log(f"检查ALSA录音设备失败: {e}", "ERROR")
    
    def check_pulseaudio(self):
        """检查PulseAudio状态"""
        self.log("=== PulseAudio检查 ===")
        
        try:
            result = subprocess.run(['pulseaudio', '--check'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log("✅ PulseAudio正在运行")
            else:
                self.log("❌ PulseAudio未运行", "WARNING")
        except Exception as e:
            self.log(f"检查PulseAudio状态失败: {e}", "ERROR")
        
        # 检查PulseAudio设备
        try:
            result = subprocess.run(['pactl', 'list', 'sources', 'short'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log("PulseAudio输入设备:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.log(f"  {line}")
            else:
                self.log("未找到PulseAudio输入设备", "WARNING")
        except Exception as e:
            self.log(f"检查PulseAudio输入设备失败: {e}", "ERROR")
    
    def check_permissions(self):
        """检查音频权限"""
        self.log("=== 权限检查 ===")
        
        # 检查用户组
        try:
            result = subprocess.run(['groups'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                groups = result.stdout.strip()
                self.log(f"用户组: {groups}")
                
                audio_groups = ['audio', 'pulse-access']
                for group in audio_groups:
                    if group in groups:
                        self.log(f"✅ 用户在 {group} 组中")
                    else:
                        self.log(f"❌ 用户不在 {group} 组中", "WARNING")
        except Exception as e:
            self.log(f"检查用户组失败: {e}", "ERROR")
        
        # 检查设备文件权限
        audio_devices = ['/dev/snd/', '/dev/dsp', '/dev/audio']
        for device in audio_devices:
            if os.path.exists(device):
                try:
                    stat_info = os.stat(device)
                    self.log(f"✅ {device} 存在，权限: {oct(stat_info.st_mode)}")
                except Exception as e:
                    self.log(f"检查 {device} 权限失败: {e}", "ERROR")
            else:
                self.log(f"❌ {device} 不存在", "WARNING")
    
    def test_python_audio(self):
        """测试Python音频库"""
        self.log("=== Python音频库测试 ===")
        
        # 测试PyAudio
        try:
            import pyaudio
            self.log("✅ PyAudio导入成功")
            
            # 尝试初始化PyAudio
            try:
                pa = pyaudio.PyAudio()
                device_count = pa.get_device_count()
                self.log(f"PyAudio找到 {device_count} 个设备")
                
                for i in range(device_count):
                    try:
                        device_info = pa.get_device_info_by_index(i)
                        device_name = device_info.get('name', 'Unknown')
                        max_input_channels = device_info.get('maxInputChannels', 0)
                        if max_input_channels > 0:
                            self.log(f"  输入设备 {i}: {device_name} ({max_input_channels} 通道)")
                    except Exception as e:
                        self.log(f"  设备 {i}: 获取信息失败 - {e}", "ERROR")
                
                pa.terminate()
            except Exception as e:
                self.log(f"PyAudio初始化失败: {e}", "ERROR")
                
        except ImportError:
            self.log("❌ PyAudio未安装", "WARNING")
        except Exception as e:
            self.log(f"PyAudio测试失败: {e}", "ERROR")
        
        # 测试SpeechRecognition
        try:
            import speech_recognition as sr
            self.log("✅ SpeechRecognition导入成功")
            
            try:
                r = sr.Recognizer()
                mic_list = sr.Microphone.list_microphone_names()
                self.log(f"SpeechRecognition找到 {len(mic_list)} 个麦克风:")
                for i, mic_name in enumerate(mic_list):
                    self.log(f"  麦克风 {i}: {mic_name}")
            except Exception as e:
                self.log(f"SpeechRecognition设备枚举失败: {e}", "ERROR")
                
        except ImportError:
            self.log("❌ SpeechRecognition未安装", "WARNING")
        except Exception as e:
            self.log(f"SpeechRecognition测试失败: {e}", "ERROR")
    
    def test_audio_recording(self):
        """测试音频录制"""
        self.log("=== 音频录制测试 ===")
        
        try:
            # 尝试使用arecord进行简单录制测试
            self.log("测试arecord录制...")
            result = subprocess.run([
                'arecord', '-d', '1', '-f', 'cd', '/dev/null'
            ], capture_output=True, text=True, timeout=3)
            
            if result.returncode == 0:
                self.log("✅ arecord录制测试成功")
            else:
                self.log(f"❌ arecord录制测试失败: {result.stderr}", "ERROR")
                
        except subprocess.TimeoutExpired:
            self.log("arecord录制测试超时", "WARNING")
        except Exception as e:
            self.log(f"arecord录制测试失败: {e}", "ERROR")
    
    def generate_debug_report(self):
        """生成完整的调试报告"""
        self.log("开始音频系统调试...")
        
        self.check_system_info()
        self.check_audio_packages()
        self.check_audio_devices()
        self.check_pulseaudio()
        self.check_permissions()
        self.test_python_audio()
        self.test_audio_recording()
        
        self.log("=== 调试完成 ===")
        
        # 生成建议
        self.log("=== 问题排查建议 ===")
        if any("WSL" in info for info in self.debug_info):
            self.log("🔧 WSL环境建议:")
            self.log("   - WSL2通常没有音频支持")
            self.log("   - 考虑使用Windows宿主机的音频API")
            self.log("   - 或使用基于文本的语音模拟模式")
        
        if any("未安装" in info for info in self.debug_info):
            self.log("🔧 缺少音频包，建议安装:")
            self.log("   sudo apt update")
            self.log("   sudo apt install alsa-utils pulseaudio portaudio19-dev")
        
        if any("权限" in info and "❌" in info for info in self.debug_info):
            self.log("🔧 权限问题建议:")
            self.log("   sudo usermod -a -G audio $USER")
            self.log("   需要重新登录后生效")
        
        return self.debug_info

def main():
    """主函数"""
    debugger = AudioDebugger()
    debug_info = debugger.generate_debug_report()
    
    # 保存调试报告到文件
    report_file = "/home/readm/MOV/game/audio_debug_report.txt"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Magic Of Voice - 音频调试报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"生成时间: {datetime.now()}\n\n")
            for info in debug_info:
                f.write(info + "\n")
        
        print(f"\n📝 调试报告已保存到: {report_file}")
    except Exception as e:
        print(f"保存调试报告失败: {e}")

if __name__ == "__main__":
    main()