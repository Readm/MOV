import pygame
import sys
from typing import Dict, Any
from scenes import Scene, MenuScene, GameScene
from enhanced_voice_recognition import create_voice_recognition

class Game:
    def __init__(self):
        pygame.init()
        
        # 游戏配置
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.TITLE = "Magic Of Voice"
        
        # 初始化显示
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.TITLE)
        self.clock = pygame.time.Clock()
        
        # 场景管理
        self.scenes: Dict[str, Scene] = {}
        self.current_scene = None
        
        # 语音识别
        self.voice_recognition = create_voice_recognition()
        
        # 游戏状态
        self.running = True
        
        # 初始化场景
        self._init_scenes()
        
    def _init_scenes(self):
        """初始化所有场景"""
        self.scenes["menu"] = MenuScene(self)
        self.scenes["game"] = GameScene(self)
        self.set_scene("menu")
        
    def set_scene(self, scene_name: str):
        """切换场景"""
        if scene_name in self.scenes:
            if self.current_scene:
                self.current_scene.on_exit()
            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter()
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_v:  # V键开始语音识别
                    self.voice_recognition.start_listening()
                # 键盘模拟语音命令 (1-5键)
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    self.voice_recognition.handle_key_test(event.key)
                # T键激活文本输入模拟语音
                elif event.key == pygame.K_t:
                    self._handle_text_input_simulation()
            elif event.type == pygame.TEXTINPUT:
                # 处理文本输入
                if hasattr(self.voice_recognition, 'handle_text_input'):
                    self.voice_recognition.handle_text_input(event.text)
            
            # 传递事件给当前场景
            if self.current_scene:
                self.current_scene.handle_event(event)
    
    def update(self, dt: float):
        """更新游戏状态"""
        # 检查语音识别结果
        voice_command = self.voice_recognition.get_command()
        if voice_command:
            if self.current_scene:
                self.current_scene.handle_voice_command(voice_command)
        
        # 更新当前场景
        if self.current_scene:
            self.current_scene.update(dt)
    
    def render(self):
        """渲染游戏"""
        self.screen.fill((0, 0, 0))  # 黑色背景
        
        if self.current_scene:
            self.current_scene.render(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """主游戏循环"""
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0  # 转换为秒
            
            self.handle_events()
            self.update(dt)
            self.render()
    
    def _handle_text_input_simulation(self):
        """处理文本输入模拟语音"""
        print("\n=== 语音模拟模式 ===")
        print("请输入语音命令 (fire/ice/heal/start/menu):")
        
        # 模拟一些常用命令
        test_commands = ["fire", "ice", "heal", "start", "menu"]
        for i, cmd in enumerate(test_commands, 1):
            print(f"{i}. {cmd}")
        
        # 这里可以扩展为实际的文本输入界面
        if hasattr(self.voice_recognition, 'simulate_voice_input'):
            self.voice_recognition.simulate_voice_input("fire")  # 默认演示
    
    def quit(self):
        """退出游戏"""
        self.running = False
        self.voice_recognition.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()