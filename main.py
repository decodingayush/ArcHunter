# main.py - Yeh main file hai jo game ko start karta hai
import os  # Operating system ke liye, screen clear karne ke liye
from characters import choose_character  # Character select karne ke liye
from battle_system import battle_run  # Battle system chalane ke liye
from save_system import load_game, delete_save  # Game save/load karne ke liye
from stats import ensure  # Statistics ke liye

# Yeh game ka logo hai - ASCII art se banaya gaya
LOGO = """
     ___    ____  ______   __  ____  ___   __________________     
   /   |  / __ \/ ____/  / / / / / / / / | / /_  __/ ____/ __ \    
  / /| | / /_/ / /      / /_/ / / / /  |/ / / / / __/ / /_/ /    
 / ___ |/ _, _/ /___   / __  / /_/ / /|  / / / / /___/ _, _/     
/_/  |_/_/ |_|\____/  /_/ /_/\____/_/ |_/ /_/ /_____/_/ |_|      
                                                                 
"""

def clear():
    """Screen ko clear kar deta hai - Windows aur Linux dono ke liye"""
    os.system('cls' if os.name == 'nt' else 'clear')

def intro():
    """Game ka introduction screen - logo aur description dikhata hai"""
    clear()
    print("☬" * 80)
    print(LOGO)
    print("=" * 80)
    print("🎮 Welcome to ARC HUNTER - The Ultimate Terminal Battle Game! 🎮")
    print("☬" * 80)
    print()
    print("📖 GAME DESCRIPTION:")
    print("   • Choose your character and battle through challenging floors")
    print("   • Fight powerful villains with unique abilities")
    print("   • Collect gold and purchase powerful skills")
    print("   • Use items strategically to survive")
    print("   • Save your progress and compete for high scores")
    print()
    print("🎯 FEATURES:")
    print("   • 4 Unique Characters with different stats")
    print("   • 4 Challenging Boss Fights")
    print("   • Skill System with special abilities")
    print("   • Item Shop for consumables")
    print("   • Save/Load System")
    print("   • Statistics Tracking")
    print()
    print("=" * 80)
    input("Press Enter to continue to the main menu...")

def show_stats():
    """Player ke statistics dikhata hai - pandas use karke CSV files se data read karta hai"""
    clear()
    print("=" * 50)
    print("📊 ARC HUNTER - STATISTICS 📊")
    print("=" * 50)
    print()
    
    try:
        import pandas as pd  # Data analysis ke liye pandas import karta hai
        # Accounts file check karta hai - player ke overall stats ke liye
        if os.path.exists("accounts.csv"):
            df = pd.read_csv("accounts.csv")
            if not df.empty:
                print("🏆 PLAYER STATISTICS:")
                print("-" * 30)
                # Har player ka data print karta hai
                for _, row in df.iterrows():
                    print(f"Player: {row['player_name']}")
                    print(f"Character: {row['char_key']}")
                    print(f"Best Floor: {row['best_floor']}")
                    print(f"Total Runs: {row['runs']}")
                    print(f"Wins: {row['wins']}")
                    print(f"Total Gold: {row['gold_total']}")
                    print("-" * 30)
            else:
                print("No player statistics available yet.")
        else:
            print("No player statistics available yet.")
            
        # Runs file check karta hai - recent games ke liye
        if os.path.exists("runs.csv"):
            df_runs = pd.read_csv("runs.csv")
            if not df_runs.empty:
                print("\n🎯 RECENT RUNS:")
                print("-" * 50)
                recent_runs = df_runs.tail(5)  # Last 5 runs dikhata hai
                for _, run in recent_runs.iterrows():
                    status = "✅ WON" if run['won'] else "❌ LOST"
                    print(f"{run['player_name']} - Floor {run['floor_reached']} - {status}")
                    print(f"  Time: {run['time_sec']}s | Gold: {run['gold_earned']} | Damage: {run['damage_done']}")
                    print("-" * 50)
            else:
                print("\nNo run history available yet.")
        else:
            print("\nNo run history available yet.")
            
    except Exception as e:
        print(f"Error loading statistics: {e}")
    
    print()
    input("Press Enter to return to main menu...")

def main():
    """Main function - game ka main loop hai"""
    ensure()  # Statistics files create karta hai agar nahi hai to
    intro()  # Introduction screen dikhata hai
    
    while True:  # Infinite loop - game tab tak chalega jab tak user exit na kare
        clear()
        print("=" * 50)
        print("🎮 ARC HUNTER - MAIN MENU 🎮")
        print("=" * 50)
        print()
        print("1) 🆕 New Game")
        print("2) 📁 Load Game") 
        print("3) 🗑️  Delete Save")
        print("4) 📊 View Statistics")
        print("5) ❌ Exit")
        print()
        print("=" * 50)
        
        choice = input("Choose: ").strip()  # User se input leta hai
        
        if choice == "1":
            # New game start karta hai
            player = choose_character()  # Character select karata hai
            player['max_hp'] = player['hp']  # Max HP set karta hai
            player['gold'] = 50  # Starting gold deta hai
            player['skills_owned'] = []  # Empty skills list
            player['items'] = {}  # Empty items dictionary
            battle_run(player, 1)  # Battle start karta hai floor 1 se
        elif choice == "2":
            # Saved game load karta hai
            state = load_game()
            if state:
                battle_run(state['player'], state.get('floor', 1))
            else:
                print("❌ No save found!")
                input("Press Enter...")
        elif choice == "3":
            # Save file delete karta hai
            if input("⚠️  Delete save? (y/n): ").lower() == "y":
                delete_save()
                print("✅ Deleted!")
                input("Press Enter...")
        elif choice == "4":
            # Statistics dikhata hai
            show_stats()
        elif choice == "5":
            # Game exit karta hai
            print("👋 Thanks for playing ARC HUNTER!")
            print("May your battles be legendary! ⚔️")
            break
        else:
            # Invalid choice ke liye error message
            print("❌ Invalid choice!")
            input("Press Enter...")

if __name__ == "__main__":
    main()  # Program start karta hai