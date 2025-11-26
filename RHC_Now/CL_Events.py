# CL_Events.py
import pygame
import random
from abc import ABC, abstractmethod
from ui_components import SimpleText
from config import * 
class GameEvent(ABC):
    def __init__(self, duration, message):
        self.duration = duration
        self.message = message
        self.timer = 0.0
        self.is_active = False
        # (수정) 위치 왼쪽 상단, 왼쪽 정렬
        self.msg_text = SimpleText(None, (30, 20), text=self.message, size=28, color=RED, align='left')

    def activate(self, game):
        print(f"[이벤트] {self.message} 시작!")
        self.is_active = True
        self.timer = 0.0
        self.msg_text.window = game.window

    def update(self, dt, game):
        if not self.is_active: return False
        self.timer += dt
        if self.timer >= self.duration:
            self.is_active = False
            self.deactivate(game)
            print(f"[이벤트] {self.message} 종료.")
            return False
        self.apply_effect(dt, game)
        return True

    def deactivate(self, game): self.is_active = False
    @abstractmethod
    def apply_effect(self, dt, game): pass
    def draw(self, window):
        if self.is_active: self.msg_text.draw()

class BrokenGrillEvent(GameEvent):
    def __init__(self):
        super().__init__(duration=5.0, message="화로 1개 고장! (5초)")
        self.broken_grill_index = -1
    def activate(self, game):
        super().activate(game)
        available_grills = [i for i, grill in enumerate(game.grills) if not grill.is_broken]
        if available_grills:
            self.broken_grill_index = random.choice(available_grills)
            game.grills[self.broken_grill_index].break_grill()
        else: self.is_active = False
    def apply_effect(self, dt, game): pass 
    def deactivate(self, game):
        super().deactivate(game)
        if 0 <= self.broken_grill_index < len(game.grills):
            game.grills[self.broken_grill_index].fix_grill()

class StockDelayEvent(GameEvent):
    def __init__(self):
        self.delay_time = random.uniform(3.0, 5.0)
        super().__init__(duration=15.0, message=f"재고 배송 딜레이! ({self.delay_time:.1f}초)")
    def activate(self, game):
        super().activate(game)
        game.player_stock.set_stock_delay(self.delay_time)
    def apply_effect(self, dt, game): pass
    def deactivate(self, game):
        super().deactivate(game)
        game.player_stock.set_stock_delay(0.0)

class CelebrityEvent(GameEvent):
    def __init__(self):
        self.duration = random.uniform(10.0, 15.0)
        self.patience_factor = random.uniform(1.1, 1.3) 
        super().__init__(self.duration, message=f"연예인 등장! 손님 대기시간 {int((self.patience_factor-1)*100)}% 단축!")
    def activate(self, game):
        super().activate(game)
        for customer in game.customers:
            if customer: customer.set_patience_factor(self.patience_factor)
    def apply_effect(self, dt, game): pass
    def deactivate(self, game):
        super().deactivate(game)
        for customer in game.customers:
            if customer: customer.set_patience_factor(1.0)