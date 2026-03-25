import re


# directly from game-init response
FREE_SPIN_SETS = {
    1: 'Q',     # set 1 expanding simbol
    2: 'Z',     # set 2 expanding simbol
    3: 'Y',     # set 3 expanding simbol
    4: 'X',     # set 4 expanding simbol
    5: 'I',     # set 5 expanding simbol
    6: 'H',     # set 6 expanding simbol
    7: 'G',     # set 7 expanding simbol
    8: 'F',     # set 8 expanding simbol
    9: 'E',     # set 9 expanding simbol
    10: 'D',    # set 10 expanding simbol
}


def _extract_reel_sets(raw_response: str) -> dict:
    pattern = r':r,(\d+),([A-Z0-9]+)'
    matches = re.findall(pattern, raw_response)

    reel_sets = {}
    for set_id_str, reel_string in matches:
        set_id = int(set_id_str)
        if set_id not in reel_sets:
            reel_sets[set_id] = []
        reel_sets[set_id].append(list(reel_string))

    return reel_sets


def parse_base_game(raw_response: str) -> list:
    reel_sets = _extract_reel_sets(raw_response)

    if 0 not in reel_sets:
        raise ValueError("Base game (set 0) not found in game-init response!")
    
    reels = reel_sets[0]
    
    if len(reels) != 5:
        raise ValueError(f"Expected 5 columns, found {len(reels)}!")
    
    return reels


def parse_free_spin_reels(raw_response: str) -> dict:
    reel_sets = _extract_reel_sets(raw_response)

    free_spin_reels = {}
    for set_id, expanding_symbol in FREE_SPIN_SETS.items():
        if set_id not in reel_sets:
            raise ValueError(f"Free spin set {set_id} not found")
        
        reels = reel_sets[set_id]
        if len(reels) != 5:
            raise ValueError(f"Set {set_id}: expected 5 columns, found {len(reels)}!")
        
        free_spin_reels[expanding_symbol] = reels

    return free_spin_reels


def get_reel_stats(reels: list) -> dict:
    stats = {}
    for i, reel in enumerate(reels):
        col_stats = {}
        for symbol in reel:
            col_stats[symbol] = col_stats.get(symbol, 0) + 1
        stats[i] = col_stats
    return stats


def print_reel_stats(reels: list) -> None:
    stats =get_reel_stats(reels)
    for col_idx, col_stats in stats.items():
        total = len(reels[col_idx])
        print(f"\nColumn {col_idx} ({total} simbols):")
        for symbol, count in sorted(col_stats.items()):
            pct = count / total * 100
            print(f"  {symbol}: {count:3d}x  ({pct:5.1f}%)")
