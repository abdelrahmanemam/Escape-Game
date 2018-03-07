from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame, random, sys
global background_id
global menuimage,unilogo
global fullscreen,sfx_volume,bgm_volume
from Main import *

#SOME LISTS OF RGB COLORS
white=[1,1,1]
red=[1,0,0]
blue=[0,0,1]
green=[0,1,0]
#SCREEN RESOLUTION
WindowWidth=1280
WindowHeight=720
#BUTTON SIZES AND COLORS
bSize=[0.35,0.35,0.35,0.35,0.35]
bColor=[white,white,white,white,white]

#DISPLAY FLAGS
intro=1
main_menu=0
menu_to_game=0
loadscreen=0
settings=0
credits=0
gameplay=0

#ٍSOME OPTIONS
sfx_volume=100
bgm_volume=100
audioPlaying=0

#TEXTURE INITIALIZATION
def texInit(name,id):
	imgload=pygame.image.load(name) #LOAD IMAGE
	imgdata=pygame.image.tostring(imgload,"RGB",1) #CONVERT IMAGE TO RAW DATA
	width=imgload.get_width()
	height=imgload.get_height()
	glBindTexture(GL_TEXTURE_2D, background_id[id]) #GIVE IT AN ID THEN SET PARAMETERS
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB,width,height,0,GL_RGB,GL_UNSIGNED_BYTE,imgdata)
	#ASSING THE IMAGE TO A 2D TEXTURE WITH THE GIVEN SPECIFICATIONS ^



def init():
	global background_id,menuimage,textsize,unilogo
	glClearColor(0,0,0,0)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0,1280,0,720,-3,3)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) #SOURCE ALPHA, DEFAULTS
	background_id=glGenTextures(10)
	texInit("Menu\Images\BG1.jpg",0)
	texInit("Menu\Images\BG2.jpg",1)
	texInit("Menu\Images\BG3.jpg",2)
	texInit("Menu\Images\Intro0.jpg",3)
	texInit("Menu\Images\Intro1.jpg",4)
	texInit("Menu\Images\Intro2.jpg",5)
	texInit("Menu\Images\Intro3.jpg",6)
	texInit("Menu\Images\LD.jpg",7)
	texInit("Menu\Images\Black.jpg",8)
	texInit("Menu\Images\TantaC.jpg",9)

	menuimage=glGenLists(1) #GENERATE A GL.LIST THAT APPLIES ANY GIVEN TEXTURE
	glNewList(menuimage,GL_COMPILE) #COMPLIE THE LIST -- BEGIN
	glEnable(GL_TEXTURE_2D) 
	glBegin(GL_QUADS) #DRAWING TEXTURES ON QUADS
	glTexCoord(0,0)
	glVertex2d(0,0)
	glTexCoord(1,0)
	glVertex2d(1280,0)
	glTexCoord(1,1)
	glVertex2d(1280,720)
	glTexCoord(0,1)
	glVertex2d(0,720)
	glEnd() #END DRAWING
	glDisable(GL_TEXTURE_2D)
	glEndList() #END THE LIST

	unilogo=glGenLists(2)
	glNewList(unilogo,GL_COMPILE) #COMPLIE THE LIST -- BEGIN
	glEnable(GL_TEXTURE_2D) 
	glBegin(GL_QUADS) #DRAWING TEXTURES ON QUADS
	glTexCoord(0,0)
	glVertex2d(0,0)
	glTexCoord(1,0)
	glVertex2d(300,0)
	glTexCoord(1,1)
	glVertex2d(300,300)
	glTexCoord(0,1)
	glVertex2d(0,300)
	glEnd() #END DRAWING
	glDisable(GL_TEXTURE_2D)
	glEndList() #END THE LIST

def drawText(lis, string,x,y,textsize=0.35):
	glLineWidth(4)
	glLoadIdentity()
	glColor(lis[0],lis[1],lis[2]) #GIVEN THE COLOR IN A LIST
	glTranslate(x,y,1)
	glScale(textsize,textsize,textsize)
	string=string.encode()
	for char in string:
		glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, char)



t=0 #INTRO TRANSPERNCY MODIFIER
introCounter=0 #INTRO FRAMES COUNTER
def displayIntro():
	global background_id,menuimage,introCounter,intro,main_menu,t
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glCallList(menuimage)
	if introCounter<100: #100 FRAMES FOR EACH LOGO
		glBindTexture(GL_TEXTURE_2D, background_id[3])
	elif introCounter<200:
		glBindTexture(GL_TEXTURE_2D, background_id[4])
	elif introCounter<300:
		glBindTexture(GL_TEXTURE_2D, background_id[5])
	elif introCounter<400:
		glBindTexture(GL_TEXTURE_2D, background_id[6])
	elif introCounter>400 and introCounter<410: #SWITCH TO MENU SCREEN AFTER LAST LOGO
		intro=0
		t=1
		main_menu=1
		print("Error loc signal")
	introCounter+=1
	glColor4f(1,1,1,t)
	if introCounter<20: #FADING DURING THE FIRST AND LAST 20 FRAMES OF EACH LOGO
		t+=0.05
	if introCounter>79 and introCounter<99:
		t-=0.05
	if introCounter>99 and introCounter<119:
		t+=0.05
	if introCounter>179 and introCounter<199:
		t-=0.05
	if introCounter>199 and introCounter<219:
		t+=0.05
	if introCounter>279 and introCounter<299:
		t-=0.05
	if introCounter>299 and introCounter<319:
		t+=0.05
	if introCounter>379 and introCounter<399:
		t-=0.05
	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(WindowWidth, WindowHeight)
	glutSwapBuffers()


getRed,zombieCounter=1,0 #COUNTER FOR DISPLAYING THE ZOMBIE IMAGE WITHIN MENU SCREEN
def displayMenu():
	global background_id,menuimage,bColor,bSize,white,red,blue,zombieCounter,t
	global current_W,current_H,introCounter,audioPlaying,menu_to_game,getRed,loadscreen,main_menu
	if not audioPlaying:
		audioPlaying=1
		bgm.play(-1)
		bgm2.play(-1)
	introCounter=450
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	current_W=glutGet(GLUT_WINDOW_WIDTH) #GETTING CURRENT ACTUAL WIDTH AND HEIGHT IF WINDOW RESIZED
	current_H=glutGet(GLUT_WINDOW_HEIGHT)

	if getRed<=0.05:
		glColor4f(1,0,0,t)
		t-=0.02

	if zombieCounter<120: #FLICKERING LAMP PHOTOS (TEXTURES) DURING 120 FRAMES
		glBindTexture(GL_TEXTURE_2D, background_id[random.choice([0,0,0,0,0,0,0,0,0,1])]) #10% Dark
	elif zombieCounter>120: #SHOW THE ZOMBIE FOR 10 FRAMES
		glBindTexture(GL_TEXTURE_2D, background_id[2])
	if zombieCounter==130:
		zombieCounter=0
	glCallList(menuimage) #CALLING THE GL.LIST TO APPLY THE SELECTED TEXTURE (PHOTO)
	#WRITING DOWN OUR BUTTONS
	if not menu_to_game:
		drawText(bColor[0], "NEW GAME",	128, 345.6, bSize[0])
		drawText(bColor[1], "LOAD GAME", 128, 288, bSize[1])
		drawText(bColor[2], "SETTINGS", 128, 230.4, bSize[2])
		drawText(bColor[3], "CREDITS", 	128, 172.8, bSize[3])
		drawText(bColor[4], "EXIT", 	128, 115.2, bSize[4])
	glColor(1,1,1) #RESETTING THE COLOR TO WHITE TO NOT AFFECT THE TEXTURE DRAWN LATER
	zombieCounter+=1
	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(WindowWidth, WindowHeight)

	if menu_to_game:
		glColor(1,getRed,getRed)
		getRed-=0.03
		if t<=0.05:
			main_menu=0
			menu_to_game=0
			loadscreen=1
			glColor(1,1,1)
			t=0
			
	glutSwapBuffers()

#THE DISPLAY FOR THE SETTINGS SCREEN, SIMILAR TO MAIN MENU SCREEN
def displaySettings():
	global background_id,menuimage,bColor,bSize,white,red,blue,zombieCounter,t
	global current_W,current_H,fullscreen,sfx_volume,bgm_volume,bSound1,bSound2,bgm,bgm2,NewGameSound
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)
	if zombieCounter<120:
		glBindTexture(GL_TEXTURE_2D, background_id[random.choice([0,0,0,0,0,0,0,0,0,1])]) #10% Dark
	elif zombieCounter>120:
		glBindTexture(GL_TEXTURE_2D, background_id[2])
	if zombieCounter==130:
		zombieCounter=0
	glCallList(menuimage)
	drawText([.5,.5,.6], "SETTINGS",	128, 450, 0.3)
	drawText([.4,.4,.4], "GRAHPICS",	128, 345.6, 0.4)
	if fullscreen:
		drawText(bColor[1], "FULLSCREEN", 128, 288, bSize[1])
	else:
		drawText(bColor[1], "WINDOWED", 128, 288, bSize[1])
	drawText(bColor[2], "MUSIC: "+str(bgm_volume), 128, 230.4, bSize[2])
	drawText(bColor[3], "SOUNDS: "+str(sfx_volume), 128, 172.8, bSize[3])
	drawText(bColor[4], "BACK", 128, 115.2, bSize[4])
	glColor(1,1,1)

	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(WindowWidth, WindowHeight)
	bSound1.set_volume(.01*sfx_volume)
	bSound2.set_volume(.01*sfx_volume)
	NewGameSound.set_volume(0.01*sfx_volume)
	bgm.set_volume(.01*bgm_volume)
	zombieCounter+=1
	glutSwapBuffers()


def displayLoading():
	global background_id,menuimage,bColor,bSize,white,red,blue,t,gameplay
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	if t<1:
		glColor4f(1,1,1,t)
		t+=0.02
	glBindTexture(GL_TEXTURE_2D, background_id[7])
	glCallList(menuimage)
	if t>1:
		gameplay=1
	glutSwapBuffers()
	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(WindowWidth, WindowHeight)


crdY=0
def displayCredits():
	global crdY,unilogo,credits,main_menu
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	glBindTexture(GL_TEXTURE_2D,background_id[9])
	glTranslate(490,-2240+crdY,0)
	glCallList(unilogo)
	#X takes Start+Shift
	drawText(white, "- ESCAPE -", (200+185), -50+crdY, 0.5)
	drawText(white, " ", (200), -200+crdY, 0.2)
	drawText(white, "A COMPUTER GRAPHICS COURSE PROJECT", (200+80), -250+crdY, 0.2)
	drawText(white, " ", 300, -300+crdY, 0.2)
	drawText(white, "PROGRAMMED IN PYTHON USING OPENGL LIBRARY", (200+20), -350+crdY, 0.2)
	drawText(white, "POWERDED BY PYGAME LIBRARY", (200+165), -400+crdY, 0.2)
	drawText(white, " ", (200), -450+crdY, 0.2)
	drawText([.7,.7,.7], "- TEAM MEMBERS -", (200+185), -650+crdY, 0.3)
	drawText(white, " ", (200), -600+crdY, 0.2)
	drawText(white, "ABDELRAHMAN METWALY", (200+250), -750+crdY, 0.2)
	drawText(white, "ABDELRAHMAN TAREK", (200+270), -800+crdY, 0.2)
	drawText(white, "ABDELRAHMAN EMAM", (200+280), -850+crdY, 0.2)
	drawText(white, "AHMED WALEED", (200+310), -900+crdY, 0.2)
	drawText(white, "AMR KHALID", (200+330), -950+crdY, 0.2)
	drawText(white, "KHALED EL-DEEP", (200+290), -1000+crdY, 0.2)
	drawText(white, "KHALID AAMIR", (200+310), -1050+crdY, 0.2)
	drawText(white, "MOHAMED LEBDA", (200+300), -1100+crdY, 0.2)
	drawText(white, "SHAKIR GAD", (200+330), -1150+crdY, 0.2)
	drawText(white, "ZEYAD EL-SAWY", (200+300), -1200+crdY, 0.2)
	drawText([.8,.8,.8], "SUPERVISING", (200+320), -1300+crdY, 0.2)
	drawText(white, "DR. MOHAMED ALI AITA", (200+230), -1350+crdY, 0.2)
	drawText(white, " ", (200), -1400+crdY, 0.2)

	drawText([.7,.7,.7], "- ABOUT THE TEAM -", (200+155), -1650+crdY, 0.3)
	drawText(white, " ", (200), -1700+crdY, 0.2)
	drawText(white, "STUDENTS AT FACULTY OF ENGINEERING", (200+75), -1750+crdY, 0.2)
	drawText(white, "COMPUTER AND CONTROL ENGINEERING DEPARTMENT", (180+5), -1800+crdY, 0.2)
	drawText(white, "TANTA UNIVERSITY", (200+270), -1850+crdY, 0.2)
	drawText(white, "MAY 2017", (200+349), -1900+crdY, 0.2)
	drawText(white, " ", (200), -1950+crdY, 0.2)

	drawText([.7,.7,.7], "- DISCLAIMER -", (200+275), -2450+crdY, 0.2)
	drawText(white, " ", (200), -2500+crdY, 0.2)
	drawText(white, "THE HAND, GUN, AXE AND ZOMBIE 3D MODELS", (200+30), -2550+crdY, 0.2)
	drawText(white, "FROM TF3DM.COM, CREDITS TO THEIR MODELERS", (200+5), -2600+crdY, 0.2)
	drawText(white, "DETAILS CAN BE FOUND IN ATTACHED FILES.", (200+30), -2650+crdY, 0.2)


	if crdY>=3500:
		crdY=0
		credits=0
		main_menu=1
	crdY+=3.5
	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(WindowWidth, WindowHeight)
	glutSwapBuffers()



#MOUSE PASSIVE FUNCTION
def Mouse(x,y):
	global bSize,bColor,red,white,blue,current_H,current_W,bSound1,bSound2
	y=current_H-y #LET THE MOUSE COORDINATES START FROM BOTTOM LEFT NOT TOP LEFT
	y=y*WindowHeight/current_H #FIXING THE MOUSE SCREEN AREA IF RESIZED
	x=x*WindowWidth/current_W
	#RESET BUTTONS TO DEFAULTS IF NO HIGHLIGHTED
	bColor=[white,white,white,white,white]
	bSize=[0.35,0.35,0.35,0.35,0.35]
	#CHECK IF THE MOUSE IS NOW HIGHLIGHTING ANY BUTTON
	if (x>=128*WindowWidth/1280 and x<=420*WindowWidth/1280): #NEWGAME
		if(y<390*WindowHeight/720 and y>345*WindowHeight/720):
				bColor[0]=red
				bSize[0]=0.4
	
	if (x>=128*WindowWidth/1280 and x<=460*WindowWidth/1280): #LOADGAME
		if(y<330*WindowHeight/720 and y>285*WindowHeight/720):
				bColor[1]=red
				bSize[1]=0.4
				
	if (x>=128*WindowWidth/1280 and x<=430*WindowWidth/1280): #SETTINGS
		if(y<275*WindowHeight/720 and y>230*WindowHeight/720):
				bColor[2]=red
				bSize[2]=0.4
				
	if (x>=128*WindowWidth/1280 and x<=400*WindowWidth/1280): #CREDITS
		if(y<215*WindowHeight/720 and y>170*WindowHeight/720):
				bColor[3]=red
				bSize[3]=0.4
				
	if (x>=128*WindowWidth/1280 and x<=300*WindowWidth/1280): #EXIT
		if(y<160*WindowHeight/720 and y>115*WindowHeight/720):
				bColor[4]=red
				bSize[4]=0.4
				


def MouseClick(key,state,x,y):
	global WindowHeight,WindowHeight,blue
	global intro,introCounter,main_menu,loadscreen,settings,credits,bColor,t,red
	global fullscreen,sfx_volume,bgm_volume,bSound1,bSound2,crdY,menu_to_game,NewGameSound

	if main_menu and not menu_to_game:
		if bColor[0]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				#main_menu=0
				settings=0
				if not menu_to_game:
					bSound2.play()
					NewGameSound.play()
				menu_to_game=1
		if bColor[1]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				print("LOAD GAME")
				bSound2.play()
		if bColor[2]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				bSound2.play()
				settings,main_menu=1,0
		if bColor[3]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				bSound2.play()
				main_menu,credits=0,1
		if bColor[4]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				bSound2.play()
				sys.exit()

	elif settings:
		if bColor[1]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				bSound2.play()
				if fullscreen:
					fullscreen=0
				else:
					fullscreen=1
		if bColor[2]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				bSound2.play()
				if bgm_volume==100:
					bgm_volume=0
				else:
					bgm_volume+=10
		if bColor[3]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				bSound2.play()
				if sfx_volume==100:
					sfx_volume=0
				else:
					sfx_volume+=10
		if bColor[4]==red:
			if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
				bSound2.play()
				settings,main_menu=0,1


def reshape(w,h): #RESHAPE FUNCTION TO FIX THE WINDOW SIZE, NOT USED CURRENTLY.
	glutReshapeWindow(WindowWidth,WindowHeight)

def keys(key,x,y):
	global intro,introCounter,main_menu,loadscreen,settings,credits,bColor,t,red
	global fullscreen,sfx_volume,bgm_volume,bSound1,bSound2,crdY,menu_to_game,NewGameSound
	if intro:
		if key==b'\x1b': #ESCAPE BUTTON \x1b
			intro=0
			introCounter=450 #THIS IS RELATED TO THE MOUSE PROBLEM
			main_menu=1
		if key==b' ':
			introCounter+=100-(introCounter%100)
			t=0

	if main_menu and not menu_to_game:
		if key==b'\r': #ENTER BUTTON \r
			if bColor[0]==red:
				#main_menu=0
				settings=0
				if not menu_to_game:
					bSound2.play()
					NewGameSound.play()
				menu_to_game=1
			if bColor[1]==red:
				print("LOAD GAME")
			if bColor[2]==red:
				main_menu,settings=0,1
			if bColor[3]==red:
				main_menu,credits=0,1
			if bColor[4]==red:
				sys.exit()

	elif settings:
		bSound2.play()
		if key==b'\r':
			if bColor[1]==red:
				if fullscreen:
					fullscreen=0
				else:
					fullscreen=1
			if bColor[2]==red:
				if bgm_volume==100:
					bgm_volume=0
				else:
					bgm_volume+=10
			if bColor[3]==red:
				if sfx_volume==100:
					sfx_volume=0
				else:
					sfx_volume+=10
			if bColor[4]==red:
				settings,main_menu=0,1
	elif credits:
		if key==b' ':
			crdY+=7

currentButton=0 #CURRENT BUTTON SELECTED BY KEYBOARD
upArrow,downArrow=101,103 #VALUES FOR UP AND DOWN ARROW
def spKeys(key,x,y):
	global bColor,currentButton,upArrow,downArrow,main_menu,settings,bSound1,bSound2,menu_to_game

	if main_menu and not menu_to_game:

		if key==upArrow:
			bSound1.play()
			bSize[currentButton]=0.35
			if currentButton==0:
				currentButton=4
			else:
				currentButton-=1
			bColor=[white,white,white,white,white]
			bSize[currentButton]=0.4
			bColor[currentButton]=red
			

		elif key==downArrow:
			bSound1.play()
			bSize[currentButton]=0.35
			if currentButton==4:
				currentButton=0
			else:
				currentButton+=1
			bColor=[white,white,white,white,white]
			bColor[currentButton]=red
			bSize[currentButton]=0.4
			

	if settings:

		if key==upArrow:
			bSound1.play()
			bSize[currentButton]=0.35
			if currentButton==1:
				currentButton=4
			else:
				currentButton-=1
			bColor=[white,white,white,white,white]
			bSize[currentButton]=0.4
			bColor[currentButton]=red
			

		elif key==downArrow:
			bSound1.play()
			bSize[currentButton]=0.35
			if currentButton==4:
				currentButton=1
			else:
				currentButton+=1
			bColor=[white,white,white,white,white]
			bColor[currentButton]=red
			bSize[currentButton]=0.4

def Timer(v):
	global intro,main_menu,loadscreen,credits
	if intro:
		displayIntro()			
	elif main_menu:
		displayMenu()
	elif settings:
		displaySettings()
	elif loadscreen:
		displayLoading()
	elif credits:
		displayCredits()
	if gameplay:
		main1()
	glutTimerFunc(30,Timer,1)


def main():
	global WindowHeight,WindowWidth,intro,main_menu,current_W,current_H,fullscreen
	global bSound1,bSound2,bgm_volume,sfx_volume,bgm,bgm2,NewGameSound
	glutInit()
	fullscreen=0
	pygame.mixer.init()
	NewGameSound=pygame.mixer.Sound("Menu\Audio\FarScream.wav")
	bSound1=pygame.mixer.Sound("Menu\Audio\ButtonScroll.wav")
	bSound2=pygame.mixer.Sound("Menu\Audio\ButtonSelect.wav")
	bgm=pygame.mixer.Sound("Menu\Audio\mainSound.wav")
	bgm2=pygame.mixer.Sound("Menu\Audio\Lamp.wav")
	
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(WindowWidth,WindowHeight)

	glutCreateWindow(b"Test")
	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)
	glutDisplayFunc(displayIntro)
	#glutReshapeFunc(reshape)
	if fullscreen:
		glutFullScreen()
	glutSpecialFunc(spKeys)
	glutKeyboardFunc(keys)
	glutPassiveMotionFunc(Mouse)
	glutMouseFunc(MouseClick)
	glutTimerFunc(30,Timer,1)
	init()
	glutMainLoop()

main()