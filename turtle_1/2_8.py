import turtle as tr
def sqspir(r,dr):
    while True:
        tr.forward(r)
        tr.left(90)
        tr.forward(r)
        tr.left(90)
        r+=dr
sqspir(20,5)