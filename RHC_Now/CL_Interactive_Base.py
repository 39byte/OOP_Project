import pygame
from abc import abstractmethod
from CL_Base import Base

class ClickableBase(Base):
    """
    Base를 상속받되, 'Normal/Hover/Active' 상태 관리가 추가된
    모든 버튼류의 새로운 부모 클래스
    """
    STATE_NORMAL = 'normal'
    STATE_HOVER = 'hover'
    STATE_ACTIVE = 'active'

    def __init__(self, window, loc, scale, align='topleft', callBack=None):
        # surface는 자식 클래스(Button, BaseButton)가 정의해야 함
        super().__init__(window, loc, scale, align) # 부모 Base의 __init__
        self.callBack = callBack
        self.state = self.STATE_NORMAL

    def handleEvent(self, eventObj):
        """
        Base 클래스의 추상 메서드를 덮어쓰기(Override)하여
        모든 클릭 가능 객체의 공통 이벤트 로직을 구현합니다.
        """
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
        """
        콜백을 실행하는 방식이 자식마다 다름
        (DifficultyButton: 인자 없음, BaseButton: self.text 인자 전달)
        """
        pass

    @abstractmethod
    def draw(self):
        """
        그리는 방식도 자식마다 다름 (이미지 vs 사각형)
        따라서 자식이 무조건 덮어쓰도록 다시 추상 메서드로 지정
        """
        pass