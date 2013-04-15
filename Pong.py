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
import time
import commands
import string
from Tkinter import *
from PongClasses import *
import tkFileDialog
import tkSimpleDialog

GamePositions = []
EndGame = 0
Start = 0
pause = 0
notpause = 1
notballspeed = [0,0]
ballspeed = [0,0]
Score1 = 0
Score2 = 0
ReplayOn = 0
P1Replay = []
P2Replay = []
BReplay = []
counter = 0
Ncounter = 0
File_Name = ""


#DEFINED FUNCTIONS######
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################


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
	Root.after(20, checkcollision)





def FreezePaddles():
	global Paddle1c
	global Paddle2c
	Paddle1c.endmoveup()
	Paddle1c.endmovedown()
	Paddle2c.endmovedown()
	Paddle2c.endmoveup()
	
	
	
def GameModeSelection():
	global Game	
	
	
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

def Handle_List_Extraction(event):
	global File_Name
	Index = Top.Selection_List.curselection()
	File_Name = Top.Selection_List.get(Index)
	Top.destroy()



def LoadGame():
	global File_Name
	global Paddle1c
	global Paddle2c
	global Ballc
	global ReplayOn
	global P1Replay
	global P2Replay
	global BReplay
	global counter
	global Ncounter
	Select_A_File()
	InFile = open(File_Name, "r")
	for line in InFile:
		#print line
		line = line.split(":")
		PaddlePos1 = line[0]
		PaddlePos2 = line[1]
		BallPos = line[2]
		
		PaddlePos1 = PaddlePos1.split(",")
		PaddlePos2 = PaddlePos2.split(",")
		BallPos = BallPos.split(",")
		#print "loop"
		#print PaddlePos1
		P1Replay.append(PaddlePos1)
		P2Replay.append(PaddlePos2)
		BReplay.append(BallPos)
		#w.coords(Paddle1c.obj, int(PaddlePos1[0]),int(PaddlePos1[1]),int(PaddlePos1[2]),int(PaddlePos1[3]))
		#w.coords(Paddle2c.obj, PaddlePos2[0],PaddlePos2[1],PaddlePos2[2],PaddlePos2[3])
		#w.coords(Ballc.obj, BallPos[0],BallPos[1],BallPos[2],BallPos[3])
		#time.sleep(0.2)
	EndGame = 1
	Ncounter = len(P1Replay)
	#print Ncounter
	Root.after(20, ReplayGame)
	conuter = 0
	time.sleep(1)
	RestartGame()

def ReplayGame():
	global EndGame
	global P1Replay
	global P2Replay
	global BReplay
	global counter
	global Ncounter
	global Paddlec1
	global Paddlec2
	global Ballc
	EndGame = 1
	i = counter
	w.coords(Paddle1c.obj, int(P1Replay[i][0]),int(P1Replay[i][1]),int(P1Replay[i][2]),int(P1Replay[i][3]))
	w.coords(Paddle2c.obj, P2Replay[i][0],P2Replay[i][1],P2Replay[i][2],P2Replay[i][3])
	w.coords(Ballc.obj, BReplay[i][0],BReplay[i][1],BReplay[i][2],BReplay[i][3])
	
	counter = counter +1
	
	#print Ncounter
	if counter < Ncounter:
		#pass
		#print "OH?"
		Root.after(20, ReplayGame)
	



	

		

def moveBall():
	global Ballc
	w.move(Ballc.obj, Ballc.CSpeed[0], Ballc.CSpeed[1])
	Root.after(20, moveBall)

		
			
		
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
		
		
		
			
				
		
def PauseGame():
	global pause
	global notpause
	temp = pause
	pause = notpause
	notpause = temp	
	
	Ballc.FlipSpeeds()
	
	
	

def process_collision(Mover, Other):
	global Paddle1c
	global Paddle2c
	global Ballc
	global GameBoard
	global GamePositions

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
			global GameBoard
			if EndGame == 0:
				localtime = time.localtime(time.time())
				#print localtime
				#print GamePositions
				if Other == WallLeft:
					#ScoreBoard[1] = ScoreBoard[1] + 1
					GameBoard.UpdateScore(1)
					print "Player 2 Wins! Press Enter to Restart."
				else:
					#ScoreBoard[0] = ScoreBoard[0] + 1
					GameBoard.UpdateScore(0)
					print "Player 1 Wins! Press Enter to Restart."
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
		

def RecordPositions():
	global Start
	global EndGame
	global GamePositions
	global Paddle1c
	global Paddle2c
	global Ballc
	
	if Start == 1 and EndGame == 0:
		
		CurrentPositions = ""
		part = []
	
		bbox = w.bbox(Paddle1c.obj)
		part.append(bbox)
		bbox = w.bbox(Paddle2c.obj)
		part.append(bbox)
		bbox = w.bbox(Ballc.obj)
		part.append(bbox)
		for tempbbox in part:
			CurrentPositions += "%d,%d,%d,%d:" % (tempbbox[0], tempbbox[1], tempbbox[2], tempbbox[3])
		GamePositions.append(CurrentPositions)
	Root.after(20, RecordPositions)





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
	global GamePositions
	
	GamePositions = []
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
	
	
def SaveGame():
	global EndGame
	global GamePositions
	if EndGame == 1:
		savetime = time.localtime(time.time())
		default = ""
		default += "Saved Game "
		default += str(savetime[0])
		default += "-"
		default += str(savetime[1])
		default += "-"
		default += str(savetime[2])
		default += " at "
		default += str(savetime[3])
		default += "."
		default += str(savetime[4])
		default += "."
		default += str(savetime[5])
		default += "."
		default += str(savetime[6])
	
		filename = tkSimpleDialog.askstring("Text Input Box","Name for file? (default date/time)")
		if filename == "" :
			filename = default
		filename += ".save"
		OutFile = open(filename, "w+")
		for snapshot in GamePositions:
			OutFile.write(snapshot)
			OutFile.write("\n")
	else:
		print "Wait until the end of a game to save replay!"


			
def Select_A_File():
	global Top
	Top = Toplevel()
	HS_Bar = Scrollbar(Top, orient=HORIZONTAL)
	HS_Bar.pack(side=BOTTOM, fill=X)

	VS_Bar = Scrollbar(Top)
	VS_Bar.pack(side=RIGHT, fill=Y)

	List = Listbox(Top, relief=SUNKEN,font=("Helvetica", 20),fg="Black", bg="White",selectforeground="White",selectbackground="Blue",cursor="arrow", yscrollcommand=VS_Bar.set, xscrollcommand=HS_Bar.set)

	HS_Bar.config(command=List.xview)
	VS_Bar.config(command=List.yview)
	List.pack(side=LEFT, expand=YES, fill=BOTH)

	Entries=commands.getoutput("ls *.save")
	Entries=string.split(Entries,"\n")
	for Item in Entries:
		List.insert(END, Item)
	Top.Selection_List = List
	List.bind("<Double-1>", Handle_List_Extraction)

	Top.focus_set()
	Top.grab_set()
	Top.wait_window()
	print File_Name 

	
	
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




#localtime = time.localtime(time.time())
#print "Local current time:", localtime
#print localtime[1]






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




#testvar = StringVar()
#testvar.set(str(Starter))






Restart_Button = Button(Root, text="Restart", command = RestartGame)#command=Print_Message)
Restart_Button.grid(row=0, column=1)

Pause_Button = Button(Root, text="Pause", command=PauseGame)#command=Print_Message)
Pause_Button.grid(row=0, column=2, sticky = W)


Exit_Button = Button(Root, text="Exit", command=Root.quit)
Exit_Button.grid(row=0, column=3, sticky=E)

Save_Button = Button(Root, text="Save Recording", command=SaveGame)
Save_Button.grid(row=3, column=3)

Load_Button = Button(Root, text="Load Recording", command=LoadGame)
Load_Button.grid(row=3, column = 2)

Mode_Button = Button(Root, text="Player vs. Player")
Mode_Button.grid(row=3, column = 0)

w = Canvas(Root, width=CanvasWidth, height=CanvasHeight) 
w.grid(row=1, column=0, columnspan=5, sticky = S)












WallLeft = w.create_line(5,0,5,CanvasHeight, fill="white")
WallRight = w.create_line(CanvasWidth,0,CanvasWidth,CanvasHeight, fill="white")
WallTop = w.create_line(0,5,CanvasWidth,5,fill="white")
WallBottom = w.create_line(0,CanvasHeight,CanvasWidth,CanvasHeight,fill="white")


GameBoard = Board(CanvasWidth, CanvasHeight, WallLeft, WallTop,WallRight,WallBottom)



#PLAYER SCORE BOARD DISPLAY NEEDS TO BE AFTER BOARD INITIALIZATION
Player1_Score = Label(Root, textvariable= GameBoard.Score1String)
Player1_Score.grid(row=0, column=0, sticky = W)
Player2_Score = Label(Root, textvariable = GameBoard.Score2String)
Player2_Score.grid(row=0, column=4, sticky = E)











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



Root.after(20, checkcollision)
Root.after(20, moveBall)
Root.after(20, movepaddle)
Root.after(20, RecordPositions)
Root.mainloop()



#CHECK LIST
#Scoreboard updates-check
#move pause button-
#move exit button
#move restart button
#Add Game Mode toggle button
#Add player vs player/cpu button
#add load recording button -check 
#add save recording button -check
# Game Records every action in a game - Check
# Game loads a game -check
# Game Saves every action in a game to a file - check












#All Rights Reserved 2013
#Christohper Holly 
#Purdue University