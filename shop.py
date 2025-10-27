# shop.py - Yeh file shop system handle karti hai
from data_manager import load_json  # JSON files load karne ke liye
import random  # Random skill selection ke liye

def skill_offers_for(char_key, n=3):
    """Character ke liye random skills offer karta hai
    char_key = character ka key, n = kitne skills offer karne hain"""
    skills = load_json("skills.json").get(char_key, [])  # Character ke skills load karta hai
    return random.sample(skills, min(n, len(skills)))  # Random skills return karta hai

def open_shop(player):
    """Shop interface dikhata hai aur player se purchase leta hai
    player = player ka data dictionary"""
    print("\n🛒 Skill & Item Shop")
    print("=" * 50)
    print(f"💰 Gold: {player['gold']}")  # Player ka current gold dikhata hai
    print("=" * 50)
    
    # Items section
    items = load_json("items.json")  # Items ka data load karta hai
    print("\n📦 ITEMS:")
    print("-" * 30)
    for i,item in enumerate(items, 1):
        print(f"[I{i}] {item['name']} - {item['price']}g")  # Item name aur price dikhata hai
    
    # Skills section
    skills = load_json("skills.json").get(player['key'], [])  # Player character ke skills load karta hai
    print("\n⚡ SKILLS:")
    print("-" * 30)
    for i,skill in enumerate(skills, 1):
        owned = skill['id'] in player['skills_owned']  # Check karta hai ki skill already owned hai ya nahi
        status = "✅ OWNED" if owned else f"💰 {skill['cost']}g"  # Status message
        print(f"[S{i}] {skill['name']} - {status}")  # Skill name aur status dikhata hai
    
    print("\n" + "=" * 50)
    print("Type 'i1' for item 1, 's1' for skill 1, or 'exit'")  # Instructions dikhata hai
    print("=" * 50)
    cmd = input("> ").lower()  # User input leta hai
    
    if cmd == "exit":
        return  # Shop se exit karta hai
    
    if cmd.startswith("i"):
        # Item purchase
        try:
            idx = int(cmd[1:]) - 1  # Item index extract karta hai
            item = items[idx]  # Selected item
            if player['gold'] >= item['price']:  # Check karta hai ki paise hain ya nahi
                player['gold'] -= item['price']  # Gold deduct karta hai
                player['items'][item['id']] = player['items'].get(item['id'], 0) + 1  # Item add karta hai
                print(f"Bought {item['name']}!")  # Success message
            else:
                print("Not enough gold!")  # Insufficient funds error
        except:
            print("Invalid!")  # Invalid input error
    
    elif cmd.startswith("s"):
        # Skill purchase
        try:
            idx = int(cmd[1:]) - 1  # Skill index extract karta hai
            skill = skills[idx]  # Selected skill
            if skill['id'] in player['skills_owned']:  # Check karta hai ki already owned hai ya nahi
                print("Already owned!")  # Already owned error
            elif player['gold'] >= skill['cost']:  # Check karta hai ki paise hain ya nahi
                player['gold'] -= skill['cost']  # Gold deduct karta hai
                player['skills_owned'].append(skill['id'])  # Skill add karta hai
                print(f"Bought {skill['name']}!")  # Success message
            else:
                print("Not enough gold!")  # Insufficient funds error
        except:
            print("Invalid!")  # Invalid input error
