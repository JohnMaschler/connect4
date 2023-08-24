import math
import copy

def cpuChooseMove(board):
    board_copy = [[None for _ in range(7)] for _ in range(6)]#create a copy of the board that is easier to work with
    for row in range(6):
        for col in range(7):
            board_copy[row][col] = board[row][col].text() #instead of working with each cell being type of QPushButton
    # print(board_copy)

    def checkWin(board, player):# check if the current player has four in a row horizontally, vertically, or diagonally
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]#tuples for each possible direction

        for row in range(6):
            for col in range(7):
                for d_row, d_col in directions:#check all possible directions
                    count = 0
                    for i in range(-3, 4):
                        r = row + i * d_row#calculate the row and column indices for the position being checked
                        c = col + i * d_col#based on i
                        if 0 <= r < 6 and 0 <= c < 7 and board[r][c] == str(player):#make sure within bounds of game and player has marker there
                            count += 1
                            if count == 4:#4 in a row
                                return True
                        else:
                            count = 0

        return False#didn't win

    def checkDraw(board):
        #check if the board completely filled up
        for row in range(6):
            for col in range(7):
                if board[row][col] == '':
                    return False
        return True

    game_over = checkWin(board_copy, 2) or checkDraw(board_copy)#did cpu win or is it a draw

    #evaluation function for the state of the game
    def evaluate(board_copy):
        # making a scoring function. These weights can be changed to change how the bot plays
        def score_configuration(p1, p2, p3, p4):
            cpu_count = [p1, p2, p3, p4].count('2')#counting the number of pieces each player has in a given configuration
            human_count = [p1, p2, p3, p4].count('1')

            #assigning a score based on the number of pieces of each player
            if cpu_count == 4:#4 in a row weighted the most
                return 100
            elif cpu_count == 3 and human_count == 0:#these weights are somewhat arbitrary but generally maximize cpu and minimize human
                return 10
            elif cpu_count == 2 and human_count == 0:
                return 1
            elif human_count == 3 and cpu_count == 0:
                return -50
            elif human_count == 2 and cpu_count == 0:
                return -10
            elif human_count ==4 and cpu_count ==0:
                return -90
            else:
                return 0


        #calculate total score for the board_copy
        total_score = 0

        #check all the rows and update total_score based on score_configuration weights
        for row in range(6):
            for col in range(4):
                p1 = board_copy[row][col]
                p2 = board_copy[row][col + 1]
                p3 = board_copy[row][col + 2]
                p4 = board_copy[row][col + 3]
                total_score += score_configuration(p1, p2, p3, p4)

        #check columns
        for row in range(3):
            for col in range(7):
                p1 = board_copy[row][col]
                p2 = board_copy[row + 1][col]
                p3 = board_copy[row + 2][col]
                p4 = board_copy[row + 3][col]
                total_score += score_configuration(p1, p2, p3, p4)

        #check diagnols
        for row in range(3):
            for col in range(4):
                p1 = board_copy[row][col]
                p2 = board_copy[row + 1][col + 1]
                p3 = board_copy[row + 2][col + 2]
                p4 = board_copy[row + 3][col + 3]
                total_score += score_configuration(p1, p2, p3, p4)

        for row in range(3):
            for col in range(3, 7):
                p1 = board_copy[row][col]
                p2 = board_copy[row + 1][col - 1]
                p3 = board_copy[row + 2][col - 2]
                p4 = board_copy[row + 3][col - 3]
                total_score += score_configuration(p1, p2, p3, p4)
        # print(total_score)

        return total_score
            # Normalize the total score to keep it in a reasonable range
        # max_possible_score = 1000
        # normalized_score = total_score / max_possible_score
        # print(normalized_score)

        # return normalized_score





    def isColumnFull(board_copy, col):#check if a column is full
        for row in range(6):
            if board_copy[row][col] == '':
                return False
        return True
    
    def makeMove(board_copy, col, player):#make a move on the board
        for row in reversed(range(6)):
            if board_copy[row][col] == '':
                board_copy[row][col] = (str(player))
                return row
    
    def undoMove(board_copy, row, col):#undo move at given location on board
        board_copy[row][col]=''

    def minimax(board_copy, depth, alpha, beta, maximizingPlayer):
        #https://en.wikipedia.org/wiki/Minimax#Pseudocode
        #check if the game is over or if we have reached the maximum depth
        if game_over or depth == 0:
            return evaluate(board_copy)#evaluation of current board state

        if maximizingPlayer:#CPU's turn
            maxEval = -math.inf#initialize max evaluation to negative inf
            for col in range(7):#iterate over all possible moves
                if not isColumnFull(board_copy, col):#column isn't full
                    row = makeMove(board_copy, col, 2)#we make the move on temp board
                    eval = minimax(board_copy, depth - 1, alpha, beta, False)#recursively call function to evaluate move
                    maxEval = max(maxEval, eval)#update maxEval and alpha values
                    alpha = max(alpha, eval)
                    undoMove(board_copy, row, col)#undo the move
                    if beta <= alpha:#stop searching branch if alpha LE beta (alpha-beta pruning - improves performance)
                        break
            return maxEval
        else:#minimizing player's turn
            minEval = math.inf#min eval is inf
            for col in range(7):#iterate over all possible columns/moves
                if not isColumnFull(board_copy, col):#if we can make the move then make it
                    row = makeMove(board_copy, col, 1)
                    eval = minimax(board_copy, depth - 1, alpha, beta, True)#evaluate with recursive call to minimax
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    undoMove(board_copy,row,col)#reset board
                    if beta <= alpha:#alpha beta pruning
                        break
            return minEval

    #choose the best move for the CPU using Minimax
    best_score = -math.inf#initialize best_score and best_move
    best_move = None
    for col in range(7):#iterate over all possible columns/moves
        if not isColumnFull(board_copy,col):
            row = makeMove(board_copy,col,2)#make temp move
            #minimax function evaluates the move with depth of 4 (can change depth)
            score = minimax(board_copy,4,-math.inf,math.inf,False)
            if score > best_score:
                best_score = score#update
                best_move = col
            undoMove(board_copy,row,col)

    print(best_move)#see best move and best score as they're being played
    print(best_score)

    return best_move