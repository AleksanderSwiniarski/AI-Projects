import numpy as np
from graphics import *
import os

# Class of game state, logic and behaviour

class ticTacToe:
 
    # Initial game state: ' ' - Empty space

    state = np.array([[' ',' ',' '],
                      [' ',' ',' '],
                      [' ',' ',' ']])

    # Vector helping to decide the sequence of the moves

    currentPlayer = ['X', 'O']
  
    # Checking if the space is occupied
  
    def occupied(self, x, y):
        if self.state[x][y] == ' ':
            return False
        return True

    # Checking if the game has ended

    def checkResult(self):
    
        # Horizontal

        for i in range(0,3):
            if(self.state[0][i] == self.state[1][i] == self.state[2][i] and self.state[0][i] != ' '):
                result = self.state[0][i]
                return result

        # Vertical
        
        for i in range(0,3):
            if(self.state[i][0] == self.state[i][1] == self.state[i][2] and self.state[i][0] != ' '):
                result = self.state[i][0]
                return result

        # Right diagonal

        if(self.state[0][0] == self.state[1][1] == self.state[2][2] and self.state[0][0] != ' '):
            result = self.state[0][0]
            return result

        # Left diagonal
        
        if(self.state[0][2] == self.state[1][1] == self.state[2][0] and self.state[0][2] != ' '):
            result = self.state[0][2]
            return result

        # Going on game

        for i in range(0,3):
            for j in range(0,3):
                if(not self.occupied(i,j)):
                    result = False
                    return result

        # Tie

        result = 'Tie'
        return  result
    
    # miniMax algorithm with alfa-beta pruning returning the score and move coordinates

    def miniMaxAlfaBeta(self, isMax, alfa, beta):

        # Checking for terminal state, if so returning payoff value

        result = self.checkResult()
        # 0 are placeholders
        match result:
            case 'X':
                return (1,0,0)
            case 'O':
                return (-1,0,0)
            case 'Tie':
                return (0,0,0)
        

        if(isMax):
            bestMax = -np.Infinity
            for i in range(0,3):
                for j in range(0,3):
                    if not self.occupied(i,j):
                        self.state[i][j] = 'X'
                        (score, _, _) = self.miniMaxAlfaBeta(False, alfa, beta)

                        if score > bestMax:
                            bestMax = score
                            x = i
                            y = j
                        self.state[i][j] = ' '

                        if bestMax >= beta:
                            return (beta, x, y)
                            
                        if bestMax > alfa:
                            alfa = bestMax
                            
            return (alfa, x, y)

        else:
            bestMin = np.Infinity
            for i in range(0,3):
                for j in range(0,3):
                    if not self.occupied(i,j):
                        self.state[i][j] = 'O'
                        (score, _, _) = self.miniMaxAlfaBeta(True, alfa, beta)

                        if score < bestMin:
                            bestMin = score
                            x = i
                            y = j
                        self.state[i][j] = ' '

                        if bestMin <= alfa:
                            return (alfa, x, y)
                        if bestMin < beta:
                            beta = bestMin

            return (beta, x, y)

# Class of game window (Created using the graphics.py)

class gameBoard:

    # Initializing clean board

    board = GraphWin("Tic-Tac-Toe", 600, 800, autoflush=False)

    # Menu of choosing a symbol

    def chooseSymbol(self):

        txt = Text(Point(300, 250), "Choose Your symbol:")
        txt.setSize(36)
        txt.setFace('courier')
        txt.draw(self.board)

        squareO = Rectangle(Point(120,370),Point(280,530))     
        squareX = Rectangle(Point(320,370),Point(480,530))    
        squareO.setWidth(5)
        squareX.setWidth(5)
        squareO.draw(self.board)
        squareX.draw(self.board)
        self.drawX(0.5,1.75)
        self.drawO(1.5,1.75)

        while True:
            click = self.board.getMouse()
            if (120 < click.x < 280) & (370 < click.y < 530):
                return 'X'
            elif (320 < click.x < 480) and (370 < click.y < 530):
                return 'O'


    # Drawing clean board

    def initializeBoard(self):

        # Horizontal lines
        for i in range(1,3):
            ln = Line(Point(20,200*i), Point(580,200*i))
            ln.setWidth(5)
            ln.draw(self.board)  

        # Vertical lines
        for i in range(1,3):
            ln = Line(Point(200*i,20), Point(200*i,580))
            ln.setWidth(5)
            ln.draw(self.board)

    # Drawing X on the given board tile

    def drawX(self, x, y):
        cellCenterX = 100+200*x
        cellCenterY = 100+200*y
        offset = 60
        ln1 = Line(Point(cellCenterX-offset,cellCenterY-offset), Point(cellCenterX+offset,cellCenterY+offset))
        ln2 = Line(Point(cellCenterX-offset,cellCenterY+offset), Point(cellCenterX+offset,cellCenterY-offset))
        ln1.setWidth(5)
        ln2.setWidth(5)
        ln1.draw(self.board)
        ln2.draw(self.board)

    # Drawing O on the given board tile

    def drawO(self, x, y):
        ln1 = Circle(Point(100+200*x,100+200*y), 60)
        ln1.setWidth(5)
        ln1.draw(self.board)

    # Anouncing the result of the game

    def printResult(self, char):
        if char == 'Tie':
            txt = Text(Point(300,700), f"It's a {char}.")
        else:
            txt = Text(Point(300,700), f"{char} wins!")
        txt.setSize(36)
        txt.setFace('courier')
        txt.draw(self.board)

    # Obtaining the move location based on the user by the mouse click input

    def getMove(self, ticTacToe, player):
        click = self.board.getMouse()
        if click.y < 600:                                                   # Checking if click location is on the board
            for i in range(0,3):
                for j in range(0,3):                                        
                    cellCenterX = 100+200*i
                    cellCenterY = 100+200*j
                    if(cellCenterX-100 < click.x < cellCenterX+100 and cellCenterY-100 < click.y < cellCenterY+100):        # Checking which tile was chosen
                        if(not ticTacToe.occupied(i,j)):                                                                    # Checking if tile is occupied
                            ticTacToe.state[i][j] = ticTacToe.currentPlayer[player]                                         # Drawing the symbol of the user
                            if player == 0:
                                self.drawX(i,j)
                            else:
                                self.drawO(i,j)
                            return False
        return True
    
    # Clearing the game window

    def clear(self):
        for item in self.board.items[:]:
            item.undraw()
        self.board.update()

def main():
    
    window = gameBoard()

    # Symbol Choice

    playerSymbol = window.chooseSymbol()
    window.clear()

    # Game initialization

    window.initializeBoard()
    game = ticTacToe()
    symbol = 0
    firstTurn = True

    # Main game loop

    while True:

        # Player move

        if ticTacToe.currentPlayer[symbol] == playerSymbol:
            while window.getMove(game,int(symbol)):
                pass

        # AI move

        else:
            if playerSymbol == 'X':
                (_, i, j) = game.miniMaxAlfaBeta(False, -np.Infinity, np.Infinity)
                game.state[i][j] = 'O'
                window.drawO(i,j)
            else:
                # Randomizing first move of the AI (otherwise the game is repetitive)
                if firstTurn:
                    (i,j) = np.random.randint(0,2,2)
                else:
                    (_, i, j) = game.miniMaxAlfaBeta(True, -np.Infinity, np.Infinity)
                game.state[i][j] = 'X'
                window.drawX(i,j)           
                    
        # Checking if the game is finished

        result = game.checkResult()
        if result:
            window.printResult(result)
            break

        firstTurn = False
        symbol = not symbol

    # Closing window after the mouse click

    window.board.getMouse()
    window.board.close()

main()
os.system('pause')