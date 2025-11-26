import pygame
from abc import ABC
from config import * 
from CL_Interactive_Base import ClickableBase

# --- 폰트 로드 (한글 깨짐 방지) ---
def load_font(size):
    try:
        return pygame.font.Font(FONT_PATH, size)
    except (FileNotFoundError, pygame.error):
        print(f"경고: '{FONT_PATH}' 폰트를 찾을 수 없습니다. 기본 폰트로 대체합니다.")
        return pygame.font.Font(None, size)

class SimpleText():
    """화면에 텍스트를 그리는 클래스"""
    def __init__(self, window, loc, text, size, color, align='left'):
        self.window = window
        self.loc = loc
        self.textColor = color
        self.align = align
        self.font = load_font(size)
        self.text = None
        self.setValue(text)

    def setValue(self, newText):
        if self.text == newText:
            return
        self.text = newText
        self.textSurface = self.font.render(self.text, True, self.textColor)

    def draw(self):
        if self.window is None: return

        if self.align == 'left':
            self.window.blit(self.textSurface, self.loc)
        elif self.align == 'right':
            rect = self.textSurface.get_rect(topright=self.loc)
            self.window.blit(self.textSurface, rect)
        elif self.align == 'center':
            rect = self.textSurface.get_rect(center=self.loc)
            self.window.blit(self.textSurface, rect)

class BaseButton(ClickableBase): 
    """기본적인 사각형 텍스트 버튼"""
    def __init__(self, window, loc, text, size, width, height, callBack=None):
        self.font = load_font(size)
        self.text = text 
        
        self.surface = pygame.Surface((width, height)) 
        
        super().__init__(window, loc, scale=(width, height), align='topleft', callBack=callBack)
        
        self.textSurface = self.font.render(text, True, WHITE)
        self.textRect = self.textSurface.get_rect(center=self.rect.center)
        
        self.colorNormal = (100, 100, 100) 
        self.colorHover = (150, 150, 150)  
        self.colorActive = (0, 150, 0)     

    def _execute_callback(self):
        if self.callBack:
            self.callBack(self.text)

    def draw(self):
        color = self.colorNormal
        if self.state == self.STATE_ACTIVE: color = self.colorActive
        elif self.state == self.STATE_HOVER: color = self.colorHover
        
        pygame.draw.rect(self.window, color, self.rect)
        self.window.blit(self.textSurface, self.textRect)

class ImageButton(ClickableBase):
    """(v13) 이미지 기반 버튼"""
    def __init__(self, window, loc, image_path, width, height, callBack=None, callback_arg=None):
        try:
            self.surface = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            print(f"이미지 로드 실패: {image_path}")
            self.surface = pygame.Surface((width, height))
            self.surface.fill((150, 150, 150)) 
            
        self.callback_arg = callback_arg
        
        # 이미지는 이미 로드했으므로 scale로 크기 조절
        super().__init__(window, loc, scale=(width, height), align='topleft', callBack=callBack)

    def _execute_callback(self):
        if self.callBack:
            if self.callback_arg: self.callBack(self.callback_arg)
            else: self.callBack()

    def draw(self):
        self.window.blit(self.surface, self.rect)

class FloatingText():
    """(v7) 팁 획득 시 떠올랐다가 사라지는 텍스트"""
    def __init__(self, window, loc, text, size, color, duration=1.5, upward_speed=20):
        self.window = window
        self.loc = list(loc)
        self.duration = duration
        self.upward_speed = upward_speed
        self.color = color
        
        self.font = load_font(size)
        self.text = text
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt
        self.loc[1] -= self.upward_speed * dt
        return self.timer < self.duration

    def draw(self):
        remaining_ratio = max(0, 1.0 - (self.timer / self.duration))
        alpha = int(255 * remaining_ratio)
        
        try:
            text_surface = self.font.render(self.text, True, self.color)
            text_surface.set_alpha(alpha)
            rect = text_surface.get_rect(center=self.loc)
            self.window.blit(text_surface, rect)
        except Exception: pass