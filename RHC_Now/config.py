# config.py
import pygame

# --- 게임 기본 설정 ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
GAME_TIME_LIMIT = 300 # 5분

# --- 난이도별 설정 ---
DIFFICULTY_SETTINGS = {
    'easy': { 'target_revenue': 300, 'customer_count_avg_sec': 5, 'wait_time_factor': 1.5, 'overcook_limit': 7 },
    'normal': { 'target_revenue': 400, 'customer_count_avg_sec': 3, 'wait_time_factor': 1.0, 'overcook_limit': 5 },
    'hard': { 'target_revenue': 500, 'customer_count_avg_sec': 2, 'wait_time_factor': 0.7, 'overcook_limit': 3 }
}

# --- 색상 정의 ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BROWN = (139, 69, 19)
POPUP_BG_COLOR = (240, 240, 240)
POPUP_DIM_COLOR = (0, 0, 0, 180) 

STOCK_PURCHASE_COST = 1# 재료 1개당 비용
# --- 폰트 경로 (한글 깨짐 해결) ---
FONT_PATH = r'C:\HUFS_Project\RHC_Now\assets\fonts\NanumGothicBold.ttf' 

# --- UI 위치 (***수정됨***) ---
# 메인 화면
CUSTOMER_SLOT_POS = [(100, 100), (250, 100), (400, 100), (550, 100)]
TIME_UI_POS = (780, 20)
DIFFICULTY_UI_POS = (780, 50)
OVERCOOK_UI_POS = (780, 80)

# (v6) 푸드트럭 영역 크기/위치 조정
TRUCK_AREA_RECT = pygame.Rect(40, 300, 570, 280) # 너비 720 -> 570
GRILL_SLOT_POS = [(60, 360), (160, 360), (60, 460), (160, 460)] 
ASSEMBLY_STATION_POS = (280, 350)
STOCK_BUTTONS_POS = (450, 350) 

# (v6) 대시보드 영역 위치 조정
DASHBOARD_RECT = pygame.Rect(610, 300, 180, 280) # 너비 160 -> 170 (매출 잘림 방지)
DASHBOARD_SCORE_POS = (620, 310)
DASHBOARD_STOCK_POS = (620, 370)

# 조리 팝업 (COOKING 상태)
POPUP_RECT = pygame.Rect(100, 100, 600, 400)
POPUP_ASSEMBLY_POS = (150, 150)
POPUP_INGREDIENT_POS = (450, 150) 
POPUP_TRASH_POS = (450, 400)
POPUP_CLOSE_POS = (680, 110)