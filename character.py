import pygame
import math

class Character():
    #constructor, initialize the values
    def __init__(self, x, y, mob_animations, char_type):
        self.char_type = char_type
        self.flip = False
        self.animation_list = mob_animations[char_type]
        #which frame of the animation that we want to show
        self.frame_index = 0
        # set idle vs running, 0 = idle 1 = run
        self.action = 0
        self.running = False
        #captures time passed to know when to update animation
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x, y)

    #update the movement before drawing
    def move(self, dx, dy):
        #reset the movement to idle, then check movement
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
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
        #check what action the player is performing
        if self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)
        #speed of animation
        animation_cooldown = 70
        #handle animations
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check time to determine update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            #changes the frame number
            self.frame_index += 1
            #reset timer
            self.update_time = pygame.time.get_ticks()
        #check animation to then loop again, we only have 4 images
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
    
    def update_action(self, new_action):
        #check if new action is different
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #drawing on surface
    def draw(self, surface, color):
        #image faces the direction of movement, image, left/right, up/down
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        #we still need the rectangle that decides the movement
        #the image is just drawn at the location of the rect
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, color, self, 1)