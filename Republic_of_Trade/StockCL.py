# 푸드트럭 재고 관리 클래스

class Stock():
    def __init__(self, money=10_000, Meat=10, Veg=10, Cheese=10):
        self.__money = money

        self.__meat = Meat
        self.__veg = Veg
        self.__cheese = Cheese

    # / ====== [ GETTER ] ====== \

    # 돈
    @property
    def money(self):
        return self.__money
    
    # 고기
    @property
    def meat(self):
        return self.__meat
    
    # 양상추
    @property
    def veg(self):
        return self.__veg
    
    @property
    def cheese(self):
        return self.__cheese
    
    # \ ========================= /

    # 돈 추가 차감
    @money.setter
    def add_money(self, amount):
        try: self.money += int(amount)
        except ValueError: print("올바르지 않은 값")
    
    @money.setter
    def remove_money(self, amount):
        try:
            if int(amount) <= self.money:
                self.money -= int(amount)
            else: print("돈이 부족합니다.")
        except ValueError: print("올바르지 않은 값")

    # 고기 추가 차감
    @meat.setter
    def add_meat(self, amount):
        try: self.meat += int(amount)
        except ValueError: print("올바르지 않은 값")
    
    @meat.setter
    def remove_meat(self, amount):
        try:
            if int(amount) <= self.meat:
                self.meat -= int(amount)
            else: print("재료가 부족합니다.")
        except ValueError: print("올바르지 않은 값")

    # 양배추 추가 차감
    @veg.setter
    def add_veg(self, amount):
        try: self.veg += int(amount)
        except ValueError: print("올바르지 않은 값")
    
    @veg.setter
    def remove_veg(self, amount):
        try:
            if int(amount) <= self.veg:
                self.veg -= int(amount)
            else: print("재료가 부족합니다.")
        except ValueError: print("올바르지 않은 값")

    # 치즈 추가 차감
    @cheese.setter
    def add_cheese(self, amount):
        try: self.cheese += int(amount)
        except ValueError: print("올바르지 않은 값")
    
    @cheese.setter
    def remove_cheese(self, amount):
        try:
            if int(amount) <= self.cheese:
                self.cheese -= int(amount)
            else: print("재료가 부족합니다.")
        except ValueError: print("올바르지 않은 값")