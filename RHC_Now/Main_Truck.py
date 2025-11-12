import pygame
import sys
import random
from CL_Difficulty_Button import Easy_Button, Normal_Button, Hard_Button
from FC_Grid import draw_grid_and_axes
from CL_Logo import Logo
from CL_Stock import Stock
# (v7) PickyCustomer, 이벤트 클래스, FloatingText 임포트
from game_object import Hamburger, Cheeseburger, NormalCustomer, VIPCustomer, PickyCustomer, GrillStation, FoodTruck
from ui_components import SimpleText, BaseButton, FloatingText 
from CL_Events import BrokenGrillEvent, StockDelayEvent, CelebrityEvent
from config import *

class GameClient:
    """메인 게임 루프(Client)를 캡슐화"""
    def __init__(self, window, clock, debug_font): 
        self.window = window # 게임 창
        self.clock = clock # 프레임 제어용 시계
        self.debug_font = debug_font # 디버그 폰트
        
        self.game_state = "START_MENU" # 초기 상태는 시작 메뉴
        self.difficulty = "None" # 현재 난이도
        self.player_stock = None  # 플레이어 재고 객체
        self.food_truck = None  # 푸드 트럭 객체
        self.menu_database = [Hamburger(), Cheeseburger()] # 메뉴 데이터베이스
        self.customers = [None, None, None, None]  # 손님 슬롯 초기화
        self.grills = [] # 그릴 스테이션 리스트
        self.game_timer = GAME_TIME_LIMIT # 게임 시간 제한
        self.show_grid = False # 그리드 표시 여부
        
        # (v7) 요청사항 1: 시작 시 손님 지연 스폰용 타이머
        self.initial_spawn_delay = 0.0 # 시작 시 지연 없음
        
        # (v7) 요청사항 3: 팁 알림용 리스트
        self.floating_texts = [] #  팁 알림 텍스트 리스트
        
        # (v7) 요청사항 2: 이벤트 관리
        self.all_event_types = [BrokenGrillEvent, StockDelayEvent, CelebrityEvent] # 이벤트 클래스 리스트
        self.current_event = None # 현재 활성화된 이벤트 객체
        self.event_spawn_timer = 0.0 # 다음 이벤트까지 남은 시간
        
        # (v7) 손님 종류 리스트 (Normal 50%, VIP 20%, Picky 30%)
        self.customer_types = [NormalCustomer, VIPCustomer, PickyCustomer]
        self.customer_weights = [0.5, 0.2, 0.3]
        
        try:
            self.background_image = pygame.image.load('C:/HUFS_Project/RHC_Now/assets/Wallpaper.png').convert() 
            self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except pygame.error:
            print("배경 이미지를 찾을 수 없습니다! 흰색으로 대체합니다.")
            self.background_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background_image.fill((255, 255, 255))
            
        self.GRID_SIZE = 50 
        
        self.start_menu_ui = [] 
        self.playing_ui_elements = [] 
        self.cooking_ui_elements = [] 
        self.game_texts = {} 
        
        self._setup_start_menu_ui()
        
    # --- 1. 콜백 함수 정의 ---
    def start_game(self, difficulty):
        """'난이도' 버튼 콜백: 게임을 시작"""
        print(f"게임 시작! 난이도: {difficulty}")
        self.difficulty = difficulty
        settings = DIFFICULTY_SETTINGS[difficulty]
        
        if difficulty == 'easy':
            self.player_stock = Stock(money=100, patty=20, bun=20, lettuce=20, cheese=20)
        elif difficulty == 'hard':
            self.player_stock = Stock(money=100, patty=5, bun=5, lettuce=5, cheese=5)
        else: # normal
            self.player_stock = Stock(money=100, patty=10, bun=10, lettuce=10, cheese=10)
        
        self.player_stock.set_overcook_limit(settings['overcook_limit'])
        self.food_truck = FoodTruck(self.player_stock)
        self.grills = [
            GrillStation(GRILL_SLOT_POS[0]),
            GrillStation(GRILL_SLOT_POS[1]),
            GrillStation(GRILL_SLOT_POS[2]),
            GrillStation(GRILL_SLOT_POS[3])
        ]
        
        self.game_timer = GAME_TIME_LIMIT
        self.customers = [None, None, None, None] # 손님 슬롯 초기화
        
        # (v7) 요청사항 1: 시작 시 5초간 손님 스폰 지연
       #self.initial_spawn_delay = 5.0 
        
        # (v7) 요청사항 3: 팁 알림 리스트 초기화
        self.floating_texts = []
        
        # (v7) 요청사항 2: 이벤트 타이머 초기화 (20~30초 뒤 첫 이벤트)
        self.current_event = None
        self.event_spawn_timer = random.uniform(20, 30) 
        
        self._setup_playing_ui()
        self._setup_cooking_ui()
        self.game_state = "PLAYING"

    # --- [PLAYING] 상태 콜백 ---
    def cb_click_grill(self, grill_index):
        if self.game_state != "PLAYING" or self.player_stock is None: return
        grill = self.grills[grill_index]
        if grill.state == "그릴":
            grill.start_cook(self.player_stock) 
        else:
            status = grill.get_click_result(self.player_stock) 
            if status == "게임오버":
                self.game_state = "GAME_OVER"

    def cb_click_assembly(self, _):
        if self.game_state != "PLAYING": return
        customer = next((c for c in self.customers if c is not None and c.order_list), None)
        if customer:
            print("[상태] 조립대를 클릭. 조리 팝업을 엽니다.")
            order_item = customer.order_list[0] 
            self.food_truck.set_new_order(order_item.get_recipe())
            self.game_state = "COOKING" 
        else:
            print("아직 손님 주문이 없습니다.")

    def cb_add_stock(self, ingredient_name):
        if self.game_state != "PLAYING": return
        ingredient_to_add = None
        if ingredient_name == "빵 추가": ingredient_to_add = "빵"
        elif ingredient_name == "치즈 추가": ingredient_to_add = "치즈"
        elif ingredient_name == "양상추 추가": ingredient_to_add = "양상추"
        elif ingredient_name == "패티 추가": ingredient_to_add = "패티"
        if ingredient_to_add:
            # (v7) Stock의 딜레이 적용된 add_ingredient 호출
            # 1. config에서 설정한 비용으로 돈이 있는지 확인하고 $1 지불
            if self.player_stock.remove_money(STOCK_PURCHASE_COST):
                # 2. 돈 지불에 성공하면 재고 추가 (딜레이 적용될 수 있음)
                self.player_stock.add_ingredient(ingredient_to_add, 1)
            else:
                # 3. 돈이 없으면 실패
                print(f"[재고] {ingredient_to_add} 구매 실패. (${STOCK_PURCHASE_COST} 필요)")
                
                # (v8) 돈 부족 알림 텍스트 띄우기 (팁 알림 재활용)
                btn_pos = STOCK_BUTTONS_POS
                fail_pos = (btn_pos[0] + 60, btn_pos[1] - 20) # 버튼 상단 중앙
                self.floating_texts.append(FloatingText(self.window, fail_pos, "돈 부족!", 20, RED, duration=1.0))

    # --- [COOKING] (팝업) 상태 콜백 ---
    def cb_popup_add_ingredient(self, ingredient_name):
        if self.game_state != "COOKING": return
        if ingredient_name == "조리된 패티": ingredient_name = "패티"
        self.food_truck.add_to_assembly(ingredient_name)

    def cb_popup_trash(self, _):
        if self.game_state != "COOKING": return
        self.food_truck.clear_assembly()
        
    def cb_popup_close_or_serve(self, action):
        if self.game_state != "COOKING": return
        
        if action == "서빙":
            customer = next((c for c in self.customers if c is not None and c.order_list), None) 
            if not customer:
                 print("서빙할 손님이 없습니다."); return
                 
            order_item_recipe = customer.order_list[0].get_recipe()

            if self.food_truck.assembly_station == order_item_recipe:
                print("--- 버거 판매 성공! ---")
                order_item = customer.order_list.pop(0) 
                
                item_price = order_item.get_price()
                revenue = customer.pay(item_price) # pay 메서드는 최종 금액 반환
                self.player_stock.add_money(revenue) 
                
                # (v7) 요청사항 3: 팁 알림 생성
                if revenue > item_price:
                    tip_amount = revenue - item_price
                    tip_msg = f"+${tip_amount} TIP!"
                    # 손님 위치 위쪽에 텍스트 생성
                    customer_index = self.customers.index(customer)
                    customer_pos = CUSTOMER_SLOT_POS[customer_index]
                    float_text_pos = (customer_pos[0], customer_pos[1] - 30) 
                    self.floating_texts.append(FloatingText(self.window, float_text_pos, tip_msg, 20, (0, 200, 0), duration=2.0))
                
                if not customer.order_list: # 주문이 더 없으면 손님 떠남
                    customer_index = self.customers.index(customer)
                    self.customers[customer_index] = None 
                
                self.food_truck.set_new_order([])
                self.game_state = "PLAYING"
            else:
                print("주문과 다릅니다! 서빙할 수 없습니다."); return

        elif action == "닫기":
            self.game_state = "PLAYING"
            print("[상태] 조리 팝업을 닫습니다.")

    # --- 2. UI 생성 ---
    def _setup_start_menu_ui(self):
        self.start_menu_ui.append(Easy_Button(self.window, (WINDOW_WIDTH // 2, 380), 200, callBack=lambda: self.start_game('easy')))
        self.start_menu_ui.append(Normal_Button(self.window, (WINDOW_WIDTH // 2, 480), 200, callBack=lambda: self.start_game('normal')))
        self.start_menu_ui.append(Hard_Button(self.window, (WINDOW_WIDTH // 2, 580), 200, callBack=lambda: self.start_game('hard')))
        self.start_menu_ui.append(Logo(self.window, (WINDOW_WIDTH // 2, 160), 400, "https://github.com/39byte/OOP_Project/tree/master"))
    
    def _setup_playing_ui(self):
        self.playing_ui_elements = [] 
        self.game_texts = {} 
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        target_revenue = settings['target_revenue']
        overcook_limit = settings['overcook_limit']
        
        self.game_texts['time'] = SimpleText(self.window, TIME_UI_POS, f"{int(self.game_timer)}초", 30, BLACK, 'right')
        self.game_texts['difficulty'] = SimpleText(self.window, DIFFICULTY_UI_POS, f"난이도: {self.difficulty}", 24, GRAY, 'right')
        self.game_texts['overcook'] = SimpleText(self.window, OVERCOOK_UI_POS, f"오버쿡: 0 / {overcook_limit}", 30, RED, 'right')
        self.game_texts['score'] = SimpleText(self.window, DASHBOARD_SCORE_POS, f"매출: ${self.player_stock.money} / ${target_revenue}", 20, BLACK, 'left')
        
        y_offset = DASHBOARD_STOCK_POS[1]
        for item, count in self.player_stock.get_stock_status().items():
            self.game_texts[f'stock_{item}'] = SimpleText(self.window, (DASHBOARD_STOCK_POS[0], y_offset), f"{item}: {count}", 18, GRAY, 'left')
            y_offset += 25
            
        self.playing_ui_elements.append(BaseButton(self.window, ASSEMBLY_STATION_POS, text="조립하기 (팝업)", size=24, width=150, height=150, callBack=self.cb_click_assembly))
        btn_x, btn_y = STOCK_BUTTONS_POS
        self.playing_ui_elements.append(BaseButton(self.window, (btn_x, btn_y + 0), "빵 추가", 20, 120, 40, callBack=self.cb_add_stock))
        self.playing_ui_elements.append(BaseButton(self.window, (btn_x, btn_y + 50), "치즈 추가", 20, 120, 40, callBack=self.cb_add_stock))
        self.playing_ui_elements.append(BaseButton(self.window, (btn_x, btn_y + 100), "양상추 추가", 20, 120, 40, callBack=self.cb_add_stock))
        self.playing_ui_elements.append(BaseButton(self.window, (btn_x, btn_y + 150), "패티 추가", 20, 120, 40, callBack=self.cb_add_stock))       
        self.game_texts['recipe'] = SimpleText(self.window, (ASSEMBLY_STATION_POS[0] + 75, ASSEMBLY_STATION_POS[1] + 210), "손님 클릭 -> 조립", 18, BLACK, 'center')
        
    def _setup_cooking_ui(self):
        """조리 팝업 UI 생성"""
        self.cooking_ui_elements = [] 
        self.popup_texts = {}
        x, y = POPUP_INGREDIENT_POS
        self.cooking_ui_elements.append(BaseButton(self.window, (x, y), "빵", 20, 120, 40, callBack=self.cb_popup_add_ingredient))
        self.popup_texts['빵'] = SimpleText(self.window, (x + 130, y + 10), ": 0개", 20, BLACK) 
        y += 50
        self.cooking_ui_elements.append(BaseButton(self.window, (x, y), "양상추", 20, 120, 40, callBack=self.cb_popup_add_ingredient))
        self.popup_texts['양상추'] = SimpleText(self.window, (x + 130, y + 10), ": 0개", 20, BLACK)
        y += 50
        self.cooking_ui_elements.append(BaseButton(self.window, (x, y), "조리된 패티", 20, 120, 40, callBack=self.cb_popup_add_ingredient))
        self.popup_texts['조리된 패티'] = SimpleText(self.window, (x + 130, y + 10), ": 0개", 20, BLACK)
        y += 50
        self.cooking_ui_elements.append(BaseButton(self.window, (x, y), "치즈", 20, 120, 40, callBack=self.cb_popup_add_ingredient))
        self.popup_texts['치즈'] = SimpleText(self.window, (x + 130, y + 10), ": 0개", 20, BLACK)
        self.cooking_ui_elements.append(BaseButton(self.window, POPUP_TRASH_POS, "버리기", 20, 120, 40, callBack=self.cb_popup_trash))
        self.cooking_ui_elements.append(BaseButton(self.window, (POPUP_CLOSE_POS[0] - 130, POPUP_CLOSE_POS[1]), "서빙", 20, 100, 40, callBack=lambda x: self.cb_popup_close_or_serve("서빙")))
        self.cooking_ui_elements.append(BaseButton(self.window, POPUP_CLOSE_POS, "닫기", 20, 100, 40, callBack=lambda x: self.cb_popup_close_or_serve("닫기")))

    # --- 3. 게임 루프 ---
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0 
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g: 
                        self.show_grid = not self.show_grid 

                # 상태에 따라 이벤트 처리 분리
                if self.game_state == "START_MENU":
                    for ui_element in self.start_menu_ui:
                        ui_element.handleEvent(event)
                elif self.game_state == "PLAYING":
                    for ui_element in self.playing_ui_elements:
                        ui_element.handleEvent(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i, grill in enumerate(self.grills):
                            if grill.rect.collidepoint(event.pos):
                                self.cb_click_grill(i) 
                elif self.game_state == "COOKING":
                    for ui_element in self.cooking_ui_elements:
                        ui_element.handleEvent(event)

            if self.game_state == "PLAYING":
                self.update_playing_state(dt)
            
            self.draw_screen()
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def update_playing_state(self, dt):
        """PLAYING 상태일 때 매 프레임 실행될 로직"""
        if self.player_stock is None: return

        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.game_timer -= dt
        
        # (v7) 재고 딜레이 큐 업데이트
        self.player_stock.update(dt)
        
        for grill in self.grills:
            grill.update(dt) 

        # --- (v7) 요청사항 2: 이벤트 시스템 업데이트 ---
        if self.current_event:
            # 1. 활성화된 이벤트가 있으면, update 호출
            # (다형성) BrokenGrill이든 Celebrity이든 update()만 호출
            if not self.current_event.update(dt, self):
                self.current_event = None # 이벤트 종료
                self.event_spawn_timer = random.uniform(30, 45) # 다음 이벤트 쿨타임
        else:
            # 2. 활성화된 이벤트가 없으면, 스폰 타이머 감소
            self.event_spawn_timer -= dt
            if self.event_spawn_timer <= 0:
                # 새 이벤트 스폰
                SelectedEvent = random.choice(self.all_event_types)
                self.current_event = SelectedEvent() # 이벤트 객체 생성
                self.current_event.activate(self) # 이벤트 활성화
            #settings = DIFFICULTY_SETTINGS[self.difficulty]
            spawn_chance = dt / settings['customer_count_avg_sec']
        
            if random.random() < spawn_chance:
                for i, slot in enumerate(self.customers):
                    if slot is None:
                    # (v7) self.customer_types 리스트에서 가중치 기반으로 무작위 선택
                        CustomerClass = random.choices(
                        self.customer_types, 
                        weights=self.customer_weights,
                        k=1
                        )[0]
                    
                        self.customers[i] = CustomerClass(wait_time=40 * settings['wait_time_factor'])
                    
                    # (v7) 만약 '연예인 이벤트' 중이면, 새 손님에게도 효과 적용
                        if self.current_event and isinstance(self.current_event, CelebrityEvent):
                            self.customers[i].set_patience_factor(self.current_event.patience_factor)
                        
                        self.customers[i].order(self.menu_database)
                        break
       
                    
        # 손님 대기 시간 (patience_factor가 적용된 update 호출)
        for i, customer in enumerate(self.customers):
            if customer:
                if not customer.update(dt): #
                    print("손님이 기다리다 떠났습니다! (패널티)")
                    if self.player_stock.add_penalty() == "GAME_OVER":
                        self.game_state = "GAME_OVER"
                    self.customers[i] = None
        
        if self.game_state == "GAME_OVER": return
        
        # (v7) 요청사항 3: 플로팅 텍스트(팁) 업데이트
        # 리스트를 뒤에서부터 순회하며 삭제 (안전한 삭제)
        for i in range(len(self.floating_texts) - 1, -1, -1):
            if not self.floating_texts[i].update(dt):
                self.floating_texts.pop(i)
        
        # 종료 조건
        target_revenue = settings['target_revenue']
        if self.game_timer <= 0:
            self.game_state = "GAME_OVER" if self.player_stock.money < target_revenue else "SUCCESS"
        if self.game_state != "GAME_OVER" and self.player_stock.money >= target_revenue:
            stock = self.player_stock.get_stock_status()
            if sum(v for k, v in stock.items() if k != "조리된 패티") == 0:
                 self.game_state = "SUCCESS"

    def draw_screen(self):
        """현재 게임 상태에 맞춰 화면을 그림"""
        self.window.blit(self.background_image, (0, 0)) 
        if self.show_grid: 
            draw_grid_and_axes(self.window, self.GRID_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, self.debug_font)

        if self.game_state == "START_MENU":
            for ui_element in self.start_menu_ui:
                ui_element.draw()
            
        elif self.game_state in ["PLAYING", "GAME_OVER", "SUCCESS"]:
            self.draw_playing_ui() # (v7) draw_playing_ui가 모든 것을 그림
            
            if self.game_state == "GAME_OVER":
                msg = SimpleText(self.window, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "GAME OVER", 80, RED, 'center')
                msg.draw()
            elif self.game_state == "SUCCESS":
                msg = SimpleText(self.window, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "SUCCESS!", 80, GREEN, 'center')
                msg.draw()

        elif self.game_state == "COOKING":
            self.draw_playing_ui() # (v7) 조리 중에도 메인 UI를 그리고
            self.draw_cooking_popup() # 그 위에 팝업을 그림

    def draw_playing_ui(self):
        """메인 게임 화면 UI 그리기"""
        if self.player_stock is None: return

        pygame.draw.rect(self.window, (220, 220, 220, 200), TRUCK_AREA_RECT, border_radius=10)
        pygame.draw.rect(self.window, (200, 200, 255, 200), DASHBOARD_RECT, border_radius=10)

        for grill in self.grills:
            grill.draw(self.window)
        
        for i, customer in enumerate(self.customers):
            if customer:
                customer.draw(self.window, CUSTOMER_SLOT_POS[i])

        for button in self.playing_ui_elements:
            button.draw()
        
        # (v7) 요청사항 3: 플로팅 텍스트(팁) 그리기
        for f_text in self.floating_texts:
            f_text.draw()
            
        # 텍스트 UI 업데이트 (setValue)
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.game_texts['time'].setValue(f"남은 시간: {int(self.game_timer)}초")
        self.game_texts['score'].setValue(f"매출: ${self.player_stock.money} / ${settings['target_revenue']}")
        self.game_texts['overcook'].setValue(f"오버쿡: {self.player_stock.overcook_count} / {settings['overcook_limit']}")
        
        recipe_text = "주문 대기 중..."
        customer = next((c for c in self.customers if c is not None and c.order_list), None)
        if customer:
            recipe_text = f"주문: {customer.order_list[0].get_recipe()}"
        self.game_texts['recipe'].setValue(recipe_text)
        
        current_stock = self.player_stock.get_stock_status()
        for item, count in current_stock.items():
            if f'stock_{item}' in self.game_texts:
                self.game_texts[f'stock_{item}'].setValue(f"{item}: {count}")
        
        for text_obj in self.game_texts.values():
            text_obj.draw()
            
        # (v7) 요청사항 2: 이벤트 알림 그리기
        if self.current_event:
            self.current_event.draw(self.window)

    def draw_cooking_popup(self):
        """조리 팝업 UI 그리기"""
        dim_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        dim_surface.fill(POPUP_DIM_COLOR)
        self.window.blit(dim_surface, (0, 0))
        
        pygame.draw.rect(self.window, POPUP_BG_COLOR, POPUP_RECT, border_radius=10)
        pygame.draw.rect(self.window, BLACK, POPUP_RECT, width=2, border_radius=10)

        for button in self.cooking_ui_elements:
            button.draw()
            
        if self.player_stock: 
            current_stock = self.player_stock.get_stock_status()
            self.popup_texts['빵'].setValue(f": {current_stock.get('빵', 0)}개")
            self.popup_texts['양상추'].setValue(f": {current_stock.get('양상추', 0)}개")
            self.popup_texts['조리된 패티'].setValue(f": {current_stock.get('조리된 패티', 0)}개")
            self.popup_texts['치즈'].setValue(f": {current_stock.get('치즈', 0)}개")

        for text_obj in self.popup_texts.values():
            text_obj.draw()
            
        self.food_truck.draw(self.window)

# --- 6. 실행 (중요) ---
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("러시아워 셰프 (7조)")
clock = pygame.time.Clock()
debug_font = pygame.font.SysFont('Arial', 14)

pygame.font.init() 
try:
    _ = pygame.font.Font(FONT_PATH, 10) 
except (FileNotFoundError, pygame.error):
    print(f"!!! 치명적 오류: '{FONT_PATH}' 폰트 파일을 찾을 수 없습니다. !!!")
    print("!!! 게임을 실행할 수 없습니다. 'assets/fonts' 폴더를 확인하세요. !!!")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game = GameClient(window, clock, debug_font)
    game.run()