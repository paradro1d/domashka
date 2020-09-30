from random import randint
import turtle


number_of_turtles = 20
dt=0.05

pool = [turtle.Turtle(shape='circle') for i in range(number_of_turtles)]
x = [randint(-200,200) for i in range(number_of_turtles)]
y = [randint(-200,200) for i in range(number_of_turtles)]
vx = [randint(-10,10) for i in range(number_of_turtles)]
vy = [randint(-10,10) for i in range(number_of_turtles)]
for unit in pool:
    unit.penup()
    unit.speed(0)
    unit.goto(x[pool.index(unit)], y[pool.index(unit)])

kof = 10000
while True:
    for unit in pool:
        i = pool.index(unit)
        unit.goto(x[i], y[i])
        x[i]+= vx[i]*dt
        y[i]+= vy[i]*dt
        if x[i] > 200:
            x[i] -= 5
            vx[i] *= -1
        if x[i] < -200:
            x[i] += 5
            vx[i] *= -1
        if y[i] > 200:
            y[i] -= 5
            vy[i] *= -1
        if y[i] < -200:
            y[i] += 5
            vy[i] *= -1
        for othunit in pool:
            j = pool.index(othunit)
            if j != i:
                dx = x[i] - x[j]
                dy = y[i] - y[j]
                if (dx ** 2) + (dy ** 2) < 800:
                    k = dy / dx
                    vx[i] += kof/(dx ** 2 + dy ** 2)*abs(dx)/dx/((1 + k ** 2)**(0.5))
                    vx[j] -= kof/(dx ** 2 + dy ** 2)*abs(dx)/dx/((1 + k ** 2)**(0.5))
                    vy[i] += kof/(dx ** 2 + dy ** 2)*abs(dy)/dy/((1 + k ** 2)**(0.5))*abs(k)
                    vy[j] -= kof/(dx ** 2 + dy ** 2)*abs(dy)/dy/((1 + k ** 2)**(0.5))*abs(k)
