import random

class AIBot:
    def __init__(self):
        self.moves_history = {}  # (x, y) -> 'hit' or 'miss'
        self.mode = 'hunt'
        self.current_target = None
        self.target_stack = []  # Stack for tracking successful hits
        self.direction_stack = []  # Stack for tracking successful directions
        self.current_direction = None
        # Track remaining ships and their lengths
        self.remaining_ships = {
            5: 1,  # Carrier
            4: 1,  # Battleship
            3: 2,  # Cruiser and Submarine
            2: 3   # Destroyers
        }
        
    def calculate_probability_map(self):
        """Calculate probability of ship presence for each cell."""
        prob_map = [[0 for _ in range(10)] for _ in range(10)]
        
        # Get longest remaining ship
        longest_ship = max((length for length, count in self.remaining_ships.items() if count > 0), default=2)
        
        # For each cell
        for row in range(10):
            for col in range(10):
                if (row, col) in self.moves_history:
                    continue
                    
                # Check horizontal placement possibility
                for ship_length, ship_count in self.remaining_ships.items():
                    if ship_count == 0:
                        continue
                        
                    # Check horizontal placement
                    for start in range(max(0, col - ship_length + 1), min(col + 1, 11 - ship_length)):
                        valid = True
                        for i in range(ship_length):
                            check_pos = (row, start + i)
                            if check_pos in self.moves_history:
                                if self.moves_history[check_pos] == 'miss':
                                    valid = False
                                    break
                        if valid:
                            prob_map[row][col] += ship_count
                            
                    # Check vertical placement
                    for start in range(max(0, row - ship_length + 1), min(row + 1, 11 - ship_length)):
                        valid = True
                        for i in range(ship_length):
                            check_pos = (start + i, col)
                            if check_pos in self.moves_history:
                                if self.moves_history[check_pos] == 'miss':
                                    valid = False
                                    break
                        if valid:
                            prob_map[row][col] += ship_count
                            
                # Add checkerboard pattern weight for efficiency
                #if (row + col) % 2 == 0:  # Alternate cells
                prob_map[row][col] *= 1.2
                prob_map[row][col] = round(prob_map[row][col], 2)

        
        
        #printing probability map for debbugigng
        for i in range(10):
            for j in range(10):
                print(prob_map[i][j], "\t", end=" ")
            print() 

                    
        return prob_map

    def hunt_mode_shot(self):
        """Make an intelligent shot based on probability map."""
        prob_map = self.calculate_probability_map()
        max_prob = -1
        best_shots = []
        
        # Find highest probability positions
        for row in range(10):
            for col in range(10):
                if (row, col) not in self.moves_history:
                    if prob_map[row][col] > max_prob:
                        max_prob = prob_map[row][col]
                        best_shots = [(row, col)]
                    elif prob_map[row][col] == max_prob:
                        best_shots.append((row, col))
        
        
        if not best_shots:
            return None, None
            
        return random.choice(best_shots)

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

    def estimate_ship_length(self, hits):
        """Estimate the length of a ship based on consecutive hits."""
        if len(hits) < 2:
            return None
            
        # Check if hits are in a line
        x_coords = [x for x, y in hits]
        y_coords = [y for x, y in hits]
        
        if len(set(x_coords)) == 1:  # Vertical ship
            length = max(y_coords) - min(y_coords) + 1
            return length
        elif len(set(y_coords)) == 1:  # Horizontal ship
            length = max(x_coords) - min(x_coords) + 1
            return length
        return None

    def update_remaining_ships(self, ship_length):
        """Update the count of remaining ships when one is sunk."""
        if ship_length in self.remaining_ships and self.remaining_ships[ship_length] > 0:
            self.remaining_ships[ship_length] -= 1

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
                    
                # Check if we've found a complete ship
                ship_length = self.estimate_ship_length(self.target_stack)
                if ship_length:
                    # Check if ship is surrounded by water/misses
                    ship_complete = True
                    for x, y in self.target_stack:
                        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                            new_x, new_y = x + dx, y + dy
                            if (0 <= new_x < 10 and 0 <= new_y < 10 and 
                                (new_x, new_y) not in self.moves_history):
                                ship_complete = False
                                break
                    if ship_complete:
                        self.update_remaining_ships(ship_length)
                        self.target_stack = []
                        self.current_target = None
                        self.current_direction = None
                        self.mode = 'hunt'
                        
        else:  # Miss
            if self.mode == 'target' and self.current_direction:
                if self.target_stack:
                    self.current_target = self.target_stack[0]
                    dx, dy = self.current_direction
                    self.current_direction = (-dx, -dy)

    def ai_shot(self, grid):
        """Make a shot based on current mode and history."""
        if self.mode == 'hunt':
            x, y = self.hunt_mode_shot()
        else:  # target mode
            x, y = self.target_mode_shot()
            
        return x, y

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