# config.py
import pygame

# --- 게임 기본 설정 ---
WINDOW_WIDTH = 800      # 창 너비
WINDOW_HEIGHT = 600     # 창 높이
FPS = 30                # 게임 프레임
GAME_TIME_LIMIT = 300   # 게임 제한 시간

# --- 난이도별 설정 ---
DIFFICULTY_SETTINGS = {
    'easy': { 'target_revenue': 300,        # 목표 매출액
             'customer_count_avg_sec': 5,   # 손님 평균 젠 시간
             'wait_time_factor': 1.5,       # 손님 대기 시간 배율 (기본보다 1.5배 더 대기)
             'overcook_limit': 7 },         # 오버쿡 허용 회수

    'normal': { 'target_revenue': 400,      
               'customer_count_avg_sec': 3, 
               'wait_time_factor': 1.0, 
               'overcook_limit': 5 },

    'hard': { 'target_revenue': 500, 
             'customer_count_avg_sec': 2, 
             'wait_time_factor': 0.7, 
             'overcook_limit': 3 }
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
POPUP_BG_COLOR = (240, 240, 240)    # 팝업창 색깔
POPUP_DIM_COLOR = (0, 0, 0, 180)    # 조리 팝업 뒤 배경 어둡게 처리할 때 뿌릴 색 (반투명)

# 재료 1개 살 때 소모되는 비용
STOCK_PURCHASE_COST = 1

# 폰트 경로
FONT_PATH = 'assets/fonts/NanumGothicBold.ttf' 

# --- UI 위치 ---
# 손님 서있는 위치
CUSTOMER_SLOT_POS = [(100, 225), (300, 225), (500, 225), (700, 225)]
TIME_UI_POS = (780, 20)         # 남은 시간 표시 위치
DIFFICULTY_UI_POS = (780, 50)   # 난이도 표시 위치
OVERCOOK_UI_POS = (780, 80)     # 오버쿡 횟수 표시

# 푸드트럭
TRUCK_AREA_RECT = pygame.Rect(40, 300, 570, 280)                # 푸드트럭 영역
GRILL_SLOT_POS = [(60, 360), (160, 360), (60, 460), (160, 460)] # 화로 위치
ASSEMBLY_STATION_POS = (280, 350)   # 조립대 위치
STOCK_BUTTONS_POS = (515, 350)      # 재료 보충 버튼 위치

# 대시보드
DASHBOARD_RECT = pygame.Rect(610, 300, 180, 280) # 대시보드 영역
DASHBOARD_SCORE_POS = (620, 310)    # 매출액 텍스트 위치
DASHBOARD_STOCK_POS = (620, 370)    # 재고 목록 텍스트 시작 위치

# 조리 팝업
POPUP_RECT = pygame.Rect(100, 100, 600, 400)    # 조립 팝업 영역
POPUP_ASSEMBLY_POS = (150, 150)     # 팝업 내 조립대 위치
POPUP_INGREDIENT_POS = (450, 150)   # 팝업 내 재료 버튼들 위치
POPUP_TRASH_POS = (195, 390)        # 쓰레기통 위치
POPUP_CLOSE_POS = (550, 110)        # 닫기 버튼 위치