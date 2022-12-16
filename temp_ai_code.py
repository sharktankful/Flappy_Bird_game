import pygame
import neat
import time
import os
import random
import sys

pygame.init()
clock = pygame.time.Clock()
# VARIABLES THAT DEFINE SCREEN SIZE
screen_width = 500
screen_height = 800

# CLOCK TO SET FRAME RATE
clock = pygame.time.Clock()

# VARIABLES THAT CONTAIN GAME IMAGES
bird_imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'yellowbird-upflap.png'))), pygame.transform.scale2x(pygame.image.load(
    os.path.join('assets', 'yellowbird-midflap.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'yellowbird-downflap.png')))]
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'background-day.png' )))

# TIMER FOR BIRD FLAP IMAGES
birdflap = pygame.USEREVENT
pygame.time.set_timer(birdflap, 200)

class Bird:
    img = bird_imgs
    gravity = 0.25

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bird_movement = 0
        self.bird_index = 0
        self.bird_rect = self.img[self.bird_index].get_rect(center = (self.x, self.y))

    def bird_animation(self, win):
        if self.bird_index < 2:
            self.bird_index += 1
        else:
            self.bird_index = 0

        win.blit(self.img[self.bird_index], self.bird_rect)
        
    def move(self):
        self.bird_movement = 8
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

        pygame.transform.rotozoom(self.img[self.bird_index], -self.bird_movement * 3, 1)


# FUNCTION TO DRAW THE WINDOW
def draw_window(win, bird):
    win.blit(bg_img, (0,0))
    bird.bird_animation(win)
    pygame.display.update()

# MAIN FUNCTION OF OUR GAME
def main():
    win = pygame.display.set_mode((screen_width, screen_height))
    bird = Bird(200, 200)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False      

            if event.type == birdflap:
                bird.bird_animation(win)

        bird.move()
        draw_window(win, bird)

    clock.tick(60)
    pygame.quit()
    sys.exit()  



main()
