# CL_Base.py
import pygame
from abc import ABC, abstractmethod

# 위치랑 크기 잡는 기능 클래스
class Base(ABC):
    def __init__(self, window, loc, scale, align='topleft'): 
        self.window = window
        self.loc = loc

        # 자식 클래스에서 self.surface를 먼저 정의해야 함
        original_width = self.surface.get_width()
        original_height = self.surface.get_height()

        new_size = None 
        if isinstance(scale, int):
            new_width = scale
            aspect_ratio = original_height / original_width
            new_height = int(new_width * aspect_ratio)
            new_size = (new_width, new_height)
        elif isinstance(scale, tuple):
            new_size = scale

        if new_size is not None:
            self.surface = pygame.transform.smoothscale(self.surface, new_size)

        self.rect = self.surface.get_rect()
        
        if align == 'center':
            self.rect.center = self.loc
        elif align == 'topright':
            self.rect.topright = self.loc
        else: 
            self.rect.topleft = self.loc

    @abstractmethod
    def handleEvent(self, event):
        pass

    @abstractmethod
    def draw(self):
        self.window.blit(self.surface, self.rect)