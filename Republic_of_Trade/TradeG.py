from CL_Country import Korea, America
from Fun_Selling import *

korea = Korea(1, 3)
america = America(3, 5)

america.Status
korea.Status

# 게임 실행 이후
Year = 1
while Year < 100:
    act = input("무엇을 하시겠습니까?\n")
    if act == "sell":
        country = input("어느 나라에 판매하시겠습니까?\n")

        if country == 'america': Selling(korea, america)
        else: print("알맞은 국가명을 기입하세요.")

    elif act == "buy":
        country = input("어느 나라에서 구매하시겠습니까?\n")
        pass
        
    elif act == "quit":
        break
    Year += 1

print("게임종료")