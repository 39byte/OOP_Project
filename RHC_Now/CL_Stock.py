import time

# 재고와 관련된 모든 것을 관리하는 클래스
# 실격 요건 판단도 같이 하는 클래스
class Stock():
    def __init__(self, money=100, patty=10, bun=10, lettuce=10, cheese=10):
        self.__money = money    # 돈 은닉화
        # 대시보드 표시 순서 (빵->치즈->양상추->패티->조리된)
        self._ingredients = {
            "빵": bun,
            "치즈": cheese,
            "양상추": lettuce,
            "패티": patty, 
            "조리된 패티": 0 
        }

        # 게임 오버 조건 위한 변수
        self._overcook_count = 0
        self._overcook_limit = 5
        
        # 재고 배송 지연 위한 변수
        self.stock_delay_duration = 0.0     # 기본 배송 시간
        self.delayed_stock_queue = []       # 배송 중인 재료 목록

    # Getter(돈, 오버쿡 카운트 은닉화)
    @property
    def money(self): return self.__money
    @property
    def overcook_count(self): return self._overcook_count
    @property
    def overcook_limit(self): return self._overcook_limit

    # 배송 지연 시간 설정
    def set_stock_delay(self, duration):
        self.stock_delay_duration = duration

    def update(self, dt):   # (매 프레임 실행)
        # 재고 보충 대기열 있는지 확인하고 있으면 실행
        if not self.delayed_stock_queue: return
        
        current_time = time.time()  # 현재 시간
        remaining_items = []        # 미도착 리스트

        for item_name, arrival_time in self.delayed_stock_queue:
            if current_time >= arrival_time:
                self._ingredients[item_name] += 10
                # 도착 시간 지나면 재고에 추가
                print(f"[재고] {item_name} 10개 배송 완료!")
            else:   # 아직 안 지났으면 다시 대기열행
                remaining_items.append((item_name, arrival_time))

        # 대기열 리스트 갱신
        self.delayed_stock_queue = remaining_items

    # 난이도 따라 오버쿡 리밋 설정
    def set_overcook_limit(self, limit): self._overcook_limit = limit

    # 돈 더하기(더하는 건 자유롭지만)
    def add_money(self, amount): 
        if amount > 0: self.__money += amount
    # 돈 빼기(빼는 건 니 맘대로 안 된다)
    def remove_money(self, amount):
        if 0 < amount <= self.__money:
            self.__money -= amount; return True
        print("돈이 부족합니다."); return False

    # 재고 추가
    def add_ingredient(self, ingredient_name, amount):
        if amount <= 0: return  # 1개 이상만 추가하도록
        if ingredient_name not in self._ingredients: return

        # 재고 보충 딜레이 있을 경우
        if self.stock_delay_duration > 0:
            for _ in range(amount): # 도착 예정 시간 계산해서 대기열(queue)에 넣기
                arrival_time = time.time() + self.stock_delay_duration
                self.delayed_stock_queue.append((ingredient_name, arrival_time))
            print(f"[재고] {ingredient_name} 주문 (딜레이).")
        else:
            self._ingredients[ingredient_name] += amount

    # 재고 있는지만 확인하는 용 (True / False)
    def has_ingredient(self, name): return self._ingredients.get(name, 0) > 0
    
    # 재고 사용 함수
    def use_ingredient(self, name):
        if self.has_ingredient(name):
            self._ingredients[name] -= 1
            return True
        print(f"Error: {name} 재고 부족!"); return False

    # 그릴 구울 때 생 패티 사용 함수
    def use_raw_patty(self):
        if self.has_ingredient("패티"):
            self._ingredients["패티"] -= 1
            return True
        return False

    # 조리 완료 후 완료 패티 추가
    def add_cooked_patty(self): self._ingredients["조리된 패티"] += 1
    
    # 재료 현황 딕셔너리로 반환
    def get_stock_status(self): return self._ingredients
    
    # 오버쿡 카운트 함수
    def add_penalty(self):
        self._overcook_count += 1
        # 한도 초과시 게임 오버 신호 보내기
        if self._overcook_count >= self._overcook_limit: return "GAME_OVER"

        print(f"[패널티] 누적: {self._overcook_count}")
        return "WARNING"
    
    # 저장용 메서드
    def to_dict(self):
        return {"money": self.__money, "ingredients": self._ingredients}
    def from_dict(self, data):
        if "money" in data: self.__money = data["money"]
        if "ingredients" in data:
            for k, v in data["ingredients"].items():
                if k in self._ingredients: self._ingredients[k] = v