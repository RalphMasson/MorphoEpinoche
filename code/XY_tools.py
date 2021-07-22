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

    def px3mm(distance_px,echelle):
        """!
        Methode pour convertir pixel en mm
        @param distance_px float : distance en pixel
        @param echelle float : echelle en pixel
        @return float : distance en mm
        """
        return round(50*distance_px/echelle,4)

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
        return round(50*distance_px/echelle,4)

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

    def calculDistances(ptsEchelle,ptsFish):
        """!
        Methode pour calculer les distances affichées sur l'interface
        @param ptsEchelle list of tuple : liste des points de l'echelle
        @param ptsFish list of tuple : liste des points de la tête
        @return distances_check list of float : liste des distances en mm
        """
        echelle3mm = Externes.euclide(ptsEchelle[0],ptsEchelle[1])
        # echelle3mm = 1
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

    def calculDistancesv2(ptsEchelle,listepoints):
        """!
        all except LS
        ['LS', 'L1-2', 'L1-3', 'L1-4', 'L1-5', 'L1-6', 'L1-7', 'L1-8', 'L1-9',
        'L1-10', 'L2-3', 'L2-4', 'L2-5', 'L2-6', 'L2-7', 'L2-8', 'L2-9',
        'L2-10', 'L3-4', 'L3-5', 'L3-6', 'L3-7', 'L3-8', 'L3-9', 'L3-10',
        'L4-5', 'L4-6', 'L4-7', 'L4-8', 'L4-9', 'L4-10', 'L5-6', 'L5-7', 'L5-8',
        'L5-9', 'L5-10', 'L6-7', 'L6-8', 'L6-9', 'L6-10', 'L7-8', 'L7-9',
        'L7-10', 'L8-9', 'L8-10', 'L9-10']
        """

        distances = []
        echelle3mm = Externes.euclide(ptsEchelle[0],ptsEchelle[1])

        L12 = Externes.euclide(listepoints[0],listepoints[1])
        L13 = Externes.euclide(listepoints[0],listepoints[2])
        L14 = Externes.euclide(listepoints[0],listepoints[3])
        L15 = Externes.euclide(listepoints[0],listepoints[4])
        L16 = Externes.euclide(listepoints[0],listepoints[5])
        L17 = Externes.euclide(listepoints[0],listepoints[6])
        L18 = Externes.euclide(listepoints[0],listepoints[7])
        L19 = Externes.euclide(listepoints[0],listepoints[8])
        L110 = Externes.euclide(listepoints[0],listepoints[9])

        L23 = Externes.euclide(listepoints[1],listepoints[2])
        L24 = Externes.euclide(listepoints[1],listepoints[3])
        L25 = Externes.euclide(listepoints[1],listepoints[4])
        L26 = Externes.euclide(listepoints[1],listepoints[5])
        L27 = Externes.euclide(listepoints[1],listepoints[6])
        L28 = Externes.euclide(listepoints[1],listepoints[7])
        L29 = Externes.euclide(listepoints[1],listepoints[8])
        L210 = Externes.euclide(listepoints[1],listepoints[9])

        L34 = Externes.euclide(listepoints[2],listepoints[3])
        L35 = Externes.euclide(listepoints[2],listepoints[4])
        L36 = Externes.euclide(listepoints[2],listepoints[5])
        L37 = Externes.euclide(listepoints[2],listepoints[6])
        L38 = Externes.euclide(listepoints[2],listepoints[7])
        L39 = Externes.euclide(listepoints[2],listepoints[8])
        L310 = Externes.euclide(listepoints[2],listepoints[9])

        L45 = Externes.euclide(listepoints[3],listepoints[4])
        L46 = Externes.euclide(listepoints[3],listepoints[5])
        L47 = Externes.euclide(listepoints[3],listepoints[6])
        L48 = Externes.euclide(listepoints[3],listepoints[7])
        L49 = Externes.euclide(listepoints[3],listepoints[8])
        L410 = Externes.euclide(listepoints[3],listepoints[9])

        L56 = Externes.euclide(listepoints[4],listepoints[5])
        L57 = Externes.euclide(listepoints[4],listepoints[6])
        L58 = Externes.euclide(listepoints[4],listepoints[7])
        L59 = Externes.euclide(listepoints[4],listepoints[8])
        L510 = Externes.euclide(listepoints[4],listepoints[9])

        L67 = Externes.euclide(listepoints[5],listepoints[6])
        L68 = Externes.euclide(listepoints[5],listepoints[7])
        L69 = Externes.euclide(listepoints[5],listepoints[8])
        L610 = Externes.euclide(listepoints[5],listepoints[9])

        L78 = Externes.euclide(listepoints[6],listepoints[7])
        L79 = Externes.euclide(listepoints[6],listepoints[8])
        L710 = Externes.euclide(listepoints[6],listepoints[9])

        L89 = Externes.euclide(listepoints[7],listepoints[8])
        L810 = Externes.euclide(listepoints[7],listepoints[9])

        L910 = Externes.euclide(listepoints[8],listepoints[9])

        distances = [L12, L13, L14, L15, L16, L17, L18, L19, L110, L23, L24, L25, L26, L27, L28, L29, L210, L34, L35, L36, L37, L38, L39, L310, L45, L46, L47, L48, L49, L410, L56, L57, L58, L59, L510, L67, L68, L69, L610, L78, L79, L710, L89, L810, L910]
        distances = Externes.px3mmListe(distances,echelle3mm)

        return distances

    def calculDistances2(ptsEchelle,ptsFish):
        """!
        Methode pour calculer les distances affichées sur l'interface
        @param ptsEchelle list of tuple : liste des points de l'echelle
        @param ptsFish list of tuple : liste des points du corps
        @return distances_check list of float : liste des distances en mm
        """
        echelle10mm = Externes.euclide(ptsEchelle[0],ptsEchelle[1])
        body_size = Externes.euclide(ptsFish[0],ptsFish[1])
        distances_check = [body_size]
        distances_check = Externes.px10mmListe(distances_check,echelle10mm)
        return distances_check

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
        texte += "2 <-> 3 : diametre oeil : "+str(distance[2])+" mm \n"
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
        # texte += "8 <-> 10 : Longueur Corps : "+str(distance[0])+" mm \n"
        # texte += " 13 <-> 15 : Largeur corps : "+str(distance[1])+" mm \n"
        return texte

    def centerPoint(pt,eye,dx,dy):
        """!
        Methode pour centrer un point sur l'interface
        @param pt tuple : point à décaler
        @return tuple : point décalé
        HeadFish : -200, -200
        ScaleFish : -25 -50
        ScaleFishBody : -25 - 125
        """
        return [pt[0]-(eye[0]-dx),pt[1]-(eye[1]-dy)]


    def centerPoints(lstpt,eye,dx,dy):
        """!
        Methode pour centrer des points sur l'interface
        @param lstpt tuple : liste de points à décaler
        @return new_lstpt : liste de points décalés
        """
        new_lstpt = []
        for x in lstpt:
            new_lstpt.append(Externes.centerPoint(x,eye,dx,dy))
        return new_lstpt



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

    def verbose_points(listepoints,listeImages,numImage):
        message = "\n# Détails de l'image n°"+str(numImage)+":\n"
        listepoints = listepoints[0]
        message += "\t Points :"+str(listepoints)
        # message += "point n°"+str(i)+": "+"X = "+str(listepoints[i][0])+" Y = " +str(listepoints[i][1])+"\t"
        message += "\n"
        return message

    def cheminAvant(aaa):
        return "\\".join(aaa.split("\\")[:-1])+"\\"
    def cheminAvant2(aaa):
        return "/".join(aaa.split("/")[:-1])+"/"
    def sizeKoParent(path_et_nom_fichier_extension):
        return str(round(int(os.path.getsize(path_et_nom_fichier_extension)/1048)))+" Ko"
