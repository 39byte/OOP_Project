import pygame
import random
from abc import ABC, abstractmethod
from ui_components import SimpleText
from config import * # 설정값 임포트

# 1. 모든 이벤트의 부모가 될 추상 클래스 (OOP 7강)
class GameEvent(ABC):
    def __init__(self, duration, message):
        self.duration = duration # 이벤트 지속시간
        self.message = message   # 화면에 표시할 메시지
        self.timer = 0.0         # 이벤트 경과 시간
        self.is_active = False
        
        # 이벤트 메시지 UI (공통)
        self.msg_text = SimpleText(
            window=None, 
            loc=(WINDOW_WIDTH // 2, 20), 
            text=self.message, 
            size=28, 
            color=RED, 
            align='center'
        )

    # 2. 이벤트 시작 시 1회 호출
    def activate(self, game):
        print(f"[이벤트] {self.message} 시작!")
        self.is_active = True
        self.timer = 0.0
        self.msg_text.window = game.window # window 객체 연결

    # 3. 이벤트가 활성화된 동안 매 프레임 호출 (다형성)
    def update(self, dt, game):
        if not self.is_active:
            return False
            
        self.timer += dt
        if self.timer >= self.duration:
            self.is_active = False
            self.deactivate(game) # 지속시간이 끝나면 비활성화
            print(f"[이벤트] {self.message} 종료.")
            return False
        
        self.apply_effect(dt, game) # 이벤트 효과 적용
        return True

    # 4. 이벤트 종료 시 1회 호출
    def deactivate(self, game):
        self.is_active = False

    # 5. 자식 클래스가 반드시 오버라이딩해야 하는 메서드 (OOP 6강)
    @abstractmethod
    def apply_effect(self, dt, game):
        """이벤트의 실제 효과 (매 프레임 적용)"""
        pass

    # 6. 화면에 메시지 그리기 (공통)
    def draw(self, window):
        if self.is_active:
            self.msg_text.draw()

# --- 1. 화로 먹통 이벤트 ---
class BrokenGrillEvent(GameEvent):
    def __init__(self):
        super().__init__(duration=5.0, message="화로 1개 고장! (5초)")
        self.broken_grill_index = -1

    def activate(self, game):
        super().activate(game)
        # 사용 가능한 그릴 중 하나를 무작위로 고장냄
        available_grills = [i for i, grill in enumerate(game.grills) if not grill.is_broken]
        if available_grills:
            self.broken_grill_index = random.choice(available_grills)
            game.grills[self.broken_grill_index].break_grill()
        else:
            self.is_active = False # 고장낼 그릴이 없음

    def apply_effect(self, dt, game):
        # 이 이벤트는 activate/deactivate에서 모든 로직이 처리됨
        pass 

    def deactivate(self, game):
        super().deactivate(game)
        if 0 <= self.broken_grill_index < len(game.grills):
            game.grills[self.broken_grill_index].fix_grill()

# --- 2. 재고 딜레이 이벤트 ---
class StockDelayEvent(GameEvent):
    def __init__(self):
        self.delay_time = random.uniform(3.0, 5.0)
        super().__init__(duration=15.0, message=f"재고 배송 딜레이! ({self.delay_time:.1f}초)")

    def activate(self, game):
        super().activate(game)
        game.player_stock.set_stock_delay(self.delay_time)

    def apply_effect(self, dt, game):
        pass # Stock 객체가 스스로 update()에서 처리함

    def deactivate(self, game):
        super().deactivate(game)
        game.player_stock.set_stock_delay(0.0) # 딜레이 원상복구

# --- 3. 연예인 등장 이벤트 ---
class CelebrityEvent(GameEvent):
    def __init__(self):
        self.duration = random.uniform(10.0, 15.0) # 이벤트 지속 시간
        self.patience_factor = random.uniform(1.1, 1.3) # 10%~30% 더 빠름
        super().__init__(self.duration, message=f"연예인 등장! 손님 대기시간 {int((self.patience_factor-1)*100)}% 단축!")

    def activate(self, game):
        super().activate(game)
        # (다형성) 모든 Customer 객체의 set_patience_factor를 호출
        for customer in game.customers:
            if customer:
                customer.set_patience_factor(self.patience_factor)

    def apply_effect(self, dt, game):
        # (참고) 이 효과는 Customer 객체가 스스로 update()에서 처리함
        # 만약 새로 스폰되는 손님에게도 적용하려면 GameClient의 스폰 로직 수정 필요
        pass

    def deactivate(self, game):
        super().deactivate(game)
        # (다형성) 모든 Customer 객체의 인내심 배율을 1.0으로 복구
        for customer in game.customers:
            if customer:
                customer.set_patience_factor(1.0)