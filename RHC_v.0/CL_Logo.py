import pygame
import webbrowser
from CL_Base import Base  # Base 클래스 임포트

class Logo(Base):  # Base 클래스 상속
    def __init__(self, window, loc, scale, url):
        self.url = url
        
        # self.surface를 먼저 정의
        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/Logo.png')

        # 부모 클래스의 __init__ 호출 (크기 조절 및 rect 설정)
        super().__init__(window, loc, scale)

    def handleEvent(self, event):
        if not hasattr(event, 'pos'):
            return False
        
        coverOX = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if coverOX:
                webbrowser.open(self.url)
                return True 

        return False

    def draw(self):
        self.window.blit(self.surface, self.rect)