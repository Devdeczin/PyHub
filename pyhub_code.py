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

# Credenciais do administrador embutidas
ADMIN_USERNAME = "Devdec"

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

# Carregar dados de usuários
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

users = load_users()

# Garantir que todos os usuários tenham as chaves necessárias
for user in users.values():
    if 'coins' not in user:
        user['coins'] = 100
    if 'inventory' not in user:
        user['inventory'] = []
save_users(users)

# Adicionar conta de administrador se não existir
if ADMIN_USERNAME not in users:
    users[ADMIN_USERNAME] = {
        'password': hash_password("#Devdec1910"),
        'coins': float('inf'),  # Quantidade inicial de moedas para o admin
        'inventory': [],
        'admin': True  # Flag de administrador
    }
    save_users(users)

ADMIN_PASSWORD_HASH = read_admin_secret()

def create_account(username, password):
    if username in users:
        return "User already exists."
    users[username] = {
        'password': hash_password(password),
        'coins': 100,  # Quantidade inicial de moedas
        'inventory': []  # Inventário inicial vazio
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
    delay_print("Bem-vindo ao Adivinhe o Número!", "green")
    delay_print("Tente adivinhar o número entre 1 e 100.", "green")
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    while True:
        tentativa = int(delay_input("Digite um número: ", "green"))
        tentativas += 1
        if tentativa < numero_secreto:
            delay_print("O número é maior. Tente novamente.", "green")
        elif tentativa > numero_secreto:
            delay_print("O número é menor. Tente novamente.", "green")
        else:
            delay_print(f"Parabéns! Você acertou o número em {tentativas} tentativas.", "green")
            add_money(username, 10)  # Adiciona 10 moedas como recompensa
            delay_print(f"Você ganhou 10 moedas! Agora você tem {users[username]['coins']} moedas.", "green")
            break

def loja_incrivel(username):
    items = {
        '1': {'name': 'Fazedor de loja (jogo)', 'price': 50},
        '2': {'name': 'Hubai (inteligências artificiais)', 'price': 70},
        '3': {'name': 'Achar imagens (nome alto explicativo)', 'price': 30}
    }

    def display_items():
        delay_print("=== Loja Incrível ===", "magenta")
        for key, item in items.items():
            delay_print(f"{key}: {item['name']} - {item['price']} moedas", "magenta")

    def buy_item(choice):
        item = items.get(choice)
        if item and users[username]['coins'] >= item['price']:
            users[username]['coins'] -= item['price']
            users[username]['inventory'].append(item['name'])
            delay_print(f"Você comprou {item['name']} por {item['price']} moedas.", "magenta")
            save_users(users)
        else:
            delay_print("Moedas insuficientes ou item inválido.", "red")

    while True:
        display_items()
        choice = delay_input("Escolha um item para comprar ou 'sair' para voltar: ", "magenta")
        if choice.lower() == 'sair':
            break
        buy_item(choice)

def view_inventory(username):
    delay_print(f"Inventário de {username}:", "cyan")
    inventory = users[username]['inventory']
    if inventory:
        for idx, item in enumerate(inventory, 1):
            delay_print(f"{idx}: {item}", "cyan")
        choice = delay_input("Digite o número do item para usar ou 'sair' para voltar: ", "cyan").strip().lower()
        if choice != 'sair' and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(inventory):
                use_item(username, inventory[idx])
            else:
                delay_print("Escolha inválida.", "red")
    else:
        delay_print("Seu inventário está vazio.", "cyan")

def achar_imagens(username):
    delay_print("=== Achar imagens ===")
    delay_print("Bem vindo ao achar imagens, melhorado pelo unsplash")
    delay_print("Antes de começar, você precisa de uma API key do unsplash, para obte-la, apenas clique no link abaixo e siga as instruções")
    delay_print("https://unsplash.com/developers")
    ACCESS_KEY = delay_input("bom coloque sua API aqui quando pega-la no site: ")
    search = delay_input("Agora que você tem sua API, coloque a imagem que quer ver: ")
    url = 'https://api.unsplash.com/photos/random'
    headers = {'Authorization': f'Client-ID {ACCESS_KEY}'}
    search = requests.get(url, headers=headers)
    data = search.json()
    delay_print(data)
    
def criador_de_loja(username):
    delay_print("")

def hubai(username):
    delay_print("")

def use_item(username, item_name):
    if item_name == 'criador de loja (jogo)':
        criador_de_loja(username)
    elif item_name == 'Hubai (inteligências artificiais)':
        delay_print("Abrindo Hubai...", "green")
        hubai(username)
    elif item_name == 'Achar imagens (nome alto explicativo)':
        delay_print("Abrindo Achar imagens...", "green")
        achar_imagens(username)
    else:
        delay_print("Item desconhecido.", "red")

def add_money(username, amount):
    users[username]['coins'] += amount
    save_users(users)

def account(username):
    delay_print(f"Bem-vindo, {username}!", color="cyan")
    if 'coins' not in users[username]:
        users[username]['coins'] = 100
    if 'inventory' not in users[username]:
        users[username]['inventory'] = []
    delay_print(f"Você tem {users[username]['coins']} moedas.", color="cyan")
    delay_print("O que você quer fazer? Olhe a lista abaixo:", color="cyan")
    delay_print('''
    1: Adivinhe o número
    2: Loja Incrível
    3: Ver Inventário
    4: Adicionar Dinheiro
    5: Sair''')
    if users[username].get('admin'):
        delay_print("6: Opções de Administrador", color="red")
    choice = delay_input("Escolha uma opção: ").strip().lower()
    if choice == "1":
        adivinhe_o_numero(username)
    elif choice == "2":
        loja_incrivel(username)
    elif choice == "3":
        view_inventory(username)
    elif choice == "4":
        amount = int(delay_input("Digite a quantidade de dinheiro para adicionar: ", "yellow"))
        add_money(username, amount)
        delay_print(f"{amount} moedas foram adicionadas. Agora você tem {users[username]['coins']} moedas.", "green")
    elif choice == "5":
        delay_print("Saindo...")
    elif choice == "6" and users[username].get('admin'):
        admin_options(username)
    else:
        delay_print("Opção inválida. Tente novamente.")
        account(username)

def admin_options(username):
    delay_print("=== Opções de Administrador ===", "red")
    delay_print("1: Ver todos os usuários", "red")
    delay_print("2: Adicionar moedas a um usuário", "red")
    delay_print("3: Atualizar senha do administrador", "red")
    delay_print("4: Sair", "red")
    choice = delay_input("Escolha uma opção: ", "red").strip().lower()
    if choice == "1":
        for user, details in users.items():
            delay_print(f"Usuário: {user}, Moedas: {details['coins']}, Inventário: {details['inventory']}", "red")
    elif choice == "2":
        user_to_add_coins = delay_input("Digite o nome do usuário: ", "yellow")
        if user_to_add_coins in users:
            amount = int(delay_input("Digite a quantidade de moedas para adicionar: ", "yellow"))
            add_money(user_to_add_coins, amount)
            delay_print(f"{amount} moedas foram adicionadas ao usuário {user_to_add_coins}.", "green")
        else:
            delay_print("Usuário não encontrado.", "red")
    elif choice == "3":
        if username != ADMIN_USERNAME:
            delay_print("Você não tem permissão para alterar a senha do administrador.", "red")
        else:
            new_password = delay_input("Digite a nova senha do administrador: ", "yellow")
            update_admin_secret(new_password)
            delay_print("Senha do administrador atualizada com sucesso.", "green")
    elif choice == "4":
        return
    else:
        delay_print("Opção inválida. Tente novamente.", "red")
        admin_options(username)

def main_login():
    delay_print("=== Bem-vindo ===", color="cyan")
    delay_print("Bem-vindo ao PyHub, um hub de jogos de texto criado pelo devdec. Crie uma conta ou entre em uma para poder usar o PyHub!", color="cyan")
    delay_print("1: Criar conta\n2: Login\n3: Sair", color="cyan")
    choice = delay_input("Escolha uma opção: ", color="cyan").strip().lower()
    if choice == "1":
        create_account_interface()
    elif choice == "2":
        login_interface()
    elif choice == "3":
        delay_print("Saindo...")
    else:
        delay_print("Opção inválida. Tente novamente.")
        main_login()

def create_account_interface():
    delay_print("==== Criar conta ====", color="cyan")
    username = delay_input("Nome de usuário: ", color="yellow")
    password = delay_input("Senha: ", color="yellow")
    confirmation = delay_input("Confirmar senha: ", color="yellow")

    if password != confirmation:
        delay_print("As senhas não batem, tente de novo", color="red")
        create_account_interface()
    else:
        result = create_account(username, password)
        delay_print(result, color="green" if "Account created successfully" in result else "red")
        if "Account created successfully" in result:
            login_interface()

def login_interface():
    delay_print("==== Login ====", color="cyan")
    username = delay_input("Usuário: ", color="yellow")
    password = delay_input("Senha: ", color="yellow")
    result = login(username, password)
    delay_print(result, color="green" if "Login successful" in result else "red")
    if "Login successful" in result:
        account(username)

if __name__ == "__main__":
    main_login()
