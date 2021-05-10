# Pour assurer le bon fonctionnement
import sys
sys.path.insert(0, 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho')

# Import des bibliothèques (s'assurer qu'elles soient installées)
import tkinter as tk
from PIL import Image, ImageTk
import math,functools,itertools,os,cv2
import Placement,Fonctions,Classification
import numpy as np

# Classe pour les points de la tête
class HeadClass():
    """Variables globales pour export
    id_polygons : liste des id des polygons (la tete et l'echelle)
    pointsTete : liste des points de la tête [(x1,y1),(x2,y2)...]
    pointsEchelle3mm : liste des points de l'echelle [(x1,y1),(x2,y2)]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    """
    id_polygons = pointsFish = pointsEchelle = distances_check = distances_all = []

    def __init__(self, canvas, points,color):
        """!
        Constructeur du polygone de la tête
        @param canvas tk.Canvas : cadre de l'image
        @param points list : liste des points du polygone
        @param color String : couleur du polygone
        """
        self.previous_x = self.previous_y = self.selected = self.x = None
        self.points = points

        if points!=None:
            if color=='red':outline='red'
            else: outline=''
            self.polygon = canvas.create_polygon(self.points,fill='',outline=outline,smooth=0,width=2,dash=())
            HeadClass.id_polygons.append(self.polygon)
            canvas.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas))
            canvas.tag_bind(self.polygon, '<B1-Motion>', lambda event = self.polygon : self.on_move_polygon(event,canvas))
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                label = canvas.create_text((x+15, y+6),text=str(node%25),font=("Purisa", 1),fill='red')
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas))
                canvas.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas))

        HeadClass.update_points(canvas)

        if(len(HeadClass.pointsEchelle)>0):
             Interface.afficheLongueur()

    def update_points(canvas):
        """!
        Methode de mise à jour de la position des points
        """
        for id in HeadClass.id_polygons:
            liste = canvas.coords(id)
            if(len(canvas.coords(id))==18):HeadClass.pointsFish=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas.coords(id))==4):HeadClass.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

    def on_press_tag(self, event, number, tag):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = tag
        self.previous_x = event.x
        self.previous_y = event.y
        print(self.selected,event,tag)

    def on_release_tag(self, event, number, tag,canvas):
        self.selected = self.previous_x = self.previous_y = None
        HeadClass.update_points(canvas)

    def on_move_node(self, event, number,canvas):
        '''move single node in polygon'''
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            canvas.move(self.selected, dx, dy)
            # print(self.selected)
            canvas.move(self.nonodes[self.nodes.index(self.selected)],dx,dy)
            self.points[number][0] += dx
            self.points[number][1] += dy
            coords = sum(self.points, [])
            canvas.coords(self.polygon, coords)
            # print(canvas.coords(self.selected))
            self.previous_x = event.x
            self.previous_y = event.y
            try:
                if( (self.selected%25==13) or (self.selected%25==15)):
                    if(self.selected%25==13):
                        id13 = self.selected
                        id11 = id13-2
                        id15 = id13+2
                        id17 = id15+2
                    if(self.selected%25==15):
                        id15 = self.selected
                        id13 = id15-2
                        id11 = id13-2
                        id17 = id15+2
                    pt13_image = [canvas.coords(id13)[0]+3,canvas.coords(id13)[1]+3]
                    pt15_image = [canvas.coords(id15)[0]+3,canvas.coords(id15)[1]+3]
                    pt13_calcul = Placement.Points.decenterPoint(pt13_image,HeadFish.centreOeil)
                    pt15_calcul = Placement.Points.decenterPoint(pt15_image,HeadFish.centreOeil)
                    pt17,pt11 = Placement.Points.points11_17(HeadFish.CV2_image_big,pt13_calcul,pt15_calcul)
                    pt11_old = [canvas.coords(id11)[0]+3,canvas.coords(id11)[1]+3]
                    pt17_old = [canvas.coords(id17)[0]+3,canvas.coords(id17)[1]+3]
                    pt11,pt17 = Placement.Points.centerPoints([pt11,pt17],HeadFish.centreOeil)
                    canvas.move(id11,pt11[0]-pt11_old[0],pt11[1]-pt11_old[1])
                    canvas.move(id17,pt17[0]-pt17_old[0],pt17[1]-pt17_old[1])
                    canvas.update()
            except:
                None


        HeadClass.update_points(canvas)
        Interface.afficheLongueur()
    def on_move_polygon(self, event,canvas):
        '''move polygon and red rectangles in nodes'''
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            # move polygon
            canvas.move(self.selected, dx, dy)
            # move red nodes
            for item,item1 in zip(self.nodes,self.nonodes):
                canvas.move(item, dx, dy)
                canvas.move(item1,dx,dy)
            # recalculate values in self.points
            for item in self.points:
                item[0] += dx
                item[1] += dy
            self.previous_x = event.x
            self.previous_y = event.y
        HeadClass.update_points(canvas)

    def genererAllDistancesHead():
        HeadClass.distances_all = Fonctions.Externes.genererAllDistancesHead(HeadClass.pointsEchelle,HeadClass.pointsFish)

    def calculDistances():
        HeadClass.distances_check = Fonctions.Externes.calculDistances(HeadClass.pointsEchelle,HeadClass.pointsFish)
        return HeadClass.distances_check


class BodyClass():
    """Variables globales pour export
    id_polygons : liste des id des polygons (le corps et l'echelle)
    pointsTete : liste des points du corps [(x1,y1),(x2,y2)...]
    pointsEchelle3mm : liste des points de l'echelle [(x1,y1),(x2,y2)]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    """

    id_polygons = pointsFish = pointsEchelle = distances_all = distances_check = []

    def __init__(self, canvas1, points,color):

        self.previous_x = self.previous_y = self.selected = self.x = None
        self.points = points

        if points!=None:
            if color=='red':outline='red'
            else: outline=''
            self.polygon = canvas1.create_polygon(self.points,fill='',outline=outline,smooth=0,width=3,dash=())
            BodyClass.id_polygons.append(self.polygon)
            canvas1.tag_bind(self.polygon, '<ButtonPress-3>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag,canvas1))
            canvas1.tag_bind(self.polygon, '<ButtonRelease-3>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas1))
            canvas1.tag_bind(self.polygon, '<B3-Motion>',lambda event = self.polygon : self.on_move_polygon(event,canvas1))
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas1.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                label = canvas1.create_text((x+15, y+6),text=str(node%15),font=("Purisa", 1),fill='green')
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas1.tag_bind(node, '<ButtonPress-3>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag,canvas1))
                canvas1.tag_bind(node, '<ButtonRelease-3>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas1))
                canvas1.tag_bind(node, '<B3-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas1))

        BodyClass.update_points(canvas1)

        if(len(BodyClass.pointsFish)>0):
            Interface.afficheLongueurBody()

    def update_points(canvas1):
        for id in BodyClass.id_polygons:
            liste = canvas1.coords(id)
            if(len(canvas1.coords(id))==8):BodyClass.pointsFish=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas1.coords(id))==4):BodyClass.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

    def on_press_tag(self, event, number, tag,canvas1):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = tag
        self.previous_x = event.x
        self.previous_y = event.y
        BodyClass.update_points(canvas1)
        Interface.afficheLongueurBody()

    def on_release_tag(self, event, number, tag,canvas1):
        self.selected = self.previous_x = self.previous_y = None
        BodyClass.update_points(canvas1)
        Interface.afficheLongueurBody()

    def on_move_node(self, event, number,canvas1):
        '''move single node in polygon'''
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            canvas1.move(self.selected, dx, dy)
            canvas1.move(self.nonodes[self.nodes.index(self.selected)],dx,dy)
            self.points[number][0] += dx
            self.points[number][1] += dy
            coords = sum(self.points, [])
            # change points in polygons
            canvas1.coords(self.polygon, coords)
            self.previous_x = event.x
            self.previous_y = event.y

        BodyClass.update_points(canvas1)
        Interface.afficheLongueurBody()

    def on_move_polygon(self, event,canvas1):
        '''move polygon and red rectangles in nodes'''
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            # move polygon
            canvas1.move(self.selected, dx, dy)
            # move red nodes
            for item,item1 in zip(self.nodes,self.nonodes):
                canvas1.move(item, dx, dy)
                canvas1.move(item1,dx,dy)
            # recalculate values in self.points
            for item in self.points:
                item[0] += dx
                item[1] += dy
            self.previous_x = event.x
            self.previous_y = event.y

        BodyClass.update_points(canvas1)
        Interface.afficheLongueurBody()

    def calculDistances():
        BodyClass.distances_check = Fonctions.Externes.calculDistances2(BodyClass.pointsEchelle,BodyClass.pointsFish)
        return BodyClass.distances_check

class HeadFish():
    """Variables globales pour export
    id_polygons : liste des id des polygons (la tete et l'echelle)
    pointsTete : liste des points de la tête [(x1,y1),(x2,y2)...]
    pointsEchelle3mm : liste des points de l'echelle [(x1,y1),(x2,y2)]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    """
    poisson = None
    centreOeil=None
    CV2_image_big = None
    def __init__(self, canvas,PIL_image,CV2_image,size):
        self.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        self.circle = Fonctions.Externes.detect_eye(cv2.resize(CV2_image,size,Image.ANTIALIAS))
        HeadFish.centreOeil = [self.circle[0],self.circle[1]]
        HeadFish.poisson = canvas.create_image(0, 0, anchor=tk.NW,image=self.img)
        HeadFish.CV2_image_big = CV2_image
        canvas.move(HeadFish.poisson,-(self.circle[0]-300),-(self.circle[1]-250))
        app.bind("<Left>",self.moveLeft)
        app.bind("<Right>",self.moveRight)
        app.bind("<Up>",self.moveUp)
        app.bind("<Down>",self.moveDown)
    def moveLeft(self,event):
        canvas.move(HeadFish.poisson,-10,0)
    def moveRight(self,event):
        canvas.move(HeadFish.poisson,10,0)
    def moveUp(self,event):
        canvas.move(HeadFish.poisson,0,-10)
    def moveDown(self,event):
        canvas.move(HeadFish.poisson,0,10)

class BodyFish():
    poisson = None
    def __init__(self, canvas1,PIL_image,size):
        self.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        BodyFish.poisson = canvas1.create_image(0, 0, anchor=tk.NW, image=self.img)
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
    def move(self,event):
        if event.char=='q':
            canvas1.move(BodyFish.poisson,-10,0)
        if event.char=='s':
            canvas1.move(BodyFish.poisson,10,0)
        if event.char =='z':
            canvas1.move(BodyFish.poisson,0,-10)


class Interface(tk.Tk):
    numImageActuelle = 0
    listeImages = ""
    def __init__(self):
        super().__init__()

        ''' Fenetre et menu'''
        # root = tk.Tk()
        self.state('zoomed')
        self.title("Sex Determination for Three Spined Stickleback")
        menubar = tk.Menu(self)
        menuFichier = tk.Menu(menubar,tearoff=0)
        # menuFichier.add_command(label="Créer", command=None)
        menuFichier.add_command(label="Importer", command=None)
        # menuFichier.add_command(label="Editer", command=None)
        menuFichier.add_separator()
        menuFichier.add_command(label="Quitter", command=self.destroy)
        menubar.add_cascade(label="Fichier", menu=menuFichier)
        menuAide = tk.Menu(menubar, tearoff=0)
        menuAide.add_command(label="A propos", command=None)
        menubar.add_cascade(label="Aide", menu=menuAide)
        self.config(menu=menubar)

        CV2_image_big = None
        ''' Label Intro de presentation'''
        tk.Label(self,text=" ",font=("Purisa",12,"bold")).grid(ipadx=2)
        tk.Label(self,text=" \t Sexing procedure of three-spined stickleback \n",font=("Andalus",16,"bold")).place(x=750,y=40,anchor=tk.CENTER)
        tk.Label(self,text="\n \n \n \n ").grid(column=0,row=1)

        ''' Boutons '''
        tk.Label(self, text = 'PREDICTION',font=("Purisa",12,"bold"),fg='purple').place(x=460,y=70)
        tk.Button(self,text = "Import image and autoplace",command = self.importImage,fg='purple').place(x=400,y=100)
        tk.Button(self,text = "Predict",command = Interface.affichePrediction,fg='purple').place(x=570,y=100)
        tk.Label(self, text = 'ADD THESE VALUES TO MODEL',font=("Purisa",12,"bold"),fg='green').place(x=760,y=70)
        tk.Button(self,text = "Model Update (developpers only)",command = HeadClass.genererAllDistancesHead,fg='green').place(x=850,y=100)
        tk.Label(self,text='Sex for model: ',fg='green').place(x=725,y=105)
        tk.Button(self,text='<--',command = None).place(x=550,y=230)
        tk.Button(self,text='-->',command = self.nextImage).place(x=600,y=230)

        self.sexModel = tk.Entry(self,width=3)
        self.sexModel.place(x=810,y=105)

        self.sexPrediction = tk.Label(self,text="")
        self.sexPrediction.place(x=650,y=190)

        self.avertissement = tk.Label(self,text="")
        self.avertissement.place(x=650,y=160)

        self.explanation = tk.Label(self,text="\n ")
        self.explanation.grid(column=0,row=3)

        ''' Labels pour les longueurs de la tête '''
        tk.Label(self,text="Longueurs caractéristiques de la tête : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=0,row=4)
        self.Longueur = tk.Label(self,text="",justify=tk.LEFT)
        self.Longueur.grid(column=0,row=5)

        ''' Labels pour les longueurs du corps '''
        tk.Label(self,text="Longueurs caractéristiques du corps : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=1,row=4)
        self.LongueurBody = tk.Label(self,text="",justify=tk.LEFT)
        self.LongueurBody.grid(column=1,row=5)

        ''' Canvas pour la tête '''
        self.canvas = tk.Canvas(self,bg='#f0f0f0',bd=0,highlightthickness=1, highlightbackground="black")
        self.canvas.config(width=600, height=500)
        self.canvas.grid(column=0,row=8)

        ''' Canvas pour le corps '''
        self.canvas1 = tk.Canvas(self,bg='#f0f0f0',highlightthickness=1, highlightbackground="black")
        self.canvas1.config(width=960, height=500)
        self.canvas1.grid(column=1,row=8)

        """Canvas pour logo"""
        self.canvas2 = tk.Canvas(self,bg='#f0f0f0')
        self.canvas2.config(width=157,height=84)
        self.canvas2.place(x=0,y=0)
        self.logoPIL = ImageTk.PhotoImage(Image.open("C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho/images/logo2.png").resize((157,84)))
        self.canvas2.create_image(0, 0, anchor=tk.NW,image=self.logoPIL)


        self.canvas3 = tk.Canvas(self,bg='#f0f0f0')
        self.canvas3.config(width = 288,height=192)
        self.canvas3.place(x=1250,y=0)
        self.schema = ImageTk.PhotoImage(Image.open("C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho/images/schema.png").resize((288,192)))
        self.canvas3.create_image(0,0,anchor=tk.NW,image=self.schema)

    def afficheLongueur():
        app.Longueur.config(text=Fonctions.Externes.Longueur(HeadClass.calculDistances()))

    def afficheLongueurBody():
        app.LongueurBody.config(text=Fonctions.Externes.LongueurBody(BodyClass.calculDistances()))

    def clearAllCanvas(self):
        HeadClass.id_polygons=[]
        HeadClass.pointsFish=[]
        HeadClass.pointsEchelle=[]
        HeadClass.distances_check=[0 for _ in range(20)]
        self.Longueur.config(text="")
        BodyClass.id_polygons=[]
        BodyClass.pointsFish=[]
        BodyClass.pointsEchelle=[]
        BodyClass.distances_check=[0 for _ in range(20)]
        self.LongueurBody.config(text="")
        self.avertissement.config(text="")
        self.sexPrediction.config(text="")
        self.canvas.delete('all')
        self.canvas1.delete('all')


    def importImage(self):
        nbPointNonDetectes = 0

        print("### Initialisation ###")
        tete,echelle10mm,echelle3mm = Placement.Points.randomPointsBis()
        pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19 = tete
        self.clearAllCanvas()
        pathok = Fonctions.Externes.openfn()
        Interface.listeImages = pathok
        print(pathok)
        ImagePIL = Image.open(pathok[app.numImageActuelle])

        ''' Resize pour le corps '''
        print("\n### Traitement du corps ###")
        corpsStandard,newPIL_image,left = Placement.Points.ImageCorps(ImagePIL)
        BodyFish(self.canvas1,newPIL_image,(1300,975))
        self.canvas1.move(BodyFish.poisson,-(left[0]-50),-(left[1]-280))
        self.canvas1.update()
        print("### OK ###")

        ''' Resize pour la tête '''
        print("\n### Traitement de la tête 1/3 ### ")
        PIL_image_big,CV2_image_big,left1 = Placement.Points.ImageTete(pathok,app.numImageActuelle)
        HeadFish(self.canvas,PIL_image_big,CV2_image_big,(3500,2625))
        self.canvas.update()
        print("### OK ###")

        print("\n### Alignement des points sur le corps'  ###")
        corpsStandard = [[x[0]-(left[0]-50),x[1]-(left[1]-280)] for x in corpsStandard]
        echelle10mm = [[x[0]-(left[0]-250),x[1]-(left[1]-350)] for x in echelle10mm]
        BodyClass(self.canvas1, echelle10mm,'red')
        BodyClass(self.canvas1,corpsStandard,'cyan')
        self.canvas1.update()
        print("### OK ###")

        ''' Initialisation des points 3 et 19 par détection auto '''
        print("\n### Calcul des points 3 et 19 ###")
        # try:
        #     [pt3,pt19]=Placement.Points.points3_19(CV2_image_big)
        #     pt3 = [pt3[0],pt3[1]]
        #     pt19 = [pt19[0],pt19[1]]
        # except:
        #     print("Impossible de déterminer les points 3 et 19")
        #     nbPointNonDetectes+=2
        [pt3,pt19]=Placement.Points.points3_19(CV2_image_big)
        pt3 = [pt3[0],pt3[1]]
        pt19 = [pt19[0],pt19[1]]
        print("### OK ###")

        '''Initialisation du point 9 par détection auto '''
        print("\n### Calcul du point 9 ###")
        _,c = Placement.Points.contoursCorpsBig(CV2_image_big)
        print(CV2_image_big.shape)
        try:
            pt9=Placement.Points.point9(c,pt19)
            pt9 = [pt9[0],pt9[1]]
            print("pt9")
            print(pt9)
            # print("left")
            # print(left)
        except:
            print("Impossible de déterminer le point 9")
            nbPointNonDetectes+=1
        print("### OK ###")

        '''Initialisation du point 15 et 13 par détection auto '''
        print("\n### Calcul des points 9 ###")
        try:
            pt15,pt13=Placement_Points.points15_13(CV2_image_big)
            pt15 = [pt15[0],pt15[1]]
            pt13 = [pt13[0],pt13[1]]
        except:
            print("Impossible de déterminer les points 15 et 13")
            pt13 = [1288, 1228]
            pt15 = [1308, 1098]
            nbPointNonDetectes+=2
        print("### OK ###")


        '''Initialisation des points 5 et 7 par détection auto '''
        print("\n### Calcul des points 5 et 7  ###")
        try:
            pt7,pt5 = Placement.Points.points5_7(CV2_image_big,pt9,left1)
            pt5 = [pt5[0],pt5[1]]
            pt7 = [pt7[0],pt7[1]]
        except:
            print("Impossible de détecter les points 5 et 7")
            nbPointNonDetectes+=2

        """Initialisation des points 11 et 17 par détection auto """
        try:
            pt17,pt11 = Placement.Points.points11_17(CV2_image_big,pt13,pt15)
        except:
            print("Impossible de détecter les points 11 et 17")
            nbPointNonDetectes+=2

        tete = Placement.Points.centerPoints([pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19],HeadFish.centreOeil)

        print("\n### Placement des points de la tête ###")
        HeadClass(self.canvas, tete,'#ff00f2')
        HeadClass(self.canvas,echelle3mm,'red')
        print("### OK ###")
        app.avertissement.config(text=str(13-nbPointNonDetectes)+" points détectés / 13 ")


    def affichePrediction():
        choix,couleur = Classification.Prediction.predict()
        app.sexPrediction.config(text="")
        app.sexPrediction.config(text=choix+" avec p=0.5",font=("Purisa",16),fg=couleur)

    def nextImage(self):
        nbPointNonDetectes = 0
        app.numImageActuelle+=1
        self.clearAllCanvas()
        tete,echelle10mm,echelle3mm = Placement.Points.randomPointsBis()
        ImagePIL = Image.open(Interface.listeImages[app.numImageActuelle])

        ''' Resize pour le corps '''
        print("\n### Traitement du corps ###")
        corpsStandard,newPIL_image,left = Placement.Points.ImageCorps(ImagePIL)
        BodyFish(self.canvas1,newPIL_image,(1300,975))
        self.canvas1.move(BodyFish.poisson,-(left[0]-50),-(left[1]-280))
        self.canvas1.update()
        print("### OK ###")

        ''' Resize pour la tête '''
        print("\n### Traitement de la tête 1/3 ### ")
        PIL_image_big,CV2_image_big,left1 = Placement.Points.ImageTete(Interface.listeImages,app.numImageActuelle)
        HeadFish(self.canvas,PIL_image_big,CV2_image_big,(3500,2625))
        self.canvas.update()
        print("### OK ###")

        print("\n### Alignement des points sur le corps'  ###")
        corpsStandard = [[x[0]-(left[0]-50),x[1]-(left[1]-280)] for x in corpsStandard]
        echelle10mm = [[x[0]-(left[0]-250),x[1]-(left[1]-350)] for x in echelle10mm]
        BodyClass(self.canvas1, echelle10mm,'red')
        BodyClass(self.canvas1,corpsStandard,'cyan')
        self.canvas1.update()
        print("### OK ###")

        ''' Initialisation des points 3 et 19 par détection auto '''
        print("\n### Calcul des points 3 et 19 ###")
        # try:
        #     [pt3,pt19]=Placement.Points.points3_19(CV2_image_big)
        #     pt3 = [pt3[0],pt3[1]]
        #     pt19 = [pt19[0],pt19[1]]
        # except:
        #     print("Impossible de déterminer les points 3 et 19")
        #     nbPointNonDetectes+=2
        [pt3,pt19]=Placement.Points.points3_19(CV2_image_big)
        pt3 = [pt3[0],pt3[1]]
        pt19 = [pt19[0],pt19[1]]
        print("### OK ###")

        '''Initialisation du point 9 par détection auto '''
        print("\n### Calcul du point 9 ###")
        _,c = Placement.Points.contoursCorpsBig(CV2_image_big)
        print(CV2_image_big.shape)
        try:
            pt9=Placement.Points.point9(c,pt19)
            pt9 = [pt9[0],pt9[1]]
            print("pt9")
            print(pt9)
            # print("left")
            # print(left)
        except:
            print("Impossible de déterminer le point 9")
            nbPointNonDetectes+=1
        print("### OK ###")

        '''Initialisation du point 15 et 13 par détection auto '''
        print("\n### Calcul des points 9 ###")
        try:
            pt15,pt13=Placement_Points.points15_13(CV2_image_big)
            pt15 = [pt15[0],pt15[1]]
            pt13 = [pt13[0],pt13[1]]
        except:
            print("Impossible de déterminer les points 15 et 13")
            pt13 = [1288, 1228]
            pt15 = [1308, 1098]
            nbPointNonDetectes+=2
        print("### OK ###")


        '''Initialisation des points 5 et 7 par détection auto '''
        print("\n### Calcul des points 5 et 7  ###")
        try:
            pt7,pt5 = Placement.Points.points5_7(CV2_image_big,pt9,left1)
            pt5 = [pt5[0],pt5[1]]
            pt7 = [pt7[0],pt7[1]]
        except:
            print("Impossible de détecter les points 5 et 7")
            nbPointNonDetectes+=2

        """Initialisation des points 11 et 17 par détection auto """
        try:
            pt17,pt11 = Placement.Points.points11_17(CV2_image_big,pt13,pt15)
        except:
            print("Impossible de détecter les points 11 et 17")
            nbPointNonDetectes+=2

        tete = Placement.Points.centerPoints([pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19],HeadFish.centreOeil)

        print("\n### Placement des points de la tête ###")
        HeadClass(self.canvas, tete,'#ff00f2')
        HeadClass(self.canvas,echelle3mm,'red')
        print("### OK ###")
        app.avertissement.config(text=str(13-nbPointNonDetectes)+" points détectés / 13 ")


    # Main


app = Interface()
app.mainloop()
#
# import inspect
# src_file_path = inspect.getfile(lambda: None)
# print(inspect.stack()[0][1])



''' Documentation

generate diagramm class

in powershell : Pyreverse -o dot Interface_Sexage.py
in pyzo : render('dot','png','C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\classes.dot')

file:///C:/Users/MASSON/Downloads/Admixture_mapping_of_male_nuptial_color_and_body_s.pdf
https://condor.depaul.edu/~waguirre/Aguirre_et_al_08_RS.pdf
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3183875/
file:///C:/Users/MASSON/Downloads/KitanoetalCopeia.pdf
https://jeb.biologists.org/content/216/5/835
file:///C:/Users/MASSON/Downloads/Environ.Biol.Fish.2005.pdf
file:///C:/Users/MASSON/Downloads/_journals_njz_28_3-4_article-p524_5-preview.pdf
https://www.researchgate.net/figure/Morphological-characters-measured-from-the-left-side-of-each-fish-1-fork-length-2-jaw_fig2_233726301
https://www.researchgate.net/figure/Morphometric-analysis-of-body-shape-and-its-association-with-colour-a-The-20-numbered_fig3_225288970
https://journals.plos.org/plosone/article/figure?id=10.1371/journal.pone.0021060.g001
https://docs.google.com/presentation/d/1HZcpJerbqx9Z-llRNlb6E30YXBvOnMuJ/edit#slide=id.p12
'''

