import pygame

# Constants
CELL_SIZE = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)  # Player's board color
ORANGE = (255, 165, 0)  # AI's board color for hits/misses

def initialize_screen(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Battleship Multiplayer (Player vs AI)")
    return screen

def draw_grid(screen, grid, offset=0):
    for row in range(10):
        for col in range(10):
            rect = pygame.Rect(col * CELL_SIZE + offset, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 0:  # Empty
                pygame.draw.rect(screen, BLUE, rect)
            elif grid[row][col] == 1:  # Ship
                pygame.draw.rect(screen, GRAY, rect)
            elif grid[row][col] == 2:  # Hit
                pygame.draw.rect(screen, RED, rect)  # Mark hits in red
            elif grid[row][col] == 3:  # Miss
                pygame.draw.rect(screen, WHITE, rect)  # Mark misses in white
            pygame.draw.rect(screen, BLACK, rect, 1)  # Grid lines

def update_display(screen):
    pygame.display.flip()


def handle_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def handle_mouse_click(pos, offset=0):
    """Returns the row and col based on where the player clicked."""
    x, y = pos
    if x >= offset and x < offset + 10 * CELL_SIZE:
        col = (x - offset) // CELL_SIZE
        row = y // CELL_SIZE
        return row, col
    return None, None
