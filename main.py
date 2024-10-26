import pygame
from gui import initialize_screen, draw_grid, update_display, handle_quit_event, handle_mouse_click, load_images
from battleship import BattleshipGame, EMPTY
from ai_bot import AIBot

# Constants
WIDTH, HEIGHT = 1320, 600  # Two grids with separation
GRID_SPACING = 120  # Separation between grids

def show_end_dialog(screen, message):
    font = pygame.font.Font(None, 36)
    dialog_width, dialog_height = 400, 200
    dialog_x = (WIDTH - dialog_width) // 2
    dialog_y = (HEIGHT - dialog_height) // 2
    dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
    pygame.draw.rect(screen, (200, 200, 200), dialog_rect)
    pygame.draw.rect(screen, (0, 0, 0), dialog_rect, 2)

    # Display the winning message
    text_surface = font.render(message, True, (0, 0, 0))
    screen.blit(text_surface, (dialog_x + 20, dialog_y + 20))

    # "Play Again" button
    play_again_rect = pygame.Rect(dialog_x + 50, dialog_y + 100, 120, 40)
    pygame.draw.rect(screen, (0, 200, 0), play_again_rect)
    play_again_text = font.render("Again", True, (255, 255, 255))
    screen.blit(play_again_text, (play_again_rect.x + 10, play_again_rect.y + 5))

    # "Exit" button
    exit_rect = pygame.Rect(dialog_x + 230, dialog_y + 100, 120, 40)
    pygame.draw.rect(screen, (200, 0, 0), exit_rect)
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (exit_rect.x + 30, exit_rect.y + 5))

    pygame.display.flip()

    # Wait for user input on the buttons
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    return "play_again"
                elif exit_rect.collidepoint(mouse_pos):
                    return "exit"

def main():
    screen = initialize_screen(WIDTH, HEIGHT)
    game = BattleshipGame()
    ai_bot = AIBot()

    # Load images (sea, miss, ship, hit, background)
    images = load_images()

    player_turn = True
    running = True
    game_over = False

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

        if not game_over:
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
                            game_over = True
                            winner_message = "Player wins!"
                        else:
                            player_turn = hit  # If hit, stay on player turn; else, switch

            else:
                pygame.time.delay(250)  # Slow down AI for visualization

                # AI makes its move
                masked_grid = [[0 if cell == 1 else cell for cell in row] for row in game.player_grid]
                x, y = ai_bot.ai_shot(masked_grid)
                hit = game.handle_hit_or_miss(game.player_grid, game.player_grid, x, y)
                ai_bot.handle_shot_result(x, y, hit)

                if hit:
                    print(f"AI hits at ({x}, {y})")
                else:
                    print(f"AI misses at ({x}, {y})")

                if game.all_ships_sunk(game.player_grid):
                    print("AI wins!")
                    game_over = True
                    winner_message = "AI BOT wins!"
                else:
                    player_turn = not hit  # If hit, stay on AI turn; else, switch to player

            # Update the display
            update_display(screen)
        else:
            # Show end dialog and handle user choice
            choice = show_end_dialog(screen, winner_message)
            if choice == "play_again":
                main()  # Restart the game
                return
            elif choice == "exit":
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
