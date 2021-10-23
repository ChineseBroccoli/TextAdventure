# commands.py
# This is where most of the action happens.
import os
import sys

import gamestate
import rooms

# This system defines a bunch of commands, which are integrated with main.py with the command_list at the bottom.
# Since 'words' involves a list such as ['move','north'], with the name of the command intact, most commands deal with the argument words[1] or words[2]

def info(words):
    # If there is no argument for the command
    if len(words) == 1:
        return print("ERROR: No entity targeted!")

    # for 'info location', prints the name, description, and paths. Note that this does NOT display hidden paths.
    if words[1] == "location":
        currentRoom = rooms.rooms[gamestate.current_room_id]

        print("INFO (LOCATION)")
        print("Name: " + currentRoom["name"])
        print("Description: " + currentRoom["desc"])
        print("Path: ")
        for direction, room_id in currentRoom["path"].items():
            # THIS MAY BE A POSSIBLE ERROR
            print("-" + direction.capitalize() + ": " + rooms.rooms[room_id]["name"])
        return

    return print("ERROR: target entity does not exist!")

def move(words):
    # sets currentRoom from gamestate
    currentRoom = rooms.rooms[gamestate.current_room_id]
    
    # If there is no argument for the command
    if len(words) == 1:
        return print("ERROR: No direction targeted!")

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
            return print("Player moved to " + rooms.rooms[room_id]["name"] + "!")
    
    return print("ERROR: Direction does not exist!")

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
        return print("You tried to say so much stuff, b")

    if words[1] in sayable_words:
        # prints whatever the dictionarys says to
        return print(sayable_words[words[1]])
    
    return print("You tried to speak, but the stuff you said was so stupid that the sound of the monsters banging their heads against the wall in agony drowned it out.")

sayable_words = {
    "gerald": "A faint groan emanates from within the walls, and the already dank atmosphere thickens.",
    "yo": "A mannequin wheels on by on a toy bicycle. She looks at you with a grin, and with three flicks of her wrist hits you squarely in the face, briefly stunning you. By the time you look back the room is empty again.",
}

# list of every command; this is how integration with main.py occurs.
command_list = {
    "info": info,
    "move": move,
    "clear": clear,
    "quit": exit,
    "exit": exit,
    "say": say,
}