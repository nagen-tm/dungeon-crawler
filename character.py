import pygame
import math

import constants

class Character():
    #constructor, initialize the values
    def __init__(self, x, y, health, mob_animations, char_type, boss, size):
        self.char_type = char_type
        self.boss = boss
        self.flip = False
        self.animation_list = mob_animations[char_type]
        #which frame of the animation that we want to show
        self.frame_index = 0
        # set idle vs running, 0 = idle 1 = run
        self.action = 0
        self.running = False
        self.score = 0
        self.health = health
        self.alive = True
        #captures time passed to know when to update animation
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)

    #update the movement before drawing
    def move(self, dx, dy, obstacle_tiles):
        screen_scroll = [0,0]
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
        #check collision
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                #check which side the collision is
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                #check which side the collision is
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        #do we need to scroll the screen for the player
        if self.char_type == 0:
            #move left and right
            right_offset = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD
            if self.rect.right > right_offset:
                screen_scroll[0] = right_offset - self.rect.right
                self.rect.right = right_offset
            if self.rect.left < constants.SCROLL_THRESHOLD:
                screen_scroll[0] = constants.SCROLL_THRESHOLD - self.rect.left
                self.rect.left = constants.SCROLL_THRESHOLD 
            #move up and down
            bottom_offset = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD
            if self.rect.bottom > bottom_offset:
                screen_scroll[1] = bottom_offset - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD
            if self.rect.top < constants.SCROLL_THRESHOLD:
                screen_scroll[1] = constants.SCROLL_THRESHOLD - self.rect.top
                self.rect.top = constants.SCROLL_THRESHOLD

        return screen_scroll
    
    def ai(self, screen_scroll):
      #reposition based on screen scroll
      self.rect.x += screen_scroll[0]
      self.rect.y += screen_scroll[1]

    #animation 
    def update(self):
        #check is char has died
        if self.health <= 0:
            self.health = 0
            self.alive = False
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
    def draw(self, surface):
        #image faces the direction of movement, image, left/right, up/down
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        #we still need the rectangle that decides the movement
        #the image is just drawn at the location of the rect
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
        else:
            surface.blit(flipped_image, self.rect)
        #pygame.draw.rect(surface, constants.RED, self, 1)