# CL_Difficulty_Button.py
import pygame
from CL_Interactive_Base import ClickableBase 

# 클릭했을 때 이미지 변경하는 기능 담당 클래스
class Button(ClickableBase): 
    def __init__(self, window, loc, scale, callBack=None): 
        self.surface = self.surfaceUp
        super().__init__(window, loc, scale, align='center', callBack=callBack)
        self.surfaceDown = pygame.transform.smoothscale(self.surfaceDown, self.rect.size)
        
        # 히트박스 최소치 보정
        desired_hitbox_height = 100 
        shrink_amount_y = desired_hitbox_height - self.rect.height
        # 기준 위치대로 크기만 늘리고 줄이기
        self.rect = self.rect.inflate(0, shrink_amount_y)

    def _execute_callback(self):
        if self.callBack: self.callBack()

    def draw(self):
        if self.state == self.STATE_ACTIVE:
            self.window.blit(self.surfaceDown, self.rect)
        else: 
            self.window.blit(self.surface, self.rect)

class Easy_Button(Button):
    def __init__(self, window, loc, scale, callBack=None):
        self.surfaceUp = pygame.image.load('assets/EasyUp.png')
        self.surfaceDown = pygame.image.load('assets/EasyDown.png')
        super().__init__(window, loc, scale, callBack=callBack)

class Normal_Button(Button):
    def __init__(self, window, loc, scale, callBack=None):
        self.surfaceUp = pygame.image.load('assets/NormalUp.png')
        self.surfaceDown = pygame.image.load('assets/NormalDown.png')
        super().__init__(window, loc, scale, callBack=callBack)

class Hard_Button(Button):
    def __init__(self, window, loc, scale, callBack=None):
        self.surfaceUp = pygame.image.load('assets/HardUp.png')
        self.surfaceDown = pygame.image.load('assets/HardDown.png')
        super().__init__(window, loc, scale, callBack=callBack)