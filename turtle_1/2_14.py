import turtle as tr
def star(n,a):
    for i in range(n):
        tr.forward(a)
        tr.left(180-(180/n))
star(int(input()),100)
tr.done()