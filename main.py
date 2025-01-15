import pygame

import constants

#game creation
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler Tutorial")

# main game loop
run = True
while run:

    #event handler for exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit