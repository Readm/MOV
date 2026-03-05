#!/usr/bin/env python3
"""
语音识别调试测试脚本
"""
from enhanced_voice_recognition import create_voice_recognition
import time

def test_voice_with_debug():
    print("🎤 语音识别调试测试")
    print("=" * 50)
    
    # 创建语音识别实例
    voice_rec = create_voice_recognition()
    
    # 获取状态信息
    status = voice_rec.get_status()
    print("\n📊 语音识别状态:")
    print(f"  音频可用: {status['audio_available']}")
    print(f"  正在监听: {status['is_listening']}")
    print(f"  依赖库状态: {status['dependencies']}")
    print(f"  命令队列大小: {status['queue_size']}")
    
    print("\n🔧 测试键盘模拟功能:")
    print("模拟按键输入...")
    
    # 模拟键盘按键
    import pygame
    pygame.init()
    
    test_keys = [
        (pygame.K_1, "fire"),
        (pygame.K_2, "ice"),
        (pygame.K_3, "heal"),
        (pygame.K_4, "start"),
        (pygame.K_5, "menu")
    ]
    
    for key, expected_command in test_keys:
        print(f"\n模拟按键 {key}...")
        voice_rec.handle_key_test(key)
        
        # 检查命令队列
        command = voice_rec.get_command()
        if command == expected_command:
            print(f"✅ 成功: {key} -> {command}")
        else:
            print(f"❌ 失败: {key} -> {command} (期望: {expected_command})")
    
    print("\n🔧 测试文本模拟功能:")
    test_texts = [
        "fire",
        "cast fireball spell",
        "use ice magic",
        "heal me now",
        "activate lightning",
        "protect with shield",
        "火球",
        "冰冻",
        "治愈"
    ]
    
    for text in test_texts:
        print(f"\n模拟文本输入: '{text}'")
        voice_rec.simulate_voice_input(text)
        
        command = voice_rec.get_command()
        if command:
            print(f"✅ 识别成功: '{text}' -> {command}")
        else:
            print(f"❌ 识别失败: '{text}'")
    
    print("\n🔧 测试语音监听启动:")
    voice_rec.start_listening()
    
    # 获取更新后的状态
    status = voice_rec.get_status()
    print(f"监听状态: {status['is_listening']}")
    
    # 清理
    voice_rec.stop()
    
    print("\n✅ 调试测试完成!")

if __name__ == "__main__":
    test_voice_with_debug()