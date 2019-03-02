import operator

#drops a token in the specified column, returns a tuple of (the game board after the drop, if the drop was successful)
def didDropToken(column, game_board, empty_num, my_player_num):
    if (game_board[0][column] != empty_num): #if the top spot is already occupied
        return game_board, False #we can't move here
    else:
        row = 1 #go to the next spot
        while row < len(game_board) - 1: #while we're stil on the board
            if (game_board[row][column] == empty_num): #if the spot is empty
                row += 1 #account for gravity
            if (game_board[row][column] != empty_num): #otherwise there's a piece here
                game_board[row - 1][column] = my_player_num #our token will land on top
                return game_board, True #it dropped!
        game_board[row][column] = my_player_num #we're at the bottom of the board
        return game_board, True #the token landed

def tryDropAndScore(column, game_board, empty_num, player_num):
    copy_game_board = [row[:] for row in game_board] #need a deep copy here
    dropAttempt = didDropToken(column, copy_game_board, empty_num, player_num) #try dropping a token 
    if (dropAttempt[1] == True): #if it worked
        score = evaluate(dropAttempt[0], player_num) #evaluate it
        return (score, dropAttempt[0]) #(the score after the drop, the game board after the drop)
    else: #if it didn't work
        score = -1000 #give it a low score
        return (score, dropAttempt[0]) #(the score after the drop, the game board after the drop)

def miniMax (game_board, empty_num, my_player_num):
    move_set = []
    scored_move_set = []
    min_max_flipper = 2
    opponent_num = getOpponentNum(my_player_num)
    cols = len(game_board[0])

    #generate the moveset
    for a in range(cols): #my first move
        for b in range(cols): #their move
            for c in range(cols): #my move
                move_set.append((a, b, c)) #including base state, this is a 4-ply moveset

    #for every combination, loop through the columns
    for move in move_set: 
        current_board = game_board #reset the game board to the current state
        my_scored_moves = []
        for token_drop in move:
            if (min_max_flipper % 2 == 0): # if it's my turn
                drop = tryDropAndScore(token_drop, current_board, empty_num, my_player_num) #drop my piece and score it
                my_scored_moves.append((drop[0], token_drop))
            else: #if it's their turn
                drop = tryDropAndScore(token_drop, current_board, empty_num, opponent_num) #drop their piece and score it
                my_scored_moves.append((drop[0], token_drop))
            current_board = drop[1] #keep this move's board intact
            min_max_flipper += 1 #it's the next player's turn
        scored_move_set.append(my_scored_moves) #put this move set into the list of scored move sets

    best_moves = max_eval(scored_move_set, 2, 1)
    best_moves1 = min_eval(best_moves, 1, 1)
    best_moves2 = max_eval(best_moves1, 0, 1)

    return best_moves2[0][0][1]

def max_eval(scored_move_set, which_tuple, which_value):
    cols_to_check = []
    for x in scored_move_set: 
        if x[which_tuple][which_value] not in cols_to_check: 
            cols_to_check.append(x[which_tuple][which_value])

    best_moves = []
    for col in cols_to_check:
        moves_this_col = [t for t in scored_move_set if t[which_tuple][which_value] == col] #all of the moves for this column in this ply
        moves_this_col.sort(key = operator.itemgetter(which_tuple), reverse = True) #sort them (MAX)
        best_moves.append(moves_this_col[0]) #grab the best and append it to the best moves
    return best_moves

def min_eval(scored_move_set, which_tuple, which_value):
    cols_to_check = []
    for x in scored_move_set: 
        if x[which_tuple][which_value] not in cols_to_check: 
            cols_to_check.append(x[which_tuple][which_value])

    best_moves = []
    for col in cols_to_check:
        moves_this_col = [t for t in scored_move_set if t[which_tuple][which_value] == col] #all of the moves for this column in this ply
        moves_this_col.sort(key = operator.itemgetter(which_tuple)) #sort them (MIN)
        best_moves.append(moves_this_col[0]) #grab the best and append it to the best moves
    return best_moves

#opponent will always be opposite of me, tell me what that is (1 or 2)
def getOpponentNum(my_player_num):
    if (my_player_num == 1):
        opponent_num = 2
    else: 
        opponent_num = 1
    return opponent_num

#give me a score for this state of the board
def evaluate(game_board, my_player_num):
    connect = 4 #we are trying to connect this many
    empty_num = 0 #this is the symbol representing an empty space
    opponent_num = getOpponentNum(my_player_num)

    # coords are a (row, column) tuple - 0 based
    my_player_coords = [] 
    opponent_coords = []

    for row in range(len(game_board)): #for all the rows
        for col in range(len(game_board[row])): #and all the columns
            if (game_board[row][col] == my_player_num): #if the current spot has my player 
                my_player_coords.append((row, col)) #add it to my coordinate list
            elif (game_board[row][col] == opponent_num): #if the current spot has the opponent
                opponent_coords.append((row, col)) #add it to the opponent's list
    
    my_score = playerScore(my_player_coords, my_player_num, game_board, connect, empty_num) #test my score
    opponent_score = playerScore(opponent_coords, opponent_num, game_board, connect, empty_num) #test opponent's score
    score = my_score - opponent_score #more positive means better for me
    return score

#take all of the coords and check out three in either direction. Gets a point if empty. Gets 2 if filled with player of same type. Stops if finds opponent.
def playerScore(player_coords, player_num, game_board, connect, empty_num):
    score = 0 
    for coord in player_coords: #for all of the coords in the list
        row = int(coord[0])
        col = int(coord[1])
        #check up, down, right, left
        #check down
        for step in range(row + 1, row + connect):
            test_result = coordScore(game_board, step, col, empty_num, player_num)
            score += test_result[0]
            if (test_result[1] == False):
                break
        #check up        
        for step in range(row - 1, row - connect, -1):
            test_result = coordScore(game_board, step, col, empty_num, player_num)
            score += test_result[0]
            if (test_result[1] == False):
                break
        #check right
        for step in range(col + 1, col + connect):
            test_result = coordScore(game_board, row, step, empty_num, player_num)
            score += test_result[0]
            if (test_result[1] == False):
                break
        #check left
        for step in range(col - 1, col - connect, -1):
            test_result = coordScore(game_board, row, step, empty_num, player_num)
            score += test_result[0]
            if (test_result[1] == False):
                break

        #check diagonal directions 
        check_row_diag = row + 1 #diag x value to check
        check_col_diag = col + 1 #diag y value to check
        while (check_row_diag <= row + connect and check_col_diag <= col + connect): #check diag down, right
            test_result = coordScore(game_board, check_row_diag, check_col_diag , empty_num, player_num)
            score += test_result[0]
            if (test_result[1] == False):
                break
            check_row_diag += 1
            check_col_diag += 1
        check_row_diag = row + 1 #diag x value to check
        check_col_diag = col - 1 #diag y value to check
        while (check_row_diag <= row + connect and check_col_diag >= col - connect): #check diag down, left
            test_result = coordScore(game_board, check_row_diag, check_col_diag , empty_num, player_num)
            score += test_result[0]
            if (test_result[1] == False):
                break
            check_row_diag += 1
            check_col_diag -= 1
        check_row_diag = row - 1 #diag x value to check
        check_col_diag = col + 1 #diag y value to check
        while (check_row_diag >= row - connect and check_col_diag <= col + connect): #check diag up, right
            test_result = coordScore(game_board, check_row_diag, check_col_diag , empty_num, player_num)
            score += test_result[0]
            if (test_result[1] == False):
                break
            check_row_diag -= 1
            check_col_diag += 1
        check_row_diag = row - 1 #diag x value to check
        check_col_diag = col - 1 #diag y value to check
        while (check_row_diag >= row - connect and check_col_diag >= col - connect): #check diag up, right
            test_result = coordScore(game_board, check_row_diag, check_col_diag , empty_num, player_num)
            score += test_result[0]
            if (test_result[1] == False):
                break
            check_row_diag -= 1
            check_col_diag -= 1
    return score

#apply a score to checked coords
def coordScore (game_board, row, col, empty_num, my_player_num):
    row_count = len(game_board)
    col_count = len(game_board[0]) #assumes uniformity
    if(row > row_count - 1 or row < 0 or col > col_count - 1 or col < 0): #if these coords aren't in the bounds of the board
        return (0, False) #don't give any points and don't allow more calls
    if (game_board[row][col] == empty_num): #if the space is empty
        return (1, True) #give 1 point and allow more calls
    elif (game_board[row][col] == my_player_num): #if the space has my player
        return (3, True) #give 2 points and allow more calls
    else: #otherwise it's the other player
        return (0, False) #subtract 2 points and don't allow more calls

if __name__ == '__main__':
  
    board3 = [[0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,1,0],
              [0,2,0,0,0,1,0]]

    print(miniMax(board3, 0, 1))