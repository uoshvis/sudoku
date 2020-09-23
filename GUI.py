import pygame
import time
pygame.font.init()


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height


def redraw_window(win, board, play_time, strikes):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont('comicsans', 40)
    # Draw time
    text = fnt.render("Time: " + format_time(play_time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    # Draw strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    time_str = ' ' + str(minute) + ':' + str(sec)

    return time_str


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption('Sudoku')
    board = Grid(9, 9, 540, 540)
    start = time.time()
    strikes = 0
    running = True

    while running:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    running = False

                if event.key == pygame.K_RETURN:
                    strikes += 1

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
