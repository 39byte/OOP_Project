# 🍔 러시아워 셰프 (Rush Hour Chef)

OOP(객체지향 프로그래밍) 4대 개념을 적용하여 Pygame으로 개발한 푸드트럭 경영 시뮬레이션 게임입니다.

## 1. 📖 게임 개요

플레이어는 5분의 제한 시간 동안 푸드트럭을 운영하는 사장이 됩니다. 손님의 주문에 맞춰 햄버거를 조리하고, 재고를 관리하며, 패널티를 피해 목표 매출을 달성해야 합니다.

* **테마:** "슈의 라면가게"와 유사한 타이밍/순서 기반 조리 + 재고 관리 타이쿤
* **게임 방식:**
    1.  **난이도 선택:** (쉬움/보통/어려움) - 손님 수, 대기 시간, 목표 금액이 달라집니다.
    2.  **주문 접수:** 손님이 햄버거(기본, 치즈)를 주문합니다.
    3.  **조리:**
        * **그릴 (타이밍):** 패티를 그릴에 올리고, 타지 않게(오버쿡) 타이밍 맞춰 가져옵니다.
        * **조립 (순서):** 빵, 패티, 양상추, 치즈 등 재료를 올바른 순서로 쌓습니다.
    4.  **판매:** 완성된 음식을 손님에게 전달하고 돈을 법니다.
* **승리 조건:** 5분 내 목표 매출액 달성 + 재고 소진
* **패배 조건:** 오버쿡 5회 누적 또는 시간 내 목표 미달성

## 2. 💡 핵심 기획 의도 (OOP 적용)

본 프로젝트는 Pygame을 활용하여 OOP 4대 개념을 명확하게 학습하고 구현하는 것을 목표로 합니다.

* **객체화:** 손님, 메뉴, 트럭, 조리대 등 모든 요소를 객체로 모델링합니다.
* **선형적 구조:** '주문 → 조리 → 판매'의 명확한 흐름은 **상속**과 **다형성**을 통한 기능 확장에 유리합니다.
* **버그 방지:** **캡슐화**를 통해 재고가 없는데 판매가 되거나, 돈이 음수가 되는 등의 치명적인 버그를 원천적으로 방지합니다.

### 🎮 OOP 4대 개념 적용 계획

* **추상화 (Abstraction):**
    * `MenuItem`, `Customer`, `CookingStation`을 **추상 기본 클래스(ABC)**로 설계합니다.
    * `MenuItem`은 `get_recipe()`, `get_price()` 등 공통 인터페이스를 정의합니다.
* **상속 (Inheritance):**
    * `MenuItem` (부모) → `Hamburger`(자식), `Cheeseburger`(자식)
    * `Customer` (부모) → `NormalCustomer`(자식), `ImpatientCustomer`(자식), `VIPCustomer`(자식)
    * `FoodTruck` (부모) → `FastTruck`(자식 - 조리 속도 빠름), `BigTruck`(자식 - 재고 많음) (향후 확장)
* **다형성 (Polymorphism):**
    * 클라이언트(`main.py`)는 `customer.pay()`라는 동일한 코드를 호출합니다.
    * 하지만 `NormalCustomer`는 정가만, `VIPCustomer`는 **오버라이딩**된 메서드에 따라 팁을 포함한 금액을 **알아서** 반환합니다.
    * `station.cook()` 호출 시, `GrillStation`은 타이머를 돌리고 `FryerStation`은 다른 타이머를 돌리는 등 다르게 작동합니다.
* **캡슐화 (Encapsulation):**
    * `FoodTruck`의 `__money`(돈), `_ingredients`(재고), `_overcook_count`(오버쿡 횟수)를 **은닉(private/protected)**합니다.
    * `use_ingredient()` 메서드 내부에서만 재고를 차감하며, 호출 시 재고가 0보다 큰지 **검사(버그 방지)**합니다.
    * `add_overcook()` 메서드 내부에서만 횟수를 증가시키며, 5가 되는지 **검사(패배 처리)**합니다.

## 3. 📂 프로젝트 구조
rush_hour_chef/ ├── assets/ │ ├── images/ │ │ ├── truck.png │ │ ├── grill.png │ │ ├── bun.png │ │ ├── patty_raw.png │ │ ├── patty_cooked.png │ │ ├── patty_overcooked.png │ │ ├── cheese.png │ │ ├── lettuce.png │ │ ├── customer_normal.png │ │ ├── customer_vip.png │ │ └── button_cook.png │ ├── sounds/ │ │ ├── grill_sizzle.wav │ │ ├── order_complete.wav │ │ ├── overcook_fail.wav │ │ └── background_music.mp3 │ └── fonts/ │ └── NotoSansKR-Bold.ttf │ ├── src/ │ ├── components/ # OOP 9강의 UI/객체 클래스 │ │ ├── init.py │ │ ├── button.py # SimpleButton 클래스 (9강) │ │ ├── text.py # SimpleText 클래스 (9강) │ │ │ ├── game_objects/ # 게임 핵심 OOP 클래스 │ │ ├── init.py │ │ ├── abc_base.py # 추상 클래스 (MenuItem, Customer, CookingStation) │ │ ├── truck.py # FoodTruck 클래스 (캡슐화의 핵심) │ │ ├── menu_items.py # Hamburger, Cheeseburger 클래스 (상속) │ │ ├── customers.py # NormalCustomer, VIPCustomer 등 (다형성) │ │ └── stations.py # GrillStation, FryerStation 등 (추상화/상속) │ │ │ ├── config.py # 설정 파일 (WINDOW_WIDTH, FPS, 색상 등) │ └── main.py # 메인 게임 루프 (클라이언트 프로그램) │ ├── requirements.txt # 필요한 라이브러리 목록 └── README.md # 현재 파일
# 4. ⚙️ 설치 및 환경 설정

본 프로젝트는 Python 3.10 이상 및 Pygame 2.x 버전에서 개발되었습니다.

1.  **가상 환경 생성 (권장):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  **필요한 라이브러리 설치:**
    ```bash
    pip install pygame
    ```
    (또는 `requirements.txt`가 있을 경우: `pip install -r requirements.txt`)

## 5. 🚀 실행 방법

프로젝트의 루트 디렉터리에서 `src/main.py` 파일을 실행합니다.

```bash
python src/main.py
