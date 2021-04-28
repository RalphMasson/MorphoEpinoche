''' Bibliothèque de fonctions externes '''


def euclideDist(a,b):
    import numpy as np
    norme = np.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
    return norme

def calculAngle(pt1,pt2,pt3):
    from math import acos,pi
    b = euclideDist(pt1,pt2)
    a = euclideDist(pt2,pt3)
    c = euclideDist(pt1,pt3)
    Apt1 = acos((b**2+c**2-a**2)/(2*b*c))*180/pi
    Apt2 = acos((b**2+a**2-c**2)/(2*b*a))*180/pi
    Apt3 = acos((a**2+c**2-b**2)/(2*a*c))*180/pi
    listeAngle = [Apt1,Apt2,Apt3]
    return listeAngle

def calculAngleBis(pt1,pt2,pt3):
    #calcul par alkashi des angles en degres du triangle reliant les 3 points
    #        pt2
    #     b /     \ a
    #  pt1 ----- pt3
    #         c
    #angle au niveau du pt2
    b = euclideDist(pt1,pt2)
    a = euclideDist(pt2,pt3)
    c = euclideDist(pt1,pt3)
    from math import acos,pi
    Apt2 = acos((b**2+a**2-c**2)/(2*b*a))*180/pi
    return Apt2




def reorder_from_idx(idx, a):
    return a[idx:] + a[:idx]
def cyclic_perm(a):
    from functools import partial
    return [partial(reorder_from_idx, i) for i in range(len(a))]
def allPointsAngles():
    from itertools import combinations,permutations,combinations_with_replacement
    atest = list(combinations([i for i in range(9)],3))
    listeCombinaisonsAngle = []

    for a in atest:
        result = cyclic_perm(a)
        for x in range(len(a)):
            listeCombinaisonsAngle.append(result[x](a))

    listeCombinaisonsDistance = list(combinations([i for i in range(9)],2))
    return listeCombinaisonsDistance,listeCombinaisonsAngle

