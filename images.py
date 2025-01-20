#import packages
import pygame

import constants

#scale images
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

def mob_animation():
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
    return mob_animations

def items():
    coin_images = []
    for x in range(4):
        coin = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
        coin_images.append(coin)
    #load potion image
    red_potion = scale_img(pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)
    item_images = []
    item_images.append(coin_images)
    item_images.append(red_potion)
    return item_images, coin_images

def health():
    heart_empty = scale_img(pygame.image.load(f"assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
    heart_half = scale_img(pygame.image.load(f"assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
    heart_full = scale_img(pygame.image.load(f"assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)
    return heart_empty, heart_half, heart_full

def weapon():
    weapon = scale_img(pygame.image.load(f"assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
    arrow_image = scale_img(pygame.image.load(f"assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
    fireball_image = scale_img(pygame.image.load(f"assets/images/weapons/fireball.png").convert_alpha(), constants.FIREBALL_SCALE)
    return weapon, arrow_image, fireball_image

def tiles():
    tile_list = []
    for i in range(constants.TILE_TYPES):
        tile_img = pygame.image.load(f"assets/images/tiles/{i}.png").convert_alpha()
        tile_img = pygame.transform.scale(tile_img, (constants.TILE_SIZE, constants.TILE_SIZE))
        tile_list.append(tile_img)
    return tile_list

def button():
    restart_img = scale_img(pygame.image.load(f"assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
    resume_img = scale_img(pygame.image.load(f"assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)
    start_img = scale_img(pygame.image.load(f"assets/images/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)
    exit_img = scale_img(pygame.image.load(f"assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
    return restart_img, resume_img, start_img, exit_img