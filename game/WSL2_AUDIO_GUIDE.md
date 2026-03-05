
# WSL2 音频配置完整指南

## 当前环境状态
- WSL版本: Unknown
- PulseAudio可用: False
- USB/IP可用: False

## 方案1: PulseAudio输出 (推荐用于播放音频)

### 在Windows上安装PulseAudio:
1. 下载 PulseAudio for Windows
2. 配置允许网络连接
3. 启动PulseAudio服务器

### 在WSL2中配置:
```bash
# 设置环境变量
export PULSE_SERVER=tcp:10.255.255.254:4713

# 或创建配置文件
mkdir -p ~/.pulse
echo "default-server = tcp:10.255.255.254:4713" > ~/.pulse/client.conf
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
