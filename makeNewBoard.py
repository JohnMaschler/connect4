from PyQt5 import QtWidgets, QtCore
import random
from cpu import cpuChooseMove

class makeBoard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(makeBoard, self).__init__(parent)
        self.current_player = 1#human player starts game
        self.game_over = False

        self.board = [[None for _ in range(7)] for _ in range(6)]#initialize the board

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        for row in range(6):
            for col in range(7):
                button = QtWidgets.QPushButton()
                button.setFixedSize(80, 80)#each cell will be a button

                button.clicked.connect(lambda row=row, col=col: self.makeMove(col))#need to connect button signal to makeMove function

                self.gridLayout.addWidget(button, row, col)#add button to grid layout
                self.board[row][col] = button

        self.message_label = QtWidgets.QLabel()#label to display messages to player
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.message_label, 6, 0, 1, 7)#add label to grid layout

        print(type(self.board[1][1]))

    def makeMove(self, col):#human player makes a move
        if self.current_player == 1:
            for r in reversed(range(6)):#find the first open row in a column from bottom up
                if self.board[r][col].text() == '':#cell is empty
                    self.board[r][col].setStyleSheet("background-color: red;")#set cell to red
                    self.board[r][col].setText('1')#store which player made the move
                    self.updateGameState(r, col)#check for winner or draw
                    if self.game_over:
                        return
                    self.current_player = 2#next player's turn
                    self.message_label.setText(f"Player {self.current_player}'s turn")#label
                    self.cpuMakeMove()  #trigger CPU move after human move
                    break

    def cpuMakeMove(self):
        if self.current_player == 2:#cpu's turn
            self.setEnabled(False)  #disable the board temporarily for CPU's turn so user 1 can't click anything
            QtCore.QTimer.singleShot(500, self.makeCPUMove)  #delayed CPU move using QTimer

    def makeCPUMove(self):
        # import random
        cpu_col = cpuChooseMove(self.board)#random.randint(0,6)# Let the CPU choose a move
        self.applyMove(cpu_col)  #apply the CPU's move
        self.setEnabled(True)  #enable the board again after CPU move

    
    def applyMove(self, col):#cpu makes a move
        for r in reversed(range(6)):
            if self.board[r][col].text() == '':#find first open row in chosen column
                self.board[r][col].setStyleSheet("background-color: yellow;")#yellow for player 2
                self.board[r][col].setText('2')
                self.updateGameState(r, col)#check for winner or draw
                if self.game_over:
                    return
                
                self.current_player = 1
                self.message_label.setText(f"Player {self.current_player}'s turn")
                break

    def updateGameState(self, row, col):
        # if self.game_over:
        #     return  # Do nothing if the game is already over
        
        #check if the current player has won
        if self.checkWin(row, col):
            self.message_label.setText(f"Player {self.current_player} wins!")
            self.game_over = True  #game over
            for row in self.board:#stop the users from giving anymore input!
                for button in row:
                    button.setEnabled(False)
        #check if the game is a draw
        elif self.checkDraw():
            self.message_label.setText("The Game is a Draw!")
            self.game_over = True  #no more moves made
            for row in self.board:#disable button for users
                for button in row:
                    button.setEnabled(False)
        else:#continue game
            pass


    def checkWin(self, row, col):
        #check if the current player has four in a row horizontally, vertically, or diagonally
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]#tuples for each possible direction
        
        for d_row, d_col in directions:#check all possible directions
            count = 0
            for i in range(-3, 4):
                r = row + i * d_row#calculate the row and column indices for the position being checked based on i
                c = col + i * d_col
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c].text() == str(self.current_player):#make sure within bounds of game and player has marker there
                    count += 1
                    if count == 4:
                        return True#won
                else:
                    count = 0
                    
        return False#didn't win

    def checkDraw(self):
        #are all the spots filled?
        for row in range(6):
            for col in range(7):
                if self.board[row][col].text() == '':
                    return False
        return True
