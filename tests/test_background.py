import sys

import pygame

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Test Invasion')

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 128))
