import re

def parse_base_game(raw_response: str) -> list:
    # Extracts base game reels (set 0).

    pattern = r':r,0,([A-Z0-9]+)'
    matches = re.findall(pattern, raw_response)

    if not matches:
        raise ValueError("Base game (set 0) not found in response!")

    reels = []
    for reel_string in matches:
        # Every character is exactly one symbol
        reels.append(list(reel_string))

    if len(reels) != 5:
        raise ValueError(f"Expected 5 reels, found {len(reels)}!")

    return reels


def parse_free_spin_reels(raw_response: str) -> dict:
    return {}
