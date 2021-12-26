

        
class Player():
    
    def __init__(self, name, dimension, default_keys = True):
        self.name = name
        self.dimension = dimension
        self.score = 0
        self.player_dictionary = self.player_dictionary_setup()
        self.position = list(self.set_position())
        
        print(f"Player {self.name} keyboard: {list(self.player_dictionary.keys())}")
        
    def player_dictionary_setup(self):
        '''
        Function to create move dictionary for the two players
        '''
        
#         add in change keys later if needed
        if self.name == "1":
            player_dictionary = {"w":'up', "a":'left', "s":'down', "d":'right'}

        else:
            player_dictionary = {"i":'up', "j":'left', "k":'down', "l":'right'}
            
        return player_dictionary
    
    
    def set_position(self):
        if self.name == "1":
            return (1, 1)
        else:
            return self.dimension, 2*self.dimension-1
        
        
        
        
        
class Board():
    """
    The Board class
    """

        
        
    def __init__(self, dimension):
        self.dimension = dimension
        self.player1 = Player(name = '1', dimension = dimension)
        self.player2 = Player(name = '2', dimension = dimension)  
        
        self.table = self.create_board(dimension)
        self.player_turn = 1


        self.show()
 
#        @staticmethod
    def insert_players(self, table, player):
    # insert players on board (customise character symbols?) add on @ symbol?
        table[player.position[0]][player.position[1]] = player.name

        return table

    def create_board(self, dimension):
        '''
        Creates a board given a dimension
        Puts players in board
        '''
        
        assert type(dimension) == int, "Please input an integer for board size"
        assert dimension > 3, "Board size must be greater than 3"

#         Create top row (different from all other rows)
        top_row = [" ","_"] * dimension
        top_row.append(" ")
        top_row.append("\n")

#         Create normal row
        base_row = ["|","_","|","\n"]

        for x in range(dimension-1):
            base_row.insert(1,'¦')
            base_row.insert(1,'_')

#         Combine rows together (copying so that not a reference)
        table = []
        for x in range(dimension+1):
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
        """Function to print the board table"""
        
        for y in range(len(self.table)):
            for x in self.table[y]:
                print(x, end="")
                
   
            
             

    def move(self, player):
        '''Function to receive input, move player, determine if move legal or not
        '''
        
#         use of dictionary, then only exception to deal with is key error
        move_dictionary = {"up":self.up, "left":self.left, "down":self.down, "right":self.right}
        direction = input(f'Player {self.player_turn} move: ').lower()
        
        
#         assert direction inputed is in the players move_dictionary.keys, ""
        try:
            direction_converted = [player.player_dictionary[direction]]
            legal = list(map(lambda x: move_dictionary[x],direction_converted))[0](player)
            
            
        except KeyError:
            print('Invalid Move')
            legal = False
       
        return legal

    
    

#     def find_player(self):
#         for el in range(len(self.table)):
#             try:
#                 col = self.table[el].index(self.player_turn)
#                 row =el
#             except ValueError:
#                 pass
#         return row, col
    
    
    def up(self, player):
        
        row = player.position[0]
        col = player.position[1]
        
        if row == 1:
            return False
        else:
            if self.table[row-1][col] == "_":
                self.table[row][col] = "X"
                self.table[row-1][col] = self.player_turn
                
                player.position[0] = row-1
                return True     
            else:
                return False
            
    def left(self, player):
        
        row = player.position[0]
        col = player.position[1]
        
        if col == 1:
            return False
        else:
            if self.table[row][col-2] == "_":
                self.table[row][col] = "X"
                self.table[row][col-2] = self.player_turn
                
                player.position[1] = col-2
                return True     
            else:
                return False     
            
    def right(self, player):
        
        row = player.position[0]
        col = player.position[1]
        
        if col == 2*self.dimension-1:
            return False
        else:
            if self.table[row][col+2] == "_":
                self.table[row][col] = "X"
                self.table[row][col+2] = self.player_turn
                
                player.position[1] = col+2
                return True     
            else:
                return False     

    def down(self, player):
        
        row = player.position[0]
        col = player.position[1]
        
        if col == self.dimension+1:
            return False
        else:
            if self.table[row+1][col] == "_":
                self.table[row][col] = "X"
                self.table[row+1][col] = self.player_turn
                
                player.position[0] = row+1
                return True     
            else:
                return False     
            
            
    def __main__(self):
        '''
        Function to run the game
        '''
#         print(f"\n Player {str(self.player_turn)}'s turn: \n ")

        legal = True
        player_tuple = (self.player1, self.player2)
        
        while legal == True:
            legal = self.move(player_tuple[self.player_turn - 1])
            if legal == True:
                self.show()
                self.player_turn = self.player_turn%2 + 1
        print(self.player_turn, "lost")
        
        
        

