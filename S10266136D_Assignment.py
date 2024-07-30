# Daksh Thapar - CSF03

"""
About the code:

All advanced features have been implemented!
 
Bonus Features:
    1) Added a high score system that saves the top 5 scores to a file
    2) Randomized crop prices after each day
    3) Bag can only hold 10 seeds in total
 
# Explaining additional functions:
    type()           -  This function returns the type of the specified object.
                        I used this function to check the type of the object.
    sum()            -  This function returns the sum of all the items in an iterable.
                        I used this function to calculate the total number of seeds in the bag.
    random.randint() -  This function returns a random integer between the specified integers.
                        I used this function to randomize the crop prices after each day.
    exit()           -  This function terminates the program.
                        I used this function to exit the program.
"""

import random 

# Game variables
game_vars = {
    'day': 1,        # Tracks the current day
    'energy': 10,    # Tracks the player's energy
    'money': 20,     # Tracks the player's money
    'bag': {},       # Tracks the seeds in the player's bag
}

# List of seed types available in the game
seed_list = ['LET', 'POT', 'CAU']

# Information about each seed type
seeds = {
    'LET': {'name': 'Lettuce',
            'price': 2,
            'growth_time': 2,
            'crop_price': 3,
            'crop_price_range': (3, 5)
            },

    'POT': {'name': 'Potato',
            'price': 3,
            'growth_time': 3,
            'crop_price': 6,
            'crop_price_range': (6, 8)
            },

    'CAU': {'name': 'Cauliflower',
            'price': 5,
            'growth_time': 6,
            'crop_price': 14,
            'crop_price_range': (12, 16)
            },
}

# Farm layout, a 5x5 grid where the player starts at (2,2) at the House
farm = [ [None, None, None, None, None],
         [None, None, None, None, None],
         [None, None, 'House', None, None],
         [None, None, None, None, None],
         [None, None, None, None, None] ]

#-----------------------------------------------------------------------
# display_town_options(game_vars)
#
#    Shows the menu of Albatross Town and returns the player's choice
#    Players can:
#      1) Visit the shop to buy seeds
#      2) Visit the farm to plant seeds and harvest crops
#      3) End the day, resetting Energy to 10 and allowing crops to grow
#      9) Save the game to file
#      0) Exit the game (without saving)
#-----------------------------------------------------------------------
def display_town_options(game_vars):

    show_stats(game_vars)  # Display current game statistics
   
    print("You are in Albatross Town")
    print("-------------------------")
    print("1) Visit Shop")
    print("2) Visit Farm")
    print("3) End Day")
    print("")
    print("9) Save Game")
    print("0) Exit Game")
    print("-------------------------")
    
#----------------------------------------------------------------------
# validate_choice(userinput, valid_choices):
#
#    Checks if the user's input is in the list of valid choices
#    Returns True if it is, False otherwise
#----------------------------------------------------------------------
def validate_choice(userinput, valid_choices):
    for choice in valid_choices:
        if userinput == choice:
            return True
    return False

#----------------------------------------------------------------------
# in_shop(game_vars)
#
#    Shows the menu of the seed shop, and allows players to buy seeds
#    Seeds can be bought if the player has enough money
#    Ends when the player selects to leave the shop
#----------------------------------------------------------------------
def in_shop(game_vars):
   
    print("Welcome to Pierce's Seed Shop!")
    
    while True:
        show_stats(game_vars)  # Display current game statistics
        
        print("What do you wish to buy?")
        
        print(f"{'Seed':<17}{'Price':^5}{'Days to Grow':^18}{'Crop Price':^11}")
        print(f"--------------------------------------------------")
        for index in range(len(seed_list)):
            seed_name = f" {index+1}) {seeds[seed_list[index]]['name']}"
            seed = seed_list[index]
            print(f"{seed_name:<17} {seeds[seed]['price']:^4}{seeds[seed]['growth_time']:^18} {seeds[seed]['crop_price']:^10}")
        print("\n 0) Leave")
        print("--------------------------------------------------")
        
        choice = input("Your choice? ")
        if validate_choice(choice, [str(i) for i in range(len(seed_list)+1)]):
            choice = int(choice)
        else:
            print("Invalid choice! Please choose a valid option.")
            continue
        
        if choice == 0:
            break
        else:
            print(f"You have ${game_vars['money']}")
            quantity = input("How many do you wish to buy? ")
            if not quantity.isdigit():
                print("Invalid input! Please enter a valid number.")
                continue
            quantity = int(quantity)
            if buy_seed(game_vars, seed_list[choice-1], quantity):
                # Purchase successful, go back to shop menu
                continue
            else:
                # Purchase failed
                continue
            
    
#-----------------------------------------------------------------------
# buy_seed(game_vars, seed, quantity)
#    Handles the purchase of seeds
#    Returns True if the purchase is successful, False otherwise
#    If the player can't afford the seeds, or the quantity is invalid,
#    the purchase fails
#-----------------------------------------------------------------------
def buy_seed(game_vars, seed, quantity):
    if game_vars['money'] < seeds[seed]['price'] * quantity:
        print("You can't afford that!")
        return False
    elif quantity <= 0:
        print("Invalid quantity! Please enter a positive number.")
        return False
    else:
        # if the bag contains 10 seeds in total, the player can't buy more
        if sum(game_vars['bag'].values()) + quantity > 10:
            print("You can't carry that many seeds!")
            return False
        
        game_vars['money'] -= seeds[seed]['price'] * quantity
        if seed in game_vars['bag']:
            game_vars['bag'][seed] += quantity
        else:
            game_vars['bag'][seed] = quantity
        print(f"You bought {quantity} {seeds[seed]['name']} seeds.")
        return True
        

#----------------------------------------------------------------------
# draw_farm(farm, farmer_row, farmer_col)
#
#    Draws the farm
#    Each space on the farm has 3 rows:
#      TOP ROW:
#        - If a seed is planted there, shows the crop's abbreviation
#        - If it is the house at (2,2), shows 'HSE'
#        - Blank otherwise
#      MIDDLE ROW:
#        - If the player is there, shows X
#        - Blank otherwise
#      BOTTOM ROW:
#        - If a seed is planted there, shows the number of turns before
#          it can be harvested
#        - Blank otherwise
#----------------------------------------------------------------------
def draw_farm(farm, farmer_row, farmer_col):
    rows, cols = len(farm), len(farm[0])
    farm_str = ""
    for row in range(rows):
        # Top border of the farm
        for col in range(cols):
            farm_str += "+-----" # Basically (+----- * cols)
        farm_str += "+\n|"
        
        # House / Plant / Empty space
        for col in range(cols):
            if farm[row][col] == 'House':
                farm_str += "HSE".center(5)
            # I used type() to check if the object is a list as if it is a list, it means that a seed is planted there
            elif farm[row][col] and type(farm[row][col]) == list: 
                farm_str += farm[row][col][0].center(5)
            else:
                farm_str += " ".center(5)
            farm_str += "|" # End of the cell
        farm_str += "\n|" # start of the next row
        
        # Person / Empty space
        for col in range(cols):
            if row == farmer_row and col == farmer_col:
                farm_str += "X".center(5) # Player
            else:
                farm_str += " ".center(5) # Empty space
            farm_str += "|" # End of the cell
        farm_str += "\n|" # start of the next row
        
        # Growth time / Empty space
        for col in range(cols):
            # same as the first row, I used type() to check if the object is a list as if it is a list, it means that a seed is planted there
            if farm[row][col] and type(farm[row][col]) == list:
                farm_str += str(farm[row][col][1]).center(5)
            else:
                farm_str += " ".center(5)
            farm_str += "|"
        farm_str += "\n"
        
    # Bottom border of the farm
    for col in range(cols):
        farm_str += "+-----" # Basically (+----- * cols)
    print(farm_str)

    

#----------------------------------------------------------------------
# in_farm(game_vars, farm)
#
#    Handles the actions on the farm. Player starts at (2,2), at the
#      farmhouse.
#
#    Possible actions:
#    W, A, S, D - Moves the player
#      - Will show error message if attempting to move off the edge
#      - If move is successful, Energy is reduced by 1
#
#    P - Plant a crop
#      - Option will only appear if on an empty space
#      - Shows error message if there are no seeds in the bag
#      - If successful, Energy is reduced by 1
#
#    H - Harvests a crop
#      - Option will only appear if crop can be harvested, i.e., turns
#        left to grow is 0
#      - Option shows the money gained after harvesting
#      - If successful, Energy is reduced by 1
#
#    R - Return to town
#      - Does not cost energy
#----------------------------------------------------------------------
def in_farm(game_vars, farm):
    # Player starts at (2,2)
    farmer_row, farmer_col = 2, 2
    
    # makes the code more readable
    energy = game_vars['energy']
    seed_bag = game_vars['bag']
    money = game_vars['money']

    # This function prints the farm, energy, and possible actions
    def print_status(plant=False, harvest=False):
        draw_farm(farm, farmer_row, farmer_col)
        print(f"Energy: {energy}")
        print("[WASD] Move")
        if plant:
            print("P)lant seed")
        if harvest:
            print(f"H)arvest {seeds[farm[farmer_row][farmer_col][0]]['name']}")
        print("R)eturn to Town")

    while True:
        # Check if player is at the house
        is_empty_space = farm[farmer_row][farmer_col] is None
        
        # Check if player can plant
        can_plant = is_empty_space and any(seed_bag.values())
        
        # Check if player can harvest
        # I used type() to check if the object is a list as if it is a list, it means that a seed is planted there
        can_harvest = farm[farmer_row][farmer_col] and type(farm[farmer_row][farmer_col]) == list and farm[farmer_row][farmer_col][1] == 0
        
        # Print the status of the farm
        print_status(plant=can_plant, harvest=can_harvest)
        action = input("Your choice? ").strip().upper()
        
        validate_choice_list = ['W', 'A', 'S', 'D', 'R']
        if can_plant:
            validate_choice_list.append('P')
        if can_harvest:
            validate_choice_list.append('H')
            
        if not validate_choice(action, validate_choice_list):
            print("Invalid choice!")
        elif action == 'R':
            print("Returning to town...")
            break    
        
        elif energy <= 0:
            print("You’re too tired. You should get back to town.")
            continue
        
        elif action == 'W' and farmer_row > 0:
                farmer_row -= 1
                energy -= 1
                
        elif action == 'A' and farmer_col > 0:
                farmer_col -= 1
                energy -= 1
                
        elif action == 'S' and  farmer_row < len(farm) - 1:
                farmer_row += 1
                energy -= 1
                
        elif action == 'D' and farmer_col < len(farm[0]) - 1:
                farmer_col += 1
                energy -= 1
                
        elif action == 'P' and can_plant:
            while True:
                print("What do you wish to plant?")
                print(f"-----------------------------------------------------")
                print(f"    Seed              Days to Grow  Crop Price  Available")
                print(f"-----------------------------------------------------")
                available_seeds = [seed for seed, qty in seed_bag.items() if qty > 0]
                for index, seed in enumerate(available_seeds, 1):
                    seed_info = seeds[seed]
                    print(f" {index}) {seed_info['name']:<21}{seed_info['growth_time']:<13}{seed_info['crop_price']:<10}{seed_bag[seed]:^4}")
                print("\n 0) Leave")
                print("-----------------------------------------------------")
                seed_choice = input("Your choice? ").strip()
                
                if seed_choice.isdigit():
                    seed_choice = int(seed_choice)
                    if seed_choice == 0:
                        print("Leaving planting menu.")
                        break
                    elif 1 <= seed_choice <= len(available_seeds):
                        selected_seed = available_seeds[seed_choice - 1]
                        farm[farmer_row][farmer_col] = [selected_seed, seeds[selected_seed]['growth_time']]
                        seed_bag[selected_seed] -= 1
                        energy -= 1
                        if seed_bag[selected_seed] == 0:
                            del seed_bag[selected_seed]
                        break
                        # print(f"Planted {seeds[selected_seed]['name']}!")
                    else:
                        print("Invalid choice!")
                        continue
                else:
                    print("Invalid input!")
                    continue
                
        elif action == 'H' and can_harvest:
            seed_choice, _ = farm[farmer_row][farmer_col]
            money_gained = seeds[seed_choice]['crop_price']
            money += money_gained
            farm[farmer_row][farmer_col] = None
            energy -= 1
            print(f"You harvest the {seeds[seed_choice]['name']} and sold it for ${money_gained}!")
            print(f"You now have ${money}!")
        else:
            print("Cannot move off the edge of the farm!")


    game_vars['energy'] = energy
    game_vars['bag'] = seed_bag
    game_vars['money'] = money

    
#----------------------------------------------------------------------
# show_stats(game_vars)
#
#    Displays the following statistics:
#      - Day
#      - Energy
#      - Money
#      - Contents of Seed Bag
#----------------------------------------------------------------------
def show_stats(game_vars):
    print("+--------------------------------------------------+")
    print(f"| Day {game_vars['day']:<11} Energy: {game_vars['energy']:<11} Money: ${game_vars['money']:<4} |")
    if len(game_vars['bag']) == 0:
        print(f"| {'You have no seeds.':<49}|")
    else:
        print(f"| Your seeds: {'':<37}|")
        for seed in game_vars['bag']:
            if game_vars['bag'][seed] == 0:
                continue
            front = f"|   {seeds[seed]['name']}: "
            print(f"{front:<20}{game_vars['bag'][seed]:<31}|")
    print("+--------------------------------------------------+")

#----------------------------------------------------------------------
# end_day(game_vars)
#
#    Ends the day
#      - The day number increases by 1
#      - Energy is reset to 10
#      - Every planted crop has their growth time reduced by 1, to a
#        minimum of 0
#----------------------------------------------------------------------
def end_day(game_vars):
    game_vars['day'] += 1
    game_vars['energy'] = 10
    
    # Reduce growth time of crops by 1
    # Go through each cell in the farm
    # If the cell contains a list, reduce the growth time by 1
    for r in range(len(farm)):
        for c in range(len(farm[0])):
            if farm[r][c] and type(farm[r][c]) == list:
                farm[r][c] = [farm[r][c][0], max(0, farm[r][c][1] - 1)]
    
    # Randomize crop prices after each day
    for seed in seed_list:
        lower_bound, upper_bound = seeds[seed]['crop_price_range']
        new_price = random.randint(lower_bound, upper_bound)
        seeds[seed]['crop_price'] = new_price

            
    if game_vars['day'] > 20:
        print(f"You have ${game_vars['money']} after 20 days.")
        if game_vars['money'] >= 100:
            print(f"You paid off your debt of $100 and made a profit of ${game_vars['money'] - 100}")
            print("You win!")
            while True:
                name = input("Enter your name: ")
                if ":" in name:
                    print("Invalid name! Please enter a name without a colon.")
                    continue
                else:
                    save_highscore_top_5(name, game_vars['money'] - 100)
                    print("High Scores:")
                    scores = load_highscores()
                    for i, score in enumerate(scores, 1):
                        print(f"{i}. {score[0]}: ${score[1]}")
                    print("----------------------------------------------------------")
                    print("Thank you for playing Sundrop Farm!")
                    exit()
        else:
            print(f"You did not pay off your debt. You lose :(")
            exit()
    else:
        # Continue the game
        print("It's a new day! Crop prices have been updated.")

#----------------------------------------------------------------------
# save_highscore_top_5(name, profit)
#
#    Saves the top 5 high scores to the file "highscores.txt"
#    If the file does not exist, it is created
#    If there are less than 5 scores, the new score is added
#    If there are 5 scores, the lowest score is replaced 
#----------------------------------------------------------------------
def save_highscore_top_5(name, profit):
    def get_profit(score):
        return int(score[1])
    
    with open("highscores.txt", "r") as f:
        scores = [line.strip().split(" ") for line in f]
    scores.append([name, profit])
    scores.sort(key=get_profit, reverse=True)
    
    with open("highscores.txt", "w") as f:
        for i in range(min(5, len(scores))):
            f.write(f"{scores[i][0]} {scores[i][1]}\n")

#----------------------------------------------------------------------
# load_highscores()
#
#     Loads the high scores from the file "highscores.txt"
#     If the file does not exist, it is created
#     Returns a list of the high scores 
#----------------------------------------------------------------------
def load_highscores():
    with open("highscores.txt", "a") as f:
        pass
    with open("highscores.txt", "r") as f:
        scores = [line.strip().split(" ") for line in f]
    if not scores:
        return []
    return scores

#----------------------------------------------------------------------
# save_game(game_vars, farm)
#
#    Saves the game into the file "savegame.txt"
#----------------------------------------------------------------------
def save_game(game_vars, farm):
    with open("savegame.txt", "w") as f:
        f.write(f"Money *:* {game_vars['money']}\n")
        f.write(f"Energy *:* {game_vars['energy']}\n")
        f.write(f"Day *:* {game_vars['day']}\n")
        bag_items = ",".join([f"{key}:{value}" for key, value in game_vars['bag'].items()])
        f.write(f"Bag *:* {bag_items}\n")
        seed_prices = ",".join([f"{seed}:{seeds[seed]['crop_price']}" for seed in seed_list])
        f.write(f"Seed Prices *:* {seed_prices}\n")
        farm_data = ""
        for row in farm:
            for col in row:
                if col is None:
                    farm_data += "None,"
                elif col == 'House':
                    farm_data += "House,"
                elif type(col) == list:
                    farm_data += f"{col[0]}:{col[1]},"
                else:
                    farm_data += col
            farm_data = farm_data[:-1]
            farm_data += "|"
        f.write(f"Farm *:* {farm_data}\n")
        

#----------------------------------------------------------------------
# load_game(game_vars, farm)
#
#    Loads the saved game by reading the file "savegame.txt"
#----------------------------------------------------------------------
def load_game(game_vars, farm):
    # Check if file exists
    with open("savegame.txt", "a") as f:
        pass
    with open("savegame.txt", "r") as f:
        # Read the file line by line
        # ALL values are "key *:* value"
        # For example, "Money *:* 20"
        # Farm is a 5x5 grid, each cell is separated by a comma
        
        lines = f.readlines()
        if lines == []:
            print("No saved game found.")
            return game_vars, farm
        for line in lines:
            if line.startswith("Money"):
                game_vars['money'] = int(line.split("*:*")[1])
            elif line.startswith("Energy"):
                game_vars['energy'] = int(line.split("*:*")[1])
            elif line.startswith("Day"):
                game_vars['day'] = int(line.split("*:*")[1])
            elif line.startswith("Bag"):
                bag_items = line.split("*:*")[1].strip().split(",")
                for item in bag_items:
                    values = item.split(":")
                    if len(values) == 1:
                        continue
                    key, value = values
                    game_vars['bag'][key] = int(value)
            elif line.startswith("Seed Prices"):
                seed_prices = line.split("*:*")[1].strip().split(",")
                for seed_price in seed_prices:
                    seed, price = seed_price.split(":")
                    seeds[seed]['crop_price'] = int(price)
            elif line.startswith("Farm"):
                farm_data = line.split("*:*")[1].strip().split("|")
                for row in range(len(farm_data)):
                    col = farm_data[row].split(",")
                    col.pop(-1)
                    for c in range(len(col)):
                        if col[c] == 'None':
                            farm[row][c] = None
                        elif col[c] == 'House':
                            farm[row][c] = 'House'
                        else:
                            seed, growth_time = col[c].split(":")
                            farm[row][c] = [seed, int(growth_time)]
    return game_vars, farm
        

#----------------------------------------------------------------------
#    Main Game Loop
#----------------------------------------------------------------------
def game():
    while True:
        display_town_options(game_vars)
        choice = input("Your choice? ")
        if not validate_choice(choice, ['1', '2', '3', '9', '0']):
            print("Invalid choice. Please choose a valid option.")
            continue
        
        choice = int(choice)
        
        if choice == 1:
            in_shop(game_vars)
                
        elif choice == 2:
            in_farm(game_vars, farm)
        elif choice == 3:
            end_day(game_vars)
        elif choice == 9:
            save_game(game_vars, farm)
        elif choice == 0:
            print("Goodbye!")
            exit()
    
print("----------------------------------------------------------")
print("Welcome to Sundrop Farm!")
print()
print("You took out a loan to buy a small farm in Albatross Town.")
print("You have 20 days to pay off your debt of $100.")
print("You might even be able to make a little profit.")
print("How successful will you be?")
print("----------------------------------------------------------")

while True:
    print("""1) Start a new game
2) Show High Scores
3) Load your saved game

0) Exit Game""")

    choice = input("Your choice? ")

    if validate_choice(choice, ['1', '2', '3', '0']):
        choice = int(choice)
    else:
        print("Invalid choice. Please choose a valid option.\n")
        continue

    if choice == 1:
        game()
    elif choice == 2:
        scores = load_highscores()
        if not scores:
            print("No high scores found.")
        else:
            print("High Scores:")
            for i, score in enumerate(scores, 1):
                print(f"{i}. {score[0]}: ${score[1]}")
    elif choice == 3:
        game_vars, farm = load_game(game_vars, farm)
        game()
    elif choice == 0:
        print("Goodbye!")
        exit()