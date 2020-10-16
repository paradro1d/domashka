import pygame
from pygame.draw import *
from random import randint
import yaml

pygame.init()
# Для изменения параметров игры воспользуйтесь config.yml.
# Считывание config.yml:
config = yaml.load(open('config.yml'), Loader=yaml.Loader)
FPS = config["FPS"]
screen = pygame.display.set_mode(config["windowsize"])
myfont = pygame.font.SysFont('Comic Sans MS', 30)
diff_settings = config["difficulty"]
buttons = config["buttons"]
colors = config['colors']
dt = 1 / FPS
pygame.display.set_caption("ШАРЫ С БРС")
kof = 100000


class ball:
    '''
    Круг, имеющий координаты x, y, скорости speed_x, speed_y, радиус r,
    цвет color, время жизни time. Отображается на поверхности surface.
    Перемещается и отражается при столкновении с краем экрана.
    '''

    def __init__(self, surface, size, timelife, speed):
        '''
        Объявление объекта класса ball. x, y - координаты, устанавливающиеся
        в пределах экрана случайным образом. speed_x, speed_y - скорости
        по горизонтальному и вертикальному направлению экрана, устанавливющиеся
        случайным образом в диапазоне (-speed, speed). Surface - поверхность
        отображения. Size - пределы размеров круга, устанавливающиеся в
        формате (a, b) от a до b случайным образом. timelife - время
        жизни шара в секундах. color - цвет шара, устанавоивающийся
        случайн из массива colors.
        '''
        self.surface = surface
        self.size = size
        self.r = randint(*size)
        self.x = randint(size[1], surface.get_width() - size[1])
        self.y = randint(size[1], surface.get_height() - size[1])
        self.time = timelife
        self.timelife = timelife
        self.color = colors[randint(0, len(colors)-3)]
        self.speed = speed
        self.speed_x = randint(-1 * speed, speed)
        self.speed_y = randint(-1 * speed, speed)

    def draw(self):
        '''
        Функция отрисовывает шар в его текущем положении
        '''
        circle(
            self.surface, colors[2],
            (int(self.x), int(self.y)), int(1.05*self.r))
        circle(self.surface, self.color, (int(self.x), int(self.y)), self.r)

    def die(self, time):
        '''
        Функция удаляет шар и создаёт новый. time - текущее время.
        '''
        self.__init__(self.surface, self.size, self.timelife, self.speed)
        self.time = self.time + time

    def move(self):
        '''
        Функция двигает шар в соответствие с характером движения.
        '''
        self.x = self.x + self.speed_x * dt
        self.y = self.y + self.speed_y * dt
        if (
            self.x + self.r > self.surface.get_width()) or (
                self.x - self.r < 0):
            self.speed_x = self.speed_x * (- 1)
        if (
            self.y + self.r > self.surface.get_height()) or (
                self.y - self.r < 0):
            self.speed_y = self.speed_y * (- 1)

    def step(self, time):
        '''
        Функция двигает шар, проверяет его время жизни и отрисовывает.
        time - текущее время.
        '''
        self.draw()
        self.move()
        if time > self.time:
            self.die(time)

    def push(self, time, score, up):
        '''
        Проверяет положение курсора по отношению к шару. Если он внутри,
        то удаляет шар при вызове и возвращает значение очков после его
        удаления. Предназначена для вызова при нажатии мыши. time -
        текущее время. score - текущий счёт. up - награда за шар.
        '''
        x, y = pygame.mouse.get_pos()
        if ((self.x - x) ** 2 + (self.y - y) ** 2 < self.r ** 2):
            self.die(time)
            score = score + up
        return score

    def check_collision(self, ball1):
        '''
        Функция проверяет шар для которого вызывается функция и
        ball1 на предмет взаимодействия.
        '''
        if not((self.x == ball1.x) and (self.y == ball1.y)):
            return ((self.x - ball1.x) ** 2 + (self.y - ball1.y) ** 2 <= (
                self.r + ball1.r + 10) ** 2)

    def collide(self, ball1):
        '''
        Функция отражает шар от шара ball1.
        '''
        dx = self.x - ball1.x
        dy = self.y - ball1.y
        k = dy / dx
        self.speed_x = self.speed_x + kof / (
            dx ** 2 + dy ** 2) * abs(dx) / dx / ((1 + k ** 2) ** (0.5))
        self.speed_y = self.speed_y + kof / (dx ** 2 + dy ** 2) * abs(
            dy) / dy / ((1 + k ** 2) ** (0.5)) * abs(k)


class superball(ball):
    '''
    Суперкруг, являющийся подклассом круга, но дающий большее количество
    очков, меньшее время жизни и случайно появляющийся
    (выглядит как мишень и двигается с ускорением).
    '''

    def draw(self):
        '''
        Функция отрисовывает суперкруг в его текущем положении.
        '''
        circle(
            self.surface, colors[2], (int(self.x), int(self.y)),
            int(1.05*self.r))
        circle(self.surface, self.color, (int(self.x), int(self.y)), self.r)
        circle(
            self.surface, colors[6], (int(self.x), int(self.y)),
            int(self.r * 0.5))
        circle(
            self.surface, colors[2], (int(self.x), int(self.y)),
            int(self.r * 0.3))
        circle(
            self.surface, colors[6], (int(self.x), int(self.y)),
            int(self.r * 0.15))

    def die(self, time):
        '''
        Функция удаляет суперкруг.
        '''
        a = self.size
        self.__init__(self.surface, (0, 0), self.timelife, self.speed)
        self.size = a

    def generate(self, time):
        '''
        При вызове функция случайным образом создает суперкруг с шансом
        1 % за кадр если его нет на поле игры.
        '''
        if (self.r == 0) and (randint(1, 100) == 1):
            self.__init__(self.surface, self.size, self.timelife, self.speed)
            self.time = self.time + time

    def move(self):
        '''
        Функция двигает суперкруг в соответствие с характером движения.
        '''
        self.x = self.x + self.speed_x * dt
        self.y = self.y + self.speed_y * dt
        self.speed_y = self.speed_y + self.x * dt -\
            self.surface.get_height() * dt
        if (
            self.x + self.r > self.surface.get_width()) or (
                self.x - self.r < 0):
            self.speed_x = self.speed_x * (- 0.9)
        if (
            self.y + self.r > self.surface.get_height()) or (
                self.y - self.r < 0):
            self.speed_y = self.speed_y * (- 0.9)


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
            rect(self.surface, colors[1], self.rect)
        textsurface = myfont.render(self.text, False, colors[2])
        surf = pygame.Surface(textsurface.get_size(), pygame.SRCALPHA)
        surfscaled = pygame.Surface(
            (self.rect[2], self.rect[3]), pygame.SRCALPHA)
        surf.blit(textsurface, (0, 0))
        pygame.transform.smoothscale(
            surf, (self.rect[2], self.rect[3]), surfscaled)
        self.surface.blit(surfscaled, (self.rect[0], self.rect[1]))


def tableoutput(surface):
    '''
    Функция выводит на экран таблицу рекордов
    (первые 12 значений). Surface - поверхность вывода.
    '''
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
            if (event.type == pygame.QUIT) or (
                    event.type == pygame.MOUSEBUTTONDOWN):
                finished_t = True
        a = 0
        for i in records[::-1]:
            a = a + 1
            textsurface = myfont.render(
                str(a) + '. ' + i[0] + ' ' + str(i[1]), False, (0, 0, 0))
            surface.blit(textsurface, (400, 10 + 40 * a))
        pygame.display.update()
        clock.tick(FPS)
        surface.fill(colors[7])


def save(name, score):
    '''
    Функция сохраняет результат игрока. name - имя игрока.
    score - его текущий счёт.
    '''
    table = open('table.txt', 'a')
    print(name + ': ' + str(score), file=table)
    table.close()


pygame.display.update()
clock = pygame.time.Clock()
finished = False
t = 0
score = 0
balls = [
    ball(screen, diff_settings[3], diff_settings[1], diff_settings[5])
    for i in range(diff_settings[0])]
sp = superball(screen, diff_settings[4], diff_settings[2], diff_settings[6])
sp.die(t)
print('Введите имя: ')
name = str(input())
b1 = button(screen, colors[0], buttons[0], 'Таблица рекордов')
b2 = button(screen, colors[5], buttons[1], 'Сохранить результат')
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in balls:
                score = i.push(t, score, 1)
            score = sp.push(t, score, 10)
            if b1.check():
                tableoutput(screen)
            if b2.check():
                save(name, score)
                finished = True
    for i in balls:
        for j in balls:
            if i.check_collision(j):
                i.collide(j)
    for i in balls:
        i.step(t)
    t = t + dt
    sp.step(t)
    sp.generate(t)
    textsurface = myfont.render(name + ': ' + str(score), False, (0, 0, 0))
    screen.blit(textsurface, (0, 0))
    b1.draw()
    b2.draw()
    pygame.display.update()
    clock.tick(FPS)
    screen.fill(colors[7])
pygame.quit()
