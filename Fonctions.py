''' Bibliothèque de fonctions externes '''

class Externes():

    def euclideDist(a,b):
        import numpy as np
        norme = np.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
        return norme

    def calculAngle(pt1,pt2,pt3):
        from math import acos,pi
        b = Externes.euclideDist(pt1,pt2)
        a = Externes.euclideDist(pt2,pt3)
        c = Externes.euclideDist(pt1,pt3)
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
        b = Externes.euclideDist(pt1,pt2)
        a = Externes.euclideDist(pt2,pt3)
        c = Externes.euclideDist(pt1,pt3)
        from math import acos,pi
        Apt2 = acos((b**2+a**2-c**2)/(2*b*a))*180/pi
        return Apt2




    def reorder_from_idx(idx, a):
        return a[idx:] + a[:idx]
    def cyclic_perm(a):
        from functools import partial
        return [partial(Externes.reorder_from_idx, i) for i in range(len(a))]
    def allPointsAngles():
        from itertools import combinations,permutations,combinations_with_replacement
        atest = list(combinations([i for i in range(9)],3))
        listeCombinaisonsAngle = []

        for a in atest:
            result = Externes.cyclic_perm(a)
            for x in range(len(a)):
                listeCombinaisonsAngle.append(result[x](a))

        listeCombinaisonsDistance = list(combinations([i for i in range(9)],2))
        return listeCombinaisonsDistance,listeCombinaisonsAngle

    def px3mm(distance_px,echelle):
        return round(3*distance_px/echelle,4)

    def px3mmListe(distances_px,echelle):
        distances = []
        for x in distances_px:
            distances.append(Externes.px3mm(x,echelle))
        return distances

    def px10mm(distance_px,echelle):
        return round(10*distance_px/echelle,4)

    def genererAllDistancesHead(ptsEchelle,ptsFish):
        import numpy as np
        distances_all = []
        listeCombinaisonsDistance,listeCombinaisonsAngle = Externes.allPointsAngles()
        pt22 = ptsEchelle[0]
        pt24 = ptsEchelle[1]
        echelle3mm_px = Externes.euclideDist(pt22,pt24)
        for x in listeCombinaisonsDistance:
            distpx = Externes.euclideDist(ptsFish[x[0]],ptsFish[x[1]])
            distmm = round(3*distpx/echelle3mm_px,4)
            distances_all.append(distmm)
        for x in listeCombinaisonsAngle:
            thetas = Externes.calculAngle(ptsFish[x[0]],ptsFish[x[1]],ptsFish[x[2]])
            thetas = np.around(thetas[0],4)
            distances_all.append(thetas)

        f = open("C:/Users/MASSON/Desktop/STAGE_EPINOCHE/DistancesPourModele.csv", "a")
        header = listeCombinaisonsDistance+listeCombinaisonsAngle
        header = "; ".join(str(i) for i in header)
        distances_all = "; ".join(str(i) for i in distances_all)
        f.write(str(header)+"\n")
        f.write(str(distances_all))
        f.close()
        return distances_all

    def calculDistances(ptsEchelle,ptsFish):
        echelle3mm = Externes.euclideDist(ptsEchelle[0],ptsEchelle[1])
        snout_eye = Externes.euclideDist(ptsFish[0],ptsFish[1])
        snout_length = Externes.euclideDist(ptsFish[1],ptsFish[2])
        eye_diameter = Externes.euclideDist(ptsFish[0],ptsFish[8])
        head_length = Externes.euclideDist(ptsFish[1],ptsFish[7])
        head_depth = Externes.euclideDist(ptsFish[4],ptsFish[7])
        jaw_length = Externes.euclideDist(ptsFish[2],ptsFish[3])
        jaw_length2 = Externes.euclideDist(ptsFish[1],ptsFish[3])
        distances_check = [snout_eye,snout_length,eye_diameter,head_length,head_depth,jaw_length,jaw_length2]
        distances_check = Externes.px3mmListe(distances_check,echelle3mm)
        return distances_check