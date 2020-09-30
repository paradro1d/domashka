import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 600))

gr1va = open('griva.txt', 'r')
clrs = open('clrs.txt', 'r')
tle = open('tale.txt', 'r')
tleclr = open('taleclrs.txt', 'r')

rect(screen, (117, 187, 253), (0, 0, 400, 300))
rect(screen, (63, 155, 11), (0, 300, 400, 300))
circle(screen, (255, 207, 72), (400, 50), 100)

rect(screen, (255, 228, 205), (50, 200, 25, 200))
tree = [(40, 150), (70, 170), (10, 170), (10, 200), (70, 200), (40, 220)]
for i in range(len(tree)):
    ellipse(screen, (92, 169, 4), (tree[i][0], tree[i][1], 50, 100))
apples = [(60, 170), (90, 200), (30, 200), (40, 250), (25, 270), (90, 270), (60, 300)]
for i in apples:
    circle(screen, (255, 8, 0), i, 10)
    
tale = tle.readlines()
tcolours = tleclr.readlines()
for i in range(len(tale)):
    ellipse(screen, list(map(int, tcolours[i].split())), list(map(int, tale[i].split())))
    
ellipse(screen, (255, 182, 193), (200, 380, 170, 110))
rect(screen, (255, 182, 193), (210, 430, 12, 100))
rect(screen, (255, 182, 193), (300, 400, 12, 130))
rect(screen, (255, 182, 193), (260, 400, 12, 150))
rect(screen, (255, 182, 193), (330, 400, 12, 150))
rect(screen, (255, 182, 193), (310, 320, 45, 90))
circle(screen, (255, 182, 193), (340, 325), 30)
ellipse(screen, (255, 182, 193), (332, 320, 68, 30))

circle(screen, (139, 0, 255), (350, 325), 10)
circle(screen, (0, 0, 0), (353, 325), 7)
ellipse(screen, (255, 255, 255), (340, 318, 12, 8))

polygon(screen, (139, 0, 255), [(350, 295), (380, 245), (360, 305)])

griva = gr1va.readlines()
colours = clrs.readlines()

for i in range(len(griva)):
    ellipse(screen, list(map(int, colours[i].split())), list(map(int, griva[i].split())))
    
clrs.close()
gr1va.close()
tle.close()
tleclr.close()
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()