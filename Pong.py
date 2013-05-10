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
Score1 = 0
Score2 = 0
ReplayOn = 0
P1Replay = []
P2Replay = []
BReplay = []
counter = 0
Ncounter = 0
File_Name = ""
PlayerMode = 0
AILocate = 0	
AIMoving = "Stop"	
ReactionTime = 10
ReactionTimeCounter = 0	
GameStarted = 0 	
TimeCounter = 0
ReleaseCounter = 0
GameModeLast = 0
trigger = 0
PlayerModeLast = 0
Pwidth = 25
GameMode = 0	
PaddleTrigger = 0
P1Prev = [0,0,0,0]
AIHardMoving = "Stop"
DoubleCheck = 0 
FirstCheck = 0
Space = 0	
GameParam = GameParameters()


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
	bbiBall = w.bbox(iBallc.obj)
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
	for objid in w.find_overlapping(bbiBall[0], bbiBall[1], bbiBall[2], bbiBall[3]):
			if objid != InvisaBall: 
				#print "Contact"
				process_collision(iBallc.obj , objid)

	Root.after(20, checkcollision)





def FreezePaddles():
	global Paddle1c
	global Paddle2c
	Paddle1c.endmoveup()
	Paddle1c.endmovedown()
	Paddle2c.endmovedown()
	Paddle2c.endmoveup()


def GameModeSelection():
	global GameMode
	if Start == 0 or EndGame ==1:
		if Mode_Button["text"] == "Unlimited Play":
			GameMode = 1
			#print "yep"
			Mode_Button["text"] = "Timed Play"
		elif Mode_Button["text"] == "Timed Play":
			GameMode = 2
			Mode_Button["text"] = "Scored Play"
		elif Mode_Button["text"] == "Scored Play":
			GameMode = 0
			Mode_Button["text"] = "Unlimited Play"


	
	
def PlayerModeSelection():
	global PlayerMode
	if Start == 0 or EndGame ==1:
		if Player_Button["text"] == "Player vs. Player":
			PlayerMode = 1
		#print "yep"
			Player_Button["text"] = "Player vs. Easy CPU"
		elif Player_Button["text"] == "Player vs. Easy CPU":
			PlayerMode = 2
			Player_Button["text"] = "Player vs. Hard CPU"
		elif Player_Button["text"] == "Player vs. Hard CPU":
			PlayerMode = 0
			Player_Button["text"] = "Player vs. Player"

def handle_key_event(event):
	global EndGame
	global pause
	global Paddle1c
	global Paddle2c
	global PlayerMode
	global Space
	if event.char == "w":
		Paddle1c.startmoveup()
	if event.char == "s":
		Paddle1c.startmovedown()
	if PlayerMode == 0:
		if event.keysym == "Up":
			Paddle2c.startmoveup()
		if event.keysym == "Down":
			Paddle2c.startmovedown()
	if Start == 1:
		if event.char == "p":
			PauseGame()
	if event.keysym == "space":
		StartGame()
		Space = 1
	if event.keysym == "Return":
		if EndGame == 1:
			RestartGame()

	
	
	
def handle_key_release_event(event):
	global EndGame
	global Paddle1c
	global Paddle2c
	global PlayerMode
	if event.char == "w":
		Paddle1c.endmoveup()
	if event.char == "s":
		Paddle1c.endmovedown()
	if event.keysym == "Up":
		Paddle2c.endmoveup()
	if event.keysym == "Down":
		Paddle2c.endmovedown()
	if event.keysym == "space":
		Space = 0
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
		line = line.split(":")
		PaddlePos1 = line[0]
		PaddlePos2 = line[1]
		BallPos = line[2]
		PaddlePos1 = PaddlePos1.split(",")
		PaddlePos2 = PaddlePos2.split(",")
		BallPos = BallPos.split(",")
		P1Replay.append(PaddlePos1)
		P2Replay.append(PaddlePos2)
		BReplay.append(BallPos)
	EndGame = 1
	Ncounter = len(P1Replay)
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
	if counter < Ncounter:
		Root.after(20, ReplayGame)
	



	

		

def moveBall():
	global Ballc
	global iBallc
	w.move(Ballc.obj, Ballc.CSpeed[0], Ballc.CSpeed[1])
	iBallc.ChangeSpeed()
	w.move(iBallc.obj, iBallc.CSpeed[0], iBallc.CSpeed[1])
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
	if Start == 0 and pause == 0:
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
	global PaddleTrigger
	global AILocate
	if Mover == Ball:
		if Other != InvisaBall:
			Ballc.ChangeSpeed()
		x = Ballc.CSpeed[0]
		y = Ballc.CSpeed[1]
		if Other == Paddle1:
			Ballc.CSpeed = [abs(x),y]
		if Other == Paddle2:
			PaddleTrigger = 1
			Ballc.CSpeed = [-(abs(x)),y]
			iBallc.CSpeed = [-(abs(x)),y]
			iBallc.NCSpeed = [0,0]
			iBallc.ChangeSpeed()
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
				if Other == WallLeft:
					GameBoard.UpdateScore(1)
					print "Player 2 Wins the Point! Press Enter to Reset."
				else:
					GameBoard.UpdateScore(0)
					print "Player 1 Wins the Point! Press Enter to Reset."
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
		
			
	if Mover == InvisaBall:
			x = iBallc.CSpeed[0]
			y = iBallc.CSpeed[1]
			if Other == iWallLeft:
				iBallc.CSpeed = [abs(x),y]
			if Other == iWallRight:
				if AILocate == 0:
					iBallc.FlipSpeeds()
				AILocate = 1
			if Other == WallTop:
				iBallc.CSpeed = [x,abs(y)]
			if Other == WallBottom:
				iBallc.CSpeed = [x,-(abs(y))]

	

def RecordPositions():
	global Start
	global EndGame
	global GamePositions
	global Paddle1c
	global Paddle2c
	global Ballc
	global pause
	if Start == 1 and EndGame == 0 and pause == 0: #check for working
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
	global trigger
	global GameMode
	global TimeCounter
	global ReleaseCounter
	global GameStarted
	global FirstCheck
	if trigger == 1:
		w.itemconfigure(PlayerWins, text="")
		GameBoard.ScoreBoard = [0,0]
		GameBoard.Score1String.set(str(GameBoard.ScoreBoard[0]))
		GameBoard.Score2String.set(str(GameBoard.ScoreBoard[1]))
		trigger = 0
		PauseGame()
		TimeCounter = 0
		ReleaseCounter = 0
		GameStarted = 0
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
	FirstCheck = 0
		
		
		
	
	
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
		#default += "."
		#default += str(savetime[6])
	
		filename = tkSimpleDialog.askstring("Text Input Box","Name for file? (default date/time)")
		if filename == "" :
			filename = default
		if filename != None:
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





def ArtificialIntelligence():
	global PlayerMode
	global Paddle2c
	if PlayerMode == 0:
		Paddle2c.paddlespeed = Paddle2c.storedpaddlespeed
	elif PlayerMode == 1:
		Paddle2c.paddlespeed = Paddle2c.easypaddlespeed
		EasyAI()
	elif PlayerMode == 2:
		Paddle2c.paddlespeed = Paddle2c.storedpaddlespeed
		HardAI()
	Root.after(20, ArtificialIntelligence)
	

	
def EasyAI():
	global Paddle1c
	global Paddle2c
	global Ballc
	global AIMoving
	global EndGame
	global ReactionTime
	global ReactionTimeCounter
	if EndGame == 1:
		AIMoving == "Stop"
		Paddle2c.endmovedown()
		Paddle2c.endmoveup()
	PaddleBox = w.bbox(Paddle2c.obj)
	Center = (PaddleBox[1] + PaddleBox[3])/2
	BallBox = w.bbox(Ballc.obj)
	BallCenter = (BallBox[1] + BallBox[3])/2
	testing = (Paddle2c.moveup +Paddle2c.movedown)
	if (testing) == 0:
		Paddle2c.endmovedown()
		Paddle2c.endmoveup()
		AIMoving = "Stop"
	if AIMoving == "Stop":
		if ReactionTime == ReactionTimeCounter:
			if BallBox[1] > Center:
				Paddle2c.startmovedown()
				AIMoving = "Down"
			elif BallBox[3] < Center:
				Paddle2c.startmoveup()
				AIMoving = "Up"
	else:
		if AIMoving == "Down":
			if Center >= BallCenter:
				Paddle2c.endmovedown()
				AIMoving = "Stop"
		if AIMoving == "Up":
			if Center <= BallCenter:
				Paddle2c.endmoveup()
				AIMoving = "Stop"
	if ReactionTime == ReactionTimeCounter:
		ReactionTimeCounter = 0
	else:
		ReactionTimeCounter += 1
		







def HardAI():
	global PaddleTrigger
	global Ballc
	global iBallc
	global Start
	global Game
	global Starter
	global Paddle1c
	global P1Prev
	global AILocate
	global AIHardMoving
	global GameBoard
	global Space
	global DoubleCheck
	global iBBSaveCenter
	global GameMode
	global FirstCheck
	BallBox = w.bbox(Ballc.obj)
	PaddleBox = w.bbox(Paddle1c.obj)
	Paddle2Box = w.bbox(Paddle2c.obj)
	if PaddleTrigger == 1 or (Start == 0 and (PaddleBox != P1Prev)) or FirstCheck == 0:
		FirstCheck = 1
		DoubleCheck = 0
		w.coords(iBallc.obj, BallBox[0],BallBox[1],BallBox[2],BallBox[3])
		AILocate = 0
		Paddle2c.endmovedown()
		Paddle2c.endmoveup()
		AIHardMoving = "Stop"
		PaddleTrigger = 0
		if Start == 0 and Starter == 0:
			iBallc.CSpeed = [abs(iBallc.ISpeed[0]), iBallc.ISpeed[1]]
			iBallc.NCSpeed = [0,0]
		if Start == 0 and Starter == 1:
			iBallc.CSpeed = [-(abs(iBallc.ISpeed[0])), iBallc.ISpeed[1]]
			iBallc.NCSpeed = [0,0]
	iBBall = w.bbox(iBallc.obj)
	iBCenter = (iBBall[1]+iBBall[3])/2
	P2Center = (Paddle2Box[1]+Paddle2Box[3])/2	
	if AILocate == 1 and (Starter == 0 or (Starter == 1 and Start == 1)):
			if AIHardMoving == "Stop":
				Paddle2c.endmovedown()
				Paddle2c.endmoveup()
				iBBSave = iBBall
				iBBSaveCenter = iBCenter
				if iBBSaveCenter < (Paddle2c.height)/2:
					iBBSaveCenter = (Paddle2c.height/2)+1
				if iBBSaveCenter  > GameBoard.CanvasHeight - (Paddle2c.height)/2:
					iBBSaveCenter = GameBoard.CanvasHeight - (Paddle2c.height)/2 -1 
				if iBCenter > P2Center:
					Paddle2c.startmovedown()
					AIHardMoving = "Down"
				elif iBCenter < P2Center:
					Paddle2c.startmoveup()
					AIHardMoving = "Up"
			elif AIHardMoving == "Down":
				if iBBSaveCenter <= P2Center:
					AIHardMoving = "Stop"
					Paddle2c.endmovedown()
					DoubleCheck = 1
					AILocate = 0
			elif AIHardMoving == "Up":
				if iBBSaveCenter >= P2Center:
					AIHardMoving = "Stop"
					Paddle2c.endmoveup()
					DoubleCheck = 1
					AILocate = 0
	P1Prev = PaddleBox
	if AILocate == 0 and PaddleTrigger == 0 and (Starter == 0 or (Starter == 1 and Start == 1)) and DoubleCheck == 0:
		center = GameBoard.CanvasHeight/2
		if center > P2Center:
			Paddle2c.startmovedown()
		if center < P2Center:
			Paddle2c.startmoveup()
	if DoubleCheck == 1:
			w.coords(iBallc.obj, BallBox[0],BallBox[1],BallBox[2],BallBox[3])
			iBallc.CSpeed = [Ballc.CSpeed[0], Ballc.CSpeed[1]]
			iBallc.ChangeSpeed()
			DoubleCheck = 2
	if AILocate == 1 and DoubleCheck == 2:
		DoubleCheck = 0
	temps = Paddle2c.moveup + Paddle2c.movedown
	if iBallc.CSpeed[0] == 0 and iBallc.CSpeed[1] == 0 and Start == 1 and temps == 0:
		AIHardMoving = "Stop"
		DoubleCheck = 1
	if Starter == 1 and GameMode == 1 and GameBoard.ScoreBoard[0] > GameBoard.ScoreBoard[1]:
		StartGame()
	
	
	
	
	
	

def GameModeLoop():
	global GameStarted
	global GameBoard
	global GameMode
	global GameModeLast
	global TimeCounter
	global TimedPlayDuration
	global Start
	global EndGame
	global pause
	global PlayerWins
	global trigger
	global ReleaseCounter
	global PlayerMode
	global PlayerModeLast
	global Ballc
	global ScoredPlayWinPoints
	tempcounter = 0
	if GameMode != GameModeLast or PlayerMode != PlayerModeLast:
		GameBoard.ScoreBoard = [0,0]
		GameBoard.Score1String.set(str(GameBoard.ScoreBoard[0]))
		GameBoard.Score2String.set(str(GameBoard.ScoreBoard[1]))
		TimeCounter = 0
		GameStarted = 0
		trigger = 0
	GameModeLast = GameMode
	PlayerModeLast = PlayerMode
	if Start == 1 and trigger == 0:
		GameStarted = 1
	if GameMode == 1 and GameStarted == 1:
		temps = TimedPlayDuration*1000
		if TimeCounter == temps:
			if trigger == 0:
				PauseGame()
				if GameBoard.ScoreBoard[0] > GameBoard.ScoreBoard[1]:
					w.itemconfigure(PlayerWins, text="Player 1 Wins!")
				elif GameBoard.ScoreBoard[0] < GameBoard.ScoreBoard[1]:
					w.itemconfigure(PlayerWins, text="Player 2 Wins!")
				else:
					w.itemconfigure(PlayerWins, text="It's a Tie!")
				trigger = 1
				EndGame = 1
		else:
			if EndGame != 1:
				if pause != 1:
					TimeCounter = TimeCounter + 20
					ReleaseCounter = ReleaseCounter + 20
					if ReleaseCounter > (TimedPlayMaxBallHoldTime*1000):
						StartGame()
			else:
				ReleaseCounter = 0
	if GameMode == 2 and GameStarted == 1:
		if GameBoard.ScoreBoard[0] >= ScoredPlayWinPoints:
			w.itemconfigure(PlayerWins, text="Player 1 Wins!")
			trigger = 1
			EndGame = 1
		if GameBoard.ScoreBoard[1] >= ScoredPlayWinPoints:
			w.itemconfigure(PlayerWins, text="Player 2 Wins!")
			trigger = 1
			EndGame = 1	
	Root.after(20, GameModeLoop)
	
	
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






Game = GameParameters() 
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
TimedPlayDuration = Cato.get("TimedPlayDuration")
TimedPlayMaxBallHoldTime = Cato.get("TimedPlayMaxBallHoldTime")
ScoredPlayWinPoints = Cato.get("ScoredPlayWinPoints")




Paddle1c = Paddlec(1,Pwidth,80,PaddleSpeed)
Paddle2c = Paddlec(2,Pwidth,80,PaddleSpeed)

iBallc = Ballc(InitialBallSpeedX, InitialBallSpeedY, BallRadius, MaxBallSpeed*2, MaxBallSpeed*2)

Ballc = Ballc(InitialBallSpeedX, InitialBallSpeedY, BallRadius, MinBallSpeed, MaxBallSpeed)
Paddle1c.InputCoords(5, 35, 5+Paddle1c.width, 35+Paddle1c.height)
Paddle2c.InputCoords(CanvasWidth-5, CanvasHeight-50, CanvasWidth-Paddle2c.width-5, CanvasHeight-50-Paddle2c.height)
Starter = random.randint(0,1)

Root = Tk()





Restart_Button = Button(Root, text="Restart", command = RestartGame)#command=Print_Message)
Restart_Button.grid(row=0, column=3, sticky = W)

Pause_Button = Button(Root, text="Pause", command=PauseGame)#command=Print_Message)
Pause_Button.grid(row=3, column=0, sticky = W)


Exit_Button = Button(Root, text="Exit", command=Root.quit)
Exit_Button.grid(row=3, column=4, sticky=E)

Save_Button = Button(Root, text="Save Recording", command=SaveGame)
Save_Button.grid(row=3, column=2, sticky = W)

Load_Button = Button(Root, text="Load Recording", command=LoadGame)
Load_Button.grid(row=3, column = 1, sticky = W)

Player_Button = Button(Root, text="Player vs. Player", command=PlayerModeSelection)
Player_Button.grid(row=0, column = 2)

Mode_Button =  Button(Root, text="Unlimited Play", command=GameModeSelection)
Mode_Button.grid(row=0, column = 1, sticky = E)


w = Canvas(Root, width=CanvasWidth, height=CanvasHeight) 
w.grid(row=1, column=0, columnspan=5, sticky = W+E+N+S)












WallLeft = w.create_line(5,0,5,CanvasHeight, fill="white")
WallRight = w.create_line(CanvasWidth,0,CanvasWidth,CanvasHeight, fill="white")
WallTop = w.create_line(0,5,CanvasWidth,5,fill="white")
WallBottom = w.create_line(0,CanvasHeight,CanvasWidth,CanvasHeight,fill="white")


iWallLeft = w.create_line(Paddle1c.width+5,0,Paddle1c.width+5,CanvasHeight, fill="white")#, state = HIDDEN)
iWallRight = w.create_line(CanvasWidth-Paddle2c.width+3-10,0,CanvasWidth-Paddle2c.width+3-10,CanvasHeight, fill="white")#, state = HIDDEN)
GameBoard = Board(CanvasWidth, CanvasHeight, WallLeft, WallTop,WallRight,WallBottom)



#PLAYER SCORE BOARD DISPLAY NEEDS TO BE AFTER BOARD INITIALIZATION
Player1_Score = Label(Root, textvariable= GameBoard.Score1String)
Player1_Score.grid(row=0, column=0)
Player2_Score = Label(Root, textvariable = GameBoard.Score2String)
Player2_Score.grid(row=0, column=4)











Paddle1 = w.create_rectangle(Paddle1c.coords[0], Paddle1c.coords[1], Paddle1c.coords[2], Paddle1c.coords[3], fill="white")
Paddle2 = w.create_rectangle(Paddle2c.coords[0], Paddle2c.coords[1], Paddle2c.coords[2], Paddle2c.coords[3], fill="white")

InvisaBall = w.create_oval(0,0,(2*Ballc.radius),(2*Ballc.radius), outline="white")#, state = HIDDEN)
Ball = w.create_oval(0,0,(2*Ballc.radius),(2*Ballc.radius), fill="white")
Ballc.InputObject(Ball)
iBallc.InputObject(InvisaBall)


iBallc.CSpeed = [iBallc.ISpeed[0], iBallc.ISpeed[1]]
#iBallc.ChangeSpeed()

Ballc.InputCoords([Paddle1c.coords[2]+2, Paddle1c.middle()-Ballc.radius, Paddle1c.coords[2]+(2*Ballc.radius)+2,Paddle1c.middle()+Ballc.radius],[Paddle2c.coords[2]-(2*Ballc.radius)-2,Paddle2c.middle()-Ballc.radius,Paddle2c.coords[2]-2,Paddle2c.middle()+Ballc.radius]) 


Ballc.restartpos(w, Starter)



Paddle1c.InputObject(Paddle1)
Paddle2c.InputObject(Paddle2)




bbBall = w.bbox(Ballc.obj)
Paddle2c.ImportCanvas(w)


Root.configure(background='grey') #white for my computer
w.configure(background='white')




PlayerWins = w.create_text(CanvasWidth/2,CanvasHeight/2,text="")
#PlayerTwoWins = w.create_text(CanvasWidth/2,CanvasHeight/2,text="Player 2 Wins!", state= HIDDEN)
#PlayerTwoWins["State"] = "NORMAL"
#PlayerWins["text"] = "It's a Tie!"

Root.bind("<Key>", handle_key_event)
Root.bind("<KeyRelease>", handle_key_release_event)
Root.title("ECE 364: Pong")


Root.after(20, checkcollision)
Root.after(20, moveBall)
Root.after(20, movepaddle)
Root.after(20, RecordPositions)
Root.after(20, ArtificialIntelligence)
Root.after(20, GameModeLoop)
Root.mainloop()

sys.exit(0)

#CHECK LIST
#Scoreboard updates-check
#move pause button- check
#move exit button - check
#move restart button -check
#Add Game Mode toggle button
#Add player vs player/cpu button - check
#add load recording button -check 
#add save recording button -check
# Game Records every action in a game - Check
# Game loads a game -check
# Game Saves every action in a game to a file - check












#All Rights Reserved 2013
#Christohper Holly 
#Purdue University