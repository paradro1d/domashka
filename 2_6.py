import turtle as tr
tr.shape('turtle')
def spider(n):
    for i in range(n):
        tr.forward(100)
        tr.stamp()
        tr.backward(100)
        tr.left(360/n)
spider(int(input()))
tr.done()