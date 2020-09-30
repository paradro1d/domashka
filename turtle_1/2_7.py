import turtle as tr
def spiral(dfi,k):
    fi=0
    while True:
        fi+=dfi
        tr.forward(k * dfi * ( 1 + fi ** 2 ) ** ( 0.5 ) )
        tr.left(dfi*360/(2*3.14))
spiral(0.1,10)