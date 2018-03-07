from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 

class obje:
	def __init__(self,OBJ=None,animation=1,lis=[0,0,0],radius=0.5,scale=1,rotate=0,doorRotation=0,doorKey=1):
		self.OBJ=OBJ

		self.x=lis[0]
		self.y=lis[1]
		self.z=lis[2]

		self.radius=radius
		self.scale=scale
		self.rotate=rotate
		
		self.animation=animation
		self.i=0
		self.angle=0

		self.doorKey=doorKey
		self.doorRotation=doorRotation
	def updatePosition(self,x,y,z):
		self.x=x
		self.y=y
		self.z=z

	def setHeight(self,height):
		self.height=height


	def disp(self):
		glTranslate(self.x,self.y,self.z)
		glScale(self.scale,self.scale,self.scale)
		glRotate(self.rotate,0,1,0)
		if(self.i>=len(self.OBJ)):
			self.i=0
		glCallList(self.OBJ[self.i].gl_list)
		if(self.animation==1):
			self.i+=1

	def dispDoor(self):
		if not self.rotate:
			glTranslate(self.x-2.5,self.y,self.z)	
		else:
			glTranslate(self.x,self.y,self.z+2.5)
			
		if(self.doorRotation):
			glRotate(-self.angle,0,1,0)
		else:
			glRotate(self.angle,0,1,0)
		if not self.rotate:
			glTranslate(2.5,0,0)
		else:
			glTranslate(0,0,-2.5)
		glRotate(self.rotate,0,1,0)
		glScale(self.scale,self.scale,self.scale)
		glCallList(self.OBJ[0].gl_list)
		if self.animation and self.angle>-120:
			self.angle-=4


