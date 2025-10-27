# data_manager.py - Yeh file JSON data loading handle karti hai
import json  # JSON data handle karne ke liye
import os  # File path operations ke liye

def load_json(name):
    """JSON file ko load karta hai aur data return karta hai
    name = JSON file ka name (data folder mein)"""
    path = os.path.join("data", name)  # Data folder mein file path banata hai
    with open(path, "r") as f:  # File open karta hai read mode mein
        return json.load(f)  # JSON data load karke return karta hai
