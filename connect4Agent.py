def evaluate(game_board, my_player_num):
    connect = 4 #we are trying to connect this many
    empty_num = 0 #this is the symbol representing an empty space
    
    #opponent will always be opposite of me
    if (my_player_num == 1):
        opponent_num = 2
    else: 
        opponent_num = 1

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
    coords_to_check = []
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

def coordScore (game_board, row, col, empty_num, my_player_num):
    row_count = len(game_board)
    col_count = len(game_board[0]) #assumes uniformity
    if(row > row_count - 1 or row < 0 or col > col_count - 1 or col < 0): #if these coords aren't in the bounds of the board
        return (0, False) #don't give any points and don't allow more calls
    if (game_board[row][col] == empty_num): #if the space is empty
        return (1, True) #give 1 point and allow more calls
    elif (game_board[row][col] == my_player_num): #if the space has my player
        return (2, True) #give 2 points and allow more calls
    else: #otherwise it's the other player
        return (0, False) #subtract 2 points and don't allow more calls

if __name__ == '__main__':
    player = 1
    board1 = [[0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,2,0,0,0],
              [0,0,0,1,0,0,0],
              [0,0,0,2,0,0,0],
              [0,2,1,1,1,2,0]]
    
    board2 = [[0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,1,0,0,0],
              [0,0,0,1,0,0,0],
              [0,0,0,1,0,0,0],
              [2,2,2,1,2,0,0]]

    print("I'm player #{}".format(player))
    print("Here's the score for the first board: {}".format(evaluate(board1, 1)))
    print("Here's the score for the second board: {}".format(evaluate(board2, 1)))