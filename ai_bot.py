import random

class AIBot:
    def __init__(self):
        self.last_hit = None
        self.mode = 'hunt'

    def random_shot(self, grid):
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if grid[x][y] == 0 or grid[x][y] == 1:  # Empty or Ship
                return x, y

    def target_adjacent(self, grid, last_hit):
        x, y = last_hit
        options = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        random.shuffle(options)
        for opt in options:
            if 0 <= opt[0] < 10 and 0 <= opt[1] < 10 and (grid[opt[0]][opt[1]] == 0 or grid[opt[0]][opt[1]] == 1):
                return opt
        return self.random_shot(grid)

    def ai_shot(self, grid):
        if self.mode == 'hunt':
            return self.random_shot(grid)
        elif self.mode == 'target' and self.last_hit:
            return self.target_adjacent(grid, self.last_hit)

    def handle_hit_or_miss(self, grid, x, y):
        if grid[x][y] == 1:  # Ship is hit
            grid[x][y] = 2  # Mark as HIT
            self.last_hit = (x, y)
            self.mode = 'target'
            return True
        else:
            grid[x][y] = 3  # Mark as MISS
            self.mode = 'hunt'
            return False
