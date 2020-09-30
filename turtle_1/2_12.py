import turtle as tr
def duga(n,r):
    for i in range(n // 2):
        tr.forward(r / n * 2 * 3.1415)
        tr.right(360 / n)
def pruzhina(n,m,rmal,rbol):
    tr.left(90)
    for i in range(n):
        duga(m,rbol)
        duga(m,rmal)
pruzhina(5,100,10,50)