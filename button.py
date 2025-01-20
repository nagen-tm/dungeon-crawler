import pygame

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        action = False
        #get the position of mouse to know if on button
        pos = pygame.mouse.get_pos()
        #check mouse over and click
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            action = True
        #draw on screen
        surface.blit(self.image, self.rect)

        return action