import random
import pygame
import sys
from pygame.locals import *
from settings import *
from collisions import *
from animations import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen_size = [600,400]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Plataformer')
clock = pygame.time.Clock()

display = pygame.Surface((300,200))

player_surf = pygame.image.load('./assets/player.png').convert_alpha()
player_surf.set_colorkey((255,255,255))
player_rect = player_surf.get_rect( midbottom = (50,50))
move_left = False
move_right = False
# player_location = [50,50]
player_y_momentum = 0
air_timer = 0

true_scroll = [0,0]

grass_surf = pygame.image.load('./assets/grass.png')
dirt_surf = pygame.image.load('./assets/dirt.png')

jump_sound = pygame.mixer.Sound('./assets/audio/jump.wav')
grass_sound = [pygame.mixer.Sound('./assets/audio/grass_0.wav'),pygame.mixer.Sound('./assets/audio/grass_1.wav')]
grass_sound[0].set_volume(0.2)
grass_sound[1].set_volume(0.2)
grass_sound_timer = 0

pygame.mixer.music.load('./assets/audio/music.wav')
pygame.mixer.music.play(-1)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


animation_database = {}

animation_database['idle'] = load_animation('./assets/player/idle',[7,7,40])
animation_database['run'] = load_animation('./assets/player/run',[7,7])

player_action = 'idle'
player_frame = 0
player_flip = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                move_right = True
            if event.key == K_LEFT:
                move_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                move_right = False
            if event.key == K_LEFT:
                move_left = False

    display.fill((146,244,255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    # 152 = display width/2 + player image width/2
    # 106 = display height/2 + player image height/2
    # so essas duas linhas de codiga ja fazem um bom trabalho de camera
    # true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    # true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20

    # camere moving
    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75), (0,120,300,80))

    # draw paralax objects
    for object in background_objects:
        object_rect = pygame.Rect(object[1][0]-scroll[0]*object[0],object[1][1]-scroll[1]*object[0],object[1][2],object[1][3])
        if object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),object_rect)
        else:
            pygame.draw.rect(display,(9,91,85),object_rect)

    # obstacle_list
    tile_rect = []

    for row_index,row in enumerate(WORLD_MAP):
        for col_index, col in enumerate(row):
            x = col_index * 16
            y = row_index * 16
            if col == '1':
                display.blit(dirt_surf,(x-scroll[0],y-scroll[1]))
            if col == '2':
                display.blit(grass_surf,(x-scroll[0],y-scroll[1]))
            if col != '0':
                tile_rect.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))


    player_movement = [0,0]

    if move_right:
        player_movement[0] += 2
    if move_left:
        player_movement[0] -= 2
    
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = False
    if player_movement[0] < 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = True
    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    
    # call def collisions
    player_rect, collisions = move(player_rect, player_movement, tile_rect)

    # animations
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]

    display.blit(pygame.transform.flip(player_img, player_flip, False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    if collisions['bottom']:
        player_y_momentum = 0 
        air_timer = 0

        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sound).play()
    else:
        air_timer += 1


    surf = pygame.transform.scale(display, screen_size)
    screen.blit(surf, (0,0))

    pygame.display.update()
    clock.tick(60)












