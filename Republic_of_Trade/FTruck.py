import pygame

# 화면 옵션 설정
BLACK = (0,0,0)
WINDOW_W = 920; WINDOW_H = 680
FPS = 60

pygame.init()
window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
clock = pygame.time.Clock()

# 실행 코드
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 갱신
    window.fill(BLACK)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit