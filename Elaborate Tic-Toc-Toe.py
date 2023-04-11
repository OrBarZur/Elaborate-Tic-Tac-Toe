import turtle

class GUI:
    def __init__(self):
        self.don = turtle.Turtle()
        self.don.hideturtle()
        self.normal()
    
    def drawBoard(self, n, x, y, size):
        self.don.speed(0)
        for c in range(x, x + size + size / (n * 2), size / n):
            self.drawLine(c, y, c, y - size)
        for r in range(y, y - size - size / (n * 2), -size / n):
            self.drawLine(x, r, x + size, r)

    def drawLine(self, startX, startY, endX, endY):
        self.don.penup()
        self.don.goto(startX, startY)
        self.don.pendown()
        self.don.goto(endX, endY)
        
    def drawO(self, x, y, size):
        self.don.speed(12)
        self.don.penup()
        self.don.goto(x + size / 2, y - 3 * size / 4)
        self.don.pendown()
        self.don.circle(size / 4)
        
    def drawX(self, x, y, size):
        self.don.speed(10)
        self.drawLine(x + size / 4, y - size / 4, x + 3 * size / 4, y - 3 * size / 4)
        self.drawLine(x + 3 * size / 4, y - size / 4, x + size / 4, y - 3 * size / 4)

    def bold(self):
        self.don.color("#c69f5b")
        self.don.pensize(10)
        
    def normal(self):
        self.don.color("blue")
        self.don.pensize(1)
               
class Board:
    playerX = 1
    playerO = -1
    draw = 2
    ongoing = 0
    gameOver = 3
    invalid = 4
    check = 7

    def __init__(self, n, x, y, size, clickable):
        self.n = n
        self.x = x
        self.y = y
        self.size = size
        self.clickable = clickable

        self.done = False
        self.count = 0
        self.board = [[0 for j in range(self.n)] for i in range(self.n)]

        self.msg_errAlreadyPlayed = "Already played, try again"
        self.msg_errBadMove = "Bad move, try again"

        self.gui = GUI()

        self.drawBoard()

    def start(self):
        if self.clickable:
            turtle.onscreenclick(self.onClick)
        turtle.mainloop()
        
    def errBadMove(self):
        if self.msg_errBadMove != "":
            print (self.msg_errBadMove)
            
    def errAlreadyPlayed(self):
        if self.msg_errAlreadyPlayed != "":
            print (self.msg_errAlreadyPlayed)

    def printBoard(self):
        print ("Board:")
        for i in range(self.n):
            print (self.board[i])
        
    def play(self, player, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n or (player != self.playerX and player != self.playerO):
            self.errBadMove()
            return False
        elif self.board[i][j] != 0:
            self.errAlreadyPlayed()
            return False
        else:
            self.board[i][j] = player
            self.count += 1
            self.drawTurn(player, i, j)
            return True

    def turn(self, player, mX, mY):
        if not self.canPlay():
            return self.gameOver
        elif self.play(player, self.getI(mY), self.getJ(mX)):
            return self.checkResult()
        else:
            return self.invalid
    
    def getI(self, mY):
         return (int(mY) - self.y) / -(self.size / self.n)
    
    def getJ(self, mX):
        return (int(mX) - self.x) / (self.size / self.n)

    def drawTurn(self, player, i, j):
        if player == self.playerX:
            self.gui.drawX(self.x + j * self.size / self.n, self.y - i * self.size / self.n, self.size / self.n)
        elif player == self.playerO:
            self.gui.drawO(self.x + j * self.size / self.n, self.y - i * self.size / self.n, self.size / self.n)
    
    def checkPlayerWin(self, player):
        cells = []
        #Rows
        for i in range(self.n):
            if sum(self.board[i]) == self.n * player:
                cells = [(i, j) for j in range(self.n)]
        #Columns
        for j in range(self.n):
            if sum([self.board[i][j] for i in range(self.n)]) == self.n * player:
                cells = [(i, j) for i in range(self.n)]
        #Main diagonal
        if sum([self.board[i][i] for i in range(self.n)]) == self.n * player:
                cells = [(i, i) for i in range(self.n)]
        #Secondary diagonal
        if sum([self.board[i][self.n - i - 1] for i in range(self.n)]) == self.n * player:
                cells = [(i, self.n - i - 1) for i in range(self.n)]

        self.gui.bold()
        for cell in cells:
            self.drawTurn(player, cell[0], cell[1])
        self.gui.normal()
        
        return len(cells) > 0

    def checkResult(self):
        if self.checkPlayerWin(self.playerX):
            self.done = True
            return self.playerX
        elif self.checkPlayerWin(self.playerO):
            self.done = True
            return self.playerO
        elif not self.canPlay():
            self.done = True
            return self.draw
        else:
            return self.ongoing
    
    def canPlay(self):
        return not self.done and self.count < self.n ** 2

    def onClick(self, mX, mY):
        turtle.onscreenclick(None)
        self.turn(-2 * (self.count % 2) + 1, mX, mY)
        turtle.onscreenclick(self.onClick)

    def drawBoard(self):
        self.gui.drawBoard(self.n, self.x, self.y, self.size)

class UltimateBoard(Board):
    def __init__(self, n, x, y, size, clickable):
        Board.__init__(self, n, x, y, size, clickable)

        self.highlight_gui = GUI()
        
        self.boards = [[Board(n, self.x + j * self.size / self.n + 5 * self.size / (self.n * 100), self.y - i * self.size / self.n - 5 * self.size / (self.n * 100), (90 * self.size) / (100 * n) ,False) for j in range(self.n)] for i in range(self.n)]
        self.curPlayer = self.playerX
        self.curI = -1
        self.curJ = -1

    def drawCell(self, n, x, y, size, i, j):
        self.highlight_gui.don.ht()
        self.highlight_gui.don.speed(0)
        self.highlight_gui.don.color("red")
        self.highlight_gui.don.pensize(3)
        self.highlight_gui.drawLine(x + j * (size / n), y - i * (size / n), x + (j + 1) * (size / n), y - i * (size / n))
        self.highlight_gui.drawLine(x + (j + 1) * (size / n), y - i * (size / n), x + (j + 1) * (size / n), y - (i + 1) * (size / n))
        self.highlight_gui.drawLine(x + (j + 1) * (size / n), y - (i + 1) * (size / n), x + (j) * (size / n), y - (i + 1) * (size / n))
        self.highlight_gui.drawLine(x + (j) * (size / n), y - (i + 1) * (size / n), x + (j) * (size / n), y - (i) * (size / n))
        self.highlight_gui.normal()
        
    def drawBigCell(self, x, y, size):
        self.highlight_gui.don.ht()
        self.highlight_gui.don.speed(0)
        self.highlight_gui.don.color("red")
        self.highlight_gui.don.pensize(3)
        self.highlight_gui.drawLine(x, y, x + size, y)
        self.highlight_gui.drawLine(x + size, y, x + size, y - size)
        self.highlight_gui.drawLine(x + size, y - size, x, y - size)
        self.highlight_gui.drawLine(x, y - size, x, y)
        self.highlight_gui.normal()
        
    def clearCell(self):
        for i in range(16):
            self.highlight_gui.don.undo()
        self.highlight_gui.normal()
            
    def onClick(self, mX, mY):
        turtle.onscreenclick(None)
        self.turn(self.curPlayer, mX, mY)
        turtle.onscreenclick(self.onClick)

    def turn(self, player, mX, mY):
        if not self.canPlay():
            return self.gameOver
        curI = self.getI(mY)
        curJ = self.getJ(mX)
        if (self.curI > -1 or self.curJ > -1) and (self.curI != curI or self.curJ != curJ):
            self.errBadMove()
            return self.invalid
        else:
            curBoard = self.boards[curI][curJ]
            res = curBoard.turn(player, mX, mY)
        if res == self.playerX or res == self.playerO or res == self.draw or res == self.ongoing:
            self.curI = curBoard.getI(mY)
            self.curJ = curBoard.getJ(mX)
            self.clearCell()
            if self.boards[self.curI][self.curJ].canPlay():
                self.drawCell(self.n, self.x, self.y, self.size, self.curI, self.curJ)
            else:
                self.drawBigCell(self.x, self.y, self.size)
                self.curI = -1
                self.curJ = -1
            self.curPlayer *= -1
            if res == self.playerX or res == self.playerO:
                self.play(res, self.getI(mY), self.getJ(mX))
                return self.checkResult()
            else:
                return self.ongoing
        else:
            return self.invalid


while True:
    Type = int(input("Which game do you want (1 - Ultimate / 2 - Regular)? "))
    if Type == 1:
        Size = int(input("Which size do you want it to be (2 or 3 or 4)? "))
        if Size >= 2 or Size <= 4:
            b = UltimateBoard(Size, -300, 300, 600, True)
            b.start()
        else:
            print ('Sorry, it is impossible')
    elif Type == 2:
        Size = int(input("Which size do you want it to be (2 or 3 or 4 or 5)? "))
        if Size >= 2 or Size <= 5:
            b = Board(Size, -300, 300, 600, True)
            b.start()
        else:
            print ('Sorry, it is impossible')
    else:
        print ('Sorry, it is impossible')
