import pygame
from abc import abstractmethod
from CL_Base import Base

# 클릭 여부 감지 기능 클래스
class ClickableBase(Base):
    STATE_NORMAL = 'normal'
    STATE_HOVER = 'hover'
    STATE_ACTIVE = 'active'

    def __init__(self, window, loc, scale, align='topleft', callBack=None):
        # surface는 자식 클래스(Button, BaseButton)가 정의해야 함
        super().__init__(window, loc, scale, align) # 부모 Base의 __init__
        self.callBack = callBack
        self.state = self.STATE_NORMAL

    # Overriding 통해 handleEvent 덮어쓰기
    def handleEvent(self, eventObj):
        if eventObj.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            return False
        if not hasattr(eventObj, 'pos'): 
            return False
            
        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos)

        if eventObj.type == pygame.MOUSEBUTTONDOWN:
            if eventPointInButtonRect: 
                self.state = self.STATE_ACTIVE
        
        elif eventObj.type == pygame.MOUSEBUTTONUP:
            if eventPointInButtonRect and self.state == self.STATE_ACTIVE:
                self.state = self.STATE_HOVER
                if self.callBack is not None:
                    # 자식이 콜백을 어떻게 실행할지 _execute_callback에 위임
                    self._execute_callback() 
                    return True
            else:
                self.state = self.STATE_NORMAL

        elif eventObj.type == pygame.MOUSEMOTION:
            if eventPointInButtonRect:
                if self.state == self.STATE_NORMAL: 
                    self.state = self.STATE_HOVER
            else:
                self.state = self.STATE_NORMAL
        return False

    @abstractmethod
    def _execute_callback(self):
        # 실행 기능은 자식 클래스에서 지정
        pass

    @abstractmethod
    def draw(self):
        # 그리는 방식은 자식 클래스에서 지정
        pass