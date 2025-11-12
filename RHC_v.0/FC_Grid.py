# 디버깅용 그리드
import pygame

class DebugGrid:
    def __init__(self, window, grid_size, window_w, window_h, font):
        self.window = window
        self.grid_size = grid_size
        self.window_w = window_w
        self.window_h = window_h
        self.font = font

        # 색상 값을 클래스 속성으로 관리
        self.GRID_COLOR = (150, 150, 150)  # 격자 색상 (회색)
        self.AXIS_COLOR = (255, 0, 0)      # 중심축 색상 (빨간색)
        self.TEXT_COLOR = (0, 0, 0)        # 좌표 텍스트 색상 (검은색)

    def draw(self):
        """그리드와 좌표축을 화면에 그립니다."""
        
        # 1. 세로줄 (X좌표)
        for x in range(0, self.window_w, self.grid_size):
            pygame.draw.line(self.window, self.GRID_COLOR, (x, 0), (x, self.window_h))
            text = self.font.render(str(x), True, self.TEXT_COLOR)
            self.window.blit(text, (x + 2, 5)) # 좌표 텍스트 (상단)

        # 2. 가로줄 (Y좌표)
        for y in range(0, self.window_h, self.grid_size):
            pygame.draw.line(self.window, self.GRID_COLOR, (0, y), (self.window_w, y))
            text = self.font.render(str(y), True, self.TEXT_COLOR)
            self.window.blit(text, (5, y + 2)) # 좌표 텍스트 (좌측)

        # 3. 중심축 (빨간색)
        center_x = self.window_w // 2
        center_y = self.window_h // 2
        pygame.draw.line(self.window, self.AXIS_COLOR, (center_x, 0), (center_x, self.window_h), 2) # 세로축
        pygame.draw.line(self.window, self.AXIS_COLOR, (0, center_y), (self.window_w, center_y), 2) # 가로축