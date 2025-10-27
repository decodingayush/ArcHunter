################# battle_system.py - this file handles the mechanics of the game ############


import random, time, os  # for Random numbers, time tracking, terminal commands 
from data_manager import load_json  
from shop import skill_offers_for 
from stats import record_run  

########for clearing the terminal using os module
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
 
######### cur = current HP, mx = max HP, length = length of bar

def hp_bar(cur, mx, length=20):
    ratio = max(0, min(1, cur/mx)) if mx>0 else 0  
    filled = int(ratio*length)  
    return "[" + "█"*filled + "-"*(length-filled) + f"] {cur}/{mx}" 

####### calculate the damage based on the attack and defense values
def damage(att, def_val, crit=False):
    base = max(1, att - def_val//2)  # Base damage - defense se kam hota hai
    dmg = int(base * random.uniform(0.8, 1.2))  # Random variation add karta hai
    return dmg * 2 if crit else dmg  # Critical hit pe double damage deta hai

######### main battle function
def battle_run(player, start_floor=1):
    clear()
    print("Welcome to ARC HUNTER!")
    
    # Villains ka data - har floor pe different villain hai
    villains = [
        {"name":"Orochimaru","hp":90,"atk":22,"def":12},  # Floor 1 villain
        {"name":"Ultron","hp":110,"atk":28,"def":16},     # Floor 2 villain
        {"name":"Titan Beast","hp":140,"atk":34,"def":18}, # Floor 3 villain
        {"name":"KIRMADA","hp":320,"atk":48,"def":28}     # Floor 4 boss villain
    ]
    
    floor = start_floor  # Current floor
    damage_total = 0     # Total damage done in this run
    run_start = time.time()  # Run start time - statistics ke liye
    
    # Main game loop - har floor ke liye
    while floor <= len(villains) and player['hp'] > 0:
        villain = villains[floor-1].copy()  # Current floor ka villain copy karta hai
        villain['hp'] = int(villain['hp'] * (1 + floor*0.1))  # Floor ke basis pe HP scale karta hai
        villain['atk'] = int(villain['atk'] * (1 + floor*0.1))  # Attack bhi scale karta hai
        villain['max_hp'] = villain['hp']  # Max HP store karta hai HP bar ke liye
        
        # Boss fight ke liye special intro
        if villain['name'] == "KIRMADA":
            clear()
            print("╔" + "═"*70 + "╗")
            print("║" + f"!!! BOSS APPEARS: {villain['name']} !!!".center(70) + "║")
            print("╚" + "═"*70 + "╝")
            time.sleep(1)
        
        used_skills = set()  # Is battle mein jo skills use ki hain
        
        # Battle loop - jab tak villain ya player mar na jaye
        while villain['hp'] > 0 and player['hp'] > 0:
            # Battle UI display karta hai
            print("╔" + "═"*70 + "╗")
            title = f"   ARC HUNTER   —  Floor {floor} / {len(villains)}   "
            print("║" + title.center(70) + "║")
            print("╟" + "─"*70 + "╢")
            print(f"║ {player['name']}: HP {hp_bar(player['hp'], player['max_hp'], 18)} ATK:{player['atk']} DEF:{player['def']} GOLD:{player['gold']} ║")
            print("╟" + "─"*70 + "╢")
            print(f"║ {villain['name']}: HP {hp_bar(villain['hp'], villain['max_hp'], 30)} ║")
            print("╟" + "─"*70 + "╢")
            print("║ Actions: [1] Attack   [2] Skill   [3] Defend   [4] Item   [5] Save   [6] Shop ║")
            print("╚" + "═"*70 + "╝")
            
            cmd = input("> ").strip()  # Player se action input leta hai
            
            if cmd == "1":
                # Normal attack
                crit = random.random() < 0.25  # 25% chance of critical hit
                dmg = damage(player['atk'], villain['def'], crit)  # Damage calculate karta hai
                villain['hp'] -= dmg  # Villain ka HP kam karta hai
                damage_total += dmg  # Total damage mein add karta hai
                print(f"You hit for {dmg}" + (" (CRIT!)" if crit else ""))  # Damage message dikhata hai
                
            elif cmd == "2":
                # Skill usage
                skills = load_json("skills.json").get(player['key'], [])  # Player ke skills load karta hai
                available = [s for s in skills if s['id'] in player['skills_owned'] and s['id'] not in used_skills]  # Available skills filter karta hai
                
                if not available:
                    print("No skills ready!")  # Agar koi skill available nahi hai
                    continue
                    
                print("Skills:")  # Available skills list dikhata hai
                for i,s in enumerate(available, 1):
                    print(f"{i}) {s['name']} - Damage:{s.get('damage',0)} Heal:{s.get('heal',0)}")
                
                try:
                    choice = int(input("Choose skill: ")) - 1  # Player se skill choice leta hai
                    skill = available[choice]
                    used_skills.add(skill['id'])  # Skill ko used mark karta hai
                    
                    if skill.get('damage',0) > 0:
                        # Damage skill
                        dmg = damage(skill['damage'] + player['atk']//3, villain['def'])  # Skill damage calculate karta hai
                        villain['hp'] -= dmg
                        damage_total += dmg
                        print(f"{skill['name']} deals {dmg} damage!")  # Skill damage message
                    elif skill.get('heal',0) > 0:
                        # Heal skill
                        heal = skill['heal']
                        player['hp'] = min(player['max_hp'], player['hp'] + heal)  # Player ko heal karta hai
                        print(f"{skill['name']} heals {heal} HP!")  # Heal message
                except:
                    print("Invalid choice!")  # Invalid input ke liye error
                    continue
                    
            elif cmd == "3":
                # Defend action
                print("You defend! DEF +15 this turn")  # Defense message
                player['def'] += 15  # Temporary defense boost
                defended = True  # Defend flag set karta hai
                
            elif cmd == "4":
                # Item usage
                items = load_json("items.json")  # Items load karta hai
                print("Items:")  # Available items dikhata hai
                for i,item in enumerate(items, 1):
                    count = player.get('items', {}).get(item['id'], 0)  # Item count check karta hai
                    print(f"{i}) {item['name']} x{count}")
                
                try:
                    choice = int(input("Use item: ")) - 1  # Item choice leta hai
                    item = items[choice]
                    if player.get('items', {}).get(item['id'], 0) > 0:  # Agar item available hai
                        if item['effect'] == "heal":  # Heal item hai to
                            player['hp'] = min(player['max_hp'], player['hp'] + item['value'])  # Heal karta hai
                            player['items'][item['id']] -= 1  # Item count kam karta hai
                            print(f"Used {item['name']}!")  # Usage message
                    else:
                        print("You don't have that item!")  # Item nahi hai to error
                except:
                    print("Invalid choice!")  # Invalid input error
                    continue
                    
            elif cmd == "5":
                # Save game
                from save_system import save_game
                save_game({"player": player, "floor": floor, "damage_total": damage_total})  # Game state save karta hai
                print("Game saved!")
                return  # save and exit
                
            elif cmd == "6":
                # Shop access
                from shop import open_shop
                open_shop(player)  # Shop open 
                continue
            else:
                print("Invalid choice!")  # Invalid action error
                continue
            
            if villain['hp'] <= 0:  #if villain dies
                break
                
            # Enemy attack phase
            vcrit = random.random() < 0.05  # 5% chance villain critical hit
            vdmg = damage(villain['atk'], player['def'], vcrit)  # Villain damage calculation
            player['hp'] -= vdmg  # Player ka HP kam karta hai
            print(f"{villain['name']} hits for {vdmg}" + (" (CRIT!)" if vcrit else ""))  # Villain damage message
            
            # Defend effect removing after each attack
            if 'defended' in locals():
                player['def'] -= 5  # Defense boost removing
                defended = False
        
        if player['hp'] <= 0:  # if player dies
            print("You died!")
            break
            
        # Floor cleared - victory rewards
        gold_gain = 50 + floor * 40  # Gold reward calculate karta hai
        player['gold'] += gold_gain  # Player ko gold deta hai
        print(f"Floor {floor} cleared! +{gold_gain} gold")  # Victory message
        
        # Skill shop after each floor
        offers = skill_offers_for(player['key'], 3)  # 3 random skills offer karta hai
        print("\nSkill Shop:")  # Shop interface
        for i,offer in enumerate(offers, 1):
            print(f"{i}) {offer['name']} - {offer['cost']}g")
        print("0) Skip")
        
        try:
            choice = int(input("Buy: "))  # Skill purchase choice
            if 1 <= choice <= len(offers):
                offer = offers[choice-1]
                if player['gold'] >= offer['cost']:  # Agar paise hain to
                    player['gold'] -= offer['cost']  # Gold deduct karta hai
                    player['skills_owned'].append(offer['id'])  # Skill add karta hai
                    print(f"Bought {offer['name']}!")  # Purchase message
                else:
                    print("Not enough gold!")  # Paise nahi hain to error
        except:
            print("Skipped!")  # Invalid input ya skip
        
        player['max_hp'] += 60
        player['hp'] = player['max_hp']
        floor += 1  
    
    # Run complete - statistics record karta hai
    run_time = time.time() - run_start  # Total run time calculate karta hai
    record_run(player['name'], player['key'], floor-1, player['hp']>0, run_time, player.get('gold',0), damage_total)
    
    # Final summary
    clear()
    print("Run Complete! In this you have achieved the following :")
    print(f"Floors: {floor-1} | Damage: {damage_total} | Gold: {player.get('gold',0)}")
    input("Press Enter...")
