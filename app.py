import pygame
import sys
from time import sleep

from buttonClass import Button
from settings import *
from solver import valid


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = testBoard3
        self.selected = None
        self.mousePos = None
        self.finished = False
        self.cellChanged = False
        self.incorrectCellsExist = False
        self.playingButtons = []
        self.lockedCells = []
        self.incorrectCells = []
        self.font = pygame.font.SysFont('arial', cellSize // 2)
        self.load()

    def run(self):
        while self.running:
            if not self.finished:
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            if self.finished:
                sleep(3)
                self.running = False
        pygame.quit()

        sys.exit()

# Playing state functions

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # User clicks
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playingButtons:
                        if button.highlighted:
                            button.click()

            # User types a key
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.lockedCells:
                    if self.isInt(event.unicode):
                        # Cell changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChanged = True
                    if event.key == pygame.K_DELETE:
                        self.grid[self.selected[1]][self.selected[0]] = 0
                        if [self.selected[0], self.selected[1]] in self.incorrectCells:
                            self.incorrectCells.remove([self.selected[0], self.selected[1]])
                        self.cellChanged = True

    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)

        if self.cellChanged and self.checkAllCellsDone():
            self.checkAllCells()
            if len(self.incorrectCells) == 0:
                self.incorrectCellsExist = False
                self.finished = True
            else:
                self.incorrectCellsExist = True

    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)

        if self.selected:
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeIncorrectCells(self.window, self.incorrectCells)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)

        if self.incorrectCellsExist:
            text = self.font.render("Wrong cells exist", 1, RED)
            self.window.blit(text, (WIDTH // 3, 40))
        if self.finished:
            text = self.font.render("You are smart! Bye.", 1, RED)
            self.window.blit(text, (WIDTH // 3, 40))

        pygame.display.update()

        self.changed = False

# Board checking functions

    def checkAllCells(self):
        print('Checking all cells')
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if [row, col] not in self.lockedCells:
                    value = self.grid[col][row]
                    if value != 0 and not valid(self.grid, value, (col, row)):
                        if [row, col] not in self.incorrectCells:
                            self.incorrectCells.append([row, col])
                    elif value != 0 and valid(self.grid, value, (col, row)):
                        if [row, col] in self.incorrectCells:
                            self.incorrectCells.remove([row, col])
        self.cellChanged = False

    def checkAllCellsDone(self):
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

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

    def shadeIncorrectCells(self, window, incorrectCells):
        for cell in incorrectCells:
            pygame.draw.rect(
                window,
                INCORRECTCELLCOLOUR,
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
            (gridPos[0], gridPos[1], BOARD_WIDTH, BOARD_HEIGHT), 2)

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
        self.playingButtons.append(Button(20, 40, WIDTH // 7, 40,
                                          function=self.checkAllCells,
                                          colour=(27, 142, 207),
                                          text='Check'))

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

    def isInt(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False
