import pygame

# Constants
CELL_SIZE = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Player's board color
ORANGE = (255, 165, 0)  # AI's board color for hits/misses

GAP = 2*CELL_SIZE

def initialize_screen(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width + CELL_SIZE, height))  # Added extra width for better visibility
    pygame.display.set_caption("Battleship Multiplayer (Player vs AI)")
    return screen

def load_images():
    sea = pygame.image.load("assets/sea.png")
    sea = pygame.transform.scale(sea, (CELL_SIZE, CELL_SIZE))
    
    miss = pygame.image.load("assets/miss.png")
    miss = pygame.transform.scale(miss, (CELL_SIZE, CELL_SIZE))
    
    ship = pygame.image.load("assets/ship.png")
    ship = pygame.transform.scale(ship, (CELL_SIZE, CELL_SIZE))
    
    hit = pygame.image.load("assets/hit.png")
    hit = pygame.transform.scale(hit, (CELL_SIZE, CELL_SIZE))
    
    # Load and scale the background (water) image
    background = pygame.image.load("assets/water.png")
    
    return sea, miss, ship, hit, background

def draw_grid(screen, grid, images, offset=0):
    sea_img, miss_img, ship_img, hit_img, _ = images
    for row in range(10):
        for col in range(10):
            rect = pygame.Rect(col * CELL_SIZE + offset, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 0:  # Empty
                screen.blit(sea_img, rect)
            elif grid[row][col] == 1:  # Ship
                screen.blit(ship_img, rect)
            elif grid[row][col] == 2:  # Hit
                screen.blit(hit_img, rect)
            elif grid[row][col] == 3:  # Miss
                screen.blit(miss_img, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Light gray border with 1px thickness

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


# Main game loop example
def main():
    screen = initialize_screen(20*CELL_SIZE + GAP, 10*CELL_SIZE)
    images = load_images()

    # Example grid: 0 = sea, 1 = ship, 2 = hit, 3 = miss
    grid = [[0]*10 for _ in range(10)]  # A 10x10 grid filled with sea (0)

    running = True
    while running:
        running = not handle_quit_event()

        # Example: Random updates to the grid (You can replace this with actual game logic)
        row, col = handle_mouse_click(pygame.mouse.get_pos())
        if row is not None and col is not None:
            grid[row][col] = (grid[row][col] + 1) % 4  # Cycle between sea, ship, hit, miss for testing

        # Draw the background first
        screen.fill(WHITE)
        screen.blit(images[4], (0, 0))  # Blit the background (water) image across the entire screen

        # Draw both player and AI grids (player on the left, AI on the right)
        draw_grid(screen, grid, images, offset=0)  # Player grid on the left
        draw_grid(screen, grid, images, offset=(CELL_SIZE*10 + GAP))  # AI grid on the right

        update_display()

    pygame.quit()

if __name__ == "__main__":
    main()
