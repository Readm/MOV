# Magic Of Voice - Python版本

基于Pygame的2D像素风格语音控制游戏

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行游戏

```bash
cd src
python game.py
```

## 控制说明

### 键盘控制
- **空格键**: 开始游戏
- **WASD**: 移动角色
- **V键**: 开始语音识别
- **M键**: 返回主菜单
- **ESC**: 退出游戏

### 语音命令
- "开始" 或 "start": 开始游戏
- "火球" 或 "fireball": 释放火球术
- "冰冻" 或 "freeze": 释放冰冻术  
- "治愈" 或 "heal": 释放治愈术
- "菜单" 或 "menu": 返回主菜单
- "退出" 或 "quit": 退出游戏

## 项目结构

```
game/
├── src/                    # 源代码
│   ├── game.py            # 主游戏类
│   ├── scenes.py          # 场景管理
│   ├── voice_recognition.py # 语音识别
│   └── __init__.py
├── assets/                # 游戏资源
│   ├── sprites/          # 精灵图片
│   ├── sounds/           # 音效文件
│   └── fonts/            # 字体文件
├── docs/                 # 文档
├── requirements.txt      # Python依赖
└── README.md            # 说明文档
```

## 功能特性

- ✅ 基础游戏框架
- ✅ 场景管理系统
- ✅ 语音识别集成
- ✅ 魔法咒语系统
- ✅ 简单的2D角色控制
- ✅ 视觉魔法效果

## 待开发功能

- [ ] 更多魔法咒语
- [ ] 敌人AI系统
- [ ] 关卡设计
- [ ] 音效和背景音乐
- [ ] 像素艺术资源
- [ ] 存档系统

## 技术栈

- **游戏引擎**: Pygame
- **语音识别**: SpeechRecognition + Google Web Speech API
- **音频处理**: PyAudio
- **开发语言**: Python 3.8+