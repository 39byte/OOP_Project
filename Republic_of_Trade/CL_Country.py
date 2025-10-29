from abc import abstractmethod, ABC

# 추상 클래스 국가
class Country(ABC):
    def __init__(self, money, wood):
        self.money = money * 10000
        self.wood = wood * 100

    def Event(self, event):
        # 산불이 날 경우 나무량 15% 손실
        if event == "wild_fire":
            self.wood *= 0.85

    def __str__(self):
        return f"[{self.__class__.__name__}] 돈 : {self.money}, 나무 : {self.wood}"

# 대한민국 클래스
class Korea(Country):
    def __init__(self, money, wood, level=1):
        super().__init__(money, wood)
        self.level = level

    @property
    def Sell(self, other, resource, amount, price):
        if resource == "wood":
            other.wood = other.wood + amount
            other.money += price * amount
            self.wood -= amount
            self.money += price * amount

            print(f"{resource} {amount}그루를 {other.__class__.__name__}에게 총 {amount * price:,}달러에 팔았습니다.")
            print(f"남은 {resource} : {self.wood}그루, 남은 돈 : {self.money:,}원")

# 미국 클래스
class America(Country):
    def __init__(self, money, wood):
        super().__init__(money, wood)