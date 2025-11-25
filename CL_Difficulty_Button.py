import pygame
from CL_Interactive_Base import ClickableBase # (!!!) 수입 변경

class Button(ClickableBase): # (!!!) 상속 변경
    # (!!!) state_normal 등 3줄 삭제 (부모가 가짐)

    def __init__(self, window, loc, scale, callBack=None): 
        # (!!!) callBack은 부모가 처리하므로 self.callBack 삭제
        # (!!!) self.state도 부모가 처리하므로 삭제
        
        # self.surfaceUp, self.surfaceDown은 자식이 먼저 정의 (Easy, Normal...)
        
        self.surface = self.surfaceUp # 기본 surface 설정
        
        # (!!!) 부모 ClickableBase의 __init__ 호출
        super().__init__(window, loc, scale, align='center', callBack=callBack)

        self.surfaceDown = pygame.transform.smoothscale(self.surfaceDown, self.rect.size)

        desired_hitbox_height = 100 
        shrink_amount_y = desired_hitbox_height - self.rect.height
        self.rect = self.rect.inflate(0, shrink_amount_y)

    # (!!!) handleEvent(self, event) 메서드 전체 삭제 (!!!)
    # (부모인 ClickableBase가 모두 처리)

    def _execute_callback(self):
        """부모의 추상 메서드 구현 (인자 없이 콜백 호출)"""
        self.callBack()

    def draw(self):
        """부모의 추상 메서드 구현 (기존 로직과 동일)"""
        if self.state == self.STATE_ACTIVE:
            self.window.blit(self.surfaceDown, self.rect)
        else: 
            self.window.blit(self.surface, self.rect)

# --- 자식 클래스 ---
# (자식 클래스들은 수정할 필요 없음)
# 부모(Button)의 __init__을 호출하기 전에 surface들을 정의하는 기존 방식이
# CL_Base의 요구사항과 일치합니다.

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