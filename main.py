# main.py
import gamestate
import creatures
import commands
import rooms
from constants import divider

print("WELCOME TO...")
print("""  ▄████ ▓█████  ██▀███   ▄▄▄       ██▓    ▓█████▄   ██████      █████▒▒█████    ██████ ▄▄▄█████▓▓█████  ██▀███      ██░ ██  ▒█████   ███▄ ▄███▓▓█████ 
 ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒▒████▄    ▓██▒    ▒██▀ ██▌▒██    ▒    ▓██   ▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒   ▓██░ ██▒▒██▒  ██▒▓██▒▀█▀ ██▒▓█   ▀ 
▒██░▄▄▄░▒███   ▓██ ░▄█ ▒▒██  ▀█▄  ▒██░    ░██   █▌░ ▓██▄      ▒████ ░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒   ▒██▀▀██░▒██░  ██▒▓██    ▓██░▒███   
░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄  ░██▄▄▄▄██ ▒██░    ░▓█▄   ▌  ▒   ██▒   ░▓█▒  ░▒██   ██░  ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄     ░▓█ ░██ ▒██   ██░▒██    ▒██ ▒▓█  ▄ 
░▒▓███▀▒░▒████▒░██▓ ▒██▒ ▓█   ▓██▒░██████▒░▒████▓ ▒██████▒▒   ░▒█░   ░ ████▓▒░▒██████▒▒  ▒██▒ ░ ░▒████▒░██▓ ▒██▒   ░▓█▒░██▓░ ████▓▒░▒██▒   ░██▒░▒████▒
 ░▒   ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░▓  ░ ▒▒▓  ▒ ▒ ▒▓▒ ▒ ░    ▒ ░   ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░    ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░   ░  ░░░ ▒░ ░
  ░   ░  ░ ░  ░  ░▒ ░ ▒░  ▒   ▒▒ ░░ ░ ▒  ░ ░ ▒  ▒ ░ ░▒  ░ ░    ░       ░ ▒ ▒░ ░ ░▒  ░ ░    ░     ░ ░  ░  ░▒ ░ ▒░    ▒ ░▒░ ░  ░ ▒ ▒░ ░  ░      ░ ░ ░  ░
░ ░   ░    ░     ░░   ░   ░   ▒     ░ ░    ░ ░  ░ ░  ░  ░      ░ ░   ░ ░ ░ ▒  ░  ░  ░    ░         ░     ░░   ░     ░  ░░ ░░ ░ ░ ▒  ░      ░      ░   
      ░    ░  ░   ░           ░  ░    ░  ░   ░          ░                ░ ░        ░              ░  ░   ░         ░  ░  ░    ░ ░         ░      ░  ░""")

def start_game():
    gamestate.game_over = False
    gamestate.player = creatures.player.copy()
    gamestate.current_action = "exploring"
    gamestate.current_room_id = 0
    rooms.set_rooms()
    game_loop()

def game_loop():
    # This While Loop constantly loops until the game is marked as over (through player choice or deaths in game).
    # This takes the commands from the player, which are elaborated in in commands.py
    commands.command_list["look"](["look"])
    print(divider)
    
    while gamestate.game_over == False:
        command = input("type command: ")
        print(divider)
        #splits up the input into a list
        words = command.lower().split()       
        # if the command exists
        if words[0] in commands.command_list:
            # execute command(words), words being the whole list.
            commands.command_list[words[0]](words)
        else:
            print("ERROR: Invalid Command!")

        if (gamestate.current_action == "fighting"):
            print(divider)
            for enemy in gamestate.get_current_room()["enemies"]:
                oldhp = gamestate.player["hp"]
                gamestate.player["hp"] -= enemy["atk"]
                
                if gamestate.player["hp"] <= 0:
                    print("Enemy " + enemy["name"] + " deals: " + str(enemy["atk"]) + " HP! (" +  str(oldhp) + "/" + str(gamestate.player["maxhp"]) + " --> 0/" + str(gamestate.player["maxhp"]) + ")")
                    print(divider)
                    print("Game Over! Player sucked and died!")
                    gamestate.game_over = True
                    break
                else:
                    print("Enemy " + enemy["name"] + " deals: " + str(enemy["atk"]) + " HP! (" +  str(oldhp) + "/" + str(gamestate.player["maxhp"]) + " --> " + str(gamestate.player["hp"]) + "/" + str(gamestate.player["maxhp"]) + ")")


        print(divider)

start_game()       

while (gamestate.game_over == True):
    play_again = input("Do you want to play again? (y/n): ")
    if (play_again.lower() in ["y", "yes", "ye", "yeah"]):
        start_game()
    elif (play_again.lower() in ["n", "no", "nae", "nah"]):
        quit()
    else:
        print("ERROR: Invalid Command!")
        print(divider)