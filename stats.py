# stats.py - Yeh file game statistics handle karti hai
import pandas as pd  # Data analysis ke liye pandas library
import time  # Time tracking ke liye

ACCOUNTS_FILE = "accounts.csv"  # Player accounts ka file name
RUNS_FILE = "runs.csv"  # Game runs ka file name

def ensure():
    """Statistics files create karta hai agar nahi hai to"""
    try:
        pd.read_csv(ACCOUNTS_FILE)  # Accounts file read karne ki koshish karta hai
    except Exception:
        # Accounts file nahi hai to create karta hai
        df = pd.DataFrame(columns=["player_name","char_key","best_floor","runs","wins","gold_total"])
        df.to_csv(ACCOUNTS_FILE, index=False)  # Empty CSV file create karta hai
    try:
        pd.read_csv(RUNS_FILE)  # Runs file read karne ki koshish karta hai
    except Exception:
        # Runs file nahi hai to create karta hai
        df = pd.DataFrame(columns=["player_name","date","floor_reached","won","time_sec","gold_earned","damage_done"])
        df.to_csv(RUNS_FILE, index=False)  # Empty CSV file create karta hai

def record_run(player_name, char_key, floor_reached, won, time_sec, gold_earned, damage_done):
    """Game run ka data record karta hai aur statistics update karta hai
    player_name = player ka name, char_key = character ka key, floor_reached = kitni floor reach ki,
    won = game jeeta ya nahi, time_sec = kitna time laga, gold_earned = kitna gold mila,
    damage_done = kitna damage kiya"""
    ensure()  # Files ensure karta hai
    
    # Runs file mein new run add karta hai
    df = pd.read_csv(RUNS_FILE)  # Runs file load karta hai
    new_row = pd.DataFrame({
        "player_name": [player_name],  # Player name
        "date": [time.strftime("%Y-%m-%d %H:%M:%S")],  # Current date time
        "floor_reached": [floor_reached],  # Floor reached
        "won": [int(bool(won))],  # Win status (1 ya 0)
        "time_sec": [int(time_sec)],  # Time taken
        "gold_earned": [int(gold_earned)],  # Gold earned
        "damage_done": [int(damage_done)]  # Damage done
    })
    df = pd.concat([df, new_row], ignore_index=True)  # New row add karta hai
    df.to_csv(RUNS_FILE, index=False)  # Updated data save karta hai
    
    # Accounts summary update karta hai
    ac = pd.read_csv(ACCOUNTS_FILE)  # Accounts file load karta hai
    if player_name in ac['player_name'].values:  # Check karta hai ki player already exist karta hai ya nahi
        # Existing player update karta hai
        idx = ac.index[ac['player_name']==player_name][0]  # Player ka index find karta hai
        ac.at[idx,"runs"] = ac.at[idx,"runs"] + 1  # Total runs increment karta hai
        ac.at[idx,"wins"] = ac.at[idx,"wins"] + int(bool(won))  # Wins increment karta hai
        ac.at[idx,"gold_total"] = ac.at[idx,"gold_total"] + gold_earned  # Total gold update karta hai
        if floor_reached > ac.at[idx,"best_floor"]:  # Best floor check karta hai
            ac.at[idx,"best_floor"] = floor_reached  # Best floor update karta hai
    else:
        # New player add karta hai
        new_account = pd.DataFrame({
            "player_name": [player_name],  # Player name
            "char_key": [char_key],  # Character key
            "best_floor": [floor_reached],  # Best floor
            "runs": [1],  # Total runs
            "wins": [int(bool(won))],  # Total wins
            "gold_total": [gold_earned]  # Total gold
        })
        ac = pd.concat([ac, new_account], ignore_index=True)  # New account add karta hai
    ac.to_csv(ACCOUNTS_FILE, index=False)  # Updated accounts save karta hai
