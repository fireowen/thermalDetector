from math import *



def deltaTmax(r, H, Q):
    ratio = r / H

    if ratio < 0.18:
        result = ((16.9 * Q ** (2 / 3)) / (H ** (5 / 3)))
    else:
        result = ((5.38 * ((Q / r) ** (2 / 3))) / (H))

    return result


def Umax(r, H, Q):
    ratio = r / H

    if ratio < 0.15:
        result1 = 0.96 * (Q / H) ** (1 / 3)
    else:
        result1 = (0.195 * Q ** (1 / 3) * H ** (1 / 2)) / (r ** (5 / 6))

    return result1

def deltaTe(u,RTI,Tg,C,Te,Ta,step):
    result2 = ((sqrt(u) / RTI) * (Tg - (1 + (C / (sqrt(u)))) * Te - Ta)) * step

    return result2
