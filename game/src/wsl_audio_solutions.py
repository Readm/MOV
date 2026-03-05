#!/usr/bin/env python3
"""
WSL2 音频解决方案检测和配置工具
"""
import subprocess
import os
import platform
from datetime import datetime

def log(message: str, level: str = "INFO"):
    """日志函数"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] WSL-AUDIO-{level}: {message}")

def check_wsl_version():
    """检查WSL版本"""
    log("检查WSL版本...")
    try:
        with open('/proc/version', 'r') as f:
            version_info = f.read()
            if 'Microsoft' in version_info:
                if 'WSL2' in version_info:
                    log("检测到WSL2环境")
                    return "WSL2"
                else:
                    log("检测到WSL1环境")
                    return "WSL1"
    except Exception as e:
        log(f"检查WSL版本失败: {e}", "ERROR")
    return "Unknown"

def check_pulseaudio_server():
    """检查Windows PulseAudio服务器"""
    log("检查Windows PulseAudio服务器连接...")
    
    # 检查PULSE_SERVER环境变量
    pulse_server = os.getenv('PULSE_SERVER')
    if pulse_server:
        log(f"发现PULSE_SERVER配置: {pulse_server}")
    else:
        log("未配置PULSE_SERVER环境变量", "WARNING")
    
    # 尝试连接PulseAudio
    try:
        result = subprocess.run(['pactl', 'info'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            log("✅ PulseAudio连接成功")
            log("PulseAudio服务器信息:")
            for line in result.stdout.split('\n')[:10]:  # 显示前10行
                if line.strip():
                    log(f"  {line}")
            return True
        else:
            log(f"❌ PulseAudio连接失败: {result.stderr}", "ERROR")
    except Exception as e:
        log(f"检查PulseAudio失败: {e}", "ERROR")
    
    return False

def setup_pulseaudio_wsl():
    """设置WSL2的PulseAudio配置"""
    log("配置WSL2 PulseAudio...")
    
    # 获取Windows主机IP
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    host_ip = line.split()[1]
                    log(f"Windows主机IP: {host_ip}")
                    break
    except Exception as e:
        log(f"获取主机IP失败: {e}", "ERROR")
        host_ip = "192.168.1.1"  # 默认值
    
    # 设置PULSE_SERVER环境变量
    pulse_server = f"tcp:{host_ip}:4713"
    log(f"建议设置PULSE_SERVER={pulse_server}")
    
    # 生成配置建议
    config_suggestions = f"""
# 将以下行添加到 ~/.bashrc 或 ~/.profile
export PULSE_SERVER={pulse_server}

# 或者创建 ~/.pulse/client.conf 文件：
mkdir -p ~/.pulse
echo "default-server = {pulse_server}" > ~/.pulse/client.conf
"""
    log("PulseAudio配置建议:")
    log(config_suggestions)
    
    return host_ip

def check_usb_ip_support():
    """检查USB/IP支持（用于USB麦克风）"""
    log("检查USB/IP支持...")
    
    try:
        result = subprocess.run(['usbip', 'version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            log("✅ USB/IP工具已安装")
            log(f"版本: {result.stdout.strip()}")
            return True
        else:
            log("❌ USB/IP工具未安装", "WARNING")
    except Exception as e:
        log("USB/IP工具未找到，可以安装: sudo apt install usbip", "INFO")
    
    return False

def test_audio_alternatives():
    """测试替代音频方案"""
    log("测试替代音频方案...")
    
    alternatives = [
        {
            'name': 'Windows Python调用',
            'description': '在Windows上运行Python脚本进行语音识别',
            'command': 'powershell.exe -c "python --version"'
        },
        {
            'name': 'Windows子进程',
            'description': '从WSL调用Windows的语音识别API',
            'command': 'cmd.exe /c "echo Windows accessible"'
        }
    ]
    
    for alt in alternatives:
        log(f"测试 {alt['name']}...")
        try:
            result = subprocess.run(alt['command'].split(), 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                log(f"✅ {alt['name']} 可用")
                log(f"  输出: {result.stdout.strip()}")
            else:
                log(f"❌ {alt['name']} 不可用")
        except Exception as e:
            log(f"测试 {alt['name']} 失败: {e}")

def generate_wsl_audio_guide():
    """生成WSL音频配置指南"""
    log("生成WSL2音频配置完整指南...")
    
    wsl_version = check_wsl_version()
    pulseaudio_ok = check_pulseaudio_server()
    host_ip = setup_pulseaudio_wsl()
    usbip_ok = check_usb_ip_support()
    test_audio_alternatives()
    
    guide = f"""
# WSL2 音频配置完整指南

## 当前环境状态
- WSL版本: {wsl_version}
- PulseAudio可用: {pulseaudio_ok}
- USB/IP可用: {usbip_ok}

## 方案1: PulseAudio输出 (推荐用于播放音频)

### 在Windows上安装PulseAudio:
1. 下载 PulseAudio for Windows
2. 配置允许网络连接
3. 启动PulseAudio服务器

### 在WSL2中配置:
```bash
# 设置环境变量
export PULSE_SERVER=tcp:{host_ip}:4713

# 或创建配置文件
mkdir -p ~/.pulse
echo "default-server = tcp:{host_ip}:4713" > ~/.pulse/client.conf
```

## 方案2: USB麦克风通过USB/IP (用于录音)

### 安装USB/IP:
```bash
sudo apt update
sudo apt install linux-tools-5.4.0-77-generic hwdata
sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/5.4.0-77-generic/usbip 20
```

### 在Windows上:
1. 安装USB/IP for Windows
2. 共享USB麦克风设备

### 在WSL2中:
```bash
sudo modprobe vhci-hcd
usbip attach -r [Windows_IP] -b [bus_id]
```

## 方案3: Windows子进程调用 (最实用)

在WSL2中调用Windows的语音识别功能：
```python
import subprocess
# 调用Windows Python进行语音识别
result = subprocess.run(['powershell.exe', '-c', 'python speech_recognition_script.py'])
```

## 方案4: 混合模式 (推荐)

结合多种方案：
1. 使用WSL2进行游戏逻辑
2. 通过Windows子进程处理语音识别
3. 使用PulseAudio播放音频反馈

## 故障排除

### 权限问题:
```bash
sudo usermod -a -G audio $USER
# 重新登录WSL
```

### 网络问题:
```bash
# 检查Windows防火墙是否阻止端口4713
# 在Windows PowerShell中:
# New-NetFirewallRule -DisplayName "PulseAudio" -Direction Inbound -Port 4713 -Protocol TCP -Action Allow
```

### 测试连接:
```bash
pactl info  # 测试PulseAudio连接
aplay /usr/share/sounds/alsa/Front_Left.wav  # 测试音频输出
```
"""
    
    # 保存指南到文件
    guide_file = "/home/readm/MOV/game/WSL2_AUDIO_GUIDE.md"
    try:
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        log(f"配置指南已保存到: {guide_file}")
    except Exception as e:
        log(f"保存指南失败: {e}", "ERROR")
    
    return guide

def main():
    """主函数"""
    log("开始WSL2音频解决方案分析...")
    guide = generate_wsl_audio_guide()
    log("分析完成！")

if __name__ == "__main__":
    main()