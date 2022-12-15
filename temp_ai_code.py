import pygame
import neat
import time
import os
import random
import sys

pygame.init()

# VARIABLES THAT DEFINE SCREEN SIZE
screen_width = 500
screen_height = 800

# VARIABLES THAT CONTAIN GAME IMAGES
bird_imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bluebird-upflap.png'))), pygame.transform.scale2x(pygame.image.load(
    os.path.join('assets', 'bluebird-midflap.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bluebird-downflap.png')))]
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'background-day.png' )))

class Bird:
    img = bird_imgs
    birdflap = pygame.USEREVENT
    pygame.time.set_timer(birdflap, 200)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bird_index = 0

    def bird_animation(self, win):
        # new_bird = bird_imgs[self.bird_index]

        for event in pygame.event.get():
            if event.type == self.birdflap:
                if self.img[self.bird_index] < 2:
                    self.bird_index += 1
                else:
                    self.bird_index = 0
        win.blit(self.img[self.bird_index], (self.x, self.y))
        


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

        draw_window(win, bird)

    pygame.quit()
    sys.exit

main()