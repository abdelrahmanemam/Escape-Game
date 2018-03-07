from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
#GAME FILES
from Loader import *
from Player import *
from Texture import *
from Collision import *
from Zombie import *
from Object import *
from World import *
#NEEDED LIBRARIES
from math import *
import sys, pygame,os,numpy,time

#Variables needed
global player1,fovy,window_width,window_height,fullscreen,fireSound,windSound,zombieSound,footSound,world1,yHouse
global paused,sound_BGM,sound_game,worldAudio,houseAudio,houseMusic,windSound,doorSound,doorSlam,axeSound,manSound,dead

dead=0
paused=0
paused_settings=0

white=[1,1,1]
blue=[1,0,0]
blue=[0,0,1]
green=[0,1,0]
bSize=[0.35,0.35,0.35,0.35,0.35]
bColor=[white,white,white,white,white]


alist1=[#Horizontal walls
		[0,0],[1,0],
		[2,0],[18,0],
		[0,4],[6,4],
		[6,6],[13,6],
		[15,3],[18,3],
		[15,6],[18,6],
		[0,9],[2,9],
		[4,9],[18,9],
		#Vertical Walls
		[0,0],[0,9],
		[6,0],[6,1.5],
		[6,2.5],[6,7],
		[6,8],[6,9],
		[13,0],[13,1.5],
		[13,2.5],[13,7],
		[13,8],[13,9],
		[15,0],[15,1],
		[15,2],[15,4],
		[15,5],[15,7],
		[15,8],[15,9],
		[18,0],[18,9],
		#Stairs
		[14,3],[14,7]
		]


lisZombies=[]
lisTexture=[]
lisObjs=[]
lisTools=[]
lisDoors=[]
lisSpecialDoors=[]
lisHouse=[]

#List of zero initialized states for all keyboard inputs
keyState=[0 for i in range(0,256)]


#30ms per frame for Timer function
time_interval=30
PI=3.14159265359

#Pause menu images (textures holders)
pauseimage_id,pauseimage=0,0

def any_line(x0,y0,x1,y1, R,G,B): 
        """ Specification of the line position and color. 
        """
        glColor(R,G,B)
        glLoadIdentity()
        glBegin(GL_LINES) 
        glVertex(x0, y0,0) 
        glVertex(x1, y1,0) 
        glEnd() 
R,G,B,R1,G1,B1=0,0,0,0,0,0

#k,k1=0,0
def DrawGLScene(): 
        """ Specification of the line position and color. 
        """      
        
 
        
        glLineWidth(10.0)
        #def health(p=3,e=100):
        global R,G,B,R1,B1,G1,p,pc,e,ec,k,k1    
        e=player1.health

        if e>75:
                R1,G1,B1=0,1,1
                k1=(e/100)-1
        elif e>50 :
                R1,G1,B1=0,0,1
                k1=(e/100)-1
        elif e<=30:
        		k1=-.7
       
       # any_line(-1.6,1.5,-.6+k,1.5, R,G,B ) # Our line to be drawn.left 
        any_line(0.7-k1,0.9,1,0.9,R1,G1,B1 ) #right
#Pause menu image initialization
def texInit(name,id):
	global pauseimage_id,pauseimage
	imgload=pygame.image.load(name) #LOAD IMAGE
	imgdata=pygame.image.tostring(imgload,"RGB",1) #CONVERT IMAGE TO RAW DATA
	width=imgload.get_width()
	height=imgload.get_height()
	glBindTexture(GL_TEXTURE_2D, pauseimage_id[id]) #GIVE IT AN ID THEN SET PARAMETERS
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB,width,height,0,GL_RGB,GL_UNSIGNED_BYTE,imgdata)
	#ASSING THE IMAGE TO A 2D TEXTURE WITH THE GIVEN SPECIFICATIONS ^

#OPENGL Initialization for the in-game scene.
def init1():
	global pauseimage_id,pauseimage
	glClearColor(1,1,1,0)
	glutSetCursor(GLUT_CURSOR_NONE)
	glEnable(GL_LIGHTING)
	
	#Flash Light
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.2, 0.2, 0.2, 1.0])
	glLightfv(GL_LIGHT0, GL_SPECULAR, [0, 0, 0, 0.0])

	#World Light "Moon"
	glEnable(GL_LIGHT1)
	glLightfv(GL_LIGHT1, GL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
	glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.01, 0.01, 0.01, 1.0])
	glLightfv(GL_LIGHT1, GL_SPECULAR, [1, 1, 1, 1.0])
	
	#Disabling glColor effects.
	glDisable(GL_COLOR_MATERIAL)

	#Making a glList for drawing pause menu background later.
	pauseimage_id=glGenTextures(2)
	texInit("Menu\Images\Paused.jpg",0)
	pauseimage=glGenLists(1) #GENERATE A GL.LIST THAT APPLIES ANY GIVEN TEXTURE
	glNewList(pauseimage,GL_COMPILE) #COMPLIE THE LIST -- BEGIN
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

	glEnable(GL_DEPTH_TEST)
	glEnable(GL_BLEND)

	#Ignore repeated consecutive inputs
	glutIgnoreKeyRepeat( GL_TRUE )
	if(fullscreen):
		glutFullScreen()

#READING SAVED SETTINGS IN THE OPTION FILE
def setting():
	global window_width,window_height,fullscreen,fovy,sound_BGM,sound_game
	f= open('Option/op.in').read().split()
	window_width=int(f[2])
	window_height=int(f[5])
	fullscreen=int(f[8])
	fovy=int(f[11])
	sound_BGM=int(f[14])
	sound_game=int(f[17])

#DISPLAY FUNCTION FOR THE PAUSE MENU
def displayPause():
	global current_H,current_W,white,blue,blue,bColor,bSize
	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)
	glClearColor(0,0,0,0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0,1280,0,720,-3,3)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glBindTexture(GL_TEXTURE_2D, pauseimage_id[0])
	glCallList(pauseimage)
	drawTextB(bColor[0], "SAVE GAME", 128, 345.6, bSize[0])
	drawTextB(bColor[1], "LOAD GAME", 128, 288, bSize[1])
	drawTextB(bColor[2], "SETTINGS", 128, 230.4, bSize[2])
	drawTextB(bColor[3], "EXIT",  128, 172.8, bSize[3])
	glColor(1,1,1)
	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(window_width, window_height)
	glutSwapBuffers()

#DISPLAY FUNCTION FOR THE SETTINGS SCREEN IN PAUSE MENU
def displaySettings():
	global bColor,bSize,white,blue,blue
	global current_W,current_H,fullscreen,sound_game,sound_BGM,bSound1,bSound2,axeSound,manSound
	glClearColor(0,0,0,0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0,1280,0,720,-3,3)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glBindTexture(GL_TEXTURE_2D, pauseimage_id[0])
	glCallList(pauseimage)

	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)
	glBindTexture(GL_TEXTURE_2D, pauseimage_id[0])
	glCallList(pauseimage)

	drawTextB([.5,.5,.6], "SETTINGS", 128, 450, 0.3)
	drawTextB([.4,.4,.4], "GRAHPICS", 128, 345.6, 0.4)
	if fullscreen:
		drawTextB(bColor[1], "FULLSCREEN", 128, 288, bSize[1])
	else:
		drawTextB(bColor[1], "WINDOWED", 128, 288, bSize[1])
	drawTextB(bColor[2], "MUSIC: "+str(sound_BGM), 128, 230.4, bSize[2])
	drawTextB(bColor[3], "SOUNDS: "+str(sound_game), 128, 172.8, bSize[3])
	drawTextB(bColor[4], "BACK", 128, 115.2, bSize[4])
	glColor(1,1,1)

	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(window_width, window_height)

	#EDITING SOUNDS AND SCREEN MODE VALUES
	bSound1.set_volume(.01*sound_game)
	bSound2.set_volume(.01*sound_game)
	fireSound.set_volume(0.1*sound_game)
	axeSound.set_volume(0.1*sound_game)
	manSound.set_volume(0.1*sound_game)
	windSound.set_volume(0.04*sound_BGM)
	houseMusic.set_volume(0.02*sound_BGM)
	zombieSound.set_volume(0.1*sound_game)
	footSound.set_volume(0.1*sound_game)
	doorSound.set_volume(0.1*sound_game)
	doorSlam.set_volume(0.1*sound_game)

	#ACCESSING THE OP FILE INDEXES THEN OVER WRITING
	opfile=open('Option/op.in','r')
	setOp=opfile.read().split()
	setOp[8]=str(fullscreen)
	setOp[14]=str(sound_BGM)
	setOp[17]=str(sound_game)
	opfile=open('Option/op.in','w')
	for item in setOp:
		opfile.write(str(item))
		opfile.write(" ")
	opfile.close()
	glutSwapBuffers()

#FUNCTION FOR BULLET COLLISION DETECTION WITH ZOMBIE
def bullet(player, enemy):
	#Bullet Direction
	xd=-sin(player.theta)
	yd=sin(player.thetaUp)
	zd=cos(player.theta)
	#Player Position
	xs=player.x
	ys=player.y
	zs=player.z
	#Zombie Position
	xc=enemy.x
	yc=enemy.y+7
	zc=enemy.z

	#This variable represents the zombie's head (sphere) radius.
	r=0.5

	#THE MATH - HIT OR NOT?
	a=xd**2+yd**2+zd**2
	b = 2*(xd*(xs-xc)+ yd*(ys-yc) + zd*(zs-zc))
	c = (xs-xc)**2 + (ys-yc)**2 + (zs-zc)**2 - r**2
	M= b**2 - 4*a*c
	#SOLVING QUADRATIC EQUATION, NO SOL IF M<0
	return M>= 0

#AXE HITTING ENEMY - DETECTING FUNCTION
def axe(player,enemy):
	distance=((enemy.x-player.x)**2+(enemy.y-player.y+player.tall)**2+(enemy.z-player.z)**2)**0.5
	return distance<10

#Real Data: Window Width = 2.2 , Depth = .2 , Height = 1.8 , Y= 3+0.55
#DRAWING HOUSE WINDOWS WITH TRANSPARENT QUADS
def draw_window(x,y,z,scale,rot=0):
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glRotate(rot,0,1,0)
	glTranslate(x,y,z)
	glDisable(GL_LIGHTING) #This is needed to avoid glColor effects
	#Drawing a normal quad.
	glColor4f(0.3,0.3,0.4,0.7)
	glBegin(GL_QUADS)
	glVertex(0,0,0)
	glVertex(0,0,2.2*scale)
	glVertex(0,1.8*scale,2.2*scale)
	glVertex(0,1.8*scale,0)
	glEnd()

	glDisable(GL_BLEND)
	glEnable(GL_LIGHTING) #Re-enable lighting.
	glDisable(GL_COLOR_MATERIAL)


LastFps=0 #COUNTING FPS USING LAST AVERAGE WITH LAST FPS

#MAIN GAME DISPLAY FUNCTION

def display():

	global houseAudio,worldAudio,houseMusic,windSound,LastFps
	global current_H,current_W,dead

	global player1,yHouse

	t=time.time() #Store the time when we enter the function (to calculate the amount of time this function needs)

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	player1.updateCamera() #PROJECTION AND LOOK AT STUFF.
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glLightfv(GL_LIGHT0, GL_POSITION,  (player1.x, player1.y, player1.z,1))
	glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 25)
	glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [-sin(player1.theta), sin(player1.thetaUp), cos(player1.theta)])
	glLightf(GL_LIGHT0, GL_SPOT_EXPONENT,20)

	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)

	glDisable(GL_LIGHT0)
	glLoadIdentity()
	player1.displayTool()
	if(player1.x>90 and player1.x<95 and player1.z>19 and player1.z<37):
		yHouse=(player1.z-19)*5/6+world1.height(26,5)
	if(not(player1.x>25 and player1.x<115 and player1.z>4 and player1.z<49)):
		player1.jump(world1.height(player1.x,player1.z))
		yHouse=world1.height(player1.x,player1.z)
		if not worldAudio:
			houseMusic.fadeout(3000)
			windSound.play(loops=-1,fade_ms=3000)
			worldAudio=1
			houseAudio=0
	else:
		if keyState[ord("f")]:
			glEnable(GL_LIGHT0)
		player1.jump(yHouse)
		
		if not houseAudio:
			windSound.fadeout(3000)
			houseMusic.play(loops=-1,fade_ms=3000)
			worldAudio=0
			houseAudio=1


	glLoadIdentity()
	glLightfv(GL_LIGHT1, GL_POSITION,  (0, 999, 0, 0))

	
	#display all texture in the world (like sky)
	glDisable(GL_COLOR_MATERIAL)

	for i in range(len(lisTexture)):
		glLoadIdentity()
		glColor(1,1,1)
		glDisable(GL_LIGHTING)
		lisTexture[i].disp()
		glEnable(GL_LIGHTING)

	for i in range(len(lisHouse)):
		glLoadIdentity()
		lisHouse[i].disp()
	#display all object in the world
	for i in range(len(lisObjs)):
		glLoadIdentity()
		lisObjs[i][0].disp()
	for i in range(len(lisDoors)):
		glLoadIdentity()
		lisDoors[i][0].dispDoor(doorSound)
	#display all zombies,make them walk.
	for i in range(len(lisZombies)):
		lisZombies[i].height(world1.height(lisZombies[i].x,lisZombies[i].z))
		if(lisZombies[i].dist(player1,zombieSound)):
			player1.health-=10
			lisZombies[i].walk2(player1)
			if(player1.health<=0):
				paused=1
				dead=1

		glLoadIdentity()
		lisZombies[i].disp()
		lisZombies[i].walk(player1)
		#if(lisZombies[i].criticalHit()==False):
			#lisZombies[i7].hit()

	for i in range(len(lisSpecialDoors)):
		glLoadIdentity()
		lisSpecialDoors[i][0].dispDoor(doorSound)
		Epressed=near(player1,None,lisSpecialDoors,keyState)
		if(Epressed):
			Pass=displayPass()
			if Pass==lisSpecialDoors[i][2]:
				lisSpecialDoors[i][0].animation=1
				lisSpecialDoors[i][0].radius=-1
			else:
				goOrtho()
				drawText("wrong pass")
				backPrespective()
				


	glLoadIdentity()
	draw_window(25.3,22.5,10.9,4.2)

	world1.disp()
	player1.move(keyState,alist1,lisObjs,lisDoors,lisSpecialDoors)

	goOrtho()
	drawCursor()
	backPrespective()

	#goOrtho()
	#drawText(str(LastFps),-0.96,0.92,0.0005,2,1,0,0)
	#backPrespective()

	goOrtho()
	DrawGLScene()
	backPrespective()

	glutSwapBuffers()
	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(window_width, window_height)


#DRAWTEXT FUNC. FOR THE MENU BUTTONS - USES LIST
def khaled():
	glColor(1,1,1)
	glLineWidth(12)
	glBegin(GL_LINES)
	glVertex(0.5,0.5,0)
	glVertex(-0.5,0.5,0)
	glEnd()
def drawTextB(lis, string,x,y,textsize=0.35):
	glLineWidth(4)
	glLoadIdentity()
	glColor(lis[0],lis[1],lis[2]) #GIVEN THE COLOR IN A LIST
	glTranslate(x,y,1)
	glScale(textsize,textsize,textsize)
	string=string.encode()
	for char in string:
		glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, char)

#DRAWING THE CURSOR ON SCREEN
def drawCursor():
	#Fix the aspect ratio for the cursor (to not be stretched).
	ratio=window_width/window_height
	glLineWidth(1)
	glColor(1,1,1)
	glLoadIdentity()
	glBegin(GL_LINES)
	glVertex(0.04/ratio,0,0) #Fix the vertical line.
	glVertex(-0.04/ratio,0,0)
	glVertex(0,0.04,0)
	glVertex(0,-0.04,0)
	glEnd()

#ANOTHER DRAWTEXT FUNC. FOR IN GAME PURPOSE
def drawText(string, x, y,scale=0.0005,w=2,r=0,g=0,b=0):
	glLineWidth(w)
	glColor(r,g,b)  # Yellow Color
	glTranslate(x-len(string)/50,y,0)
	glScale(scale,scale,1)
	string = string.encode() # conversion from Unicode string to byte string
	for c in string:
		glutStrokeCharacter(GLUT_STROKE_ROMAN , c )  

#THIS FUNCTION CHANGES TO ORTHOGRAPHIC PROJECTION
#TO DISPLAY 2D STUFF ON SCREEN BEFORE GOING BACK PERSPECTIVE

def goOrtho():
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho(-1,1,-1,1,-1,1)
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	glDisable(GL_LIGHTING)

#THIS FUNCTION GOES BACK PERSPECTIVE AFTER
#DISPLAYING THE 2D STUFF

def backPrespective():
	glEnable(GL_LIGHTING)
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	

def displayPass():
	s=input("enter the pass:")
	return s

def Timer(v):
	global LastFps
	t=time.time()#store the time when we enter the function (to calculate the amount of time this function needs)
	global paused
	if paused and not paused_settings:
		glDisable(GL_LIGHTING) #WE DON'T NEED LIGHTING IN THE PAUSE MENU, DO WE?
		displayPause()
	elif paused and paused_settings:
		glDisable(GL_LIGHTING)
		displaySettings()
	else:
		glEnable(GL_LIGHTING)
		display()

	time_calculated=time.time()-t

	LastFps=int((1/(time_calculated)+LastFps)/2)

	if(time_interval-time_calculated*1000>0):
		t=time_interval-time_calculated*1000
	else:
		t=1

	glutTimerFunc(int(t),Timer,1)
1494670355
#call function if any key pressed 
def keyDown(key,xx,yy):
	global window_height,window_width,current_H,current_W
	global bSize,bColor,blue,white,blue,current_H,current_W,bSound1,bSound2
	global paused_settings,bColor,blue
	global fullscreen,sound_game,sound_BGM,bSound1,bSound2
	global player1,jum,keyState,paused,dead


	if not paused: #NOT PAUSE = IN GAME
		if key==b"\x1b": #ESCAPE BUTTON SETS THE GAME STATE TO PAUSE.
			paused=1
		if(key==b" "): #JUMP WITH SPACE
			player1.jumping=1
		if (key==b"f"): #IF PRESSED 'F' CHANGE THE KEYSTATE
			keyState[ord(key.decode('unicode_escape'))]=not keyState[ord(key.decode('unicode_escape'))]
		else:
			keyState[ord(key.decode('unicode_escape'))]=1

	else: #GAME IS PAUSED
		if key==b"\x1b" and not dead: #ESCAPE TO RETURN
			paused=0
		if not paused_settings: #NOT IN THE SETTINGS MENU
			if key==b'\r': #ENTER BUTTON
				if bColor[0]==blue:
					print("SAVE GAME")
				if bColor[1]==blue:
					print("LOAD GAME")
				if bColor[2]==blue:
					paused_settings=1
				if bColor[3]==blue:
					sys.exit()

		else: #IN THE SETTINGS MENU
			bSound2.play()
			if key==b'\r':
				if bColor[1]==blue:
					if fullscreen:
						fullscreen=0
					else:
						fullscreen=1
				if bColor[2]==blue:
					if sound_BGM==100:
						sound_BGM=0
					else:
						sound_BGM+=10
				if bColor[3]==blue:
					if sound_game==100:
						sound_game=0
					else:
						sound_game+=10
				if bColor[4]==blue:
					paused_settings=0

#THIS FUNCTION IS CALLED ON KEYBOARD RELEASING EVENT
def keyUp(key,xx,yy):
	global keyStates
	if not paused:
		if key != b"f": #ALL KEYS EXCEPT 'F' CHANGES STATE ON RELEASING THE BUTTON
				keyState[ord(key.decode('unicode_escape'))]=0


currentButton=0 #CURRENT BUTTON SELECTED BY KEYBOARD
upArrow,downArrow=101,103 #VALUES FOR UP AND DOWN ARROW
def specialKey(key,xx,yy):
	global bColor,currentButton,upArrow,downArrow
	global window_height,window_width,current_H,current_W
	global bSize,bColor,blue,white,blue,current_H,current_W,bSound1,bSound2
	global paused_settings,bColor,blue
	global fullscreen,sound_game,sound_BGM,bSound1,bSound2
	global player1, keyState


	if not paused:
		keyState[key]=1

	else:
		if not paused_settings:

			if key==upArrow:
				bSound1.play()
				bSize[currentButton]=0.35
				if currentButton==0: #WE ARE GOING UP FROM FIRST BUTTON
					currentButton=3 #GO TO LAST BUTTON
				else:
					currentButton-=1
				bColor=[white,white,white,white,white]
				bSize[currentButton]=0.4 #SIZE AND COLOR FOR CURRENT SELECTED BUTTON
				bColor[currentButton]=blue
				

			elif key==downArrow:
				bSound1.play()
				bSize[currentButton]=0.35
				if currentButton==3 or currentButton==4: #GOING DOWN FROM LAST BUTTON (MENU OR SETTINGS)
					currentButton=0 #GO TO FIRST BUTTON
				else:
					currentButton+=1
				bColor=[white,white,white,white,white]
				bColor[currentButton]=blue
				bSize[currentButton]=0.4
				

		else:
			#SETTINGS
			if key==upArrow:
				bSound1.play()
				bSize[currentButton]=0.35
				if currentButton==1:
					currentButton=4
				else:
					currentButton-=1
				bColor=[white,white,white,white,white]
				bSize[currentButton]=0.4
				bColor[currentButton]=blue
				

			elif key==downArrow:
				bSound1.play()
				bSize[currentButton]=0.35
				if currentButton==4:
					currentButton=1
				else:
					currentButton+=1
				bColor=[white,white,white,white,white]
				bColor[currentButton]=blue
				bSize[currentButton]=0.4

def specialKeyUp(key,xx,yy):
	keyState[key]=0
#get the mouse position in the screen 
def mouseMove(x,y):
	global window_height,window_width,PI,current_H,current_W
	global bSize,bColor,blue,white,blue,current_H,current_W,bSound1,bSound2
	global paused_settings,bColor,blue
	global fullscreen,sound_game,sound_BGM,bSound1,bSound2

	if paused:
		y=current_H-y #LET THE MOUSE COORDINATES START FROM BOTTOM LEFT NOT TOP LEFT
		y=y*window_height/current_H #FIXING THE MOUSE SCREEN AREA IF RESIZED
		x=x*window_width/current_W

		#RESET BUTTONS TO DEFAULTS IF NO HIGHLIGHTED
		bColor=[white,white,white,white,white]
		bSize=[0.35,0.35,0.35,0.35,0.35]
		#CHECK IF THE MOUSE IS NOW HIGHLIGHTING ANY BUTTON
		if (x>=128*window_width/1280 and x<=420*window_width/1280): #SAVE GAME
			if(y<390*window_height/720 and y>345*window_height/720):
					bColor[0]=blue
					bSize[0]=0.4
		
		if (x>=128*window_width/1280 and x<=460*window_width/1280): #LOADGAME
			if(y<330*window_height/720 and y>285*window_height/720):
					bColor[1]=blue
					bSize[1]=0.4
					
		if (x>=128*window_width/1280 and x<=430*window_width/1280): #SETTINGS
			if(y<275*window_height/720 and y>230*window_height/720):
					bColor[2]=blue
					bSize[2]=0.4
					
		if (x>=128*window_width/1280 and x<=400*window_width/1280): #EXIT
			if(y<215*window_height/720 and y>170*window_height/720):
					bColor[3]=blue
					bSize[3]=0.4
					
		if (x>=128*window_width/1280 and x<=300*window_width/1280): #EMPTY PLACE ((NOT NEEDED))
			if(y<160*window_height/720 and y>115*window_height/720):
					bColor[4]=blue
					bSize[4]=0.4
	else:
		if(x<2):
			glutWarpPointer( window_width-2 , y ) #AT THE END OF THE SCREEN MOVE THE MOUSE TO THE OTHER SIDE
		if(x>window_width-2):
			glutWarpPointer(2,y)

		player1.theta=(PI*x)/(window_width/2)-PI #MOUSE LOCATION INDICATES THETA AND THETA UP
		player1.thetaUp=-(PI*y)/(window_height)+PI/2
		#SOLVE THETA WITH X, THETA UP WITH Y ACCORDING TO ANGLE AND RESOLUTION

#MOUSE-CLICK FUCNTION
def mouseShoot(key,state,x,y):
	global window_height,window_width,PI,current_H,current_W
	global bSize,bColor,blue,white,blue,current_H,current_W,bSound1,bSound2
	global paused_settings,bColor,blue
	global fullscreen,sound_game,sound_BGM,bSound1,bSound2,axeSound,manSound
	if paused:
		if not paused_settings:
			if bColor[0]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					print("SAVE GAME")
					bSound2.play()
			if bColor[1]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					print("LOAD GAME")
					bSound2.play()
			if bColor[2]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					paused_settings=1
			if bColor[3]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					sys.exit()

		else: #SETTTINGS
			if bColor[1]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					if fullscreen:
						fullscreen=0
					else:
						fullscreen=1
			if bColor[2]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					if sound_BGM==100:
						sound_BGM=0
					else:
						sound_BGM+=10
			if bColor[3]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					if sound_game==100:
						sound_game=0
					else:
						sound_game+=10
			if bColor[4]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					paused_settings=0


	else:
		if(key==0 and state==0 and player1.animation==0):
			player1.animation=1
			if(player1.t==0):
				fireSound.stop()
				fireSound.play()
				for i in range(len(lisZombies)):
					if(bullet(player1,lisZombies[i]) ):
						lisZombies[i].zombieSound.fadeout(16000)
						manSound.play()
						del lisZombies[i] #Die
						break
			else:
				axeSound.stop()
				axeSound.play()
				for i in range(len(lisZombies)):
					if(axe(player1,lisZombies[i])):
						lisZombies[i].health-=50
					if(lisZombies[i].health<0):
						del lisZombies[i]
						break

		if((key==3 or key==4 )and state==0):
			player1.updateTool()
			#get next gun
			#play voice

def main1():
	t=time.time()#to calculate time needed to load the game
	global current_H,current_W,manSound
	global player1,lisTexture,fireSound,windSound,zombieSound,footSound,world1,alist1,yHouse,lisSpecialDoors,lisHouse
	global sound_BGM,sound_game,worldAudio,houseAudio,houseMusic,windSound,doorSound,doorSlam,bSound2,bSound1,axeSound
	pygame.init()
	setting()
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	init1()

	current_W=glutGet(GLUT_WINDOW_WIDTH) #IN CASE ANY RESHAPE HAPPENS
	current_H=glutGet(GLUT_WINDOW_HEIGHT) #GET NEW COORDINATES

	for i in range(len(alist1)):
		alist1[i][0]=alist1[i][0]*5+25
		alist1[i][1]=alist1[i][1]*5+4

	
	Zlis=[]
	G1lis=[]
	M1lis=[]


	for i in range(1,65,2):#156
		sr="Monster_"
		ss=""
		for j in range(0,5-int(log10(i))):
			ss+=str(0)
		sr+=ss+str(i)+".obj"
		Zlis.append(sr)	
	Zlis=[OBJ(Zlis[i],False,"Models/MonsterLowQ/Low/") for i in range (len(Zlis))]

	for i in range(1,11): #APPEND GUN FRAMES TO THE G1 LIST
		sr="Gun_"
		ss=""
		for j in range(0,5-int(log10(i))): #NAME_(NUMBER OF ZEROS)+FrameNo. Ex: GUN_000001.obj
			ss+=str(0) #APPEND NUMBER OF ZEROS
		sr+=ss+str(i)+".obj" #APPEND NUMBER OF THE FRAME + Extention
		G1lis.append(sr)
	G1lis=[OBJ(G1lis[i],False,"Models/Gun/") for i in range (len(G1lis))]


	for i in range(1,15): #APPEND FRAMES FOR AXE TO MELEE 1 LIST
		sr="Axe_"
		ss=""
		for j in range(0,5-int(log10(i))):
			ss+=str(0)
		sr+=ss+str(i)+".obj"
		M1lis.append(sr)
	M1lis=[OBJ(M1lis[i],False,"Models/Axe/") for i in range (len(M1lis))]

	
	zombieSound=pygame.mixer.Sound("Sounds/zombieSound.wav")
	zombieSound.set_volume(0.1*sound_game)

	#CREATE ZOMBIES
	lisZombies.append(zombie(100,Zlis,[70,0,32],25,0.5,-90,zombieSound))
	lisZombies.append(zombie(100,Zlis,[105,0,14],15,0.5,-90,zombieSound))
	#lisZombies.append(zombie(100,Zlis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[-20,0,-20],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[30,0,0],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[0,0,50],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[1,0,1],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[5,0,30],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[0,0,30],30,0.5,-90))

	
	#CREATE THE SKYBOX
	lisTexture.append(texture('nightsky_up.jpg',[[-1,10000,-1],[-1,10000,1],[1,10000,1],[1,10000,-1]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_up.jpg',[[-1000,1000,-1000],[-1000,1000,1000],[1000,1000,1000],[1000,1000,-1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_ft.jpg',[[-1000,1000,1000],[-1000,-1000,1000],[1000,-1000,1000],[1000,1000,1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_lf.jpg',[[1000,1000,1000],[1000,-1000,1000],[1000,-1000,-1000],[1000,1000,-1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_bk.jpg',[[1000,1000,-1000],[1000,-1000,-1000],[-1000,-1000,-1000],[-1000,1000,-1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_rt.jpg',[[-1000,1000,-1000],[-1000,-1000,-1000],[-1000,-1000,1000],[-1000,1000,1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	#lisTexture.appedn(texture('Ghost1.jpeg',[[],[],[],[]],[[1,0],[0,0],[0,1],[1,1]],1))

	#RENDER THE WORLD FROM THE HEIGHTMAP
	world1=world('world.png',-500,-500) #TRANSLATE THE MAP TO -500,-500
	world1.render(4,100) #RESIZE IT 4x AND SET HEIGHT RATIO TO 100
	yHouse=world1.height(26,5) #HEIGHT OF HOUSE IS SET TO WORLD HEIGHT AT 26,5

	lisTexture.append(texture('Ghost1.jpeg',[[69,yHouse+10,4+0.5],[69,yHouse+10-5,4+0.5],[65,yHouse+10-5,4+0.5],[65,yHouse+10,4+0.5]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('Ghost2.jpeg',[[69+4,yHouse+10,34-0.6],[69+4,yHouse+10-5,34-0.6],[72+4,yHouse+10-5,34-0.6],[72+4,yHouse+10,34-0.6]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('Ghost3.jpeg',[[50,yHouse+10,4+0.5],[50,yHouse+10-5,4+0.5],[45,yHouse+10-5,4+0.5],[45,yHouse+10,4+0.5]],[[1,0],[0,0],[0,1],[1,1]],1))
	
	#LIST OF HOUSES MODELS CONTAIN OUR ONLY HOUSE MODEL
	lisHouse.append(obje([OBJ("House.obj",False,"Models/House/")],0,[25,yHouse+0.1,4],-1,0.05,0))

	#DOORS OBJECTS LIST TAKES THE DOOR MODEL
	Dlis=[OBJ("Door1.obj",False,"Models/Door1/")]
	
	#ENTERY DOOR
	lisDoors.append([obje(Dlis,0,[32.5,world1.height(32.5,4),4],3,0.05,0,0,1),"open the Door"])
	
	#FIRST FLOOR DOORS
	lisDoors.append([obje(Dlis,0,[55,world1.height(32.5,4),14],3,0.05,90,0,1),"open the Door"])
	lisSpecialDoors.append([obje(Dlis,0,[90,world1.height(32.5,4),14],3,0.05,90,1,0),"write the password","HELP!"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),11.5],3,0.05,90,0,1),"open the Door"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),26.5],3,0.05,90,0,1),"open the Door"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),41.5],3,0.05,90,0,1),"open the Door"])
	
	#SECOND FLOOR DOORS
	lisSpecialDoors.append([obje(Dlis,0,[100,world1.height(32.5,4)+15,41.5],3,0.05,90,0,0),"write the password","Done"])
	lisDoors.append([obje(Dlis,0,[90,world1.height(32.5,4)+15,41.5],3.5,0.05,90,1,1),"open the Door"])
	lisDoors.append([obje(Dlis,0,[55,world1.height(32.5,4)+15,41.5],3.5,0.05,90,1,1),"open the Door"])


	#CREATING THE SOUNDS
	axeSound=pygame.mixer.Sound("Sounds/Axe.wav")
	axeSound.set_volume(0.1*sound_game)

	fireSound=pygame.mixer.Sound("Sounds/gun_fire.wav")
	fireSound.set_volume(0.1*sound_game)

	manSound=pygame.mixer.Sound("Sounds/Breathing.wav")
	manSound.set_volume(0.1*sound_game)

	windSound=pygame.mixer.Sound("Sounds/Wind.wav")
	windSound.set_volume(0.04*sound_BGM)
	windSound.play(-1)
	worldAudio=1 #FLAG FOR CURRENT WORLD MUSIC STATE

	houseMusic=pygame.mixer.Sound("Sounds/Nightmare.wav")
	houseMusic.set_volume(0.02*sound_BGM)
	houseAudio=0 #FLAG FOR CURRENT HOUSE MUSIC STATE

	footSound=pygame.mixer.Sound("Sounds/FootStep.wav")
	footSound.set_volume(0.1*sound_game)

	doorSound=pygame.mixer.Sound("Sounds/DoorOpen.wav")
	doorSound.set_volume(0.1*sound_game)

	doorSlam=pygame.mixer.Sound("Sounds/DoorSlam.wav")
	doorSlam.set_volume(0.1*sound_game)

	bSound1=pygame.mixer.Sound("Menu\Audio\ButtonScroll.wav")
	bSound2=pygame.mixer.Sound("Menu\Audio\ButtonSelect.wav")

	#CREATE THE PLAYER (CAMERA)
	player1=player(fovy,window_width,window_height,footSound,[G1lis,M1lis])


	glutKeyboardFunc(keyDown)
	glutKeyboardUpFunc(keyUp)
	glutSpecialFunc(specialKey)
	glutSpecialUpFunc(specialKeyUp)
	glutPassiveMotionFunc(mouseMove)
	glutMouseFunc(mouseShoot)
	glutDisplayFunc(display)
	glutTimerFunc(time_interval,Timer,1)
	
	print((time.time()-t)*1000)#print the time needed to load 
	glutMainLoop()

if __name__=="__main__":
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(1366,768)
	glutInitWindowPosition(0,0)
	glutCreateWindow(b"WAR")
	main1()