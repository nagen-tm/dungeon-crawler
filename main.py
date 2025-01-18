#import packages
import pygame

#import other local files
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World

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
#load player health
heart_empty = scale_img(pygame.image.load(f"assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load(f"assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load(f"assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)
#load coin images
coin_images = []
for x in range(4):
    coin = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(coin)
#load potion image
red_potion = scale_img(pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)
#load weapon images 
weapon = scale_img(pygame.image.load(f"assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load(f"assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)

#load tile map images
tile_list = []
for i in range(constants.TILE_TYPES):
    tile_img = pygame.image.load(f"assets/images/tiles/{i}.png").convert_alpha()
    tile_img = pygame.transform.scale(tile_img, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_img)

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
            player_image = scale_img(pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha(), constants.SCALE)
            temp_list.append(player_image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#function for outputting text on screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

#function for game display information
def draw_info():
    #draw the panel at top of screen
    pygame.draw.rect(screen, constants.PANEL, (0,0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    half_heart_drawn = False
    #draw lives
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20  > 0) and half_heart_drawn ==False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))
    #show the score
    draw_text(f"X{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

#basically the numbers corrolate to the tiles
#building out the map, 5x5 grid
world_data = [
    [7, 7, 7, 7, 7],
    [7, 0, 1, 2, 7],
    [7, 3, 4, 5, 7],
    [7, 6, 6, 6, 7],
    [7, 7, 7, 7, 7]
]

world = World()
world.process_data(world_data, tile_list)

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

#create instances
player = Character(100, 100, 70, mob_animations, 0)
enemy = Character(200, 300, 100, mob_animations, 1)
bow = Weapon(weapon, arrow_image)

enemy_list = []
enemy_list.append(enemy)

#create groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images)
item_group.add(score_coin)

potion = Item(200, 200, 1, [red_potion])
item_group.add(potion)
coin = Item(400, 400, 0, coin_images)
item_group.add(coin)

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
    item_group.update(player)

    #draw world
    world.draw(screen)

    #draw enemies
    for enemy in enemy_list:
        enemy.draw(screen)
    #draw player on screen
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)
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