import turtle as tr
Vx = 8
Vy = 60
ay = -10
dt = 0.03
x = -200
y = 0
tr.goto(500,0)
while True:
    tr.goto(x,y)
    x+=Vx*dt
    y+= Vy * dt + ay * dt ** 2 / 2
    Vy+= ay * dt
    if y < 0:
        Vy*= -0.8
        y+=3