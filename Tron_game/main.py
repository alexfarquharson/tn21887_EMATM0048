# Alexander Farquharson, TRON GAME, script for setting up game and managing the run of the game


########
# Import game classes
########

from tron_classes import Player
from tron_classes import Human
from tron_classes import Computer
from tron_classes import Board



########
# Define functions to set up game
########

def setup():
    '''
    Function to initiate setup
        gets human input: either continues setup, repeats or ends
    '''
    global begin
    begin = [input("Would you like to play Tron? (y/n)").lower()]
    begin_dict = {'y':None,'n':None}
    try:
        list(map(lambda x: begin_dict[x],begin))[0]
        if begin == ['n']:
            print('Have a nice day')
        else:
            print('##############################')
            game_type_qu()
    except KeyError:
        print('Invalid option: (type y or n)')
        setup()
        

def game_type_qu():
    '''
    Function to get game_type 
        gets human input: either continues setup, repeats or ends
    '''
        
    global game_type_input
    game_type_input = input('What game version would you like to play?: \n a. Consecutive turns? \n b. Simultaneous turns? \n (Choose a or b) \n').lower()
    game_type_dict = {'a':'consecutive','b':'simultaneous'}
    try:
        game_type_input = list(map(lambda x: game_type_dict[x],game_type_input))[0]
        print('##############################')
        player_type_qu()
    except:
        print('Invalid option: (type a or b)')
        game_type_qu()
        

def player_type_qu():
    '''
    Function to get player_type
        gets human input: either continues setup, repeats or ends
    '''
        
    global player_type_input
    player_type_input = input('Who do you want to play?: \n a. PVP? \n b. PVC (easy)? \n c. PVC (hard)? \n (Choose a, b or c) \n').lower()
    player_type_dict = {'a':'PVP','b':'PVC (easy)', 'c': 'PVC (hard)'}
    try:
        player_type_input = list(map(lambda x: player_type_dict[x],player_type_input))[0]
        print('##############################')
        dimension_qu()
    except:
        print('Invalid option: (type a, b or c)')
        player_type_qu()
        
        
def dimension_qu():
    '''
    Function to get board dimension
        gets human input: either continues setup, repeats or ends
    '''
        
    global dimension_input
    while True:
        try:
            dimension_input = int(input('Please insert board size (minimum 4).'))
            if dimension_input >= 4:
                print('##############################')
                break
            else:
                print("(Board size minimum is 4)")
        except:
            print("I didn't quite get that, please input a number")

            
def play_again_qu(game):
    '''
    Function to play again
        gets human input: either plays game again, changes setup, repeats or ends
    '''
        
    play_again = [input('Would you like to play again? \n a. Yes (same setup) \n b. Yes (change setup) \n c. No \n (Type a, b or c):').lower()]
    play_again_dict = {'a':None,'b':None, 'c':None}
    try:
        list(map(lambda x: play_again_dict[x],play_again))[0]
        if play_again == ['a']:
            play_game(game)
        elif play_again == ['b']:
            print('##############################')
            game_type_qu()
            game = initialise_game(dimension_input, player_type_input, game_type_input)
            play_game(game)
        else:
            print('Thanks for playing')
            
    except KeyError:
        print('Invalid option: (type a,b or c)')
        play_again_qu(game)


def initialise_game(dimension_input, player_type_input, game_type_input):
    '''
    Function to initiate game class
    Inputs:
        dimension_input: int
        player_type_input: str
        game_type_input: str
    Outputs:
        game: Board object
    '''
        
#     initialise game
    game = Board(dimension = dimension_input, player_type = player_type_input, game_type = game_type_input)
    return game

def play_game(game):
    '''
    Function to play game
    '''
    
    game.play()
    play_again_qu(game)
    
    
    
    
########
# Running game script
########

if __name__ == '__main__':
    
#     run setup
    setup()
    
#     create game instance
    if begin == ["y"]:
        print('\n ############################## \n Creating game...')
        game = initialise_game(dimension_input, player_type_input, game_type_input)

    #     play game code
        play_game(game)

