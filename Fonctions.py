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

    def px10mmListe(distances_px,echelle):
        distances = []
        for x in distances_px:
            distances.append(Externes.px10mm(x,echelle))
        return distances

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

    def calculDistances2(ptsEchelle,ptsFish):
        echelle10mm = Externes.euclideDist(ptsEchelle[0],ptsEchelle[1])
        body_size = Externes.euclideDist(ptsFish[0],ptsFish[2])
        body_depth = Externes.euclideDist(ptsFish[1],ptsFish[3])
        distances_check = [body_size,body_depth]
        distances_check = Externes.px10mmListe(distances_check,echelle10mm)
        return distances_check

    def find_nearest(array, value):
        import numpy as np
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def detect_eye(img):
        import cv2
        import numpy as np
        img_couleur = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray,21)
        circles1 = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=70,param2=65, minDist=100, minRadius=25,maxRadius=45)
        circles = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=100,param2=30, minDist=120, minRadius=80,maxRadius=95)
        circles = np.round(circles[0, :]).astype("int32")
        return circles1[0][0]

    def openfn():
        import tkinter.filedialog,tkinter as tk
        filepath = tk.filedialog.askopenfilenames(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('jpeg files','.jpeg')])
        return filepath

    def Longueur(distance):
        texte = ""
        texte += "5 <-> 3 : distance nez oeil : "+str(distance[0])+" mm \n"
        texte += "5 <-> 7 : longueur museau : "+str(distance[1])+" mm \n"
        texte += "3 <-> 19 : diametre oeil : "+str(distance[2])+" mm \n"
        texte += "5 <-> 17 : longueur tête : "+str(distance[3])+" mm \n"
        texte += "11 <-> 17 : largeur tête : "+str(distance[4])+" mm \n"
        # texte += "7 <-> 9 : bas bouche - menton : "+str(distance[5])+" mm \n"
        # texte += "5 <-> 9 : haut bouche - menton : "+str(distance[6])+" mm "
        return texte

    def LongueurBody(distance):
        texte = ""
        texte += "8 <-> 10 : Longueur Corps : "+str(distance[0])+" mm \n"
        texte += " 13 <-> 15 : Largeur corps : "+str(distance[1])+" mm \n"
        return texte

    def projeteOrtho(pente,intercept,xA,yA):
        import numpy as np
        matriceA = np.array([[pente,-1],[1,pente]])
        vecteurB = np.array([[-intercept],[xA+pente*yA]])
        invMatA = np.linalg.inv(matriceA)
        projete = np.dot(invMatA,vecteurB)
        return projete