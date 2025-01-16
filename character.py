import pygame
import math

class Character():
    #constructor, initialize the values
    def __init__(self, x, y, animation_list):
        self.flip = False
        self.animation_list = animation_list
        #which frame of the animation that we want to show
        self.frame_index = 0
        #captures time passed to know when to update animation
        self.update_time = pygame.time.get_ticks()
        self.image = animation_list[self.frame_index]
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x, y)

    #update the movement before drawing
    def move(self, dx, dy):
        #check direction for flip
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        #control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        #then update the coords
        self.rect.x += dx
        self.rect.y += dy
    
    #animation 
    def update(self):
        #speed of animation
        animation_cooldown = 70
        #handle animations
        #update image
        self.image = self.animation_list[self.frame_index]
        #check time to determine update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            #changes the frame number
            self.frame_index += 1
            #reset timer
            self.update_time = pygame.time.get_ticks()
        #check animation to then loop again, we only have 4 images
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    #drawing on surface
    def draw(self, surface, color):
        #image faces the direction of movement, image, left/right, up/down
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        #we still need the rectangle that decides the movement
        #the image is just drawn at the location of the rect
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, color, self, 1)