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
class Ballc:
	def __init__(self, ISpeedX, ISpeedY, radius, min, max):
		self.ISpeed = [ISpeedX, ISpeedY]
		self.radius = radius
		self.CSpeed = [0,0]
		self.NCSpeed = [0,0]
		self.min = min
		self.max = max
		
		
	def getISpeed(self):
		return self.ISpeed
		
	def getRadius(self):
		return self.radius
		
	def ChangeSpeed(self):
		scale = 0
		while scale == 0:
			scale = random.uniform(self.min, self.max)
		x = self.CSpeed[0]
		y = self.CSpeed[1]
		current = pow(pow(x,2)+pow(y,2),0.5)
		if current != 0:
			x = (x/current)
			y = (y/current)
			x = x*scale
			y = y*scale
			self.CSpeed = [x,y]
		
	def InputObject(self, obj):
		self.obj = obj
		
		
	def StartSpeed(self):
		self.CSpeed[0] = self.ISpeed[0]
		self.CSpeed[1] = self.ISpeed[1]
		
		
		
	def FlipSpeeds(self):
		temp = self.CSpeed[0]
		self.CSpeed[0] = self.NCSpeed[0]
		self.NCSpeed[0] = temp
		temp = self.CSpeed[1]
		self.CSpeed[1] = self.NCSpeed[1]
		self.NCSpeed[1] = temp
		
	def InputCoords(self, p1, p2):
		self.startpos = [p1,p2]
		
	def restartpos(self, w, Starter):
		w.coords(self.obj, self.startpos[Starter][0], self.startpos[Starter][1], self.startpos[Starter][2], self.startpos[Starter][3])
		
		
		
class Paddlec:
	def __init__(self, paddlenum, paddlewidth, paddleheight, paddlespeed):
		self.paddlenum = paddlenum
		self.height = paddleheight
		self.width = paddlewidth
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
	def InputCoords(self, x1, y1, x2, y2):
		self.coords = [x1, y1, x2, y2]
		
	def middle(self):
		return int((self.coords[1]+self.coords[3])/2)
	
	def restartpos(self, w):
		w.coords(self.obj, self.coords[0],self.coords[1],self.coords[2], self.coords[3])
		
		
		
class Board:
	def __init__(self, CanvasWidth, CanvasHeight, WallLeft, WallTop, WallRight, WallBottom):
		self.CanvasWidth = CanvasWidth
		self.CanvasHeight = CanvasHeight
		self.WallLeft = WallLeft
		self.WallTop = WallTop
		self.WallRight = WallRight
		self.WallBottom = WallBottom
		
		