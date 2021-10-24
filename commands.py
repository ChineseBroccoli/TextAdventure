# commands.py
# This is where most of the action happens.
import os
import sys

import gamestate
import rooms

from constants import divider

# This system defines a bunch of commands, which are integrated with main.py with the command_list at the bottom.
# Since 'words' involves a list such as ['move','north'], with the name of the command intact, most commands deal with the argument words[1] or words[2]

def look(words):
    # Prints info about the room. This command can be extended to refer to items too. 
    currentRoom = gamestate.get_current_room()
    print("INFO (LOCATION)")
    print("Name: " + currentRoom["name"])
    print("Description: " + currentRoom["desc"])
    print("Path: ")
    # lists every single possible (non-hidden) path
    for direction, room_id in currentRoom["path"].items():
        print("-" + direction.capitalize() + ": " + rooms.rooms[room_id]["name"])
    # lists all enemies, if there are any.
    if "enemies" in gamestate.get_current_room():
        print("Enemies: ")
        for enemy in gamestate.get_current_room()["enemies"]:
            print("-" + enemy["name"] + " | HP:" + "(" + str(enemy["hp"]) + "/" + str(enemy["maxhp"]) + ")" + " ATK:" + str(enemy["atk"]))
    # lists any present items, if there are any.
    if "items" in gamestate.get_current_room():
        print("Items: ")
        for item in gamestate.get_current_room()["items"]:
            print("-" + item["name"])
    return

# used by 'info' to save space. prints all information about an item.
def print_item_info(index, item):
    print(item["name"] + " (" + str(index) + "/" + str(gamestate.player["invspace"]) + "): ")
    print("-Description: " + str(item["desc"]))
    if "equipable" in item:
        print("-Equipable: True")
        print("-Attack: " + str(item["atk"]))

def info(words):
    # for 'info location', prints the name, description, and paths. Note that this does NOT display hidden paths.
    if words[1] == "location": 
        return look(words)
    
    # shows information about the player (HP, inventory, attack power, etc.), when 'info player' is typed.
    if words[1] == "player":
        print("INFO (PLAYER)")
        print("Name: " + gamestate.player["name"])
        print("HP: " + "(" + str(gamestate.player["hp"]) + "/" + str(gamestate.player["maxhp"]) + ")")
        print("ATK: " + str(gamestate.player["atk"]))
        # shows your equipped weapon
        if (not gamestate.player["equipped"] is None):
            print("Equipped: " + gamestate.player["equipped"]["name"])
        else:
            print("Equipped: None")
        # How many spaces of inventory you have used
        print("Inventory (" + str(len(gamestate.player["inv"])) + "/" + str(gamestate.player["invspace"]) + " slots used):")
        # lists nothing if there is nothing
        if len(gamestate.player["inv"]) == 0:
            print("*Empty! You poor person!*")
        else:
            # lists all items
            for item in gamestate.player["inv"]:
                print("-" + item["name"])
        return
    
    # shows information about enemies.
    if words[1] == "enemies":
        if not (len(gamestate.get_current_room()["enemies"]) == 0):
            print("INFO (ENEMIES)")
            for enemy in gamestate.get_current_room()["enemies"]:
                print(enemy["name"] + ":")
                print("-Description: " + str(enemy["desc"]))
                print("-Health: " + str(enemy["hp"]) + "/" + str(enemy["maxhp"]))
                print("-Attack: " + str(enemy["atk"]))
            return
        else:
            return print ("There are no enemies to show information for!")

    # Shows indepth info about inventory.
    if words[1] == "inventory":   
        # if inventory empty
        if len(gamestate.player["inv"]) == 0:
            return print("Your inventory is empty! You poor person!")
        # prints info about inventory (for 'info inventory')
        if len(words) == 2:
            print("INFO (INVENTORY)")
            for index, item in enumerate(gamestate.player["inv"]):
                print_item_info(index, item)
            return
        # prints info about item in inventory (for 'info inventory stick')
        if len(words) == 3:
            for index, item in enumerate(gamestate.player["inv"]):
                if (words[2] == item["name"].lower()):
                    print("INFO (INVENTORY)")
                    return print_item_info(index, item)
            return print("No item with that name in your inventory!")
    
    # shows info about item equipped.
    if words[1] == "equipped":
        if gamestate.player["equipped"] == None:
            return print("You do not have an item equipped!")
        index = gamestate.player["inv"].index(gamestate.player["equipped"])
        return print_item_info(index, gamestate.player["equipped"])
            
    #ERROR
    return print("You looked around, but couldn't see what you were looking for.")

def move(words):
    # sets currentRoom from gamestate
    currentRoom = gamestate.get_current_room()
    
    # If there is no argument for the command
    if len(words) == 1:
        #ERROR
        return print("You tried to move, but since you couldn't decide which direction to go, you hummed a few bars to yourself and planted yourself exactly where you started.")

    # copies the list of all possible paths from the rooms.py dictionary
    all_paths = currentRoom["path"].copy()
    if "hiddenpath" in currentRoom:
        #adds hidden paths to the list if they exist.
        all_paths.update(currentRoom["hiddenpath"])
    
    # loops through, checks to see if there are any paths that go in the direction typed.
    for direction, room_id in all_paths.items():
        if words[1] == direction:
            # changes gamestate to the new room.
            gamestate.current_room_id = room_id

            print("Player moved to " + rooms.rooms[room_id]["name"] + "!")
            print(divider)
            look(words)

            if "enemies" in gamestate.get_current_room():
                # initiates combat
                print(divider)
                print("Enemies spotted! You must either fight or flight!")
                gamestate.current_action = "fighting"
            elif gamestate.current_action == "fighting" and not ("enemies" in gamestate.get_current_room()):
                # if you change a room when you were meant to be fighting, implies you fled, and resets back to exploring mode.
                print(divider)
                print("Player successfully ran away! What a coward!")
                gamestate.current_action = "exploring"

            return 
    
    #ERROR
    return print("You tried to go that way, but you rammed into something and got a splinter instead.")

# clears all text; may not work on all platforms
def clear(words):
    os.system('cls' if os.name == 'nt' else 'clear')

# exits the game
def exit(words):
    sys.exit()

# You can say stuff now. Good luck figuring out what you can actually say.
def say(words):
    # if there is no argument
    if len(words) == 1:
        # TO-DO: Add "silence descriptors" to rooms.py, replacing 'faint creaking'.
        return print("You open your mouth, but silence fills the air. Only a faint creaking is audible.")

    if len(words) > 2:
        return print("You tried to speak, but you said so much that it came out as a garbled mess. A toilet flushes in the distance.")

    if words[1] in sayable_words:
        # prints whatever the dictionarys says to
        return print(sayable_words[words[1]])
    
    #ERROR
    return print("You tried to speak, but the stuff you said was so stupid that the sound of the monsters banging their heads against the wall in agony drowned it out.")

sayable_words = {
    "gerald": "A faint groan emanates from within the walls, and the already dank atmosphere thickens.",
    "yo": "A mannequin wheels on by on a toy bicycle. She looks at you with a grin, and with three flicks of her wrist hits you squarely in the face with a yo-yo, briefly stunning you. By the time you look back the room is empty again.",
}

def attack(words):
    if len(words) == 1:
        #ERROR
        return print("You tried to swing at nothing, and ended up making a fool of yourself. Try again.")

    if not "enemies" in gamestate.get_current_room():
        #ERROR
        return print("You charge aggressively at the enemy, before realising that the room is completely empty. There are no enemies here...")

    # loops through each enemy in room
    for enemy in gamestate.get_current_room()["enemies"]:
        # if argument matches an enemy
        if words[1] == enemy["name"].lower():
            # gives damage equal to player's base attack.
            damage = gamestate.player["atk"]
            # adds weapon damage if it is equipped
            if (not gamestate.player["equipped"] is None):
                damage += gamestate.player["equipped"]["atk"]
            # gives damage.
            print("Player deals: " + str(damage) + " to " + enemy["name"] + "!")
            enemy["hp"] -= damage
            if enemy["hp"] <= 0:
                gamestate.get_current_room()["enemies"].remove(enemy)
                print(divider)
                print(enemy["name"] + " dies!")
            break
    
    # if no enemies, shows text to player telling them that they've cleared everything.
    if (len(gamestate.get_current_room()["enemies"]) == 0):
        del gamestate.get_current_room()["enemies"]
        gamestate.current_action = "exploring"
        print(divider)
        print("You defeated all the enemies!")

#regains hp
def rest(words):
    #only works in 'rest' rooms
    if "rest" in gamestate.get_current_room():
        gamestate.player["hp"] = gamestate.player["maxhp"]
        return print("Player rests and heals wounds")
    else:
        return print("ERROR: You can't rest you lazy bum! (Find a room you can rest in!)")

#pickup item from room
def pickup(words):
    #if no argument
    if len(words) == 1:
        return print("ERROR: No item targeted!")
    # if no items in room
    if not "items" in gamestate.get_current_room():
        return print("ERROR: No items to pick up!")
    
    # loops through all items in rooms
    for item in gamestate.get_current_room()["items"]:
        # if it matches
        if words[1] == item["name"].lower():
            # checks inventory space; if inventory space is reached, doesn't work.
            if len(gamestate.player["inv"]) == gamestate.player["invspace"]:
                return print("ERROR: Not enough inventory space!")
            # adds item if everything else clears.
            else:
                # adds to inventory list
                gamestate.player["inv"].append(item)
                # removes from the room
                gamestate.get_current_room()["items"].remove(item)
                print("Player picks up: " + item["name"])
                # if no items in room, shows that there are none left.
                if (len(gamestate.get_current_room()["items"]) == 0):
                    del gamestate.get_current_room()["items"]
                    print(divider)
                    print("Player picked up all the items in the area!")
                return

    return print("No item with that name to pickup!")

# equips the weapon from inventory
def equip(words):
    # if there ain't no argument
    if len(words) == 1:
        return print("ERROR: No item targeted!")
    # if there ain't nothing in inventory to equip
    if len(gamestate.player["inv"]) == 0:
        return print("ERROR: No item to equip! Inventory is empty!")

    #loops through each item
    for item in gamestate.player["inv"]:
        # if item is found
        if words[1] == item["name"].lower():
            if not "equipable" in item:
                return print("ERROR: This item is not equipable!")
            else:
                # equips the item.
                gamestate.player["equipped"] = item
                return print("Player equiped: " + item["name"])
    
    return print("ERROR: Item does not exist.")

# I tried automating it but it didn't work. Just update it if you update command_list please :)
def help(words):
    print("COMMANDS:")
    print("Info: Prints info about stuff. Aliases: look")
    print("Move: Moves in a direction. Aliases: go, walk, climb")
    print("Clear: Clears screen (only works in console). Aliases: cls")
    print("Exit: Quits game. Aliases: quit")
    print("Say: Say something. Aliases: speak")
    print("Attack: Attack something. Aliases: fight")
    print("Rest: Rest for a while. Aliases: sleep")
    print("Pickup: Pick an item up. Aliases: take")
    print("Equip: Equip a weapon from inventory. Aliases: puton")
    return

# list of every command; this is how integration with main.py occurs.
command_list = {
    "info": info,
    "move": move,
    "clear": clear,
    "cls": clear,
    "quit": exit,
    "exit": exit,
    "say": say,
    # might seem contradictory but its so you can 'look item' or whatever.
    "look": info,
    "attack": attack,
    "rest": rest,
    "pickup": pickup,
    "equip": equip,
    "help": help,
    "go": move,
    "take": pickup,
    "walk": move,
    "climb": move,
    "speak": say,
    "fight": attack,
    "sleep": rest,
    "puton": equip,
}