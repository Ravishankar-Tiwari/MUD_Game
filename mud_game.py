import os
import random
import json


# ------------------ ANSI Color Class ------------------ #
class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'


# ------------------ ASCII Art & Story ------------------ #
def display_ascii_art():
    ascii_art = r"""
__________.__                 __            .__                            
\______   \  | _____    ____ |  | __   ____ |  |   _______  __ ___________ 
 |    |  _/  | \__  \ _/ ___\|  |/ / _/ ___\|  |  /  _ \  \/ // __ \_  __ \
 |    |   \  |__/ __ \\  \___|    <  \  \___|  |_(  <_> )   /\  ___/|  | \/
 |______  /____(____  /\___  >__|_ \  \___  >____/\____/ \_/  \___  >__|    
        \/          \/     \/     \/      \/                      \/       
"""
    print(ascii_art)


STORY_TEXT = """
You are a young mage in the world of Black Clover, aspiring to become the Wizard King.
To achieve greatness, you must train, battle, complete quests, and rise through the ranks of the Magic Knights.
Join a squad, enhance your grimoire, and face powerful foes.
Only the strongest and most strategic will survive the trials ahead.
Are you ready to embark on your journey?
"""


# ------------------ Player Class ------------------ #
class Player:
    def __init__(self, name, magic_type, password):
        self.name = name
        self.magic_type = magic_type
        self.password = password
        self.level = 1
        self.experience = 0
        self.spells = []  # Additional spells can be added
        self.kingdoms_won = []   # Kingdoms the player has conquered
        self.sword_awards = []   # Swords earned from elite battles
        self.kingdom = ""        # Current kingdom engaged
        self.magic = 10          # Generic magic attribute (unused so far)
        # New attributes for interactive battle
        self.hp = 100
        self.max_hp = 100
        self.mana = 50
        self.max_mana = 50
        self.inventory = {"Health Potion": 2, "Mana Potion": 1}

    def level_up(self):
        self.level += 1
        print(f"{self.name} leveled up to level {self.level}!")
        # Increase max HP and Mana with level (optional)
        self.max_hp += 10
        self.max_mana += 5
        # Restore health and mana on level up
        self.hp = self.max_hp
        self.mana = self.max_mana

    def cast_spell(self, spell):
        # Spell is a dict containing 'name', 'cost', and 'damage_range'
        if self.mana >= spell['cost']:
            self.mana -= spell['cost']
            damage = random.randint(*spell['damage_range'])
            print(f"{self.name} casts {spell['name']} for {damage} damage (cost {spell['cost']} mana)!")
            return damage
        else:
            print("Not enough mana!")
            return 0

    def login(self, entered_password):
        return entered_password == self.password

    def to_dict(self):
        return {
            'name': self.name,
            'magic_type': self.magic_type,
            'password': self.password,
            'level': self.level,
            'experience': self.experience,
            'spells': self.spells,
            'kingdoms_won': self.kingdoms_won,
            'sword_awards': self.sword_awards,
            'kingdom': self.kingdom,
            'magic': self.magic,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'inventory': self.inventory
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data['name'], data['magic_type'], data['password'])
        player.level = data['level']
        player.experience = data['experience']
        player.spells = data['spells']
        player.kingdoms_won = data['kingdoms_won']
        player.sword_awards = data['sword_awards']
        player.kingdom = data.get('kingdom', "")
        player.magic = data.get('magic', 10)
        player.hp = data.get('hp', 100)
        player.max_hp = data.get('max_hp', 100)
        player.mana = data.get('mana', 50)
        player.max_mana = data.get('max_mana', 50)
        player.inventory = data.get('inventory', {"Health Potion": 2, "Mana Potion": 1})
        return player


# ------------------ BlackCloverMUD Class ------------------ #
class BlackCloverMUD:
    data_folder = "LoadData"
    valid_magic_types = ["Fire", "Water", "Wind", "Earth", "Lightning"]
    levels = ['Ignite', 'Illuminate', 'Elite']

    def __init__(self):
        self.players = []
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    # -------- Player Creation -------- #
    def create_player(self, name, magic_type, password):
        for player in self.players:
            if player.name.lower() == name.lower():
                print("Username already taken. Please choose a different name.")
                return False

        if magic_type.capitalize() not in self.valid_magic_types:
            print("Invalid magic type. Please choose from:", ", ".join(self.valid_magic_types))
            return False

        player = Player(name, magic_type.capitalize(), password)
        self.players.append(player)
        print(f"Welcome to the Black Clover MUD, {player.name}! You are a {player.magic_type} mage.")
        return True

    # -------- Login -------- #
    def login_player(self, entered_name, entered_password):
        for player in self.players:
            if player.name.lower() == entered_name.lower():
                if player.login(entered_password):
                    print(f"Welcome back, {player.name}!")
                    return player
                else:
                    print("Incorrect password. Please try again.")
                    return None
        print("Player not found.")
        return None

    # -------- Default Spell Lookup -------- #
    def get_default_spell(self, player):
        default_spells = {
            "Fire": {"name": "Fireball", "cost": 10, "damage_range": (15, 25)},
            "Water": {"name": "Water Jet", "cost": 10, "damage_range": (12, 22)},
            "Wind": {"name": "Wind Slash", "cost": 8, "damage_range": (10, 20)},
            "Earth": {"name": "Rock Smash", "cost": 12, "damage_range": (14, 24)},
            "Lightning": {"name": "Lightning Strike", "cost": 10, "damage_range": (15, 25)}
        }
        return default_spells.get(player.magic_type, None)

    # -------- Interactive Turn-Based Battle -------- #
    def battle(self, player):
        level_index = 0
        while level_index < len(self.levels):
            level = self.levels[level_index]
            print(f"\n{Color.BOLD}{player.name}, you are entering the {level} level battle in the {player.kingdom} kingdom!{Color.RESET}")
            # Restore player's HP and mana at the start of each level
            player.hp = player.max_hp
            player.mana = player.max_mana

            # Generate enemy based on level
            enemy_hp = 20 + level_index * 10
            enemy_attack_min = 5 + level_index
            enemy_attack_max = 10 + level_index
            enemy_name = random.choice(["Goblin", "Dark Mage", "Imp", "Demon Servant"])
            enemy = {"name": enemy_name, "hp": enemy_hp, "attack_min": enemy_attack_min, "attack_max": enemy_attack_max}
            print(f"A wild {enemy['name']} appears with {enemy['hp']} HP!")

            defended = False  # Flag for defending this turn

            # Battle loop for the current level
            while enemy["hp"] > 0 and player.hp > 0:
                print(f"\n{Color.CYAN}{player.name}'s HP: {player.hp}/{player.max_hp} | Mana: {player.mana}/{player.max_mana}{Color.RESET}")
                print(f"{Color.MAGENTA}{enemy['name']}'s HP: {enemy['hp']}{Color.RESET}")
                print("Choose your action:")
                print("1. Attack")
                print("2. Cast Spell")
                print("3. Defend")
                print("4. Use Item")
                print("5. Flee")

                action = input(Color.YELLOW + "Enter action (1-5): " + Color.RESET).strip()

                if action == '1':
                    # Normal attack
                    damage = random.randint(5, 10) + player.level
                    enemy["hp"] -= damage
                    print(f"You attack and deal {damage} damage!")
                elif action == '2':
                    # Cast spell using default spell for player's magic type
                    spell = self.get_default_spell(player)
                    if spell:
                        damage = player.cast_spell(spell)
                        enemy["hp"] -= damage
                    else:
                        print("No default spell available for your magic type.")
                elif action == '3':
                    # Defend (reduces damage on enemy attack)
                    defended = True
                    print("You brace yourself to reduce incoming damage.")
                elif action == '4':
                    # Use item from inventory
                    if player.inventory:
                        print("Inventory:")
                        for item, count in player.inventory.items():
                            print(f"- {item}: {count}")
                        item_choice = input("Enter the item name to use: ").strip()
                        if item_choice in player.inventory and player.inventory[item_choice] > 0:
                            if item_choice.lower() == "health potion":
                                heal = 30
                                player.hp = min(player.hp + heal, player.max_hp)
                                print(f"You used a Health Potion and recovered {heal} HP!")
                            elif item_choice.lower() == "mana potion":
                                restore = 20
                                player.mana = min(player.mana + restore, player.max_mana)
                                print(f"You used a Mana Potion and restored {restore} mana!")
                            else:
                                print("Item has no effect.")
                            player.inventory[item_choice] -= 1
                        else:
                            print("You don't have that item.")
                    else:
                        print("Your inventory is empty.")
                elif action == '5':
                    # Attempt to flee (50% chance)
                    if random.random() < 0.5:
                        print("You managed to flee from the battle!")
                        return  # Exit battle (counts as a loss)
                    else:
                        print("Flee attempt failed!")
                else:
                    print("Invalid action. Try again.")
                    continue

                # Check if enemy is defeated
                if enemy["hp"] <= 0:
                    print(Color.BOLD + Color.GREEN + f"You defeated the {enemy['name']}!" + Color.RESET)
                    if level == 'Elite':
                        sword_award = self.get_sword_award(player.kingdom)
                        print(f"Congratulations, {player.name}! You've conquered the {player.kingdom} kingdom and earned a {sword_award}!")
                        player.sword_awards.append(sword_award)
                        player.kingdoms_won.append(player.kingdom)
                        if set(player.sword_awards) == {'Demon Slayer', 'Demon Dweller', 'Demon Destroyer', 'Demon-Majestic'}:
                            print(f"Congratulations, {player.name}! You are now the Wizard King!")
                    player.level_up()
                    break

                # Enemy's turn to attack if still alive
                enemy_damage = random.randint(enemy["attack_min"], enemy["attack_max"])
                if defended:
                    enemy_damage = enemy_damage // 2
                    print("Your defense reduces the incoming damage!")
                    defended = False  # Reset defend flag
                player.hp -= enemy_damage
                print(f"{enemy['name']} attacks and deals {enemy_damage} damage!")

                # Check if player is defeated
                if player.hp <= 0:
                    print(Color.BOLD + Color.RED + "You have been defeated!" + Color.RESET)
                    # Offer restart or repeat option
                    while True:
                        choice = input("Do you want to restart this level or repeat the previous one? (restart/repeat): ").lower()
                        if choice == 'restart':
                            break  # Restart current level (will reinitialize HP/mana)
                        elif choice == 'repeat' and level_index > 0:
                            level_index -= 1  # Go back to previous level
                            break
                        else:
                            print("Invalid choice. Please enter 'restart' or 'repeat'.")
                    break  # Exit the battle loop for this level

            # If player was defeated, exit battle early
            if player.hp <= 0:
                print("Recover and try again later...")
                return

            level_index += 1

    def get_sword_award(self, kingdom):
        sword_rewards = {
            'Clover': 'Demon Slayer',
            'Diamond': 'Demon Dweller',
            'Heart': 'Demon Destroyer',
            'Spade': 'Demon-Majestic'
        }
        return sword_rewards.get(kingdom, 'Unknown Sword')

    # -------- Quest System -------- #
    def quest(self, player):
        print("\nA mysterious quest appears!")
        print("You must retrieve a lost grimoire page from the cursed library.")
        answer = input("Do you accept the quest? (yes/no): ").strip().lower()
        if answer == "yes":
            print("You embark on the quest...")
            # Simulate quest challenge with a success chance
            if random.random() < 0.7:
                print(Color.GREEN + "Quest successful! You found the grimoire page." + Color.RESET)
                player.experience += 50
                print("You gained 50 experience points!")
            else:
                print(Color.RED + "Quest failed. Better luck next time." + Color.RESET)
        else:
            print("You declined the quest.")

    # -------- Saving & Loading -------- #
    def save_game(self, player):
        with open(os.path.join(self.data_folder, f"{player.name}_save.json"), 'w') as file:
            json.dump(player.to_dict(), file)
        print(Color.BOLD + Color.GREEN + "Game saved successfully." + Color.RESET)

    def load_game(self, player_name):
        existing_player = next((p for p in self.players if p.name.lower() == player_name.lower()), None)
        if existing_player:
            print(f"Player {player_name} is already loaded.")
            return existing_player
        try:
            with open(os.path.join(self.data_folder, f"{player_name}_save.json"), 'r') as file:
                data = json.load(file)
                player = Player.from_dict(data)
                self.players.append(player)
                print(f"Game loaded successfully for {player_name}.")
                return player
        except FileNotFoundError:
            print(f"No saved game found for {player_name}.")
        return None

    def save_players_data(self):
        data = [player.to_dict() for player in self.players]
        with open(os.path.join(self.data_folder, 'players_data.json'), 'w') as file:
            json.dump(data, file)
        print("Players' data saved successfully.")

    def load_players_data(self):
        try:
            with open(os.path.join(self.data_folder, 'players_data.json'), 'r') as file:
                data = json.load(file)
                self.players = [Player.from_dict(player_data) for player_data in data]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"An error occurred while loading players' data: {e}")

    # -------- Other Utilities -------- #
    def list_players(self):
        print("Current Players:")
        for player in self.players:
            print(f"- {player.name}, {player.magic_type} mage")

    def display_leaderboard(self):
        sorted_players = sorted(self.players, key=lambda x: (len(x.sword_awards), x.level), reverse=True)
        print("\nLeaderboard:")
        for i, player in enumerate(sorted_players, start=1):
            swords_earned = ', '.join(player.sword_awards) if player.sword_awards else 'None'
            kingdoms_won = ', '.join(player.kingdoms_won) if player.kingdoms_won else 'None'
            print(f"{i}. {player.name} - Level: {player.level}, Swords: {swords_earned}, Kingdoms Conquered: {kingdoms_won}")

    def delete_player_data(self, player_name):
        player_to_delete = next((p for p in self.players if p.name.lower() == player_name.lower()), None)
        if player_to_delete:
            self.players.remove(player_to_delete)
            save_file_path = os.path.join(self.data_folder, f"{player_name}_save.json")
            if os.path.exists(save_file_path):
                os.remove(save_file_path)
            print(f"Player data for {player_name} deleted successfully.")
        else:
            print(f"No player found with the name {player_name}.")

    # -------- Main Game Loop -------- #
    def start_game(self):
        self.load_players_data()
        display_ascii_art()
        print(Color.BOLD + Color.GREEN + STORY_TEXT + Color.RESET)

        if os.path.exists('welcome.txt'):
            with open('welcome.txt', 'r') as file:
                welcome_message = file.read()
                print(Color.BOLD + Color.GREEN + welcome_message + Color.RESET)

        active_player = None

        while True:
            print("\n" + Color.BOLD + "MAIN MENU" + Color.RESET)
            print("1. " + Color.BLUE + "Create a new player" + Color.RESET)
            print("2. " + Color.BLUE + "Log in" + Color.RESET)
            print("3. " + Color.BLUE + "Choose Kingdom (for active player)" + Color.RESET)
            print("4. " + Color.BLUE + "List players" + Color.RESET)
            print("5. " + Color.BLUE + "Leaderboard" + Color.RESET)
            print("6. " + Color.BLUE + "Save Game (active player)" + Color.RESET)
            print("7. " + Color.BLUE + "Load Game" + Color.RESET)
            print("8. " + Color.BLUE + "Delete Player Data" + Color.RESET)
            print("9. " + Color.BLUE + "Embark on a Quest" + Color.RESET)
            print("10. " + Color.RED + "Exit" + Color.RESET)

            choice = input(Color.YELLOW + "Enter your choice: " + Color.RESET).strip()

            if choice == '1':
                name = input("Enter your name: ").strip()
                magic_type = input("Choose your magic type (Fire, Water, Wind, Earth, Lightning): ").strip()
                password = input("Enter your password: ").strip()
                created = self.create_player(name, magic_type, password)
                if created:
                    active_player = next((p for p in self.players if p.name.lower() == name.lower()), None)

            elif choice == '2':
                while True:
                    entered_name = input("Enter your name (or type 'back' to return): ").strip()
                    if entered_name.lower() == 'back':
                        break
                    entered_password = input("Enter your password: ").strip()
                    player = self.login_player(entered_name, entered_password)
                    if player is None:
                        retry_choice = input("Would you like to try again (T) or create a new character (N)? ").strip().lower()
                        if retry_choice == 'n':
                            name = input("Enter your name: ").strip()
                            magic_type = input("Choose your magic type (Fire, Water, Wind, Earth, Lightning): ").strip()
                            password = input("Enter your password: ").strip()
                            created = self.create_player(name, magic_type, password)
                            if created:
                                active_player = next((p for p in self.players if p.name.lower() == name.lower()), None)
                                break
                        else:
                            continue
                    else:
                        active_player = player
                        break

            elif choice == '3':
                if not active_player:
                    print("No active player. Please create or log in first.")
                else:
                    # Let the active player choose a kingdom if not already conquered
                    print("\nChoose the kingdom you want to battle in:")
                    available_kingdoms = [kingdom for kingdom in ["Clover", "Diamond", "Heart", "Spade"]
                                          if kingdom not in active_player.kingdoms_won]
                    if not available_kingdoms:
                        print("You have already won all kingdoms. There are no more battles.")
                    else:
                        for idx, kingdom in enumerate(available_kingdoms, 1):
                            print(f"{idx}. {kingdom}")
                        choice_kingdom = input(f"Enter your choice (1-{len(available_kingdoms)}): ").strip()
                        if choice_kingdom.isdigit() and 1 <= int(choice_kingdom) <= len(available_kingdoms):
                            selected_kingdom = available_kingdoms[int(choice_kingdom) - 1]
                            active_player.kingdom = selected_kingdom
                            print(f"{active_player.name}, you have chosen the {selected_kingdom} kingdom for battle!")
                            self.battle(active_player)
                        else:
                            print("Invalid kingdom choice.")

            elif choice == '4':
                self.list_players()

            elif choice == '5':
                self.display_leaderboard()

            elif choice == '6':
                if not active_player:
                    print("No active player. Please create or log in first.")
                else:
                    self.save_game(active_player)

            elif choice == '7':
                player_name = input("Enter your name to load the game: ").strip()
                loaded_player = self.load_game(player_name)
                if loaded_player:
                    active_player = loaded_player

            elif choice == '8':
                player_name = input("Enter the name of the player to delete: ").strip()
                self.delete_player_data(player_name)

            elif choice == '9':
                if not active_player:
                    print("No active player. Please create or log in first.")
                else:
                    self.quest(active_player)

            elif choice == '10':
                self.save_players_data()
                print("Thanks for playing! Goodbye.")
                break

            else:
                print(Color.RED + "Invalid choice. Please try again." + Color.RESET)


# ------------------ Main Execution ------------------ #
if __name__ == "__main__":
    game = BlackCloverMUD()
    game.start_game()
