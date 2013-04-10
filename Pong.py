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
from Tkinter import *

EndGame = 0
Start = 0
pause = 0
notpause = 1
notballspeed = [0,0]
ballspeed = [0,0]


class Ballc:
	def __init__(self, ISpeedX, ISpeedY, radius):
		self.ISpeed = [ISpeedX, ISpeedY]
		self.radius = radius
		self.CSpeed = [0,0]
		self.NCSpeed = [0,0]
		
		
	def getISpeed(self):
		return self.ISpeed
		
	def getRadius(self):
		return self.radius
		
	def IncreaseSpeed(self):
		pass
		
	def InputObject(self, obj):
		self.obj = obj
	def StartSpeed(self):
		self.CSpeed[0] = self.ISpeed[0]
		self.CSpeed[1] = self.ISpeed[1]
		
		
class Paddlec:
	def __init__(self, paddlenum, paddlewidth, paddleheight, paddlespeed):
		self.paddlenum = paddlenum
		self.paddleheight = paddleheight
		self.paddlewidth = paddlewidth
		self.paddlespeed = paddlespeed
		self.moveup = 0
		self.movedown = 0
	def startmoveup(self):
		self.moveup = -(self.paddlespeed)
		#print self.moveup
	def startmovedown(self):
		self.movedown = (self.paddlespeed)
		#print self.movedown
	def endmoveup(self):
		self.moveup = 0
		#print self.moveup
	def endmovedown(self):
		self.movedown = 0
		#print self.movedown
	def InputObject(self, obj):
		self.obj = obj
	
		


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
		
		
	if event.char == "p":
		PauseGame()
	if event.keysym == "space":
		StartGame()
	if event.keysym == "Return":
		if EndGame == 1:
			RestartGame()
			
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
	pass
			
		
		
def StartGame():
	global Start
	global Ballc
	if Start == 0:
		Start = 1
		global ballspeed
		global InitialBallSpeedX
		global InitialBallSpeedY
		ballspeed = [InitialBallSpeedX, InitialBallSpeedY]
		Ballc.StartSpeed()
		
		
def PauseGame():
	global pause
	global notpause
	global ballspeed
	global notballspeed
	temp = pause
	pause = notpause
	notpause = temp
	temp = ballspeed[0]
	ballspeed[0] = notballspeed[0]
	notballspeed[0] = temp
	temp = ballspeed[1]
	ballspeed[1] = notballspeed[1]
	notballspeed[1] = temp
	#print pause	
	
		
def movepaddle():
	global Paddle1c
	global Paddle2c
	global Start
	move1 = Paddle1c.moveup + Paddle1c.movedown
	move2 = Paddle2c.moveup + Paddle2c.movedown
	w.move(Paddle1, 0, move1)
	w.move(Paddle2, 0, move2)
	Root.after(20, movepaddle)
	if Start == 0:
		w.move(Ball, 0, move1)
		
		
		
		
	
def process_collision(Mover, Other):
	global ballspeed
	global Paddle1c
	global Paddle2c
	global Ballc
	x = ballspeed[0]
	y = ballspeed[1]
	
	if Mover == Ball:
			
		if Other == Paddle1:
		#print "Paddle"
			ballspeed = [abs(x),y]
		if Other == Paddle2:
			ballspeed = [-(abs(x)),y]
		if Other == WallTop:
			ballspeed = [x,abs(y)]
		if Other == WallBottom:
			ballspeed = [x, -(abs(y))]
		if Other == WallLeft or Other == WallRight:
			global pause
			global notpause
			global EndGame
			if EndGame == 0:
				if Other ==WallLeft:
					print "Player 2 Wins!"
				else:
					print "Player 1 Wins!"
			pause = 1
			notpause = 1
			ballspeed = [0,0]
			EndGame = 1
			
	if Mover == Paddle1:
		if Other == WallTop:
			Paddle1c.moveup = 0
		



def moveBall():
	global Ballc
	#print ballspeed
	w.move(Ballc.obj, ballspeed[0],ballspeed[1])
	Root.after(20, moveBall)




def checkcollision():
	global Ballc
	global Paddle1c
	global Paddle2c
	bbBall = w.bbox(Ball)
	for objid in w.find_overlapping(bbBall[0], bbBall[1], bbBall[2], bbBall[3]):
		if objid != Ball: 
			process_collision(Ball , objid)
	Root.after(5, checkcollision)


def RestartGame():
	#print "Restarting Game"
	global Start
	global pause
	global notpause
	global EndGame
	global notballspeed
	global ballspeed
	global Ball
	global Paddle1
	global Paddle2
	global centerofpaddle
	EndGame = 0
	Start = 0
	pause = 0
	notpause = 1
	notballspeed = [0,0]
	ballspeed = [0,0]
	w.coords(Paddle1, 5, 35, 30, 115)
	w.coords(Paddle2c.obj,CanvasWidth, CanvasHeight-50, CanvasWidth-Paddle2c.paddlewidth, CanvasHeight-50-Paddle2c.paddleheight)
	#w.coords(Ballc.obj, 30+1+1,(35+115)/2-10+1,30+20+1,(35+115)/2+10+1)
	w.coords(Ballc.obj, 6+Paddle1c.paddlewidth,centerofpaddle-Ballc.radius,6+Paddle1c.paddlewidth+(2*Ballc.radius),centerofpaddle+Ballc.radius)
	
	
	
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
Ballc = Ballc(InitialBallSpeedX, InitialBallSpeedY, BallRadius)




Root = Tk()









# MOST OF THIS WILL BE PUT INTO THE CONFIGURATION FILE



Restart_Button = Button(Root, text="Restart", command = RestartGame )#command=Print_Message)
Restart_Button.grid(row=0, column=0,columnspan =2, sticky = W)

Pause_Button = Button(Root, text="Pause", command=PauseGame )#command=Print_Message)
Pause_Button.grid(row=0, column=1, sticky = W)


Exit_Button = Button(Root, text="Exit", command=Root.quit)
Exit_Button.grid(row=0, column=4, sticky=E)


w = Canvas(Root, width=CanvasWidth, height=CanvasHeight) 



w.grid(row=1, column=0, columnspan=5, sticky = S)


WallLeft = w.create_line(5,0,5,CanvasHeight, fill="white")
WallRight = w.create_line(CanvasWidth,0,CanvasWidth,CanvasHeight, fill="white")
WallTop = w.create_line(0,5,CanvasWidth,5,fill="white")
WallBottom = w.create_line(0,CanvasHeight,CanvasWidth,CanvasHeight,fill="white")



Paddle1 = w.create_rectangle(5, 35, 5+Paddle1c.paddlewidth, 35+Paddle1c.paddleheight, fill="white")
Paddle2 = w.create_rectangle(CanvasWidth, CanvasHeight-50, CanvasWidth-Paddle2c.paddlewidth, CanvasHeight-50-Paddle2c.paddleheight, fill="white")



centerofpaddle = (35+35+Paddle1c.paddleheight)/2
Ball = w.create_oval(6+Paddle1c.paddlewidth,centerofpaddle-Ballc.radius,6+Paddle1c.paddlewidth+(2*Ballc.radius),centerofpaddle+Ballc.radius, fill="white")



Ballc.InputObject(Ball)
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