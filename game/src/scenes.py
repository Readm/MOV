import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from font_manager import font_manager

if TYPE_CHECKING:
    from game import Game

class Scene(ABC):
    """场景基类"""
    
    def __init__(self, game: 'Game'):
        self.game = game
    
    @abstractmethod
    def on_enter(self):
        """进入场景时调用"""
        pass
    
    @abstractmethod
    def on_exit(self):
        """退出场景时调用"""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """处理pygame事件"""
        pass
    
    @abstractmethod
    def handle_voice_command(self, command: str):
        """处理语音命令"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """更新场景"""
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """渲染场景"""
        pass

class MenuScene(Scene):
    """主菜单场景"""
    
    def __init__(self, game: 'Game'):
        super().__init__(game)
        
    def on_enter(self):
        print("进入主菜单")
    
    def on_exit(self):
        print("退出主菜单")
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.set_scene("game")
    
    def handle_voice_command(self, command: str):
        command_lower = command.lower()
        if "开始" in command_lower or "start" in command_lower:
            self.game.set_scene("game")
        elif "退出" in command_lower or "quit" in command_lower:
            self.game.quit()
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        # 标题
        title_text = font_manager.render_text("Magic Of Voice", 74, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 200))
        screen.blit(title_text, title_rect)
        
        # 说明文字
        instructions = [
            "Press SPACE to start game",
            "Press V for voice recognition", 
            "Press T for text simulation",
            "Keyboard: 1-Fire 2-Ice 3-Heal 4-Start 5-Menu",
            "Press ESC to exit"
        ]
        
        y_offset = 300
        for instruction in instructions:
            text = font_manager.render_text(instruction, 36, (200, 200, 200))
            text_rect = text.get_rect(center=(screen.get_width()//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40

class GameScene(Scene):
    """游戏场景"""
    
    def __init__(self, game: 'Game'):
        super().__init__(game)
        
        # 玩家
        self.player_pos = [400, 300]
        self.player_size = 32
        self.player_speed = 200
        
        # 魔法效果
        self.magic_effects = []
        
    def on_enter(self):
        print("进入游戏")
    
    def on_exit(self):
        print("退出游戏")
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.game.set_scene("menu")
    
    def handle_voice_command(self, command: str):
        command_lower = command.lower()
        
        # 魔法咒语
        if command_lower == "fire":
            self.cast_fireball()
        elif command_lower == "ice":
            self.cast_freeze()
        elif command_lower == "heal":
            self.cast_heal()
        elif command_lower == "lightning":
            self.cast_lightning()
        elif command_lower == "shield":
            self.cast_shield()
        elif command_lower == "menu":
            self.game.set_scene("menu")
    
    def cast_fireball(self):
        """释放火球术"""
        effect = {
            'type': 'fireball',
            'pos': self.player_pos.copy(),
            'color': (255, 100, 0),
            'radius': 20,
            'lifetime': 2.0
        }
        self.magic_effects.append(effect)
        print("释放火球术!")
    
    def cast_freeze(self):
        """释放冰冻术"""
        effect = {
            'type': 'freeze',
            'pos': self.player_pos.copy(),
            'color': (100, 200, 255),
            'radius': 30,
            'lifetime': 1.5
        }
        self.magic_effects.append(effect)
        print("释放冰冻术!")
    
    def cast_heal(self):
        """释放治愈术"""
        effect = {
            'type': 'heal',
            'pos': self.player_pos.copy(),
            'color': (100, 255, 100),
            'radius': 25,
            'lifetime': 1.0
        }
        self.magic_effects.append(effect)
        print("释放治愈术!")
    
    def cast_lightning(self):
        """释放闪电术"""
        effect = {
            'type': 'lightning',
            'pos': self.player_pos.copy(),
            'color': (255, 255, 0),
            'radius': 35,
            'lifetime': 0.8
        }
        self.magic_effects.append(effect)
        print("释放闪电术!")
    
    def cast_shield(self):
        """释放护盾术"""
        effect = {
            'type': 'shield',
            'pos': self.player_pos.copy(),
            'color': (0, 200, 255),
            'radius': 40,
            'lifetime': 3.0
        }
        self.magic_effects.append(effect)
        print("释放护盾术!")
    
    def update(self, dt: float):
        # 玩家移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_pos[0] -= self.player_speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_pos[0] += self.player_speed * dt
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_pos[1] -= self.player_speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_pos[1] += self.player_speed * dt
        
        # 边界检查
        self.player_pos[0] = max(self.player_size//2, min(self.game.SCREEN_WIDTH - self.player_size//2, self.player_pos[0]))
        self.player_pos[1] = max(self.player_size//2, min(self.game.SCREEN_HEIGHT - self.player_size//2, self.player_pos[1]))
        
        # 更新魔法效果
        for effect in self.magic_effects[:]:
            effect['lifetime'] -= dt
            if effect['lifetime'] <= 0:
                self.magic_effects.remove(effect)
    
    def render(self, screen: pygame.Surface):
        # 绘制玩家
        pygame.draw.circle(screen, (255, 255, 255), 
                          [int(self.player_pos[0]), int(self.player_pos[1])], 
                          self.player_size // 2)
        
        # 绘制魔法效果
        for effect in self.magic_effects:
            alpha = effect['lifetime'] / 2.0 * 255
            alpha = max(0, min(255, alpha))
            
            # 创建带透明度的表面
            surf = pygame.Surface((effect['radius'] * 2, effect['radius'] * 2), pygame.SRCALPHA)
            color_with_alpha = (*effect['color'], int(alpha))
            pygame.draw.circle(surf, color_with_alpha, (effect['radius'], effect['radius']), effect['radius'])
            
            screen.blit(surf, (effect['pos'][0] - effect['radius'], effect['pos'][1] - effect['radius']))
        
        # 说明文字
        instructions = [
            "WASD to move",
            "Voice spells: Fire/Ice/Heal/Lightning/Shield", 
            "Keyboard: 1-Fire 2-Ice 3-Heal",
            "Press T for text simulation",
            "Press M for menu"
        ]
        
        y_offset = 10
        for instruction in instructions:
            text = font_manager.render_text(instruction, 30, (200, 200, 200))
            screen.blit(text, (10, y_offset))
            y_offset += 35