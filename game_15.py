# John Dowling and Jay Huskins
# CS269 Game Design
# Jan 2017
# Avoid the Ex
import pygame
import math
import sys
import random
import re

class Gamestate():
	#psuedo enum class to control game flow
	def __init__(self):
		self.values = ["play", "win", "lose"]
		self.cur = self.values[0]
	def goto(self, string):
		for val in self.values:
			if val == string:
				self.cur = val

class Spritesheet(object):
	def __init__(self, filename):
		try:
			self.sheet = pygame.image.load(filename).convert()
		except pygame.error, message:
			print 'Unable to load spritesheet image:', filename
			raise SystemExit, message
	# Load a specific image from a specific rectangle
	def image_at(self, rectangle, colorkey = None):
		"Loads image from x,y,x+offset,y+offset"
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0, 0), rect)
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, pygame.RLEACCEL)
		return image
	# Load a whole bunch of images and return them as a list
	def images_at(self, rects, colorkey = None):
		"Loads multiple images, supply a list of coordinates" 
		return [self.image_at(rect, colorkey) for rect in rects]
	# Load a whole strip of images
	def load_strip(self, rect, image_count, colorkey = None):
		"Loads a strip of images and returns them as a list"
		tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
		return self.images_at(tups, colorkey)

class Player:
	#controls player rules/art
	def __init__(self, x, y, size, speed):
		self.rect = pygame.Rect(x,y, size, size)
		self.speed = int(speed)
		self.date = 0
		self.dir = 1
	def set_Size(self, size):
		self.rect = pygame.Rect(self.rect.x, self.rect.y, size, size)
	def collide(self):
		for rect in MAP:
			if rect.colliderect(self.rect):
				return True# player is in at least 1 rect
		return False #player is not in any rect
	def up(self):
		self.rect.move_ip(0, -1*self.speed)
		if self.collide():
			self.rect.move_ip(0, self.speed)
		else:
			self.dir = 2
	def down(self):
		self.rect.move_ip(0, self.speed)
		if self.collide():
			self.rect.move_ip(0, -1*self.speed)
		else:
			self.dir = 3
	def left(self):
		self.rect.move_ip(-1*self.speed, 0)
		if self.collide():
			self.rect.move_ip(self.speed, 0)
		else:
			self.dir = 0
	def right(self):
		self.rect.move_ip(self.speed, 0)
		if self.collide():
			self.rect.move_ip(-1*self.speed, 0)
		else:
			self.dir = 1
	def draw(self, screen):
		if self.date:
			screen.blit(playerwD[self.dir], (self.rect.x, self.rect.y))
		else:
			screen.blit(playerPic[self.dir], (self.rect.x, self.rect.y))
		#pygame.draw.rect(screen, WHITE, self.rect)
	def isAt(self, x0, y0, err):
		if math.fabs(self.rect.centerx - x0) < err and math.fabs(self.rect.centery - y0) <err:
			return True
		return False
	def isDead(self, exes):
		for ex in exes:
			if math.hypot(self.rect.centerx - ex.x, self.rect.centery - ex.y) < (ex.r*.7)+self.rect.width:
			   return True
		return False

class Exes:
	#stores ex data and design
	def __init__(self, x0, y0, x1 = math.pi, y1 =math.pi, speed = 1, radius = 20):
		self.x = x0
		self.y = y0
		self.start = (x0, y0)
		self.end = (x1, y1)
		if x1 == y1 and x1 == math.pi:
			self.end = (x0, y0)
		self.toEnd = True
		self.speed = speed
		self.r = int(radius)
	def draw(self, screen):
		screen.blit(exPic, (self.x - self.r*1.15, self.y -self.r*1.15), None, 0)
	def move(self):
		if (self.x, self.y) == self.end and self.toEnd:
			self.toEnd = False
		if (self.x, self.y) == self.start and not self.toEnd:
			self.toEnd = True
		if self.toEnd:
			goal = self.end
		else:
			goal = self.start
		tempX = self.x
		if self.x != goal[0]:
			self.x += math.copysign(self.speed + (goal[0] -self.x) % self.speed, (goal[0] - self.x))
		# if x value is correct, move vertically
		if tempX == self.x and self.y != goal[1]:
			self.y += math.copysign(self.speed + (goal[1] - self.y) % self.speed, (goal[1] - self.y))

def globals():
	global LEVEL ####
	LEVEL = 1 ####
	global LIVES #!
	LIVES = 3

	#define colors
	global BLACK
	BLACK = (0, 0, 0)
	global WHITE 
	WHITE= (255, 255, 255)
	global RED
	RED = (255, 0, 0)
	global GREEN 
	GREEN= (0, 255, 0)
	global BLUE 
	BLUE= (0,0, 255)
	global CYAN
	CYAN = (0, 255, 255)
	global MAGENTA
	MAGENTA = (255, 0, 255)
	global YELLOW
	YELLOW = (255,255,0)

	#screen size
	global WIDTH
	WIDTH = 960
	global HEIGHT
	HEIGHT = 540

	#define RECTS
	global MAP
	borders = [pygame.Rect(0,0, WIDTH, -1), pygame.Rect(0,0, -1, HEIGHT), pygame.Rect(0,HEIGHT-1, WIDTH, -1), 
			pygame.Rect(WIDTH-1,0, -1, HEIGHT),]
	MAP = borders + [pygame.Rect(60,60,60,60), pygame.Rect(60,180,120,180), pygame.Rect(60,420,60,60), 
			pygame.Rect(180,0,60,480), pygame.Rect(300,60,150,240), pygame.Rect(300,360,150,120), 
			pygame.Rect(510,60,150,120), pygame.Rect(510,240,150,240), pygame.Rect(720,60,60,480), 
			pygame.Rect(840,60,60,60), pygame.Rect(780,180,120,180), pygame.Rect(840,420,60,60) ]
	#fonts
	global font
	font = pygame.font.SysFont("monospace", 30)
	global afont
	afont = pygame.font.SysFont( "Helvetica", 20, bold=False )
	global bfont
	bfont = pygame.font.SysFont( "Helvetica", 40, bold=True )
	global cfont
	cfont = pygame.font.SysFont( "Helvetica", 60, bold=True )
	#screen
	global screen
	screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
	pygame.display.set_caption("Avoid the Ex")
	#images
	global startScreen
	startScreen = pygame.image.load("ATEStartScreen.png").convert_alpha()
	global loseScreen
	loseScreen = pygame.image.load("YouLose.png").convert_alpha()
	global winScreen
	winScreen =  pygame.image.load("YouWin.png").convert_alpha()
	global exPic
	exPic = pygame.image.load("Ex2.png").convert_alpha()
	global endLight
	endLight = pygame.image.load("Streetlight.png").convert_alpha()
	global playerPic
	playerPic = Spritesheet("PlayerStrip2.png").load_strip(pygame.Rect(0,0,28,28), 4)
	global playerwD
	playerwD = Spritesheet("PlayerStrip3.png").load_strip(pygame.Rect(0,0,35,35), 4)
	global datePic
	datePic = Spritesheet("Date4.png").load_strip(pygame.Rect(0,0,48,48), 2)
	#fps tracker
	global fpsList
	fpsList = []

def updateScoreFile(text): ####
	newHighScore.close() #### you'll get a syntax warning in the terminal for this, but not to worry, it is not used before its definition
	global newHighScore #### need to make the variable global again when you redefine it
	newHighScore = file('highscore.txt','w')
	for line in text:
		newHighScore.write(line)

def readNum(string): #### in order to return strings of decimals at the varying lengths
	if string[4] == ',':
		return 4
	if string[5] == ',':
		return 5
	else:
		return 6

def getFPS():
	avg = 0
	for x in fpsList:
		avg += x
	avg = (avg/len(fpsList))
	print "\nfps: " + str(avg)

def getDesign(setup):
	text = open("lvl_" + str(setup)  + ".txt")
	read = re.split('\W+', text.read())
	design = [int(x) for x in read if x.isdigit()]
	return design

def system():

	button1 = pygame.Rect(35, 448, 164, 66)
	button2 = pygame.Rect(278, 448, 164, 66)
	button3 = pygame.Rect(521, 448, 164, 66)

	text1 = afont.render( "START", True, CYAN )
	text1altered = afont.render( "START", True, WHITE )
	text2 = afont.render( "How to Play", True, CYAN )
	text2altered = afont.render( "How to Play", True, WHITE )
	text3 = afont.render( "QUIT", True, CYAN )
	text3altered = afont.render( "QUIT", True, WHITE )

	t1pos = (button1.x + button1.width/3,  button1.y + button1.height/3)
	t2pos = (button2.x + button2.width/4,  button2.y + button2.height/3)
	t3pos = (button3.x + 3*button3.width/8,  button3.y + button3.height/3)

	text1focus = False
	text2focus = False
	text3focus = False

	screen.fill(BLACK)
	screen.blit(startScreen, (0,0) )
	pygame.display.update()

	win = False
	played = False
	skill = 1
	setup = 1
	while 1:

		mpos = pygame.mouse.get_pos()
		
		if played:
			if LIVES == 0:
				text1 = afont.render( "Restart Game", True, CYAN ) #!
				text1altered = afont.render( "Restart Game", True, WHITE ) #!
				t1pos = (button1.x + button1.width/5, button1.y + button1.height/3)
			else:
				text1 = afont.render( "Replay level", True, CYAN ) #!
				text1altered = afont.render( "Replay level", True, WHITE ) #!
				t1pos = (button1.x + button1.width/4, button1.y + button1.height/3)
			text2 = afont.render( "", True, CYAN )
			text2altered = afont.render( "", True, CYAN )
		if win:
			text2 = afont.render( "Next Level", True, CYAN )
			text2altered = afont.render( "Next Level", True, WHITE )


		if button1.collidepoint(mpos):
			text1focus = True
		elif button2.collidepoint(mpos):
			text2focus = True
		elif button3.collidepoint(mpos):
			text3focus = True
		else:
			text1focus = False
			text2focus = False
			text3focus = False
		
		if text1focus:
			screen.blit(text1altered, t1pos)
		else:
			screen.blit( text1, t1pos )
		if text2focus:
			screen.blit( text2altered, t2pos )
		else:
			screen.blit( text2, t2pos )
		if text3focus:
			screen.blit( text3altered, t3pos)
		else:
			screen.blit(text3, t3pos)

		pygame.display.update()
			
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if text1focus:
					if played and not win: #!
						if LIVES == 0:
							global LIVES
							LIVES = 3
							global LEVEL
							LEVEL = 1 #!
							setup = 1
							skill = 1
					win = play(skill, getDesign(setup))
					played = True
				elif text2focus:
					if win:
						skill += 1
						if getDesign(setup)[(-1*skill)] == 9999:
							skill = 1
							setup += 1
						global LEVEL #### need to call this or else it treats LEVEL as a local variable
						LEVEL += 1 ####
						win = play(skill, getDesign(setup))
					elif not played: ####
						showInstructions()
				elif text3focus:
					getFPS()
					sys.exit()

			if event.type == pygame.QUIT:
				getFPS()
				sys.exit()

def play(skill, design):

	#controlled player
	player = Player( design[0], design[1], 28, 5)

	#date
	goal_x = design[2]
	goal_y = design[3]
	goal_r = 20
	dateFrame = 0
	dateFrameCourse = True

	#end Location
	end_x = design[4]
	end_y = design[5]

	#enemies
	exes = []
	for i in range(6, len(design[6:design.index(9999)]) + 6, 4):
		exes.append(Exes(design[i], design[i+1], design[i+2], design[i+3], design[(-1*skill)], 30))

	#timing
	clock = pygame.time.Clock()
	timeInit = pygame.time.get_ticks()
	timeNum = 0

	#manages the gamestate
	game = Gamestate()

	# Loop until the user clicks the close button.
	done = False

	# -------- Main Program Loop -----------
	while not done:
		if game.cur == "play":
			# --- Main event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					getFPS()
					sys.exit()
			#key pressed
			if( pygame.key.get_pressed()[pygame.K_UP] != 0 ):
				player.up()
			if( pygame.key.get_pressed()[pygame.K_DOWN] != 0 ):
				player.down()
			if( pygame.key.get_pressed()[pygame.K_LEFT] != 0 ):
				player.left()
			if( pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
				player.right()

			if player.isDead(exes):
				game.goto("lose")
			for ex in exes:
				ex.move()
			if player.isAt(goal_x, goal_y, goal_r*(.7)+player.rect.width) and not player.date:
				player.date = True
				player.set_Size(35)
			if player.date and player.isAt(end_x, end_y, goal_r*(.7)+player.rect.width):
				game.goto("win")
			
			if timeNum == 59:
				game.goto("lose")

			# clear the screen to black
			screen.fill(BLACK)
		 
			# --- Drawing code
			for rect in MAP[:4]:
				pygame.draw.rect( screen, BLACK, rect)
			for rect in MAP[4:]:
				pygame.draw.rect( screen, BLUE, rect)
			for ex in exes:
			   ex.draw(screen)
			if not player.date:
				screen.blit(datePic[dateFrame/10], (goal_x, goal_y))
				if dateFrameCourse:
					dateFrame += 1
					if dateFrame == 19:
						dateFrameCourse = False
				else:
					dateFrame -= 1
					if dateFrame == 0:
						dateFrameCourse = True
			else:
				screen.blit(endLight, (end_x - goal_r, end_y - goal_r))
			timeNum = (30+ int((pygame.time.get_ticks() - timeInit) / 1000))
			yourTime = float( '%.3f' % (30.0 + ( float(pygame.time.get_ticks()) - float(timeInit) ) / 1000.0)) #### we limit the time to 3 decimal places
			timer = font.render( "7:" + str(timeNum), 1, WHITE)
			screen.blit(timer, (520, 280))
			
			livesText = afont.render('Second chances: ' + str(LIVES), 1, WHITE) #!
			screen.blit(livesText, (0,0)) #!
			
			player.draw(screen)

		elif game.cur == "lose":
			screen.fill(BLACK)
			screen.blit(loseScreen, (0, 0))
			
			global LIVES #!
			LIVES -= 1 #!
			livesText = bfont.render('You have ' + str(LIVES) + ' second chances left', 1, RED) #!
			screen.blit(livesText, (WIDTH/4, 3*HEIGHT/4)) #!
			
			return False
		
		elif game.cur == "win":
			screen.fill(BLACK)
			screen.blit(winScreen, (0, 0))
			try:
				bestTimeString = str(prevHighScoreText[LEVEL-1])
				bestTimeList = []
				reference = True
			except:
				bestTimeString = "[59.0, 59.0, 59.0]\n"
				bestTimeList = []
				reference = False
			
			digits1 = readNum(bestTimeString[1:7])
			num1 = bestTimeString[1:1+digits1]
			digits2 = readNum(bestTimeString[3+digits1:9+digits1])
			num2 = bestTimeString[3+digits1:3+digits1+digits2]
			num3 = bestTimeString[5+digits1+digits2:-2]
			
			bestTimeList.append(float(num1))
			bestTimeList.append(float(num2))
			bestTimeList.append(float(num3))
			
			if reference:
				prevHighScoreText[LEVEL-1] = bestTimeList
			else:
				prevHighScoreText.append(bestTimeList)

			if yourTime < bestTimeList[2]:
				prevHighScoreText[LEVEL-1][2] = yourTime
				prevHighScoreText[LEVEL-1].sort()
				prevHighScoreText[LEVEL-1] = str(prevHighScoreText[LEVEL-1])+'\n'
				updateScoreFile(prevHighScoreText)
			else:
				prevHighScoreText[LEVEL-1] = str(prevHighScoreText[LEVEL-1])+'\n'
				updateScoreFile(prevHighScoreText)

			bestTimeText1 = bfont.render("%.3f" % bestTimeList[0], True, WHITE)
			bestTimeText2 = bfont.render("%.3f" % bestTimeList[1], True, WHITE)
			bestTimeText3 = bfont.render("%.3f" % bestTimeList[2], True, WHITE)
			yourTimeText = cfont.render("%.3f" % yourTime, True, WHITE)
			screen.blit(bestTimeText1, (WIDTH/2 + 50, HEIGHT/2 + 2) )
			screen.blit(bestTimeText2, (WIDTH/2 + 40, HEIGHT/2 + 46) )
			screen.blit(bestTimeText3, (WIDTH/2 + 40, HEIGHT/2 + 89) )
			screen.blit(yourTimeText, (WIDTH/6, HEIGHT/2) )

			return True

		# --- update the screen
		pygame.display.flip()

	 
		# --- Limit to 60 frames per second
		global fpsList
		fpsList.append(clock.get_fps())
		clock.tick(60)

def showInstructions():
	screen.fill((0,0,0))
	instructionsText = afont.render( "Instructions go here", True, CYAN ) ####CYAN
	returnText = afont.render( "Return to title screen", True, CYAN ) ####CYAN
	rtpos = (750,450)
	screen.blit(instructionsText, (420,250) )
	screen.blit(returnText, rtpos )
	
	pygame.display.update()
	
	
	rtfocus = False
	while 1:
		mpos = pygame.mouse.get_pos()
		rtrect = returnText.get_rect()
		if mpos[0]>rtpos[0] and mpos[0]<rtpos[0]+rtrect[2] and mpos[1]>rtpos[1] and mpos[1]<rtpos[1]+rtrect[3]:
			rtfocus = True
			
			rtaltered = afont.render( "Return to title screen", True, WHITE ) ####WHITE
			
			screen.fill(BLACK, rtrect ) ####BLACK
			screen.blit(rtaltered, rtpos )
			
		else:
			rtfocus = False
			
			screen.fill(BLACK, rtrect ) ####BLACK
			screen.blit(returnText, rtpos )

		pygame.display.update()
			
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if rtfocus:
					showTitle(screen)
			if event.type == pygame.QUIT:
				getFPS()
				sys.exit()


if __name__ == '__main__':
	pygame.font.init()
	globals()
	
	try: ####
		prevHighScore = file('highscore.txt','r') #### reads in any previous text in the file
	except: #### if the file does not exist, it will encounter an error which is avoided with the try/except statement
		prevHighScore = file('highscore.txt','w')
		prevHighScore.close()
		prevHighScore = file('highscore.txt','r') #### creates the file if it does not exist
	prevHighScoreText = prevHighScore.readlines()
	print prevHighScoreText
	prevHighScore.close()
	global newHighScore #### need to make this global so that we can write to it from anywhere
	newHighScore = file('highscore.txt','w') #### allows us to write to it
	for line in prevHighScoreText:
		newHighScore.write(line) #### rewrites the old high score to the file to preserve it if it is not beaten
	
	system()