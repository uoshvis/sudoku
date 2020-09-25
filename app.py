import pygame
import sys
from settings import *
from buttonClass import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = testBoard2
        self.selected = None
        self.mousePos = None
        self.state = 'playing'
        self.playingButtons = []
        self.menuButtons = []
        self. endButtons = []
        self.lockedCells = []
        self.font = pygame.font.SysFont('arial', cellSize // 2)
        self.load()


    def run(self):
        while self.running:
            if self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()

        sys.exit()
# Playing state functions

    def playing_events(self):
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

    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)

    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)

        if self.selected:
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.lockedCells)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)
        pygame.display.update()

# Helper functions

    def shadeLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(
                window,
                LOCKEDCELLCOLOUR,
                (
                    (cell[0] * cellSize) + gridPos[0],
                    (cell[1] * cellSize) + gridPos[1],
                    cellSize, cellSize)
            )

    def drawNumbers(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = [(xidx * cellSize) + gridPos[0], (yidx * cellSize) + gridPos[1]]
                    self.textToScreen(window, str(num), pos)

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
            2)

        for x in range(ROWS):
            # Vertical lines
            pygame.draw.line(
                window,
                BLACK,
                (gridPos[0] + (x * cellSize), gridPos[1]),
                (gridPos[0] + (x * cellSize), gridPos[1] + BOARD_HEIGHT),
                2 if x % 3 == 0 else 1)
            # Horizontal lines
            pygame.draw.line(
                window,
                BLACK,
                (gridPos[0], gridPos[1] + (x * cellSize)),
                (gridPos[0] + BOARD_WIDTH, gridPos[1] + (x * cellSize)),
                2 if x % 3 == 0 else 1)

    def mouseOnGrid(self):
        x_onBoard = gridPos[0] < self.mousePos[0] < gridPos[0] + BOARD_WIDTH
        y_onBoard = gridPos[1] < self.mousePos[1] < gridPos[1] + BOARD_HEIGHT
        if not x_onBoard or not y_onBoard:
            return False
        else:
            row_x = (self.mousePos[0] - gridPos[0]) // cellSize
            row_y = (self.mousePos[1] - gridPos[1]) // cellSize
            return (row_x, row_y)

    def loadButtons(self):
        self.playingButtons.append(Button(20, 40, 100, 40))

    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2
        window.blit(font, pos)

    def load(self):
        self.loadButtons()
        # Setting locked cells
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xidx, yidx])

