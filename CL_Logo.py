import pygame
import webbrowser
from CL_Base import Base  # (수정) CL_Base 임포트

class Logo(Base):  # (수정) Base 클래스 상속
    def __init__(self, window, loc, scale, url):
        self.url = url
        
        # (수정) 부모 클래스의 __init__을 호출하기 전에 self.surface를 먼저 정의
        self.surface = pygame.image.load('assets/Logo.png')

        # (수정) 부모 __init__ 호출
        # align='center'를 전달하여 이미지를 loc 좌표 기준으로 중앙 정렬
        super().__init__(window, loc, scale, align='center')
        
        # (삭제) 기존의 스케일링 및 rect 생성, 중앙 정렬 코드는
        # 이제 부모 클래스(Base)가 모두 처리하므로 삭제합니다.

    def handleEvent(self, event):
        """Base 클래스의 추상 메서드를 구현"""
        if not hasattr(event, 'pos'):
            return False
        
        coverOX = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if coverOX:
                webbrowser.open(self.url)
                return True 

        return False

    def draw(self):
        """Base 클래스의 추상 메서드를 구현"""
        # (수정) 부모 클래스의 draw 메서드를 호출하여 self.surface를 blit
        super().draw()