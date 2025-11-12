# 모든 것을 실행하는 메인 파일 (중앙통제소)
import pygame
from CL_Difficulty_Button import * # 난이도 버튼 임포트
from FC_Grid import DebugGrid           # 그리드 '클래스' 임포트
from CL_Logo import Logo                # 로고 표시 (이스터에그)

# 화면 옵션 설정
WINDOW_W = 1080; WINDOW_H = 680; FPS = 60
GRID_SIZE = 50  

pygame.init()
debug_font = pygame.font.SysFont('Arial', 14)       # 폰트 설정

window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
clock = pygame.time.Clock()

# 배경 이미지 불러오고 창 크기로 변환
background_image = pygame.image.load('Rush_Hour_Chef/Assets/Wallpaper.png').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_W, WINDOW_H))

# 난이도 버튼 객체 생성
easy_button = Easy_Button(window, (WINDOW_W // 2, 400), 200)        # 이지 버튼 객체 생성
normal_button = Normal_Button(window, (WINDOW_W // 2, 500), 200)    # 노말 버튼 객체 생성
hard_button = Hard_Button(window, (WINDOW_W // 2, 600), 200)        # 하드 버튼 객체 생성

# 로고 객체 생성
logo_url = "https://github.com/39byte/OOP_Project/tree/master"
logo = Logo(window, (WINDOW_W // 2, 180), 400, logo_url)

# 그리드 객체 생성 (초기화)
debug_grid = DebugGrid(window, GRID_SIZE, WINDOW_W, WINDOW_H, debug_font)

show_grid = False 

# ========== 실행 코드 ==========
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # G키 누르면 그리드 펼치기
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g: 
                show_grid = not show_grid 
        
        # 난이도 버튼 코드 실행
        easy_button.handleEvent(event)
        normal_button.handleEvent(event)
        hard_button.handleEvent(event)

        # 로고 버튼 코드 실행
        logo.handleEvent(event)

    # 화면 갱신
    window.blit(background_image, (0, 0)) 

    # 그리드 펼쳐져 있으면 화면에 출력
    if show_grid: debug_grid.draw()
        
    # 버튼, 로고 그리기
    easy_button.draw()
    normal_button.draw()
    hard_button.draw()
    logo.draw()
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()