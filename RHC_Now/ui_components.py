import pygame
from abc import ABC
from config import * 
from CL_Interactive_Base import ClickableBase

def load_font(size):
    try:
        return pygame.font.Font(FONT_PATH, size)
    except (FileNotFoundError, pygame.error):
        print(f"경고: '{FONT_PATH}' 폰트를 찾을 수 없습니다. 기본 폰트로 대체합니다.")
        return pygame.font.Font(None, size)

# 화면에 텍스트 그리는 클래스
class SimpleText():
    def __init__(self, window, loc, text, size, color, align='left'):
        self.window = window
        self.loc = loc
        self.textColor = color
        self.align = align
        self.font = load_font(size)     # 폰트 로드
        self.text = None
        self.setValue(text)         # 초기 텍스트 설정

    # 텍스트 바뀔 경우 갱신하기
    def setValue(self, newText):
        if self.text == newText:
            return
        self.text = newText
        self.textSurface = self.font.render(self.text, True, self.textColor)

    def draw(self):
        if self.window is None: return

        # 정렬 방식에 따라 달라지는 표시 방식
        if self.align == 'left':
            self.window.blit(self.textSurface, self.loc)
        elif self.align == 'right':
            rect = self.textSurface.get_rect(topright=self.loc)
            self.window.blit(self.textSurface, rect)
        elif self.align == 'center':
            rect = self.textSurface.get_rect(center=self.loc)
            self.window.blit(self.textSurface, rect)

# 사각형 텍스트 버튼
class BaseButton(ClickableBase): 
    def __init__(self, window, loc, text, size, width, height, callBack=None):
        self.font = load_font(size)
        self.text = text 
        
        self.surface = pygame.Surface((width, height)) 
        
        super().__init__(window, loc, scale=(width, height), align='topleft', callBack=callBack)
        
        self.textSurface = self.font.render(text, True, WHITE)
        self.textRect = self.textSurface.get_rect(center=self.rect.center)
        
        # 상태별 버튼 색상
        self.colorNormal = (100, 100, 100) 
        self.colorHover = (150, 150, 150)  
        self.colorActive = (0, 150, 0)     

    # 클릭 시 실행할 동장
    def _execute_callback(self):
        if self.callBack:
            self.callBack(self.text)

    # 상태에 따라 달라지는 색깔
    def draw(self):
        color = self.colorNormal
        if self.state == self.STATE_ACTIVE: color = self.colorActive
        elif self.state == self.STATE_HOVER: color = self.colorHover
        
        pygame.draw.rect(self.window, color, self.rect)
        self.window.blit(self.textSurface, self.textRect)

# 이미지 기반 버튼 방식
class ImageButton(ClickableBase):
    def __init__(self, window, loc, image_path, width, height, callBack=None, callback_arg=None):
        try:
            self.surface = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            print(f"이미지 로드 실패: {image_path}")
            self.surface = pygame.Surface((width, height))
            self.surface.fill((150, 150, 150)) 
            
        self.callback_arg = callback_arg        # 콜백 함수에 전달할 인자
        
        # 이미지는 이미 로드했으므로 scale로 크기 조절
        super().__init__(window, loc, scale=(width, height), align='topleft', callBack=callBack)

    def _execute_callback(self):
        if self.callBack:   # 콜백 함수 인자 있으면 인자와 호출, 없으면 인자 없이 호출
            if self.callback_arg: self.callBack(self.callback_arg)
            else: self.callBack()

    def draw(self):
        self.window.blit(self.surface, self.rect)

# 잠깐 떠올랐다가 사라지는 텍스트
class FloatingText():
    def __init__(self, window, loc, text, size, color, duration=1.5, upward_speed=20):
        self.window = window
        self.loc = list(loc)        # Y좌표 계속 변경해야 해서 리스트로 저장
        self.duration = duration
        self.upward_speed = upward_speed        # 초당 위로 올라가는 픽셀 수
        self.color = color
        
        self.font = load_font(size)
        self.text = text
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt
        self.loc[1] -= self.upward_speed * dt   # Y좌표 위로 올리기
        return self.timer < self.duration       # 아직 지속시간 내인지 확인

    def draw(self):     # 남은 시간 비례해서 투명도 조절
        remaining_ratio = max(0, 1.0 - (self.timer / self.duration))
        alpha = int(255 * remaining_ratio)
        
        try:
            text_surface = self.font.render(self.text, True, self.color)
            text_surface.set_alpha(alpha)   # 텍스트 투명도 설정
            rect = text_surface.get_rect(center=self.loc)
            self.window.blit(text_surface, rect)
        except Exception: pass