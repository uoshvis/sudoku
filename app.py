import pygame
import sys
from settings import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = testBoard
        self.rows = 9

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        self.window.fill(WHITE)
        self.drawGrid(self.window)
        pygame.display.update()

    def drawGrid(self, window):
        pygame.draw.rect(
            window,
            BLACK,
            (gridPos[0], gridPos[1], BOARD_WIDTH, BOARD_HEIGHT),
            2
        )

        for x in range(self.rows):
            if x % 3 == 0:
                thick = 2
            else:
                thick = 1
            # Vertical lines
            pygame.draw.line(
                window,
                BLACK,
                (gridPos[0] + (x * cellSize), gridPos[1]),
                (gridPos[0] + (x * cellSize), gridPos[1] + BOARD_HEIGHT),
                thick
            )
            # Horizontal lines
            pygame.draw.line(
                window,
                BLACK,
                (gridPos[0], gridPos[1] + (x * cellSize)),
                (gridPos[0] + BOARD_WIDTH, gridPos[1] + (x * cellSize)),
                thick
            )
