import turtle as tr
def square(r):
    for i in range(4):
        tr.forward(r)
        tr.left(90)
def sqrs(n,r,dr):
    for i in range(n):
        square(r)
        r+=dr
        tr.penup()
        tr.right(135)
        tr.forward(dr / ( 2 ** ( 0.5 )))
        tr.left(135)
        tr.pendown()
sqrs(10,100,30)
tr.done()