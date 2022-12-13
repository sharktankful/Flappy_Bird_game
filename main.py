import pygame
import sys
import os
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True


pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

# GAME VARIABLES
gravity = 0.25
bird_movement = 0
game_active = True

# SCALED IMAGES
bg_surface = pygame.image.load(os.path.join(
    'assets', 'background-day.png')).convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load(os.path.join('assets', 'base.png')).convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_surface = pygame.image.load(os.path.join(
    'assets', 'bluebird-midflap.png')).convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load(
    os.path.join('assets', 'pipe-green.png')).convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [400, 600, 800]


# MAIN GAME LOOP WHERE THE GAME RUNS
while True:
    # IF WE PRESS THE CLOSE BUTTON ON THE GAME WINDOW IT WILL CLOSE THE GAME
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -12
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

    # BACKGROUND SURFACE
    screen.blit(bg_surface, (0, 0))

    if game_active:
        # CREATES GRAVITY FOR BIRD
        bird_movement += gravity
        bird_rect.centery += bird_movement
        # DRAWS BIRD RECTANGLE
        screen.blit(bird_surface, bird_rect)
        # CHECK FOR COLLISION BETWEEN PIPES AND BIRD
        game_active = check_collision(pipe_list)
        # PIPES
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # IF FLOOR POSITION REACHES SPECIFIC NUMBER, IT RESETS BACK TO THE BEGINNING
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    # DRAWS ALL SURFACES TO THE DISPLAY SURFACE
    pygame.display.update()

    # CONTROLS THE FRAME RATE AT 120FPS
    clock.tick(120)
