import pygame
import webbrowser

class Logo():
    def __init__(self, window, loc, scale, url):
        self.window = window
        self.loc = loc
        self.url = url

        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/Logo.png')

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

        # 히트박스 설정
        self.rect = self.surface.get_rect()
        # 위치 설정
        self.rect.center = self.loc

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