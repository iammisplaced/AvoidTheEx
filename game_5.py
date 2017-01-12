import pygame
import math
import random
import re

class Gamestate():
    #psuedo enum class to control game flow
    def __init__(self):
        self.values = ["play", "win", "lose"]
        self.num = 0
        self.cur = self.values[self.num]
    def next(self):
        self.num += 1
        if self.num > len(self.values):
            self.num = 0
        self.cur = values[num]
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
    def __init__(self, x0, y0, radius):
        self.x = x0
        self.y = y0
        self.r = radius
    def draw(self, screen):
        circle(screen, RED, self.x, self.y, self.r)

def circle(screen, color, x0, y0, radius):
        pygame.draw.circle(screen, color, (x0, y0), int(radius))

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


def main():
    pygame.init()
    globals()
    size = (WIDTH,HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Avoid the Ex")
    font = pygame.font.SysFont("monospace", 30)
    text = open("lvl_1.txt")
    level = re.split('\W+', text.read())
    for i in range(len(level)):
        level[i] = int(level[i])
    print(level)

    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #manages the gamestate
    game = Gamestate()

    #controlled sprite
    player = Player( level[0], level[1], 25, 5)

    #enemies
    exes = []
    for i in range(4, len(level[4:]) + 4, 2):
        exes.append(Exes(level[i], level[i+1], 30))

    #date
    goal_x = level[2]
    goal_y = level[3]


    # -------- Main Program Loop -----------
    while not done:
        if game.cur == "play":
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            if pygame.mouse.get_pressed()[0] != 0:
                print(pygame.mouse.get_pos())
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
            if player.isAt(goal_x, goal_y, 20) and not player.date:
                print("got your date")
                player.date = True
            if player.date and player.isAt(700, 100, 20):
                game.goto("win")
            timeNum = (30+ int(pygame.time.get_ticks() / 1000))
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
                circle(screen, CYAN, 700, 100, 20)
            timer = font.render( "7:" + str(timeNum), 1, WHITE)
            screen.blit(timer, (520, 280))
            player.draw(screen)

        elif game.cur == "lose":
            screen.fill(BLACK)
            endText = font.render( "You Lose", 1, RED)
            screen.blit(endText, (WIDTH/3, HEIGHT/3))
            done = True
        elif game.cur == "win":
            screen.fill(BLACK)
            endText = font.render( "You Win", 1, BLUE)
            screen.blit(endText, (WIDTH/3, HEIGHT/3))
            done = True

        # --- update the screen
        pygame.display.flip()
        if game.cur != "play":
            pygame.time.wait(1000)
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
if __name__ == "__main__" :
    main()
    # Close the window and quit.
    pygame.quit()