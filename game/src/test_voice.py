#!/usr/bin/env python3
"""
语音识别测试脚本
"""
from web_speech_recognition import SimpleSpeechRecognition

def test_voice_recognition():
    print("🎤 语音识别功能测试")
    print("=" * 40)
    
    # 创建语音识别实例
    recognizer = SimpleSpeechRecognition()
    
    # 测试用例
    test_cases = [
        "fire",
        "fireball", 
        "ice",
        "freeze",
        "cold",
        "heal",
        "cure", 
        "health",
        "start",
        "begin",
        "menu",
        "back",
        "quit",
        "exit",
        "hello fire spell",  # 包含命令的句子
        "I want to cast ice magic",  # 复杂句子
        "random text",  # 无效命令
        "火球",  # 中文
        "冰冻",
        "治愈",
    ]
    
    print("测试语音命令识别:")
    print("-" * 40)
    
    for test_input in test_cases:
        recognizer.simulate_voice_input(test_input)
        
        # 检查是否有命令被识别
        command = recognizer.get_command()
        if command:
            print(f"✅ '{test_input}' -> {command}")
        else:
            print(f"❌ '{test_input}' -> 未识别")
    
    print("\n🎯 测试完成!")
    
    # 统计识别率
    total_tests = len(test_cases)
    valid_commands = ["fire", "fireball", "ice", "freeze", "cold", "heal", "cure", "health", "start", "begin", "menu", "back", "quit", "exit", "hello fire spell", "I want to cast ice magic", "火球", "冰冻", "治愈"]
    
    print(f"📊 测试用例总数: {total_tests}")
    print(f"📊 预期可识别: {len(valid_commands)}")

if __name__ == "__main__":
    test_voice_recognition()