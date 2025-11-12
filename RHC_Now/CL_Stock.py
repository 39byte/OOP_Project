# CL_Stock.py (수정된 버전)
import time

class Stock():
    # ... (__init__, getter, add_money, remove_money 메서드는 동일) ...
    def __init__(self, money=100, patty=10, bun=10, lettuce=10, cheese=10):
        self.__money = money
        self._ingredients = {
            "패티": patty, # 날고기
            "빵": bun, # 빵
            "양상추": lettuce,
            "치즈": cheese,
            "조리된 패티": 0 # 조리 완료 재고
        }
        self._overcook_count = 0
        self._overcook_limit = 5
        self.stock_delay_duration = 0.0 # 딜레이 시간 (0이면 즉시)
        self.delayed_stock_queue = [] # (재료, 도착시간) 튜플 리스트

    @property
    def money(self): return self.__money
    @property
    def overcook_count(self): return self._overcook_count
    @property
    def overcook_limit(self): return self._overcook_limit

    def set_stock_delay(self, duration):
        self.stock_delay_duration = duration

    # (추가) GameClient의 update 루프에서 호출될 메서드
    def update(self, dt):
        """딜레이 중인 재고가 있는지 확인하고, 시간이 되면 추가합니다."""
        if not self.delayed_stock_queue:
            return

        current_time = time.time()
        # 큐의 맨 앞 아이템 확인 (도착 시간이 되었는지)
        # (참고: 큐가 매우 길어지면 비효율적이므로, 여기선 간단히 구현)
        
        # 도착한 아이템들을 실제 재고에 추가
        remaining_items = []
        added_count = 0
        for item_name, arrival_time in self.delayed_stock_queue:
            if current_time >= arrival_time:
                self._ingredients[item_name] += 1
                print(f"[재고] {item_name} 1개 배송 완료!")
                added_count += 1
            else:
                remaining_items.append((item_name, arrival_time))
        
        self.delayed_stock_queue = remaining_items

    def set_overcook_limit(self, limit):
        self._overcook_limit = limit

    def add_money(self, amount):
        if amount > 0: self.__money += amount
    
    def remove_money(self, amount):
        if 0 < amount <= self.__money:
            self.__money -= amount; return True
        print("돈이 부족합니다."); return False

    # --- (!!!) 여기에 메서드 추가 (!!!) ---
    def add_ingredient(self, ingredient_name, amount):
        """(v6) 재료를 이름으로 찾아 안전하게 추가하는 메서드 (캡슐화)"""
        if amount <= 0: return
        
        if ingredient_name not in self._ingredients:
            print(f"Error: {ingredient_name}는 존재하지 않는 재료입니다.")
            return

        # (수정) 재고 딜레이가 활성화되었는지 확인
        if self.stock_delay_duration > 0:
            for _ in range(amount):
                arrival_time = time.time() + self.stock_delay_duration
                self.delayed_stock_queue.append((ingredient_name, arrival_time))
            print(f"[재고] {ingredient_name} {amount}개 주문. ({self.stock_delay_duration:.1f}초 후 도착)")
        else:
            # 딜레이가 없으면 즉시 추가 (기존 로직)
            self._ingredients[ingredient_name] += amount
            print(f"[재고] {ingredient_name} {amount}개 추가.")
    # ------------------------------------

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

    def use_raw_patty(self):
        if self.has_ingredient("패티"):
            self._ingredients["패티"] -= 1
            print(f"[재고] 날패티 사용. (남은 수량: {self._ingredients['패티']})")
            return True
        print("Error: 날패티 재고 부족!"); return False

    def add_cooked_patty(self):
        self._ingredients["조리된 패티"] += 1
        print(f"[재고] 조리된 패티 1개 추가. (현재: {self._ingredients['조리된 패티']})")

    def get_stock_status(self):
        return self._ingredients

    def add_penalty(self):
        self._overcook_count += 1
        print(f"[패널티] 조리 실패/손님 이탈! (누적: {self._overcook_count}/{self._overcook_limit})")
        if self._overcook_count >= self._overcook_limit:
            return "GAME_OVER"
        return "WARNING"