''' Bibliothèque de fonctions externes '''

import sys,inspect,os
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])

class Externes():
    def euclide(X,Y):
        """!
        Efficiently calculates the euclidean distance
        between two vectors using Numpys einsum function.
        @param X : array, (n_samples x d_dimensions)
        @param Y : array, (n_samples x d_dimensions)
        @return D : array, (n_samples, n_samples)
        """
        import numpy as np
        XY = np.array(X)-np.array(Y)
        return np.sqrt(np.einsum('i,i->', XY, XY))

    def calculAngle(pt1,pt2,pt3):
        """!
        Methode pour calculer les 3 angles du triangle crée par 3 points
        @param pt1 tuple : coordonnees du point1 : [x1,y1]
        @param pt2 tuple : coordonnees du point2 : [x2,y2]
        @param pt3 tuple : coordonnees du point3 : [x3,y3]
        @return listeAngle list of float : liste des 3 angles
        """
        from math import acos,pi
        b = Externes.euclide(pt1,pt2)
        a = Externes.euclide(pt2,pt3)
        c = Externes.euclide(pt1,pt3)
        Apt1 = acos((b**2+c**2-a**2)/(2*b*c))*180/pi
        Apt2 = acos((b**2+a**2-c**2)/(2*b*a))*180/pi
        Apt3 = acos((a**2+c**2-b**2)/(2*a*c))*180/pi
        listeAngle = [Apt1,Apt2,Apt3]
        return listeAngle

    def calculAngleBis(pt1,pt2,pt3):
        """!
        Methode pour calculer les 3 angles du triangle crée par 3 points
        @param pt1 tuple : coordonnees du point1 : [x1,y1]
        @param pt2 tuple : coordonnees du point2 : [x2,y2]
        @param pt3 tuple : coordonnees du point3 : [x3,y3]
        @return Apt2 float : angle du point2
        """
        b = Externes.euclide(pt1,pt2)
        a = Externes.euclide(pt2,pt3)
        c = Externes.euclide(pt1,pt3)
        from math import acos,pi
        Apt2 = acos((b**2+a**2-c**2)/(2*b*a))*180/pi
        return Apt2

    def reorder_from_idx(idx, a):
        """!
        Methode pour avoir la liste décalée de a indice vers la gauche
        @param idx int : indice de décalage
        @param a list : liste de référence
        @return list : liste décalée
        """
        return a[idx:] + a[:idx]

    def cyclic_perm(a):
        """!
        Methode pour avoir toutes les permutations circulaire possibles
        @param a list : liste de référence
        @return list of object : liste des permutations circulaires
        """
        from functools import partial
        return [partial(Externes.reorder_from_idx, i) for i in range(len(a))]

    def allPointsAngles():
        """!
        Methode pour les combinaisons des points pour les distances (2 pts) et angles (3 pts)
        @return listeDistance,listeAngle: liste des indices des points
        """
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
        """!
        Methode pour convertir pixel en mm
        @param distance_px float : distance en pixel
        @param echelle float : echelle en pixel
        @return float : distance en mm
        """
        return round(3*distance_px/echelle,4)

    def px3mmListe(distances_px,echelle):
        """!
        Methode pour convertir une liste de distances pixel en mm
        @param distances_px list of float : liste de distances en pixel
        @param echelle float : echelle en pixel
        @return distances list of float : liste de distances en mm
        """
        distances = []
        for x in distances_px:
            distances.append(Externes.px3mm(x,echelle))
        return distances

    def px10mm(distance_px,echelle):
        """!
        Methode pour convertir pixel en mm
        @param distance_px float : distance en pixel
        @param echelle float : echelle en pixel
        @return float : distance en mm
        """
        return round(10*distance_px/echelle,4)

    def px10mmListe(distances_px,echelle):
        """!
        Methode pour convertir une liste de distances pixel en mm
        @param distances_px list of float : liste de distances en pixel
        @param echelle float : echelle en pixel
        @return distances list of float : liste de distances en mm
        """
        distances = []
        for x in distances_px:
            distances.append(Externes.px10mm(x,echelle))
        return distances

    def genererAllDistancesHead(ptsEchelle,ptsFish,sex,chemin):
        """!
        Methode pour generer les distances et angles de la tete et remplir le fichier csv
        @param ptsEchelle list of tuple : liste des points de l'echelle
        @param ptsFish list of tuple : liste des points de la tête
        @param sex char : F ou M
        @param chemin String : chemin du fichier csv
        """
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
            echelle3mm_px = Externes.euclide(pt22,pt24)
            for x in listeCombinaisonsDistance:
                distpx = Externes.euclide(ptsFish[x[0]],ptsFish[x[1]])
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


    def calculDistances(ptsEchelle,ptsFish):
        """!
        Methode pour calculer les distances affichées sur l'interface
        @param ptsEchelle list of tuple : liste des points de l'echelle
        @param ptsFish list of tuple : liste des points de la tête
        @return distances_check list of float : liste des distances en mm
        """
        print(ptsEchelle)
        # echelle3mm = Externes.euclide(ptsEchelle[0],ptsEchelle[1])
        echelle3mm = 1
        snout_eye = Externes.euclide(ptsFish[0],ptsFish[1])
        snout_length = Externes.euclide(ptsFish[1],ptsFish[2])
        eye_diameter = Externes.euclide(ptsFish[0],ptsFish[8])
        head_length = Externes.euclide(ptsFish[1],ptsFish[7])
        head_depth = Externes.euclide(ptsFish[4],ptsFish[7])
        jaw_length = Externes.euclide(ptsFish[2],ptsFish[3])
        jaw_length2 = Externes.euclide(ptsFish[1],ptsFish[3])
        distances_check = [snout_eye,snout_length,eye_diameter,head_length,head_depth,jaw_length,jaw_length2]
        distances_check = Externes.px3mmListe(distances_check,echelle3mm)
        return distances_check

    def calculDistances2(ptsEchelle,ptsFish):
        """!
        Methode pour calculer les distances affichées sur l'interface
        @param ptsEchelle list of tuple : liste des points de l'echelle
        @param ptsFish list of tuple : liste des points du corps
        @return distances_check list of float : liste des distances en mm
        """
        # echelle10mm = Externes.euclide(ptsEchelle[0],ptsEchelle[1])
        echelle10mm = 1
        # body_size = Externes.euclide(ptsFish[0],ptsFish[2])
        body_size=1
        # body_depth = Externes.euclide(ptsFish[1],ptsFish[3])
        body_depth = 1
        distances_check = [body_size,body_depth]
        distances_check = Externes.px10mmListe(distances_check,echelle10mm)
        return distances_check

    def findNearestValueFromArray(array, value):
        """!
        Methode pour trouver a partir d'une valeur de référence, la valeur la plus proche dans une liste
        @param array list : liste de référence
        @param value float : valeur a trouver ou se rapprocher
        @return idx float : indice de la valeur la plus proche de ce qu'on cherche
        """
        import numpy as np
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        dist = np.min(np.abs(array - value))
        print(dist)
        return idx,dist

    def openfn():
        """!
        Methode pour sélectionner les images dans la fenetre
        """
        import tkinter.filedialog,tkinter as tk
        filepath = tk.filedialog.askopenfilenames(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('jpeg files','.jpeg')])
        return filepath

    def opentps():
        """!
        Methode pour sélectionner les images dans la fenetre
        """
        import tkinter.filedialog,tkinter as tk
        filepath = tk.filedialog.askopenfilename(title="Ouvrir le fichier tps",filetypes=[('tps files','.tps')])
        return filepath

    def openxml():
        """!
        Methode pour sélectionner les images dans la fenetre
        """
        import tkinter.filedialog,tkinter as tk
        filepath = tk.filedialog.askopenfilename(title="Ouvrir le fichier xml",filetypes=[('xml files','.xml')])
        return filepath

    def opencsv():
        """!
        Methode pour sélectionner les images dans la fenetre
        """
        import tkinter.filedialog,tkinter as tk
        filepath = tk.filedialog.askopenfilename(title="Ouvrir le fichier csv",filetypes=[('csv files','.csv')])
        return filepath

    def openfolder():
        """!
        Methode pour sélectionner les images dans la fenetre
        """
        import tkinter.filedialog,tkinter as tk
        filepath = tk.filedialog.askdirectory()
        return filepath

    def Longueur(distance):
        """!
        Methode pour modifier les distances affichées sur l'interface
        @param distance list of tuple :liste des distances en mm
        @return texte String : texte affiché sur l'interface
        """
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
        """!
        Methode pour modifier les distances affichées sur l'interface
        @param distance list of tuple :liste des distances en mm
        @return texte String : texte affiché sur l'interface
        """
        texte = ""
        texte += "8 <-> 10 : Longueur Corps : "+str(distance[0])+" mm \n"
        texte += " 13 <-> 15 : Largeur corps : "+str(distance[1])+" mm \n"
        return texte

    def centerPoint(pt,eye):
        """!
        Methode pour centrer un point sur l'interface
        @param pt tuple : point à décaler
        @return tuple : point décalé
        """
        return [pt[0]-(eye[0]-300),pt[1]-(eye[1]-250)]

    def decenterPoint(A,eye):
        """!
        Methode pour décentrer un point sur l'interface
        @param pt tuple : point à décaler
        @return tuple : point décalé
        """
        return [A[0]+eye[0]-300,A[1]+eye[1]-250]

    def centerPoints(lstpt,eye):
        """!
        Methode pour centrer des points sur l'interface
        @param lstpt tuple : liste de points à décaler
        @return new_lstpt : liste de points décalés
        """
        new_lstpt = []
        for x in lstpt:
            new_lstpt.append(Externes.centerPoint(x,eye))
        return new_lstpt

    def projeteOrtho(pente,intercept,xA,yA):
        """!
        Methode pour calculer le projete orthogonal d'un point sur une droite
        @param float pente : pente de la droite
        @param float intercept : ordonnee à l'origine de la droite
        @param float xA : abscisse du point
        @param float yA : ordonnee du point
        @return projete float : coordonnées du projete
        """
        import numpy as np
        matriceA = np.array([[pente,-1],[1,pente]])
        vecteurB = np.array([[-intercept],[xA+pente*yA]])
        invMatA = np.linalg.inv(matriceA)
        projete = np.dot(invMatA,vecteurB)
        return projete

    def findNearestPointFromListOfPoints(pointA,listeOfPoints):
        """!
        Methode pour trouver a partir d'une point de référence, le point le plus proche dans une liste
        @param listeOfPoints list of tuple : liste de points
        @param pointA tuple : point a trouver ou se rapprocher
        @return indexMin int : indice du point le plus proche de ce qu'on cherche
        @return pointB tuple : point le plus proche
        @return distance float : distance du pointA au point le plus proche
        """
        import numpy as np
        #liste = [[x,y],[x,y]...]
        #point = [x,y]
        listeDistances = [Externes.euclide(pointA,x) for x in listeOfPoints]
        indexMin = np.argmin(listeDistances)
        pointB = listeOfPoints[indexMin]
        distanceMin = listeDistances[indexMin]
        return indexMin,pointB,distanceMin


    def checkIfProcessRunning(processName):
        """!
        Methode pour déterminer si un processus est en cours ou non
        @param processName String : nom du processus
        @return boolean : Vrai ou Faux
        """
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
        """!
        Methode pour trouver la droite passant par deux points
        @param a tuple : point a
        @param b tuple : point b
        @return pente : pente de la droite
        @return intercept : ordonnees à l'origine de la droite
        """
        if(b[0]-a[0]==0):
            pente =  (b[1]-a[1])/0.001
        else:
            pente = (b[1]-a[1])/(b[0]-a[0])
        intercept = b[1]-pente*b[0]
        return (pente,intercept)

    def isContoursLineLike(c):
        """!
        Methode pour avoir des informations sur le caractère longiligne du contours
        @param c contours (list of tuple) : contours de l'image
        @return pente float : pente de la droite passant par le contours
        @return distanceTotale float : distance des points du contours à la droite du contours
        """
        import numpy as np
        top = tuple(c[c[:, :, 1].argmin()][0])
        bottom = tuple(c[c[:, :, 1].argmax()][0])
        pente,intercept = Externes.penteIntercept(top,bottom)
        x = c.T[0][0]
        y = c.T[1][0]
        abscisse = x
        ordonnee = np.round(pente*abscisse+intercept,1)
        distanceTotale = 0
        for i in range(len(ordonnee)):
            distanceTotale += (y[i]-ordonnee[i])**2
        return pente,distanceTotale

    def averagePixelValue(imgNB,c,windowSize):
        """!
        Methode pour calculer la valeur moyenne autour d'un contour
        @param imgNB list of list: matrice de l'image en noir et blanc
        @param c contours : 1 contour de l'image
        @param windowSize : taille du voisinage (à choisir impair)
        @return moy float : valeur moyenne de niveau de gris
        """
        import numpy as np
        import itertools
        x = c.T[0][0]
        y = c.T[1][0]
        low = (windowSize-1)//2
        up = (windowSize+1)//2
        test =  list(itertools.chain.from_iterable([list(itertools.product(range(x[i]-low,x[i]+up),range(y[i]-low,y[i]+up))) for i in range(len(x))]))
        pixel = [imgNB[x[1]][x[0]] for x in test]
        moy = np.mean(pixel)
        return moy

    def averagePixelsValue(imgNB,listePoints):
        import numpy as np
        mean = np.median([imgNB[x[1]][x[0]] for x in listePoints])
        return mean


    def diamondCV2():
        """!
        Methode pour avoir le patron de diamant
        @return diamond list of list : matrice de 1 et de 0 représentant un diamant
        """
        import cv2
        diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        diamond[0, 0] = 0
        diamond[0, 1] = 0
        diamond[1, 0] = 0
        diamond[4, 4] = 0
        diamond[4, 3] = 0
        diamond[3, 4] = 0
        diamond[4, 0] = 0
        diamond[4, 1] = 0
        diamond[3, 0] = 0
        diamond[0, 3] = 0
        diamond[0, 4] = 0
        diamond[1, 4] = 0
        return diamond

    def resource_path(relative_path):
        """!
        Méthode permettant d'avoir le chemin absolu temporaire (pour l'exe) ou normal
        @param relative_path String : chemin du fichier dans le pc
        @return resource_path : chemin temporaire
        """

        try:
            base_path = sys._MEIPASS
            print(base_path)
        except Exception:
            base_path = pypath2+"/images/"
            base_path = '/'.join(pypath1.split("/")[:-1])+"/images"

        return os.path.join(base_path, relative_path)

    def getVersion():
        """!
        Méthode permettant d'avoir la dernière version du projet
        @return version float (par exemple 1.4, 1.5)
        """
        import requests
        response = str(requests.get('https://github.com/RalphMasson/MorphoEpinoche/tags').content)
        response = response.split('\\n')
        response = [x if ".zip" in x else '' for x in response]
        response = list(filter(None, response))
        response = ''.join(response).split(" ")
        response = list(filter(None, response))
        response = [x if x.startswith("href") else '' for x in response]
        response = list(filter(None, response))
        response = ','.join(response).split('"')
        response = [x if x.endswith(".zip") else '' for x in response]
        response = list(filter(None, response))
        response = ''.join(response).split("/")
        response = [x if x.endswith(".zip") else '' for x in response]
        response = list(filter(None, response))
        response = ','.join(response).replace(".zip","").replace("v","").split(",")
        response = max(list(map(float,response)))
        version = response
        return version

    def changer_noir_en_blanc(img):
        """!
        Méthode permettant de changer le fond noir en blanc
        @param img : image detouree avec fond noir
        @return img : image detouree avec fond blanc
        """
        import cv2
        IMG_DETOURE_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mask = cv2.compare(IMG_DETOURE_gray,5,cv2.CMP_LT)
        img[mask > 0] = 255
        return img

    def mask_points_rouges(img):
        """!
        Méthode permettant d'avoir le masque des points rouges (pointage)
        @param img : image non détourée pointée en rouge
        @return mask : masque des points rouges de l'image non détourée
        """
        import cv2
        IMG_POINTE_hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
        lower,upper = Externes.low_up_red()
        mask = cv2.inRange(IMG_POINTE_hsv, lower, upper)
        return mask

    def low_up_red():
        """!
        Méthode permettant les bornes de la couleur rouge
        @return lower,upper : bornes inférieure et supérieure du rouge
        """
        import numpy as np
        lower = np.array([0,230,230])
        upper = np.array([1,255,255])
        return lower,upper

    def pointage_image_detouree(img_pointe,img_detoure):
        """!
        Méthode permettant de transferer les points rouges sur l'image détourée
        @param img_pointe : path image non détourée et pointée
        @param img_detoure : path image détourée et non pointée
        @return IMG_DETOURE : image détourée et pointée
        """
        import cv2
        IMG_POINTE = cv2.imread(img_pointe)
        IMG_POINTE = cv2.cvtColor(IMG_POINTE,cv2.COLOR_BGR2RGB)
        IMG_DETOURE = cv2.imread(img_detoure)
        IMG_DETOURE = cv2.cvtColor(IMG_DETOURE,cv2.COLOR_BGR2RGB)
        IMG_DETOURE = cv2.resize(IMG_DETOURE,(4000,3000))
        IMG_DETOURE = Externes.changer_noir_en_blanc(IMG_DETOURE)
        mask = Externes.mask_points_rouges(IMG_POINTE)
        IMG_DETOURE[mask != 0] = [255,0,0]

        return IMG_DETOURE

    def grossir_point(IMG_DETOURE,iterations):
        """!
        Méthode permettant de grossir les points après transfert
        @param IMG_DETOURE : image detouree et pointee
        @param iterations : nombre d'itérations (default = 5)
        @return IMG_DETOURE : image detouree et pointee
        """
        import cv2
        import numpy as np
        for k in range(iterations):
            IMG_DETOURE_hsv = cv2.cvtColor(IMG_DETOURE,cv2.COLOR_RGB2HSV)
            lower,upper = Externes.low_up_red()
            mask = cv2.inRange(IMG_DETOURE_hsv, lower, upper)
            x_red = np.where(mask!=0)[0]
            y_red = np.where(mask!=0)[1]
            for i in range(len(x_red)):
                IMG_DETOURE[x_red[i]-1][y_red[i]+1] = [255,0,0]
                IMG_DETOURE[x_red[i]][y_red[i]+1] = [255,0,0]
                IMG_DETOURE[x_red[i]+1][y_red[i]+1] = [255,0,0]
                IMG_DETOURE[x_red[i]-1][y_red[i]] = [255,0,0]
                IMG_DETOURE[x_red[i]+1][y_red[i]] = [255,0,0]
                IMG_DETOURE[x_red[i]-1][y_red[i]-1] = [255,0,0]
                IMG_DETOURE[x_red[i]][y_red[i]-1] = [255,0,0]
                IMG_DETOURE[x_red[i]+1][y_red[i]-1] = [255,0,0]
        return IMG_DETOURE

    def traitement_final_pointage(path_img_pointe,path_img_detoure):
        """!
        Méthode utilisant les méthodes décrites précédemment
        @param img_pointe : path image non détourée et pointée
        @param img_detoure : path image détourée et non pointée
        @return img_detoure : image detouree et pointee
        """
        img_detoure = Externes.pointage_image_detouree(path_img_pointe,path_img_detoure)
        img_detoure = Externes.grossir_point(img_detoure,5)
        # path_img_pointe = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_pointe\\Dataset1\\IMGP1862M.JPG"
        # path_img_detoure = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_detoure\\Dataset1\\IMGP1862M.JPG"

        return img_detoure


    def getRandomPointInCircle(r,xc,yc):
        import random
        import math

        circle_r = r
        circle_x = xc
        circle_y = yc
        alpha = 2 * math.pi * random.random()
        r = circle_r * math.sqrt(random.random())
        x = int(r * math.cos(alpha) + circle_x)
        y = int(r * math.sin(alpha) + circle_y)
        return x,y


    def getRandomPointsInCircleOriented(r,xc,yc,orientation):
        import random
        import math
        import numpy as np

        circle_r = np.linspace(0,int(r),int(r)+1)
        circle_x = int(xc)
        circle_y = int(yc)
        if(orientation=='nw'):
            alpha = 1/0.93*math.pi
        if(orientation=='nw1'):
            alpha = 1/0.95*math.pi
        if(orientation=='nw2'):
            alpha = 1/0.97*math.pi
        if(orientation=='sw'):
            alpha = 0.93*math.pi
        if(orientation=='sw1'):
            alpha = 0.95*math.pi
        if(orientation=='sw2'):
            alpha = 0.97*math.pi
        x = circle_r * math.cos(alpha) + circle_x
        y = circle_r * math.sin(alpha) + circle_y
        return [x,y]


    def getRandomPointsInCircle(r,xc,yc,n):
        listePoints = [Externes.getRandomPointInCircle(r,xc,yc) for _ in range(n)]
        return listePoints

    def lissage(signal_brut):
        from scipy.signal import savgol_filter
        signal_lisse = savgol_filter(signal_brut,window_length=51,polyorder=6,deriv=0)
        return signal_lisse

    def derive(signal_lisse):
        from scipy.signal import savgol_filter
        signal_derive = savgol_filter(signal_brut,window_length=51,polyorder=6,deriv=1)
        return signal_derive

    def removeOutliers(x, outlierConstant):
        import numpy as np
        a = np.array(x)
        upper_quartile = np.percentile(a, 75)
        lower_quartile = np.percentile(a, 25)
        IQR = (upper_quartile - lower_quartile) * outlierConstant
        quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
        resultList = []
        # print(quartileSet)
        for y in a.tolist():
            if y >= quartileSet[0] and y <= quartileSet[1]:
                resultList.append(y)
        return resultList

    def displayGraph(longueur_deplacement,liste,intensite_est):
        # plt.figure()
        # for x in liste:
        #     plt.plot(longueur_deplacement,x)
        # plt.plot(longueur_deplacement,intensite_est)
        # plt.legend('intensite_nw','intensite_nw1','intensite_sw','intensite_sw1','intensite_ouest','intensite_est')
        return 0

    def cheminAvant(aaa):
        return "\\".join(aaa.split("\\")[:-1])+"\\"
    def cheminAvant2(aaa):
        return "/".join(aaa.split("/")[:-1])+"/"
    def sizeKoParent(path_et_nom_fichier_extension):
        return str(round(int(os.path.getsize(path_et_nom_fichier_extension)/1048)))+" Ko"
