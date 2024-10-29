import pygame
import random

pygame.init()

# Initial setup
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# Color lib
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 184, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'bg': (187, 173, 160)}

# variables
board_val = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''

# taking turns in form of directions
def take_turn(direc, board):
    merge = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for x in range(4):
            for y in range(4):
                shift = 0
                if x > 0:
                    for z in range(x):
                        if board[z][y] == 0:
                            shift += 1
                    if shift > 0:
                        board[x - shift][y] = board[x][y]
                        board[x][y] = 0
                    if board[x - shift - 1][y] == board[x - shift][y] and not merge[x - shift - 1][y] \
                            and not merge[x - shift][y]:
                        board[x - shift - 1][y] *= 2
                        board[x - shift][y] = 0
                        merge[x - shift - 1][y] = True

    elif direc == 'LEFT ':
        for x in range(4):
            for y in range(4):
                shift = 0
                for z in range(y):
                    if board[x][z] == 0:
                        shift += 1
                if shift > 0:
                    board[x][y - shift] = board[x][y]
                    board[x][y] = 0
                if board[x][y - shift] == board[x][y - shift - 1] and not merge[x][y - shift - 1] \
                        and not merge[x][y - shift]:
                    board[x][y - shift - 1] *= 2
                    board[x][y - shift] = 0
                    merge[x][y - shift - 1] = True
                    
    elif direc == 'RIGHT':
        pass


    return board
