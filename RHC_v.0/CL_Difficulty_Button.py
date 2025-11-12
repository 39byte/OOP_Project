# 난이도 버튼을 위한 추상 클래스

import pygame
from abc import ABC
from CL_Base import Base

class Button(Base):
    state_normal = 'normal'
    state_hover = 'hover'
    state_active = 'active'

    def __init__(self, window, loc, scale):
        # 자식 클래스(Easy, Normal, Hard)가 surfaceUp/Down을 설정한 상태
        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/EasyUp.png')
        
        # 부모 클래스 __init__ 호출 (surfaceUp 크기 조절, rect 생성)
        super().__init__(window, loc, scale)

        # surfaceUp, Down 이미지 크기 스케일에 맞춰 조정
        self.surfaceUp = pygame.transform.smoothscale(self.surfaceUp, self.rect.size)
        self.surfaceDown = pygame.transform.smoothscale(self.surfaceDown, self.rect.size)

        # 히트박스 확장 로직 (기존 유지)
        desired_hitbox_height = 100 
        shrink_amount_y = desired_hitbox_height - self.rect.height
        self.rect = self.rect.inflate(0, shrink_amount_y)

        # 버튼의 상태를 노말 상태로 초기화
        self.state = Button.state_normal
        self.rect.center = self.loc

    def handleEvent(self, event):
        # (이하 로직은 기존과 동일)
        if not hasattr(event, 'pos'):
            return False
        
        coverOX = self.rect.collidepoint(event.pos)

        # '보통' 상태일 때
        if self.state == Button.state_normal:
            if event.type == pygame.MOUSEMOTION:
                if coverOX:
                    self.state = Button.state_hover
        
        # '호버' 상태일 때
        elif self.state == Button.state_hover:
            if event.type == pygame.MOUSEMOTION:
                if not coverOX:
                    self.state = Button.state_normal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if coverOX:
                    self.state = Button.state_active  
        
        # '활성' (클릭된) 상태일 때
        elif self.state == Button.state_active:
            # 2. 마우스를 떼었을 때
            if event.type == pygame.MOUSEBUTTONUP:
                # 3. 마우스가 여전히 버튼 위에 있다면
                if coverOX:
                    self.state = Button.state_hover  
                    return True                     
                else:
                    # 마우스를 누른 채로 버튼 밖으로 나갔다가 뗐을 경우 (클릭 취소)
                    self.state = Button.state_normal
            
            elif event.type == pygame.MOUSEMOTION:
                if not coverOX:
                    self.state = Button.state_hover 

        return False

    # 상태에 따라 모양 바뀌기
    def draw(self):
        if self.state == Button.state_active:
            self.window.blit(self.surfaceDown, self.rect)
        else: self.window.blit(self.surfaceUp, self.rect)


# 쉬움 난이도 버튼
class Easy_Button(Button):
    def __init__(self, window, loc, scale):
        self.surfaceUp = pygame.image.load('Rush_Hour_Chef/Assets/EasyUp.png')
        self.surfaceDown = pygame.image.load('Rush_Hour_Chef/Assets/EasyDown.png')
        super().__init__(window, loc, scale)

# 노말 난이도 버튼
class Normal_Button(Button):
    def __init__(self, window, loc, scale):
        self.surfaceUp = pygame.image.load('Rush_Hour_Chef/Assets/NormalUp.png')
        self.surfaceDown = pygame.image.load('Rush_Hour_Chef/Assets/NormalDown.png')
        super().__init__(window, loc, scale)

# 하드 난이도 버튼
class Hard_Button(Button):
    def __init__(self, window, loc, scale):
        self.surfaceUp = pygame.image.load('Rush_Hour_Chef/Assets/HardUp.png')
        self.surfaceDown = pygame.image.load('Rush_Hour_Chef/Assets/HardDown.png')
        super().__init__(window, loc, scale)