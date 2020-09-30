import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 600))

gr1va = open('griva.txt', 'r')
clrs = open('clrs.txt', 'r')
tle = open('tale.txt', 'r')
tleclr = open('taleclrs.txt', 'r')

griva = gr1va.readlines()
colours = clrs.readlines()
tale = tle.readlines()
tcolours = tleclr.readlines()

rect(screen, (117, 187, 253), (0, 0, 500, 300))
rect(screen, (63, 155, 11), (0, 300, 500, 300))


def pony(x, y, o, size):
    tcord = [list(map(int, tale[i].split())) for i in range(len(tale))]
    gcord = [list(map(int, griva[i].split())) for i in range(len(griva))]
    for i in range(len(tcord)):
        tcord[i][0] = round(tcord[i][0] * size * o + x)
        tcord[i][1] = round(tcord[i][1] * size + y)
        tcord[i][2] = round(tcord[i][2] * size * o)
        tcord[i][3] = round(tcord[i][3] * size)
        ellipse(screen, list(map(int, tcolours[i].split())), \
        (tcord[i][0] + (o < 0) * tcord[i][2], tcord[i][1], abs(tcord[i][2]), \
        tcord[i][3]))
    ellipse(screen, (255, 182, 193), (round(x + size * o * 60 + \
    int(o < 0) * size * o * 170), round(y + size * 135), \
    abs(round(size * o * 170)), round(size * 110)))
    rect(screen, (255, 182, 193), (round(x + size * o * 70), \
    round(y + size * 185), round(size * o * 12), round(size * 100)))
    rect(screen, (255, 182, 193), (round(x + size * o * 160), \
    round(y + size * 155), round(size * o * 12), round(size * 130)))
    rect(screen, (255, 182, 193), (round(x + size * o * 120), \
    round(y + size * 155), round(size * o * 12), round(size * 150)))
    rect(screen, (255, 182, 193), (round(x + size * o * 190), \
    round(y + size * 155), round(size * o * 12), round(size * 150)))
    rect(screen, (255, 182, 193), (round(x + size * o * 170), \
    round(y + size * 75), round(size * o * 45), round(size * 90)))
    circle(screen, (255, 182, 193), (round(x + size * o * 200), \
    round(y + size * 80)), round(size * 30))
    ellipse(screen, (255, 182, 193), (round(x + size * o * 192 + \
    int(o < 0) * size * o * 68), round(y + size * 75), \
    abs(round(size * o * 68)), round(size * 30)))

    circle(screen, (139, 0, 255), (round(x + size * o * 210), \
    round(y + size * 80)), round(size * 10))
    circle(screen, (0, 0, 0), (round(x + size * o * 213), \
    round(y + size * 80)), round(size * 7))
    ellipse(screen, (255, 255, 255), (round(x + size * o * 200 + \
    int(o < 0) * size * o * 12), round(y + size * 73), \
    abs(round(size * o * 12)), round(size * 8)))

    polygon(screen, (139, 0, 255), [(round(x + size * o * 210), \
    round(y + size * 50)), (round(x + size * o * 240), y), \
    (round(x + size * o * 220), round(y + size * 60))])
    for i in range(len(griva)):
        gcord[i][0] = round(gcord[i][0] * size * o + x)
        gcord[i][1] = round(gcord[i][1] * size + y)
        gcord[i][2] = round(gcord[i][2] * size * o)
        gcord[i][3] = round(gcord[i][3] * size)
        ellipse(screen, list(map(int, colours[i].split())), \
        (gcord[i][0] + (o < 0) * gcord[i][2], gcord[i][1], abs(gcord[i][2]), \
        gcord[i][3]))


def sun(x, y, r):
    for i in range(1, 256):
        circle(screen, (117 + round(i / 256 * 138), 187 + \
        round(i / 256 * 68), 253 - round(i / 256 * 253)), (x, y), \
        round((256 - i) / 256 * r))


def tri(x, y, sx, sy):
    tree = [
        (30 * sx + x, y), (60 * sx + x, 20 * sy + y), (x, y + sy * 20), 
        (x, 50 * sy + y), (60 * sx + x, 50 * sy + y), (30 * sx + x, 70 * sy + y)
    ]
    apples = [
        (40 * sx + x, 10 * sy + y), (70 * sx + x, 40 * sy + y), 
        (10 * sx + x, 40 * sy + y), (20 * sx + x, 90 * sy + y), 
        (5 * sx + x, 110 * sy + y), (70 * sx + x, 110 * sy + y), 
        (40 * sx + x, 140 * sy + y)
    ]
    rect(screen, (255, 228, 205), (round(40 * sx + x), \
    round(50 * sy + y), round(25 * sx), round(200 * sy)))
    for i in range(len(tree)):
        ellipse(screen, (92, 169, 4), (round(tree[i][0]), \
        round(tree[i][1]), round(50 * sx), round(100 * sy)))
    for i in range(len(tree)):
        ellipse(screen, (90, 255, 170), (round(tree[i][0]), \
        round(tree[i][1]), round(50 * sx), round(100 * sy)), 2)
    for i in range(len(apples)):
        ellipse(screen, (255, 8, 0), (round(apples[i][0]), \
        round(apples[i][1]), round(15 * sx), round(15 * sy)))
    for i in range(len(apples)):
        ellipse(screen, (90, 255, 170), (round(apples[i][0]), \
        round(apples[i][1]), round(15 * sx), round(15 * sy)), 2)


sun(400, 100, 140)

tri(50, 10, 1.3, 1.3)
tri(150, 60, 1.5, 1)
tri(10, 150, 1.3, 0.8)
tri(150, 150, 0.6, 1.3)
tri(0, 250, 1.2, 1)
tri(20, 350, 2, 0.6)

pony(160, 350, 1, 0.8)
pony(500, 300, -1, 0.55)
pony(220, 250, 1, 0.4)
pony(450, 250, -1, 0.2)

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