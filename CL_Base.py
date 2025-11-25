import pygame
from abc import ABC, abstractmethod

class Base(ABC):
    # (수정) align='topleft' 매개변수 추가
    def __init__(self, window, loc, scale, align='topleft'): 
        """
        오브젝트를 "화면에 띄우기 위한" 공통 초기화 로직
        자식 클래스에서 self.surface를 먼저 정의한 후 호출해야 합니다.
        """
        self.window = window
        self.loc = loc

        # 자식 클래스에서 설정한 self.surface를 기반으로 크기 조절
        original_width = self.surface.get_width()
        original_height = self.surface.get_height()

        new_size = None 

        # 매개변수 바탕으로 스케일 설정
        if isinstance(scale, int):
            new_width = scale
            aspect_ratio = original_height / original_width
            new_height = int(new_width * aspect_ratio)
            new_size = (new_width, new_height)
        elif isinstance(scale, tuple):
            new_size = scale

        if new_size is not None:
            self.surface = pygame.transform.smoothscale(self.surface, new_size)

        # 히트박스 설정
        self.rect = self.surface.get_rect()
        
        # (수정) align 매개변수에 따라 위치 기준을 설정
        if align == 'center':
            self.rect.center = self.loc
        elif align == 'topright':
            self.rect.topright = self.loc
        # (다른 정렬 기준이 필요하면 elif로 추가...)
        else: # 기본값 'topleft'
            self.rect.topleft = self.loc

    @abstractmethod
    def handleEvent(self, event):
        """이벤트를 처리하는 추상 메서드"""
        pass

    @abstractmethod
    def draw(self):
        """화면에 그리는 추상 메서드"""
        self.window.blit(self.surface, self.rect)