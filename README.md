# MOV
Magic Of Voice — 用声音施法的像素风战斗游戏

> 无论你发出什么声音，都能转化为一个技能。

## 快速开始

**环境要求：** Python 3.x，Chrome 浏览器（语音识别需要）

```bash
# 克隆仓库
git clone https://github.com/Readm/MOV.git
cd MOV

# 启动本地服务器（Web Speech API 需要 localhost）
python demo/serve.py
```

然后在 **Chrome** 中打开 `http://localhost:8080`，允许麦克风权限即可开始游戏。

### 操作说明

| 操作 | 说明 |
|---|---|
| `WASD` | 移动角色 |
| `空格` / 鼠标点击 | 消耗专注值，时停，开始语音施法 |
| 说出音节 | 识别完成后自动释放技能 |
| 无麦克风 | 3秒后回退键盘输入，打字后按回车 |

### 咒语示例

| 喊出 | 效果 |
|---|---|
| `a` | 火（1级） |
| `a ka` | 火弹（2级） |
| `da a ka` | 强火弹（3级） |
| `i shi` | 冰盾 |
| `u ka to` | 追踪雷弹 |
| `e mi` | 土愈（回血） |

任何不在列表中的声音也会被推断为技能，慢慢探索规律！

---

## 项目结构

```
MOV/
├── demo/              # 可直接运行的 HTML5 游戏 Demo
│   ├── index.html     # 游戏主体
│   ├── sprites.js     # 像素风精灵系统
│   └── serve.py       # 本地服务器
├── cocos/             # Cocos Creator 3.x 项目骨架（TypeScript）
│   └── assets/scripts/
│       ├── voice/     # 语音引擎（Web / 微信小游戏双平台）
│       ├── spell/     # 咒语解析系统
│       ├── game/      # 战斗管理、角色、敌人
│       └── scenes/    # 场景脚本
├── DOC/
│   └── 设计文档.md    # 游戏设计文档 v0.1
└── game/              # 早期 Python/Pygame 原型（已弃用）
```

## 技术栈

- **Demo**：纯 HTML5 Canvas + Web Speech API，无依赖，Chrome 直接运行
- **正式版**：Cocos Creator 3.x + TypeScript，目标平台 PC Web + 微信小游戏

---

## 历史进度

+ 2017 第一阶段调研（Unity + 语音识别算法）
+ Python/Pygame 原型（基础施法系统）
+ 2026 重启：切换至 HTML5 + Cocos Creator 方案，完成玩法设计文档与可玩 Demo
