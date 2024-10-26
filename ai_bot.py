import random

class AIBot:
    def __init__(self):
        self.moves_history = {}  # (x, y) -> 'hit' or 'miss'
        self.mode = 'hunt'
        self.current_target = None
        self.target_stack = []  # Stack for tracking successful hits
        self.direction_stack = []  # Stack for tracking successful directions
        self.current_direction = None
        
    def mask_grid(self, grid):
        """Creates a masked copy where unseen ships appear as water."""
        masked = [[0 for _ in range(10)] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                if (i, j) in self.moves_history:
                    masked[i][j] = grid[i][j]  # Show actual state for cells we've hit
                else:
                    masked[i][j] = 0  # Hide ships as water
        return masked

    def get_valid_adjacent_cells(self, x, y, tried_directions=None):
        """Get valid adjacent cells that haven't been tried yet."""
        all_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        if tried_directions:
            directions = [d for d in all_directions if d not in tried_directions]
        else:
            directions = all_directions
            
        random.shuffle(directions)
        valid_cells = []
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < 10 and 0 <= new_y < 10 and 
                (new_x, new_y) not in self.moves_history):
                valid_cells.append((new_x, new_y, (dx, dy)))
                
        return valid_cells

    def hunt_mode_shot(self):
        """Make a random shot at an untried position."""
        available_cells = [
            (x, y) for x in range(10) for y in range(10)
            if (x, y) not in self.moves_history
        ]
        if not available_cells:
            return None, None
        return random.choice(available_cells)

    def target_mode_shot(self):
        """Make a targeted shot based on previous hits."""
        if not self.current_target:
            return self.hunt_mode_shot()
            
        x, y = self.current_target
        
        if self.current_direction:
            dx, dy = self.current_direction
            new_x, new_y = x + dx, y + dy
            
            if (0 <= new_x < 10 and 0 <= new_y < 10 and 
                (new_x, new_y) not in self.moves_history):
                return new_x, new_y
            else:
                if self.target_stack:
                    orig_x, orig_y = self.target_stack[0]
                    new_x, new_y = orig_x - dx, orig_y - dy
                    if (0 <= new_x < 10 and 0 <= new_y < 10 and 
                        (new_x, new_y) not in self.moves_history):
                        return new_x, new_y
                self.current_direction = None
        
        valid_cells = self.get_valid_adjacent_cells(x, y)
        if valid_cells:
            new_x, new_y, direction = valid_cells[0]
            self.current_direction = direction
            return new_x, new_y
            
        if self.target_stack:
            self.current_target = self.target_stack.pop()
            self.current_direction = None
            return self.target_mode_shot()
            
        self.mode = 'hunt'
        return self.hunt_mode_shot()

    def ai_shot(self, grid):
        """Make a shot based on current mode and history."""
        masked_grid = self.mask_grid(grid)
        
        if self.mode == 'hunt':
            x, y = self.hunt_mode_shot()
        else:  # target mode
            x, y = self.target_mode_shot()
            
        return x, y

    def handle_shot_result(self, x, y, is_hit):
        """Process the result of the shot."""
        self.moves_history[(x, y)] = 'hit' if is_hit else 'miss'
        
        if is_hit:
            if self.mode == 'hunt':
                self.mode = 'target'
                self.current_target = (x, y)
                self.target_stack = [(x, y)]
            else:  # target mode
                if self.current_direction:
                    self.target_stack.append((x, y))
                    self.current_target = (x, y)
                else:
                    self.target_stack.append((x, y))
                    self.current_target = (x, y)
        else:  # Miss
            if self.mode == 'target' and self.current_direction:
                if self.target_stack:
                    self.current_target = self.target_stack[0]
                    dx, dy = self.current_direction
                    self.current_direction = (-dx, -dy)