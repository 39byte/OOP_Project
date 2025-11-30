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
from CL_GameSaver import GameSaver # (v10) 저장 기능 추가

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
        
        # (!!!) 추가: 현재 선택된 손님을 추적하기 위한 변수
        self.selected_customer = None 
        self.selected_customer_index = -1   
        
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
        
        # (v10) 게임 저장 시스템
        self.saver = GameSaver()
        self.game_saved = False # 중복 저장 방지 플래그

        # (v12) 배경 이미지 로드 분리 (시작화면 / 게임화면)
        self.bg_start = self._load_bg_image('assets/Wallpaper.png')
        self.bg_game = None # start_game에서 로드

        self.GRID_SIZE = 50 
        #UI 객체 리스트 초기화
        self.start_menu_ui = [] 
        self.playing_ui_elements = [] 
        self.cooking_ui_elements = [] 
        self.game_texts = {} 
        
        self._setup_start_menu_ui()

    # (v12) 배경 이미지 로드 헬퍼 함수
    def _load_bg_image(self, path):
        try:
            img = pygame.image.load(path).convert()
            return pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except pygame.error:
            print(f"배경 이미지({path})를 찾을 수 없습니다! 흰색으로 대체합니다.")
            bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            bg.fill((255, 255, 255))
            return bg

    # --- 2. UI 생성 함수들 ---
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
        # (v12) 난이도 글씨 색 변경: GRAY -> BLACK
        self.game_texts['difficulty'] = SimpleText(self.window, DIFFICULTY_UI_POS, f"난이도: {self.difficulty}", 24, BLACK, 'right')
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
        
        self.game_texts['recipe'] = SimpleText(self.window, (ASSEMBLY_STATION_POS[0] + 75, ASSEMBLY_STATION_POS[1] + 210), "주문 대기 중... (손님 클릭)", 18, BLACK, 'center')
        
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

    # --- 3. 콜백 함수 정의 그룹 ---
    
    def start_game(self, difficulty):
        """'난이도' 버튼 콜백: 게임을 시작"""
        print(f"게임 시작! 난이도: {difficulty}")
        self.difficulty = difficulty
        settings = DIFFICULTY_SETTINGS[difficulty]
        
        if difficulty == 'easy':
            self.player_stock = Stock(money=100, patty=20, bun=20, lettuce=20, cheese=20)
        elif difficulty == 'hard':
            self.player_stock = Stock(money=100, patty=10, bun=10, lettuce=10, cheese=10)
        else: # normal
            self.player_stock = Stock(money=100, patty=15, bun=15, lettuce=15, cheese=15)
        
        self.player_stock.set_overcook_limit(settings['overcook_limit'])
        self.food_truck = FoodTruck(self.player_stock)
        self.grills = [
            GrillStation(GRILL_SLOT_POS[0]),
            GrillStation(GRILL_SLOT_POS[1]),
            GrillStation(GRILL_SLOT_POS[2]),
            GrillStation(GRILL_SLOT_POS[3])
        ]
        #게임 상태 초기화
        self.game_timer = GAME_TIME_LIMIT
        self.customers = [None, None, None, None] 
        self.selected_customer = None 
        self.selected_customer_index = -1   
        self.floating_texts = []
        self.current_event = None
        self.event_spawn_timer = random.uniform(10, 30) 
        
        self.game_saved = False # (v10) 저장 플래그 초기화

        # (v12) 게임 시작 시 게임용 배경 이미지 로드
        if self.bg_game is None:
            self.bg_game = self._load_bg_image('assets/Wallpaper2.png')
        
        self._setup_playing_ui()
        self._setup_cooking_ui()
        self.game_state = "PLAYING"

    # --- [PLAYING] 상태 콜백 ---
    
    def cb_click_grill(self, grill_index):
        if self.game_state != "PLAYING" or self.player_stock is None: return
        grill = self.grills[grill_index]
        if grill.state == "대기":
            grill.start_cook(self.player_stock) 
        else:
            status = grill.get_click_result(self.player_stock) 
            if status == "게임오버":
                self.game_state = "GAME_OVER"

    def cb_click_assembly(self, _):
        if self.game_state != "PLAYING": return
        
        customer = self.selected_customer
        
        if customer and customer.order_list: 
            print("[상태] 조립대를 클릭. 선택된 손님의 팝업을 엽니다.")
            order_item = customer.order_list[0] 
            self.food_truck.set_new_order(order_item.get_recipe())
            self.game_state = "COOKING" 
        elif not customer:
            print("먼저 손님을 클릭하여 선택해주세요.")
        else:
            print("선택된 손님의 주문이 없습니다.")

    def cb_add_stock(self, ingredient_name):
        if self.game_state != "PLAYING": return
        ingredient_to_add = None
        if ingredient_name == "빵 추가": ingredient_to_add = "빵"
        elif ingredient_name == "치즈 추가": ingredient_to_add = "치즈"
        elif ingredient_name == "양상추 추가": ingredient_to_add = "양상추"
        elif ingredient_name == "패티 추가": ingredient_to_add = "패티"
        if ingredient_to_add:
            if self.player_stock.remove_money(STOCK_PURCHASE_COST):
                self.player_stock.add_ingredient(ingredient_to_add, 1)
            else:
                print(f"[재고] {ingredient_to_add} 구매 실패. (${STOCK_PURCHASE_COST} 필요)")
                btn_pos = STOCK_BUTTONS_POS
                fail_pos = (btn_pos[0] + 60, btn_pos[1] - 20) 
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
            customer = self.selected_customer
             
            if not customer:
                 print("서빙할 손님이 선택되지 않았습니다."); return
                 
            order_item_recipe = customer.order_list[0].get_recipe()
            
            # [검사] 현재 조립된 버거가 주문 레시피와 같은지 확인
            if self.food_truck.assembly_station == order_item_recipe:
                # --- 성공 로직 (기존과 동일) ---
                print("--- 버거 판매 성공! ---")
                order_item = customer.order_list.pop(0) 
                
                item_price = order_item.get_price()
                revenue = customer.pay(item_price)
                self.player_stock.add_money(revenue) 
                
                if revenue > item_price:
                    tip_amount = revenue - item_price
                    tip_msg = f"+${tip_amount} TIP!"
                    customer_pos = CUSTOMER_SLOT_POS[self.selected_customer_index] 
                    float_text_pos = (customer_pos[0], customer_pos[1] - 30) 
                    self.floating_texts.append(FloatingText(self.window, float_text_pos, tip_msg, 20, (0, 200, 0), duration=2.0))
                
                if not customer.order_list: 
                    self.customers[self.selected_customer_index] = None 
                    self.selected_customer = None 
                    self.selected_customer_index = -1   
                
                self.food_truck.set_new_order([])
                self.game_state = "PLAYING"
            
            # --- [수정된 부분] 실패 로직: 잘못된 버거 서빙 ---
            else:
                print("잘못된 버거 서빙! (패널티 발생)")
                
                # 1. 아깝지만 잘못 만든 버거는 버립니다 (재료 낭비)
                self.food_truck.clear_assembly() 
                
                # 2. 패널티 부여 (오버쿡 카운트 증가) 및 게임오버 체크
                if self.player_stock.add_penalty() == "GAME_OVER":
                    self.game_state = "GAME_OVER"
                
                # 3. 팝업을 닫지 않고(return) 다시 만들 기회를 줍니다.
                return 

        elif action == "닫기":
            self.game_state = "PLAYING"
            self.selected_customer = None
            self.selected_customer_index = -1
            print("[상태] 조리 팝업을 닫고 손님 선택을 해제합니다.")

    # --- 4. 게임 상태 업데이트 ---
    
    def update_playing_state(self, dt):
        """PLAYING 상태일 때 매 프레임 실행될 로직"""
        if self.player_stock is None: return

        # (!!!) 설정 변수 정의
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        
        self.game_timer -= dt
        
        self.player_stock.update(dt)
        
        for grill in self.grills:
            grill.update(dt) 

        # --- 이벤트 시스템 업데이트 ---
        if self.current_event:
            if not self.current_event.update(dt, self):
                self.current_event = None 
                self.event_spawn_timer = random.uniform(30, 45) 
        else:
            self.event_spawn_timer -= dt
            if self.event_spawn_timer <= 0:
                SelectedEvent = random.choice(self.all_event_types)
                self.current_event = SelectedEvent() 
                self.current_event.activate(self) 
        
        # --- 손님 스폰 로직 ---
        spawn_chance = dt / settings['customer_count_avg_sec']
        if random.random() < spawn_chance:
            for i, slot in enumerate(self.customers):
                if slot is None:
                    CustomerClass = random.choices(
                        self.customer_types, 
                        weights=self.customer_weights,
                        k=1
                    )[0]
                    
                    customer_pos = CUSTOMER_SLOT_POS[i]
                    self.customers[i] = CustomerClass(self.window, customer_pos, wait_time=40 * settings['wait_time_factor'])
                    
                    if self.current_event and isinstance(self.current_event, CelebrityEvent):
                        self.customers[i].set_patience_factor(self.current_event.patience_factor)
                        
                    self.customers[i].order(self.menu_database)
                    break
       
        # --- 손님 대기 시간 업데이트 ---
        for i, customer in enumerate(self.customers):
            if customer:
                if not customer.update(dt): 
                    print("손님이 기다리다 떠났습니다! (패널티)")
                    if self.player_stock.add_penalty() == "GAME_OVER":
                        self.game_state = "GAME_OVER"
                    self.customers[i] = None
                    
                    if i == self.selected_customer_index:
                        self.selected_customer = None
                        self.selected_customer_index = -1
                        print("[선택] 선택된 손님이 떠났습니다. 선택 해제.")
        
        if self.game_state == "GAME_OVER": return
        
        # --- 플로팅 텍스트 업데이트 ---
        for i in range(len(self.floating_texts) - 1, -1, -1):
            if not self.floating_texts[i].update(dt):
                self.floating_texts.pop(i)
        
        # --- 종료 조건 및 저장 ---
        target_revenue = settings['target_revenue']
        
        # 1. 실시간 승리
        if self.game_state == "PLAYING" and self.player_stock.money >= target_revenue:
            self.game_state = "SUCCESS"
            print("[게임] 목표 매출액 달성! SUCCESS!")
            if not self.game_saved:
                time_taken = GAME_TIME_LIMIT - self.game_timer
                self.saver.save_result(self.player_stock.money, time_taken, True)
                self.game_saved = True
        
        # 2. 시간 종료
        if self.game_timer <= 0:
            if self.game_state != "SUCCESS": 
                self.game_state = "GAME_OVER" if self.player_stock.money < target_revenue else "SUCCESS"
                if not self.game_saved:
                    time_taken = GAME_TIME_LIMIT
                    # 목표 달성 여부 다시 확인
                    is_success = self.player_stock.money >= target_revenue
                    self.saver.save_result(self.player_stock.money, time_taken, is_success)
                    self.game_saved = True

    # --- 5. 그리기 함수들 ---

    def draw_screen(self):
        """현재 게임 상태에 맞춰 화면을 그림"""
        
        # (v12) 상태에 따라 다른 배경 그리기
        if self.game_state == "START_MENU":
            self.window.blit(self.bg_start, (0, 0))
        else: # PLAYING, COOKING, SUCCESS, GAME_OVER
            if self.bg_game:
                 self.window.blit(self.bg_game, (0, 0))
            else:
                 self.window.fill((255, 255, 255)) 

        if self.show_grid: 
            draw_grid_and_axes(self.window, self.GRID_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, self.debug_font)

        if self.game_state == "START_MENU":
            for ui_element in self.start_menu_ui:
                ui_element.draw()
            
        elif self.game_state in ["PLAYING", "GAME_OVER", "SUCCESS"]:
            self.draw_playing_ui()
            
            if self.game_state in ["GAME_OVER", "SUCCESS"]:
                # 결과 화면 오버레이 및 랭킹 표시
                dim_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                dim_surface.fill((0, 0, 0, 200))
                self.window.blit(dim_surface, (0, 0))
                
                if self.game_state == "SUCCESS":
                    msg = "MISSION SUCCESS!"
                    color = GREEN
                else:
                    msg = "GAME OVER"
                    color = RED
                    
                title_text = self.debug_font.render(msg, True, color)
                self.window.blit(title_text, (WINDOW_WIDTH//2 - 50, 100))
                
                # (v10) 랭킹 보드 그리기
                self.draw_leaderboard()
                
                restart_msg = self.debug_font.render("Click to Return to Menu", True, WHITE)
                self.window.blit(restart_msg, (WINDOW_WIDTH//2 - 70, 500))

        elif self.game_state == "COOKING":
            self.draw_playing_ui() 
            self.draw_cooking_popup() 

    # (v10) 랭킹 그리기 메서드 추가
    def draw_leaderboard(self):
        """저장된 기록 중 상위 5개(빠른 시간 순)를 화면에 그립니다."""
        ranking = self.saver.get_sorted_ranking()
        
        start_y = 180
        x_center = WINDOW_WIDTH // 2
        
        header = "Rank   |   Date   |   Time   |   Money"
        header_surf = self.debug_font.render(header, True, (255, 255, 0))
        header_rect = header_surf.get_rect(center=(x_center, start_y))
        self.window.blit(header_surf, header_rect)
        
        for i, record in enumerate(ranking):
            short_date = record['date'][5:] 
            row_str = f"{i+1}위   |   {short_date}   |   {record['time_taken']}s   |   ${record['money']}"
            row_surf = self.debug_font.render(row_str, True, WHITE)
            row_rect = row_surf.get_rect(center=(x_center, start_y + 40 * (i + 1)))
            self.window.blit(row_surf, row_rect)
            
        if not ranking:
            no_data = self.debug_font.render("No Success Records Yet", True, GRAY)
            self.window.blit(no_data, (x_center - 60, start_y + 50))

    def draw_playing_ui(self):
        """메인 게임 화면 UI 그리기"""
        if self.player_stock is None: return

        pygame.draw.rect(self.window, (220, 220, 220, 200), TRUCK_AREA_RECT, border_radius=10)
        pygame.draw.rect(self.window, (200, 200, 255, 200), DASHBOARD_RECT, border_radius=10)

        for grill in self.grills:
            grill.draw(self.window)
        
        for i, customer in enumerate(self.customers):
            if customer:
                if i == self.selected_customer_index:
                    pygame.draw.circle(self.window, (255, 220, 0), CUSTOMER_SLOT_POS[i], 45, 4) # 선택 원 크기 조정
                
                customer.draw()

        for button in self.playing_ui_elements:
            button.draw()
        
        for f_text in self.floating_texts:
            f_text.draw()
            
        # 텍스트 UI 업데이트 (setValue)
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.game_texts['time'].setValue(f"남은 시간: {int(self.game_timer)}초")
        self.game_texts['score'].setValue(f"매출: ${self.player_stock.money} / ${settings['target_revenue']}")
        self.game_texts['overcook'].setValue(f"오버쿡: {self.player_stock.overcook_count} / {settings['overcook_limit']}")
        
        recipe_text = "주문 대기 중... (손님 클릭)"
        customer = self.selected_customer 
        if customer and customer.order_list:
            recipe_text = f"선택: {customer.order_list[0].get_recipe()}"
        elif customer and not customer.order_list:
            recipe_text = "주문 완료! (선택됨)"
        self.game_texts['recipe'].setValue(recipe_text)
        
        current_stock = self.player_stock.get_stock_status()
        for item, count in current_stock.items():
            if f'stock_{item}' in self.game_texts:
                self.game_texts[f'stock_{item}'].setValue(f"{item}: {count}")
        
        for text_obj in self.game_texts.values():
            text_obj.draw()
            
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

    # --- 6. 메인 게임 루프 ---
    
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
                        clicked_customer = False
                        for i, pos in enumerate(CUSTOMER_SLOT_POS):
                            # 손님 이미지 크기에 맞춘 히트박스
                            customer_rect = pygame.Rect(pos[0] - 40, pos[1] - 40, 80, 80)
                            
                            if customer_rect.collidepoint(event.pos) and self.customers[i] is not None:
                                self.selected_customer = self.customers[i]
                                self.selected_customer_index = i
                                print(f"[선택] {i}번 손님 선택.")
                                clicked_customer = True
                                break 

                        if not clicked_customer:
                            for i, grill in enumerate(self.grills):
                                if grill.rect.collidepoint(event.pos):
                                    self.cb_click_grill(i)
                                    break 
                                    
                elif self.game_state == "COOKING":
                    for ui_element in self.cooking_ui_elements:
                        ui_element.handleEvent(event)
                
                elif self.game_state == "SUCCESS" or self.game_state == "GAME_OVER":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(f"[{self.game_state}] 상태에서 클릭. 시작 메뉴로 돌아갑니다.")
                        self.game_state = "START_MENU" 

            if self.game_state == "PLAYING":
                self.update_playing_state(dt)
            
            self.draw_screen()
            pygame.display.update()

        pygame.quit()
        sys.exit()


# --- 7. 실행 (중요) ---
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