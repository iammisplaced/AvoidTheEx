# John Dowling
# CS269 Jan Plan Game Design
# Avoid the Ex
# startscreen.py

import sys
import pygame
import game_6

pygame.font.init()
screen = pygame.display.set_mode( (960, 540) )
pygame.display.set_caption("Avoid the Ex")

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

	#									rgb color
	text1 = afont.render( "Start", True, (0, 255, 255) )
	text1altered = afont.render( "Start", True, (255, 255, 255) )
	text2 = afont.render( "How to Play", True, (0, 255, 255) )
	text2altered = afont.render( "How to Play", True, (255, 255, 255) )
	win = False
	played = False
	text3 = afont.render( "Quit", True, (0, 255, 255) )
	text3altered = afont.render( "Quit", True, (255, 255, 255) )


	t1rect = text1.get_rect()
	t2rect = text2.get_rect()
	t3rect = text3.get_rect()
	t1pos = (button1pos[0]+button1size[0]/2-t1rect[2]/2,button1pos[1]+button1size[1]/2-t1rect[3]/2)
	t2pos = (button2pos[0]+button2size[0]/2-t2rect[2]/2,button2pos[1]+button2size[1]/2-t2rect[3]/2)
	t3pos = (button3pos[0]+button3size[0]/2-t3rect[2]/2,button3pos[1]+button3size[1]/2-t3rect[3]/2)

	screen.fill((0, 0, 0))
	screen.blit(background, (0,0) )
	screen.blit( text1, t1pos )
	screen.blit( text2, t2pos )

	pygame.display.update()
	
	text1focus = False
	text2focus = False
	text3focus = False
	while 1:

		mpos = pygame.mouse.get_pos()
		
		if played:
			text1 = afont.render( "Restart", True, (0, 255, 255) )
			text1altered = afont.render( "Restart", True, (255, 255, 255) )
			text2 = afont.render( "", True, (0, 255, 255) )
			text2altered = afont.render( "", True, (0, 255, 255) )
		if win:
			text2 = afont.render( "Next Level", True, (0, 255, 255) )
			text2altered = afont.render( "Next Level", True, (255, 255, 255) )


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
					win = game_6.play(screen)
					played = True
				elif text2focus:
					showInstructions(screen)
				elif text3focus:
					sys.exit()

			if event.type == pygame.QUIT:
				sys.exit()

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
	showTitle(screen)