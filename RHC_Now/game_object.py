import pygame
import random
from abc import ABC, abstractmethod
from config import *        # 설정값 불러오기
from ui_components import load_font
from collections import Counter     # 주문내역 세는 용도
from copy import deepcopy           # 손님 주문 내역 복사
from CL_Base import Base            # 객체 생성의 기본 클래스

# ------ 메뉴 자체에 관한 클래스 ------
class MenuItem(ABC):
    def __init__(self, name, price, recipe):    # 메뉴 이름, 가격, 레시피
        self.name = name; self.price = price; self.recipe = recipe
    def get_price(self):
        return self.price      # 가격 반환

    @abstractmethod
    def get_recipe(self):
        pass                  # 레시피 반환

# 기본 버거 클래스
class Hamburger(MenuItem):
    def __init__(self):
        super().__init__(name="햄버거", price=10, recipe=["빵", "양상추", "조리된 패티", "빵"].copy())
    def get_recipe(self):
        return self.recipe

# 치즈 버거 클래스
class Cheeseburger(MenuItem):
    def __init__(self):
        super().__init__(name="치즈버거", price=13, recipe=["빵", "양상추", "조리된 패티", "치즈", "빵"].copy())
    def get_recipe(self):
        return self.recipe

# -------------------------------------------

# ------ 손님 클래스 ------
class Customer(Base):   # 손님들 공통 클래스
    def __init__(self, window, loc, wait_time, scale=80, align='center'):
        self.wait_time = wait_time      # 총 대기 시간
        self.wait_timer = wait_time     # 남은 대기 시간
        self.font = load_font(18)       # 주문 내역 표시용 폰트
        self.patience_factor = 1.0      # 인내심 배율 (이벤트용)
        
        # 이미지 처리, 히트박스 생성, 위치 정렬
        super().__init__(window, loc, scale, align)

    @abstractmethod
    def order(self, menu_list):
        pass    # 주문 받기 기능
    @abstractmethod
    def pay(self, total_price):
        pass    # 정산하기 기능

    # 이벤트에 의한 인내심 조절 기능
    def set_patience_factor(self, factor):
        self.patience_factor = factor

    def draw(self):
        super().draw() # Base의 draw (캐릭터 이미지)

        # 주문 내역 텍스트 표시 기능
        order_counts = Counter(item.name for item in self.order_list)   # 주문 목록 개수 세기 (Count 모듈 사용)
        order_str = " /\n ".join([f"{name} x{count}" for name, count in order_counts.items()])
        order_text = self.font.render(order_str, True, BLACK)
        # 그 텍스트 머리 위에 띄우기
        order_rect = order_text.get_rect(centerx=self.rect.centerx, bottom=self.rect.top - 10)
        self.window.blit(order_text, order_rect)

        # 인내심 바 표시 기능
        wait_ratio = self.wait_timer / self.wait_time   # 남은 시간 비율(1.0 ~ 0.0)
        bar_width = self.rect.width
        if bar_width > 0:
            # 빨간 배경(줄어드는 부분)
            pygame.draw.rect(self.window, (200, 0, 0), (self.rect.x, self.rect.bottom + 10, bar_width, 10))
            # 초록 배경(남은 부분)
            pygame.draw.rect(self.window, (0, 200, 0), (self.rect.x, self.rect.bottom + 10, bar_width * wait_ratio, 10))

    def update(self, dt):   # 시간(dt) 흐른 만큼 대기 시간 감소
        self.wait_timer -= (dt * self.patience_factor)  # 가속 배율 반영해서 감소시키기
        return self.wait_timer > 0      # 시간 남았는지(True) / 떠났는지(False)
    
    def handleEvent(self, event):   # 클릭 상호작용 따로 적용 X
        pass


# 일반 손님 클래스
class NormalCustomer(Customer):
    def __init__(self, window, loc, wait_time):
        self.surface = pygame.image.load('assets/Char1.png')
        # Customer 클래스 호출 -> Base 클래스 호출
        super().__init__(window, loc, wait_time, scale=80, align='center')
        
    def order(self, menu_list):         # 메뉴 리스트 중에 하나 골라 주문
        self.order_list = [deepcopy(random.choice(menu_list))]; return self.order_list
    
    def pay(self, total_price):
        return total_price      # 정가 지불

# VIP 손님 클래스
class VIPCustomer(Customer): 
    def __init__(self, window, loc, wait_time):
        self.surface = pygame.image.load('assets/Char2.png')
        super().__init__(window, loc, wait_time, scale=80, align='center')
        
    def order(self, menu_list):
        count = random.randint(1, 2)    # 1~2개 주문
        self.order_list = [deepcopy(random.choice(menu_list)) for _ in range(count)]
        return self.order_list
    
    def pay(self, total_price):
        tip_multiplier = random.uniform(1.3, 2.0)       # 팁 배율 (1.3 ~ 2.0)
        final_price = int(total_price * tip_multiplier) # 최종 지불 금액
        print(f"VIP 손님이 팁을 주었습니다! (총 ${final_price})")
        return final_price

# 요상한 손님 클래스
class PickyCustomer(Customer):
    def __init__(self, window, loc, wait_time):
        self.surface = pygame.image.load('assets/Char1.png')
        super().__init__(window, loc, wait_time, scale=80, align='center')
        
    def order(self, menu_list):
        item = deepcopy(random.choice(menu_list))   # 메뉴 선택
        try:    # 패티 아래에 패티 한 장 더 깔아달라고 부탁
            item.recipe.insert(-1, "조리된 패티")
            item.name += "\n+패티추가"
            item.price += 2
            print(f"까다로운 손님 주문: {item.name}")
        except Exception:
            item = deepcopy(random.choice(menu_list))   # 예외 발생시 그냥 일반 주문으로 대체

        self.order_list = [item]
        return self.order_list
    
    def pay(self, total_price):
        return total_price      # 정가 지불

# -----------------------------------------

# ------ 그릴 ------
class GrillStation:
    STATE_IDLE = "대기"
    STATE_COOKING = "조리중"
    STATE_OVERCOOKED = "오버쿡"
    STATE_BROKEN = "고장"

    def __init__(self, pos):
        self.state = self.STATE_IDLE; self.timer = 0.0; self.cook_time = 5.0 
        # 성공 범위: 5.0초 +- 0.3초
        self.precision_window = 0.6
        self.rect = pygame.Rect(pos[0], pos[1], 80, 80)
        self.font = load_font(16)
        self.is_broken = False      # 고장 여부
        
        # 그릴 이미지 로드
        try:
            self.image = pygame.image.load('assets/Grill.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 80))
        except pygame.error:
            print("그릴 이미지(assets/Grill.png)를 찾을 수 없어 기본 사각형을 사용합니다.")
            self.image = None
            
        # 고장 났을 때 빨간색으로 오버레이
        self.broken_overlay = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.broken_overlay.fill((200, 0, 0, 100)) 

    # 그릴 고장 났을 때
    def break_grill(self):
        print(f"[그릴] 고장 발생!")
        self.is_broken = True
        self.state = self.STATE_BROKEN
        self.timer = 0.0
    
    # 그릴 고쳐졌을 때
    def fix_grill(self):
        print(f"[그릴] 수리 완료!")
        self.is_broken = False
        self.state = self.STATE_IDLE
        self.timer = 0.0

    # 그릴 조리 시작했을 때
    def start_cook(self, stock_manager):
        if self.is_broken: 
            print("[그릴] 고장나서 사용할 수 없습니다.")
            return False
        
        if self.state == self.STATE_IDLE:
            if stock_manager.use_raw_patty():   # 날패티 사용하기
                self.state = self.STATE_COOKING; self.timer = 0.0
                print("[그릴] 패티 굽기 시작..."); return True
        print("[그릴] 이미 사용 중이거나 날패티 재고가 없습니다.")
        return False
    
    # 시간 업데이트
    def update(self, dt):
        if self.state == self.STATE_COOKING:
            self.timer += dt
            # 오버쿡 여부 체크
            if self.timer > (self.cook_time + self.precision_window / 2):
                self.state = self.STATE_OVERCOOKED
                print(f"[그릴] 패티가 탔습니다! ({self.timer:.2f}초)")

    # 클릭시 결과 판정
    def get_click_result(self, stock_manager):
        if self.is_broken:
            return "고장"
        
        if self.state == self.STATE_OVERCOOKED:     # 탔을 때
             print("[그릴] 클릭: 이미 탔습니다. (패널티)"); 
             
             self.state = self.STATE_IDLE; 
             self.timer = 0.0
             if stock_manager.add_penalty() == "GAME_OVER":
                 return "게임오버"
             return "오버쿡"
        if self.state != self.STATE_COOKING:    # 
            print("[그릴] 클릭: 그릴이 비어있습니다.")
            return "빈그릴"
        
        # 굽기 성공 조건 경계
        lower_bound = (self.cook_time - self.precision_window / 2)      # 4.7초
        upper_bound = (self.cook_time + self.precision_window / 2)      # 5.3초

        if  lower_bound <= self.timer <= upper_bound:       # 성공시 조리된 패티 추가
            print("[그릴] 5초 정밀 굽기 성공!"); 
            self.state = self.STATE_IDLE; 
            self.timer = 0.0

            stock_manager.add_cooked_patty()
            return "성공"     
        else:       # 실패시 오버쿡 추가
            result = "언더쿡"; print(f"[그릴] 굽기 실패! ({result}: {self.timer:.2f}초)")
            self.state = self.STATE_IDLE; 
            self.timer = 0.0

            if stock_manager.add_penalty() == "GAME_OVER": return "게임오버"
            return "실패"

    # 그릴 이미지 화면에 표시
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

# -------------------------------------------------------------

# ----------------------- 푸드 트럭 클래스 --------------------------------
class FoodTruck:
    def __init__(self, stock_manager):
        self.stock = stock_manager          # 재고 객체 참조
        self.assembly_station = []          # 현재 조립 중인 재료 리스트
        self.current_order_recipe = []      # 현재 만들어야 할 목표 레시피 리스트
        self.font = load_font(18); self.rect = pygame.Rect(POPUP_ASSEMBLY_POS[0], POPUP_ASSEMBLY_POS[1], 150, 200)
        
        # 재료 이미지 로드 및 크기 조정
        self.images = {}
        try:
            self.images["빵_아래"] = pygame.transform.scale(pygame.image.load('assets/BreadDown.png'), (100, 50))
            self.images["빵_위"] = pygame.transform.scale(pygame.image.load('assets/BreadUp.png'), (100, 60))
            self.images["패티"] = pygame.transform.scale(pygame.image.load('assets/Patty.png'), (90, 40))
            self.images["조리된 패티"] = self.images["패티"]
            self.images["치즈"] = pygame.transform.scale(pygame.image.load('assets/Cheese.png'), (95, 30))
            self.images["양상추"] = pygame.transform.scale(pygame.image.load('assets/Vegtable.png'), (95, 40))
        except pygame.error: pass

    # 새 주문 받았을 때
    def set_new_order(self, recipe):
        self.assembly_station = []
        self.current_order_recipe = recipe
        print(f"[주문] 새 주문 받음: {self.current_order_recipe}")

    # 재료를 조립대에 추가
    def add_to_assembly(self, ingredient_name):
        if len(self.assembly_station) >= 10:
            print("더 이상 쌓을 수 없습니다! (최대 10개)")
            return "가득참"
        
        if ingredient_name == "패티": ingredient_name = "조리된 패티"       # 버튼 이름 통일

        # 재고 관리자한테 재고 요청
        if not self.stock.use_ingredient(ingredient_name):  # 없으면 (False)
            print(f"Error: {ingredient_name} 재고 부족!")
            return "재고없음"

        self.assembly_station.append(ingredient_name)
        current_len = len(self.assembly_station)
        
        # 순서 검사(레시피대로 쌓았는가?)
        #if self.assembly_station != self.current_order_recipe[:current_len]:
         #   print(f"조리 순서 오류! 재료 손실")
          #  self.assembly_station = []      # 실패시 쌓은 거 초기화
           # self.stock.add_penalty()        # 패널티 추가
            #return "순서틀림"
        
        if self.assembly_station == self.current_order_recipe:
            print("버거 완성!")
            return "완성"
        
        return "조리중"

    # 조립대 초기화 기능 (쓰레기통)
    def clear_assembly(self):
        print("[조립] 조립대를 비우고 재료를 버립니다."); self.assembly_station = []
        
    # 조립대 쌓아올리는 거 시각화
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect) 
        
        start_x = self.rect.centerx
        current_y = self.rect.bottom - 10   # 시작 위치
        
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
                current_y -= (img_rect.height * 0.7) # 재료 사이 빈공간 조정 
            else:
                text = self.font.render(item_name, True, BLACK)
                text_rect = text.get_rect(midbottom=(start_x, current_y))
                screen.blit(text, text_rect)
                current_y -= 70