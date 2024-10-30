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

    elif direc == 'DOWN':
        for x in range(3):
            for y in range(4):
                shift = 0
                for z in range(x + 1):
                    if board[3 - z][y] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - x + shift][y] = board[2 - x][y]
                    board[2 - x][y] = 0
                if 3 - x + shift <= 3:
                    if board[2 - x + shift][y] == board[3 - x + shift][y] and not merge[3 - x + shift][y] \
                            and not merge[2 - x + shift][y]:
                        board[3 - x + shift][y] *= 2
                        board[2 - x + shift][y] = 0
                        merge[3 - x + shift][y] = True

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



# spawn new pieces randomly
def new_pieces(board):
    count = 0
    full = True
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full



# spawn new pieces randomly
def new_pieces(board):
    count = 0
    full = True
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw bg for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    pass



# draw tiles
def draw_pieces(board):
    for x in range(4):
        for y in range(4):
            value = board[x][y]
            if value > 8:
                val_col = colors['light text']
            else:
                val_col = colors['dark text']

            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']

            pygame.draw.rect(screen, color, [y * 95 + 20, x * 95 + 20, 75, 75], 0, 5)

            if value > 0:
                val_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * val_len))
                val_txt = font.render(str(value), True, val_col)
                txt_rect = val_txt.get_rect(center=(y * 95 + 57, x * 95 + 57))
                screen.blit(val_txt, txt_rect)
                # box outline
                pygame.draw.rect(screen, 'black', [y * 95 + 20, x * 95 + 20, 75, 75], 2, 5)



# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_val)
    if spawn_new or init_count < 2:
        board_val, game_over = new_pieces(board_val)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_val = take_turn(direction, board_val)
        direction = ''
        spawn_new = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'

    pygame.display.flip()
pygame.quit()
