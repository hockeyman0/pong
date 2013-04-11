#! /usr/bin/env python



#
#$Author$
#$Date$
#$HeadURL$
#$Revision$
#



import sys
import os
import re
import math
import random
from Tkinter import *
from PongClasses import *
EndGame = 0
Start = 0
pause = 0
notpause = 1
notballspeed = [0,0]
ballspeed = [0,0]

		

#DEFINED FUNCTIONS######
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################



def handle_key_event(event):
	global EndGame
	global pause
	global Paddle1c
	global Paddle2c
	#print event.keysym
	
	if event.char == "w":
		Paddle1c.startmoveup()
	if event.char == "s":
		Paddle1c.startmovedown()
		
	if event.keysym == "Up":
		Paddle2c.startmoveup()
	if event.keysym == "Down":
			Paddle2c.startmovedown()
	if Start == 1:
		
		if event.char == "p":
			PauseGame()
	if event.keysym == "space":
		StartGame()
	if event.keysym == "Return":
		if EndGame == 1:
			RestartGame()

def FreezePaddles():
	global Paddle1c
	global Paddle2c
	Paddle1c.endmoveup()
	Paddle1c.endmovedown()
	Paddle2c.endmovedown()
	Paddle2c.endmoveup()
	
	
	
def handle_key_release_event(event):
	#print event.keysym
	global EndGame
	global Paddle1c
	global Paddle2c
	if event.char == "w":
		Paddle1c.endmoveup()
	if event.char == "s":
		Paddle1c.endmovedown()
		
	if event.keysym == "Up":
		Paddle2c.endmoveup()
	if event.keysym == "Down":
		Paddle2c.endmovedown()
			
		
		
def StartGame():
	global Start
	global Ballc
	global Starter
	if Start == 0:
		Start = 1
		global ballspeed
		global InitialBallSpeedX
		global InitialBallSpeedY
		Ballc.StartSpeed()
		if Starter == 0:
			Ballc.CSpeed[0] = abs(Ballc.CSpeed[0])
		else:
			Ballc.CSpeed[0] = -(abs(Ballc.CSpeed[0]))
		
		
def PauseGame():
	global pause
	global notpause
	temp = pause
	pause = notpause
	notpause = temp	
	
	Ballc.FlipSpeeds()
	
		
def movepaddle():
	global Paddle1c
	global Paddle2c
	global Start
	global Starter
	global pause
	global EndGame
	move1 = Paddle1c.moveup + Paddle1c.movedown
	move2 = Paddle2c.moveup + Paddle2c.movedown
	if EndGame == 0 and pause == 0:
		
		w.move(Paddle1, 0, move1)
		w.move(Paddle2, 0, move2)
	if Start == 0:
		if Starter == 0:
			w.move(Ball, 0, move1)
		else:
			w.move(Ball, 0, move2)
	Root.after(20, movepaddle)
		
		
		
	
def process_collision(Mover, Other):
	global Paddle1c
	global Paddle2c
	global Ballc
	global GameBoard

	if Mover == Ball:
		Ballc.ChangeSpeed()
		x = Ballc.CSpeed[0]
		y = Ballc.CSpeed[1]
		if Other == Paddle1:
		#print "Paddle"
			Ballc.CSpeed = [abs(x),y]
		if Other == Paddle2:
			Ballc.CSpeed = [-(abs(x)),y]
		if Other == WallTop:
			Ballc.CSpeed = [x,abs(y)]
		if Other == WallBottom:
			Ballc.CSpeed = [x,-(abs(y))]
			
			
		if Other == WallLeft or Other == WallRight:
			global pause
			global notpause
			global EndGame
			if EndGame == 0:
				if Other == WallLeft:
					print "Player 2 Wins!"
				else:
					print "Player 1 Wins!"
			pause = 1
			notpause = 1
			ballspeed = [0,0]
			Ballc.CSpeed = [0,0]
			EndGame = 1
			FreezePaddles()
			
	if Mover == Paddle1c.obj:
		if Other == WallTop:
			Paddle1c.moveup = 0
		if Other == WallBottom:
			Paddle1c.movedown = 0
	
	if Mover == Paddle2c.obj:
		if Other == GameBoard.WallTop:
			Paddle2c.moveup = 0
		if Other == GameBoard.WallBottom:
			Paddle2c.movedown = 0
		



def moveBall():
	global Ballc
	w.move(Ballc.obj, Ballc.CSpeed[0], Ballc.CSpeed[1])
	Root.after(20, moveBall)




def checkcollision():
	global Ballc
	global Paddle1c
	global Paddle2c
	global GameBoard
	#global GameBoard
	bbBall = w.bbox(Ballc.obj)
	bbPaddle1 = w.bbox(Paddle1c.obj)
	bbPaddle2 = w.bbox(Paddle2c.obj)
	#print "check"
	for objid in w.find_overlapping(bbBall[0], bbBall[1], bbBall[2], bbBall[3]):
		if objid != Ball: 
			#print "Contact"
			process_collision(Ballc.obj , objid)
	for objid in w.find_overlapping(bbPaddle1[0], bbPaddle1[1], bbPaddle1[2], bbPaddle1[3]):
		if objid != Paddle1c.obj and objid != GameBoard.WallLeft: 
			process_collision(Paddle1c.obj , objid)
				
	for objid in w.find_overlapping(bbPaddle2[0], bbPaddle2[1], bbPaddle2[2], bbPaddle2[3]):
		if objid != Paddle2c.obj and objid != GameBoard.WallRight: 
			process_collision(Paddle2c.obj , objid)
	Root.after(5, checkcollision)






def RestartGame():
	#print "Restarting Game"
	global Start
	global pause
	global notpause
	global EndGame
	global Paddle1c
	global Paddle2c
	global Ballc
	global Starter
	EndGame = 0
	Start = 0
	pause = 0
	notpause = 1
	Ballc.NCSpeed = [0,0]
	Ballc.CSpeed = [0,0]
	Starter = random.randint(0,1)
	Paddle1c.restartpos(w)
	Paddle2c.restartpos(w)
	Ballc.restartpos(w, Starter)
	
	
	
	
	
	
	
	##################################################################
	##################################################################
	##################################################################
	##################################################################
	##################################################################
	##################################################################
	##################################################################
	##################################################################
	##################################################################
	##################################################################











Cato = {}


argv = len(sys.argv)
if argv != 2:
	print "usage: Pong.py <config file>"
	sys.exit(1)
argo = sys.argv[1]

if (os.access(argo, os.R_OK) == 0):
	print"Error:",argo, "is not a readable."
	sys.exit(2)
		
InFile = open(argo, "r")
Arr = []
for line in InFile:
	arrr = []
	#print line
	
	line = line.split(":")
	Cato[line[0]] = int(line[1])
	Arr.append(int(line[1]))
	#print line
#print Arr
InitialBallSpeedX = Cato.get("InitialBallSpeedX")
#print InitialBallSpeedX
InitialBallSpeedY = Cato.get("InitialBallSpeedY")
PaddleSpeed = Cato.get("PaddleSpeed")
BallRadius = Cato.get("BallRadius")
CanvasWidth = Cato.get("CanvasWidth")
CanvasHeight = Cato.get("CanvasHeight")
MaxBallSpeed = Cato.get("MaxBallSpeed")
MinBallSpeed = Cato.get("MinBallSpeed")




Paddle1c = Paddlec(1,25,80,PaddleSpeed)
Paddle2c = Paddlec(2,25,80,PaddleSpeed)
Ballc = Ballc(InitialBallSpeedX, InitialBallSpeedY, BallRadius, MinBallSpeed, MaxBallSpeed)
Paddle1c.InputCoords(5, 35, 5+Paddle1c.width, 35+Paddle1c.height)
Paddle2c.InputCoords(CanvasWidth, CanvasHeight-50, CanvasWidth-Paddle2c.width, CanvasHeight-50-Paddle2c.height)
Starter = random.randint(0,1)

Root = Tk()









Restart_Button = Button(Root, text="Restart", command = RestartGame)#command=Print_Message)
Restart_Button.grid(row=0, column=0,columnspan =2, sticky = W)

Pause_Button = Button(Root, text="Pause", command=PauseGame)#command=Print_Message)
Pause_Button.grid(row=0, column=1, sticky = W)


Exit_Button = Button(Root, text="Exit", command=Root.quit)
Exit_Button.grid(row=0, column=4, sticky=E)


w = Canvas(Root, width=CanvasWidth, height=CanvasHeight) 
w.grid(row=1, column=0, columnspan=5, sticky = S)








WallLeft = w.create_line(5,0,5,CanvasHeight, fill="white")
WallRight = w.create_line(CanvasWidth,0,CanvasWidth,CanvasHeight, fill="white")
WallTop = w.create_line(0,5,CanvasWidth,5,fill="white")
WallBottom = w.create_line(0,CanvasHeight,CanvasWidth,CanvasHeight,fill="white")





GameBoard = Board(CanvasWidth, CanvasHeight, WallLeft, WallTop,WallRight,WallBottom)





Paddle1 = w.create_rectangle(Paddle1c.coords[0], Paddle1c.coords[1], Paddle1c.coords[2], Paddle1c.coords[3], fill="white")
Paddle2 = w.create_rectangle(Paddle2c.coords[0], Paddle2c.coords[1], Paddle2c.coords[2], Paddle2c.coords[3], fill="white")

Ball = w.create_oval(0,0,(2*Ballc.radius),(2*Ballc.radius), fill="white")
Ballc.InputObject(Ball)

Ballc.InputCoords([Paddle1c.coords[2]+2, Paddle1c.middle()-Ballc.radius, Paddle1c.coords[2]+(2*Ballc.radius)+2,Paddle1c.middle()+Ballc.radius],[Paddle2c.coords[2]-(2*Ballc.radius)-2,Paddle2c.middle()-Ballc.radius,Paddle2c.coords[2]-2,Paddle2c.middle()+Ballc.radius]) 


Ballc.restartpos(w, Starter)



Paddle1c.InputObject(Paddle1)
Paddle2c.InputObject(Paddle2)




bbBall = w.bbox(Ballc.obj)





Root.bind("<Key>", handle_key_event)
Root.bind("<KeyRelease>", handle_key_release_event)



Root.after(5, checkcollision)
Root.after(20, moveBall)
Root.after(20, movepaddle)
Root.mainloop()


#All Rights Reserved 2013
#Christohper Holly 
#Purdue University