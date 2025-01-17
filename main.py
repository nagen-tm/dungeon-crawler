#import packages
import pygame

#import other local files
import constants
from character import Character
from weapon import Weapon

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

#define font, with size
font = pygame.font.Font('assets/fonts/AtariClassic.ttf', 20)

#scale images
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

#load in multiple images for animations for different items using same classes
#names are looped through for the loading of file

#load weapon images 
weapon = scale_img(pygame.image.load(f"assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load(f"assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)

#load character images
mob_animations = []
mob_types = ['elf', 'imp', 'skeleton', 'goblin', 'muddy', 'tiny_zombie', 'big_demon']
animation_types = ['idle', 'run']
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            #converts the image to match format of game window with transparancy 
            player_image = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            player_image = scale_img(player_image, constants.SCALE)
            temp_list.append(player_image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)


#damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        #convert test into an image with font
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    #to remove after being drawn
    def update(self):
        #moves number up the screen
        self.rect.y -= 1
        #deletes counter eventually
        self.counter+= 1
        if self.counter > 25:
            self.kill()

#create player
player = Character(100, 100, 100, mob_animations, 0)
#player's weapon
bow = Weapon(weapon, arrow_image)
#sprite groups
arrow_group = pygame.sprite.Group()

#create enemy
enemy = Character(200, 300, 100, mob_animations, 1)
enemy_list = []
enemy_list.append(enemy)

#damage text
damage_text_group = pygame.sprite.Group()

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

    #update enemies
    for enemy in enemy_list:
        enemy.update()

    #update player for animations
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()

    #draw enemies
    for enemy in enemy_list:
        enemy.draw(screen)
    #draw player on screen
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
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