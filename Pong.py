#! /usr/bin/env python

import sys
import os
import re
import math
from Tkinter import *




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
	Arr.append(int(line))
	#print line
print Arr
InitialBallSpeedX = int(Arr[0])
InitialBallSPeedY = int(Arr[1])
PaddleSpeed = int(Arr[2])
BallRadius = int(Arr[3])
CanvasWidth = int(Arr[4])
CanvasHeight = int(Arr[5])
MaxBallSpeed = int(Arr[6])
MinBallSpeed = int(Arr[7])

Root = Tk()




# MOST OF THIS WILL BE PUT INTO THE CONFIGURATION FILE
Restart_Button = Button(Root, text="Restart", )#command=Print_Message)
Restart_Button.grid(row=0, column=0,columnspan =2, sticky = W)

Pause_Button = Button(Root, text="Pause", )#command=Print_Message)
Pause_Button.grid(row=0, column=1, sticky = W)


Exit_Button = Button(Root, text="Exit", command=Root.quit)
Exit_Button.grid(row=0, column=4, sticky=E)


w = Canvas(Root, width=CanvasWidth, height=CanvasHeight) 

w.grid(row=1, column=0, columnspan=5, sticky = S)


paddle1 = w.create_rectangle(5, 35, 30, 115, fill="white")
paddle2 = w.create_rectangle(500, 35+300, 475, 115+300, fill="white")

ball = w.create_oval(30,(35+115)/2-10,30+20,(35+115)/2+10, fill="white")

Root.mainloop()