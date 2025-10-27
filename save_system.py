# save_system.py - Yeh file game save/load functionality handle karti hai
import json  # JSON data handle karne ke liye
import os  # File operations ke liye

SAVE_FILE = "arc_save.json"  # Save file ka name

def save_game(state):
    """Game state ko file mein save karta hai
    state = game ka current state dictionary"""
    with open(SAVE_FILE, "w") as f:  # File open karta hai write mode mein
        json.dump(state, f, indent=2)  # JSON data file mein write karta hai
    print("✅ Game saved to arc_save.json")  # Success message dikhata hai

def load_game():
    """Saved game ko load karta hai
    Returns: game state dictionary ya None agar file nahi hai"""
    if os.path.exists(SAVE_FILE):  # Check karta hai ki save file exist karti hai ya nahi
        with open(SAVE_FILE, "r") as f:  # File open karta hai read mode mein
            return json.load(f)  # JSON data load karke return karta hai
    return None  # File nahi hai to None return karta hai

def delete_save():
    """Save file ko delete karta hai"""
    if os.path.exists(SAVE_FILE):  # Check karta hai ki file exist karti hai ya nahi
        os.remove(SAVE_FILE)  # File delete karta hai
        print("🗑️ Save file deleted!")  # Success message dikhata hai
