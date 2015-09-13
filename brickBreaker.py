#!/usr/bin/python
# andrewID: kscharm
# author Kenny Scharm
# version 8/7/14
#------------------------
from random import randint
from Tkinter import *
import sys
import math

# initializes the game 
def init():
    canvas.data.emptyColor = "black"
    rows = canvas.data.rows
    cols = canvas.data.cols
    canvas.data.score = 0 
    canvas.data.xCoord = 0 
    canvas.data.yCoord = 0
   
    canvas.data.powerupx0 = 0
    canvas.data.powerupy0 = 0
    canvas.data.powerupx1 = 0
    canvas.data.powerupy1 = 0
    canvas.data.powerupdx = 0     # initial powerupx velocity
    canvas.data.powerupdy = 4     # initial powerupy velocity
    canvas.data.powerupInGame = False # boolean to test if a powerup is currently in the game
    canvas.data.hasSafetyBar = False
    canvas.data.currentLevel = 1 
    canvas.data.board = [[canvas.data.emptyColor for x in xrange(cols)] for x in xrange(rows)]
    canvas.data.board[0][1] = "blue"
    canvas.data.board[0] = ["blue" for x in xrange(cols)]
    canvas.data.board[3] = ["blue" for x in xrange(cols)]
    canvas.data.board[6] = ["blue" for x in xrange(cols)]
    canvas.data.csoordinates = []
    
    setup()   
    redrawAll()
    
def setup():
    canvas.data.ballx0 = 335		# initial left-most edge of ball
    canvas.data.bally0 = 452     # initial top-most edge of ball
    canvas.data.ballx1 = 345		# initial right-most edge of ball
    canvas.data.bally1 = 462       # initial bottom edge of the ball
    
    canvas.data.balldx = -6		# ballx velocity	
    canvas.data.balldy = -6	    # bally velocity
    canvas.data.paddleCenter = 340 # initial paddle cent
    canvas.data.leftMousePos = canvas.data.paddleCenter
    canvas.data.isGameOver = False  # boolean to test if the game is over 
    canvas.data.isPaused = True # boolean to test if the game is paused
    canvas.data.coordinates = []
    initializeCoordinates()
    canvas.data.photo = PhotoImage(file="C:\PythonPrograms\kscharm\gregkesden.gif")
    redrawAll()
    
# runs the game  
def run(rows, cols):
    root = Tk()
    global canvas
    canvas = Canvas(root, width = 650, height = 500)
    canvas.pack()
    root.resizable(width = 0, height = 0)
    class Struct: pass
    canvas.data = Struct()
    canvas.data.root = root
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.lives = 3

    init()
    drawGame()
    # Mouse-press bindings
    root.bind('<KeyPress>', keyPressed)
    root.bind('<Button-1>', leftMousePressed)
    canvas.bind('<B1-Motion>', leftMouseMoved)
    root.bind('<B1-ButtonRelease>', leftMouseReleased)
    timerFired()
    root.mainloop()    
# draws the images in the game
def drawGame():
    canvas.configure(background = "green")
    drawBoard()
    drawBall()
    drawPaddle()
    if(canvas.data.powerupInGame):
        drawPowerUp(canvas.data.yCoord, canvas.data.xCoord)
        if(canvas.data.powerupy1 > 500):
            canvas.data.powerupInGame = False
# redraws the window screen            
def redrawAll():
    canvas.delete(ALL)
    drawGame()
    drawScore()
    if(canvas.data.isGameOver):
        canvas.create_rectangle(0,0, 650, 500, fill = "green")
        canvas.create_text(325, 200, font = ("Times New Roman", 30), text = "You have " + str(canvas.data.lives) + " lives left")
        canvas.create_text(325, 300, font = ("Times New Roman", 20), text = "Press 'n' to continue")
        if(canvas.data.lives == 0):
            canvas.create_rectangle(0,0, 650, 500, fill = "white")
            canvas.create_text(325, 250, font = ("Times New Roman", 80), text = "GAME OVER")
            canvas.create_text(325, 350, font = ("Times New Roman", 40), text = "Score: " + str(canvas.data.score))
            canvas.create_text(325, 450, font = ("Times New Roman", 20), text = "Press 'e' to escape")
            for i in range(0, 6):
                canvas.create_image(85 + (i * 95),100, image = canvas.data.photo)
            
# draws the board            
def drawBoard():
    canvas.create_rectangle(20, 20, 630, 480, fill = "black")  
    for row in xrange(0, len(canvas.data.board)):
        for col in xrange(0, len(canvas.data.board[row])):
            color = canvas.data.board[row][col]
            drawCell(row, col, color)
    if canvas.data.hasSafetyBar:
        canvas.create_rectangle(20, 470, 630, 480, fill = "yellow")
# draws the score in the upper-left corner            
def drawScore():
    canvas.create_text(10, 10, anchor = W, font = ("Times New Roman", 16), text = "Score: " + str(canvas.data.score))
# draws each individual cell in the board of bricks   
def drawCell(row, col, color):
    # width: 50
    # height: 25
    canvas.create_rectangle(25 + (50 * col), 25 + (25 * row), 25 + (50 * (col + 1)), 25 + (25 * (row + 1)), fill = color)
    
# draws the end screen    
def levelFinishedScreen2():
    canvas.data.balldx = 0
    canvas.data.balldy = 0
    canvas.data.score += 50
    level2()
def levelFinishedScreen3():
    canvas.data.balldx = 0
    canvas.data.balldy = 0
    canvas.data.score += 150
    level3()
# draws the ball   
def drawBall():
	canvas.data.ball = canvas.create_oval(canvas.data.ballx0,canvas.data.bally0,canvas.data.ballx1,canvas.data.bally1,fill= "white")
# draws the paddle	
def drawPaddle():
    if canvas.data.leftMousePos < 52:
        canvas.data.leftMousePos = 52
    if canvas.data.leftMousePos > 598:
        canvas.data.leftMousePos = 598
    canvas.data.paddle = canvas.create_rectangle(canvas.data.leftMousePos - 32, 465,canvas.data.leftMousePos + 32, 480, fill = "red")  
# draws a power-up   
def drawPowerUp(row, col):
    canvas.data.star = canvas.create_rectangle(canvas.data.powerupx0, canvas.data.powerupy0, canvas.data.powerupx1, canvas.data.powerupy1, fill = "yellow")
# produces an array of coordinates representing the upper-left corner of each brick   
def initializeCoordinates():
    for row in xrange(0, len(canvas.data.board)):
        for col in xrange(0, len(canvas.data.board[row])): 
            canvas.data.coordinates.append([25 + (50 * col), 25 + (25 * row)]) 
# key presses             
def keyPressed(event):
    if(event.char == 's'):
        canvas.data.isPaused = False 
    if(event.char == 'e'):
        close_window(canvas.data.root)
        sys.exit()  
    if(event.char == 'n' and canvas.data.isGameOver):
        if(canvas.data.lives > 0):
            setup()
# creates level 2 and 3 by initializing different blocks
def level2():  
    setup()
    canvas.data.balldx -= 1
    canvas.data.balldy -= 1
    for row in xrange (canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if(col % 3 == 0):
               canvas.data.board[row][col] = "red"
    canvas.data.board[0] = ["red" for x in xrange(canvas.data.cols)]
    canvas.data.board[7] = ["red" for x in xrange(canvas.data.cols)]
    redrawAll()   
    
def level3():
    setup()
    canvas.data.balldx -= 1
    canvas.data.balldy -= 1
    for row in xrange (canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if(col % 3 == 0):
                canvas.data.board[row][col] = "red"
    canvas.data.board[2] = ["green" for x in xrange(canvas.data.cols)]
    canvas.data.board[3] = ["green" for x in xrange(canvas.data.cols)]    
    canvas.data.board[4] = ["blue" for x in xrange(canvas.data.cols)]    
    
# left mouse press
def leftMousePressed(event):
    canvas.data.leftMousePos = event.x
    
# left mouse move    
def leftMouseMoved(event):
    if(inBoundaries()):
        canvas.data.leftMousePos = event.x
        
# left mouse release        
def leftMouseReleased(event):
        canvas.data.leftMousPos = canvas.data.paddleCenter
        redrawAll()
        
# checks for collisions with the wall        
def collisionWithWall():
    if(canvas.data.isGameOver == True):
        return
    if canvas.data.bally1 >= 470 and canvas.data.hasSafetyBar:
        canvas.data.balldy *= -1
        canvas.data.hasSafetyBar = False
        
    if canvas.data.ballx1 >= 630:
        canvas.data.balldx *= -1 # changes the velocity of the ball
    if canvas.data.bally1 >= 480:
        canvas.data.lives -= 1
        canvas.data.isGameOver = True 
        canvas.data.balldx = 0
        canvas.data.balldy = 0        
    if canvas.data.ballx0 <= 20:
        canvas.data.balldx *= -1
    if canvas.data.bally0 <= 20:
        canvas.data.balldy *= -1
        
# checks to make sure the ball is within the boundaries 
def inBoundaries():
        if(canvas.data.leftMousePos >= 51 and canvas.data.leftMousePos <= 598):
            return True
        return False
        
# destroys a block when hit by the ball      
def destroyBlock(xCoord, yCoord, hitSide):
    xCoord -= 25
    xCoord /= 50
    yCoord -= 25
    yCoord /= 25
    rand = randint(0, 10) 
    # test for collisions with blue blocks
    if(canvas.data.board[yCoord][xCoord] == "blue"):
        canvas.data.board[yCoord][xCoord] = canvas.data.emptyColor
    elif(canvas.data.board[yCoord][xCoord] == "red"):
        canvas.data.board[yCoord][xCoord] = "blue"
    elif(canvas.data.board[yCoord][xCoord] == "green"):
        canvas.data.board[yCoord][xCoord] = "red"
    else:
        return
        
    if hitSide:
        canvas.data.balldx *= -1
    else:
        canvas.data.balldy *= -1
    canvas.data.score += 15
    if(rand > 9 and canvas.data.powerupInGame == False):
        canvas.data.powerupInGame = True
        canvas.data.xCoord = xCoord
        canvas.data.yCoord = yCoord
        canvas.data.powerupx0 = (xCoord * 50) + 25
        canvas.data.powerupx1 = (xCoord * 50) + 75
        canvas.data.powerupy0 = (yCoord * 25) + 25
        canvas.data.powerupy1 = (yCoord * 25) + 50
        drawPowerUp(xCoord, yCoord)
    if(levelComplete() and canvas.data.currentLevel == 1):
        levelFinishedScreen2()
        canvas.data.currentLevel += 1
    if(levelComplete() and canvas.data.currentLevel == 2):
        levelFinishedScreen3()
        
# checks for collisions with the paddle 
def collisionWithPaddle():
    # paddle width: 64
    # paddle height: 15
    if(canvas.data.bally1 > 460):
        xDiff = abs(canvas.data.leftMousePos - canvas.data.ballx1)
        if(xDiff < 32):
            if canvas.data.balldy > 0:
                if canvas.data.balldx < 0:
                    xDiff *= -1
                canvas.data.balldx += 5 * xDiff /32
                canvas.data.balldx /= 2
            canvas.data.balldy = abs(canvas.data.balldy) * -1
            
# checks for collisions with blocks            
def collisionWithBlock():
    for i in range(0, len(canvas.data.coordinates)):
        point = canvas.data.coordinates[i]
        if(canvas.data.bally1 < 460):
            xDiff = (canvas.data.ballx0 + canvas.data.ballx1) / 2 - (point[0] + 25)
            yDiff = (canvas.data.bally0 + canvas.data.bally1) / 2 - (point[1] + 12.5)
            if(abs(xDiff) < 25 and abs(yDiff) < 12.5):
                destroyBlock(point[0], point[1], abs(yDiff) < 8)
                
# checks for collisions with power-ups                 
def collisionWithPowerup():
    if(abs(canvas.data.powerupx1 - canvas.data.leftMousePos) < 32):
        if(canvas.data.powerupy1 > 450 and canvas.data.powerupInGame):
            canvas.data.score += 10
            addPowerup()
# adds a power-up to the game       
def addPowerup():
    canvas.data.hasSafetyBar = True
    canvas.data.powerupInGame = False
    
# checks to see if a level is completed    
def levelComplete():
    for row in xrange(0, len(canvas.data.board)):
        for col in xrange(0, len(canvas.data.board[row])):
            if(canvas.data.board[row][col] != canvas.data.emptyColor):
                return False            
    return True
    
# closes the window   
def close_window (root): 
    root.destroy()
    
def timerFired():
    if canvas.data.isPaused == False:
        canvas.data.ballx0 += canvas.data.balldx
        canvas.data.bally0 += canvas.data.balldy
        canvas.data.ballx1 += canvas.data.balldx
        canvas.data.bally1 += canvas.data.balldy
        canvas.data.powerupx0 += canvas.data.powerupdx
        canvas.data.powerupx1 += canvas.data.powerupdx
        canvas.data.powerupy0 += canvas.data.powerupdy
        canvas.data.powerupy1 += canvas.data.powerupdy
        collisionWithWall()	
        collisionWithPaddle()
        collisionWithBlock()       
        collisionWithPowerup()
    redrawAll()
    delay = 20 
    canvas.after(delay, timerFired)
 
run(8, 12)   