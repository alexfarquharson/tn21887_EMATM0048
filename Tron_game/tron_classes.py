# Alexander Farquharson, TRON GAME, script for creating the board and player classes for the Tron game


# import standard libraries
import random
import copy

########
# Player classes
########

class Player():
    '''
    Class to hold all attributes unique to the player
    '''
    
    def __init__(self, name, dimension):
        '''
        Function to initialise Player object:
        Inputs:
            name: str ('1' or '2')
            dimension: int
        '''
        
        assert name in ('1','2'), 'Player name must be either: 1 or 2'
        self.name = name
        self.dimension = dimension
        self.score = 0
        self.position = list(self.reset_position())
        
        
        
        
    def reset_position(self):
        '''
        Function to get player position
        Depends on player name and board dimension
        '''
        if self.name == "1":
            return (1, 1)
        else:
            return self.dimension, 2*self.dimension-1
        
        
        
class Human(Player):
    '''
    Player class child:
        Type set to human
        Additional keys related information
    '''
    
    def __init__(self, name, dimension, default_keys = True):
        '''
        Function to initialise Human object:
        Inputs:
            name: str ('1' or '2')
            dimension: int (>3)
        '''
        super().__init__(name, dimension)
        self.type = "Human"
        self.player_dictionary = self.player_dictionary_setup()       

        
    def player_dictionary_setup(self):
        '''
        Function to create move dictionary for the two players
        '''
        
        if self.name == "1":
            player_dictionary = {"w":'up', "a":'left', "s":'down', "d":'right'}

        else:
            player_dictionary = {"i":'up', "j":'left', "k":'down', "l":'right'}
            
        return player_dictionary
    
    def show_keys(self):
        '''
        Function to print instructions of the player
        '''
        
        print(f"\n Player {self.name} keyboard: ")
        for (key, value) in (self.player_dictionary.items()):
            print(f"{value}: {key}")
            
class Computer(Player):
    '''
    Player class chikld:
        Type set to computer.
        Additional difficulty input.
    '''
    
    def __init__(self, name, dimension, difficulty):
        '''
        Function to initialise Computer object:
        Inputs:
            name: str ('1' or '2')
            dimension: int (>3)
            difficulty: str ('easy','difficult')
        '''
        super().__init__(name, dimension)
        
        assert difficulty in ('easy', 'hard'), 'Computer Player difficulty must be either: easy or difficult'
        self.type = "Computer"
        self.difficulty = difficulty
        

########
# Board class
########

class Board():
    """
    The Board class
        Creates board
        Functionality to play consecutive or simultaneous game
        Creates computer player move input, or gets human player move input
        Functionality to move player given human or computer input
    """


        
        
        
    def __init__(self, dimension, game_type, player_type):
        '''
        Function to initialise the board object:
            Creates board, players
            
        Inputs:
            game_type: str ('consecutive' or 'simultaneous')
            player_type: str: ('PVP', 'PVC (easy)' or 'PVC (hard)')
            dimension: int (>3)
            
            '''
#         game configuration
        assert type(game_type) == str
        assert type(player_type) == str
        assert game_type in ('consecutive', 'simultaneous'), "game_type must be either: consecutive or simultaneous"
        assert player_type in ('PVP', 'PVC (easy)', 'PVC (hard)'), "game_type must be either: PVP, PVC (easy), PVC (hard)"
        self.game_type = game_type
        self.player_type = player_type
            
        assert type(dimension) == int, "Please input an integer for board size"
        assert dimension > 3, "Board size must be greater than 3"
        self.dimension = dimension
        
#         player 1 creation - must be human
        self.player1 = Human(name = '1', dimension = self.dimension)
        self.player1.show_keys()
#         player 2 creation - human, computer easy, computer hard
        if self.player_type == "PVP":
            self.player2 = Human(name = '2', dimension = self.dimension)
            self.player2.show_keys()
        elif self.player_type == "PVC (easy)":
            print('Computer is player 2 \n Difficulty: Easy')
            self.player2 = Computer(name = '2', dimension = self.dimension, difficulty = 'easy')  
        else:
            print('Computer is player 2 \n Difficulty: Hard')
            self.player2 = Computer(name = '2', dimension = self.dimension, difficulty = 'hard')  

#         create table
        self.table = self.create_board()
        
#         dictionaries used repeatedly across the whole class
        self.perform_move_dict = {"up":self.perform_up, "left":self.perform_left, "down":self.perform_down, "right":self.perform_right}
        self.check_move_dict = {"up":self.check_up, "left":self.check_left, "down":self.check_down, "right":self.check_right}

#         random player starts
        self.player_turn = random.randint(1,2)
#         print(player_)


###########
# table creation methods
###########
    def insert_players(self, table, player):
        '''
        Function to insert players in board
        '''
        table[player.position[0]][player.position[1]] = player.name
        return table

    def create_board(self):
        '''
        Function to create a board of a certain dimension
            Puts players in board given player.position
        Outputs:
            table: list
        '''
        
#         Create top row (different from all other rows)
        top_row = [" ","_"] * self.dimension
        top_row.append(" ")
        top_row.append("\n")

#         Create normal row
        base_row = ["|","_","|","\n"]
        for x in range(self.dimension-1):
            base_row.insert(1,'¦')
            base_row.insert(1,'_')

#         Combine rows together into table (copying so that not a reference)
        table = []
        for x in range(self.dimension+1):
            if x ==0:
                table.append(top_row.copy())
            else:
                table.append(base_row.copy())

#         Insert players in table
        players = (self.player1, self.player2)
        for player in players:
            table = self.insert_players(table, player)

        return table
    
    def show(self):
        """
        Function to print the board table
        """
        
        for y in range(len(self.table)):
            for x in self.table[y]:
                print(x, end="")
                

###########
# play game related methods
###########

    def play(self):
        '''
        Play game initialiser:
            Calls either consecutive or simultaneous play method
            Resets table and player positions
        '''
        
        print(f"\n ############################## \n Let the game begin! \n Player {self.player_turn} starts. \n Board:")
        
        if self.game_type == "consecutive":
            self.play_consecutive()
        else:
            self.play_simultaneous()
        
        self.player1.position = list(self.player1.reset_position())
        self.player2.position = list(self.player2.reset_position())
        self.table = self.create_board()
        
       
    def play_consecutive(self):
        '''
        Wrapper function to play the game in consecutive turns
            Shows board
            Gets/checks and performs move
            Changes player turn
            Repeats until illegal move made - then shows play game outpus.
        '''

        legal = True
        players = (self.player1, self.player2)
        
#         perform moves/switch player turn until illegal move made
        while legal == True:
            self.show()
            check_move, direction_converted = self.get_move(players[self.player_turn - 1])
            legal = self.perform_move(players[self.player_turn - 1], check_move, direction_converted)
            if legal == True:
                self.player_turn = self.player_turn%2 + 1
                
#         update/print game outcome
        self.show()
        print(f'Player: {players[self.player_turn - 1].name} lost')
        players[self.player_turn - 2].score +=1
        print(f'The score is: \n Player {self.player1.name}: {self.player1.score}.')
        print(f'Player {self.player2.name}: {self.player2.score} \n')  
        

    def play_simultaneous(self):
        '''
        Wrapper function to play the game in simultaneous turns
            Shows board
            Gets, checks and performs move of both players independent of each other
            Repeats until illegal move made - then shows play game outputs (additional possibility of a draw)
        '''

        legal_1 = True
        legal_2 = True
        
        while legal_1 == True & legal_2 == True:
            self.show()
            
#     checks if both moves are legal (independent of each others moves), and performs moves
            check_move_1, direction_converted_1 = self.get_move(self.player1)
            check_move_2, direction_converted_2 = self.get_move(self.player2)

            legal_1 = self.perform_move(self.player1, check_move_1, direction_converted_1)
            legal_2 = self.perform_move(self.player2, check_move_2, direction_converted_2)
            
#     deal with draw collision scenario
            if self.player1.position == self.player2.position:
                self.table[self.player1.position[0]][self.player1.position[1]] = 'O'

                print('You crashed head on!')
                legal_1 = False
                legal_2 = False

#     all the win logic
        self.show()
        if not legal_1 and not legal_2:
            print('Draw')
        elif not legal_2:
            print(f'Player {self.player1.name} wins')
            self.player1.score +=1
        else:
            self.player2.score +=1
            print(f'Player {self.player2.name} wins.\n')
            
        print(f'The score is: \n Player {self.player1.name}: {self.player1.score}.')
        print(f'Player {self.player2.name}: {self.player2.score} \n')      
            
                
    def get_move(self, player):
        '''
        Function to:
            Receive, check and output human or computer input
            
        Inputs:
            player: Player object
        Outputs:
            check_move: bool
            direction_converted: list
        '''
        
#     deal with human input
        if player.type == "Human":
            direction = input(f'Input player {player.name} move: ').lower()
            
#     check direction inputed is in the players move_dictionary.keys, ""
            try:
                direction_converted = [player.player_dictionary[direction]]
#     check move is legal   
                check_move = list(map(lambda x: self.check_move_dict[x],direction_converted))[0](player)
        
            except KeyError:
                check_move = False
                direction_converted = None

                

        else:
#     get easy computer input
            if player.difficulty == 'easy':
                possible_moves = ['up','left','down','right']
                check_move, direction_converted = self.random_move(player = player, possible_moves = possible_moves)

#     get hard computer input
            else:
                check_move, direction_converted = self.smart_move(player = player)
            
# return move output
        return check_move, direction_converted


    def perform_move(self, player, check_move, direction_converted):
        '''
        Function to perform move
        Inputs:
            check_move: bool
            direction_converted: list
        Ouputs:
            bool - (whether move was legal or not)
        '''
    
        if check_move == True:
            list(map(lambda x: self.perform_move_dict[x],direction_converted))[0](player)
            return True
        else:
            print(f'Player {player.name} performed invalid move')
            return False
        

    
# Check move and perform move functions for each direction
    def check_up(self, player):
        '''
        Checks if up move is allowed or not
        Inputs: player: Player object
        '''
        row = player.position[0]
        col = player.position[1]

#         needed to avoid false index
        if row == 1:
            return False
        elif self.table[row-1][col] == "_":
            return True
        else:
            return False
            
                    
    def perform_up(self, player):
        '''
        Performs up move:
        Should only be performed if check_up returns True.
        Updates table and player position
        Inputs: player: Player object
        '''
        row = player.position[0]
        col = player.position[1]
        
        self.table[row][col] = "X"
        self.table[row-1][col] = player.name
        player.position[0] = row-1
            
            
    def check_left(self, player):
        '''
        Checks if left move is allowed or not
        Inputs: player: Player object
        '''
        row = player.position[0]
        col = player.position[1]

#         needed to avoid false index
        if col == 1:
            return False
        elif self.table[row][col-2] == "_":
            return True
        else:
            return False
            
                    
    def perform_left(self, player):
        '''
        Performs left move:
        Should only be performed if check_up returns True.
        Updates table and player position
        Inputs: player: Player object
        '''
        row = player.position[0]
        col = player.position[1]
        
        self.table[row][col] = "X"
        self.table[row][col-2] = player.name
        player.position[1] = col-2
         
            
    def check_down(self, player):
        '''
        Checks if down move is allowed or not
        Inputs: player: Player object
        '''
        row = player.position[0]
        col = player.position[1]

#         needed to avoid false index
        if row == self.dimension:
            return False
        elif self.table[row+1][col] == "_":
            return True
        else:
            return False
            
                    
    def perform_down(self, player):
        '''
        Performs down move:
        Should only be performed if check_up returns True.
        Updates table and player position
        Inputs: player: Player object
        '''
        row = player.position[0]
        col = player.position[1]
        
        self.table[row][col] = "X"
        self.table[row+1][col] = player.name
        player.position[0] = row+1
        
        
    def check_right(self, player):
        '''
        Checks if right move is allowed or not
        Inputs: player: Player object
        '''
        row = player.position[0]
        col = player.position[1]

#         needed to avoid false index
        if col == 2*self.dimension-1:
            return False
        elif self.table[row][col+2] == "_":
            return True
        else:
            return False
            
                    
    def perform_right(self, player):
        '''
        Performs right move:
        Should only be performed if check_up returns True!
        Updates table and player position
        Inputs: player: Player object
        '''
        row = player.position[0]
        col = player.position[1]
        
        self.table[row][col] = "X"
        self.table[row][col+2] = player.name
        player.position[1] = col+2


########
# Computer input methods
########

# method for easy computer input
    def random_move(self, player, possible_moves):
        '''
        Function to create random, non-suicidal input
        Input:
            player: Player object
            possible_moves: list
        Output:
            check_move: bool
            direction_converted: list
        '''
        
#         if run out of moves, return invalid move
        if len(possible_moves) == 0:
            check_move = False
            direction_converted = None
            return check_move, direction_converted
        
#         try random move - if allowed return it, else remove move from list and recursively use function
        else:
            rand = random.randint(0,len(possible_moves)-1)
            direction_converted = [possible_moves[rand]]            
            check_move = list(map(lambda x: self.check_move_dict[x],direction_converted))[0](player)
            if check_move == True:
                return check_move, direction_converted
            else:
                possible_moves.remove(direction_converted[0])
                return self.random_move(player, possible_moves)
    
    
    
# methods for smart computer input
    def get_coords_options(self, player, input_table):
        '''
        Function to output list of possible next move coordinates
        Inputs:
            player: Player object
            input_table: list
        Outputs:
            List of two element tuples
        '''

# use find player method instead of player.position (as looking at theoretical table objects)
        player_position = self.find_player(player, input_table)
        row = player_position[0]
        col = player_position[1]
        coords = []

# if move is allowed add coords to list
        if row==1:
            pass
        elif input_table[row-1][col] == "_":
            coords.append((row-1,col))

        if row==self.dimension:
            pass
        elif input_table[row+1][col] == "_":
            coords.append((row+1,col))

        if col==1:
            pass
        elif input_table[row][col-2]  == "_":
            coords.append((row,col-2))

        if col== 2*self.dimension-1:
            pass
        elif input_table[row][col+2]  == "_":
            coords.append((row,col+2))

        return coords


    def get_coords_values(self, player, input_table):
        '''
        Function to find values of possible move coordinates
        Inputs:
            player: Player object
            input_table: list
        Outputs:
            List of two element tuples
            Dictionary: {coordinates : coordinates value}
        '''
        
# get list of coords
        coords_options = self.get_coords_options(player, input_table)
        coords_values_dict = {}

# depending on number of possible options of coords assign a value to it
        for row, col in coords_options:
            value = 1
            if row==1:
                pass
            elif input_table[row-1][col] == "_":
                value += 1
            if row==self.dimension:
                pass
            elif input_table[row+1][col] == "_":
                value += 1
            if col==1:
                pass
            elif input_table[row][col-2]  == "_":
                value += 1
            if col==2*self.dimension -1:
                pass
            elif input_table[row][col+2]  == "_":
                value += 1
            coords_values_dict[(row,col)] = value

        return coords_options, coords_values_dict


    def update_table(self, player, input_table, coords):
        '''
        Function to create hypothetical, updated table for next iteration
        Inputs:
            player: Player object
            input_table: list
            coords: tuple
        Outputs:
            updated_table: list
        '''
        
#         copy table, make player position = X and coords = player name
        updated_table = copy.deepcopy(input_table)
        player_coords = self.find_player(player, updated_table)
        
        updated_table[player_coords[0]][player_coords[1]] = "X"
        updated_table[coords[0]][coords[1]] = player.name
        return updated_table

    def find_player(self, player, input_table):
        '''
        Function to find ad return player coordinates in a Board table
        Inputs:
            player: Player object
            input_table: list
        Outputs:
            tuple
        '''
        for el in range(len(input_table)):
            try:
                col = input_table[el].index(player.name)
                row = el
                return (row, col)
            except ValueError:
                pass
   

    def coords_direction_converter(self, player, best_coords):
        '''
        Function to convert coords into direction converted that can be used later
        Inputs:
            player: Player object
            best_coords: tuple
        Outputs:
            check_move: bool
            direction_converted: list
        '''
#     convert into direction
        if best_coords[0] < player.position[0]:
            direction_converted = ['up']
        elif best_coords[0] > player.position[0]:
            direction_converted = ['down']
        elif best_coords[1] < player.position[1]:
            direction_converted = ['left']
        else:
            direction_converted = ['right']
            
#     check move is legal
        check_move = False
        if list(map(lambda x: self.check_move_dict[x],direction_converted))[0](player):
            check_move = True
        return check_move, direction_converted
            

    def smart_move(self, player):
        '''
        Wrapper function to find and return best move for inputed player.
        Of all possible routes (limited to next five gos), find one with best value, and return the first move of that route
        (Number of iterations can be increased by adding additional for loop(s))
        Inputs:
            player: Player object 
        Outputs:
            check_move: bool
            direction_converted: list
        '''
        
        final_dict = {}
#         get coords_options, and coord values - then for each of those coords get new coords options and coords values
#         repeat x times
        it0_coords_options, it0_coords_values_dict = self.get_coords_values(player, input_table = self.table)
        
        for it_0 in it0_coords_options:
            final_dict[it_0] = 0

#         for each possible route, sum the values of each coordinate at that point in time
#         if value improves current then modify first move coordinates value
#         necessary to do this incrementally at each for loop (if doesnt reach last for loop, value will not be checkpointed)
            trail_value = it0_coords_values_dict[it_0]
            if trail_value > final_dict[it_0]:
                final_dict[it_0] = trail_value

            updated_table1 = self.update_table(player, input_table = self.table, coords = it_0)
            it1_coords_options, it1_coords_values_dict = self.get_coords_values(player, input_table = updated_table1)
            

            for it_1 in it1_coords_options:
                trail_value = it0_coords_values_dict[it_0] + it1_coords_values_dict[it_1]
                if trail_value > final_dict[it_0]:
                    final_dict[it_0] = trail_value
                
                updated_table2 = self.update_table(player, input_table = updated_table1, coords = it_1)
                it2_coords_options, it2_coords_values_dict = self.get_coords_values(player, input_table = updated_table2)


                for it_2 in it2_coords_options:
                    trail_value = it0_coords_values_dict[it_0] + it1_coords_values_dict[it_1] + it2_coords_values_dict[it_2]
                    if trail_value > final_dict[it_0]:
                        final_dict[it_0] = trail_value
                    
                    
                    updated_table3 = self.update_table(player, input_table = updated_table2, coords = it_2)
                    it3_coords_options, it3_coords_values_dict = self.get_coords_values(player, input_table = updated_table3)

                    for it_3 in it3_coords_options:
                        trail_value = it0_coords_values_dict[it_0] + it1_coords_values_dict[it_1] + it2_coords_values_dict[it_2] + it3_coords_values_dict[it_3]
                        if trail_value > final_dict[it_0]:
                            final_dict[it_0] = trail_value
                        
                        updated_table4 = self.update_table(player, input_table = updated_table3, coords = it_3)
                        it4_coords_options, it4_coords_values_dict = self.get_coords_values(player, input_table = updated_table4)

                        for it_4 in it4_coords_options:
                            trail_value = it0_coords_values_dict[it_0] + it1_coords_values_dict[it_1] + it2_coords_values_dict[it_2] + it3_coords_values_dict[it_3] + it4_coords_values_dict[it_4]
                            if trail_value > final_dict[it_0]:
                                final_dict[it_0] = trail_value                      
                        
                            updated_table5 = self.update_table(player, input_table = updated_table4, coords = it_4)
                            it5_coords_options, it5_coords_values_dict = self.get_coords_values(player, input_table = updated_table5)

                            for it_5 in it5_coords_options:
                                trail_value = it0_coords_values_dict[it_0] + it1_coords_values_dict[it_1] + it2_coords_values_dict[it_2] + it3_coords_values_dict[it_3] + it4_coords_values_dict[it_4] + it5_coords_values_dict[it_5]
                                if trail_value > final_dict[it_0]:
                                    final_dict[it_0] = trail_value                      

                                updated_table6 = self.update_table(player, input_table = updated_table5, coords = it_5)
                                it6_coords_options, it6_coords_values_dict = self.get_coords_values(player, input_table = updated_table6)

                                for it_6 in it6_coords_options:
                                    trail_value = it0_coords_values_dict[it_0] + it1_coords_values_dict[it_1] + it2_coords_values_dict[it_2] + it3_coords_values_dict[it_3] + it4_coords_values_dict[it_4] + it5_coords_values_dict[it_5] + it6_coords_values_dict[it_6]
                                    if trail_value > final_dict[it_0]:
                                        final_dict[it_0] = trail_value                      

                                    updated_table7 = self.update_table(player, input_table = updated_table6, coords = it_6)
                                    it7_coords_options, it7_coords_values_dict = self.get_coords_values(player, input_table = updated_table7)

                                    for it_7 in it7_coords_options:
                                        trail_value = it0_coords_values_dict[it_0] + it1_coords_values_dict[it_1] + it2_coords_values_dict[it_2] + it3_coords_values_dict[it_3] + it4_coords_values_dict[it_4] + it5_coords_values_dict[it_5] + it6_coords_values_dict[it_6] + it7_coords_values_dict[it_7]
                                        if trail_value > final_dict[it_0]:
                                            final_dict[it_0] = trail_value                      

                                        updated_table8 = self.update_table(player, input_table = updated_table7, coords = it_7)
                                        it8_coords_options, it8_coords_values_dict = self.get_coords_values(player, input_table = updated_table8)

                                
                                        for it_8 in it8_coords_options:
                                            trail_value = it0_coords_values_dict[it_0] + it1_coords_values_dict[it_1] + it2_coords_values_dict[it_2] + it3_coords_values_dict[it_3] + it4_coords_values_dict[it_4] + it5_coords_values_dict[it_5] + it6_coords_values_dict[it_6] + it7_coords_values_dict[it_7] + it8_coords_values_dict[it_8]

                                            if trail_value > final_dict[it_0]:
                                                final_dict[it_0] = trail_value

                                    
# if best_coords_list is not empty get best_coords, choose random one (if theres more than one)
# convert coords to move and check move
        if len(final_dict) > 0:
            best_coords_list = [(key, value) for key, value in final_dict.items() if value == max(final_dict.values())]
            rand = random.randint(0,len(best_coords_list)-1)
            best_coords = best_coords_list[rand][0]
            check_move, direction_converted = self.coords_direction_converter(player, best_coords)

        else:
            check_move = False
            direction_converted = None
        
        return check_move, direction_converted

 