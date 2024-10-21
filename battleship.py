import random

EMPTY = 0
SHIP = 1
HIT = 2
MISS = 3

class BattleshipGame:
    def __init__(self):
        self.player_grid = [[EMPTY for _ in range(10)] for _ in range(10)]
        self.ai_grid = [[EMPTY for _ in range(10)] for _ in range(10)]
        self.player_shots = [[EMPTY for _ in range(10)] for _ in range(10)]  # Player's shots on AI
        self.place_ships(self.player_grid)
        self.place_ships(self.ai_grid)

    def place_ships(self, grid):
        ship_lengths = [5, 4, 3, 3, 2]  # Carrier, battleship, cruiser, submarine, destroyer
        for length in ship_lengths:
            while True:
                orientation = random.choice(['H', 'V'])
                if orientation == 'H':
                    row = random.randint(0, 9)
                    col = random.randint(0, 10 - length)
                    if all(grid[row][col + i] == EMPTY for i in range(length)):
                        for i in range(length):
                            grid[row][col + i] = SHIP
                        break
                else:
                    row = random.randint(0, 10 - length)
                    col = random.randint(0, 9)
                    if all(grid[row + i][col] == EMPTY for i in range(length)):
                        for i in range(length):
                            grid[row + i][col] = SHIP
                        break

    def check_hit(self, grid, x, y):
        return grid[x][y] == SHIP

    def handle_hit_or_miss(self, grid, shots_grid, x, y):
        if self.check_hit(grid, x, y):
            grid[x][y] = HIT
            shots_grid[x][y] = HIT
            return True
        else:
            grid[x][y] = MISS
            shots_grid[x][y] = MISS
            return False

    def all_ships_sunk(self, grid):
        for row in grid:
            if SHIP in row:
                return False
        return True
