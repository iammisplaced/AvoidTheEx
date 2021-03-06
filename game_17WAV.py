# John Dowling and Jay Huskins
# CS269 Game Design
# Jan 2017
# Avoid the Ex
import pygame
import math
import sys
import random
import re
from pygame import mixer

class Gamestate():
	#psuedo enum class to control game flow
	def __init__(self):
		self.values = ["play", "win", "lose"]
		self.cur = self.values[0]
	def goto(self, string):
		for val in self.values:
			if val == string:
				self.cur = val

class Player:
	#controls player rules/art
	def __init__(self, x, y, size, speed):
		self.rect = pygame.Rect(x,y, size, size)
		self.prevRect = pygame.Rect(x - speed,y - speed, size*2, size*2)
		self.speed = int(speed)
		self.date = 0
		self.dir = 1
		self.bounce = 0.0
	def set_Size(self, size):
		self.rect = pygame.Rect(self.rect.x, self.rect.y, size, size)
	def collide(self):
		for rect in MAP:
			if rect.colliderect(self.rect):
				return True# player is in at least 1 rect
		return False #player is not in any rect
	def move(self):
		self.prevRect.x = self.rect.x -self.speed
		self.prevRect.y = self.rect.y -self.speed
		self.bounce += .1
	def up(self):
		self.move()
		self.rect.move_ip(0, -1*self.speed)
		if self.collide():
			self.rect.move_ip(0, self.speed)
		else:
			self.dir = 2
	def down(self):
		self.move()
		self.rect.move_ip(0, self.speed)
		if self.collide():
			self.rect.move_ip(0, -1*self.speed)
		else:
			self.dir = 2
	def left(self):
		self.move()
		self.rect.move_ip(-1*self.speed, 0)
		if self.collide():
			self.rect.move_ip(self.speed, 0)
		else:
			self.dir = 0
	def right(self):
		self.move()
		self.rect.move_ip(self.speed, 0)
		if self.collide():
			self.rect.move_ip(-1*self.speed, 0)
		else:
			self.dir = 0
	def clean(self, screen):
		screen.blit(mapPic, (self.prevRect.x, self.prevRect.y), self.prevRect )
	def draw(self, screen):
		if self.bounce > 1.9:
			self.bounce = 0
		if self.date:
			screen.blit(playerwD[self.dir + int(self.bounce)], (self.rect.x, self.rect.y))
		else:
			screen.blit(playerList[self.dir + int(self.bounce)], (self.rect.x, self.rect.y))
		#pygame.draw.rect(screen, WHITE, self.rect)
	def isAt(self, x0, y0, err = 0):
		if math.hypot(self.rect.centerx - x0, self.rect.centery - y0) < err + self.rect.width*.8:
			return True
		return False
	def isDead(self, exes):
		for ex in exes:
			if self.isAt(ex.x, ex.y, ex.r*.65):
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
	def clean(self, screen):
		prevRect = pygame.Rect(self.x - self.r*1.15 - self.speed, self.y -self.r*1.15 - self.speed, 3*self.r + 2*self.speed, 3*self.r + 2*self.speed)
		screen.blit(mapPic, (self.x - self.r*1.15 - self.speed, self.y -self.r*1.15 - self.speed), prevRect )
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
	#gameplay
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
	afont = pygame.font.SysFont( "Helvetica", 20, bold= False)
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
	global instr
	instr = [pygame.image.load('instrLeft.png').convert_alpha(), pygame.image.load('instrRight.png').convert_alpha(), 
	pygame.image.load('instrUp.png').convert_alpha(), pygame.image.load('instrDown.png').convert_alpha(), 
	pygame.image.load('instr1.png').convert_alpha(), pygame.image.load('instr2.png').convert_alpha(), pygame.image.load('instr3.png').convert_alpha()]
	global exPic
	exPic = pygame.image.load("Ex2.png").convert_alpha()
	global mapPic
	mapPic = pygame.image.load("ATEGameMap.png").convert_alpha()
	global endLight
	endLight = pygame.image.load("Streetlight.png").convert_alpha()
	global chance
	chance = pygame.image.load("Chance.png").convert_alpha()
	global playerList
	playerList = [pygame.image.load('Player1.png').convert_alpha(),pygame.image.load('Player2.png').convert_alpha(), 
	pygame.image.load('Player3.png').convert_alpha(), pygame.image.load('Player4.png').convert_alpha()]
	global playerwD
	playerwD = [pygame.image.load('player-date1.png').convert_alpha(),pygame.image.load('player-date2.png').convert_alpha(), 
	pygame.image.load('player-date3.png').convert_alpha(), pygame.image.load('player-date4.png').convert_alpha()]
	global datePic
	datePic = [pygame.image.load('DateBig.png').convert_alpha(),pygame.image.load('DateLittle.png').convert_alpha()]
	


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

def getTextPos(buttonRect, text):
	return buttonRect.x + buttonRect.width/2 - text.get_rect()[2]/2,  buttonRect.y + buttonRect.height/2 - text.get_rect()[3]/2

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
	button3 = pygame.Rect(519, 448, 164, 66)
	button4 = pygame.Rect(762, 448, 164, 66)

	text1 = afont.render( "Start", True, CYAN )
	text1altered = afont.render( "Start", True, WHITE )
	text2 = afont.render( "How to Play", True, CYAN )
	text2altered = afont.render( "How to Play", True, WHITE )
	text3 = afont.render( "Quit", True, CYAN )
	text3altered = afont.render( "Quit", True, WHITE )
	text4 = afont.render( "Credits", True, CYAN )
	text4altered = afont.render( "Credits", True, WHITE )

	t1pos = getTextPos(button1, text1)
	t2pos = getTextPos(button2, text2)
	t3pos = getTextPos(button3, text3)
	t4pos = getTextPos(button4, text4)

	text1focus = False
	text2focus = False
	text3focus = False
	text4focus = False

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
			else:
				text1 = afont.render( "Replay level", True, CYAN ) #!
				text1altered = afont.render( "Replay level", True, WHITE ) #!
			t1pos = getTextPos(button1, text1)
			text2 = afont.render( "Main Menu", True, CYAN )
			text2altered = afont.render( "Main Menu", True, WHITE )
			t2pos = getTextPos(button2, text2)
		if win:
			text1 = afont.render( "Next Level", True, CYAN )
			text1altered = afont.render( "Next Level", True, WHITE )
			t1pos = getTextPos(button1, text1)


		if button1.collidepoint(mpos):
			text1focus = True
		elif button2.collidepoint(mpos):
			text2focus = True
		elif button3.collidepoint(mpos):
			text3focus = True
		elif button4.collidepoint(mpos):
			text4focus = True
		else:
			text1focus = False
			text2focus = False
			text3focus = False
			text4focus = False
		
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
		if text4focus:
			if not played:
				screen.blit( text4altered, t4pos)
		else:
			if not played:
				screen.blit(text4, t4pos)

		pygame.display.update()
			
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if text1focus:
					if not win: #!
						mixer.music.load("track3.wav")
						mixer.music.play(-1)
						if LIVES == 0:
							global LIVES
							LIVES = 3
							global LEVEL
							LEVEL = 1 #!
							setup = 1
							skill = 1
					else:
						skill += 1
						if getDesign(setup)[(-1*skill)] == 9999:
							skill = 1
							setup += 1
						global LEVEL #### need to call this or else it treats LEVEL as a local variable
						LEVEL += 1 ####
					win = play(skill, getDesign(setup))
					played = True
				elif text2focus:
					if not played: ####
						showInstructions()
					else:
						mixer.music.load("track2.wav")
						mixer.music.play(-1)
						system()
				elif text3focus:
					getFPS()
					sys.exit()
				elif text4focus:
					if not played:
						showCredits()

			if event.type == pygame.QUIT:
				getFPS()
				sys.exit()

def play(skill, design):

	#controlled player
	player = Player( design[0], design[1], 28, 5)

	#date
	goal_x = design[2]
	goal_y = design[3]
	goal_rect = pygame.Rect(goal_x, goal_y, 48, 48)
	frame = 0

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

	screen.blit(mapPic, (0,0))
	for i in range(LIVES):
		screen.blit(chance, (20 + 40 * i, 13))
	pygame.display.flip()

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
			if goal_rect.colliderect(player.rect) and not player.date:
				player.date = True
				player.set_Size(35)
			if player.date and player.isAt(end_x, end_y):
				game.goto("win")
			
			if timeNum == 59:
				game.goto("lose")
		 
			# --- Drawing code
			screen.blit(mapPic, (end_x-20, end_y-20), pygame.Rect(end_x-20, end_y-20, 30, 30) )
			screen.blit(mapPic, (goal_x, goal_y), pygame.Rect(goal_x, goal_y, 50, 50) )
			player.clean(screen)
			for ex in exes:
			   ex.clean(screen)
			for ex in exes:
			   ex.draw(screen)
			if player.isAt(80, 13, 70):
				for i in range(LIVES):
					screen.blit(chance, (20 + 40 * i, 13))
			player.draw(screen)
			frame += .05
			if frame > 1.8:
				frame = 0
			if not player.date:
				screen.blit(datePic[int(frame)], (goal_x, goal_y))
			else:
				screen.blit(endLight, (end_x - 20, end_y - 20), pygame.Rect(0 + 30 * int(frame),0,30,30))
			timeNum = (30+ int((pygame.time.get_ticks() - timeInit) / 1000))
			yourTime = float( '%.3f' % (30.0 + ( float(pygame.time.get_ticks()) - float(timeInit) ) / 1000.0)) #### we limit the time to 3 decimal places
			timer = font.render( "7:" + str(timeNum), 1, RED)
			screen.blit(mapPic, (330, 205), pygame.Rect(330,205, 80, 80) )
			screen.blit(timer, (330, 205))

		elif game.cur == "lose":
			mixer.music.load("slap.wav")
			mixer.music.play()
			pygame.time.wait(500)
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

			bestTimeText1 = bfont.render("7:" + "%.3f" % bestTimeList[0], True, WHITE)
			bestTimeText2 = bfont.render("7:" + "%.3f" % bestTimeList[1], True, WHITE)
			bestTimeText3 = bfont.render("7:" + "%.3f" % bestTimeList[2], True, WHITE)
			yourTimeText = cfont.render("7:" + "%.3f" % yourTime, True, WHITE)
			screen.blit(bestTimeText1, (WIDTH/2 + 40, HEIGHT/2 + 2) )
			screen.blit(bestTimeText2, (WIDTH/2 + 40, HEIGHT/2 + 46) )
			screen.blit(bestTimeText3, (WIDTH/2 + 40, HEIGHT/2 + 89) )
			screen.blit(yourTimeText, (WIDTH/6, HEIGHT/2) )

			return True

		# --- update the screen
		pygame.display.flip()

	 
		# --- Limit to 60 frames per second
		global fpsList
		fpsList.append(clock.get_fps())
		clock.tick(52)

def showInstructions():
	textA = afont.render( "NEXT", True, CYAN )
	textAlit = afont.render( "NEXT", True, WHITE )
	textB = afont.render( "QUIT", True, CYAN )
	textBlit = afont.render( "QUIT", True, WHITE )
	buttonA = pygame.Rect(35, 448, 164, 66)
	buttonB = pygame.Rect(762, 448, 164, 66)
	tApos = getTextPos(buttonA, textA)
	tBpos = getTextPos(buttonB, textB)
	screen.fill(BLACK)
	pygame.display.update()

	direction = 0
	
	go = False
	tAfocus = False
	tBfocus = False
	while 1:
		if go:
			textA = afont.render( "Return Home", True, CYAN )
			textAlit = afont.render( "Return Home", True, WHITE )
			tApos = getTextPos(buttonA, textA)
		mpos = pygame.mouse.get_pos()
		if buttonA.collidepoint(mpos) :
			tAfocus = True
		elif buttonB.collidepoint(mpos) :
			tBfocus = True
		else:
			tAfocus = False
			tBfocus = False

		if not go:
			if( pygame.key.get_pressed()[pygame.K_UP] != 0 ):
					direction = 2
			if( pygame.key.get_pressed()[pygame.K_DOWN] != 0 ):
					direction = 3
			if( pygame.key.get_pressed()[pygame.K_LEFT] != 0 ):
					direction = 0
			if( pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
					direction = 1

		if not go:
			screen.blit(instr[direction], (0,0))
		else:
			direction += .005
			if direction > len(instr):
				direction = 4
			screen.blit(instr[int(direction)], (0,0))
		if tAfocus:
			screen.blit(textAlit, tApos)
		else:
			screen.blit(textA, tApos)
		if tBfocus:
			screen.blit(textBlit, tBpos)
		else:
			screen.blit(textB, tBpos)

		pygame.display.update()
			
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if tAfocus and not go:
					go = True
					direction = 4
				elif tAfocus and go:
					system()
				elif tBfocus:
					getFPS()
					sys.exit()	
			if event.type == pygame.QUIT:
				getFPS()
				sys.exit()

def showCredits():
	textB = afont.render( "Main Menu", True, CYAN )
	textBlit = afont.render( "Main Menu", True, WHITE )
	buttonB = pygame.Rect(762, 448, 164, 66)
	tBpos = getTextPos(buttonB, textB)
	screen.fill(BLACK)
	pygame.display.update()

	direction = 0
	
	tBfocus = False
	while 1:
		mpos = pygame.mouse.get_pos()
		if buttonB.collidepoint(mpos) :
			tBfocus = True
		else:
			tBfocus = False
			
#		screen.blit(instr[direction], (0,0))
			
		if tBfocus:
			screen.blit(textBlit, tBpos)
		else:
			screen.blit(textB, tBpos)

		pygame.display.update()
			
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if tBfocus:
					system()
			if event.type == pygame.QUIT:
				getFPS()
				sys.exit()


if __name__ == '__main__':
	pygame.font.init()
	mixer.init()
	mixer.music.load("track2.wav")
	mixer.music.play(-1)
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