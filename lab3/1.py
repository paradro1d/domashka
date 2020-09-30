import pygame
from pygame.draw import *
    
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

circle(screen, (255,255,0), (200,200), 100)
circle(screen, (255,0,0), (150,150), 25)
circle(screen, (255,0,0), (250,150), 25)
circle(screen, (0,0,0), (150,150), 15)
circle(screen, (0,0,0), (250,150), 15)
line(screen, (0, 0, 0), (210,150), (300,100), 10)
line(screen, (0, 0, 0), (190,150), (100,100), 10)
rect(screen, (0, 0, 0), (150, 220, -100, -30))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()