import turtle as tr
import numpy as np
def mnogoug(n,a):
    tr.left(90+180/n)
    for i in range(n):
        tr.forward(a)
        tr.left(360/n)
    tr.right(90+180/n)
def alotofangles(n,a,da):
    for i in range(1,n+1):
        mnogoug(i+2,a)
        tr.penup()
        tr.forward((a+da)/(2*np.sin(np.pi/(i+3)))-a/(2*np.sin(np.pi/(i+2))))
        tr.pendown()
        a+=da
alotofangles(10,20,10)
tr.done()
        