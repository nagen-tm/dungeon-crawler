#import packages
import pygame
import csv

#import other local files
import constants
import images
from weapon import Weapon
from items import Item
from world import World

#game creation
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler Tutorial")

#create clock for maintaining frame rate
clock = pygame.time.Clock()

#define game variables
level = 1
screen_scroll = [0, 0]

#define movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#define font, with size
font = pygame.font.Font('assets/fonts/AtariClassic.ttf', 20)

# get images from separate file to pair down main.py
weapon, arrow_image = images.weapon()
heart_empty, heart_half, heart_full = images.health()
item_images, coin_images = images.items()
mob_animations = images.mob_animation()
tile_list = images.tiles()

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
    #level
    draw_text(f"LEVEL: {str(level)}", font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)
    #show the score
    draw_text(f"X{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

#create the empty tile list that will be overriden by file
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
#load files created from a level editor
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter= ",")
    for x, row in enumerate(reader): 
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

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
        #reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        #moves number up the screen
        self.rect.y -= 1
        #deletes counter eventually
        self.counter+= 1
        if self.counter > 25:
            self.kill()

#create instances
player = world.player
bow = Weapon(weapon, arrow_image)
enemy_list = world.enemy_list

#create groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

#static coin for score
score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)
#add items from level data
for item in world.item_list:
    item_group.add(item)

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
    screen_scroll = player.move(dx, dy, world.obstacle_tiles)

    #update all objects
    world.update(screen_scroll)
    for enemy in enemy_list:
        enemy.ai(player, world.obstacle_tiles, screen_scroll)
        if enemy.alive:
            enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(screen_scroll, player)

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