import time

class Stock():
    def __init__(self, money=100, patty=10, bun=10, lettuce=10, cheese=10):
        self.__money = money
        # 대시보드 표시 순서 (빵->치즈->양상추->패티->조리된)
        self._ingredients = {
            "빵": bun,
            "치즈": cheese,
            "양상추": lettuce,
            "패티": patty, 
            "조리된 패티": 0 
        }
        self._overcook_count = 0
        self._overcook_limit = 5
        self.stock_delay_duration = 0.0 
        self.delayed_stock_queue = [] 

    @property
    def money(self): return self.__money
    @property
    def overcook_count(self): return self._overcook_count
    @property
    def overcook_limit(self): return self._overcook_limit

    def set_stock_delay(self, duration):
        self.stock_delay_duration = duration

    def update(self, dt):
        """딜레이 중인 재고가 있는지 확인하고, 시간이 되면 추가합니다."""
        if not self.delayed_stock_queue: return
        
        current_time = time.time()
        remaining_items = []
        for item_name, arrival_time in self.delayed_stock_queue:
            if current_time >= arrival_time:
                self._ingredients[item_name] += 1
                print(f"[재고] {item_name} 1개 배송 완료!")
            else:
                remaining_items.append((item_name, arrival_time))
        self.delayed_stock_queue = remaining_items

    def set_overcook_limit(self, limit): self._overcook_limit = limit
    
    def add_money(self, amount): 
        if amount > 0: self.__money += amount
    
    def remove_money(self, amount):
        if 0 < amount <= self.__money:
            self.__money -= amount; return True
        print("돈이 부족합니다."); return False

    def add_ingredient(self, ingredient_name, amount):
        if amount <= 0: return
        if ingredient_name not in self._ingredients: return

        if self.stock_delay_duration > 0:
            for _ in range(amount):
                arrival_time = time.time() + self.stock_delay_duration
                self.delayed_stock_queue.append((ingredient_name, arrival_time))
            print(f"[재고] {ingredient_name} 주문 (딜레이).")
        else:
            self._ingredients[ingredient_name] += amount

    def has_ingredient(self, name): return self._ingredients.get(name, 0) > 0
    
    def use_ingredient(self, name):
        if self.has_ingredient(name):
            self._ingredients[name] -= 1
            return True
        print(f"Error: {name} 재고 부족!"); return False

    def use_raw_patty(self):
        if self.has_ingredient("패티"):
            self._ingredients["패티"] -= 1
            return True
        return False

    def add_cooked_patty(self): self._ingredients["조리된 패티"] += 1
    
    def get_stock_status(self): return self._ingredients
    
    def add_penalty(self):
        self._overcook_count += 1
        print(f"[패널티] 누적: {self._overcook_count}")
        if self._overcook_count >= self._overcook_limit: return "GAME_OVER"
        return "WARNING"
    
    # 저장용 메서드
    def to_dict(self):
        return {"money": self.__money, "ingredients": self._ingredients}
    def from_dict(self, data):
        if "money" in data: self.__money = data["money"]
        if "ingredients" in data:
            for k, v in data["ingredients"].items():
                if k in self._ingredients: self._ingredients[k] = v