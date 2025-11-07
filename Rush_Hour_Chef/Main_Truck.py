# 모든 것을 실행하는 메인 파일 (중앙통제소)
import pygame
from CL_Difficulty_Button import *
from FC_Grid import draw_grid_and_axes  # 그리드 함수를 임포트
from CL_Logo import Logo

# 화면 옵션 설정
WINDOW_W = 1080; WINDOW_H = 680
FPS = 60
GRID_SIZE = 50  

pygame.init()
debug_font = pygame.font.SysFont('Arial', 14) 

window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
clock = pygame.time.Clock()

background_image = pygame.image.load('Rush_Hour_Chef/Assets/Wallpaper.png').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_W, WINDOW_H))


easy_button = Easy_Button(window, (WINDOW_W // 2, 400), 200) # 이지 버튼 객체 생성
normal_button = Normal_Button(window, (WINDOW_W // 2, 500), 200) # 노말 버튼 객체 생성
hard_button = Hard_Button(window, (WINDOW_W // 2, 600), 200) # 하드 버튼 객체 생성

logo_url = "https://github.com/39byte/OOP_Project/tree/master"
logo = Logo(window, (WINDOW_W // 2, 180), 400, logo_url)

show_grid = False 

# ========== 실행 코드 ==========
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g: 
                show_grid = not show_grid 

        easy_button.handleEvent(event)
        normal_button.handleEvent(event)
        hard_button.handleEvent(event)
        logo.handleEvent(event)

    # 화면 갱신
    window.blit(background_image, (0, 0)) 

    if show_grid: 
        draw_grid_and_axes(window, GRID_SIZE, WINDOW_W, WINDOW_H, debug_font)

    easy_button.draw()
    normal_button.draw()
    hard_button.draw()
    logo.draw()
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()