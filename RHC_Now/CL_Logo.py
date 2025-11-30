import pygame
import webbrowser
from CL_Base import Base

# 처음 로고 이미지를 위한 클래스
class Logo(Base):
    def __init__(self, window, loc, scale, url):
        self.url = url
        
        # 부모 클래스의 __init__을 호출하기 전, self.surface를 먼저 정의
        try:
            self.surface = pygame.image.load('assets/Logo.png').convert_alpha()
        except pygame.error:
            print("로고 이미지(assets/Logo.png)를 찾을 수 없습니다.")
            self.surface = pygame.Surface((200, 100))
            self.surface.fill((0, 0, 255)) # 못 불러오면 파란색 박스로 대체

        super().__init__(window, loc, scale, align='center')    # 중앙 정렬

    def handleEvent(self, event):
        # Base 클래스의 추상 메서드 구현
        if not hasattr(event, 'pos'):
            return False
        
        coverOX = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if coverOX:
                webbrowser.open(self.url)
                return True 

        return False

    def draw(self):
        # Base 클래스의 추상 메서드 구현
        super().draw()