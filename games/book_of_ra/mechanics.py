import random

from games.book_of_ra.config import (
    WILD,
    SCATTER,
    BASE_PAYTABLE,
    FREE_SPIN_PAYTABLE,
    SCATTER_PAYS,
    FREE_SPINS,
    FREE_SPIN_SYMBOLS
)


def _get_middle_line(grid):
    middle_line = []

    for col in range(len(grid[1])):
        middle_line.append(grid[1][col])

    return middle_line


def _apply_expanding(grid, expanding_symbol):
    # Applies the expanding symbol mechanic during free spins.

    # make a copy so we dont modify the original grid
    new_grid = []
    for row in grid:
        new_row = []
        for symbol in row:
            new_row.append(symbol)
        new_grid.append(new_row)

    # check each column for the expanding symbol
    for col in range(len(grid[0])):

        # collect all symbols in this column
        col_symbols = []
        for row in range(len(grid)):
            col_symbols.append(grid[row][col])

        # if expanding symbol is anywhere in this column, fill entire column
        if expanding_symbol in col_symbols:
            for row in range(len(grid)):
                new_grid[row][col] = expanding_symbol

    return new_grid


def _resolve_wilds(line):
    # Replaces wild symbols (B) on the line with the first non-wild symbol.

    # find the first non-wild symbol on the line
    first_non_wild = None
    for symbol in line:
        if symbol != WILD:
            first_non_wild = symbol
            break

    # if no non-wild found (all wilds) — Book pays as itself, return as is
    if first_non_wild is None:
        return line

    # replace all wilds with the first non-wild symbol
    resolved_line = []
    for symbol in line:
        if symbol == WILD:
            resolved_line.append(first_non_wild)
        else:
            resolved_line.append(symbol)

    return resolved_line


def _count_consecutive(line):
    # counts consecutive matching symbols from left to right.

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


def _evaluate_line(line, paytable):
    # Evaluates a single payline and returns the win amount in credits.

    resolved = _resolve_wilds(line)
    symbol, count = _count_consecutive(resolved)

    if symbol is None:
        return 0

    # check if this symbol has any payout defined
    if symbol not in paytable:
        return 0

    # check if this count has a payout for this symbol
    if count not in paytable[symbol]:
        return 0

    return paytable[symbol][count]


def _count_scatter(grid):
    # Counts scatter symbols (Book/B) anywhere on the entire grid.

    count = 0

    for row in grid:
        for symbol in row:
            if symbol == SCATTER:
                count += 1

    return count


def _evaluate_scatter(scatter_count):
    # Returns scatter payout multiplier based on scatter count.
 
    if scatter_count in SCATTER_PAYS:
        return SCATTER_PAYS[scatter_count]

    return 0


def evaluate(grid, is_free_spin=False, game_state=None):
    
    # 1. Read expanding symbol from game_state if it exists
    expanding_symbol = None
    if game_state is not None and 'expanding_symbol' in game_state:
        expanding_symbol = game_state['expanding_symbol']

    # 2. Apply expanding symbol mechanic if this is a free spin
    if is_free_spin and expanding_symbol is not None:
        grid = _apply_expanding(grid, expanding_symbol)

    # 3. Choose correct paytable
    if is_free_spin:
        paytable = FREE_SPIN_PAYTABLE
    else:
        paytable = BASE_PAYTABLE

    # 4. Get middle line
    line = _get_middle_line(grid)

    # 5. Evaluate line win
    line_win = _evaluate_line(line, paytable)

    # 6. Evaluate scatter
    scatter_count = _count_scatter(grid)
    scatter_win_mult = _evaluate_scatter(scatter_count)

    # 7. Check if free spins triggered
    if scatter_count >= FREE_SPINS['trigger_count']:
        trigger = True
        free_spin_count = FREE_SPINS['count']
    else:
        trigger = False
        free_spin_count = 0
        
    # 8. Manage game_state
    new_game_state = game_state
    
    # If we hit a trigger from the BASE GAME, we must pick a random expanding symbol
    if trigger and not is_free_spin:
        chosen_symbol = random.choice(FREE_SPIN_SYMBOLS)
        new_game_state = {'expanding_symbol': chosen_symbol}

    return {
        'line_win':           line_win,
        'scatter_win_mult':   scatter_win_mult,
        'scatter_count':      scatter_count,
        'trigger_free_spins': trigger,
        'free_spin_count':    free_spin_count,
        'grid':               grid,
        'line':               line,
        'game_state':         new_game_state
    }