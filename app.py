import pygame
import sys
from settings import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = testBoard
        self.selected = None
        self.mousePos = None

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None

    def update(self):
        self.mousePos = pygame.mouse.get_pos()

    def draw(self):
        self.window.fill(WHITE)
        if self.selected:
            self.drawSelection(self.window, self.selected)
        self.drawGrid(self.window)
        pygame.display.update()

    def drawSelection(self, window, selected):
        pygame.draw.rect(
            window,
            LIGHTBLUE,
            (
                (selected[0] * cellSize) + gridPos[0],
                (selected[1] * cellSize) + gridPos[1],
                cellSize,
                cellSize
            )
        )

    def drawGrid(self, window):
        pygame.draw.rect(
            window,
            BLACK,
            (gridPos[0], gridPos[1], BOARD_WIDTH, BOARD_HEIGHT),
            2
        )

        for x in range(ROWS):
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

    def mouseOnGrid(self):
        x_onBoard = gridPos[0] < self.mousePos[0] < gridPos[0] + BOARD_WIDTH
        y_onBoard = gridPos[1] < self.mousePos[1] < gridPos[1] + BOARD_HEIGHT
        if not x_onBoard or not y_onBoard:
            return False
        else:
            row_x = (self.mousePos[0] - gridPos[0]) // cellSize
            row_y = (self.mousePos[1] - gridPos[1]) // cellSize
            return (row_x, row_y)
