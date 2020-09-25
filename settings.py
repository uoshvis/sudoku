# Main window size
WIDTH = 600
HEIGHT = 600
ROWS = 9


# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (100, 200, 230)
LOCKEDCELLCOLOUR = (190, 190, 190)

# Boards

testBoard1 = [[0 for x in range(9)] for x in range(9)]
testBoard2 = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
              [6, 0, 0, 0, 7, 5, 0, 0, 9],
              [0, 0, 0, 6, 0, 1, 0, 7, 8],
              [0, 0, 7, 0, 4, 0, 2, 6, 0],
              [0, 0, 1, 0, 5, 0, 9, 3, 0],
              [9, 0, 4, 0, 6, 0, 0, 0, 5],
              [0, 7, 0, 3, 0, 0, 0, 1, 2],
              [1, 2, 0, 0, 0, 7, 4, 0, 0],
              [0, 4, 9, 2, 0, 6, 0, 0, 7]]

# Positions and sizes
BOARD_WIDTH = 450
BOARD_HEIGHT = 450
gridPos = (75, 100)
cellSize = 50
GRIDSIZE = cellSize * ROWS
