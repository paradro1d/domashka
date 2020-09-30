import turtle as tr
def round(n, r):
    for i in range(n):
        tr.forward(r / n * 2 * 3.1415)
        tr.left(360 / n)
round(100,50)
tr.done()