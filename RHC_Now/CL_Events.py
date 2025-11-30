# CL_Events.py
import pygame
import random
from abc import ABC, abstractmethod
from ui_components import SimpleText
from config import * 

# 이벤트 지속 시간 계산 / 화면 출력 기능 담당 클래스
class GameEvent(ABC):
    def __init__(self, duration, message):
        self.duration = duration
        self.message = message
        self.timer = 0.0
        self.is_active = False
        # 메세지 표시 위치
        self.msg_text = SimpleText(None, (30, 20), text=self.message, size=28, color=RED, align='left')

    # 이벤트가 시작할 때
    def activate(self, game):
        print(f"[이벤트] {self.message} 시작!")

        self.is_active = True
        self.timer = 0.0
        self.msg_text.window = game.window

    def update(self, dt, game):     # dt : 흐른 시간 주입
        if not self.is_active: return False     # 이벤트 시작 안 했으면 작동 안 함
        self.timer += dt
        if self.timer >= self.duration:
            self.is_active = False
            self.deactivate(game)       # 지속 시간 초과하면 이벤트 종료
            print(f"[이벤트] {self.message} 종료.")
            return False
        self.apply_effect(dt, game)     # 즉발성이 아닌 지속적인 이벤트
        return True

    def deactivate(self, game): self.is_active = False      # 이벤트 종료 명령
    @abstractmethod
    def apply_effect(self, dt, game): pass
    def draw(self, window):
        if self.is_active: self.msg_text.draw()

# 화로 고장 이벤트
class BrokenGrillEvent(GameEvent):
    def __init__(self):
        super().__init__(duration=5.0, message="화로 1개 고장! (5초)")
        self.broken_grill_index = -1

    def activate(self, game):
        super().activate(game)
        # 정상 그릴 탐색
        available_grills = [i for i, grill in enumerate(game.grills) if not grill.is_broken]
        if available_grills:    # 정상 있다면 그거 뿌시기
            self.broken_grill_index = random.choice(available_grills)
            game.grills[self.broken_grill_index].break_grill()
        else: self.is_active = False

    def apply_effect(self, dt, game): pass  # 즉발성이기 때문에 함수 정의 X

    def deactivate(self, game):     # 이벤트 끝나면 고장난 화로 정상화
        super().deactivate(game)
        if 0 <= self.broken_grill_index < len(game.grills):
            game.grills[self.broken_grill_index].fix_grill()

# 재고 보충 딜레이 이벤트
class StockDelayEvent(GameEvent):
    def __init__(self):
        self.delay_time = random.uniform(3.0, 5.0)
        super().__init__(duration=15.0, message=f"재고 배송 딜레이! ({self.delay_time:.1f}초)")

    def activate(self, game):
        super().activate(game)
        game.player_stock.set_stock_delay(self.delay_time)      # 재고 보충 딜레이 명령

    def apply_effect(self, dt, game): pass
    def deactivate(self, game):
        super().deactivate(game)
        game.player_stock.set_stock_delay(0.0)      # 재고 보충 딜레이 정상화

# 연예인 등장 이벤트
class CelebrityEvent(GameEvent):
    def __init__(self):
        self.duration = random.uniform(10.0, 15.0)
        self.patience_factor = random.uniform(1.1, 1.3) 
        super().__init__(self.duration, message=f"연예인 등장! 손님 대기시간 {int((self.patience_factor-1)*100)}% 단축!")

    def activate(self, game):
        super().activate(game)
        for customer in game.customers:
            if customer: customer.set_patience_factor(self.patience_factor)     # 인내심 수치 조절

    def apply_effect(self, dt, game): pass
    def deactivate(self, game):
        super().deactivate(game)
        for customer in game.customers:
            if customer: customer.set_patience_factor(1.0)      # 인내심 수치 정상화