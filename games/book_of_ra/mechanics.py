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

# Kombinujemo obe tabele isplata jer u besplatnim spinovima reelovi
# mogu da vrate i normalne simbole ali i one nove poput 'Z', 'Y' itd.
FULL_PAYTABLE = {**BASE_PAYTABLE, **FREE_SPIN_PAYTABLE}

def _get_middle_line(grid):
    middle_line = []
    for col in range(len(grid[1])):
        middle_line.append(grid[1][col])
    return middle_line


def _resolve_wilds(line):
    first_non_wild = None
    for symbol in line:
        if symbol != WILD:
            first_non_wild = symbol
            break

    if first_non_wild is None:
        return line

    resolved_line = []
    for symbol in line:
        if symbol == WILD:
            resolved_line.append(first_non_wild)
        else:
            resolved_line.append(symbol)

    return resolved_line


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


def _evaluate_line(line, paytable):
    resolved = _resolve_wilds(line)
    symbol, count = _count_consecutive(resolved)

    if symbol is None:
        return 0
    if symbol not in paytable:
        return 0
    if count not in paytable[symbol]:
        return 0

    return paytable[symbol][count]


def _count_scatter(grid):
    count = 0
    for row in grid:
        for symbol in row:
            if symbol == SCATTER:
                count += 1
    return count


def _evaluate_scatter(scatter_count):
    # Prevent KeyError limits if by some miracle grid gives > 5 books
    if scatter_count >= 5:
        scatter_count = 5
        
    if scatter_count in SCATTER_PAYS:
        return SCATTER_PAYS[scatter_count]

    return 0


def evaluate(grid, is_free_spin=False, game_state=None):
    
    # 1. State check
    expanding_symbol = None
    if game_state is not None and 'expanding_symbol' in game_state:
        expanding_symbol = game_state['expanding_symbol']

    # 2. Extract line and evaluate STANDARD left-to-right combo
    line = _get_middle_line(grid)
    line_win = _evaluate_line(line, FULL_PAYTABLE)

    # 3. Evaluate scattered Books
    scatter_count = _count_scatter(grid)
    scatter_win_mult = _evaluate_scatter(scatter_count)

    # 4. EXPANING SYMBOL LOGIC (Only during Free Spins)
    # Book of Ra explicitly dictates expanding symbol acts as scatter-pay on active lines!
    if is_free_spin and expanding_symbol is not None:
        exp_reels_count = 0
        
        # We exclusively count in how many distinct columns it appeared
        for col in range(len(grid[0])):
            for row in range(len(grid)):
                if grid[row][col] == expanding_symbol:
                    exp_reels_count += 1
                    break # Stop checking this reel, we just needed it anywhere on the reel
                    
        # Verify if amount of reels corresponds to a win in the paytable
        if expanding_symbol in FULL_PAYTABLE:
            if exp_reels_count in FULL_PAYTABLE[expanding_symbol]:
                # Since we simulate exactly 1 payline, it gets awarded exactly 1 time.
                line_win += FULL_PAYTABLE[expanding_symbol][exp_reels_count]

    # 5. Check if free spins triggered inside base game or retriggered inside free spins
    if scatter_count >= FREE_SPINS['trigger_count']:
        trigger = True
        free_spin_count = FREE_SPINS['count']
    else:
        trigger = False
        free_spin_count = 0
        
    # 6. Manage Game state explicitly
    new_game_state = game_state
    
    # Generate new random expanding symbol ONLY if it's hitting free spins from BASE GAME
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
