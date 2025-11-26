import pygame
import random
from abc import ABC, abstractmethod
from config import *
from ui_components import load_font
from collections import Counter
import time
from copy import deepcopy
from CL_Base import Base

# --- 1 & 2. 추상화(Abstraction) 및 상속(Inheritance) ---
class MenuItem(ABC):
    def __init__(self, name, price, recipe):
        self.name = name; self.price = price; self.recipe = recipe
    def get_price(self): return self.price
    @abstractmethod
    def get_recipe(self): pass

class Customer(Base):
    """모든 손님의 공통 부모 클래스"""
    def __init__(self, window, loc, wait_time, scale=80, align='center'):
        # 1. Customer 고유 속성 초기화
        self.wait_time = wait_time
        self.wait_timer = wait_time
        self.font = load_font(18)
        self.patience_factor = 1.0
        
        # 2. 부모(Base) 초기화 호출 (이미지 처리, rect 생성)
        super().__init__(window, loc, scale, align)

    @abstractmethod
    def order(self, menu_list): pass
    @abstractmethod
    def pay(self, total_price): pass

    def set_patience_factor(self, factor):
        self.patience_factor = factor

    def draw(self):
        super().draw() # Base의 draw (캐릭터 이미지)

        # 주문 내역 텍스트
        order_counts = Counter(item.name for item in self.order_list)
        order_str = " / ".join([f"{name} x{count}" for name, count in order_counts.items()])
        order_text = self.font.render(order_str, True, BLACK)
        order_rect = order_text.get_rect(centerx=self.rect.centerx, bottom=self.rect.top - 10)
        self.window.blit(order_text, order_rect)

        # 인내심 바
        wait_ratio = self.wait_timer / self.wait_time
        bar_width = self.rect.width
        if bar_width > 0:
            pygame.draw.rect(self.window, (200, 0, 0), (self.rect.x, self.rect.bottom + 10, bar_width, 10))
            pygame.draw.rect(self.window, (0, 200, 0), (self.rect.x, self.rect.bottom + 10, bar_width * wait_ratio, 10))

    def update(self, dt):
        self.wait_timer -= (dt * self.patience_factor)
        return self.wait_timer > 0
    
    def handleEvent(self, event):
        pass

class Hamburger(MenuItem):
    def __init__(self):
        super().__init__(name="햄버거", price=10, recipe=["빵", "양상추", "조리된 패티", "빵"].copy())
    def get_recipe(self): return self.recipe
class Cheeseburger(MenuItem):
    def __init__(self):
        super().__init__(name="치즈버거", price=13, recipe=["빵", "양상추", "조리된 패티", "치즈", "빵"].copy())
    def get_recipe(self): return self.recipe

# --- 자식 클래스들 (수정됨) ---
class NormalCustomer(Customer):
    def __init__(self, window, loc, wait_time):
        self.surface = pygame.image.load('assets/Char1.png')
        # 부모(Customer)의 __init__ 호출 -> Customer가 Base의 __init__ 호출
        super().__init__(window, loc, wait_time, scale=80, align='center')
        
    def order(self, menu_list):
        self.order_list = [deepcopy(random.choice(menu_list))]; return self.order_list
    def pay(self, total_price): return total_price

class VIPCustomer(Customer): 
    def __init__(self, window, loc, wait_time):
        self.surface = pygame.image.load('assets/Char2.png')
        super().__init__(window, loc, wait_time, scale=80, align='center')
        
    def order(self, menu_list):
        count = random.randint(1, 2)
        self.order_list = [deepcopy(random.choice(menu_list)) for _ in range(count)]
        return self.order_list
    def pay(self, total_price):
        tip_multiplier = random.uniform(1.3, 2.0)
        final_price = int(total_price * tip_multiplier)
        print(f"VIP 손님이 팁을 주었습니다! (총 ${final_price})")
        return final_price

class PickyCustomer(Customer):
    def __init__(self, window, loc, wait_time):
        self.surface = pygame.image.load('assets/Char1.png')
        super().__init__(window, loc, wait_time, scale=80, align='center')
        
    def order(self, menu_list):
        item = deepcopy(random.choice(menu_list))
        try:
            item.recipe.insert(-1, "조리된 패티")
            item.name += "+패티추가"
            item.price += 2
            print(f"까다로운 손님 주문: {item.name}")
        except Exception:
            item = deepcopy(random.choice(menu_list))
        self.order_list = [item]
        return self.order_list
    def pay(self, total_price): return total_price

# --- 4. 캡슐화 (Encapsulation) ---
class GrillStation:
    STATE_IDLE = "대기"
    STATE_COOKING = "조리중"
    STATE_OVERCOOKED = "오버쿡"
    STATE_BROKEN = "고장"

    def __init__(self, pos):
        self.state = self.STATE_IDLE; self.timer = 0.0; self.cook_time = 5.0 
        self.precision_window = 0.4; self.rect = pygame.Rect(pos[0], pos[1], 80, 80)
        self.font = load_font(16)
        self.is_broken = False
        
        try:
            self.image = pygame.image.load('assets/Grill.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 80))
        except pygame.error:
            print("그릴 이미지(assets/Grill.png)를 찾을 수 없어 기본 사각형을 사용합니다.")
            self.image = None
            
        self.broken_overlay = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.broken_overlay.fill((200, 0, 0, 100)) 

    def break_grill(self):
        print(f"[그릴] 고장 발생!")
        self.is_broken = True
        self.state = self.STATE_BROKEN
        self.timer = 0.0
    
    def fix_grill(self):
        print(f"[그릴] 수리 완료!")
        self.is_broken = False
        self.state = self.STATE_IDLE
        self.timer = 0.0

    def start_cook(self, stock_manager):
        if self.is_broken: 
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
        if self.is_broken: return "고장"
        
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
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, DARK_GRAY, self.rect) 

        text_to_show = self.state
        text_color = WHITE
        
        if self.state == self.STATE_BROKEN:
            screen.blit(self.broken_overlay, self.rect)
            text_to_show = self.state
            
        elif self.state == self.STATE_COOKING:
            text_to_show = f"{self.timer:.1f}초"
            bar_width = self.rect.width
            cook_ratio = self.timer / self.cook_time
            color = (0, 255 * (cook_ratio if cook_ratio < 1 else 1), 0)
            if (self.cook_time - self.precision_window / 2) <= self.timer <= (self.cook_time + self.precision_window / 2):
                color = (255, 255, 0)
            elif self.timer > (self.cook_time + self.precision_window / 2):
                color = RED; cook_ratio = 1.0; text_color = RED
            pygame.draw.rect(screen, color, (self.rect.x, self.rect.bottom + 5, bar_width * min(cook_ratio, 1), 10))
        
        elif self.state == self.STATE_OVERCOOKED:
            text_color = RED
        
        text = self.font.render(text_to_show, True, text_color)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery - 10))
        screen.blit(text, text_rect)

class FoodTruck:
    def __init__(self, stock_manager):
        self.stock = stock_manager; self.assembly_station = []; self.current_order_recipe = []
        self.font = load_font(18); self.rect = pygame.Rect(POPUP_ASSEMBLY_POS[0], POPUP_ASSEMBLY_POS[1], 150, 200)
        
        self.images = {}
        try:
            self.images["빵_아래"] = pygame.transform.scale(pygame.image.load('assets/BreadDown.png'), (100, 30))
            self.images["빵_위"] = pygame.transform.scale(pygame.image.load('assets/BreadUp.png'), (100, 40))
            self.images["패티"] = pygame.transform.scale(pygame.image.load('assets/Patty.png'), (90, 25))
            self.images["조리된 패티"] = self.images["패티"]
            self.images["치즈"] = pygame.transform.scale(pygame.image.load('assets/Cheese.png'), (95, 10))
            self.images["양상추"] = pygame.transform.scale(pygame.image.load('assets/Vegtable.png'), (95, 20))
        except pygame.error: pass

    def set_new_order(self, recipe):
        self.assembly_station = []; self.current_order_recipe = recipe
        print(f"[주문] 새 주문 받음: {self.current_order_recipe}")

    def add_to_assembly(self, ingredient_name):
        if ingredient_name == "패티": ingredient_name = "조리된 패티"
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
        
        start_x = self.rect.centerx
        current_y = self.rect.bottom - 20 
        
        for i, item_name in enumerate(self.assembly_station):
            image_to_draw = None
            
            if item_name == "빵":
                if i == len(self.current_order_recipe) - 1: 
                    image_to_draw = self.images.get("빵_위")
                else:
                    image_to_draw = self.images.get("빵_아래")
            else:
                image_to_draw = self.images.get(item_name)
            
            if image_to_draw:
                img_rect = image_to_draw.get_rect(midbottom=(start_x, current_y))
                screen.blit(image_to_draw, img_rect)
                current_y -= (img_rect.height * 0.7) 
            else:
                text = self.font.render(item_name, True, BLACK)
                text_rect = text.get_rect(midbottom=(start_x, current_y))
                screen.blit(text, text_rect)
                current_y -= 20