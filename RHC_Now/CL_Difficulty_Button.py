# CL_Difficulty_Button.py (수정됨)
import pygame
from abc import ABC

class Button(ABC):
    state_normal = 'normal'
    state_hover = 'hover'
    state_active = 'active'

    # 1. callBack=None 매개변수 추가
    def __init__(self, window, loc, scale, callBack=None): 
        self.window = window
        self.loc = loc
        self.callBack = callBack # 2. 콜백 저장
        
        # 3. 부모 클래스는 자식 클래스가 surfaceUp/Down을 먼저 정의했다고 가정함
        #    따라서 이 코드는 자식 클래스의 __init__에서 super()보다 먼저 호출되어야 함
        
        original_width = self.surfaceUp.get_width()
        original_height = self.surfaceUp.get_height()

        new_size = None 

        if isinstance(scale, int):
            new_width = scale
            aspect_ratio = original_height / original_width
            new_height = int(new_width * aspect_ratio)
            new_size = (new_width, new_height)
        elif isinstance(scale, tuple):
            new_size = scale

        if new_size is not None:
            self.surfaceUp = pygame.transform.smoothscale(self.surfaceUp, new_size)
            self.surfaceDown = pygame.transform.smoothscale(self.surfaceDown, new_size)

        self.rect = self.surfaceUp.get_rect()
        self.rect.center = self.loc

        desired_hitbox_height = 100 
        shrink_amount_y = desired_hitbox_height - self.rect.height
        self.rect = self.rect.inflate(0, shrink_amount_y)

        self.state = Button.state_normal

    def handleEvent(self, event):
        if not hasattr(event, 'pos'):
            return False
        
        coverOX = self.rect.collidepoint(event.pos)

        if self.state == Button.state_normal:
            if event.type == pygame.MOUSEMOTION:
                if coverOX:
                    self.state = Button.state_hover
        
        elif self.state == Button.state_hover:
            if event.type == pygame.MOUSEMOTION:
                if not coverOX:
                    self.state = Button.state_normal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if coverOX:
                    self.state = Button.state_active  
        
        elif self.state == Button.state_active:
            if event.type == pygame.MOUSEBUTTONUP:
                if coverOX:
                    self.state = Button.state_hover
                    
                    # 4. 콜백 실행 (OOP 9강 방식) [cite: 6492-6493, 6498]
                    if self.callBack is not None:
                        self.callBack() # 저장된 함수 실행
                        
                    return True                     
                else:
                    self.state = Button.state_normal
            
            elif event.type == pygame.MOUSEMOTION:
                if not coverOX:
                    self.state = Button.state_hover 

        return False

    def draw(self):
        if self.state == Button.state_active:
            self.window.blit(self.surfaceDown, self.rect)
        else: self.window.blit(self.surfaceUp, self.rect)


# --- 자식 클래스 수정 ---

class Easy_Button(Button):
    # 5. callBack=None 추가
    def __init__(self, window, loc, scale, callBack=None):
        # 6. (중요!) super().__init__보다 *먼저* 이미지를 로드해야 함
        self.surfaceUp = pygame.image.load(r'C:\HUFS_Project\RHC_Now\assets\EasyUp.png')
        self.surfaceDown = pygame.image.load(r'C:\HUFS_Project\RHC_Now\assets\EasyDown.png')
        
        # 7. 이미지가 로드된 후 부모 생성자 호출 (callBack 전달)
        super().__init__(window, loc, scale, callBack=callBack)

class Normal_Button(Button):
    # 5. callBack=None 추가
    def __init__(self, window, loc, scale, callBack=None):
        # 6. (중요!) super().__init__보다 *먼저* 이미지를 로드해야 함
        self.surfaceUp = pygame.image.load(r'C:\HUFS_Project\RHC_Now\assets\NormalUp.png')
        self.surfaceDown = pygame.image.load(r'C:\HUFS_Project\RHC_Now\assets\NormalDown.png')
        
        # 7. 이미지가 로드된 후 부모 생성자 호출 (callBack 전달)
        super().__init__(window, loc, scale, callBack=callBack)

class Hard_Button(Button):
    # 5. callBack=None 추가
    def __init__(self, window, loc, scale, callBack=None):
        # 6. (중요!) super().__init__보다 *먼저* 이미지를 로드해야 함
        self.surfaceUp = pygame.image.load(r'C:\HUFS_Project\RHC_Now\assets\HardUp.png')
        self.surfaceDown = pygame.image.load(r'C:\HUFS_Project\RHC_Now\assets\HardDown.png')
        
        # 7. 이미지가 로드된 후 부모 생성자 호출 (callBack 전달)
        super().__init__(window, loc, scale, callBack=callBack)