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

# Constants
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
TILE_PADDING = 10

# Initialize grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def draw_grid():
    """Draw the grid and tiles."""
    screen.fill(colors['bg'])
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            color = colors[value] if value in colors else colors['other']
            text_color = colors['light text'] if value > 4 else colors['dark text']
            
            # Draw the tile
            pygame.draw.rect(screen, color, 
                             (col * TILE_SIZE + TILE_PADDING, row * TILE_SIZE + TILE_PADDING, 
                              TILE_SIZE - TILE_PADDING * 2, TILE_SIZE - TILE_PADDING * 2), 0)

            # Draw the number on the tile
            if value != 0:
                text = font.render(str(value), True, text_color)
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2,
                                                  row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)


def add_new_tile():
    """Add a new 2 or 4 tile at a random empty location."""
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        grid[row][col] = random.choice([2, 4])


def rotate_grid_clockwise():
    """Rotate the grid 90 degrees clockwise to handle all directions using the same logic."""
    return [[grid[GRID_SIZE - c - 1][r] for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]


def move_left():
    """Handle the leftward movement and merging of tiles."""
    moved = False
    for row in grid:
        # Filter out non-zero values and shift tiles to the left
        tiles = [num for num in row if num != 0]
        merged_tiles = []
        skip = False
        
        # Merge tiles
        for i in range(len(tiles)):
            if skip:
                skip = False
                continue
            if i != len(tiles) - 1 and tiles[i] == tiles[i + 1]:
                merged_tiles.append(tiles[i] * 2)
                skip = True
            else:
                merged_tiles.append(tiles[i])
        
        # Add zeros to maintain row length
        merged_tiles += [0] * (GRID_SIZE - len(merged_tiles))
        
        if row != merged_tiles:
            moved = True
        row[:] = merged_tiles
    
    return moved


def move(direction):
    """Move the grid in the given direction and add a new tile if tiles moved."""
    moved = False
    for _ in range(direction):
        grid[:] = rotate_grid_clockwise()
    
    if move_left():
        moved = True
    
    for _ in range((4 - direction) % 4):
        grid[:] = rotate_grid_clockwise()
    
    if moved:
        add_new_tile()


def check_game_over():
    """Check if there are no valid moves left."""
    for row in grid:
        if 0 in row:
            return False
    
    for row in grid:
        for col in range(GRID_SIZE - 1):
            if grid[row][col] == grid[row][col + 1]:
                return False
    
    for row in range(GRID_SIZE - 1):
        for col in range(GRID_SIZE):
            if grid[row][col] == grid[row + 1][col]:
                return False
    
    return True


def main():
    """Main game loop."""
    add_new_tile()
    add_new_tile()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move(0)  # Move left
                elif event.key == pygame.K_RIGHT:
                    move(2)  # Move right
                elif event.key == pygame.K_UP:
                    move(1)  # Move up
                elif event.key == pygame.K_DOWN:
                    move(3)  # Move down
        
        draw_grid()
        pygame.display.update()
        
        if check_game_over():
            print("Game Over!")
            running = False
        
        timer.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
