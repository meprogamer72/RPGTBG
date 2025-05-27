import random

GRID_SIZE = 10
GRID = [["~"] * GRID_SIZE for _ in range(GRID_SIZE)]
POSSIBLE_COORDS = list(range(GRID_SIZE))
player_x = 0
player_y = 0
player_hp = 3  # Initial player health
found = False
enemy_x = -1  # Initialize enemy coordinates
enemy_y = -1
enemy_hp = 3  # enemy hp
enemy2_x = -1
enemy2_y = -1
enemy2_hp = 3
enemy_defeated = False  # Flag to track enemy defeat
enemy2_defeated = False
unlocked_strong_attack = False
player_name = ""
moves_since_encounter = 0
encounter_chance = 0


def generate_secret_coordinates():
    """Generates secret coordinates, ensuring they are not (0, 0)."""
    while True:
        secret_x = random.choice(POSSIBLE_COORDS)
        secret_y = random.choice(POSSIBLE_COORDS)
        if (secret_x, secret_y) != (0, 0):
            return secret_x, secret_y


def generate_enemy_coordinates(secret_x, secret_y):
    """Generates enemy coordinates, ensuring they are not (0, 0) or the same as the secret."""
    while True:
        enemy_x = random.choice(POSSIBLE_COORDS)
        enemy_y = random.choice(POSSIBLE_COORDS)
        if (
            (enemy_x, enemy_y) != (0, 0)
            and (enemy_x, enemy_y) != (secret_x, secret_y)
        ):
            return enemy_x, enemy_y


def generate_enemy2_coordinates(secret_x, secret_y, enemy_x, enemy_y):
    while True:
        enemy2_x = random.choice(POSSIBLE_COORDS)
        enemy2_y = random.choice(POSSIBLE_COORDS)
        if (
            (enemy2_x, enemy2_y) != (0, 0)
            and (enemy2_x, enemy2_y) != (secret_x, secret_y)
            and (enemy2_x, enemy2_y) != (enemy_x, enemy_y)
        ):
            return enemy2_x, enemy2_y


def generate_player_coordinates(secret_x, secret_y, enemy_x, enemy_y, enemy2_x, enemy2_y):
    """Generates player coordinates, ensuring they are not on the secret or enemy locations."""
    while True:
        player_x = random.choice(POSSIBLE_COORDS)
        player_y = random.choice(POSSIBLE_COORDS)
        if (player_x, player_y) not in [
            (secret_x, secret_y),
            (enemy_x, enemy_y),
            (enemy2_x, enemy2_y),
        ]:
            return player_x, player_y


def display_grid():
    """Displays the grid with player, secret, and enemy positions."""
    for y in range(GRID_SIZE):
        row_str = ""
        for x in range(GRID_SIZE):
            if x == player_x and y == player_y:
                row_str += "[P]"  # Player
            elif x == enemy_x and y == enemy_y:
                row_str += "[E1]"  # Enemy 1
            elif x == enemy2_x and y == enemy2_y:
                row_str += "[E2]"  # Enemy 2
            elif GRID[x][y] == "X":
                row_str += "[X]"  # Treasure
            else:
                row_str += "[~]"  # Water
        print(row_str)


def handle_enemy_combat(enemy_num):
    """Handles combat with the enemy."""
    global player_hp, enemy_hp, enemy2_hp, enemy_defeated, enemy2_defeated, unlocked_strong_attack  # Need to modify the global variables
    if enemy_num == 1:
        print("A wild enemy 1 appears!")
    elif enemy_num == 2:
        print("A wild enemy 2 appears!")

    while player_hp > 0 and (
        (enemy_num == 1 and enemy_hp > 0) or (enemy_num == 2 and enemy2_hp > 0)
    ):
        print(f"{player_name}'s HP: {player_hp}")  # Use player's name
        if enemy_num == 1:
            print(f"Enemy 1 HP: {enemy_hp}")
        elif enemy_num == 2:
            print(f"Enemy 2 HP: {enemy2_hp}")
        print("Choose your attack:")
        print("1. Quick Attack")
        print("2. Strong Attack")
        if unlocked_strong_attack:
            print("3. Super Attack (Unlocked!)")
        action = input("Fight/Run? ").capitalize()
        if action == "Fight":
            attack = input("Enter attack number (1-3): ")
            if attack == "1":
                player_attack = (
                    random.randint(1, 2) #+ wooden_sword_buff # Removed
                )  # Quick Attack damage
                print(
                    f"{player_name} uses Quick Attack for {player_attack} damage!"
                )  # Use player's name
            elif attack == "2":
                player_attack = (
                    random.randint(2, 3) #+ wooden_sword_buff # Removed
                )  # Strong Attack damage
                print(
                    f"{player_name} uses Strong Attack for {player_attack} damage!"
                )  # Use player's name
            elif attack == "3" and unlocked_strong_attack:
                player_attack = (
                    random.randint(4, 5) #+ wooden_sword_buff # Removed
                )  # Super Attack damage
                print(
                    f"{player_name} uses Super Attack for {player_attack} damage!"
                )  # Use player's name
            else:
                print("Invalid attack choice. Using Quick Attack.")
                player_attack = random.randint(1, 2) #+ wooden_sword_buff # Removed
                print(
                    f"{player_name} uses Quick Attack for {player_attack} damage!"
                )  # Use player's name

            enemy_attack = random.randint(1, 2)  # Enemy attack
            if enemy_num == 1:
                enemy_hp -= player_attack
                if enemy_hp > 0:
                    print(f"Enemy 1 attacks for {enemy_attack} damage!")
                    player_hp -= enemy_attack
                else:
                    print("You defeated enemy 1!")
                    return 1  # Returns 1 if enemy 1 is defeated
            elif enemy_num == 2:
                enemy2_hp -= player_attack
                if enemy2_hp > 0:
                    print(f"Enemy 2 attacks for {enemy_attack} damage!")
                    player_hp -= enemy_attack
                else:
                    print("You defeated enemy 2!")
                    return 2  # Returns 2 if enemy 2 is defeated
        elif action == "Run":
            print(f"{player_name} ran away!")  # Use player's name
            return 0  # Player ran away, no game over, but no treasure either.
        else:
            print("Invalid action!")

    if player_hp <= 0:
        print(f"{player_name} was defeated!")  # Use player's name
        return 3  # Returns 3 if player is defeated
    return 0


def handle_encounter():
    """Handles random encounters."""
    global player_hp, player_x, player_y, enemy_x, enemy_y, enemy2_x, enemy2_y #, wooden_sword_buff #Removed
    encounter_chance = random.randint(1, 3)  # 1 for wizard, 2 for old man, 3 for nothing
    if encounter_chance == 1:  # Wizard encounter
        print("You encounter a mysterious wizard!")
        if player_hp > 2:
            teleport_choice = input(
                "The wizard offers to teleport you to an enemy for 2 HP. Do you accept? (yes/no) "
            ).lower()
            if teleport_choice == "yes":
                player_hp -= 2
                print(f"{player_name} agrees to the teleport. HP: {player_hp}")
                # Teleport player to a random enemy
                if enemy_x != -1 and enemy2_x != -1:
                    target_enemy = random.choice([1, 2])
                    if target_enemy == 1:
                        player_x, player_y = enemy_x, enemy_y
                        print(f"{player_name} was teleported to Enemy 1!")
                    else:
                        player_x, player_y = enemy2_x, enemy2_y
                        print(f"{player_name} was teleported to Enemy 2!")
                elif enemy_x != -1:
                    player_x, player_y = enemy_x, enemy_y
                    print(f"{player_name} was teleported to Enemy 1!")
                elif enemy2_x != -1:
                    player_x, player_y = enemy2_x, enemy2_y
                    print(f"{player_name} was teleported to Enemy 2!")
                else:
                    print("But there are no enemies to teleport to!")
            else:
                print("The wizard disappears.")
        else:
            print("The wizard offers a teleport, but you don't have enough HP.")
    elif encounter_chance == 2:  # Wise old man encounter
        print("You meet a wise old man.")
        print("He heals you, increasing your HP by 2!")
        player_hp += 2
        print(f"{player_name}'s HP is now {player_hp}!")
    else:
        print("Nothing happens.")


secret_x, secret_y = generate_secret_coordinates()
enemy_x, enemy_y = generate_enemy_coordinates(secret_x, secret_y)  # Generate enemy AFTER secret
enemy2_x, enemy2_y = generate_enemy2_coordinates(
    secret_x, secret_y, enemy_x, enemy_y
)
player_x, player_y = generate_player_coordinates(
    secret_x, secret_y, enemy_x, enemy_y, enemy2_x, enemy2_y
)  # generate player coordinates
GRID[secret_x][secret_y] = "X"  # Place the secret
GRID[enemy_x][enemy_y] = "E"  # Place the enemy #  Show
GRID[enemy2_x][enemy2_y] = "E"  # Place the enemy # Show

player_name = input("Enter your character's name: ")

print(
    f"Welcome, {player_name}, to the adventure! Your starting position is {player_x + 1}, {player_y + 1}."
)  # Use player's name
while not found and player_hp > 0 and (
    not enemy_defeated or not enemy2_defeated
):  # Added condition to check if both enemies are defeated
    display_grid()
    print(f"{player_name}'s HP: {player_hp}")  # Show Player HP
    player_input = input("(Help for help) >").capitalize()

    move = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}.get(player_input)

    if move:
        dx, dy = move
        new_x, new_y = player_x + dx, player_y + dy

        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            print(f"{player_name} Moved {player_input.lower()}!")  # Use player's name
            player_x, player_y = new_x, new_y
            moves_since_encounter += 1

            if moves_since_encounter >= 2:
                handle_encounter()
                moves_since_encounter = 0  # Reset counter

            if player_x == enemy_x and player_y == enemy_y and enemy_hp > 0:
                result = handle_enemy_combat(1)  # call the function
                if result == 3:
                    break  # game over
                elif result == 1:
                    enemy_defeated = True
                    unlocked_strong_attack = True
                    GRID[enemy_x][enemy_y] = (
                        "~"  #  Show
                    )
                    enemy_x = -1
                    enemy_y = -1
            elif player_x == enemy2_x and player_y == enemy2_y and enemy2_hp > 0:
                result = handle_enemy_combat(2)
                if result == 3:
                    break
                elif result == 2:
                    enemy2_defeated = True
                    unlocked_strong_attack = True
                    GRID[enemy2_x][enemy2_y] = (
                        "~"  #  Show
                    )
                    enemy2_x = -1
                    enemy2_y = -1
            elif GRID[player_x][player_y] == "X" and enemy_defeated and enemy2_defeated:
                found = True
        else:
            print("You're Out Of Range!")

    elif player_input == "Lifeistoohard":
        print(f"Secret: {secret_x + 1}, {secret_y + 1}")
        print(f"Enemy 1: {enemy_x + 1}, {enemy_y + 1}")
        print(f"Enemy 2: {enemy2_x + 1}, {enemy2_y + 1}")
        print("Found Is", found)
        print(f"Player HP: {player_hp}")
        print("Enemy 1 Defeated:", enemy_defeated)
        print("Enemy 2 Defeated", enemy2_defeated)
        print("Moves Since Encounter:", moves_since_encounter)

    elif player_input == "Help":
        print("Type Up, Down, Left or Right to move one spot in the grid")
        print("Move around until you find the secret grid block")
        print("Defeat the Enemies!")
        print("Every 2 moves, you will encounter a random event.")
        print("Good Luck, " + player_name + "!")  # Use player's name
        print("--------------------------")

if found:
    display_grid()
    print(
        f"Congratulations, {player_name}! You Found The Secret Square and defeated both enemies!"
    )  # Use player's name
    print("Thanks For Playing! :D")

elif player_hp <= 0:  # check player hp
    display_grid()
    print(f"Alas, {player_name} was defeated by the enemy!")  # Use player's name
    print("Game Over!")
elif not enemy_defeated or not enemy2_defeated:
    display_grid()
    print(f"Alas, {player_name} you were unable to defeat both enemies")
    print("Game Over!")
