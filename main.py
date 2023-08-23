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

        #create QLabel widget to display the title
        title_label = QtWidgets.QLabel("Connect Four")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        #create a makeBoard widget and add it to the layout
        self.board = makeBoard()
        layout.addWidget(self.board)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = mainWindow()
    window.resize(800, 600)
    window.show()
    app.exec()
