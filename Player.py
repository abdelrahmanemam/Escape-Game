from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from pygame.locals import *
from pygame.constants import *
import sys, pygame, math,os,numpy,time
from PIL import Image
from Collision import *
from math import *

class player:
	def __init__(self,fovy,Width,Height,footSound,lisOBJ):
		self.fovy=fovy
		self.speed=0.25
		self.footSound=footSound
		self.jumpStrength=0.5
		self.jumpSpeed=self.jumpStrength
		self.deacceleration=-0.05
		self.jumping=0
		self.tall=6

		self.x=0
		self.y=self.tall
		self.z=0
		self.lookx=0
		self.looky=0
		self.lookz=0

		self.thetaUp=0
		self.theta=0

		self.Width=Width
		self.Height=Height

		self.playerMove=0
		self.animation=0
		self.i=0
		self.lisOBJ=lisOBJ
		self.t=0
		self.currentTool=lisOBJ[self.t]
		self.tools=len(self.lisOBJ)
		self.walkingAudio=0

	def hieght(self,hieght):
		self.y=hieght+self.tall

	#update the postion of the player and where he is looking to
	def updateCamera(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(self.fovy,self.Width/self.Height,0.01,3000)
		gluLookAt(self.x,self.y,self.z	,	self.x-sin(self.theta), self.y+sin(self.thetaUp), self.z+cos(self.theta)	,	0,1,0)

	def updateTool(self):
		#get next tool
		self.t+=1
		if(self.t>=self.tools):
			self.t=0
		self.currentTool=self.lisOBJ[self.t]


	def displayTool(self):
		if(self.t==0):
			glLoadIdentity()
			glTranslate(self.x-sin(self.theta)/8.0-0.05*cos(self.theta), self.y+sin(self.thetaUp)/8.0-0.05, self.z+cos(self.theta)/8.0-0.05*sin(self.theta))
			glRotate(-self.theta*180/3.14,0,1,0)
			glRotate(-self.thetaUp*180/3.14,1,0,0)
			glRotate(0,0,1,0)
			glScale(0.05,0.05,0.05)
		else:
			glLoadIdentity()
			#the item postion in x - a small value of(sin(theta)) to translate the obj in front of the camera 
			#and a small value to translate it right
			glTranslate(self.x-sin(self.theta)/8.0-0.05*cos(self.theta), self.y+sin(self.thetaUp)/8.0-0.1, self.z+cos(self.theta)/8.0-0.05*sin(self.theta))
			glRotate(-self.theta*180/3.14,0,1,0)
			glRotate(-self.thetaUp*180/3.14,1,0,0)
			glRotate(90,0,1,0)
			glScale(0.02,0.02,0.02)

		if(self.animation):
			self.i+=1
			if(self.i>=len(self.currentTool)):
				self.i=0
				self.animation=0
		glCallList(self.currentTool[self.i].gl_list)
			


	def jump(self,h):
		h+=self.tall

		if(self.jumping):
			self.jumpSpeed+=self.deacceleration
			if(self.y+self.jumpSpeed<h):
				self.jumping=0
				self.y=h
			else:
				self.y+=self.jumpSpeed
		else:
			self.jumpSpeed=self.jumpStrength
			if(self.y>h):
				self.jumping=1
				self.jumpSpeed=0
			else:
				self.y=h#height map



	#make the player to move , depend on the key pressed on the keyboard 
	#and check the collision
	def move(self,keyState,alist,lisObjs,lisDoors):
		self.playerMove=0

		x=self.x
		y=self.y+self.tall
		z=self.z
		if(keyState[112]):
			speed=self.speed*2
		else:
			speed=self.speed
		if keyState[ord('s')] and  keyState[ord('d')]:
			self.x+=speed*sin(self.theta)/2**0.5
			self.z-=speed*cos(self.theta)/2**0.5
			self.z-=speed*sin(self.theta)/2**0.5
			self.x-=speed*cos(self.theta)/2**0.5
			self.playerMove=1
		elif keyState[ord('s')] and keyState[ord('a')]:
			self.x+=speed*sin(self.theta)/2**0.5
			self.z-=speed*cos(self.theta)/2**0.5
			self.z+=speed*sin(self.theta)/2**0.5
			self.x+=speed*cos(self.theta)/2**0.5
			self.playerMove=1
		elif keyState[ord('d')] and  keyState[ord('w')]:
			self.z-=speed*sin(self.theta)/2**0.5
			self.x-=speed*cos(self.theta)/2**0.5
			self.x-=speed*sin(self.theta)/2**0.5
			self.z+=speed*cos(self.theta)/2**0.5
			self.playerMove=1
		elif keyState[ord('a')] and  keyState[ord('w')]:
			self.z+=speed*sin(self.theta)/2**0.5
			self.x+=speed*cos(self.theta)/2**0.5
			self.x-=speed*sin(self.theta)/2**0.5
			self.z+=speed*cos(self.theta)/2**0.5
			self.playerMove=1
		elif keyState[ord('s')]:
			self.x+=speed*sin(self.theta)
			self.z-=speed*cos(self.theta)
			self.playerMove=1
		elif keyState[ord('w')]:
			self.x-=speed*sin(self.theta)
			self.z+=speed*cos(self.theta)
			self.playerMove=1
		elif keyState[ord('a')]:
			self.z+=speed*sin(self.theta)
			self.x+=speed*cos(self.theta)
			self.playerMove=1
		elif keyState[ord('d')]:
			self.z-=speed*sin(self.theta)
			self.x-=speed*cos(self.theta)
			self.playerMove=1
			
		collied=collision(self,alist,lisObjs,lisDoors)
		Near=near(self,None,lisDoors,keyState)
		if(self.playerMove):
			if not self.walkingAudio:
				self.footSound.play(-1)
				self.walkingAudio=1
		else:
			self.footSound.stop()
			self.walkingAudio=0
			
		if(collied or ((self.x>=35 and self.x<=45) and (self.z<50) and (self.z>49) and (self.y<10))):
			print(collied)
			self.x=x
			self.z=z
		

		









