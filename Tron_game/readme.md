# readme: Tron game

## Overview
* main.py and tron_classes.py are only scripts. All other files are working/can be ignored

## main.py
* Creates setup functions for game.
* imports game classes
* Running script to play game

## tron_classes.py
* Creates player and board classes for game



### Player class(es):
* Holds attributes associated with players that do not effect board attributes.
* Player class holds maximum methods/attributes that are common to both player and computer classes.
* Human class requires additional method and function to create/show keys.
* Computer class requires additional dofficulty input.

### Board class:
* Holds all atributes and methods to create game and run game.
* Board setup depends on input variables: (table) dimension, game_type and player_type
* In summary:
    * Creates table, creates players
    * Function to play game (depends on game_type)
        * Gets, then checks human/computer move input
        * Performs move (if legal)
        * Repeat until a player makes an illegal move
        * Outputs game conclusion, and resets table
    * Computer input:
        * Easy:
            * Either random and non-suicidal
        * Hard: **

            * Assign a value to the resultant state of a possible move at that particular time point (value = 1 (if state exists +1 for each possible direction from that state)
            * Create a hypothetical new board of that new state and then repeat previous step x times (max 9) (keeping the value of that previous state)
            * At the max no. of iterations, sum the values of all states that lead to the final state, and assign the best paths value to the first move in a dictionary.
            * Then return the move that has the highest path value (random choice if more than one)
            * Assumptions: Other player does not move.
            
        * Both Computer functions then produce a check_move and direction_converted output that then is applied to the perform_xxxx functions to update the board and players positions.
        

## Discussion/thoughts as game was made

* setup functions - lookup input into a dictionary as then only had to deal with keyerrors.

* decided to have a player.position attribute that gets updated instead of calling a find_player method every time (this is more efficient, no need to iterate trhough table), and makes more sense that position is a player attribute not a board attribute

* table design - went for this one as was the nicest and most consistent/simple (equal length of each row list) - easier for moveing players etc.

* play structure:
    * tried to make functions as modular (so reusable) as possible, e.g.:
    * all move related functions are irrelevant of game_type - (any dependence on this variable is restricted to differences in play_consecutive/play_simultaneous functions only)
    * modified get_move to ensure all performing/checking move input is irrelevant of player type (and player_type dependence is restricted in the get_move function)
    * originally had 4 up/left/down/right functions that checked if move was legal and performed move at once. changed to 8 check_up/perform_up functions - which checked and performed the move individually. This was because: Simultaneous game mode and computer move functions would benefit from a function that checks the move is legal without performing move. (Allowed me to remove complex head-on-crash draw logic, and use functions in get.check computer inputs).
    
* Easy computer discussion:
    * Choose random direction results in very quick game (dies immediately).
    * So improved to:
        * Choose a random direction - check direction, remove from list if illegal, repeat until all directions tried.
        * Use function recursively to repeat
    
* Smart computer discussion:
    * Reading on dynamic programming/reinforcement learning, attempted to introduce a dynamic prgramming algorithm with the following parameters:
        * Time: Finite. T = no. of free spaces/2
        * States: No. of states is dependent on time - is number of free spaces
        * Policy: Start with random policy (equal chance of up/down/left/right)
        * Cost function: Use positive reinforcement: Assign positive value of +1 to each square (state) +1 for each possible direction from that state
        * Unsuccessful in building this, as struggled trying to take into account the possible different states at the ultimate time T, T-1 etc.
        
    * Simpler method:
        * Instead of working backward, work forwards, and only go a finite number of moves ahead (e.g. 9).
        * Use same value calculation for each state - (only calculate value for the states in question instead of all states - quicker).
        * Assume other player is stationary (this is inaccurate but too complex if try to model other player)
        * This then resulted in the algorithm that I have - see earlier ** for description.
        * Attempted to make function recursive and thus occur a maximum number of times (depending on no. of empty spaces left, but failed as needed to keep previous functions outputs, could have done but would have required a lot more time..)
        * Structure considerations:
            * Break up function into modular parts and then combine in the smart_move wrapper function.
            * Get smart_move wrapper function to output the same as random_move and human_move - so compatible with rest of programme.


                    

