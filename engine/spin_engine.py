import random


def _generate_grid(reels, num_rows):
    # Creates a random grid by selecting random stop positions on each reel.
    
    grid = []
    
    # Initialize empty rows for the grid
    for r in range(num_rows):
        grid.append([])
        
    stops = []
    
    # For each column, pick a random starting position and fill the rows
    for col_idx in range(len(reels)):
        current_reel = reels[col_idx]
        reel_length = len(current_reel)
        
        # Choose a random stop position on this reel
        stop_pos = random.randint(0, reel_length - 1)
        stops.append(stop_pos)
        
        # Fill all rows for this specific column
        for row_idx in range(num_rows):
            symbol_pos = (stop_pos + row_idx) % reel_length
            symbol = current_reel[symbol_pos]
            
            grid[row_idx].append(symbol)
            
    return grid, stops


def spin(reels, num_rows, evaluate_func, is_free_spin=False, expanding_symbol=None):
    # Executes a single spin.
 
    # 1. Generate the random grid
    grid, stops = _generate_grid(reels, num_rows)
    
    # 2. Ask the specific game logic to evaluate the generated grid
    evaluation_result = evaluate_func(
        grid=grid,
        is_free_spin=is_free_spin,
        expanding_symbol=expanding_symbol
    )
    
    # 3. Create a final result dictionary with engine data + game data
    result = {}
    
    # Copy all data from game mechanics evaluation
    for key in evaluation_result:
        result[key] = evaluation_result[key]
        
    # Append the raw engine data (useful for debugging and UI representation later)
    result['initial_grid'] = grid
    result['stops'] = stops
    
    return result
