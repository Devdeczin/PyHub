import hashlib
import json
import os
import random
import sys
import time
import requests
from rich import print as rprint

USER_DATA_DIR = os.path.join(os.path.expanduser('~'), 'PyHubData')
USER_DATA_FILE = os.path.join(USER_DATA_DIR, 'users.json')
ADMIN_SECRET_FILE = os.path.join(USER_DATA_DIR, 'admin_secret.txt')
os.makedirs(USER_DATA_DIR, exist_ok=True)

ADMIN_USERNAME = "ADM"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def read_admin_secret():
    if os.path.exists(ADMIN_SECRET_FILE):
        with open(ADMIN_SECRET_FILE, 'r') as f:
            return f.read().strip()
    return None

def update_admin_secret(new_password):
    with open(ADMIN_SECRET_FILE, 'w') as f:
        f.write(hash_password(new_password))

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

users = load_users()

# Ensure all users have the necessary keys
for user in users.values():
    if 'coins' not in user:
        user['coins'] = 100
    if 'inventory' not in user:
        user['inventory'] = []
    if 'games_played' not in user:
        user['games_played'] = 0  # New key for tracking games played
save_users(users)

# Add admin account if it does not exist
if ADMIN_USERNAME not in users:
    users[ADMIN_USERNAME] = {
        'password': hash_password("#Devdec1910"),
        'coins': float('inf'),  # Initial coin amount for admin
        'inventory': [],
        'admin': True  # Admin flag
    }
    save_users(users)

ADMIN_PASSWORD_HASH = read_admin_secret()

def create_account(username, password):
    if username in users:
        return "User already exists."
    users[username] = {
        'password': hash_password(password),
        'coins': 100,  # Initial coin amount
        'inventory': [],  # Empty inventory
        'games_played': 0  # Track games played
    }
    save_users(users)
    return "Account created successfully."

def login(username, password):
    if username not in users:
        return "User not found."
    if users[username]['password'] != hash_password(password):
        return "Incorrect password."
    return "Login successful."

def delay_print(text, color="white"):
    for char in text:
        rprint(f"[{color}]{char}[/{color}]", end='')
        sys.stdout.flush()
        time.sleep(0.05)
    rprint()

def delay_input(prompt, color="white"):
    for char in prompt:
        rprint(f"[{color}]{char}[/{color}]", end='')
        sys.stdout.flush()
        time.sleep(0.05)
    return input()

def adivinhe_o_numero(username):
    delay_print("Welcome to Guess the Number!", "green")
    delay_print("Try to guess the number between 1 and 100.", "green")
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    while True:
        tentativa = int(delay_input("Enter a number: ", "green"))
        tentativas += 1
        if tentativa < numero_secreto:
            delay_print("The number is higher. Try again.", "green")
        elif tentativa > numero_secreto:
            delay_print("The number is lower. Try again.", "green")
        else:
            delay_print(f"Congratulations! You guessed the number in {tentativas} attempts.", "green")
            add_money(username, 10)  # Add 10 coins as a reward
            users[username]['games_played'] += 1  # Increment games played
            delay_print(f"You earned 10 coins! Now you have {users[username]['coins']} coins.", "green")
            save_users(users)  # Save user data after updating
            break

def loja_incrivel(username):
    items = {
        '1': {'name': 'Store Creator (Game)', 'price': 50},
        '2': {'name': 'Hubai (AI Intelligence)', 'price': 70},
        '3': {'name': 'Image Finder (explanatory name)', 'price': 30},
        '4': {'name': 'Lucky Spin (Mini-game)', 'price': 20}  # New item
    }

    def display_items():
        delay_print("=== Incredible Store ===", "magenta")
        for key, item in items.items():
            delay_print(f"{key}: {item['name']} - {item['price']} coins", "magenta")

    def buy_item(choice):
        item = items.get(choice)
        if item and users[username]['coins'] >= item['price']:
            users[username]['coins'] -= item['price']
            users[username]['inventory'].append(item['name'])
            delay_print(f"You bought {item['name']} for {item['price']} coins.", "magenta")
            save_users(users)
        else:
            delay_print("Insufficient coins or invalid item.", "red")

    while True:
        display_items()
        choice = delay_input("Choose an item to buy or 'exit' to return: ", "magenta")
        if choice.lower() == 'exit':
            break
        buy_item(choice)

def lucky_spin(username):
    delay_print("=== Lucky Spin ===", "yellow")
    delay_print("Spin the wheel for a chance to win coins!", "yellow")
    spin_result = random.choice([0, 10, 20, 50, 100])  # Possible winnings
    delay_print(f"You won {spin_result} coins!", "yellow")
    add_money(username, spin_result)

def view_inventory(username):
    delay_print(f"{username}'s Inventory:", "cyan")
    inventory = users[username]['inventory']
    if inventory:
        for idx, item in enumerate(inventory, 1):
            delay_print(f"{idx}: {item}", "cyan")
        choice = delay_input("Enter the number of the item to use or 'exit' to return: ", "cyan").strip().lower()
        if choice != 'exit' and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(inventory):
                use_item(username, inventory[idx])
            else:
                delay_print("Invalid choice.", "red")
    else:
        delay_print("Your inventory is empty.", "cyan")

def achar_imagens(username):
    delay_print("=== Image Finder ===", "cyan")
    delay_print("Welcome to Image Finder, improved by Unsplash.")
    delay_print("Before you start, you need an API key from Unsplash. To obtain it, just click the link below and follow the instructions.")
    delay_print("https://unsplash.com/developers")
    ACCESS_KEY = delay_input("Please enter your API key here: ")
    search = delay_input("Now that you have your API, enter the image you want to see: ")
    url = f'https://api.unsplash.com/photos/random?query={search}'
    headers = {'Authorization': f'Client-ID {ACCESS_KEY}'}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        image_url = data['urls']['regular']
        delay_print(f"Here is your image: {image_url}", "cyan")
    else:
        delay_print("Failed to retrieve image. Check your API key and try again.", "red")

def criador_de_loja(username):
    delay_print("Store Creator functionality coming soon...")

def hubai(username):
    delay_print("Hubai functionality coming soon...")

def use_item(username, item_name):
    if item_name == 'Store Creator (Game)':
        criador_de_loja(username)
    elif item_name == 'Hubai (AI Intelligence)':
        delay_print("Opening Hubai...", "green")
        hubai(username)
    elif item_name == 'Image Finder (explanatory name)':
        delay_print("Opening Image Finder...", "green")
        achar_imagens(username)
    elif item_name == 'Lucky Spin (Mini-game)':
        lucky_spin(username)
    else:
        delay_print("Unknown item.", "red")

def add_money(username, amount):
    users[username]['coins'] += amount
    save_users(users)

def account(username):
    delay_print(f"Welcome, {username}!", color="cyan")
    delay_print(f"You have {users[username]['coins']} coins.", color="cyan")
    delay_print(f"You have played {users[username]['games_played']} games.", color="cyan")  # Show games played
    delay_print("What would you like to do? Look at the list below:", color="cyan")
    delay_print('''
    1: Guess the Number
    2: Incredible Store
    3: View Inventory
    4: Add Money
    5: Exit''')
    if users[username].get('admin'):
        delay_print("6: Admin Options", color="red")
    choice = delay_input("Choose an option: ").strip().lower()
    if choice == "1":
        adivinhe_o_numero(username)
    elif choice == "2":
        loja_incrivel(username)
    elif choice == "3":
        view_inventory(username)
    elif choice == "4":
        amount = int(delay_input("Enter amount to add: ", "cyan"))
        add_money(username, amount)
        delay_print(f"You added {amount} coins. Now you have {users[username]['coins']} coins.", "cyan")
    elif choice == "5":
        return
    elif choice == "6" and users[username].get('admin'):
        delay_print("Admin options coming soon...", color="red")
    else:
        delay_print("Invalid choice. Please try again.", "red")

def main():
    while True:
        delay_print("Welcome to PyHub! Please select an option:", color="green")
        delay_print('''
        1: Create Account
        2: Login
        3: Exit''')
        choice = delay_input("Choose an option: ")
        if choice == "1":
            username = delay_input("Enter a username: ", "green")
            password = delay_input("Enter a password: ", "green")
            message = create_account(username, password)
            delay_print(message, "green")
        elif choice == "2":
            username = delay_input("Enter your username: ", "green")
            password = delay_input("Enter your password: ", "green")
            message = login(username, password)
            delay_print(message, "green")
            if message == "Login successful.":
                account(username)
        elif choice == "3":
            delay_print("Exiting... Bye!", "green")
            break
        else:
            delay_print("Invalid choice. Please try again.", "red")

if __name__ == "__main__":
    main()
