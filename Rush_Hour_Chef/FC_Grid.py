# 디버깅용 그리드와 좌표계를 그리는 모듈

import pygame

def draw_grid_and_axes(window, grid_size, window_w, window_h, font):
    """디버깅용 그리드, 좌표, 중심축을 그립니다."""
    GRID_COLOR = (150, 150, 150)  # 격자 색상 (회색)
    AXIS_COLOR = (255, 0, 0)      # 중심축 색상 (빨간색)
    TEXT_COLOR = (0, 0, 0)        # 좌표 텍스트 색상 (검은색)

    # 1. 세로줄 (X좌표)
    for x in range(0, window_w, grid_size):
        pygame.draw.line(window, GRID_COLOR, (x, 0), (x, window_h))
        text = font.render(str(x), True, TEXT_COLOR)
        window.blit(text, (x + 2, 5)) # 좌표 텍스트 (상단)

    # 2. 가로줄 (Y좌표)
    for y in range(0, window_h, grid_size):
        pygame.draw.line(window, GRID_COLOR, (0, y), (window_w, y))
        text = font.render(str(y), True, TEXT_COLOR)
        window.blit(text, (5, y + 2)) # 좌표 텍스트 (좌측)

    # 3. 중심축 (빨간색)
    center_x = window_w // 2
    center_y = window_h // 2
    pygame.draw.line(window, AXIS_COLOR, (center_x, 0), (center_x, window_h), 2) # 세로축
    pygame.draw.line(window, AXIS_COLOR, (0, center_y), (window_w, center_y), 2) # 가로축