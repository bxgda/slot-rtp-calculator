# basic info
GAME_NAME = "Book of Ra Deluxe 95%"
ROWS = 3        # number of visible rows on screen
COLS = 5        # number of reels (columns)
NUM_LINES = 10  # total paylines available (we use only line 1 for RTP calc)

#symbols
WILD = 'B'                                                          # wild symbol — substitutes all other symbols except scatter
SCATTER = 'B'                                                       # scatter symbol — triggers free spins, pays anywhere on the grid
BASE_SYMBOLS = ['B', 'P', 'M', 'S', 'C', 'A', 'K', 'Q', 'J', '1']   # all base game symbols ordered by value (highest to lowest)
FREE_SPIN_SYMBOLS = ['Z', 'Y', 'X', 'I', 'H', 'G', 'F', 'E', 'D']   # expanding symbols — only appear in free spin reel sets (1-10)

# base game paytable
BASE_PAYTABLE = {
    'B': {5: 200,  4: 20,   3: 2},
    'P': {5: 5000, 4: 1000, 3: 100, 2: 10},
    'M': {5: 2000, 4: 400,  3: 40,  2: 5},
    'S': {5: 750,  4: 100,  3: 30,  2: 5},
    'C': {5: 750,  4: 100,  3: 30,  2: 5},
    'A': {5: 150,  4: 40,   3: 5},
    'K': {5: 150,  4: 40,   3: 5},
    'Q': {5: 100,  4: 25,   3: 5},
    'J': {5: 100,  4: 25,   3: 5},
    '1': {5: 100,  4: 25,   3: 5},
}

# free spin paytable
FREE_SPIN_PAYTABLE = {
    'Z': {5: 5000, 4: 1000, 3: 100, 2: 10},
    'Y': {5: 2000, 4: 400,  3: 40,  2: 5},
    'X': {5: 750,  4: 100,  3: 30,  2: 5},
    'I': {5: 750,  4: 100,  3: 30,  2: 5},
    'H': {5: 150,  4: 40,   3: 5},
    'G': {5: 150,  4: 40,   3: 5},
    'F': {5: 100,  4: 25,   3: 5},
    'E': {5: 100,  4: 25,   3: 5},
    'D': {5: 100,  4: 25,   3: 5},
}

# scatter payouts
SCATTER_PAYS = {
    3: 2,                   # 3x Book anywhere = 2x total bet
    4: 20,                  # 4x Book anywhere = 20x total bet
    5: 200,                 # 5x Book anywhere = 200x total bet
}

# free spins configuration
FREE_SPINS = {
    'trigger_count': 3,     # minimum scatter symbols needed to trigger
    'count': 10,            # number of free spins awarded
    'retrigger': True,      # can free spins be retriggered during free spins
}

# paylines
PAYLINES = {
    1:  [1, 1, 1, 1, 1],  # -----  middle row (used for RTP calculation)
    2:  [0, 0, 0, 0, 0],  # ^^^^^  top row
    3:  [2, 2, 2, 2, 2],  # _____  bottom row
    4:  [0, 1, 2, 1, 0],  # ^-_-^  V shape
    5:  [2, 1, 0, 1, 2],  # _-^-_  inverted V
    6:  [1, 2, 2, 2, 1],  # -___-  bottom middle
    7:  [1, 0, 0, 0, 1],  # -^^^-  top middle
    8:  [2, 2, 1, 0, 0],  # __-^^  diagonal up-right
    9:  [0, 0, 1, 2, 2],  # ^^-__  diagonal down-right
    10: [2, 1, 1, 1, 0],  # _---^  diagonal
}

# expanding symbol mapping
EXPANDING_SYMBOLS = {
    1:  'Q',
    2:  'Z',
    3:  'Y',
    4:  'X',
    5:  'I',
    6:  'H',
    7:  'G',
    8:  'F',
    9:  'E',
    10: 'D',
}
