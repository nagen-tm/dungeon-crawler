#import packages
import pygame

#import other files
import constants
from character import Character

#game creation
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler Tutorial")

#create clock for maintaining frame rate
clock = pygame.time.Clock()

#define movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#create player
player = Character(100, 100)

#main game loop
run = True
while run:
    #control frame rate
    clock.tick(constants.FPS)
    #clears screen by creating the bg with every while loop update
    screen.fill(constants.BG)

    #calculate player movement (delta x, delta y)
    dx = 0
    dy = 0
    if moving_right == True:
        dx = constants.SPEED
    if moving_left == True:
        dx = -constants.SPEED
    if moving_up == True:
        dy = -constants.SPEED
    if moving_down == True:
        dy = constants.SPEED

    #move player
    player.move(dx, dy)

    #draw player on screen
    player.draw(screen, constants.RED)
    #event handler for exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    #updates the display with all the drawn elements
    pygame.display.update()

pygame.quit