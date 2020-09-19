import turtle as tr
from random import *
def BrDv():
    while True:
        tr.forward(random()*30)
        r= randint(1,2)
        if r == 1:
            tr.left(random()*180)
        else:
            tr.right(random()*180)
BrDv()