from random import randrange as rnd, choice
from pygame.draw import *
import pygame
import math
import time

pygame.init()
# Размеры окна
screen = pygame.display.set_mode((800, 600))
# Количество шаров
n = 5
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
# Цвет кнопок
butt_color = (255, 0, 0)
name = ''
alphabet = 'qwertyuiopasdfghjklzxcvbnm1234567890'


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


class button(object):
    '''
    Кнопка на поверности surface цвета color, являющаяся
    прямоугольником rect c текстом text.
    '''

    def __init__(self, surface, color, rectan, text):
        '''
        Объявление объекта класса кнопки. Surface - поверхность,
        на которой она отображается. color - её цвет. rectan -
        прямоугольник, в который она вписана.
        text - текст на кнопке.
        '''
        self.surface = surface
        self.color = color
        self.rect = rectan
        self.text = text

    def check(self):
        '''
        Проверяет положение курсора по отношению к кнопке.
        Если она внутри, то возвращает True. Иначе - False.
        '''
        x, y = pygame.mouse.get_pos()
        x0, y0, dx, dy = self.rect
        return ((x > x0) and (x < x0 + dx) and (y > y0) and (y < y0 + dy))

    def draw(self):
        '''
        Функция отрисовывает кнопку
        '''
        rect(self.surface, self.color, self.rect)
        if self.check():
            rect(self.surface, (0, 0, 255), self.rect)
        textsurface = myfont.render(self.text, False, black)
        surf = pygame.Surface(textsurface.get_size(), pygame.SRCALPHA)
        surfscaled = pygame.Surface(
            (self.rect[2], self.rect[3]), pygame.SRCALPHA)
        surf.blit(textsurface, (0, 0))
        pygame.transform.smoothscale(
            surf, (self.rect[2], self.rect[3]), surfscaled)
        self.surface.blit(surfscaled, (self.rect[0], self.rect[1]))


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


clock = pygame.time.Clock()


def save(name, score):
    '''
    Функция сохраняет результат игрока. name - имя игрока.
    score - его текущий счёт.
    '''
    table = open('table.txt', 'a')
    print(name + ': ' + str(score), file=table)
    table.close()


def game():
    '''
    Функция прорисовывает окно игры
    '''
    global FPS, score, dt, bullets, best_res
    g1 = gun(screen, *gun_pos)
    finished = False
    targets = [target(screen) for i in range(n)]
    balls = []
    bullets = 0
    save_butt = button(screen, butt_color, (10, 200, 100, 30), 'Сохранить')
    exit_butt = button(screen, butt_color, (10, 250, 100, 30), 'Выйти')
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if save_butt.check():
                    if best_res != 0:
                        save(name, best_res)
                    finished = True
                elif exit_butt.check():
                    finished = True
                else:
                    g1.fire_start()
            elif event.type == pygame.MOUSEBUTTONUP:
                if not save_butt.check():
                    bullets = g1.fire_end(balls, bullets)
        g1.draw()
        textsurface = myfont.render(
            name + ': ' + str(bullets), False, (0, 0, 0))
        screen.blit(textsurface, (0, 0))
        textsurface1 = myfont.render(
            'Лучший результат: ' + str(best_res), False, (0, 0, 0))
        screen.blit(textsurface1, (0, 30))
        save_butt.draw()
        exit_butt.draw()
        for i in balls:
            i.step(0.6)
            for j in targets:
                if i.hittest(j):
                    score = j.hit(1, score)
                    targets.remove(j)
                    balls.remove(i)
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
            if bullets < best_res + 1000*(best_res == 0):
                best_res = bullets
            screen.blit(textsurface, (100, 300))
            if balls == []:
                pygame.event.set_allowed([
                    pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
                pygame.display.update()
                clock.tick(0.5)
                finished = True
                game()
        if g1.on:
            g1.targetting()
        g1.aim()
        pygame.display.update()
        clock.tick(FPS)
        screen.fill((255, 255, 255))


def tableoutput(surface):
    '''
    Функция выводит на экран таблицу рекордов
    (первые 12 значений). Surface - поверхность вывода.
    '''
    Exit = button(surface, butt_color, (50, 50, 80, 30), 'Вернуться')
    finished_t = False
    table = open('table.txt', 'r')
    inp = table.readlines()
    records = []
    for i in inp:
        i = i.split()
        i[1] = int(i[1])
        records.append([i[0], i[1]])

    def scorekey(arr):
        return arr[1]

    records = sorted(records, key=scorekey)
    table.close()
    global FPS
    while not finished_t:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                finished_t = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Exit.check():
                    finished_t = True
        a = 0
        for i in records:
            a = a + 1
            textsurface = myfont.render(
                str(a) + '. ' + i[0] + ' ' + str(i[1]), False, (0, 0, 0))
            surface.blit(textsurface, (400, 10 + 40 * a))
        Exit.draw()
        pygame.display.update()
        clock.tick(FPS)
        surface.fill((255, 255, 255))


def main_window():
    '''
    Фуекция прорисовывет главное окно
    '''
    finished = False
    butts = []
    butts.append(button(
        screen, butt_color, (350, 100, 100, 30), 'Начать игру'))
    butts.append(button(
        screen, butt_color, (350, 200, 100, 30), 'Таблица рекордов'))
    butts.append(button(
        screen, butt_color, (350, 300, 100, 30), 'Выйти'))
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if butts[0].check():
                    name_input()
                    game()
                if butts[1].check():
                    tableoutput(screen)
                if butts[2].check():
                    finished = True
        for b in butts:
            b.draw()
        pygame.display.update()
        clock.tick(FPS)
        screen.fill((255, 255, 255))


def key_check(string, name):
    '''
    Обработка нажатия клавиши при вводе имени.
    Возвращает имя после нажатия клавиши.
    '''
    if string in alphabet:
        name = name + string
    elif string == 'backspace':
        name = name[0:len(name)-1]
    return name


def name_input():
    '''
    Фуекция прорисовывает окно ввода имени.
    '''
    global name, best_res
    best_res = 0
    b = button(screen, butt_color, (350, 100, 100, 30), 'Начать игру')
    name = ''
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                name = key_check(pygame.key.name(event.key), name)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if b.check():
                    finished = True
        b.draw()
        textsurface = myfont.render(name, False, (0, 0, 0))
        screen.blit(textsurface, (350, 200))
        textsurface1 = myfont.render('Введите имя:', False, (0, 0, 0))
        screen.blit(textsurface1, (350, 150))
        pygame.display.update()
        clock.tick(FPS)
        screen.fill((255, 255, 255))


main_window()
pygame.quit()
