import sys
import time
import hashlib
import requests
from rich import print as rprint
import os
import json
from groq import Groq
import random

USER_DATA_DIR = os.path.join(os.path.expanduser('~'), 'PyHubData')
USER_DATA_FILE = os.path.join(USER_DATA_DIR, 'users.json')
NOTES_DATA_FILE = os.path.join(USER_DATA_DIR, 'notes.json')
os.makedirs(USER_DATA_DIR, exist_ok=True)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users():
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_notes():
    if os.path.exists(NOTES_DATA_FILE):
        with open(NOTES_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_notes():
    with open(NOTES_DATA_FILE, 'w') as f:
        json.dump(notes, f, indent=4)

users = load_users()
notes = load_notes()

def create_account(username, password):
    if username in users:
        return "User already exists."
    users[username] = hash_password(password)
    save_users()
    return "Account created successfully."

def login(username, password):
    if username not in users:
        return "User not found."
    if users[username] != hash_password(password):
        return "Incorrect password."
    return "Login successful."

def delay_print(text, color="white"):
    for char in text:
        rprint(f"[{color}]{char}[/{color}]", end='')
        sys.stdout.flush()
        time.sleep(0.1)
    rprint()

def delay_input(prompt, color="white"):
    for char in prompt:
        rprint(f"[{color}]{char}[/{color}]", end='')
        sys.stdout.flush()
        time.sleep(0.1)
    user_input = input()
    return user_input

def fast_print(text, color="white"):
    for char in text:
        rprint(f"[{color}]{char}[/{color}]", end='')
        sys.stdout.flush()
        time.sleep(0.01)
    rprint()

#==================================================================================================
PEXELS_API_KEY = "YOUR_API_KEY_HERE"

def search_images():
    delay_print("=== Search Images ===", color="cyan")
    delay_print("WARMING: Modify the code to put your API key of pexels", color="red")
    query = delay_input("Enter search query: ", color="yellow")
    
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": query,
        "per_page": 5
    }

    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['total_results'] == 0:
            delay_print("No images found.", color="red")
        else:
            delay_print(f"Found {data['total_results']} images. Showing top {len(data['photos'])}:", color="green")
            for photo in data['photos']:
                delay_print(f"URL: {photo['url']}", color="blue")
    else:
        delay_print(f"Error: {response.status_code} - {response.text}", color="red")
#==================================================================================================
def hubgames():
    delay_print("Welcome to hubgames, look the list of games: ", color="blue")
    fast_print('''
1. Space room (not finish)
2. Abandoned house (not finish)
3. number guessing game
(more comming soon)''')
    chose = delay_input("Put the number of game: ")
    if chose == "1":
        number_guessing_game()
    if chose == "2":
        abandoned_house()
    if chose == "3": 
        number_guessing_game()
def abandoned_house():
    delay_print("not finish")

def scape_room():
    delay_print("not finish")

def number_guessing_game():
    delay_print("=== Number Guessing Game ===", color="green")
    number = random.randint(1, 100)
    attempts = 0
    delay_print("I have chosen a number between 1 and 100. Try to guess it!", color="yellow")

    while True:
        guess = int(delay_input("Your guess: ", color="cyan"))
        attempts += 1

        if guess < number:
            delay_print("Too low!", color="red")
        elif guess > number:
            delay_print("Too high!", color="red")
        else:
            delay_print(f"Congratulations! You guessed the number in {attempts} attempts.", color="green")
            break
#==================================================================================================
def note_motion(username):
    delay_print("=== Note Motion ===", color="cyan")

    if username not in notes:
        notes[username] = []

    while True:
        delay_print(f"Notes for {username}:", color="yellow")
        for i, note in enumerate(notes[username], 1):
            delay_print(f"{i}. {note}", color="white")
        
        fast_print('''
1: Add a note
2: Edit a note
3: Delete a note
4: Exit
''', color="cyan")

        option = delay_input("Choose an option: ", color="cyan")

        if option == "1":
            new_note = delay_input("Enter your new note: ", color="yellow")
            notes[username].append(new_note)
            save_notes()
            delay_print("Note added.", color="green")

        elif option == "2":
            note_number = int(delay_input("Enter the note number to edit: ", color="yellow"))
            if 1 <= note_number <= len(notes[username]):
                edited_note = delay_input("Enter the new text: ", color="yellow")
                notes[username][note_number - 1] = edited_note
                save_notes()
                delay_print("Note edited.", color="green")
            else:
                delay_print("Invalid note number.", color="red")

        elif option == "3":
            note_number = int(delay_input("Enter the note number to delete: ", color="yellow"))
            if 1 <= note_number <= len(notes[username]):
                del notes[username][note_number - 1]
                save_notes()
                delay_print("Note deleted.", color="green")
            else:
                delay_print("Invalid note number.", color="red")

        elif option == "4":
            delay_print("Exiting Note Motion...", color="cyan")
            break

        else:
            delay_print("Invalid option. Please try again.", color="red")
#==================================================================================================
def hubai():
    delay_print("Welcome to hubai, look the list of ai: ")
    fast_print('''
1: grok, made by API of groq, for talking
2: Codte, made by API of groq, for codes
3: Milenius, made by API of groq, for text role play(TRP)''')
    delay_print('''WARMING: Modify the code and put your API keys in "YOUR_API_KEY_HERE"''', color="red")
    chose = delay_input("put the number of IA you want")
    if chose == "1":
        grok()
    if chose == "2":
        codte()
    if chose == "3":
        milenius()
    
def milenius():
        client = Groq(
            api_key="YOUR_API_KEY_HERE", )
        delay_print(
            "Tip: Put E to exit\n")

        while True:
            user_input = delay_input("You: \n")

            if user_input.lower() == "s":
                delay_print("Goodbye")
            

            chat_completion = client.chat.completions.create(
                messages=[{
                "role":
                "system",
                "content":
                "You are Grok, an ia create for play text role play (TRP)"
            }, {
                "role": "user",
                "content": user_input,
            }],
            model="llama3-8b-8192",
        )

            response = chat_completion.choices[0].message.content

            rprint("Grok: \n")
            delay_print("", response)
            print("\n")

def codte():
        client = Groq(
            api_key="YOUR_API_KEY_HERE", )
        delay_print(
            "Tip: Put E to exit\n")

        while True:
            user_input = delay_input("You: \n")

            if user_input.lower() == "s":
                delay_print("Goodbye")
            

            chat_completion = client.chat.completions.create(
                messages=[{
                "role":
                "system",
                "content":
                "You are Codte, an AI make for create a codes"
            }, {
                "role": "user",
                "content": user_input,
            }],
            model="llama3-8b-8192",
        )

            response = chat_completion.choices[0].message.content

            rprint("Grok: \n")
            delay_print(""+ response)
            print("\n")

def grok():
        client = Groq(
            api_key="YOUR_API_KEY_HERE", )
        delay_print(
            "Tip: Put E to exit\n")

        while True:
            user_input = delay_input("You: \n")

            if user_input.lower() == "s":
                delay_print("Goodbye")
            

            chat_completion = client.chat.completions.create(
                messages=[{
                "role":
                "system",
                "content":
                "You are Grok, an ia create for chating with everything"
            }, {
                "role": "user",
                "content": user_input,
            }],
            model="llama3-8b-8192",
        )

            response = chat_completion.choices[0].message.content

            rprint("Grok: \n")
            delay_print(""+ response)
            print("\n")
#==================================================================================================
def account(username):
    delay_print(f"Welcome, {username}!", color="cyan")
    delay_print("Here are your options:")
    fast_print('''
1: Hubgames
2: Search images
3: Hubai (modify the code and put your API)
4: Note motion''', color="cyan")
    choice = delay_input("Enter the number of what you want to do: ", color="cyan")
    if choice == "1":
        delay_print("Opening Hubgames...", color="blue")
        hubgames()
    elif choice == "2":
        delay_print("Opening search images with Pexels API...", color="blue")
        search_images()
    elif choice == "3":
        delay_print("Opening Hubai (warning: Modify the code to use the AI function)", color="blue")
        hubai()
    elif choice == "4":
        delay_print("Opening Note Motion...", color="blue")
        note_motion(username)
    else:
        delay_print("Invalid option. Please try again.", color="red")
        account(username)
#==================================================================================================
def main_login():
    rprint('''[green]
  ____   __   __  _   _    _   _    ____   
U|  _"\ u\ \ / / |'| |'|U |"|u| |U | __")u 
\| |_) |/ \ V / /| |_| |\\| |\| | \|  _ \/ 
 |  __/  U_|"|_uU|  _  |u | |_| |  | |_) | 
 |_|       |_|   |_| |_| <<\___/   |____/  
 ||>>_ .-,//|(_  //   \\(__) )(   _|| \\_  
(__)__) \_) (__)(_") ("_)   (__) (__) (__) \n
    0.0.0.1
    (note: Not everything is ready)''')
    time.sleep(2)
    delay_print("Welcome to PyHub, a simple hub in constant updating. You need to create an account or log in to an account")
    fast_print('''1: Create Account
2: Login
3: Exit''')

    choice = delay_input("Choose an option: ", color="cyan")

    if choice == "1":
        create_account_interface()
    elif choice == "2":
        login_interface()
    elif choice == "3":
        delay_print("Exiting...")
    else:
        delay_print("Invalid option. Please try again.")
        main_login()
#==================================================================================================
def create_account_interface():
    delay_print("==== Create Account ====", color="cyan")
    username = delay_input("Username: ", color="yellow")
    password = delay_input("Password: ", color="yellow")
    confirmation = delay_input("Confirm your password: ", color="yellow")

    if password != confirmation:
        delay_print("Passwords do not match. Please try again.", color="red")
        os.system("clear")
        create_account_interface()
    else:
        result = create_account(username, password)
        delay_print(result, color="green" if "successfully" in result else "red")
        main_login()
#==================================================================================================
def login_interface():
    delay_print("==== Login ====", color="cyan")
    username = delay_input("Username: ", color="yellow")
    password = delay_input("Password: ", color="yellow")
    result = login(username, password)
    delay_print(result, color="green" if "successful" in result else "red")
    if "successful" in result:
        account(username)
#==================================================================================================

if __name__ == "__main__":
    main_login()
