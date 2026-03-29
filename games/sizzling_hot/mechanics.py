from games.sizzling_hot.config import (
    SCATTER,
    BASE_PAYTABLE,
    SCATTER_PAYS_TOTAL_BET_MULT
)

def _get_middle_line(grid):
    middle_line = []
    for col in range(len(grid[1])):
        middle_line.append(grid[1][col])
    return middle_line

def _count_consecutive(line):
    if not line:
        return (None, 0)
    symbol = line[0]
    count = 1
    for i in range(1, len(line)):
        if line[i] == symbol:
            count += 1
        else:
            break
    return (symbol, count)

def _evaluate_line(line):
    symbol, count = _count_consecutive(line)
    if symbol is None:
        return 0
    if symbol not in BASE_PAYTABLE:
        return 0
    if count not in BASE_PAYTABLE[symbol]:
        return 0
    return BASE_PAYTABLE[symbol][count]

def _count_scatter(grid):
    count = 0
    for row in grid:
        for symbol in row:
            if symbol == SCATTER:
                count += 1
    return count

def evaluate(grid, is_free_spin=False, game_state=None):
    # 1. Get middle line ONLY
    line = _get_middle_line(grid)
    line_win = _evaluate_line(line)

    # 2. Count scatters
    scatter_count = _count_scatter(grid)
    
    # 3. Calculate scatter win. 
    # CIST RACUN: Posto simuliramo samo 1 liniju, nas ulog je 1x. 
    # Zato scatter mnozimo samo sa osnovnim mnoziocem iz tabele, bez dodavanja broja linija.
    scatter_win_mult = 0
    if scatter_count in SCATTER_PAYS_TOTAL_BET_MULT:
        scatter_win_mult = SCATTER_PAYS_TOTAL_BET_MULT[scatter_count]

    # Sizzling hot never triggers free spins
    trigger_free_spins = False
    free_spin_count = 0

    return {
        'line_win':           line_win,
        'scatter_win_mult':   scatter_win_mult,
        'scatter_count':      scatter_count,
        'trigger_free_spins': trigger_free_spins,
        'free_spin_count':    free_spin_count,
        'grid':               grid,
        'line':               line,
        'game_state':         game_state
    }