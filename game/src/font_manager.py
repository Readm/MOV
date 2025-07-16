import pygame
import os
from typing import Dict, Optional

class FontManager:
    """字体管理器"""
    
    def __init__(self):
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.font_path = self._get_chinese_font_path()
        
    def _get_chinese_font_path(self) -> Optional[str]:
        """获取字体路径，优先使用系统默认字体"""
        # 直接返回None，让pygame使用默认字体
        return None
    
    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        """获取指定大小的字体"""
        font_key = f"{size}_{bold}"
        
        if font_key not in self.fonts:
            if self.font_path and os.path.exists(self.font_path):
                try:
                    self.fonts[font_key] = pygame.font.Font(self.font_path, size)
                    print(f"使用中文字体: {self.font_path}")
                except Exception as e:
                    print(f"加载字体失败: {e}")
                    self.fonts[font_key] = pygame.font.Font(None, size)
            else:
                print("未找到中文字体，使用默认字体")
                self.fonts[font_key] = pygame.font.Font(None, size)
        
        return self.fonts[font_key]
    
    def render_text(self, text: str, size: int, color: tuple, bold: bool = False) -> pygame.Surface:
        """渲染文本"""
        if not text or text.strip() == "":
            # 返回空白表面
            surface = pygame.Surface((1, size))
            surface.fill((0, 0, 0))
            return surface
            
        font = self.get_font(size, bold)
        try:
            return font.render(text, True, color)
        except pygame.error as e:
            print(f"渲染文本失败 '{text}': {e}")
            # 使用默认字体作为备用
            default_font = pygame.font.Font(None, size)
            return default_font.render(text, True, color)

# 全局字体管理器实例
font_manager = FontManager()