import pygame
import math

class Character():
    #constructor
    def __init__(self, x, y):
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x, y)

    #update the movement before drawing
    def move(self, dx, dy):
        #control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        #then update the coords
        self.rect.x += dx
        self.rect.y += dy

    #drawing on surface
    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self)