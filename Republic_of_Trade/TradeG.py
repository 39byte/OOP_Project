from CL_Country import Korea, America

korea = Korea(1, 3)
america = America(3, 5)
print(america)
print('\n')

print(korea)
print(america)

Year = 1
while Year < 100:
    act = input("무엇을 하시겠습니까?\n")
    if act == "sell":
        resource = input("무엇을 판매하시겠습니까?\n")
        amount, price = map(int, input("판매 개수, 판매 단가를 적어주세요.\n").replace(" ", "").split(','))
        korea.Sell(america, resource, amount, price)
        
        print()

    elif act == "종료":
        break
    Year += 1

print("게임종료")