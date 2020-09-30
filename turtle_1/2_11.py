import turtle as tr
def tworounds(n,r):
    for i in range(n):
        tr.forward(r / n * 2 * 3.1415)
        tr.left(360 / n)
    for i in range(n):
        tr.forward(r / n * 2 * 3.1415)
        tr.right(360 / n)
def butterfly(n,m,r,dr):
    tr.right(90)
    for i in range(n):
        tworounds(m,r)
        r+=dr
butterfly(10,100,50,10)
tr.done()