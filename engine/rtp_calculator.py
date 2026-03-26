from tqdm import tqdm
from engine.spin_engine import spin

def simulate_rtp(
    num_spins, 
    base_reels, 
    free_spin_reels_dict, 
    num_rows, 
    evaluate_func, 
    bet_per_spin=1
):
    
    total_bet = 0
    total_win = 0
    
    base_game_win = 0
    free_spin_win = 0
    free_spins_triggered = 0
    total_free_spins_played = 0
    
    print(f"Starting simulation of {num_spins} spins...")
    
    for i in tqdm(range(num_spins)):
        # 1. Deduct bet for a base game spin
        total_bet += bet_per_spin
        
        # 2. Run a base game spin passing the base matrix
        base_spin_result = spin(
            reels=base_reels, 
            num_rows=num_rows, 
            evaluate_func=evaluate_func, 
            is_free_spin=False,
            game_state=None
        )
        
        # Extract wins
        scatter_win = base_spin_result['scatter_win_mult'] * bet_per_spin
        line_win = base_spin_result['line_win'] * bet_per_spin
        
        spin_total_win = scatter_win + line_win
        base_game_win += spin_total_win
        total_win += spin_total_win
        
        # 3. Check for Free Spins
        if base_spin_result.get('trigger_free_spins', False):
            free_spins_triggered += 1
            
            remaining_free_spins = base_spin_result.get('free_spin_count', 0)
            
            # Extract state which tells us WHICH reels to use from the matrix
            current_game_state = base_spin_result.get('game_state', {})
            
            # 4. Play Free Spins until empty
            while remaining_free_spins > 0:
                remaining_free_spins -= 1
                total_free_spins_played += 1
                
                # Dinamically select reels from the matrix (fallback to base_reels if not special)
                expanding_symbol = current_game_state.get('expanding_symbol')
                if expanding_symbol and free_spin_reels_dict:
                    fs_reels = free_spin_reels_dict[expanding_symbol]
                else:
                    fs_reels = base_reels
                
                # Pass ONLY the selected reels for this spin into spin_engine
                fs_result = spin(
                    reels=fs_reels,
                    num_rows=num_rows,
                    evaluate_func=evaluate_func,
                    is_free_spin=True,
                    game_state=current_game_state
                )
                
                # Free spins don't deduct bet! We just add the wins.
                fs_scatter_win = fs_result['scatter_win_mult'] * bet_per_spin
                fs_line_win = fs_result['line_win'] * bet_per_spin
                
                fs_spin_total_win = fs_scatter_win + fs_line_win
                free_spin_win += fs_spin_total_win
                total_win += fs_spin_total_win
                
                # Check for retrigger (getting 3+ scatters inside free spins)
                if fs_result.get('trigger_free_spins', False):
                    remaining_free_spins += fs_result.get('free_spin_count', 0)
                    
    # 5. Calculate final RTP
    rtp_percentage = 0.0
    if total_bet > 0:
        rtp_percentage = (total_win / total_bet) * 100
        
    return {
        'num_spins': num_spins,
        'total_bet': total_bet,
        'total_win': total_win,
        'base_game_win': base_game_win,
        'free_spin_win': free_spin_win,
        'free_spins_triggered': free_spins_triggered,
        'total_free_spins_played': total_free_spins_played,
        'rtp_percentage': rtp_percentage
    }
