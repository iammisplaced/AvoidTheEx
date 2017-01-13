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

class Player:
    #controls player rules/art
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x,y, size, size)
        self.speed = int(speed)
        self.date = False
    def collide(self):
        for rect in MAP:
            if rect.colliderect(self.rect):
                return True# player is in at least 1 rect
        return False #player is not in any rect
    def up(self):
        self.rect.move_ip(0, -1*self.speed)
        if self.collide():
            self.rect.move_ip(0, self.speed)
    def down(self):
        self.rect.move_ip(0, self.speed)
        if self.collide():
            self.rect.move_ip(0, -1*self.speed)
    def left(self):
        self.rect.move_ip(-1*self.speed, 0)
        if self.collide():
            self.rect.move_ip(self.speed, 0)
    def right(self):
        self.rect.move_ip(self.speed, 0)
        if self.collide():
            self.rect.move_ip(-1*self.speed, 0)
    def draw(self, screen):
        circle(screen, GREEN, self.rect.centerx, self.rect.centery, self.rect.width*.7)
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
        circle(screen, RED, self.x, self.y, self.r)
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

def circle(screen, color, x0, y0, radius):
        pygame.draw.circle(screen, color, (int(x0), int(y0)), int(radius))

def globals():
     # Define some colors
    global BLACK
    BLACK = (0, 0, 0)
    global WHITE 
    WHITE= (255, 255, 255)
    global GREEN 
    GREEN= (0, 255, 0)
    global RED
    RED = (255, 0, 0)
    global BLUE 
    BLUE= (0,0, 255)
    global YELLOW
    YELLOW = (255,255,0)
    global CYAN
    CYAN = (0, 255, 255)
    #screen size
    global WIDTH
    WIDTH = 960
    global HEIGHT
    HEIGHT = 540
    #define RECTS
    global MAP
    borders = [pygame.Rect(0,0, WIDTH, 1), pygame.Rect(0,0, 1, HEIGHT), pygame.Rect(0,HEIGHT-1, WIDTH, 1), 
            pygame.Rect(WIDTH-1,0, 1, HEIGHT),]
    MAP = borders + [pygame.Rect(60,60,60,60), pygame.Rect(60,180,120,180), pygame.Rect(60,420,60,60), 
            pygame.Rect(180,0,60,480), pygame.Rect(300,60,150,240), pygame.Rect(300,360,150,120), 
            pygame.Rect(510,60,150,120), pygame.Rect(510,240,150,240), pygame.Rect(720,60,60,480), 
            pygame.Rect(840,60,60,60), pygame.Rect(780,180,120,180), pygame.Rect(840,420,60,60) ]


def showTitle(screen):
	
	background = pygame.image.load("ATEStartScreen.png").convert_alpha()
	global afont
	afont = pygame.font.SysFont( "Helvetica", 20, bold=False )
	button1pos = (35,448)
	button1size = (164,66)
	button1 = pygame.Rect(35, 448, 164, 66)
	button2pos = (278,448)
	button2size = (164,66)

	button2 = pygame.Rect(278, 448, 164, 66)

	button3pos = (521,448)
	button3size = (164,66)
	button3 = pygame.Rect(521, 448, 164, 66)

	text1 = afont.render( "Start", True, CYAN )
	text1altered = afont.render( "Start", True, WHITE )
	text2 = afont.render( "How to Play", True, CYAN )
	text2altered = afont.render( "How to Play", True, WHITE )
	win = False
	played = False
	text3 = afont.render( "Quit", True, CYAN )
	text3altered = afont.render( "Quit", True, WHITE )


	t1rect = text1.get_rect()
	t2rect = text2.get_rect()
	t3rect = text3.get_rect()
	t1pos = (button1pos[0]+button1size[0]/2-t1rect[2]/2,button1pos[1]+button1size[1]/2-t1rect[3]/2)
	t2pos = (button2pos[0]+button2size[0]/2-t2rect[2]/2,button2pos[1]+button2size[1]/2-t2rect[3]/2)
	t3pos = (button3pos[0]+button3size[0]/2-t3rect[2]/2,button3pos[1]+button3size[1]/2-t3rect[3]/2)

	screen.fill(BLACK)
	screen.blit(background, (0,0) )
	screen.blit( text1, t1pos )
	screen.blit( text2, t2pos )

	pygame.display.update()
	
	text1focus = False
	text2focus = False
	text3focus = False
	skill = 4
	while 1:

		mpos = pygame.mouse.get_pos()
		
		if played:
			text1 = afont.render( "Restart", True, CYAN )
			text1altered = afont.render( "Restart", True, WHITE )
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
					win = play(screen, skill)
					played = True
				elif text2focus:
					if win:
						skill += 4
						win = play(screen, skill)
					else:
						showInstructions(screen)
				elif text3focus:
					sys.exit()

			if event.type == pygame.QUIT:
				sys.exit()

def play(screen, skill):
    font = pygame.font.SysFont("monospace", 30)
    text = open("lvl_2.txt")
    level = re.split('\W+', text.read())
    for i in range(len(level)):
        level[i] = int(level[i])

    # Loop until the user clicks the close button.
    done = False

    #manages the gamestate
    game = Gamestate()

    #controlled sprite
    player = Player( level[0], level[1], 25, 10)

    #enemies
    exes = []
    for i in range(4, len(level[4:]) + 4, 4):
        exes.append(Exes(level[i], level[i+1], level[i+2], level[i+3], skill, 30))

    #date
    goal_x = level[2]
    goal_y = level[3]
    #timing
    clock = pygame.time.Clock()
    timeInit = pygame.time.get_ticks()
    timeNum = 0
    # -------- Main Program Loop -----------
    while not done:
        if game.cur == "play":
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
            if player.isAt(goal_x, goal_y, 20) and not player.date:
                player.date = True
            if player.date and player.isAt(700, 30, 20):
                game.goto("win")
            
            if timeNum == 59:
                game.goto("lose")

            # clear the screen to black background
            screen.fill(BLACK)
         
            # --- Drawing code
            for rect in MAP[:4]:
                pygame.draw.rect( screen, BLACK, rect)
            for rect in MAP[4:]:
                pygame.draw.rect( screen, BLUE, rect)
            for ex in exes:
               ex.draw(screen)
            if not player.date:
                circle(screen, YELLOW, goal_x, goal_y, 20)
            else:
                circle(screen, CYAN, 700, 30, 20)
            timeNum = (30+ int((pygame.time.get_ticks() - timeInit) / 1000))
            timer = font.render( "7:" + str(timeNum), 1, WHITE)
            screen.blit(timer, (520, 280))
            player.draw(screen)

        elif game.cur == "lose":
            screen.fill(BLACK)
            endText = font.render( "You Lose", 1, RED)
            screen.blit(endText, (WIDTH/3, HEIGHT/3))
            return False
        elif game.cur == "win":
            screen.fill(BLACK)
            endText = font.render( "You Win", 1, BLUE)
            screen.blit(endText, (WIDTH/3, HEIGHT/3))
            return True

        # --- update the screen
        pygame.display.flip()

     
        # --- Limit to 30 frames per second
        clock.tick(30)

def showInstructions(screen):
	screen.fill((0,0,0))
	instructionsText = afont.render( "Instructions go here", True, (0, 255, 0) )
	returnText = afont.render( "Return to title screen", True, (0, 255, 0) )
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
			
			rtaltered = afont.render( "Return to title screen", True, (255, 255, 255) )
			
			screen.fill((0, 0, 0), rtrect )
			screen.blit(rtaltered, rtpos )
			
		else:
			rtfocus = False
			
			screen.fill((0, 0, 0), rtrect )
			screen.blit(returnText, rtpos )

		pygame.display.update()
			
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if rtfocus:
					showTitle(screen)
			if event.type == pygame.QUIT:
				sys.exit()


if __name__ == '__main__':
	pygame.font.init()
	globals()
	screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
	pygame.display.set_caption("Avoid the Ex")
	showTitle(screen)