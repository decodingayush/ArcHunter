# characters.py - Yeh file character selection handle karti hai
from data_manager import load_json  # JSON files load karne ke liye

def choose_character():
    """Player se character select karata hai aur character data return karta hai"""
    chars = load_json("characters.json")  # Characters ka data load karta hai
    print("=" * 60)
    print("🎭 CHOOSE YOUR CHARACTER 🎭")
    print("=" * 60)
    print()
    # Har character ka info dikhata hai
    for i,c in enumerate(chars, 1):
        print(f"[{i}] {c['name']}")  # Character name
        print(f"    {c['short']}")   # Character description
        print(f"    HP:{c['hp']} ATK:{c['atk']} DEF:{c['def']} SPD:{c['spd']}")  # Character stats
        print()
    print("☬" * 60)
    
    # User se character choice leta hai
    while True:
        try:
            choice = int(input("Pick your character: "))  # User input
            if 1 <= choice <= len(chars):  # Valid choice check karta hai
                char = chars[choice-1].copy()  # Selected character copy karta hai
                char['gold'] = 50  # Starting gold deta hai
                char['skills_owned'] = []  # Empty skills list
                char['items'] = {}  # Empty items dictionary
                print(f"✅ Selected {char['name']}!")  # Confirmation message
                input("Press Enter to continue...")  # Continue ke liye wait karta hai
                return char  # Character data return karta hai
        except:
            pass  # Invalid input ignore karta hai
        print("❌ Invalid choice!")  # Error message dikhata hai
