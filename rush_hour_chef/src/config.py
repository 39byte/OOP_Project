# config.py
import pygame

# --- 게임 기본 설정 ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30
GAME_TIME_LIMIT = 300 # 5분 (300초)

# --- 난이도별 설정 (***수정됨***) ---
DIFFICULTY_SETTINGS = {
    'easy': {
        'target_revenue': 500, # 목표 매출 (50 -> 500)
        'customer_count': 3,
        'wait_time_factor': 1.5,
        'overcook_limit': 7
    },
    'normal': {
        'target_revenue': 1000, # (100 -> 1000)
        'customer_count': 5,
        'wait_time_factor': 1.0,
        'overcook_limit': 5
    },
    'hard': {
        'target_revenue': 2000, # (200 -> 2000)
        'customer_count': 7,
        'wait_time_factor': 0.7,
        'overcook_limit': 3
    }
}

# --- 색상 정의 ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BROWN = (139, 69, 19) # 조립대

# --- 폰트 경로 (한글 깨짐 해결) ---
FONT_PATH = 'assets/fonts/NanumGothicBold.ttf' # 이 파일이 필요합니다.

# --- UI 위치 (***전면 수정됨***) ---
# 스케치 기반 재배치
TIME_UI_POS = (780, 20)           # 우상단 (시간)
DIFFICULTY_UI_POS = (780, 50)     # 우상단 (난이도)
OVERCOOK_UI_POS = (780, 80)       # 우상단 (오버쿡)
SCORE_UI_POS = (20, 560)          # 좌하단 (매출)
STOCK_UI_POS = (550, 480)         # 우하단 (재고)
CUSTOMER_ORDER_POS = (20, 20)     # 좌상단 (손님)

# 조리대
ASSEMBLY_POS = (50, 350)          # 조립대 (갈색 상자)
GRILL_POS = (250, 350)            # 그릴 (검은 상자)
TRASH_POS = (450, 350)            # 쓰레기통 (회색 상자)

# 버튼
INGREDIENT_BUTTON_START_POS = (50, 480) # 재료 버튼 시작 위치
GRILL_BUTTON_POS = (250, 400)
TRASH_BUTTON_POS = (450, 400)