# wins are typically multiplied by the bet per line.
# since we are evaluating the center line, the win is sourced from this table.
PAYTABLE = {
    'P': {2: 10, 3: 100, 4: 1000, 5: 5000},     # Pharaoh / Explorer (highest value)
    'M': {2: 5,  3: 40,  4: 400,  5: 2000},     # Mummy / Cowboy
    'S': {2: 5,  3: 30,  4: 100,  5: 750},      # Scarab
    'C': {2: 5,  3: 30,  4: 100,  5: 750},      # Cat / Statue
    'A': {3: 5,  4: 40,  5: 150},               # Ace
    'K': {3: 5,  4: 40,  5: 150},               # King
    'Q': {3: 5,  4: 25,  5: 100},               # Queen
    'J': {3: 5,  4: 25,  5: 100},               # Jack
    '1': {3: 5,  4: 25,  5: 100},               # Ten (1)
    # book acts as Scatter and Wild. 
    # scatter wins are usually multiplied by the TOTAL bet, not bet per line.
    'B': {3: 2,  4: 20,  5: 200},            
}

WILD_SYMBOL = 'B'
SCATTER_SYMBOL = 'B'

# displayed grid dimensions for a single spin
COLS = 5
ROWS = 3

# free spins rules
FREE_SPINS_TRIGGER = 3 # number of scatters required to trigger free spins
FREE_SPINS_COUNT = 10  # number of free spins awarded