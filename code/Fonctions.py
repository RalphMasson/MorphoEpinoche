''' Bibliothèque de fonctions externes '''

class Externes():
    nbClic = 0

    def euclideDist(a,b):
        """!
        Methode pour calculer la distance euclidienne entre deux points
        @param a tuple : coordonnees du point a : [x1,y1]
        @param b tuple : coordonnees du point b : [x2,y2]
        @return norme float : distance entre a et b
        """
        import numpy as np
        norme = np.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
        return norme

    def calculAngle(pt1,pt2,pt3):
        """!
        Methode pour calculer les 3 angles du triangle crée par 3 points
        @param pt1 tuple : coordonnees du point1 : [x1,y1]
        @param pt2 tuple : coordonnees du point2 : [x2,y2]
        @param pt3 tuple : coordonnees du point3 : [x3,y3]
        @return listeAngle list of float : liste des 3 angles
        """
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

    def genererAllDistancesHead(ptsEchelle,ptsFish,sex,chemin):
        import numpy as np
        import time,os
        from win32com.client import Dispatch
        from tkinter import messagebox
        import tkinter as tk


        if(len(ptsEchelle)==0 or len(ptsFish)==0):
            tk.messagebox.showwarning(title="Attention",message="Importer une image")

        elif(sex==''):
            tk.messagebox.showwarning(title="Attention",message="Renseigner un sexe avant de mettre à jour le modèle")


        elif(sex=='F' or sex=='M'):
            distances_all = []
            listeCombinaisonsDistance,listeCombinaisonsAngle = Externes.allPointsAngles()
            pt22 = ptsEchelle[0]
            pt24 = ptsEchelle[1]
            if(sex=='F'):sex=0
            if(sex=='M'):sex=1

            distances_all.append(sex)
            echelle3mm_px = Externes.euclideDist(pt22,pt24)
            for x in listeCombinaisonsDistance:
                distpx = Externes.euclideDist(ptsFish[x[0]],ptsFish[x[1]])
                distmm = round(3*distpx/echelle3mm_px,4)
                distances_all.append(distmm)
            for x in listeCombinaisonsAngle:
                thetas = Externes.calculAngle(ptsFish[x[0]],ptsFish[x[1]],ptsFish[x[2]])
                thetas = np.around(thetas[0],4)
                distances_all.append(thetas)

            # chemin = "C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho/"
            chemin2 = os.getcwd()
            if(len(chemin)>len(chemin2)):
                try:
                    f = open(chemin+"/DistancesPourModele.csv", "a+")
                except PermissionError:
                    print(Externes.checkIfProcessRunning("excel"))
                    print(Externes.checkIfProcessRunning("scalc"))
                    print(Externes.checkIfProcessRunning("soffice"))
                    print(Externes.checkIfProcessRunning("notepad"))

                    if(Externes.checkIfProcessRunning("excel")):
                        excel = Dispatch("Excel.Application")
                        excel.Visible=False
                        workbook = excel.Workbooks.Open(chemin+"/DistancesPourModele.csv")
                        excel.DisplayAlerts = False
                        excel.ActiveWorkbook.Save()
                        excel.Quit()
                        os.system('taskkill /f /im excel.exe')
                    if(Externes.checkIfProcessRunning("scalc")):
                        os.system('taskkill /f /im scalc.exe')

                    if(Externes.checkIfProcessRunning("soffice")):
                        os.system('taskkill /f /im soffice.exe')
                        os.system('taskkill /f /im soffice.bin')
                    if(Externes.checkIfProcessRunning("notepad")):
                        os.system('taskkill /f /im notepad.exe')
                    time.sleep(0.5)
                    f = open(chemin+"\DistancesPourModele.csv","a+")
            if(len(chemin2)>len(chemin)):
                try:
                    f = open(chemin2+"\DistancesPourModele.csv","a+")
                except PermissionError:
                    print(Externes.checkIfProcessRunning("excel"))
                    print(Externes.checkIfProcessRunning("scalc"))
                    print(Externes.checkIfProcessRunning("soffice"))
                    print(Externes.checkIfProcessRunning("notepad"))

                    if(Externes.checkIfProcessRunning("excel")):
                        excel = Dispatch("Excel.Application")
                        excel.Visible=False
                        workbook = excel.Workbooks.Open(chemin2+"\DistancesPourModele.csv")
                        excel.DisplayAlerts = False
                        excel.ActiveWorkbook.Save()
                        excel.Quit()
                        os.system('taskkill /f /im excel.exe')
                    if(Externes.checkIfProcessRunning("scalc")):
                        os.system('taskkill /f /im scalc.exe')

                    if(Externes.checkIfProcessRunning("soffice")):
                        os.system('taskkill /f /im soffice.exe')
                        os.system('taskkill /f /im soffice.bin')
                    if(Externes.checkIfProcessRunning("notepad")):
                        os.system('taskkill /f /im notepad.exe')
                    time.sleep(0.5)
                    f = open(chemin2+"\DistancesPourModele.csv","a+")

            header = ['Sexe (0:F, 1:M)']+listeCombinaisonsDistance+listeCombinaisonsAngle
            header = "; ".join(str(i) for i in header)
            distances_all = "; ".join(str(i) for i in distances_all)
            f.seek(0)
            if(f.read(1)!="S"):
                f.write(str(header)+"\n")
            f.read()
            f.write(str(distances_all)+"\n")
            f.close()

        else:
            tk.messagebox.showwarning(title="Attention",message="Le sexe doit être F ou M")


        # return distances_all

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

    def findNearestValueFromArray(array, value):
        import numpy as np
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

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

    def centerPoint(pt,eye):
        return [pt[0]-(eye[0]-300),pt[1]-(eye[1]-250)]

    def decenterPoint(A,eye):
        return [A[0]+eye[0]-300,A[1]+eye[1]-250]

    def centerPoints(lstpt,eye):
        new_lstpt = []
        for x in lstpt:
            new_lstpt.append(Externes.centerPoint(x,eye))
        return new_lstpt

    def projeteOrtho(pente,intercept,xA,yA):
        import numpy as np
        matriceA = np.array([[pente,-1],[1,pente]])
        vecteurB = np.array([[-intercept],[xA+pente*yA]])
        invMatA = np.linalg.inv(matriceA)
        projete = np.dot(invMatA,vecteurB)
        return projete

    def findNearestPointFromListOfPoints(pointA,listeOfPoints):
        import numpy as np
        #liste = [[x,y],[x,y]...]
        #point = [x,y]
        listeDistances = [Externes.euclideDist(pointA,x) for x in listeOfPoints]
        indexMin = np.argmin(listeDistances)
        pointB = listeOfPoints[indexMin]
        distance = listeDistances[indexMin]
        return indexMin,pointB,distance


    def checkIfProcessRunning(processName):
        import psutil
        #Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def penteIntercept(a,b):
        if(b[0]-a[0]==0):
            pente =  (b[1]-a[1])/0.001
        else:
            pente = (b[1]-a[1])/(b[0]-a[0])
        intercept = b[1]-pente*b[0]
        return (pente,intercept)

    def isContoursLineLike(c):
        import numpy as np
        #[[ [x1,y1]
        top = tuple(c[c[:, :, 1].argmin()][0])
        bottom = tuple(c[c[:, :, 1].argmax()][0])
        pente,intercept = Externes.penteIntercept(top,bottom)

        # plt.plot(top[0],top[1],'ro')
        # plt.plot(bottom[0],bottom[1],'go')

        listPointDroite = []
        x = c.T[0][0]
        y = c.T[1][0]

        abscisse = x
        ordonnee = np.round(pente*abscisse+intercept,1)

        # print(abscisse)
        # print(ordonnee)
        # plt.figure()
        # plt.plot(abscisse,ordonnee)
        distanceTotale = 0
        for i in range(len(ordonnee)):
            distanceTotale += (y[i]-ordonnee[i])**2

        # plt.plot(x,y)

        # plt.show()




        return pente,distanceTotale