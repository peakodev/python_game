import random
import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200
HEIGHT_5_PERCENT = HEIGHT // 20
WIDTH_5_PERCENT = WIDTH // 20
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
BONUS_WIDTH = 10
BONUS_HEIGHT = 10
IMAGES_PATH = 'images'
IMAGES_GOOSE_ANIMATION_PATH = os.path.join(IMAGES_PATH, 'goose_animation')
IMAGE_BG_PATH = os.path.join(IMAGES_PATH, 'background.png')
IMAGE_PLAYER_PATH = os.path.join(IMAGES_PATH, 'player.png')
IMAGE_ENEMY_PATH = os.path.join(IMAGES_PATH, 'enemy.png')
IMAGE_BONUS_PATH = os.path.join(IMAGES_PATH, 'bonus.png')

PLAYER_IMAGES = os.listdir(IMAGES_GOOSE_ANIMATION_PATH)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load(IMAGE_BG_PATH), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

font = pygame.font.SysFont('arial', 20)

player = pygame.image.load(IMAGE_PLAYER_PATH).convert_alpha()
player_rect = pygame.Rect(20, HEIGHT//2, player.get_rect().width, player.get_rect().height)

player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]

score = 0
image_index = 0




def create_enemy():
    enemy = pygame.image.load(IMAGE_ENEMY_PATH).convert_alpha()
    enemy_size = [enemy.get_rect().width, enemy.get_rect().height]
    enemy_rect = pygame.Rect(WIDTH, random.randint(HEIGHT_5_PERCENT, HEIGHT - HEIGHT_5_PERCENT), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]




def create_bonus():
    bonus = pygame.image.load(IMAGE_BONUS_PATH).convert_alpha()
    bonus_size = [bonus.get_rect().width, bonus.get_rect().height]
    rand_max_width_x =WIDTH - bonus.get_rect().width - WIDTH_5_PERCENT
    bonus_rect = pygame.Rect(random.randint(WIDTH_5_PERCENT, rand_max_width_x), -bonus.get_rect().height, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]




CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1000)
bonuses = []

CHANGE_PLAYER_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_PLAYER_IMAGE, 250)

playing = True




while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_PLAYER_IMAGE:
            player = pygame.image.load(os.path.join(IMAGES_GOOSE_ANIMATION_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    main_display.blit(font.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    main_display.blit(player, player_rect)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))
        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))





