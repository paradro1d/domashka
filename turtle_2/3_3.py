import turtle as tr
shr = open('shrift.txt','r')
a = shr.readlines()
for i in range(10):
    a[i] = list(map(float,a[i].split()))
def letter(m,n):
    for i in range(len(m[n])):
        if i % 2 == 0:
            tr.left(m[n][i])
        else:
            tr.forward(m[n][i])

def text(m,a):
    tr.left(180)
    for i in range(len(a)):
        letter(m,a[i])
        tr.penup()
        tr.forward(20)
        tr.left(180)
        tr.pendown()

text(a,list(map(int,input().split())))
shr.close()
tr.done()