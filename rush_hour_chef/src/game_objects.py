# game_objects.py
import random
from abc import ABC, abstractmethod

# --- 1. 추상화 (Abstraction) ---
class MenuItem(ABC):
    def __init__(self, name, price, recipe, cook_time=0):
        self.name = name
        self.price = price
        self.recipe = recipe
        self.cook_time = cook_time
    def get_price(self):
        return self.price
    @abstractmethod
    def get_recipe(self):
        pass

class Customer(ABC):
    def __init__(self, wait_time):
        self.wait_time = wait_time
        self.order_list = []
        self.wait_timer = wait_time
    @abstractmethod
    def order(self, menu_list):
        pass
    @abstractmethod
    def pay(self, total_price):
        pass

# --- 2. 상속 (Inheritance) ---
class Hamburger(MenuItem):
    def __init__(self):
        super().__init__(
            name="햄버거", price=5,
            recipe=["빵(아래)", "양상추", "패티", "빵(위)"],
            cook_time=5
        )
    def get_recipe(self):
        return self.recipe

class Cheeseburger(MenuItem):
    def __init__(self):
        super().__init__(
            name="치즈버거", price=6,
            recipe=["빵(아래)", "양상추", "패티", "치즈", "빵(위)"],
            cook_time=5
        )
    def get_recipe(self):
        return self.recipe

class NormalCustomer(Customer):
    def order(self, menu_list):
        self.order_list = [random.choice(menu_list)]
        return self.order_list
    def pay(self, total_price):
        print(f"일반 손님: {total_price}$ 지불")
        return total_price

class VIPCustomer(Customer):
    def order(self, menu_list):
        self.order_list = [random.choice(menu_list), random.choice(menu_list)]
        return self.order_list
    def pay(self, total_price):
        tip = random.randint(3, 10)
        print(f"VIP 손님: {total_price}$ + 팁 {tip}$ 지불")
        return total_price + tip

# --- 4. 캡슐화 (Encapsulation) & 버그 방지 ---
class FoodTruck:
    STATE_IDLE = "대기"
    STATE_COOKING = "조리중"
    STATE_COOKED = "조리완료"
    STATE_OVERCOOKED = "오버쿡"

    def __init__(self, difficulty_settings):
        # *** 수정됨: 초기 자본 300 -> 100 ***
        self.__money = 100 # (private) 자본금 (300이면 easy가 바로 성공)
        
        self._ingredients = {"빵(아래)": 15, "빵(위)": 15, "패티": 10, "치즈": 10, "양상추": 10}
        self._overcook_count = 0
        self._overcook_limit = difficulty_settings['overcook_limit']
        
        self.grill_state = self.STATE_IDLE
        self.grill_timer = 0.0
        self.patty_cook_time = 5.0
        self.patty_overcook_time = 8.0 

        self.assembly_station = []
        self.current_order_recipe = []

    # --- 돈 관련 (Private) ---
    def earn(self, amount):
        if amount > 0:
            self.__money += amount
    
    @property
    def money(self):
        return self.__money

    # --- 재고 관련 (Protected) ---
    def has_ingredient(self, name):
        return self._ingredients.get(name, 0) > 0

    def use_ingredient(self, name):
        if self.has_ingredient(name):
            self._ingredients[name] -= 1
            print(f"[재고] {name} 사용. (남은 수량: {self._ingredients[name]})")
            return True
        else:
            print(f"Error: {name} 재고 부족!")
            return False

    def get_stock_status(self):
        return self._ingredients

    # --- 오버쿡 관련 (Protected) ---
    def add_overcook(self):
        self._overcook_count += 1
        print(f"[패널티] 오버쿡 발생! (누적: {self._overcook_count}/{self._overcook_limit})")
        if self._overcook_count >= self._overcook_limit:
            return "GAME_OVER"
        return "WARNING"
    
    @property
    def overcook_count(self):
        return self._overcook_count

    # --- 조리 로직 (캡슐화된 행동) ---
    def set_new_order(self, recipe):
        self.assembly_station = []
        self.current_order_recipe = recipe
        print(f"[주문] 새 주문 받음: {self.current_order_recipe}")

    def add_to_assembly(self, ingredient_name):
        if ingredient_name == "패티":
             if self.grill_state == self.STATE_COOKED:
                 print("[그릴] 잘 구워진 패티 획득!")
                 self.grill_state = self.STATE_IDLE
                 self.grill_timer = 0.0
                 # 패티는 재고 소모 없이 조립대에 추가
             else:
                 print("Error: 패티가 아직 조리되지 않았습니다!")
                 return "조리안됨"
        
        elif not self.use_ingredient(ingredient_name):
             return "재고없음"

        self.assembly_station.append(ingredient_name)
        
        # 순서 검증
        current_len = len(self.assembly_station)
        if self.assembly_station != self.current_order_recipe[:current_len]:
            print(f"조리 순서 오류! 재료 손실")
            self.assembly_station = []
            return "순서틀림"
        
        if self.assembly_station == self.current_order_recipe:
            print("버거 완성!")
            return "완성"
        
        return "조리중"

    def clear_assembly(self):
        print("[조립] 조립대를 비우고 재료를 버립니다. (재료 손실)")
        self.assembly_station = []

    def start_grill(self):
        if self.grill_state == self.STATE_IDLE:
            if self.use_ingredient("패티"):
                self.grill_state = self.STATE_COOKING
                self.grill_timer = 0.0
                print("[그릴] 패티 굽기 시작...")
                return True
        print("[그릴] 이미 굽고 있거나 재고가 없습니다.")
        return False

    def update_grill(self, dt):
        if self.grill_state == self.STATE_COOKING:
            self.grill_timer += dt
            if self.grill_timer > self.patty_overcook_time:
                self.grill_state = self.STATE_OVERCOOKED
                print("[그릴] 패티가 타버렸습니다!")
            elif self.grill_timer > self.patty_cook_time:
                self.grill_state = self.STATE_COOKED
                print("[그릴] 패티 조리 완료!")
                
    def get_patty_from_grill(self):
        """(v3 수정) 이 함수는 패티를 조립대로 옮기는 전용 함수가 됨"""
        if self.grill_state == self.STATE_COOKED:
            return self.add_to_assembly("패티") # add_to_assembly가 상태를 확인하도록
        
        elif self.grill_state == self.STATE_OVERCOOKED:
            print("[그릴] 탄 패티를 버렸습니다...")
            self.grill_state = self.STATE_IDLE
            self.grill_timer = 0.0
            if self.add_overcook() == "GAME_OVER":
                return "게임오버"
            return "오버쿡"
            
        elif self.grill_state == self.STATE_COOKING:
            print("[그릴] 아직 덜 익었습니다!")
            return "덜익음"
        
        print("[그릴] 그릴이 비어있습니다.")
        return "빈그릴"