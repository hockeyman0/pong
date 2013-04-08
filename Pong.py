#! /usr/bin/env python


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


def handle_key_event(event):
	print event.keysym
	if re.match(r"[ws]", event.keysym):
		Root.after(20, movepaddle(1,event.keysym))
	elif re.match(r"[(Up)(Down)]", event.keysym):
		Root.after(20, movepaddle(2,event.keysym))
	if event.char == "p":
		PauseGame()
	if event.keysym == "space":
		StartGame()
			
		
		
def StartGame():
	global Start
	if Start == 0:
		Start = 1
		global ballspeed
		global InitialBallSpeedX
		global InitialBallSpeedY
		ballspeed = [InitialBallSpeedX, InitialBallSpeedY]
		
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
	print pause	
	
		
def movepaddle(paddleNum, direction):
	global Start
	if direction == "w" and pause == 0:
		w.move(Paddle1, 0, -10)
		if Start == 0:
			w.move(Ball, 0, -10)
	if direction == "s" and pause == 0:
		w.move(Paddle1, 0, 10)
		if Start ==0:
			w.move(Ball, 0, 10)
	if direction == "Up" and pause == 0:
		w.move(Paddle2, 0, -10)
	if direction == "Down" and pause == 0:
		w.move(Paddle2, 0, 10)
		
	
def process_collision(Ball, Other):
	global ballspeed
	x = ballspeed[0]
	y = ballspeed[1]
	
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
		pause = 1
		notpause = 1
		ballspeed = [0,0]
		EndGame = 1
		
		



def moveBall():
	print ballspeed
	w.move(Ball, ballspeed[0],ballspeed[1])
	Root.after(20, moveBall)




def checkcollision():
	bbBall = w.bbox(Ball)
	for objid in w.find_overlapping(bbBall[0], bbBall[1], bbBall[2], bbBall[3]):
		if objid != Ball: 
			process_collision(Ball , objid)
	Root.after(5, checkcollision)


def RestartGame():
	global Start
	global pause
	global notpause
	global EndGame
	global notballspeed
	global ballspeed
	global Ball
	global Paddle1
	global Paddle2
	
	EndGame = 0
	Start = 0
	pause = 0
	notpause = 1
	notballspeed = [0,0]
	ballspeed = [0,0]
	w.coords(Paddle1, 5, 35, 30, 115)
	w.coords(Paddle2, CanvasWidth,CanvasHeight-165, CanvasWidth-25, CanvasHeight-85)
	w.coords(Ball, 30+1+1,(35+115)/2-10+1,30+20+1,(35+115)/2+10+1)
	
	
	











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
	print line
	line = line.split(":")
	Arr.append(int(line[1]))
	#print line
print Arr
InitialBallSpeedX = int(Arr[0])
print InitialBallSpeedX
InitialBallSpeedY = int(Arr[1])
PaddleSpeed = int(Arr[2])
BallRadius = int(Arr[3])
CanvasWidth = int(Arr[4])
CanvasHeight = int(Arr[5])
MaxBallSpeed = int(Arr[6])
MinBallSpeed = int(Arr[7])

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



Paddle1 = w.create_rectangle(5, 35, 30, 115, fill="white")
Paddle2 = w.create_rectangle(500, 35+300, 475, 115+300, fill="white")

bbPaddle1 = w.bbox(Paddle1)
bbPaddle2 = w.bbox(Paddle2)


Ball = w.create_oval(30+1+1,(35+115)/2-10+1,30+20+1,(35+115)/2+10+1, fill="white")
bbBall = w.bbox(Ball)




Root.bind("<Key>", handle_key_event)



Root.after(5, checkcollision)
Root.after(20, moveBall)
Root.mainloop()


#All Rights Reserved 2013
#Christohper Holly 
#Purdue University