import pygame
import math
import random
 

class Player:
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x,y, size, size)
        self.speed = int(speed)
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
        if math.hypot(self.rect.centerx -350, self.rect.centery - 250) < 90+self.rect.width:
            return True
        else:
            return False


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
    #screen size
    global WIDTH
    WIDTH = 960
    global HEIGHT
    HEIGHT = 540
    #define RECTS
    global MAP
    borders = [pygame.Rect(0,0, WIDTH, 1), pygame.Rect(0,0, 1, HEIGHT), pygame.Rect(0,HEIGHT-1, WIDTH, 1), pygame.Rect(WIDTH-1,0, 1, HEIGHT),]
    MAP = borders + [pygame.Rect(800,400, 40, 40), pygame.Rect(600,500, 80, 40)]


def main():

    pygame.init()

    globals()
    
    size = (WIDTH,HEIGHT)
    screen = pygame.display.set_mode(size)
     
    pygame.display.set_caption("Base")
     
    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #controlled sprite
    player = Player(50,50,25, 5)


    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #key pressed
        if( pygame.key.get_pressed()[pygame.K_UP] != 0 ):
            player.up()
        if( pygame.key.get_pressed()[pygame.K_DOWN] != 0 ):
            player.down()
        if( pygame.key.get_pressed()[pygame.K_LEFT] != 0 ):
            player.left()
        if( pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
            player.right()
     
        # --- Game logic

        # clear the screen to white background
        screen.fill(BLACK)
     
        # --- Drawing code
        for rect in MAP[:4]:
            pygame.draw.rect( screen, BLACK, rect)
        for rect in MAP[4:]:
            pygame.draw.rect( screen, BLUE, rect)
        circle(screen, RED, 350, 250, 100)
        if player.draw(screen):
            done = True
        # --- update the screen
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
if __name__ == "__main__" :
    main()
    # Close the window and quit.
    pygame.quit()