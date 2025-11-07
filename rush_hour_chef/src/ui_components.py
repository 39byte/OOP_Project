# ui_components.py
import pygame
from config import FONT_PATH

class SimpleText():
    """OOP 9강 SimpleText 클래스 기반 (한글 폰트 적용)"""
    def __init__(self, window, loc, text, size, color, align='left'):
        pygame.font.init()
        self.window = window
        self.loc = loc
        self.textColor = color
        self.align = align
        try:
            self.font = pygame.font.Font(FONT_PATH, size)
        except (FileNotFoundError, pygame.error):
            print(f"'{FONT_PATH}' 폰트를 찾을 수 없습니다. 기본 폰트로 대체합니다.")
            self.font = pygame.font.Font(None, size)
        
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

class SimpleButton():
    """OOP 9강 SimpleButton 클래스 기반 (텍스트 버튼 + 콜백 적용)"""
    STATE_NORMAL = 'normal'
    STATE_HOVER = 'hover'
    STATE_ACTIVE = 'active'

    def __init__(self, window, loc, text, size, width, height, callBack=None):
        self.window = window
        self.loc = loc
        self.callBack = callBack
        self.state = self.STATE_NORMAL
        
        try:
            self.font = pygame.font.Font(FONT_PATH, size)
        except Exception:
            self.font = pygame.font.Font(None, size)

        self.text = text
        self.width = width
        self.height = height
        self.rect = pygame.Rect(loc[0], loc[1], width, height)

        # 텍스트 렌더링
        self.textSurface = self.font.render(text, True, (255, 255, 255)) # 흰색 텍스트
        self.textRect = self.textSurface.get_rect(center=self.rect.center)
        
        # 상태별 배경색
        self.colorNormal = (100, 100, 100) # 회색
        self.colorHover = (150, 150, 150)  # 밝은 회색
        self.colorActive = (0, 150, 0)    # 초록색

    def handleEvent(self, eventObj):
        if eventObj.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            return False

        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos)

        if eventObj.type == pygame.MOUSEBUTTONDOWN:
            if eventPointInButtonRect:
                self.state = self.STATE_ACTIVE
        
        elif eventObj.type == pygame.MOUSEBUTTONUP:
            if eventPointInButtonRect and self.state == self.STATE_ACTIVE:
                self.state = self.STATE_HOVER
                if self.callBack is not None:
                    self.callBack(self.text) # 콜백 실행 (버튼 텍스트를 인자로 전달)
                    return True
            else:
                self.state = self.STATE_NORMAL

        elif eventObj.type == pygame.MOUSEMOTION:
            if eventPointInButtonRect:
                if self.state == self.STATE_NORMAL:
                    self.state = self.STATE_HOVER
            else:
                self.state = self.STATE_NORMAL
        
        return False

    def draw(self):
        # 상태별 배경 그리기
        if self.state == self.STATE_ACTIVE:
            pygame.draw.rect(self.window, self.colorActive, self.rect)
        elif self.state == self.STATE_HOVER:
            pygame.draw.rect(self.window, self.colorHover, self.rect)
        else: # STATE_NORMAL
            pygame.draw.rect(self.window, self.colorNormal, self.rect)
        
        # 텍스트 그리기
        self.window.blit(self.textSurface, self.textRect)