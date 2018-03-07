from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from pygame.locals import *
from pygame.constants import *
import pygame
from PIL import Image
from math import *

class texture:
	def __init__(self,fileName,v,t,skybox=0):
		img = pygame.image.load('Texture/'+fileName)
		img_data = pygame.image.tostring(img, "RGBA",1)
		ID = glGenTextures(1)
		glGenerateMipmap( GL_TEXTURE_2D )
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glBindTexture(GL_TEXTURE_2D, ID)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
		if(skybox):
			glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_CLAMP)
			glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_CLAMP)

		else:
			glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_REPEAT)
			glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_REPEAT)
		glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS,-1)
		gluBuild2DMipmaps(GL_TEXTURE_2D,GL_RGBA,img.get_width(),img.get_height(),GL_RGBA,GL_UNSIGNED_BYTE,img_data)
		self.T=glGenLists(1)
		glNewList(self.T,GL_COMPILE)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D,ID)
		glBegin(GL_QUADS)
		glVertex3d(v[0][0],v[0][1],v[0][2])
		glTexCoord2f(t[0][0],t[0][1])
		glVertex3d(v[1][0],v[1][1],v[1][2])
		glTexCoord2f(t[1][0],t[1][1])
		glVertex3d(v[2][0],v[2][1],v[2][2])
		glTexCoord2f(t[2][0],t[2][1])
		glVertex3d(v[3][0],v[3][1],v[3][2])
		glTexCoord2f(t[3][0],t[3][1])
		glEnd()
		glDisable(GL_TEXTURE_2D)
		glEndList()


	def disp(self):
		glDisable(GL_COLOR_MATERIAL)
		glCallList(self.T)
		
