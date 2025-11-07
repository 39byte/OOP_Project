# self_cl = 판매(구매)하는 국가 객체 / country_cl = 판매(구매)당하는 국가 객체
resource_list = ["wood"]

def Selling(self_cl, country_cl):
    resource = input("무엇을 판매하시겠습니까?\n")
    amount = int(input("얼마나 판매하시겠습니까?\n"))
    price = int(input("개당 얼마에 판매하시겠습니까?\n"))

    print(f"{resource}, {amount}, {price}")
    try:
        self_cl.Sell(country_cl, resource, amount, price)
    except TypeError:
        print("값이 제대로 할당되지 않았습니다.")
        pass

def Buying(self_cl, country_cl):
    resource = input("무엇을 구매하시겠습니까?\n")
    amount = int(input("얼마나 구매하시겠습니까?\n"))
    price = int(input("개당 얼마에 구매하시겠습니까?\n"))
    try:
        self_cl.Sell(country_cl, resource, amount, price)
    except TypeError:
        print("값이 제대로 할당되지 않았습니다.")
        pass