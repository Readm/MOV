#!/usr/bin/env python3
"""
增强语音识别测试脚本
"""
from web_speech_recognition import SimpleSpeechRecognition

def test_enhanced_voice():
    print("🎤 增强语音识别测试")
    print("=" * 50)
    
    recognizer = SimpleSpeechRecognition()
    
    # 新的测试用例，包含多语言和新魔法
    test_cases = [
        # 英文基础命令
        "fire", "fireball", "flame", "burn", "blaze",
        "ice", "freeze", "cold", "frost", "blizzard", 
        "heal", "cure", "health", "restore",
        "lightning", "thunder", "bolt", "shock",
        "shield", "protect", "guard", "defend",
        
        # 中文命令
        "火球", "火焰", "燃烧",
        "冰冻", "寒冰", "霜冻",
        "治愈", "治疗", "恢复",
        "闪电", "雷电", "电击",
        "盾牌", "防护", "保护",
        
        # 日文命令
        "ファイア", "フィア",
        "アイス", "フリーズ", 
        "ヒール", "キュア",
        "サンダー", "ライトニング",
        "シールド", "ガード",
        
        # 西班牙文命令
        "fuego", "hielo", "sanar", "rayo", "escudo",
        
        # 法文命令  
        "feu", "glace", "guérir", "foudre", "bouclier",
        
        # 复杂句子
        "I want to cast a fireball spell",
        "Please use ice magic now",
        "Cast healing magic on me",
        "Strike with lightning bolt",
        "Activate protective shield",
        
        # 游戏控制
        "start game", "begin", "menu", "back", "quit", "exit",
        
        # 无效命令
        "random text", "hello world", "invalid command"
    ]
    
    print(f"测试 {len(test_cases)} 个语音命令:")
    print("-" * 50)
    
    recognized_count = 0
    total_count = len(test_cases)
    
    for test_input in test_cases:
        recognizer.simulate_voice_input(test_input)
        command = recognizer.get_command()
        
        if command:
            print(f"✅ '{test_input}' -> {command}")
            recognized_count += 1
        else:
            print(f"❌ '{test_input}' -> 未识别")
    
    print("\n📊 测试统计:")
    print("-" * 50)
    print(f"总测试数: {total_count}")
    print(f"识别成功: {recognized_count}")
    print(f"识别失败: {total_count - recognized_count}")
    print(f"识别率: {recognized_count/total_count*100:.1f}%")
    
    print("\n🎯 支持的魔法命令:")
    print("-" * 50)
    magic_commands = ["fire", "ice", "heal", "lightning", "shield"]
    for cmd in magic_commands:
        print(f"⚡ {cmd.upper()}")
    
    print("\n🌍 支持的语言:")
    print("-" * 50)
    languages = ["English", "中文", "日本語", "Español", "Français"]
    for lang in languages:
        print(f"🗣️ {lang}")

if __name__ == "__main__":
    test_enhanced_voice()