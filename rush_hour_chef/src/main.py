# main.py
import pygame
import sys
import random
from config import *
from ui_components import SimpleButton, SimpleText
from game_objects import FoodTruck, Hamburger, Cheeseburger, NormalCustomer, VIPCustomer

class GameClient:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.game_state = "START_MENU"
        self.player_truck = None
        self.menu_database = [Hamburger(), Cheeseburger()]
        self.current_customer = None
        self.game_timer = GAME_TIME_LIMIT
        self.difficulty = "normal"
        self.start_menu_buttons = []
        self.game_buttons = []
        self.game_texts = {}
        
        self._setup_start_menu_ui()

    # --- 1. 콜백 함수 정의 ---
    def start_game(self, difficulty):
        print(f"게임 시작: {difficulty} 난이도")
        self.difficulty = difficulty
        settings = DIFFICULTY_SETTINGS[difficulty]
        # FoodTruck 객체는 게임 시작 시 생성
        self.player_truck = FoodTruck(difficulty_settings=settings)
        self.game_timer = GAME_TIME_LIMIT
        self._setup_game_ui() # 게임 UI 생성
        self.game_state = "PLAYING"

    def cb_handle_ingredient(self, ingredient_name):
        if self.game_state == "PLAYING":
            self.player_truck.add_to_assembly(ingredient_name)

    def cb_handle_grill(self, action):
        if self.game_state == "PLAYING":
            if action == "패티 굽기":
                self.player_truck.start_grill()
            elif action == "패티 가져오기":
                status = self.player_truck.get_patty_from_grill()
                if status == "게임오버":
                    self.game_state = "GAME_OVER"

    def cb_handle_trash(self, _):
        if self.game_state == "PLAYING":
            self.player_truck.clear_assembly()

    # --- 2. UI 생성 ---
    def _setup_start_menu_ui(self):
        # ... (이전 코드와 동일, lambda x: self.start_game(...) 사용) ...
        self.start_menu_buttons.append(
            SimpleButton(self.screen, (300, 200), "EASY", 40, 200, 50, callBack=lambda x: self.start_game('easy'))
        )
        self.start_menu_buttons.append(
            SimpleButton(self.screen, (300, 300), "NORMAL", 40, 200, 50, callBack=lambda x: self.start_game('normal'))
        )
        self.start_menu_buttons.append(
            SimpleButton(self.screen, (300, 400), "HARD", 40, 200, 50, callBack=lambda x: self.start_game('hard'))
        )
    
    def _setup_game_ui(self):
        """ (***수정됨***) UI 생성 및 동적 텍스트 설정 """
        self.game_texts = {} # UI 초기화
        
        # 난이도별 목표/패널티 설정
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        target_revenue = settings['target_revenue']
        overcook_limit = settings['overcook_limit']
        
        # 텍스트 UI (동적으로 값 설정)
        self.game_texts['time'] = SimpleText(self.screen, TIME_UI_POS, f"{int(self.game_timer)}초", 30, BLACK, 'right')
        self.game_texts['difficulty'] = SimpleText(self.screen, DIFFICULTY_UI_POS, f"난이도: {self.difficulty}", 24, GRAY, 'right')
        self.game_texts['overcook'] = SimpleText(self.screen, OVERCOOK_UI_POS, f"오버쿡: 0 / {overcook_limit}", 30, RED, 'right')
        self.game_texts['score'] = SimpleText(self.screen, SCORE_UI_POS, f"매출: ${self.player_truck.money} / ${target_revenue}", 30, BLACK, 'left')
        self.game_texts['customer_order'] = SimpleText(self.screen, CUSTOMER_ORDER_POS, "손님 대기 중...", 28, BLUE, 'left')
        self.game_texts['assembly'] = SimpleText(self.screen, (ASSEMBLY_POS[0], ASSEMBLY_POS[1] - 30), f"조립대: {[]}", 20, BLACK, 'left')
        self.game_texts['grill'] = SimpleText(self.screen, (GRILL_POS[0], GRILL_POS[1] - 30), "그릴: 대기", 20, BLACK, 'left')
        
        # 재고 텍스트
        y_offset = STOCK_UI_POS[1]
        for item, count in self.player_truck.get_stock_status().items():
            self.game_texts[f'stock_{item}'] = SimpleText(self.screen, (STOCK_UI_POS[0], y_offset), f"{item}: {count}", 22, GRAY, 'left')
            y_offset += 30

        # 버튼 UI (재료)
        self.game_buttons = []
        btn_y = INGREDIENT_BUTTON_START_POS[1]
        btn_x = INGREDIENT_BUTTON_START_POS[0]
        self.game_buttons.append(SimpleButton(self.screen, (btn_x, btn_y), "빵(아래)", 20, 100, 40, callBack=self.cb_handle_ingredient))
        self.game_buttons.append(SimpleButton(self.screen, (btn_x + 110, btn_y), "양상추", 20, 100, 40, callBack=self.cb_handle_ingredient))
        self.game_buttons.append(SimpleButton(self.screen, (btn_x + 220, btn_y), "치즈", 20, 100, 40, callBack=self.cb_handle_ingredient))
        self.game_buttons.append(SimpleButton(self.screen, (btn_x + 330, btn_y), "빵(위)", 20, 100, 40, callBack=self.cb_handle_ingredient))
        
        # 버튼 UI (조리대)
        self.game_buttons.append(SimpleButton(self.screen, (GRILL_POS[0], GRILL_BUTTON_POS[1]), "패티 굽기", 20, 120, 40, callBack=self.cb_handle_grill))
        self.game_buttons.append(SimpleButton(self.screen, (GRILL_POS[0], GRILL_BUTTON_POS[1] + 50), "패티 가져오기", 20, 120, 40, callBack=self.cb_handle_grill))
        self.game_buttons.append(SimpleButton(self.screen, (TRASH_POS[0], TRASH_BUTTON_POS[1]), "비우기", 20, 120, 80, callBack=self.cb_handle_trash))

    # --- 3. 게임 루프 ---
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0 
            
            # 3-1. 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.game_state == "START_MENU":
                    for button in self.start_menu_buttons:
                        button.handleEvent(event)
                
                elif self.game_state == "PLAYING":
                    for button in self.game_buttons:
                        button.handleEvent(event)

            # 3-2. 상태 업데이트
            if self.game_state == "PLAYING":
                self.update_playing_state(dt)
            
            # 3-3. 화면 그리기
            self.draw_screen()
            
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def update_playing_state(self, dt):
        """ (***수정됨***) 게임 로직 및 UI 텍스트 갱신 """
        self.game_timer -= dt
        self.player_truck.update_grill(dt) 

        # --- 손님 로직 ---
        if self.current_customer is None:
            settings = DIFFICULTY_SETTINGS[self.difficulty]
            # (수정) 난이도별 customer_count를 기반으로 스폰 확률 계산
            # 예: normal 5명 -> 300초 / 5명 = 60초. 1/FPS/60 보다 낮게
            # 여기서는 간단하게 5초에 한 명꼴로 시도
            spawn_chance = dt / 5.0 
            
            if random.random() < spawn_chance:
                if random.random() < 0.2: # 20% VIP (이벤트)
                    self.current_customer = VIPCustomer(wait_time=30 * settings['wait_time_factor'])
                else:
                    self.current_customer = NormalCustomer(wait_time=40 * settings['wait_time_factor'])
                
                order_item = self.current_customer.order(self.menu_database)[0]
                self.player_truck.set_new_order(order_item.get_recipe())
                self.game_texts['customer_order'].setValue(f"주문: {order_item.name} 1개!")
        
        else:
            self.current_customer.wait_timer -= dt
            if self.current_customer.wait_timer <= 0:
                print("손님이 기다리다 떠났습니다! (패널티)")
                if self.player_truck.add_overcook() == "GAME_OVER":
                    self.game_state = "GAME_OVER"
                self.current_customer = None
                self.player_truck.clear_assembly()
                self.game_texts['customer_order'].setValue("손님 대기 중...")

        # --- 버거 완성 체크 및 판매 ---
        if self.player_truck.assembly_station == self.player_truck.current_order_recipe and self.player_truck.current_order_recipe:
            print("--- 버거 판매 성공! ---")
            order_item = self.current_customer.order_list[0] 
            
            revenue = self.current_customer.pay(order_item.get_price()) # 다형성
            self.player_truck.earn(revenue) # 캡슐화
            
            self.current_customer = None 
            self.player_truck.set_new_order([]) 
            self.game_texts['customer_order'].setValue("손님 대기 중...")
            
        # --- 종료 조건 검사 (***수정됨***) ---
        target_revenue = DIFFICULTY_SETTINGS[self.difficulty]['target_revenue']
        if self.game_timer <= 0:
            if self.player_truck.money < target_revenue:
                self.game_state = "GAME_OVER"
            else:
                self.game_state = "SUCCESS" # 시간 종료 시 돈 넘었으면 성공

        if self.game_state != "GAME_OVER" and self.player_truck.money >= target_revenue:
             # (v2) 재고까지 다 팔았는지 체크 (기획안)
            current_stock = self.player_truck.get_stock_status()
            if sum(current_stock.values()) == 0:
                 self.game_state = "SUCCESS"
            # (v2) 여기서는 돈만 넘으면 성공으로 간주 (간략화)
            # self.game_state = "SUCCESS" # -> 돈만 넘으면 성공
        
        # --- UI 텍스트 업데이트 ---
        self.game_texts['time'].setValue(f"남은 시간: {int(self.game_timer)}초")
        self.game_texts['score'].setValue(f"매출: ${self.player_truck.money} / ${target_revenue}")
        self.game_texts['overcook'].setValue(f"오버쿡: {self.player_truck.overcook_count} / {DIFFICULTY_SETTINGS[self.difficulty]['overcook_limit']}")
        self.game_texts['assembly'].setValue(f"조립: {self.player_truck.assembly_station}")
        grill_status_text = f"그릴: {self.player_truck.grill_state}"
        if self.player_truck.grill_state == "조리중":
            grill_status_text += f" ({self.player_truck.grill_timer:.1f}초)"
        self.game_texts['grill'].setValue(grill_status_text)
        
        current_stock = self.player_truck.get_stock_status()
        for item, count in current_stock.items():
            if f'stock_{item}' in self.game_texts:
                self.game_texts[f'stock_{item}'].setValue(f"{item}: {count}")

    def draw_screen(self):
        """ (***수정됨***) 스케치에 맞게 UI 그리기 """
        self.screen.fill(WHITE)

        if self.game_state == "START_MENU":
            title_text = SimpleText(self.screen, (WINDOW_WIDTH//2, 100), "러시아워 셰프", 60, BLACK, 'center')
            title_text.draw()
            for button in self.start_menu_buttons:
                button.draw()
            
        elif self.game_state in ["PLAYING", "GAME_OVER", "SUCCESS"]:
            # 조리대 배경 (스케치 기반)
            pygame.draw.rect(self.screen, BROWN, (*ASSEMBLY_POS, 150, 100)) # 조립대
            pygame.draw.rect(self.screen, DARK_GRAY, (*GRILL_POS, 150, 100)) # 그릴
            pygame.draw.rect(self.screen, GRAY, (*TRASH_POS, 150, 100)) # 쓰레기통

            # 버튼 그리기
            for button in self.game_buttons:
                button.draw()
            
            # 텍스트 그리기
            for text_obj in self.game_texts.values():
                text_obj.draw()
            
            # 손님 대기 시간 바
            if self.current_customer and self.game_state == "PLAYING":
                wait_ratio = self.current_customer.wait_timer / self.current_customer.wait_time
                bar_width = 300 * wait_ratio
                if bar_width > 0:
                    pygame.draw.rect(self.screen, RED, (CUSTOMER_ORDER_POS[0], CUSTOMER_ORDER_POS[1] + 40, bar_width, 10))

            # 게임 상태 메시지
            if self.game_state == "GAME_OVER":
                msg = SimpleText(self.screen, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "GAME OVER", 80, RED, 'center')
                msg.draw()
            elif self.game_state == "SUCCESS":
                msg = SimpleText(self.screen, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "SUCCESS!", 80, GREEN, 'center')
                msg.draw()

# --- 6. 실행 (수정됨) ---
# Pygame 초기화 및 전역 변수 생성을 '먼저' 수행합니다.
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("러시아워 셰프")
clock = pygame.time.Clock()

# `screen`과 `clock`이 생성된 후에 `GameClient` 객체를 만듭니다.
if __name__ == "__main__":
    game = GameClient(screen, clock)
    game.run()