import pygame
import math
import random
 

class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.r = radius
    def up(self):
        if self.y > 50:
            self.y -= 5
    def down(self):
        if self.y < HEIGHT - self.r:
            self.y += 5
    def left(self):
        if self.x > 50:
            self.x -= 5
    def right(self):
        if self.x < WIDTH - self.r:
            self.x += 5
    def draw(self, screen):

        circle(screen, GREEN, self.x, self.y, self.r)
        if math.hypot(self.x -350, self.y - 250) < 90+self.r:
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
    WIDTH = 1300
    global HEIGHT
    HEIGHT = 600
    #define RECTS
    global MAP
    MAP = [pygame.Rect(500,500, 10, 10)] #possibly use Union funtion to cut down on number of rectangles
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
    player = Player(50,50,50)


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
        for rect in MAP:
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