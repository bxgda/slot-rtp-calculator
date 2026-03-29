GAME_NAME = "Sizzling Hot Deluxe 95.6%"
ROWS = 3
COLS = 5
NUM_LINES = 5       # Total lines, we simulate 1 for RTP

WILD = None         # This game has NO wild symbol
SCATTER = 'S'       # Star symbol

# Organized paytable from positive values in response (:w)
BASE_PAYTABLE = {
    '7': {5: 5000, 4: 1000, 3: 100},
    'M': {5: 500,  4: 200,  3: 50},         # Melon
    'G': {5: 500,  4: 200,  3: 50},         # Grapes
    'P': {5: 200,  4: 50,   3: 20},         # Plum
    'O': {5: 200,  4: 50,   3: 20},         # Orange
    'L': {5: 200,  4: 50,   3: 20},         # Lemon
    'C': {5: 200,  4: 50,   3: 20, 2: 5},   # Cherries (pays from 2 symbols)
}

SCATTER_PAYS_TOTAL_BET_MULT = {
    5: 50,
    4: 10,
    3: 2
}
