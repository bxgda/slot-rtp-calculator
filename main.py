import os
from games.book_of_ra import parser
from games.book_of_ra import config
from games.book_of_ra import mechanics
from engine.rtp_calculator import simulate_rtp

def main():
    print(f"=== {config.GAME_NAME} RTP Calculator ===")
    
    # 1. Load raw response data
    input_path = os.path.join("input", "raw_response_book_of_ra.txt")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_response = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{input_path}'. Make sure the file exists.")
        return

    # 2. Parse all matrices from raw response (Base + Free Spins)
    print("Parsing reels from raw response...")
    base_reels = parser.parse_base_game(raw_response)
    free_spin_reels_dict = parser.parse_free_spin_reels(raw_response)
    
    # 3. Simulation settings
    NUMBER_OF_SPINS = 100_000   # You can increase this to 100_000 or 1_000_000 for more precise RTP
    BET_PER_SPIN = 10         # Standard bet (creates round numbers for evaluation)

    # 4. Run the simulation
    results = simulate_rtp(
        num_spins=NUMBER_OF_SPINS,
        base_reels=base_reels,
        free_spin_reels_dict=free_spin_reels_dict,
        num_rows=config.ROWS,
        evaluate_func=mechanics.evaluate,
        bet_per_spin=BET_PER_SPIN
    )

    # 5. Print final statistics
    print("\n" + "="*50)
    print("                SIMULATION RESULTS")
    print("="*50)
    print(f"Total Spins:          {results['num_spins']:,}")
    print(f"Bet Per Spin:         {BET_PER_SPIN}")
    print(f"Total Invested (Bet): {results['total_bet']:,}")
    print(f"Total Won:            {results['total_win']:,}")
    print("-" * 50)
    print(f"Base Game Win:        {results['base_game_win']:,}")
    print(f"Free Spin Win:        {results['free_spin_win']:,}")
    print("-" * 50)
    print(f"Free Spins Triggered: {results['free_spins_triggered']:,} times")
    print(f"Free Spins Played:    {results['total_free_spins_played']:,}")
    print("="*50)
    # Target RTP from config name is 95%
    print(f"FINAL CALCULATED RTP: {results['rtp_percentage']:.4f}%")
    print("="*50)

if __name__ == "__main__":
    main()
