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
        pipe.centerx -= 3
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

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_front.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_front.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_front.render(f'High Score: {int(score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_front = pygame.font.Font('04B_19.ttf', 40)

# GAME VARIABLES
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# SCALED IMAGES
bg_surface = pygame.image.load(os.path.join(
    'assets', 'background-day.png')).convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load(os.path.join('assets', 'base.png')).convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bluebird-downflap.png'))).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bluebird-midflap.png'))).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bluebird-upflap.png'))).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))


birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
# bird_surface = pygame.image.load(os.path.join(
#     'assets', 'bluebird-midflap.png')).convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center=(100, 512))

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
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -8
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface, bird_rect = bird_animation()
                
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

    # BACKGROUND SURFACE
    screen.blit(bg_surface, (0, 0))

    if game_active:
        # CREATES GRAVITY FOR BIRD
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        # DRAWS BIRD RECTANGLE
        screen.blit(rotated_bird, bird_rect)
        # CHECK FOR COLLISION BETWEEN PIPES AND BIRD
        game_active = check_collision(pipe_list)
        # PIPES
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')

    # IF FLOOR POSITION REACHES SPECIFIC NUMBER, IT RESETS BACK TO THE BEGINNING
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    # DRAWS ALL SURFACES TO THE DISPLAY SURFACE
    pygame.display.update()

    # CONTROLS THE FRAME RATE AT 120FPS
    clock.tick(120)
