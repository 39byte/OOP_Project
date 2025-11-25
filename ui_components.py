# ui_components.py
import pygame
from abc import ABC
from config import FONT_PATH # (v3) config에서 폰트 경로 임포트
from CL_Interactive_Base import ClickableBase
# --- 폰트 로드 (한글 깨짐 방지) ---
def load_font(size):
    try:
        return pygame.font.Font(FONT_PATH, size)
    except (FileNotFoundError, pygame.error):
        print(f"경고: '{FONT_PATH}' 폰트를 찾을 수 없습니다. 기본 폰트로 대체합니다.")
        return pygame.font.Font(None, size)

class SimpleText():
    """OOP 9강 SimpleText 클래스"""
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
        if self.align == 'left':
            self.window.blit(self.textSurface, self.loc)
        elif self.align == 'right':
            rect = self.textSurface.get_rect(topright=self.loc)
            self.window.blit(self.textSurface, rect)
        elif self.align == 'center':
            rect = self.textSurface.get_rect(center=self.loc)
            self.window.blit(self.textSurface, rect)

class BaseButton(ClickableBase): # (!!!) 상속 변경 (ABC -> ClickableBase)
    # (!!!) STATE_NORMAL 등 3줄 삭제 (부모가 가짐)

    def __init__(self, window, loc, text, size, width, height, callBack=None):
        self.font = load_font(size)
        self.text = text 
        
        # (!!!) ClickableBase의 __init__에 필요한 surface를 미리 생성
        self.surface = pygame.Surface((width, height)) # 임시 surface
        
        # (!!!) 부모 ClickableBase의 __init__ 호출
        # (참고: BaseButton은 scale 대신 width/height를 쓰므로 scale=None 전달)
        super().__init__(window, loc, scale=(width, height), align='topleft', callBack=callBack)
        
        # (!!!) self.state는 부모가 관리하므로 삭제
        
        # self.rect는 부모가 (loc[0], loc[1], width, height)로 이미 생성해 줌

        self.textSurface = self.font.render(text, True, (255, 255, 255))
        self.textRect = self.textSurface.get_rect(center=self.rect.center)
        
        self.colorNormal = (100, 100, 100)
        self.colorHover = (150, 150, 150)
        self.colorActive = (0, 150, 0)

    # (!!!) handleEvent(self, eventObj) 메서드 전체 삭제 (!!!)
    # (부모인 ClickableBase가 모두 처리)

    def _execute_callback(self):
        """부모의 추상 메서드 구현 (self.text를 인자로 콜백 호출)"""
        self.callBack(self.text)

    def draw(self):
        """부모의 추상 메서드 구현 (기존 로직과 동일)"""
        color = self.colorNormal
        if self.state == self.STATE_ACTIVE: color = self.colorActive
        elif self.state == self.STATE_HOVER: color = self.colorHover
        pygame.draw.rect(self.window, color, self.rect)
        self.window.blit(self.textSurface, self.textRect)

class FloatingText():
    """
    (v7) 팁 획득 시 떠올랐다가 사라지는 텍스트
    OOP 9강의 SimpleText와 유사하지만, update 기능이 추가됨
    """
    def __init__(self, window, loc, text, size, color, duration=1.5, upward_speed=20):
        self.window = window
        self.loc = list(loc) # (x, y) 좌표, 리스트로 저장해야 수정 가능
        self.duration = duration
        self.upward_speed = upward_speed
        self.color = color
        
        self.font = load_font(size)
        self.text = text
        self.timer = 0.0

    def update(self, dt):
        """매 프레임 텍스트를 위로 이동시키고, 타이머를 갱신"""
        self.timer += dt
        
        # y좌표를 위로(감소) 이동
        self.loc[1] -= self.upward_speed * dt
        
        # duration이 지나면 False를 반환하여 삭제 신호를 보냄
        return self.timer < self.duration

    def draw(self):
        """텍스트를 화면에 그림 (점점 투명해지는 효과)"""
        
        # 남은 수명 비율 (1.0 -> 0.0)
        remaining_ratio = max(0, 1.0 - (self.timer / self.duration))
        # 투명도 (255 -> 0)
        alpha = int(255 * remaining_ratio)
        
        try:
            # 폰트 렌더링
            text_surface = self.font.render(self.text, True, self.color)
            # 투명도 설정
            text_surface.set_alpha(alpha)
            # 중앙 정렬
            rect = text_surface.get_rect(center=self.loc)
            self.window.blit(text_surface, rect)
            
        except Exception as e:
            print(f"FloatingText 그리기 오류: {e}")