from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from pygame.locals import *
from pygame.constants import *
import pygame,numpy
from PIL import Image
from math import *


class world:
	def __init__(self,fileName,x,z):
		self.x=x
		self.z=z
		self.gl_lis=0
		self.size=1
		self.heightRatio=0
		self.mapArray=[]
		rows=[]
		file=Image.open('Texture/'+fileName)
		hmap=file.load()
		for i in range(file.height):
			rows=[]
			for j in range(file.width):
				rows.append(hmap[i,j][0]/255.0)
			self.mapArray.append(rows)


	def render(self,s,h):
		self.size=s
		self.heightRatio=h
		img = pygame.image.load('Texture/ground.png')
		img_data = pygame.image.tostring(img, "RGBA",1)
		ID = glGenTextures(1)
		glGenerateMipmap( GL_TEXTURE_2D )
		#glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glBindTexture(GL_TEXTURE_2D, ID)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
		glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_REPEAT)
		glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_REPEAT)
		glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS,-1)
		gluBuild2DMipmaps(GL_TEXTURE_2D,GL_RGBA,img.get_width(),img.get_height(),GL_RGBA,GL_UNSIGNED_BYTE,img_data)
		
		self.gl_lis=glGenLists(1)
		glNewList(self.gl_lis, GL_COMPILE)
		#glEnable(GL_COLOR_MATERIAL)
		#glDisable(GL_LIGHTING)
		for i in range(len(self.mapArray)-1):
			glEnable(GL_TEXTURE_2D)
			glBindTexture(GL_TEXTURE_2D,ID)
			glBegin(GL_TRIANGLE_STRIP)
			for j in range(len(self.mapArray[i])-1):
				v1=[s*i,h*self.mapArray[i][j],s*j]
				v2=[s*(i+1),h*self.mapArray[i+1][j],s*j]
				v3=[s*i,h*self.mapArray[i][j+1],s*(j+1)]
				v4=[s*(i+1),h*self.mapArray[i+1][j+1],s*(j+1)]
				v=[v1,v2,v3,v4]
				t=[[1,0],[0,0],[0,1],[1,1]]
				glVertex3d(v[0][0],v[0][1],v[0][2])
				glTexCoord2f(t[0][0],t[0][1])
				glVertex3d(v[1][0],v[1][1],v[1][2])
				glTexCoord2f(t[1][0],t[1][1])
				glVertex3d(v[2][0],v[2][1],v[2][2])
				glTexCoord2f(t[2][0],t[2][1])
				glVertex3d(v[3][0],v[3][1],v[3][2])
				glTexCoord2f(t[3][0],t[3][1])
				
				glNormal(h*self.mapArray[i-1][j]-h*self.mapArray[i+1][j],2,h*self.mapArray[i][j-1]-h*self.mapArray[i][j+1])
				#glNormal(0,1,0)
				#glVertex3d(v[0][0],v[0][1],v[0][2])
				#glVertex3d(v[1][0],v[1][1],v[1][2])
				#glVertex3d(v[2][0],v[2][1],v[2][2])
				#glVertex3d(v[3][0],v[3][1],v[3][2])
			glEnd()
			glDisable(GL_TEXTURE_2D)
		glEndList()
		glDisable(GL_COLOR_MATERIAL)
		#glEnable(GL_LIGHTING)

	def disp(self):
		glLoadIdentity()
		glTranslate(self.x,0,self.z)
		glCallList(self.gl_lis)

	def height(self,x,z):
		return self.mapArray[int((x-self.x)/self.size)][int((z-self.z)/self.size)]*self.heightRatio
	def setheight(self,x,z,h):
		self.mapArray[int((x-self.x)/self.size)][int((z-self.z)/self.size)]=h/self.heightRatio
