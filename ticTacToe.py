# CPTR 251
# Jeffrey Filiberto II
# Sources:
# Pyside documentation
# Pyside6 Tutorial
# History:
# 11/14/22- Started, started init and made a loop that creates buttons to add to a grid
# 11/16/22 got move, reset, alternating and decting wins to work
# 11/17/22 hyperventallated, Added win tallies, reformatted some stuff, completed

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QLabel, QPushButton

class ticTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic-Tac-Toe! :,)")
        self.setFixedSize(QSize(650, 700))

        self.gameBoard = QGridLayout()
        self.currentTurn = "X"
        self.tileList = []
        self.winner = ''
        
        for row in range(1,3+1):
            for square in range(0, 3):
                self.tile = QPushButton(self)
                self.tile.setFixedSize(180,180)
                self.gameBoard.addWidget(self.tile, row, square)
                def callMove(r = row, s = square, t = self.tile):
                    self.move(r, s, t)
                self.tile.pressed.connect(callMove)
                self.tileList.append(self.tile)

        self.turnLabel = QLabel()
        self.turnLabel.setText(f"It is {self.currentTurn}'s turn!")
        self.turnLabel.setFont(QFont('Arial', 25))
        self.gameBoard.addWidget(self.turnLabel, 0,0)

        self.resetButton = QPushButton(f"Resest Game")
        self.gameBoard.addWidget(self.resetButton, 0,2)
        self.resetButton.pressed.connect(self.gameReset)

        # current fix for first reset not asked for conformation
        self.gameReset()

        self.xWin = 0
        self.xWinTally = QLabel(f"X's Wins: {self.xWin}")
        self.xWinTally.setFont(QFont('Arial', 30))
        self.gameBoard.addWidget(self.xWinTally, 4 , 0)

        self.oWin = 0
        self.oWinTally = QLabel(f"O's Wins: {self.oWin}")
        self.oWinTally.setFont(QFont('Arial', 30))
        self.gameBoard.addWidget(self.oWinTally, 4 , 1)

        self.Draws = 0
        self.drawTally = QLabel(f"Draws: {self.Draws}")
        self.drawTally.setFont(QFont('Arial', 30))
        self.gameBoard.addWidget(self.drawTally, 4 , 2)

        widget = QWidget()
        widget.setLayout(self.gameBoard)
        self.setCentralWidget(widget)

    def move(self, row : int, square : int, tile : QPushButton):
        """Changes the pressed Buttons text to the current players token, also calls detectWin, alternatePlayer and detectDraw"""
        if tile.text() == "":
            tile.setText(self.currentTurn)
            tile.setFont(QFont('Arial', 75))
            tile.setFlat(True)
            self.alternatePlayer()
            self.detectWin()
            self.detectDraw()
    
    def alternatePlayer(self):
        """Changes the token after every turn"""
        self.currentTurn = "O" if self.currentTurn == "X" else "X"
        self.turnLabel.setText(f"It is {self.currentTurn}'s turn!")

    def gameReset(self):
        """resets all the buttons to blanks and starts a new game"""
        if self.resetButton.text() == "Reset Game":
            self.resetButton.setText("Are you sure?")
        else:
            for tile in self.tileList:
                tile.setText('')
                tile.setFlat(False)
                tile.setEnabled(True)
                tile.setStyleSheet('color: white;')
                self.resetButton.setText("Reset Game")
                self.currentTurn = "X"
                self.turnLabel.setText(f"It is {self.currentTurn}'s turn!")

    def detectWin(self):
        """checks the tiles to see if there is a win after every move, checks 3 different ways, Vertically Horizontally and Diagonally
        if a win is detected it calls win"""
        #---------D Wins
        if (self.tileList[0].text() == self.tileList[4].text() and self.tileList[0].text() == self.tileList[8].text() and self.tileList[0].text() != ""):
            self.win(0, 4, 8)   
        elif (self.tileList[2].text() == self.tileList[4].text() and self.tileList[2].text() == self.tileList[6].text() and self.tileList[2].text() != ""):
            self.win(2,4,6)       
        #------------V Wins
        for tile in range(3):
            if self.tileList[tile].text() == self.tileList[tile + 3].text() and self.tileList[tile].text() == self.tileList[tile + 6].text() and self.tileList[tile].text() != "":
                self.win(tile, tile+3, tile+6)
        #--------H Wins
        for tile in range(0, len(self.tileList), 3):
            if self.tileList[tile].text() == self.tileList[tile + 1].text() and self.tileList[tile].text() ==self.tileList[tile + 2].text() and self.tileList[tile].text() != "": 
                self.win(tile, tile + 1, tile +2) 
                
    def win(self, tile1, tile2, tile3):
        """Takes the position of the winning tiles and highlights the winning tiles, changes the turn label to 
        announce the winner, and adds a tally to the counters"""
        self.winner = self.tileList[tile1].text()
        for tiles in self.tileList:
            tiles.setEnabled(False)
        self.tileList[tile1].setStyleSheet('color: red;')
        self.tileList[tile2].setStyleSheet('color: red;')
        self.tileList[tile3].setStyleSheet('color: red;')
        self.turnLabel.setText(f"{self.winner} WINS!")
        if self.winner == "X":
            self.xWin +=1
            self.xWinTally.setText(f"X's Wins: {self.xWin}")
        else:
            self.oWin +=1
            self.oWinTally.setText(f"O's Wins: {self.oWin}")
        
    
    def detectDraw(self):
        """after every move it detects if there is a draw, and if there is it adds to the draw tally"""
        draw = True
        for tile in self.tileList:
            if tile.text() == "":
                draw = False
                break
        if draw == True and self.turnLabel.text() != f"{self.winner} WINS!":
            self.Draws +=1
            self.turnLabel.setText(f"Draw!")
            self.drawTally.setText(f"Draws: {self.Draws}")
        

if __name__ in "__main__":
    import doctest
    doctest.testmod()
    app = QApplication()
    window = ticTacToe()
    window.show()
    app.exec()
