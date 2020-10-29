from random import randrange as rnd, choice
from pygame.draw import *
import pygame
import math
import time

pygame.init()
# Размеры окна
screen = pygame.display.set_mode((800, 600))
# Количество шаров
n = 20
myfont = pygame.font.SysFont('Comic Sans MS', 20)
bullet = 0
score = 0
# Список цветов для патронов
colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0)]
black = (0, 0, 0)
# Частота обновления картинки
FPS = 30
dt = 1/FPS
# Положение пушки
gun_pos = (40, 450)


class ball():
    def __init__(self, surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(colors)
        self.surface = surface
        self.lifetime = 1.5
        self.time = 0

    def draw(self):
        '''
        Прорисовывает шар
        '''
        circle(self.surface, self.color, (int(self.x), int(self.y)), self.r)
        circle(self.surface, black, (int(self.x), int(self.y)), self.r, 1)

    def move(self, kof):
        '''
        Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки.
        То есть обновляет значения self.x и self.y с учетом скоростей
        self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        '''
        global dt
        self.x += self.vx * dt
        self.y -= self.vy * dt
        self.vy -= 450 * dt
        if (self.x >= 800):
            self.vx *= -1
            self.x += self.vx * dt
            self.vx *= kof
        if (self.y >= 580):
            if abs(self.vy) <= 100:
                self.vy = 0
                self.y = 580
                self.vx = 0
            self.vy *= -1
            self.vx *= kof
            self.y -= self.vy * dt
            self.vy *= kof

    def step(self, kof):
        '''
        Премешает шар по прошествии единицы времени и прорисовывает его
        '''
        self.move(kof)
        self.draw()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью,
        описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели.
            В противном случае возвращает False.
        """
        return ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (
            self.r + obj.r) ** 2)


class gun():
    def __init__(self, surface, x, y):
        '''
        Конструктор класса gun.
        surface - поверхность пушки
        x, y - координаты ее начала
        '''
        self.on = 0
        self.an = 1
        self.surface = surface
        self.color = black
        self.x = x + 15
        self.y = y
        self.x0 = x
        self.y0 = y
        self.length = 30

    def fire_start(self):
        '''
        Начало огня. Предназначено для вызова во время нажатия кнопки.
        '''
        self.on = 1

    def aim(self):
        '''
        Прицеливание пушки к курсору мыши.
        '''
        x, y = pygame.mouse.get_pos()
        if not((x == self.x0) and (y == self.y0)):
            self.x = (x - self.x0)/((x - self.x0) ** 2 + (
                y - self.y0) ** 2) ** 0.5 * self.length + 40
            self.y = (y - self.y0)/((x - self.x0) ** 2 + (
                y - self.y0) ** 2) ** 0.5 * self.length + 450

    def draw(self):
        '''
        Прорисовка пушки.
        '''
        line(self.surface, self.color, (40, 450), (
            int(self.x), int(self.y)), 7)

    def fire_end(self, balls, bullet):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча
        vx и vy зависят от положения мыши.
        """
        bullet += 1
        new_ball = ball(self.surface, self.x0, self.y0)
        new_ball.r += 5
        self.an = math.atan((self.y-new_ball.y) / (self.x-new_ball.x))
        new_ball.vx = self.length * math.cos(self.an) * 18
        new_ball.vy = - self.length * math.sin(self.an) * 18
        balls += [new_ball]
        self.on = 0
        self.length = 30
        self.color = black
        return bullet

    def targetting(self):
        """Прицеливание. Зависит от положения мыши."""
        if self.length <= 60:
            self.length += 1
        if self.length >= 45:
            self.color = colors[3]


class target(ball):
    def __init__(self, surface):
        '''
        Конструктор класса target подкласса ball.
        surface - поверхность цели.
        '''
        self.vx = 0
        self.vy = 0
        self.surface = surface
        self.x = rnd(500, 780)
        self.y = rnd(100, 550)
        self.r = rnd(2, 50)
        self.color = colors[2]

    def hit(self, points, score):
        '''
        Попадание шарика в цель.
        points - количество добавляемых очков. score - текщий счет игрока.
        Возвращает счет игрока после попадания
        '''
        score += points
        return score


pygame.display.update()
clock = pygame.time.Clock()
score = 0
bullets = 0


def game():
    global FPS, score, dt, bullets
    g1 = gun(screen, *gun_pos)
    finished = False
    targets = [target(screen) for i in range(n)]
    balls = []
    bullets = 0
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                g1.fire_start()
            elif event.type == pygame.MOUSEBUTTONUP:
                bullets = g1.fire_end(balls, bullets)
        g1.draw()
        textsurface = myfont.render(str(score), False, (0, 0, 0))
        screen.blit(textsurface, (0, 0))
        for i in balls:
            i.step(0.6)
            for j in targets:
                if i.hittest(j):
                    score = j.hit(1, score)
                    targets.remove(j)
            if (i.vx == 0) and (i.vy == 0):
                i.time += dt
                if i.time >= i.lifetime:
                    balls.remove(i)
        for i in targets:
            i.step(0.9)
        if targets == []:
            pygame.event.set_blocked([
                pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
            g1 = gun(screen, *gun_pos)
            textsurface = myfont.render(
                'Вы уничтожили цели за ' + str(
                    bullets) + ' выстрелов...', False, (0, 0, 0))
            screen.blit(textsurface, (100, 300))
            if balls == []:
                pygame.event.set_allowed([
                    pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
                finished = True
                game()
        if g1.on:
            g1.targetting()
        g1.aim()
        pygame.display.update()
        clock.tick(FPS)
        screen.fill((255, 255, 255))


game()
pygame.quit()
