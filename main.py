from PyQt5 import QtWidgets, QtCore
from makeNewBoard import makeBoard

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        title = "CONNECT4"
        self.setWindowTitle(title)

        #create a central widget to hold the layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        #create vertical layout
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)


        self.play_again_button = QtWidgets.QPushButton("Play Again")
        self.play_again_button.clicked.connect(self.play_again)
        # Add the "Play Again" button to the layout
        layout.addWidget(self.play_again_button)
        self.play_again_button.setStyleSheet('background-color: red;')
        self.play_again_button.setVisible(False)

        #create QLabel widget to display the title
        title_label = QtWidgets.QLabel("Connect Four")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        #create a makeBoard widget and add it to the layout
        self.board = makeBoard(self.play_again_button)
        layout.addWidget(self.board)
        
        self.setStyleSheet('background-color: lightblue;')

        for row in self.board.board:
            for button in row:
                button.setStyleSheet("background-color: lightgray;")

    def play_again(self):
        self.board.reset_game()
        self.play_again_button.setVisible(False)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = mainWindow()
    window.resize(800, 600)
    window.show()
    app.exec()
