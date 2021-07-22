''' Module pour l'interface GUI '''

# Pour assurer le bon fonctionnement
import sys,inspect
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)

# Import des bibliothèques (s'assurer qu'elles soient installées)
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import math,os,cv2,webbrowser
import XY_tools,IA_sexage,GUI_little,GUI_update
import IA_morph as ML
from datetime import datetime
import numpy as np
import xgboost as xgb
import pandas as pd
## Classes pour afficher les points sur les images

class Polygone():
    # classe polygone pour les 2 images principales
    def __init__(self, canvas, points,color):
        """!
        Constructeur du polygone de la tête
        @param canvas tk.Canvas : cadre de l'image
        @param points list : liste des points du polygone
        @param color String : couleur du polygone
        """
        self.previous_x = self.previous_y = self.selected = self.x = None
        self.points = points
        self.id_polygons = []
        self.distances_all = []
        self.pointsEchelle = []
        listenode = [i for i in range(1,13)]
        num = 0
        if points!=None:
            if color=='red':outline='red'
            else: outline=''
            self.polygon = canvas.create_polygon(self.points,fill='',outline=outline,smooth=0,width=2,dash=(1,))
            self.id_polygons.append(self.polygon)
            canvas.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas))
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                label = canvas.create_text((x+15, y+6),text=str(listenode[num]),font=("Purisa", 12),fill='purple')
                num+=1
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas))
                canvas.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas))

        self.update_points(canvas)
        if(len(self.pointsEchelle)>0):
             Interface.afficheLongueur()

    def update_points(self,canvas):
        """!
        Methode de mise à jour de la position des points
        @param canvas tk.Canvas : cadre de l'image
        """
        for id in self.id_polygons:
            liste = canvas.coords(id)
            if(len(liste)==20):self.pointsFish=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

    def on_press_tag(self, event, number, tag):
        """!
        Methode pour determiner l'item relaché
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = tag
        self.previous_x = event.x
        self.previous_y = event.y

    def on_release_tag(self, event, number, tag,canvas):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = self.previous_x = self.previous_y = None
        self.update_points(canvas)

    def on_move_node(self, event, number,canvas):
        """!
        Methode pour deplacer un noeud du graphe
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            canvas.move(self.selected, dx, dy)
            canvas.move(self.nonodes[self.nodes.index(self.selected)],dx,dy)
            self.points[number][0] += dx
            self.points[number][1] += dy
            coords = sum(self.points, [])
            canvas.coords(self.polygon, coords)
            self.previous_x = event.x
            self.previous_y = event.y
        self.update_points(canvas)
        Interface.afficheLongueur()

    def calculDistances(self):
        """!
        Methode pour calculer certaines distances caractéristiques
        """
        print("PointsEchelle")
        print(self.pointsEchelle)
        print("points")
        print(self.points)
        # self.distances_check = XY_tools.Externes.calculDistances(self.pointsEchelle,self.points)
        self.distances_all = XY_tools.Externes.calculDistancesv2(self.pointsEchelle, self.points)
        return self.distances_all


class ScaleClass():
    """Variables globales pour export
    id_polygons : liste des id des polygons (la tete et l'echelle)
    pointsFish : liste des points de la tête [(x1,y1),(x2,y2)...]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    pointsEchelle : liste des points de l'echelle [(x1,y1),(x2,y2)]
    """
    id_polygons = []
    pointsFish = []
    distances_check = []
    distances_all = []
    pointsEchelle = []
    def __init__(self, canvas2, points,color):
        """!
        Constructeur du polygone de la tête
        @param canvas2 tk.Canvas : cadre de l'image
        @param points list : liste des points du polygone
        @param color String : couleur du polygone
        """
        self.previous_x = self.previous_y = self.selected = self.x = None
        self.points = points
        listenode = [i for i in range(1,13)]
        num = 0
        if points!=None:
            if color=='red':outline='white'
            else: outline=''
            self.polygon = canvas2.create_polygon(self.points,fill='',outline=outline,smooth=0,width=2,dash=(1,))
            Interface.PolygoneA.id_polygons.append(self.polygon)
            canvas2.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas2.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas2))
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas2.create_rectangle((x-3, y-3, x+3, y+3), fill='#f0f0f0',outline="#f0f0f0")
                label = canvas2.create_text((x+15, y+6),text=str(listenode[num]),font=("Purisa", 12),fill='#f0f0f0')
                num+=1
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas2.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas2.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas2))
                canvas2.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas2))
        ScaleClass.update_points(canvas2)

    def update_points(canvas2):
        """!
        Methode de mise à jour de la position des points
        @param canvas2 tk.Canvas : cadre de l'image
        """
        for id in Interface.PolygoneA.id_polygons:
            liste = canvas2.coords(id)
            if(len(canvas2.coords(id))==4):ScaleClass.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

    def on_press_tag(self, event, number, tag):
        """!
        Methode pour determiner l'item relaché
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = tag
        self.previous_x = event.x
        self.previous_y = event.y

    def on_release_tag(self, event, number, tag,canvas2):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = self.previous_x = self.previous_y = None
        ScaleClass.update_points(canvas2)

    def on_move_node(self, event, number,canvas2):
        """!
        Methode pour deplacer un noeud du graphe
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            canvas2.move(self.selected, dx, dy)
            canvas2.move(self.nonodes[self.nodes.index(self.selected)],dx,dy)
            self.points[number][0] += dx
            self.points[number][1] += dy
            coords = sum(self.points, [])
            canvas2.coords(self.polygon, coords)
            self.previous_x = event.x
            self.previous_y = event.y
            px50mm = XY_tools.Externes.euclide(Interface.canvasEchelle.coords(Interface.PolygoneC.nodes[0]),Interface.canvasEchelle.coords(Interface.PolygoneC.nodes[1]))

            if self.selected==5:
                Interface.canvasCorps.move(9,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(Interface.PolygoneB.nonodes[Interface.PolygoneB.nodes.index(9)],dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.PolygoneB.points[3][0] += dx
                Interface.PolygoneB.points[3][1] += dy
                coordes = sum(Interface.PolygoneB.points, [])
                Interface.canvasCorps.coords(Interface.PolygoneB.polygon, coordes)
                Interface.canvasCorps.update()
                Interface.PolygoneB.previous_x = event.x
                Interface.PolygoneB.previous_y = event.y
                Interface.PolygoneB.update_points(Interface.canvasCorps)
                Interface.afficheLongueur()
                Interface.allDist(Interface.lenBody)

            if self.selected==3:
                Interface.canvasCorps.move(7,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(Interface.PolygoneB.nonodes[Interface.PolygoneB.nodes.index(7)],dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.PolygoneB.points[2][0] += dx
                Interface.PolygoneB.points[2][1] += dy
                coordes = sum(Interface.PolygoneB.points, [])
                Interface.canvasCorps.coords(Interface.PolygoneB.polygon, coordes)
                Interface.canvasCorps.update()
                Interface.PolygoneB.previous_x = event.x
                Interface.PolygoneB.previous_y = event.y
                Interface.PolygoneB.update_points(Interface.canvasCorps)
                Interface.afficheLongueur()
                Interface.allDist(Interface.lenBody)

            Interface.allDist(Interface.lenBody)
        ScaleClass.update_points(canvas2)



class ScaleClassBody():
    """Variables globales pour export
    id_polygons : liste des id des polygons (la tete et l'echelle)
    pointsFish : liste des points de la tête [(x1,y1),(x2,y2)...]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    pointsEchelle : liste des points de l'echelle [(x1,y1),(x2,y2)]
    """
    id_polygons = []
    pointsFish = []
    distances_check = []
    distances_all = []
    pointsEchelle = []
    def __init__(self, canvas3, points,color):
        """!
        Constructeur du polygone de la tête
        @param canvas2 tk.Canvas : cadre de l'image
        @param points list : liste des points du polygone
        @param color String : couleur du polygone
        """
        self.previous_x = self.previous_y = self.selected = self.x = None
        self.points = points
        listenode = [i for i in range(1,13)]
        num = 0
        if points!=None:
            if color=='red':outline='white'
            else: outline=''
            self.polygon = canvas3.create_polygon(self.points,fill='',outline=outline,smooth=0,width=2,dash=(1,))
            Interface.PolygoneA.id_polygons.append(self.polygon)
            canvas3.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas3.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas3))
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas3.create_rectangle((x-3, y-3, x+3, y+3), fill='#f0f0f0',outline="#f0f0f0")
                label = canvas3.create_text((x+15, y+6),text=str(listenode[num]),font=("Purisa", 12),fill='#f0f0f0')
                num+=1
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas3.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas3.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas3))
                canvas3.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas3))

        ScaleClassBody.update_points(canvas3)



    def update_points(canvas3):
        """!
        Methode de mise à jour de la position des points
        @param canvas2 tk.Canvas : cadre de l'image
        """
        for id in Interface.PolygoneA.id_polygons:
            liste = canvas3.coords(id)
            if(len(canvas3.coords(id))==4):ScaleClassBody.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
    def on_press_tag(self, event, number, tag):
        """!
        Methode pour determiner l'item relaché
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = tag
        self.previous_x = event.x
        self.previous_y = event.y

    def on_release_tag(self, event, number, tag,canvas3):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = self.previous_x = self.previous_y = None
        ScaleClassBody.update_points(canvas3)

    def on_move_node(self, event, number,canvas3):
        """!
        Methode pour deplacer un noeud du graphe
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            canvas3.move(self.selected, dx, dy)
            canvas3.move(self.nonodes[self.nodes.index(self.selected)],dx,dy)
            self.points[number][0] += dx
            self.points[number][1] += dy
            coords = sum(self.points, [])
            canvas3.coords(self.polygon, coords)
            self.previous_x = event.x
            self.previous_y = event.y

            if self.selected==5:
                Interface.canvasCorps.move(5,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(Interface.PolygoneB.nonodes[Interface.PolygoneB.nodes.index(5)],dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.PolygoneB.points[1][0] += dx
                Interface.PolygoneB.points[1][1] += dy
                coordes = sum(Interface.PolygoneB.points, [])
                Interface.canvasCorps.coords(Interface.PolygoneB.polygon, coordes)
                Interface.canvasCorps.update()
                Interface.PolygoneB.previous_x = event.x
                Interface.PolygoneB.previous_y = event.y
                Interface.PolygoneB.update_points(Interface.canvasCorps)
                # Interface.afficheLongueurBody()

            if self.selected==3:
                Interface.canvasCorps.move(3,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(Interface.PolygoneB.nonodes[Interface.PolygoneB.nodes.index(3)],dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.PolygoneB.points[0][0] += dx
                Interface.PolygoneB.points[0][1] += dy
                coordes = sum(Interface.PolygoneB.points, [])
                Interface.canvasCorps.coords(Interface.PolygoneB.polygon, coordes)
                Interface.canvasCorps.update()
                Interface.PolygoneB.previous_x = event.x
                Interface.PolygoneB.previous_y = event.y
                Interface.PolygoneB.update_points(Interface.canvasCorps)
                # Interface.afficheLongueurBody()
        # Interface.afficheLongueurBody()
        ScaleClassBody.update_points(canvas3)

## Canvas pour les images

class HeadFish():
    poisson = None
    centreOeil=None
    CV2_image_big = None
    img = None
    def __init__(self, canvas,PIL_image,CV2_image,size):
        HeadFish.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        HeadFish.poisson = canvas.create_image(0, 0, anchor=tk.NW,image=HeadFish.img)
        HeadFish.CV2_image_big = CV2_image
        canvas.move(HeadFish.poisson,-(HeadFish.oeilXY[0]-200),-(HeadFish.oeilXY[1]-200))

class BodyFish():
    poisson = None
    img = None
    def __init__(self, canvas1,PIL_image,size):
        BodyFish.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        BodyFish.poisson = canvas1.create_image(0, 0, anchor=tk.NW, image=BodyFish.img)
        canvas1.move(BodyFish.poisson, -(BodyFish.left[0]-50),-(BodyFish.left[1]-150))

class ScaleFish():
    poisson = None
    img = None
    def __init__(self, canvas2,PIL_image,size):
        ScaleFish.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        ScaleFish.poisson = canvas2.create_image(0, 0, anchor=tk.NW, image=ScaleFish.img)
        Interface.canvasEchelle.itemconfig(ScaleFish.poisson,state='normal')
        canvas2.move(ScaleFish.poisson,-(ScaleFish.left[0]-25),-(ScaleFish.left[1]-50))

class ScaleFishBody():
    poisson = None
    img = None
    def __init__(self, canvas3,PIL_image,size):
        ScaleFishBody.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        ScaleFishBody.poisson = canvas3.create_image(0, 0, anchor=tk.NW, image=ScaleFishBody.img)
        Interface.canvasEchelle2.itemconfig(ScaleFishBody.poisson,state='hidden')
        Interface.canvasEchelle2.move(ScaleFishBody.poisson,-(ScaleFishBody.left[0]-25),-(ScaleFishBody.left[1]-160))


## Import du modèle de détection
class ModelPoints():
    """!
        Classe de préparation du modèle Regression Trees pour la détection des
        points par Machine Learning
    """

    def __init__(self,aa,bb):
        """!
            Constructeur de la classe
                Example : a = ModelPoints()
        """
        ModelPoints.pointsML = ML.ML_pointage(aa,bb)

    def predict(self,path_newimage,predictor_path,predictor_name):
        ModelPoints.pointsML.predict(path_newimage,predictor_path,predictor_name)

## Interface finale

class Interface(tk.Tk):
    sexModele = None
    version = 1.9
    canvasTete = None
    def __init__(self):
        """!
        Constructeur de l'interface
        """
        super().__init__()
        self.listeImages = []
        self.numImageActuelle = 0
        self.add_menu()
        self.add_buttons()
        self.add_labels()
        self.add_canvas()
        self.createlog()
        self.verbose_intro()

    def add_canvas(self):
        ''' Canvas pour la tête '''
        Interface.canvasTete = tk.Canvas(self,bg='#f0f0f0',bd=0,highlightthickness=1, highlightbackground="black")
        Interface.canvasTete.config(width=500, height=370)
        Interface.canvasTete.grid(column=0,row=8)

        ''' Canvas pour le corps '''
        Interface.canvasCorps = tk.Canvas(self,bg='#f0f0f0',highlightthickness=1, highlightbackground="black")
        Interface.canvasCorps.config(width=630, height=370)
        Interface.canvasCorps.grid(column=1,row=8)

        ''' Canvas pour l'échelle '''
        Interface.canvasEchelle = tk.Canvas(self,bg='#f0f0f0')
        Interface.canvasEchelle.config(width=1590, height=200)
        Interface.canvasEchelle.place(relx=0,rely=0.7)

        """Canvas pour logo"""
        pathLogo = XY_tools.Externes.resource_path("logo2.png")
        self.canvasLogo2 = tk.Canvas(self,bg='#f0f0f0')
        self.canvasLogo2.config(width=157,height=84)
        self.canvasLogo2.place(x=0,y=0)
        self.imgLogo2 = ImageTk.PhotoImage(Image.open(pathLogo).resize((157,84)))
        self.canvasLogo2.create_image(0, 0, anchor=tk.NW,image=self.imgLogo2)

        """Canvas pour logo"""
        Interface.canvasEchelle2 = tk.Canvas(self,bg='#f0f0f0')
        Interface.canvasEchelle2.config(width=1590,height=240)
        Interface.canvasEchelle2.place(relx=0,rely=0.66)

        ''' Canvas pour le schema '''
        pathSchema = XY_tools.Externes.resource_path("schema.png")
        self.canvasSchema = tk.Canvas(self,bg='#f0f0f0')
        self.canvasSchema.config(width = 288,height=192)
        self.canvasSchema.place(x=1250,y=0)
        self.imgSchema = ImageTk.PhotoImage(Image.open(pathSchema).resize((288,192)))
        self.canvasSchema.create_image(0,0,anchor=tk.NW,image=self.imgSchema)


    def add_buttons(self):


        # self.boutonImport = tk.Button(self,text = "Import images",command = self.importImage,fg='purple')
        self.boutonImport = ttk.Button(self,text = "Importer les images",command = self.importImage)
        try:
            self.logo = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_import.png'))
        except:
            self.logo = tk.PhotoImage(file = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\images\logo_import.png')
        self.boutonImport.config(image=self.logo, compound=tk.LEFT)
        self.small_logo = self.logo.subsample(7,7)
        self.boutonImport.config(image = self.small_logo)
        self.boutonImport.place(relx=0.20,rely=0.12)
        self.boutonImport.bind('<Control-o>',self.importImage)


        # self.boutonPredict = tk.Button(self,text = "Predict",command = self.Model_Sexage,fg='purple')
        self.boutonPredict = ttk.Button(self,text = "Predire",command = self.Model_Sexage)
        try:
            self.logo2 = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_predict.png'))
        except:
            self.logo2 = tk.PhotoImage(file = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\images\logo_predict.png')
        self.boutonPredict.config(image=self.logo2, compound=tk.LEFT)
        self.small_logo2 = self.logo2.subsample(15,15)
        self.boutonPredict.config(image = self.small_logo2)
        self.boutonPredict.place(relx=0.31,rely=0.12)
        self.boutonPredict.bind('<Control-p>',self.Model_Sexage)



        # self.boutonPrevious = tk.Button(self,text='<--',fg='red',command = self.previousImage)
        self.boutonPrevious = ttk.Button(self,text="",command = self.previousImage)
        try:
            self.logo3 = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_left_arrow.png'))
        except:
            self.logo3 = tk.PhotoImage(file = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\images\logo_left_arrow.png')
        self.boutonPrevious.config(image=self.logo3, compound=tk.LEFT)
        self.small_logo3 = self.logo3.subsample(15,15)
        self.boutonPrevious.config(image = self.small_logo3)
        self.boutonPrevious.place(relx=0.40,rely=0.12)


        # self.boutonNext = tk.Button(self,text='-->',fg='red',command = self.nextImage)
        self.boutonNext = ttk.Button(self,text="",command = self.nextImage)
        try:
            self.logo4 = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_right_arrow.png'))
        except:
            self.logo4 = tk.PhotoImage(file = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\images\logo_right_arrow.png')
        self.boutonNext.config(image=self.logo4, compound=tk.LEFT)
        self.small_logo4 = self.logo4.subsample(15,15)
        self.boutonNext.config(image = self.small_logo4)
        self.boutonNext.place(relx=0.47,rely=0.12)

        ttk.Button(self,text="1) Réglage corps", command = self.afficheCorps).place(relx = 0.75,rely=0.5)
        ttk.Button(self,text="2) Réglage échelle",command = self.hideCorps).place(relx=0.75,rely=0.55)
        ttk.Button(self,text="3) Cacher l'image",command = self.hideScale).place(relx = 0.75,rely=0.6)

    def add_labels(self):
        ''' Label Intro de presentation'''
        # tk.Label(self, text = 'PREDICTION',font=("Purisa",12,"bold"),fg='purple').place(relx=0.25,rely=0.08)
        tk.Label(self,text=" ",font=("Purisa",12,"bold")).grid(ipadx=2)
        tk.Label(self,text=" Procédure de sexage de l'épinoche à trois épines \n",font=("Andalus",16,"bold")).place(relx=0.3,rely=0.01)
        tk.Label(self,text="\n \n \n \n ").grid(column=0,row=1)

        self.labelSex = tk.Label(self,text="")
        self.labelSex.place(relx=0.55,rely=0.13)
        tk.Label(self,text=" ").grid(column=0,row=3)

        self.labelNumImage = tk.Label(self,text="",font=("Purisa",11),fg='gray')
        self.labelNumImage.place(relx=0.05,rely=0.975)
        self.labelNomImage = tk.Label(self,text="",font=("Purisa",11),fg='gray')
        self.labelNomImage.place(relx=0.1,rely=0.975)
        tk.Label(self,text="\n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=2,row=4)

    def add_menu(self):
        ''' Fenetre et menu'''
        self.state('zoomed')
        self.title("Sex Determination for Three Spined Stickleback")
        menubar = tk.Menu(self)
        menuFichier = tk.Menu(menubar,tearoff=0)
        menuFichier.add_command(label="Importer", command=self.importImage,accelerator="(Ctrl+O)")
        self.bind_all("<Control-o>",lambda e : self.importImage())
        menuFichier.add_separator()
        menuFichier.add_command(label="Quitter", command=self.destroy,accelerator="(Ctrl+Q)")
        self.bind_all("<Control-q>",lambda e : self.destroy())
        menubar.add_cascade(label="Fichier", menu=menuFichier)

        menuOutils = tk.Menu(menubar,tearoff=0)
        menuOutils.add_command(label="Prédire le sexe",command=self.Model_Sexage,accelerator="(Ctrl+P)")
        self.bind_all("<Control-p>",lambda e : self.Model_Sexage())
        menuOutils.add_command(label="Image suivante",command=self.nextImage,accelerator="(Ctrl+Entrée)")
        self.bind_all("<Control-Return>",lambda e : self.nextImage())
        menuOutils.add_command(label="Image précédente",command=self.previousImage,accelerator="(Ctrl+Backspace)")
        self.bind_all("<Control-BackSpace>",lambda e : self.previousImage())

        menuOutils.add_separator()
        menuOutils.add_command(label="Ouvrir base de données",command=self.openDataBase,accelerator="(Ctrl+H)")
        self.bind_all("<Control-h>",lambda e : self.openDataBase())
        menubar.add_cascade(label="Outils",menu=menuOutils)

        menuModeles = tk.Menu(menubar,tearoff=0)
        menuModeles.add_command(label="Prépare MaJ Pointage",command=Interface.improveLandmarksModel)
        menuModeles.add_command(label="MaJ Pointage 🔒",command=self.updatePointModel)
        menuModeles.add_command(label="MaJ Sexage 🔒",command=self.updatePointModel1)
        menubar.add_cascade(label="Modèles",menu=menuModeles)

        menuAffichage = tk.Menu(menubar,tearoff=0)
        menuAffichage.add_command(label="Vue pour petit écran",command=self.changeView,accelerator="(Ctrl+N)")
        self.bind_all("<Control-n>",lambda e : self.changeView())
        menubar.add_cascade(label="Affichage",menu=menuAffichage)

        menuAide = tk.Menu(menubar, tearoff=0)
        menuAide.add_command(label="A propos", command=self.help,accelerator="(Ctrl+I)")
        self.bind_all("<Control-i>",lambda e : self.help())
        menuAide.add_command(label="Version",command=Interface.getVersion)
        menubar.add_cascade(label="Aide", menu=menuAide)
        self.config(menu=menubar)

    def createlog(self):
        if not os.path.exists(os.getcwd()+"/log"):
            os.mkdir(os.getcwd()+"/log")
            pathname = os.getcwd()+"/log/"
            date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = date+"_"+"rapport"
            filename2 = date+"_"+"resultats"
            self.finalname = pathname+filename+".txt"
            self.finalname2 = pathname+filename2+".csv"
            f = open(self.finalname,"w+")
            f.close()

        if os.path.exists(os.getcwd()+"/log"):
            pathname = os.getcwd()+"/log/"
            date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = date+"_"+"rapport"
            filename2 = date+"_"+"resultats"
            self.finalname = pathname+filename+".txt"
            self.finalname2 = pathname+filename2+".csv"
            f = open(self.finalname,"w+")
            f.close()
        self.data_result = pd.DataFrame()
        self.NomImages = []
        self.data_distances = []
        self.LS = []
        self.sexe = []
        self.NumImages = []

    def verbose_intro(self):
        message = "Rapport généré le "+datetime.now().strftime("%d/%m/%Y")+" à "+datetime.now().strftime("%H:%M:%S")+"\n\n"
        message += "# Morphométrie Epinoche Ineris v"+str(Interface.version)+"\n"
        message += "- Développé par Ralph MASSON pour l'unité ESMI \n"
        message += "- Contact : ralph.masson@gmail.com \n\n"
        message += "# Langage et bibliothèques utilisés : \n"
        message += "- Python 3.8.6 \n"
        message += "- sklearn 0.23.2 - numpy 1.18.5 - scipy 1.5.2 - dlib 19.22.0 - xgboost 1.4.2 \n\n"
        message += "# ML_morph\n"
        message += "\t - Algorithme utilisé : Regression trees (gradient boosting) \n"
        message += "\t - Performances : erreur de placement moyenne de 4 pixels (0.25% de la longueur standard) \n\n"
        message += "# ML_gender\n"
        message += "\t - Algorithmes utilisés : Gradient Boosting, SVM, XGBoost (consensus) \n"
        message += "\t - Performances : 100% de bonne classification (10% d'indéterminé en moyenne) par consensus stricte de 3 modèles \n"

        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_photo(self):
        message = "\n# Photos importées pour la prédiction :\n"
        for x in self.listeImages:
            message += "\t - "+x+"\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()
    def verbose_points(self,listepoints):
        message = XY_tools.Externes.verbose_points(listepoints,self.listeImages, self.numImageActuelle)
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_distances(self,df_distance):
        message = "\t Distances : "+str(list(df_distance.values[0]))[1:-1]
        message += "\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()



    def verbose_sexe(self,text,proba):
        message = "\t Sexe : "+text+"\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_conclusion(self):
        message = "\nFIN \n"
        message += datetime.now().strftime("%d/%m/%Y")+" à "+datetime.now().strftime("%H:%M:%S")+"\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def Model_Tete(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_head.dat')
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_head.dat")
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\predictor_head.dat'
            a = ModelPoints(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\',"")
            a.predict(pathimage,pypath2+"\models\\","predictor_head.dat")
            listepoints = ML.ML_pointage.xmltolistY(pypath2+"\models\\"+"output.xml",0)

        self.verbose_points(listepoints)
        return listepoints[0]

    def Model_Echelle(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_scale2.dat')
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_scale2.dat")
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\predictor_scale2.dat'
            a = ModelPoints(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\',"")
            a.predict(pathimage,pypath2+"\models\\","predictor_scale2.dat")
            listepoints = ML.ML_pointage.xmltolistY(pypath2+"\models\\"+"output.xml",0)

        return listepoints[0]


    def Model_Longueur(self,pathimage):
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_LS.dat')
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_LS.dat")
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\predictor_LS.dat'
            a = ModelPoints(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\',"")
            a.predict(pathimage,pypath2+"\models\\","predictor_LS.dat")
            listepoints = ML.ML_pointage.xmltolistY(pypath2+"\models\\"+"output.xml",0)

        return listepoints[0]


    def Model_Sexage(self):

        try:
            Interface.lenBody = XY_tools.Externes.euclide(Interface.canvasEchelle2.coords(Interface.PolygoneD.nodes[0]),Interface.canvasEchelle2.coords(Interface.PolygoneD.nodes[1]))
        except:
            pass
        Interface.allDist(Interface.lenBody)
        text,ae,proba = IA_sexage.Prediction.load_models(Interface.modeleDistances)

        self.verbose_distances(ae)
        self.verbose_sexe(text,proba)

        app.labelSex.config(text = text)
        nomImage = "".join(self.listeImages[self.numImageActuelle].split("/")[-1])
        self.NomImages.append(nomImage)
        self.NumImages.append(self.numImageActuelle+1)
        self.LS.append(list(ae.values[0])[0])
        self.sexe.append(text.split(">")[-1])

        if(self.numImageActuelle==len(self.listeImages)-1):

            try:
                self.verbose_conclusion()
                self.data_result['ID'] = self.NumImages
                self.data_result['Nom'] = self.NomImages
                self.data_result['LS'] = self.LS
                self.data_result['Sexe'] = self.sexe
                self.data_result = self.data_result.drop_duplicates()
                self.data_result.to_csv(self.finalname2,index=False,sep=";",encoding="UTF-8")

            except:
                pass

    def afficheScale(self):
        Interface.canvasEchelle.itemconfig(ScaleFish.poisson,state='normal')

    def hideScale(self):
        Interface.canvasEchelle.itemconfig(ScaleFish.poisson,state='hidden')

    def afficheCorps(self):
        Interface.canvasEchelle2.itemconfig(ScaleFishBody.poisson,state='normal')

    def hideCorps(self):
        Interface.canvasEchelle2.itemconfig(ScaleFishBody.poisson,state='hidden')
        Interface.lenBody = XY_tools.Externes.euclide(Interface.canvasEchelle2.coords(3),Interface.canvasEchelle2.coords(5))
        Interface.canvasEchelle2.destroy()

    def improveLandmarksModel():
        message = "Pour ajouter des données au modèle v1 de placement de points :"
        message += "\n\n1) Ajouter les photos nouvelles dans un dossier tmp"
        message += "\n2) Créer un fichier temp.tps grâce à tpsUtils (build tps)"
        message += "\n3) Créer un fichier v2.tps grâce à tpsUtils (append temp+v1) sans inclure path"
        message += "\n4) Pointer les images avec tpsDig"
        message += "\n5) Sauvegarder (overwrite) v2.tps"
        message += "\n6) Déplacer les images novelles dans le même dossier que les anciennes"

        tk.messagebox.showinfo(title="Informations",message=message)

    def changeView(self):
        GUI_little.Temp.chemin = pypath3
        GUI_little.Temp.ppath2 = pypath2
        self.destroy()
        root = tk.Tk()
        GUI_little.app = GUI_little.Interface(root)
        GUI_little.app.pack(side="top", fill="both", expand=True)
        GUI_little.app.mainloop()

    def updatePointModel(self):
        GUI_update.InterfacePoint()

    def updatePointModel1(self):
        GUI_update.InterfaceGender()

    def afficheLongueur():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs dans l'interface
        """
        Interface.PolygoneA.calculDistances()

    def afficheLongueurBody():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs du corps dans l'interface
        """
        Interface.PolygoneB.calculDistances()

    def clearAllCanvas(self):
        """!
        Méthode permettant de remettre à zero l'interface
        """
        Interface.PolygoneA.id_polygons=[]
        Interface.PolygoneA.pointsFish=[]
        Interface.PolygoneA.pointsEchelle=[]
        Interface.PolygoneA.distances_check=[0 for _ in range(20)]
        Interface.PolygoneB.id_polygons=[]
        Interface.PolygoneB.pointsFish=[]
        Interface.PolygoneB.pointsEchelle=[]
        Interface.PolygoneB.distances_check=[0 for _ in range(20)]
        self.labelSex.config(text="")
        Interface.canvasTete.delete('all')
        Interface.canvasCorps.delete('all')
        Interface.canvasEchelle2.delete('all')
        Interface.canvasEchelle.delete('all')

        ScaleClassBody.pointsEchelle = []
        self.labelNomImage.config(text="")

    def resetListeImages(self):
        """!
        Méthode permettant de remettre à zero les images chargées
        """
        self.listeImages = []
        self.numImageActuelle = 0

    def getVersion():

        try:
            version = XY_tools.Externes.getVersion()
        except:
            version = "-- No internet connection --"

        message = "Dernière version disponible : "+"v"+str(version)
        message += "\nVersion actuelle : "+"v"+str(Interface.version)
        message += "\nCliquez sur OK pour télécharger"

        reponse = tk.messagebox.askyesnocancel(title="Informations",message=message)
        if(reponse):
            Interface.updateVersion()


    def updateVersion():
        """!
        Méthode permettant d'ouvrir le lien github du projet
        """
        webbrowser.open('https://github.com/RalphMasson/MorphoEpinoche/releases/')


    def allDist(lenBody):
        px50mm = XY_tools.Externes.euclide(Interface.canvasEchelle.coords(Interface.PolygoneC.nodes[0]),Interface.canvasEchelle.coords(Interface.PolygoneC.nodes[1]))
        listedistances2 = []
        listedistances2.append(round(lenBody*50/px50mm,5))
        for x in Interface.PolygoneA.distances_all:
            listedistances2.append(x)
        Interface.modeleDistances = listedistances2

    def importImage(self,event=' '):
        """!
        Méthode permettant de charger 1 ou plusieurs images
        """
        self.choice = 0
        self.resetListeImages()
        self.listeImages = XY_tools.Externes.openfn()
        self.verbose_photo()
        self.calculPoints()

    def calculPoints(self):
        """!
        Méthode permettant de calculer les points et de les disposer sur l'image
        """
        path_global = '/'.join(self.listeImages[self.numImageActuelle].split('/')[:-1])
        self.imgActuelle = self.listeImages[self.numImageActuelle]
        app.labelNomImage.config(text=self.imgActuelle)
        app.labelNumImage.config(text=str(self.numImageActuelle+1)+"/"+str(len(self.listeImages)))

        # ScaleFish Model_Echelle
        ScaleFish.left = self.Model_Echelle(self.imgActuelle)[0]
        points_echelle = self.Model_Echelle(self.imgActuelle)
        points_echelle = XY_tools.Externes.centerPoints(points_echelle[0:2],ScaleFish.left,25,50)

        # HeadFish Model_Tete
        points_tete = self.Model_Tete(self.imgActuelle)
        HeadFish.oeilXY = [np.mean(np.array(points_tete).T[0][1:3])]
        HeadFish.oeilXY.append(np.mean(np.array(points_tete).T[1][1:3]))
        points_tete = XY_tools.Externes.centerPoints(points_tete[0:10],HeadFish.oeilXY,200,200)

        # BodyFish Model Longueur + Model_Echelle
        corpsStandard = self.Model_Longueur(self.imgActuelle)
        corpsStandard = [list(np.array(corpsStandard[0])/3),list(np.array(corpsStandard[1])/3)]
        BodyFish.left = corpsStandard[0]
        points_echelle2 = self.Model_Echelle(self.imgActuelle)
        corpsStandard.extend([list(np.array(points_echelle2[0])/3),list(np.array(points_echelle2[1])/3)])
        corpsStandard = XY_tools.Externes.centerPoints(corpsStandard[0:4],BodyFish.left,50,150)

        # ScaleFishBody Model_Longueur
        points_longueur = self.Model_Longueur(self.imgActuelle)
        pt1,pt2 = points_longueur[0],points_longueur[1]
        ScaleFishBody.left = pt1
        points_longueur = XY_tools.Externes.centerPoints([pt1,pt2],ScaleFishBody.left,25,160)

        # Images
        HeadFish(self.canvasTete,Image.open(self.imgActuelle),cv2.imread(self.imgActuelle),(1920,1440))
        BodyFish(Interface.canvasCorps,Image.open(self.imgActuelle),(640,480))
        ScaleFish(Interface.canvasEchelle,Image.open(self.imgActuelle),(1920,1440))
        ScaleFishBody(Interface.canvasEchelle2,Image.open(self.imgActuelle),(1920,1440))

        # Points
        Interface.PolygoneA = Polygone(self.canvasTete,points_tete,'#ff00f2')
        Interface.PolygoneA.pointsEchelle = points_echelle
        Interface.PolygoneA.calculDistances()

        Interface.PolygoneB = Polygone(Interface.canvasCorps,corpsStandard,'cyan')

        Interface.PolygoneC = ScaleClass(Interface.canvasEchelle,points_echelle,'#ffffff')

        Interface.PolygoneD = ScaleClassBody(Interface.canvasEchelle2,points_longueur,'#ffffff')


    def affichePrediction(self):
        """!
        Méthode permettant d'afficher la prédiction du sexe
        """
        choix,couleur,p = IA_sexage.Prediction.predict(None,"","")
        app.labelSex.config(text="")
        app.labelSex.config(text=choix+" avec p="+str(round(p,2)),font=("Purisa",16),fg=couleur)


    def nextImage(self):
        """!
        Méthode permettant de passer à l'image d'après
        """
        if(self.numImageActuelle<len(self.listeImages)):
            self.blockButton(+1)

    def previousImage(self):
        """!
        Méthode permettant de revenir a l'image précédente
        """
        if(self.numImageActuelle>0):
            self.blockButton(-1)

    def blockButton(self,param):
        """!
        Méthode permettant de désactiver temporairement les boutons pour éviter une superposition d'images
        @param param : +1 pour passer à l'image suivante, -1 pour la précédente
        """
        import time
        self.unbind_all("<Control-Return>")
        self.unbind_all("<Control-BackSpace>")
        self.numImageActuelle+=param
        nbPointNonDetectes = 0
        time.sleep(0.3)
        self.boutonPrevious.configure(state=tk.DISABLED)
        self.boutonNext.configure(state=tk.DISABLED)
        self.clearAllCanvas()
        self.calculPoints()
        time.sleep(0.3)
        self.boutonPrevious.configure(state=tk.ACTIVE)
        self.boutonNext.configure(state=tk.ACTIVE)
        self.bind_all("<Control-Return>",lambda e : self.nextImage())
        self.bind_all("<Control-BackSpace>",lambda e : self.previousImage())

    def openDataBase(self):
        """!
        Méthode permettant d'ouvrir le fichier csv s'il existe
        """
        pypath = inspect.getfile(lambda: None)
        pypath = '/'.join(pypath.split('\\')[:-1])
        import subprocess
        if(os.path.exists(pypath3+"/DistancesPourModele.csv")):
            try:
                subprocess.Popen(pypath3+"/DistancesPourModele.csv",shell=True)
            except:
                commande = "start notepad.EXE "
                commande += pypath3+"/DistancesPourModele.csv"
                os.system(commande)

        elif(os.path.exists(os.getcwd()+"\DistancesPourModele.csv")):
            try:
                subprocess.Popen(os.getcwd()+"\DistancesPourModele.csv",shell=True)
            except:
                commande = "start notepad.EXE "
                commande += os.getcwd()+"\DistancesPourModele.csv"
                os.system(commande)

        else:
            message = "La base de données n'a pas été trouvée"
            message += "\n\n1) Vérifier qu'elle est située ici : "
            message += "\n"+pypath3+"/DistancesPourModele.csv"
            test = os.getcwd()
            test2 = inspect.getfile(lambda: None)
            message += "\n"+test
            message += "\n"+'/'.join(test2.split('\\')[:-1])+"/DistancesPourModele.csv"
            message += "\n\n2) Commencer par créer une base de données"
            # message += "\n"+str(len(test))
            # message += "\n"+str(len('/'.join(test2.split('\\')[:-1])))
            tk.messagebox.showwarning(title="Attention", message=message)

    def help(self):
        """!
        Méthode permettant d'afficher des informations
        """
        message = "PROCEDURE DE SEXAGE DE L'EPINOCHE v1.8"
        message += "\n\n- Modèle de placement de points par Machine Learning (learning : 200 individus)"
        message += "\n\n- Modèle de classification Male/Femelle par Machine Learning (learning : 336 individus)"
        message += "\n\n\n Interface développée par R. Masson pour l'INERIS"
        tk.messagebox.showinfo(title="Informations",message=message)


app = Interface()
app.mainloop()