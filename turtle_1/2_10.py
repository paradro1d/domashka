import turtle as tr
def tworounds(n,r):
    for i in range(n):
        tr.forward(r / n * 2 * 3.1415)
        tr.left(360 / n)
    for i in range(n):
        tr.forward(r / n * 2 * 3.1415)
        tr.right(360 / n)
def flower(n,m,r):
    for i in range(n):
        tworounds(m,r)
        tr.right(180/n)
flower(3,100,50)
tr.done()