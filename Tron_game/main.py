# create game function
def main():

    start = input("Would you like to play Tron? (y/n)")
    
    if start.lower() == "n":
        print("Have a nice day")
        
    elif start.lower() == "y":
        
        correct_input = True
        while correct_input:
            game_type = input('What game version would yo like to play?: \n a. Consecutive turns? \n b. Simultaneous turns? \n (Choose a or b) \n').lower()
        
            if game_type in ("a","b"):
                break
            else:
                print("I didn't quite get that, (type a or b):")
            

        correct_input = 0
        while correct_input == 0:
            try:
                dimension = int(input('Please insert board size (minimum 4).'))
                if dimension >= 4:
                    correct_input = 1
                else:
                    print("(Board size minimum is 4)")
            except:
                print("I didn't quite get that, please input an number")
                
            
            
            
        
        game = Board(dimension)
        
        

        

if __name__ == '__main__':

    a = Board(7)
    a.__main__()
    

    