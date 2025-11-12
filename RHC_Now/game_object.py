# game_objects.py
import pygame
import random
from abc import ABC, abstractmethod
from config import *
from ui_components import load_font
from collections import Counter
import time
from copy import deepcopy
# --- 1 & 2. 추상화(Abstraction) 및 상속(Inheritance) ---
class MenuItem(ABC):
    # ... (이전과 동일) ...
    def __init__(self, name, price, recipe):
        self.name = name; self.price = price; self.recipe = recipe
    def get_price(self): return self.price
    @abstractmethod
    def get_recipe(self): pass

class Customer(ABC):
    # ... (이전과 동일) ...
    def __init__(self, wait_time):
        self.wait_time = wait_time; self.order_list = []; self.wait_timer = wait_time
        self.font = load_font(18); self.face_color = (255, 220, 180)
        self.patience_factor = 1.0  # (추가) 인내심 배율 (연예인 이벤트용)

    @abstractmethod
    def order(self, menu_list): pass
    @abstractmethod
    def pay(self, total_price): pass

    def set_patience_factor(self, factor):
        self.patience_factor = factor

    def draw(self, screen, pos):
        pygame.draw.circle(screen, self.face_color, pos, 30)
        order_counts = Counter(item.name for item in self.order_list)
        order_str = " / ".join([f"{name} x{count}" for name, count in order_counts.items()])
        order_text = self.font.render(order_str, True, BLACK)
        order_rect = order_text.get_rect(center=(pos[0], pos[1] - 40))
        screen.blit(order_text, order_rect)
        wait_ratio = self.wait_timer / self.wait_time
        bar_width = 80 * wait_ratio
        if bar_width > 0:
            pygame.draw.rect(screen, (200,0,0), (pos[0]-40, pos[1] + 40, 80, 5))
            pygame.draw.rect(screen, (0,200,0), (pos[0]-40, pos[1] + 40, bar_width, 5))
    def update(self, dt):
        self.wait_timer -= (dt * self.patience_factor)
        return self.wait_timer > 0

class Hamburger(MenuItem):
    def __init__(self):
        super().__init__(name="햄버거", price=10, recipe=["빵", "양상추", "조리된 패티", "빵"].copy())
    def get_recipe(self): return self.recipe
class Cheeseburger(MenuItem):
    def __init__(self):
        super().__init__(name="치즈버거", price=13, recipe=["빵", "양상추", "조리된 패티", "치즈", "빵"].copy())
    def get_recipe(self): return self.recipe

class NormalCustomer(Customer):
    def order(self, menu_list):
        self.order_list = [deepcopy(random.choice(menu_list))]; return self.order_list
    def pay(self, total_price): return total_price
class VIPCustomer(Customer): 
    def __init__(self, wait_time):
        super().__init__(wait_time); self.face_color = (255, 215, 0)
    def order(self, menu_list):
        count = random.randint(1, 2)
        self.order_list = [deepcopy(random.choice(menu_list)) for _ in range(count)]
        return self.order_list
    def pay(self, total_price):
        tip_multiplier = random.uniform(1.3, 2.0)
        final_price = int(total_price * tip_multiplier)
        print(f"VIP 손님이 {tip_multiplier:.2f}배 팁을 주었습니다! (총 ${final_price})")
        return final_price
class PickyCustomer(Customer):
    """
    상속(Inheritance)을 이용한 새로운 손님.
    기존 메뉴(햄버거/치즈버거)에 패티를 1장 더 추가해서 주문합니다.
    """
    def __init__(self, wait_time):
        super().__init__(wait_time); self.face_color = (150, 150, 255) # 파란색 얼굴

    def order(self, menu_list):
        # (수정) deepcopy로 아이템 복제
        item = deepcopy(random.choice(menu_list))
        
        # 메서드 오버라이딩: 주문(recipe)을 수정합니다.
        # 맨 위 빵("빵") 바로 아래에 "조리된 패티"를 추가
        try:
            item.recipe.insert(-1, "조리된 패티")
            item.name += "+패티추가" # 이름 변경
            item.price += 2 # 패티 추가 가격
            print(f"까다로운 손님 주문: {item.name}")
        except Exception as e:
            print(f"패티 추가 중 오류: {e}") # 기본 아이템으로 대체
            item = deepcopy(random.choice(menu_list))

        self.order_list = [item]
        return self.order_list
        
    def pay(self, total_price):
        return total_price # 팁은 없음
# --- 4. 캡슐화 (Encapsulation) ---
class GrillStation:
    # ... (이전과 동일) ...
    STATE_IDLE = "그릴"
    STATE_COOKING = "조리중"
    STATE_OVERCOOKED = "오버쿡"
    STATE_BROKEN = "고장"

    def __init__(self, pos):
        self.state = self.STATE_IDLE; self.timer = 0.0; self.cook_time = 5.0 
        self.precision_window = 0.4; self.rect = pygame.Rect(pos[0], pos[1], 80, 80)
        self.font = load_font(16)
        self.is_broken = False # (추가) 고장 상태 플래그

    # (추가) 이벤트용 메서드
    def break_grill(self):
        print(f"[그릴] 고장 발생!")
        self.is_broken = True
        self.state = self.STATE_BROKEN
        self.timer = 0.0
    
    # (추가) 이벤트용 메서드
    def fix_grill(self):
        print(f"[그릴] 수리 완료!")
        self.is_broken = False
        self.state = self.STATE_IDLE
        self.timer = 0.0

    def start_cook(self, stock_manager):
        if self.is_broken: # (추가) 고장 시 작동 불가
            print("[그릴] 고장나서 사용할 수 없습니다.")
            return False
        
        if self.state == self.STATE_IDLE:
            if stock_manager.use_raw_patty(): 
                self.state = self.STATE_COOKING; self.timer = 0.0
                print("[그릴] 패티 굽기 시작..."); return True
        print("[그릴] 이미 사용 중이거나 날패티 재고가 없습니다."); return False
    
    def update(self, dt):
        if self.state == self.STATE_COOKING:
            self.timer += dt
            if self.timer > (self.cook_time + self.precision_window / 2):
                self.state = self.STATE_OVERCOOKED
                print(f"[그릴] 패티가 탔습니다! ({self.timer:.2f}초)")

    def get_click_result(self, stock_manager):
        if self.is_broken: # (추가) 고장 시 작동 불가
            print("[그릴] 고장나서 사용할 수 없습니다.")
            return "고장"
        
        if self.state == self.STATE_OVERCOOKED:
             print("[그릴] 클릭: 이미 탔습니다. (패널티)"); self.state = self.STATE_IDLE; self.timer = 0.0
             if stock_manager.add_penalty() == "GAME_OVER": return "게임오버"
             return "오버쿡"
        if self.state != self.STATE_COOKING:
            print("[그릴] 클릭: 그릴이 비어있습니다."); return "빈그릴"
        if (self.cook_time - self.precision_window / 2) <= self.timer <= (self.cook_time + self.precision_window / 2):
            print("[그릴] 5초 정밀 굽기 성공!"); self.state = self.STATE_IDLE; self.timer = 0.0
            stock_manager.add_cooked_patty(); return "성공"
        else:
            result = "언더쿡"; print(f"[그릴] 굽기 실패! ({result}: {self.timer:.2f}초)")
            self.state = self.STATE_IDLE; self.timer = 0.0
            if stock_manager.add_penalty() == "GAME_OVER": return "게임오버"
            return "실패"
    def draw(self, screen):
        # (***수정됨***) 그릴 버튼과 겹치지 않도록 타이머/상태 텍스트 위치 조정
        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        text_to_show = self.state
        text_color = WHITE
        if self.state == self.STATE_BROKEN:
            pygame.draw.rect(screen, (100, 0, 0), self.rect) # 어두운 빨간색
            text_color = WHITE
            text_to_show = self.state
        
        # 2. 고장이 아닐 때 (기존 로직)
        else:
            pygame.draw.rect(screen, DARK_GRAY, self.rect)
            text_to_show = self.state
            text_color = WHITE
            
            if self.state == self.STATE_COOKING:
                text_to_show = f"{self.timer:.1f}초"
                # 타이밍 바
                bar_width = self.rect.width
                cook_ratio = self.timer / self.cook_time
                color = (0, 255 * (cook_ratio if cook_ratio < 1 else 1), 0)
                if (self.cook_time - self.precision_window / 2) <= self.timer <= (self.cook_time + self.precision_window / 2):
                    color = (255, 255, 0)
                elif self.timer > (self.cook_time + self.precision_window / 2):
                    color = RED; cook_ratio = 1.0; text_color = RED
                pygame.draw.rect(screen, color, (self.rect.x, self.rect.bottom - 10, bar_width * min(cook_ratio, 1), 10))
            
            elif self.state == self.STATE_OVERCOOKED:
                text_color = RED
            
        text = self.font.render(text_to_show, True, text_color)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery - 10)) # 텍스트를 위로 올림
        screen.blit(text, text_rect)

class FoodTruck:
    """조립대 로직을 캡슐화 (팝업창 역할)"""
    def __init__(self, stock_manager):
        self.stock = stock_manager; self.assembly_station = []; self.current_order_recipe = []
        self.font = load_font(18); self.rect = pygame.Rect(POPUP_ASSEMBLY_POS[0], POPUP_ASSEMBLY_POS[1], 150, 200)

    def set_new_order(self, recipe):
        self.assembly_station = []; self.current_order_recipe = recipe
        print(f"[주문] 새 주문 받음: {self.current_order_recipe}")

    def add_to_assembly(self, ingredient_name):
        if ingredient_name == "패티":
             ingredient_name = "조리된 패티"
        if not self.stock.use_ingredient(ingredient_name): 
            print(f"Error: {ingredient_name} 재고 부족!"); return "재고없음"

        self.assembly_station.append(ingredient_name)
        current_len = len(self.assembly_station)
        
        if self.assembly_station != self.current_order_recipe[:current_len]:
            print(f"조리 순서 오류! 재료 손실"); self.assembly_station = []
            self.stock.add_penalty(); return "순서틀림"
        
        if self.assembly_station == self.current_order_recipe:
            print("버거 완성!"); return "완성"
        return "조리중"

    def clear_assembly(self):
        print("[조립] 조립대를 비우고 재료를 버립니다."); self.assembly_station = []
        
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)
        y_stack = self.rect.bottom - 10
        for item_name in reversed(self.assembly_station):
             text = self.font.render(item_name, True, BLACK)
             text_rect = text.get_rect(centerx=self.rect.centerx, bottom=y_stack)
             screen.blit(text, text_rect)
             y_stack -= 20