import random

def get_spin_outcome(reels: list[list[str]], rows: int) -> list[list[str]]:
    grid_cols = []

    for reel in reels:
        reel_len = len(reel)
        stop_idx = random.randint(0, reel_len - 1)

        col_symbols = []
        for i in range(rows):
            current_idx = (stop_idx + i) % reel_len
            col_symbols.append(reel[current_idx])

        grid_cols.append(col_symbols)

    grid_rows = []
    for row_idx in range(rows):
        current_row = []
        for col_idx in range(len(grid_cols)):
            symbol = grid_cols[col_idx][row_idx]
            current_row.append(symbol)
            
        grid_rows.append(current_row)
        
    return grid_rows