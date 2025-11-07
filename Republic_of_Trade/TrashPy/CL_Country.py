from abc import abstractmethod, ABC

# 추상 클래스 국가
class Country(ABC):
    def __init__(self, money, wood):
        self.__money = money * 10000
        self.__wood = wood * 100

    def Event(self, event):
        # 산불이 날 경우 나무량 15% 손실
        if event == "wild_fire":
            self.wood *= 0.85
    
    @property
    def Status(self):
        print(f"[{self.__class__.__name__}] 돈 : {self.__money}, 나무 : {self.__wood}")

    # ====== getter ====== #
    @property
    def money(self):
        return self.__money
    
    @property
    def wood(self):
        return self.__wood
    # ===================== #

    # ====== setter ======= #
    def add_money(self, total):
        self.__money += total

    def add_wood(self, amount):
        self.__wood += amount

    def remove_money(self, total):
        self.__money -= total

    def remove_wood(self, amount):
        self.__wood -= amount
    # ====================== #


# 대한민국 클래스
class Korea(Country):
    def __init__(self, money, wood, level=1):
        super().__init__(money, wood)
        self.level = level

    def Sell(self, other, resource, amount, price):
        total = amount * price
        if resource != "wood":
            print("판매 자원을 정확히 적어주세요.")
            return
        if self.wood < amount:
            print("판매하려는 나무 양이 부족합니다.")
            return
        if other.money < total:
            print("상대 국가의 돈이 부족합니다.")
            return
        
        elif resource == "wood":
            other.remove_money(total)
            other.add_wood(amount)

            self.add_money(total)
            self.remove_wood(amount)

            print(f"""{resource} {amount:,}그루를 {other.__class__.__name__}에게 총 {amount * price:,}달러에 팔았습니다. 남은 {resource} : {self.wood:,}그루, 남은 돈 : {self.money:,}원""")

# 미국 클래스
class America(Country):
    def __init__(self, money, wood):
        super().__init__(money, wood)

class Saudi(Country):
    def __init__(self, money, wood):
        super().__init__(money, wood)