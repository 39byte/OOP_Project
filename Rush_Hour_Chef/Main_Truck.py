# 모든 것을 실행하는 메인 파일 (중앙통제소)
import pygame
from FC_Grid import DebugGrid
from CL_Kitchen_Interface import *

# 화면 옵션 설정
WINDOW_W = 1080; WINDOW_H = 680
FPS = 60
GRID_SIZE = 50  

pygame.init()
# 폰트 설정
debug_font = pygame.font.SysFont('Arial', 14) 

window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
clock = pygame.time.Clock()

# 배경 이미지 불러오고 창 크기로 변환
background_image = pygame.image.load('Rush_Hour_Chef/Assets/Truck_kitchen/BasyWall.png').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_W, WINDOW_H))

# 객체화
debug_grid = DebugGrid(window, GRID_SIZE, WINDOW_W, WINDOW_H, debug_font)       # 그리드
truck_floor = Truck_Floor(window, (50, 300), (750, 350))
dash_board = DashBoard(window, (1050, 300), (225, 350))     # topright가 기준
kitchen = Kitchen(window, (75, 325), (525, 150))
grill = Grill(window, (75, 325), (325, 150))
timer = Timer(window, (1050, 50), (225, 100))       # topright

sit_1 = Customer_Sit(window, (700, 200), (50,50))
sit_2 = Customer_Sit(window, (500, 200), (50,50))
sit_3 = Customer_Sit(window, (300, 200), (50,50))
sit_4 = Customer_Sit(window, (100, 200), (50,50))

show_grid = True       # 그리드 기본 상태

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

    # 화면 갱신
    window.blit(background_image, (0, 0)) 

    # 그리드 그리기
    if show_grid: debug_grid.draw()
    
    # 인터페이스 그리기
    truck_floor.draw()
    dash_board.draw()
    kitchen.draw()
    grill.draw()
    timer.draw()
    sit_1.draw(); sit_2.draw(); sit_3.draw(); sit_4.draw()
        
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()