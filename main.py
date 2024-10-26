import pygame
from gui import initialize_screen, draw_grid, update_display, handle_quit_event, handle_mouse_click, load_images
from battleship import BattleshipGame, EMPTY, HIT, MISS
from ai_bot import AIBot

# Constants
WIDTH, HEIGHT = 1320, 600  # Two grids with separation
GRID_SPACING = 120  # Separation between grids

def main():
    screen = initialize_screen(WIDTH, HEIGHT)
    game = BattleshipGame()
    ai_bot = AIBot()

    # Load images (sea, miss, ship, hit, background)
    images = load_images()

    player_turn = True
    running = True

    while running:
        # Fill background
        screen.fill((255, 255, 255))
        screen.blit(images[4], (0, 0))  # Set the background image

        # Draw both grids: Player's on the left, AI's on the right with spacing
        draw_grid(screen, game.player_grid, images, offset=0)  # Player's grid (left)
        draw_grid(screen, game.player_shots, images, offset=((WIDTH // 2) + GRID_SPACING))  # Player's shots on AI's grid (right)

        # Check for quit events
        if handle_quit_event():
            running = False

        if player_turn:
            # Player's turn to shoot at AI's board
            if pygame.mouse.get_pressed()[0]:  # Detect left mouse button click
                pos = pygame.mouse.get_pos()
                row, col = handle_mouse_click(pos, offset=(WIDTH // 2) + GRID_SPACING)  # AI's grid starts at offset
                if row is not None and col is not None and game.player_shots[row][col] == EMPTY:
                    hit = game.handle_hit_or_miss(game.ai_grid, game.player_shots, row, col)
                    if hit:
                        print(f"Player hits at ({row}, {col})")
                    else:
                        print(f"Player misses at ({row}, {col})")

                    if game.all_ships_sunk(game.ai_grid):
                        print("Player wins!")
                        running = False

                    # If hit, it's still the player's turn; otherwise, switch to AI
                    player_turn = hit
        else:
            # AI makes its move
            x, y = ai_bot.ai_shot(game.player_grid)
            hit = game.handle_hit_or_miss(game.player_grid, game.player_grid, x, y)
            ai_bot.handle_shot_result(x, y, hit)  # Update AI's knowledge of the result
            
            if hit:
                print(f"AI hits at ({x}, {y})")
            else:
                print(f"AI misses at ({x}, {y})")

            if game.all_ships_sunk(game.player_grid):
                print("AI wins!")
                running = False

            # If hit, it's still the AI's turn; otherwise, switch to the player
            player_turn = not hit

        # Update the display
        update_display(screen)

        # Slow down AI for visualization
        pygame.time.delay(250)

    pygame.quit()

if __name__ == "__main__":
    main()