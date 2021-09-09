''' Module pour l'interface GUI '''

# Pour assurer le bon fonctionnement
import sys,inspect
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
print("path2")
print(pypath2)
sys.path.insert(0,pypath1)

pathPython = r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\DEPLOIEMENT_INERIS_2021\\"

# Import des bibliothèques de python (s'assurer qu'elles soient installées si le code est lancé depuis la console)
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import math,os,cv2,webbrowser
from datetime import datetime
import numpy as np
import xgboost as xgb
import pandas as pd

# Import des bibliothèques liées à l'interface
import XY_tools,IA_sexage,GUI_update
import IA_morph as ML


## VERSION NORMALE

''' Les classes Polygone, ScaleClass, ScaleClassBody servent à
gérer l'affichage et le déplacement des points sur l'image. A priori,
il n'est pas nécessaire de vouloir modifier le code de ces classes. '''

class Polygone():
    # classe polygone pour la gestion des points sur les deux images principales
    def __init__(self, canvas, points,color,ligne):
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
            if ligne:
                canvas.create_line(self.points[2][0],self.points[2][1],self.points[3][0],self.points[3][1],fill="green")
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                if not ligne:
                    canvas.tag_bind(node, '<Enter>',   lambda event: self.check_hand_enter(canvas))
                    canvas.tag_bind(node, '<Leave>',   lambda event: self.check_hand_leave(canvas))
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

    def check_hand_enter(self,canvas):
        canvas.config(cursor="hand1")
    def check_hand_leave(self,canvas):
        canvas.config(cursor="")

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
        print(canvas)
        if(int(str(canvas)[-1])==4):
            if self.selected:
                print(self.selected)
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
        print(self.points)
        self.distances_all = XY_tools.Externes.calculDistancesv2(self.pointsEchelle, self.points)
        return self.distances_all

class ScaleClass():
    # classe ScaleClass pour la gestion des points lors de la correction de l'échelle
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
                canvas2.tag_bind(node, '<Enter>',   lambda event: self.check_hand_enter(canvas2))
                canvas2.tag_bind(node, '<Leave>',   lambda event: self.check_hand_leave(canvas2))
                label = canvas2.create_text((x+15, y+6),text=str(listenode[num]),font=("Purisa", 12),fill='#f0f0f0')
                num+=1
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas2.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas2.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas2))
                canvas2.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas2))
        ScaleClass.update_points(canvas2)

    def check_hand_enter(self,canvas2):
        canvas2.config(cursor="hand1")
    def check_hand_leave(self,canvas2):
        canvas2.config(cursor="")

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
            print(self.selected)
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

            if self.selected==5+Interface.numImageActuelle*6:
                Interface.canvasCorps.move(10+Interface.numImageActuelle*11,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(Interface.PolygoneB.nonodes[Interface.PolygoneB.nodes.index(10+Interface.numImageActuelle*11)],dx/3,dy/3)
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

            if self.selected==3+Interface.numImageActuelle*6:
                Interface.canvasCorps.move(8+Interface.numImageActuelle*11,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(Interface.PolygoneB.nonodes[Interface.PolygoneB.nodes.index(8+Interface.numImageActuelle*11)],dx/3,dy/3)
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
    # classe ScaleClassBody pour la gestion des points lors de la correction du corps
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
                canvas3.tag_bind(node, '<Enter>',   lambda event: self.check_hand_enter(canvas3))
                canvas3.tag_bind(node, '<Leave>',   lambda event: self.check_hand_leave(canvas3))
                label = canvas3.create_text((x+15, y+6),text=str(listenode[num]),font=("Purisa", 12),fill='#f0f0f0')
                num+=1
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas3.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas3.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas3))
                canvas3.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas3))
        ScaleClassBody.update_points(canvas3)

    def check_hand_enter(self,canvas3):
        canvas3.config(cursor="hand1")
    def check_hand_leave(self,canvas3):
        canvas3.config(cursor="")

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
            print(self.selected)
            if self.selected==5+Interface.numImageActuelle*6:
                Interface.canvasCorps.move(6+Interface.numImageActuelle*11,dx/3,dy/3)
                print(6+Interface.numImageActuelle*11)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(Interface.PolygoneB.nonodes[Interface.PolygoneB.nodes.index(6+Interface.numImageActuelle*11)],dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.PolygoneB.points[1][0] += dx
                Interface.PolygoneB.points[1][1] += dy
                coordes = sum(Interface.PolygoneB.points, [])
                Interface.canvasCorps.coords(Interface.PolygoneB.polygon, coordes)
                Interface.canvasCorps.update()
                Interface.PolygoneB.previous_x = event.x
                Interface.PolygoneB.previous_y = event.y
                Interface.PolygoneB.update_points(Interface.canvasCorps)

            if self.selected==3+Interface.numImageActuelle*6:
                Interface.canvasCorps.move(4+Interface.numImageActuelle*11,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(Interface.PolygoneB.nonodes[Interface.PolygoneB.nodes.index(4+Interface.numImageActuelle*11)],dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.PolygoneB.points[0][0] += dx
                Interface.PolygoneB.points[0][1] += dy
                coordes = sum(Interface.PolygoneB.points, [])
                Interface.canvasCorps.coords(Interface.PolygoneB.polygon, coordes)
                Interface.canvasCorps.update()
                Interface.PolygoneB.previous_x = event.x
                Interface.PolygoneB.previous_y = event.y
                Interface.PolygoneB.update_points(Interface.canvasCorps)

        ScaleClassBody.update_points(canvas3)

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
        canvas1.move(BodyFish.poisson, -(BodyFish.left[0]-590),-(BodyFish.left[1]-340))

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
        """!
        Constructeur du polygone du corps
        @param canvas tk.Canvas : cadre de l'image
        @param points list : liste des points du polygone
        @param color String : couleur du polygone
        """
        self.previous_x = self.previous_y = self.selected = self.x = None
        self.points = points

        if points!=None:
            if color=='red':outline='red'
            else: outline=''
            self.polygon = canvas1.create_polygon(self.points,fill='',outline=outline,smooth=0,width=3,dash=())
            BodyClass.id_polygons.append(self.polygon)
            canvas1.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag,canvas1))
            canvas1.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas1))
            canvas1.tag_bind(self.polygon, '<B1-Motion>',lambda event = self.polygon : self.on_move_polygon(event,canvas1))
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas1.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                canvas1.tag_bind(node, '<Enter>',   lambda event: self.check_hand_enter(canvas1))
                canvas1.tag_bind(node, '<Leave>',   lambda event: self.check_hand_leave(canvas1))
                label = canvas1.create_text((x+15, y+6),text=str(node%15),font=("Purisa", 1),fill='green')
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas1.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag,canvas1))
                canvas1.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas1))
                canvas1.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas1))

        BodyClass.update_points(canvas1)

        if(len(BodyClass.pointsFish)>0):
            InterfaceC.afficheLongueurBody()

    def check_hand_enter(self,canvas1):
        canvas1.config(cursor="hand1")
    def check_hand_leave(self,canvas1):
        canvas1.config(cursor="")


    def update_points(canvas1):
        """!
        Methode de mise à jour de la position des points
        @param canvas tk.Canvas : cadre de l'image
        """
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
        InterfaceC.afficheLongueurBody()

    def on_release_tag(self, event, number, tag,canvas1):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = self.previous_x = self.previous_y = None
        BodyClass.update_points(canvas1)
        InterfaceC.afficheLongueurBody()

    def on_move_node(self, event, number,canvas1):
        """!
        Methode pour deplacer un noeud du graphe
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        print(self.selected)
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

            px50mm = XY_tools.Externes.euclide(InterfaceC.canvasEchelle.coords(3),InterfaceC.canvasEchelle.coords(5))
            print("\n\nPoints sélectionné \n\n")
            print(self.selected)

            if self.selected==5+10*InterfaceC.numImageActuelle:
                InterfaceC.canvasEchelle2.move(5,3*dx,3*dy)
                InterfaceC.canvasEchelle2.update()
                InterfaceC.canvasEchelle2.move(InterfaceC.PolygoneC.nonodes[InterfaceC.PolygoneC.nodes.index(5)],3*dx,3*dy)
                InterfaceC.PolygoneC.pointsEchelle[1][0] += dx
                InterfaceC.PolygoneC.pointsEchelle[1][1] += dy
                coordes = sum(InterfaceC.PolygoneC.pointsEchelle, [])
                InterfaceC.canvasEchelle2.coords(InterfaceC.PolygoneC.polygon, coordes)
                Interface.canvasEchelle2.update()
                InterfaceC.PolygoneC.previous_x = event.x
                InterfaceC.PolygoneC.previous_y = event.y
                InterfaceC.PolygoneC.update_points(InterfaceC.canvasEchelle2)
                InterfaceC.afficheLongueur()

            if self.selected==3+10*InterfaceC.numImageActuelle:
                InterfaceC.canvasEchelle2.move(3,3*dx,3*dy)
                InterfaceC.canvasEchelle2.update()
                InterfaceC.canvasEchelle2.move(InterfaceC.PolygoneC.nonodes[InterfaceC.PolygoneC.nodes.index(3)],3*dx,3*dy)
                InterfaceC.canvasEchelle2.update()
                InterfaceC.PolygoneC.pointsEchelle[0][0] += dx
                InterfaceC.PolygoneC.pointsEchelle[0][1] += dy
                coordes = sum(InterfaceC.PolygoneC.pointsEchelle, [])
                InterfaceC.canvasEchelle2.coords(InterfaceC.PolygoneC.polygon, coordes)
                InterfaceC.canvasEchelle2.update()
                InterfaceC.PolygoneC.previous_x = event.x
                InterfaceC.PolygoneC.previous_y = event.y
                InterfaceC.PolygoneC.update_points(InterfaceC.canvasEchelle2)
                InterfaceC.afficheLongueur()

            if self.selected==7+10*InterfaceC.numImageActuelle:
                InterfaceC.canvasEchelle.move(3,3*dx,3*dy)
                InterfaceC.canvasEchelle.update()
                InterfaceC.canvasEchelle.move(InterfaceC.PolygoneB.nonodes[InterfaceC.PolygoneB.nodes.index(3)],3*dx,3*dy)
                Interface.canvasEchelle.update()
                InterfaceC.PolygoneB.pointsEchelle[0][0] += dx
                InterfaceC.PolygoneB.pointsEchelle[0][1] += dy
                coordes = sum(InterfaceC.PolygoneB.pointsEchelle, [])
                InterfaceC.canvasEchelle.coords(InterfaceC.PolygoneB.polygon, coordes)
                Interface.canvasEchelle.update()
                InterfaceC.PolygoneB.previous_x = event.x
                InterfaceC.PolygoneB.previous_y = event.y
                InterfaceC.PolygoneB.update_points(InterfaceC.canvasEchelle)
                InterfaceC.afficheLongueur()

            if self.selected==9+10*InterfaceC.numImageActuelle:
                InterfaceC.canvasEchelle.move(5,3*dx,3*dy)
                InterfaceC.canvasEchelle.update()
                InterfaceC.canvasEchelle.move(InterfaceC.PolygoneB.nonodes[InterfaceC.PolygoneB.nodes.index(5)],3*dx,3*dy)
                Interface.canvasEchelle.update()
                InterfaceC.PolygoneB.pointsEchelle[1][0] += dx
                InterfaceC.PolygoneB.pointsEchelle[1][1] += dy
                coordes = sum(InterfaceC.PolygoneB.pointsEchelle, [])
                InterfaceC.canvasEchelle.coords(InterfaceC.PolygoneB.polygon, coordes)
                Interface.canvasEchelle.update()
                InterfaceC.PolygoneB.previous_x = event.x
                InterfaceC.PolygoneB.previous_y = event.y
                InterfaceC.PolygoneB.update_points(InterfaceC.canvasEchelle)
                InterfaceC.afficheLongueur()

        ScaleClassC.update_points(self,canvas1)
        BodyClass.update_points(canvas1)
        InterfaceC.afficheLongueurBody()

    def on_move_polygon(self, event,canvas1):
        """!
        Methode pour deplacer le polygone entier
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
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
        InterfaceC.afficheLongueurBody()

    def calculDistances():
        """!
        Methode pour calculer certaines distances caractéristiques
        """
        BodyClass.distances_check = XY_tools.Externes.calculDistances2(BodyClass.pointsFish[2:4],BodyClass.pointsFish[0:2])
        return BodyClass.distances_check


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


from tkinter import font as tkfont

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_propagate(False)
        self.frames = {}
        for F in (Interface, InterfaceC):
            frame = F(master = container, controller = self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Interface)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Interface(tk.Frame):
    sexModele = None
    version = 2.0
    canvasTete = None
    def __init__(self,master,controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.listeImages = []
        self.add_labels()
        Interface.numImageActuelle = 0
        self.add_menu(master)
        self.add_canvas()
        self.add_buttons()
        self.add_labels()
        self.createlog()
        self.verbose_intro()

    def restart_program(self):
        import sys
        import os
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def changeLangueFr(self):
        self.boutonImport.config(text = "Importer les images")
        self.boutonPredict.config(text = "Prédire")
        self.boutonCorps.config(text = "1) Réglage corps")
        self.boutonEchelle.config(text = "2) Réglage échelle")
        self.labelIntro.config(text=" Procédure de sexage de l'épinoche à trois épines",font=("Andalus",16,"bold"))
        self.menubar.entryconfig(1,label = "Fichier")
        self.menubar.entryconfig(2,label = "Outils")
        self.menubar.entryconfig(3,label = "Modèles")
        self.menubar.entryconfig(4,label = "Affichage")
        self.menubar.entryconfig(5,label = "Langue")
        self.menubar.entryconfig(6,label = "Aide")
        self.menuFichier.entryconfig(0,label="Importer")
        self.menuFichier.entryconfig(2,label="Quitter")
        self.menuOutils.entryconfig(0,label="Prédire le sexe")
        self.menuOutils.entryconfig(1,label="Image suivante")
        self.menuOutils.entryconfig(2,label="Image précédente")

        self.menuModeles.entryconfig(0,label = "Préparer MaJ Pointage")
        self.menuModeles.entryconfig(1,label = "MaJ Pointage 🔒")
        self.menuModeles.entryconfig(2,label = "MaJ Sexage 🔒")

        self.menuAffichage.entryconfig(0,label = "Vue pour petit écran")
        self.menuAffichage.entryconfig(1,label = "Vue pour grand écran")


    def changeLangueEn(self):
        self.boutonImport.config(text = "Import images")
        self.boutonPredict.config(text = "Predict")
        self.boutonCorps.config(text = "1) Check Body landmarks")
        self.boutonEchelle.config(text = "2) Check Scale landmarks")
        self.labelIntro.config(text="",font=("Andalus",16,"bold"))

        self.labelIntro.config(text=" Sexing procedure for three-spined stickleback  ",font=("Andalus",16,"bold"))

        self.menubar.entryconfig(1,label = "File")
        self.menubar.entryconfig(2,label = "Tools")
        self.menubar.entryconfig(3,label = "Models")
        self.menubar.entryconfig(4,label = "Display")
        self.menubar.entryconfig(5,label = "Language")
        self.menubar.entryconfig(6,label = "Help")


        self.menuFichier.entryconfig(0,label="Import")
        self.menuFichier.entryconfig(2,label="Quit")

        self.menuOutils.entryconfig(0,label="Predict the gender")
        self.menuOutils.entryconfig(1,label="Next image")
        self.menuOutils.entryconfig(2,label="Previous image")

        self.menuModeles.entryconfig(0,label = "Prepare Update")
        self.menuModeles.entryconfig(1,label = "Landmark Model Update 🔒")
        self.menuModeles.entryconfig(2,label = "Classification Model Update 🔒")

        self.menuAffichage.entryconfig(0,label = "Mini View")
        self.menuAffichage.entryconfig(1,label = "Normal View")



    def add_canvas(self):
        """Canvas pour logo Ineris"""
        # pathLogo = XY_tools.Externes.resource_path("logo2.png")
        try:
            pathLogo = XY_tools.Externes.resource_path("logo2.png")
            self.imgLogo2 = ImageTk.PhotoImage(Image.open(pathLogo).resize((157,84)))

        except:
            pathLogo = pathPython + "\images\logo2.png"
            self.imgLogo2 = ImageTk.PhotoImage(Image.open(pathLogo).resize((157,84)))

        self.canvasLogo2 = tk.Canvas(self,bg='#f0f0f0')
        self.canvasLogo2.config(width=157,height=84)
        self.canvasLogo2.place(x=0,y=0)
        self.canvasLogo2.create_image(0, 0, anchor=tk.NW,image=self.imgLogo2)

        ''' Canvas blanc '''
        pathBlank = XY_tools.Externes.resource_path("logo_blank.png")
        self.canvasBlank = tk.Canvas(self,bg='#f0f0f0')
        self.canvasBlank.config(width = 1,height=150)
        self.canvasBlank.grid(row=1)

        ''' Canvas pour le schema de pointage '''
        # pathSchema = XY_tools.Externes.resource_path("schema.png")
        try:
            pathSchema = XY_tools.Externes.resource_path("schema.png")
            self.imgSchema = ImageTk.PhotoImage(Image.open(pathSchema).resize((288,192)))
        except:
            pathSchema = pathPython + "\images\schema.png"
            self.imgSchema = ImageTk.PhotoImage(Image.open(pathSchema).resize((288,192)))

        self.canvasSchema = tk.Canvas(self,bg='#f0f0f0')
        self.canvasSchema.config(width = 288,height=192)
        self.canvasSchema.place(relx=0.79,rely=0)
        self.canvasSchema.create_image(0,0,anchor=tk.NW,image=self.imgSchema)

        ''' Canvas pour la tête '''
        Interface.canvasTete = tk.Canvas(self,bg='#f0f0f0',bd=0,highlightthickness=1, highlightbackground="black")
        Interface.canvasTete.config(width=500, height=370)
        Interface.canvasTete.grid(column=0,row=8)

        ''' Canvas pour le corps '''
        Interface.canvasCorps = tk.Canvas(self,bg='#f0f0f0',highlightthickness=1, highlightbackground="black")
        Interface.canvasCorps.config(width=700, height=370)
        Interface.canvasCorps.grid(column=1,row=8)

        ''' Canvas pour corriger les points de l'échelle '''
        Interface.canvasEchelle = tk.Canvas(self,bg='#f0f0f0')
        Interface.canvasEchelle.config(width=1590, height=200)
        Interface.canvasEchelle.place(relx=0,rely=0.7)

        """Canvas pour corriger les points du corps"""
        Interface.canvasEchelle2 = tk.Canvas(self,bg='#f0f0f0')
        Interface.canvasEchelle2.config(width=1590,height=240)
        Interface.canvasEchelle2.place(relx=0,rely=0.66)


    def add_buttons(self):

        self.boutonMini = ttk.Button(self,text = "Mini GUI", command=lambda: self.controller.show_frame(InterfaceC))
        try:
            self.logo00 = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_mini.png'))
        except:
            self.logo00 = tk.PhotoImage(file = pathPython+'\images\logo_mini.png')

        self.boutonMini.config(image=self.logo00, compound=tk.LEFT)
        self.small_logo00 = self.logo00.subsample(15,15)
        self.boutonMini.config(image = self.small_logo00)
        self.boutonMini.place(relx=0.125,rely=0.12)



        self.boutonRestart = ttk.Button(self,text="Restart",command = self.restart_program)
        try:
            self.logo0 = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_restart.png'))
        except:
            self.logo0 = tk.PhotoImage(file = pathPython+'\images\logo_restart.png')

        self.boutonRestart.config(image=self.logo0, compound=tk.LEFT)
        self.small_logo0 = self.logo0.subsample(17,17)
        self.boutonRestart.config(image = self.small_logo0)
        self.boutonRestart.place(relx=0.05,rely=0.12)

        self.boutonImport = ttk.Button(self,text = "Importer les images",command = self.importImage)
        try:
            self.logo = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_import.png'))
        except:
            self.logo = tk.PhotoImage(file =pathPython+'images\logo_import.png')
        self.boutonImport.config(image=self.logo, compound=tk.LEFT)
        self.small_logo = self.logo.subsample(7,7)
        self.boutonImport.config(image = self.small_logo)
        self.boutonImport.place(relx=0.20,rely=0.12)

        self.boutonImport.bind('<Control-o>',self.importImage)

        self.boutonPredict = ttk.Button(self,text = "Predire",command = self.Model_Sexage)
        try:
            self.logo2 = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_predict.png'))
        except:
            self.logo2 = tk.PhotoImage(file = pathPython+'images\logo_predict.png')
        self.boutonPredict.config(image=self.logo2, compound=tk.LEFT)
        self.small_logo2 = self.logo2.subsample(15,15)
        self.boutonPredict.config(image = self.small_logo2)
        self.boutonPredict.place(relx=0.31,rely=0.12)

        self.boutonPredict.bind('<Control-p>',self.Model_Sexage)

        self.boutonPrevious = ttk.Button(self,text="",command = self.previousImage)
        try:
            self.logo3 = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_left_arrow.png'))
        except:
            self.logo3 = tk.PhotoImage(file = pathPython+'images\logo_left_arrow.png')
        self.boutonPrevious.config(image=self.logo3, compound=tk.LEFT)
        self.small_logo3 = self.logo3.subsample(15,15)
        self.boutonPrevious.config(image = self.small_logo3)
        self.boutonPrevious.place(relx=0.40,rely=0.12)

        self.boutonNext = ttk.Button(self,text="",command = self.nextImage)
        try:
            self.logo4 = tk.PhotoImage(file = os.path.join(sys._MEIPASS, 'logo_right_arrow.png'))
        except:
            self.logo4 = tk.PhotoImage(file = pathPython+'images\logo_right_arrow.png')
        self.boutonNext.config(image=self.logo4, compound=tk.LEFT)
        self.small_logo4 = self.logo4.subsample(15,15)
        self.boutonNext.config(image = self.small_logo4)
        self.boutonNext.place(relx=0.47,rely=0.12)

        self.boutonCorps = ttk.Button(self,text="1) Réglage corps", command = self.afficheCorps)
        self.boutonCorps.place(relx = 0.75,rely=0.5)

        self.boutonEchelle = ttk.Button(self,text="2) Réglage échelle",command = self.hideCorps)
        self.boutonEchelle.place(relx=0.75,rely=0.55)

    def add_labels(self):
        ''' Label Intro de presentation'''

        self.labelIntro = tk.Label(self,text=" Procédure de sexage de l'épinoche à trois épines",font=("Andalus",16,"bold"))
        self.labelIntro.place(relx=0.3,rely=0)

        self.labelSex = tk.Label(self,text="")
        self.labelSex.place(relx=0.55,rely=0.13)

        self.labelNumImage = tk.Label(self,text="",font=("Purisa",11),fg='gray')
        self.labelNumImage.place(relx=0.05,rely=0.975)
        self.labelNomImage = tk.Label(self,text="",font=("Purisa",11),fg='gray')
        self.labelNomImage.place(relx=0.1,rely=0.975)

    def add_menu(self,master):
        ''' Fenetre et menu'''
        self.controller.state('zoomed')
        self.controller.title("Morphométrie Ineris (Epinoche)")
        self.menubar = tk.Menu(self)
        self.menuFichier = tk.Menu(self.menubar,tearoff=0)
        self.menuFichier.add_command(label="Importer", command=self.importImage,accelerator="(Ctrl+O)")
        self.bind_all("<Control-o>",lambda e : self.importImage())
        self.menuFichier.add_separator()
        self.menuFichier.add_command(label="Quitter", command=self.destroy,accelerator="(Ctrl+Q)")
        self.bind("<Control-q>",lambda e : self.destroy())
        self.menubar.add_cascade(label="Fichier", menu=self.menuFichier)

        self.menuOutils = tk.Menu(self.menubar,tearoff=0)
        self.menuOutils.add_command(label="Prédire le sexe",command=self.Model_Sexage,accelerator="(Ctrl+P)")
        self.bind("<Control-p>",lambda e : self.Model_Sexage())
        self.menuOutils.add_command(label="Image suivante",command=self.nextImage,accelerator="(Ctrl+Entrée)")
        self.bind("<Control-Return>",lambda e : self.nextImage())
        self.menuOutils.add_command(label="Image précédente",command=self.previousImage,accelerator="(Ctrl+Backspace)")
        self.bind("<Control-BackSpace>",lambda e : self.previousImage())
        self.menubar.add_cascade(label="Outils",menu=self.menuOutils)

        self.menuModeles = tk.Menu(self.menubar,tearoff=0)
        self.menuModeles.add_command(label="Prépare MaJ Pointage",command=Interface.improveLandmarksModel)
        self.menuModeles.add_command(label="MaJ Pointage 🔒",command=GUI_update.InterfacePoint)
        self.menuModeles.add_command(label="MaJ Sexage 🔒",command=GUI_update.InterfaceGender)
        self.menubar.add_cascade(label="Modèles",menu=self.menuModeles)

        self.menuAffichage = tk.Menu(self.menubar,tearoff=0)
        self.menuAffichage.add_command(label="Vue pour petit écran",command=lambda:self.controller.show_frame(InterfaceC),accelerator="(Alt+c)")
        self.bind_all("<Alt-c>",lambda e: self.controller.show_frame(InterfaceC))
        self.menuAffichage.add_command(label="Vue pour grand écran",command=lambda:self.controller.show_frame(Interface),accelerator="(Alt+v)")
        self.bind_all("<Alt-v>",lambda e: self.controller.show_frame(Interface))
        self.menubar.add_cascade(label="Affichage",menu=self.menuAffichage)

        menuLangue = tk.Menu(self.menubar,tearoff=0)
        menuLangue.add_command(label="Français",command=self.changeLangueFr)
        menuLangue.add_command(label="English",command=self.changeLangueEn)
        self.menubar.add_cascade(label="Langues",menu=menuLangue)

        menuAide = tk.Menu(self.menubar, tearoff=0)
        menuAide.add_command(label="A propos", command=self.help)
        menuAide.add_command(label="Exemple d'image acceptée",command=Interface.displayExample)
        menuAide.add_command(label="Version",command=Interface.getVersion)
        self.menubar.add_cascade(label="Aide", menu=menuAide)
        self.controller.config(menu=self.menubar)

    def displayExample():
        import sys,subprocess
        cmdline = {'win32':'explorer'}[sys.platform]
        try:
            path = pathPython+"images\example.jpg"
        except:
            path = os.path.join(sys._MEIPASS, 'example.jpg')
        subprocess.Popen([cmdline,path])

    def createlog(self):
        if not os.path.exists(os.getcwd()+"/log"):
            os.mkdir(os.getcwd()+"/log")

        pathname = os.getcwd()+"/log/"
        date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = date+"_"+"rapport"
        filename2 = date+"_"+"resultats"
        self.finalname = pathname+filename+".txt"
        self.finalname2 = pathname+filename2+".csv"
        os.umask(0)
        f = open(self.finalname,"w+")
        f.close()
        os.chmod(self.finalname, 0o777)
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
        message = XY_tools.Externes.verbose_points(listepoints,self.listeImages, Interface.numImageActuelle)
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
        #modify the following line to update head landmark model
        name_predictor = 'predictor_head2.dat'
        try:
            pathPredictor = os.path.join(sys._MEIPASS, name_predictor)
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),name_predictor)
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = pathPython+"\models"+"\\"+name_predictor
            a = ModelPoints(pathPython+"models\\","")
            a.predict(pathimage,pathPython+"\models\\",name_predictor)
            listepoints = ML.ML_pointage.xmltolistY(pathPython+"\models\\"+"output.xml",0)

        self.verbose_points(listepoints)
        return listepoints[0]

    def Model_Echelle(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_scale3.dat')
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_scale3.dat")
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = pathPython+"models\\predictor_scale3.dat"
            a = ModelPoints(pathPython+"\models\\","")
            a.predict(pathimage,pathPython+"\models\\","predictor_scale3.dat")
            listepoints = ML.ML_pointage.xmltolistY(pathPython+"\models\\"+"output.xml",0)

        return listepoints[0]


    def Model_Longueur(self,pathimage):
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_LS3.dat')
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_LS3.dat")
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = pathPython+"models\\predictor_LS3.dat"
            a = ModelPoints(pathPython+"models\\","")
            a.predict(pathimage,pathPython+"\models\\","predictor_LS3.dat")
            listepoints = ML.ML_pointage.xmltolistY(pathPython+"\models\\"+"output.xml",0)

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
        text2 = text.split(";")
        print(text2)
        self.labelSex.config(text = text)
        # print(text)
        nomImage = "".join(self.listeImages[Interface.numImageActuelle].split("/")[-1])
        self.NomImages.append(nomImage)
        self.NumImages.append(Interface.numImageActuelle+1)
        self.LS.append(list(ae.values[0])[0])
        self.sexe.append(text.split(">")[-1])

        if(Interface.numImageActuelle==len(self.listeImages)-1):

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
        # Interface.canvasEchelle2.delete('all')



    def improveLandmarksModel():
        message = "Pour ajouter des données au modèle v1 de placement de points :"
        message += "\n\n1) Ajouter les photos nouvelles dans un dossier tmp"
        message += "\n2) Créer un fichier temp.tps grâce à tpsUtils (build tps)"
        message += "\n3) Créer un fichier v2.tps grâce à tpsUtils (append temp+v1) sans inclure path"
        message += "\n4) Pointer les images avec tpsDig"
        message += "\n5) Sauvegarder (overwrite) v2.tps"
        message += "\n6) Déplacer les images novelles dans le même dossier que les anciennes"

        tk.messagebox.showinfo(title="Informations",message=message)

    def afficheLongueur():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs dans l'interface
        """
        Interface.PolygoneA.calculDistances()

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
        try:
            Interface.canvasEchelle2.delete('all')
        except:
            Interface.canvasEchelle2 = tk.Canvas(self,bg='#f0f0f0')
            Interface.canvasEchelle2.config(width=1590,height=240)
            Interface.canvasEchelle2.place(relx=0,rely=0.66)
        Interface.canvasEchelle.delete('all')

        ScaleClassBody.pointsEchelle = []
        self.labelNomImage.config(text="")

    def resetListeImages(self):
        """!
        Méthode permettant de remettre à zero les images chargées
        """
        self.listeImages = []
        Interface.numImageActuelle = 0

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
            webbrowser.open('https://github.com/RalphMasson/MorphoEpinoche/releases/')

    def allDist(lenBody):
        px50mm = XY_tools.Externes.euclide(Interface.canvasEchelle.coords(Interface.PolygoneC.nodes[0]),Interface.canvasEchelle.coords(Interface.PolygoneC.nodes[1]))
        listedistances2 = []
        listedistances2.append(round(lenBody*50/px50mm,5))
        for x in Interface.PolygoneA.distances_all:
            listedistances2.append(x)
        Interface.modeleDistances = listedistances2
        print(Interface.modeleDistances)


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
        path_global = '/'.join(self.listeImages[Interface.numImageActuelle].split('/')[:-1])
        self.imgActuelle = self.listeImages[Interface.numImageActuelle]
        self.labelNomImage.config(text=self.imgActuelle)
        self.labelNumImage.config(text=str(Interface.numImageActuelle+1)+"/"+str(len(self.listeImages)))

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

        points_echelle2 = self.Model_Echelle(self.imgActuelle)
        corpsStandard.extend([list(np.array(points_echelle2[0])/3),list(np.array(points_echelle2[1])/3)])
        BodyFish.left = corpsStandard[3]
        corpsStandard = XY_tools.Externes.centerPoints(corpsStandard[0:4],BodyFish.left,590,340)

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
        Interface.PolygoneA = Polygone(self.canvasTete,points_tete,'#ff00f2',ligne=False)
        Interface.PolygoneA.pointsEchelle = points_echelle
        Interface.PolygoneA.calculDistances()

        Interface.PolygoneB = Polygone(Interface.canvasCorps,corpsStandard,'cyan',ligne=True)

        Interface.PolygoneC = ScaleClass(Interface.canvasEchelle,points_echelle,'#ffffff')

        Interface.PolygoneD = ScaleClassBody(Interface.canvasEchelle2,points_longueur,'#ffffff')


    def nextImage(self):
        """!
        Méthode permettant de passer à l'image d'après
        """
        if(Interface.numImageActuelle<len(self.listeImages)):
            self.blockButton(+1)

    def previousImage(self):
        """!
        Méthode permettant de revenir a l'image précédente
        """
        if(Interface.numImageActuelle>0):
            self.blockButton(-1)

    def blockButton(self,param):
        """!
        Méthode permettant de désactiver temporairement les boutons pour éviter une superposition d'images
        @param param : +1 pour passer à l'image suivante, -1 pour la précédente
        """
        import time
        self.unbind_all("<Control-Return>")
        self.unbind_all("<Control-BackSpace>")
        Interface.numImageActuelle+=param
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

    def help(self):
        """!
        Méthode permettant d'afficher des informations
        """
        message = "PROCEDURE DE SEXAGE DE L'EPINOCHE v"+str(Interface.version)
        message += "\n\n- Modèle de placement de points par Machine Learning (learning : 385 individus)"
        message += "\n\n- Modèle de classification Male/Femelle par Machine Learning (learning : 336 individus)"
        message += "\n\n\n Interface développée par R. Masson pour l'INERIS"
        tk.messagebox.showinfo(title="Informations",message=message)






## VERSION MINI

class HeadFishC():
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
    img = None
    def __init__(self, canvas,PIL_image,CV2_image,size):
        HeadFishC.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        HeadFishC.poisson = canvas.create_image(0, 0, anchor=tk.NW,image=HeadFishC.img)
        HeadFishC.CV2_image_big = CV2_image
        canvas.move(HeadFishC.poisson,-(HeadFishC.oeilXY[0]-200),-(HeadFishC.oeilXY[1]-200))

class HeadClass():
    """Variables globales pour export
    id_polygons : liste des id des polygons (la tete et l'echelle)
    pointsTete : liste des points de la tête [(x1,y1),(x2,y2)...]
    pointsEchelle3mm : liste des points de l'echelle [(x1,y1),(x2,y2)]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    """
    id_polygons = []
    pointsFish = []
    pointsEchelle = []
    distances_check = []
    distances_all = []

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
            HeadClass.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                canvas.tag_bind(node, '<Enter>',   lambda event: self.check_hand_enter(canvas))
                canvas.tag_bind(node, '<Leave>',   lambda event: self.check_hand_leave(canvas))

                label = canvas.create_text((x+15, y+6),text=str(node%25),font=("Purisa", 1),fill='red')
                HeadClass.nodes.append(node)
                self.nonodes.append(label)
                canvas.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag,canvas))
                canvas.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number,canvas))

        HeadClass.update_points(canvas)

        if(len(HeadClass.pointsEchelle)>0):
             InterfaceC.afficheLongueur()

    def check_hand_enter(self,canvas):
        canvas.config(cursor="hand1")
    def check_hand_leave(self,canvas):
        canvas.config(cursor="")

    def update_points(canvas):
        """!
        Methode de mise à jour de la position des points
        @param canvas tk.Canvas : cadre de l'image
        """
        for id in HeadClass.id_polygons:
            liste = canvas.coords(id)
            if(len(liste)==20):HeadClass.pointsFish=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

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
        print(self.selected,event,tag)

    def on_release_tag(self, event, number, tag,canvas):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = self.previous_x = self.previous_y = None
        HeadClass.update_points(canvas)

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
            # print(self.selected)
            canvas.move(self.nonodes[HeadClass.nodes.index(self.selected)],dx,dy)
            self.points[number][0] += dx
            self.points[number][1] += dy
            coords = sum(self.points, [])
            canvas.coords(self.polygon, coords)
            # print(canvas.coords(self.selected))
            self.previous_x = event.x
            self.previous_y = event.y

        HeadClass.update_points(canvas)
        InterfaceC.afficheLongueur()
    def on_move_polygon(self, event,canvas):
        """!
        Methode pour deplacer le polygone entier
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            # move polygon
            canvas.move(self.selected, dx, dy)
            # move red nodes
            for item,item1 in zip(HeadClass.nodes,self.nonodes):
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
        """!
        Methode pour calculer toutes les distances de la tete
        """
        XY_tools.Externes.genererAllDistancesHead(HeadClass.pointsEchelle,HeadClass.pointsFish,Interface.sexModele.get(),pypath3)

    def calculDistances():
        """!
        Methode pour calculer certaines distances caractéristiques
        """
        print("points fish")
        print(HeadClass.pointsFish)
        print("point echelle")
        print(HeadClass.pointsEchelle)

        HeadClass.distances_all = XY_tools.Externes.calculDistancesv2(HeadClass.pointsEchelle, HeadClass.pointsFish)
        print("distance all")
        print(HeadClass.distances_all)
        # print(HeadClass.distances_all)
        # return HeadClass.distances_check

class ScaleClassC():
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
            print("scale")
            print(self.polygon)
            HeadClass.id_polygons.append(self.polygon)
            canvas2.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas2.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas2))
            canvas2.tag_bind(self.polygon, '<B1-Motion>', lambda event = self.polygon : self.on_move_polygon(event,canvas2))
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
        ScaleClassC.update_points(self,canvas2)



    def update_points(self,canvas2):
        """!
        Methode de mise à jour de la position des points
        @param canvas2 tk.Canvas : cadre de l'image
        """
        for id in HeadClass.id_polygons:
            liste = canvas2.coords(id)
            if(len(canvas2.coords(id))==4):ScaleClassC.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
        ScaleClassC.pointsEchelle = [[ScaleClassC.pointsEchelle[0][0],ScaleClassC.pointsEchelle[0][1]],[ScaleClassC.pointsEchelle[1][0],ScaleClassC.pointsEchelle[1][1]]]

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
        # print(self.selected,event,tag)

    def on_release_tag(self, event, number, tag,canvas2):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = self.previous_x = self.previous_y = None
        ScaleClassC.update_points(self,canvas2)

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
            px50mm = XY_tools.Externes.euclide(InterfaceC.canvasEchelle.coords(3),Interface.canvasEchelle.coords(5))
            print("\n\n Point selectionné \n\n")
            print(self.selected)
            if self.selected==5:
                InterfaceC.canvasCorps.move(9,dx/3,dy/3)
                InterfaceC.canvasCorps.update()
                InterfaceC.canvasCorps.move(BodyClass.nonodes[BodyClass.nodes.index(9)],dx/3,dy/3)
                InterfaceC.canvasCorps.update()
                BodyClass.points[3][0] += dx
                BodyClass.points[3][1] += dy
                coordes = sum(BodyClass.points, [])
                InterfaceC.canvasCorps.coords(BodyClass.polygon, coordes)
                InterfaceC.canvasCorps.update()
                BodyClass.previous_x = event.x
                BodyClass.previous_y = event.y
                BodyClass.update_points(Interface.canvasCorps)
                InterfaceC.afficheLongueur()
                app.labelLongueurBody.config(text="Longueur = "+str(round(Interface.lenBody*50/px50mm,3)))
                Interface.allDist(Interface.lenBody)

            if self.selected==3:
                InterfaceC.canvasCorps.move(7,dx/3,dy/3)
                InterfaceC.canvasCorps.update()
                InterfaceC.canvasCorps.move(BodyClass.nonodes[BodyClass.nodes.index(7)],dx/3,dy/3)
                InterfaceC.canvasCorps.update()
                BodyClass.points[2][0] += dx
                BodyClass.points[2][1] += dy
                coordes = sum(BodyClass.points, [])
                InterfaceC.canvasCorps.coords(BodyClass.polygon, coordes)
                InterfaceC.canvasCorps.update()
                BodyClass.previous_x = event.x
                BodyClass.previous_y = event.y
                BodyClass.update_points(InterfaceC.canvasCorps)
                InterfaceC.afficheLongueur()
                InterfaceC.allDist(Interface.lenBody)

            app.labelLongueurBody.config(text="Longueur = "+str(round(InterfaceC.lenBody*50/px50mm,3)))
            InterfaceC.allDist(InterfaceC.lenBody)



        ScaleClassC.update_points(self,canvas2)
        # Interface.afficheLongueur()
    def on_move_polygon(self, event,canvas2):
        """!
        Methode pour deplacer le polygone entier
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            # move polygon
            canvas2.move(self.selected, dx, dy)
            # move red nodes
            for item,item1 in zip(self.nodes,self.nonodes):
                canvas2.move(item, dx, dy)
                canvas2.move(item1,dx,dy)
            # recalculate values in self.points
            for item in self.points:
                item[0] += dx
                item[1] += dy
            self.previous_x = event.x
            self.previous_y = event.y
        ScaleClassC.update_points(self,canvas2)



class ScaleClassBodyC():
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
            HeadClass.id_polygons.append(self.polygon)
            canvas3.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas3.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas3))
            canvas3.tag_bind(self.polygon, '<B1-Motion>', lambda event = self.polygon : self.on_move_polygon(event,canvas3))
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

        ScaleClassBodyC.update_points(self,canvas3)



    def update_points(self,canvas3):
        """!
        Methode de mise à jour de la position des points
        @param canvas2 tk.Canvas : cadre de l'image
        """
        for id in HeadClass.id_polygons:
            liste = canvas3.coords(id)
            if(len(canvas3.coords(id))==4):
                ScaleClassBodyC.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
        ScaleClassBodyC.pointsEchelle = [[ScaleClassBodyC.pointsEchelle[0][0],ScaleClassBodyC.pointsEchelle[0][1]],[ScaleClassBodyC.pointsEchelle[1][0],ScaleClassBodyC.pointsEchelle[1][1]]]

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
        ScaleClassBodyC.update_points(self,canvas3)

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
                print(self.selected)
                InterfaceC.canvasCorps.move(5,dx/3,dy/3)
                InterfaceC.canvasCorps.update()
                InterfaceC.canvasCorps.move(BodyClass.nonodes[BodyClass.nodes.index(5)],dx/3,dy/3)
                InterfaceC.canvasCorps.update()
                BodyClass.points[1][0] += dx
                BodyClass.points[1][1] += dy
                coordes = sum(BodyClass.points, [])
                InterfaceC.canvasCorps.coords(BodyClass.polygon, coordes)
                InterfaceC.canvasCorps.update()
                BodyClass.previous_x = event.x
                BodyClass.previous_y = event.y
                BodyClass.update_points(InterfaceC.canvasCorps)
                InterfaceC.afficheLongueurBody()

            if self.selected==3:
                print(self.selected)
                InterfaceC.canvasCorps.move(3,dx/3,dy/3)
                InterfaceC.canvasCorps.update()
                InterfaceC.canvasCorps.move(BodyClass.nonodes[BodyClass.nodes.index(3)],dx/3,dy/3)
                InterfaceC.canvasCorps.update()
                BodyClass.points[0][0] += dx
                BodyClass.points[0][1] += dy
                coordes = sum(BodyClass.points, [])
                InterfaceC.canvasCorps.coords(BodyClass.polygon, coordes)
                InterfaceC.canvasCorps.update()
                BodyClass.previous_x = event.x
                BodyClass.previous_y = event.y
                BodyClass.update_points(InterfaceC.canvasCorps)
                InterfaceC.afficheLongueurBody()

            print("\n\n points \n\n")
            print(self.selected)


        ScaleClassBodyC.update_points(canvas3)
    def on_move_polygon(self, event,canvas3):
        """!
        Methode pour deplacer le polygone entier
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            canvas3.move(self.selected, dx, dy)
            for item,item1 in zip(self.nodes,self.nonodes):
                canvas3.move(item, dx, dy)
                canvas3.move(item1,dx,dy)
            for item in self.points:
                item[0] += dx
                item[1] += dy
            self.previous_x = event.x
            self.previous_y = event.y
        ScaleClassBodyC.update_points(canvas3)


class BodyFishC():
    poisson = None
    img = None
    def __init__(self, canvas1,PIL_image,size):
        BodyFishC.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        BodyFishC.poisson = canvas1.create_image(0, 0, anchor=tk.NW, image=BodyFishC.img)

class ScaleFishC():
    poisson = None
    img = None
    def __init__(self, canvas2,PIL_image,size):
        ScaleFishC.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        ScaleFishC.poisson = canvas2.create_image(0, 0, anchor=tk.NW, image=ScaleFishC.img)
        InterfaceC.canvasEchelle.itemconfig(ScaleFishC.poisson,state='normal')
        canvas2.move(ScaleFishC.poisson,-(ScaleFishC.left[0]-25),-(ScaleFishC.left[1]-50))

class ScaleFishBodyC():
    poisson = None
    img = None
    def __init__(self, canvas3,PIL_image,size):
        ScaleFishBodyC.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        ScaleFishBodyC.poisson = canvas3.create_image(0, 0, anchor=tk.NW, image=ScaleFishBodyC.img)
        InterfaceC.canvasEchelle2.itemconfig(ScaleFishBodyC.poisson,state='normal')
        InterfaceC.canvasEchelle2.move(ScaleFishBodyC.poisson,-(ScaleFishBodyC.left[0]-25),-(ScaleFishBodyC.left[1]-50))

class InterfaceC(tk.Frame):
    sexModele = None
    app = None
    chemin = ""
    version = 2.0
    def __init__(self, master,controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.root = master
        self.canvasGeneral = tk.Canvas(self,width=600,height=700,highlightthickness=0, highlightbackground="black")
        self.frame = tk.Frame(self.canvasGeneral)
        self.frame.pack(fill=tk.BOTH,expand=True)
        self.add_scrollbar()
        self.listeImages = []
        tk.Label(self.frame,text=" Sexing procedure of three-spined stickleback (mini) \n",font=("Andalus",16,"bold")).pack(padx=5,pady=5)
        self.add_buttons()
        self.labelSex = tk.Label(self.frame,text="")
        self.labelSex.pack()
        self.add_canvas()
        self.add_labels()
        self.createlog()
        self.verbose_intro()

    def add_scrollbar(self):
        self.vsb = tk.Scrollbar(self,orient="vertical",command=self.canvasGeneral.yview)
        self.hsb = tk.Scrollbar(self,orient="horizontal",command=self.canvasGeneral.xview)
        self.canvasGeneral.configure(yscrollcommand=self.vsb.set)
        self.canvasGeneral.configure(xscrollcommand=self.hsb.set)
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvasGeneral.pack(side="left", fill="both", expand=True)
        self.canvasGeneral.create_window((0,0), window=self.frame, anchor="nw",tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvasGeneral.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvasGeneral.bind_all("<Control-MouseWheel>", self.on_mousewheel2)

    def on_mousewheel2(self,event):
        scroll = -1 if event.delta > 0 else 1
        self.canvasGeneral.xview_scroll(scroll, "units")

    def on_mousewheel(self,event):
        scroll = -1 if event.delta > 0 else 1
        self.canvasGeneral.yview_scroll(scroll, "units")

    def add_canvas(self):
        """Canvas pour logo"""

        self.canvasLogo = tk.Canvas(self.frame,bg='#f0f0f0')
        self.canvasLogo.config(width=157,height=84)
        try:
            pathLogo = InterfaceC.resource_path("logo2.png")
            self.imgLogo = ImageTk.PhotoImage(Image.open(pathLogo).resize((157,84)))
        except:
            pathLogo = pathPython+'\images\logo2.png'
            self.imgLogo = ImageTk.PhotoImage(Image.open(pathLogo).resize((157,84)))
        self.canvasLogo.create_image(0, 0, anchor=tk.NW,image=self.imgLogo)

        ''' Canvas pour le schema '''
        self.canvasSchema = tk.Canvas(self.frame,bg='#f0f0f0')
        self.canvasSchema.config(width = 288,height=192)

        try:
            pathSchema = InterfaceC.resource_path("schema.png")
            self.imgSchema = ImageTk.PhotoImage(Image.open(pathSchema).resize((157,84)))
        except:
            pathSchema = pathPython+'\images\schema.png'
            self.imgSchema = ImageTk.PhotoImage(Image.open(pathSchema).resize((157,84)))
        self.canvasSchema.create_image(0,0,anchor=tk.NW,image=self.imgSchema)

        ''' Canvas pour la tête '''
        self.labelLongueur = tk.Label(self.frame,text="",justify=tk.LEFT)
        InterfaceC.canvasTete = tk.Canvas(self.frame,bg='#f0f0f0',bd=0,highlightthickness=1, highlightbackground="black")
        InterfaceC.canvasTete.config(width=500, height=500)
        InterfaceC.canvasTete.pack()
        self.labelLongueurBody = tk.Label(self.frame,justify=tk.LEFT)

        ''' Canvas pour le corps '''
        InterfaceC.canvasCorps = tk.Canvas(self.frame,bg='#f0f0f0',highlightthickness=1, highlightbackground="black")
        InterfaceC.canvasCorps.config(width=630, height=500)
        InterfaceC.canvasCorps.pack(padx=6)

        ''' Canvas pour gérer les corrections '''
        InterfaceC.canvasEchelle2 = tk.Canvas(self.frame,bg='#f0f0f0')
        # InterfaceC.canvasEchelle2.pack()
        InterfaceC.canvasEchelle = tk.Canvas(self.frame,bg='#f0f0f0')

    def add_labels(self):
        self.labelInfoPoints = tk.Label(self.frame,text="")
        self.labelNumImage = tk.Label(self.frame,text="Image :",font=("Purisa",11),fg='gray')
        self.labelNumImage.pack()
        self.labelNomImage = tk.Label(self.frame,text="",font=("Purisa",11),fg='gray')
        self.labelNomImage.pack()

    def add_buttons(self):
        self.boutonImport = tk.Button(self.frame,text = "Import image and autoplace",command = self.importImage,fg='purple')
        self.boutonImport.pack(anchor=tk.W,padx=5,pady=5,ipady=15,expand=True,fill='x')
        self.boutonImport.bind('<Control-o>',self.importImage)
        tk.Button(self.frame,text = "Predict",command = self.Model_Sexage,fg='purple').pack(anchor=tk.W,padx=5,ipady=8,fill='x')
        InterfaceC.sexModele = tk.StringVar(self.frame)
        self.boutonNext = tk.Button(self.frame,text='→',font=("Purisa",13,"bold"),command = self.nextImage)
        self.boutonNext.pack(fill='x',ipady=8)
        self.boutonPrevious = tk.Button(self.frame,text='←',font=("Purisa",13,"bold"),command = self.previousImage)
        self.boutonPrevious.pack(fill='x',ipady=8)
        tk.Button(self.frame,text="Normal version",command=lambda: self.controller.show_frame(Interface)).pack(fill='x',ipady=8)


    def allDist(lenBody):
        listepoints = []
        for i in HeadClass.nodes:
            listepoints.append([InterfaceC.canvasTete.coords(i)[0]+3,InterfaceC.canvasTete.coords(i)[1]+3])
        px50mm = XY_tools.Externes.euclide(InterfaceC.canvasEchelle.coords(3),InterfaceC.canvasEchelle.coords(5))
        listedistances2 = []
        listedistances2.append(round(lenBody*50/px50mm,5))

        for x in HeadClass.distances_all:
            listedistances2.append(x)
        InterfaceC.modeleDistances = listedistances2

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvasGeneral.configure(scrollregion=self.canvasGeneral.bbox("all"))

    def createlog(self):
        if not os.path.exists(os.getcwd()+"/log"):
            os.mkdir(os.getcwd()+"/log")

        pathname = os.getcwd()+"/log/"
        date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = date+"_"+"rapport"
        filename2 = date+"_"+"resultats"
        self.finalname = pathname+filename+".txt"
        self.finalname2 = pathname+filename2+".csv"
        os.umask(0)
        f = open(self.finalname,"w+")
        f.close()
        os.chmod(self.finalname, 0o777)
        self.data_result = pd.DataFrame()
        self.NomImages = []
        self.data_distances = []
        self.LS = []
        self.sexe = []
        self.NumImages = []


    def verbose_intro(self):
        message = "Rapport généré le "+datetime.now().strftime("%d/%m/%Y")+" à "+datetime.now().strftime("%H:%M:%S")+"\n"
        message += "# Morphométrie Epinoche Ineris v"+str(InterfaceC.version)+"\n\n"
        message += "Version mini utilisée"
        message += "- Développé par Ralph MASSON pour l'unité ESMI \n"
        message += "- Contact : ralph.masson@gmail.com \n\n"
        message += "# Langage et bibliothèques utilisés : \n"
        message += "- Python 3.8.6 \n"
        message += "- sklearn 0.23.2 - numpy 1.18.5 - scipy 1.5.2 - dlib 19.22.0 - xgboost 1.4.2 \n\n"
        message += "# ML_morph version\n"
        message += "\t - Algorithme utilisé : Regression trees (gradient boosting) \n"
        message += "\t - Performances : erreur de placement moyenne de 4 pixels (0.25% de la longueur standard) \n\n"
        message += "# ML_gender version\n"
        message += "\t - Algorithmes utilisés : Gradient Boosting, SVM, Random Forest (consensus) \n"
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
        message = XY_tools.Externes.verbose_points(listepoints,self.listeImages, InterfaceC.numImageActuelle)
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_distances(self,df_distance):
        print("toto")
        print(df_distance)
        print(type(df_distance))
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

    def getVersion():
        try:
            version = XY_tools.Externes.getVersion()
        except:
            version = "-- No internet connection --"

        message = "Dernière version disponible : "+"v"+str(version)
        message += "\nVersion actuelle : "+"v"+str(InterfaceC.version)
        message += "\nCliquez sur OK pour télécharger"

        reponse = tk.messagebox.askyesnocancel(title="Informations",message=message)
        if(reponse):
            InterfaceC.updateVersion()

    def resource_path(relative_path):
        """!
        Méthode permettant d'avoir le chemin absolu temporaire (pour l'exe) ou normal
        @param relative_path String : chemin du fichier dans le pc
        @return resource_path : chemin temporaire
        """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = pypath2+"/images/"
            base_path = '/'.join(pypath1.split("/")[:-1])+"/images"
            print('/'.join(pypath1.split("/")[:-1])+"/images")
        return os.path.join(base_path, relative_path)

    def afficheLongueur():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs dans l'interface
        """
        HeadClass.calculDistances()

    def afficheLongueurBody():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs du corps dans l'interface
        """
        BodyClass.calculDistances()

    def clearAllCanvas(self):
        """!
        Méthode permettant de remettre à zero l'interface
        """
        HeadClass.id_polygons=[]
        HeadClass.pointsFish=[]
        HeadClass.pointsEchelle=[]
        HeadClass.distances_check=[0 for _ in range(20)]
        self.labelLongueur.config(text="")
        BodyClass.id_polygons=[]
        BodyClass.pointsFish=[]
        BodyClass.pointsEchelle=[]
        BodyClass.distances_check=[0 for _ in range(20)]
        self.labelLongueurBody.config(text="")
        self.labelInfoPoints.config(text="")
        self.labelSex.config(text="")
        self.canvasTete.delete('all')
        self.canvasCorps.delete('all')
        self.labelNomImage.config(text="")

    def resetListeImages(self):
        """!
        Méthode permettant de remettre à zero les images chargées
        """
        self.listeImages = []
        InterfaceC.numImageActuelle = 0

    def updateVersion():
        """!
        Méthode permettant d'ouvrir le lien github du projet
        """
        webbrowser.open('https://github.com/RalphMasson/MorphoEpinoche/releases/')

    def importImage(self,event=' '):
        """!
        Méthode permettant de charger 1 ou plusieurs images
        """
        self.choice = 0
        self.resetListeImages()
        self.listeImages = XY_tools.Externes.openfn()
        self.calculPoints2()

    def calculPoints2(self):
        """!
        Méthode permettant de calculer les points et de les disposer sur l'image
        """

        path_global = '/'.join(self.listeImages[InterfaceC.numImageActuelle].split('/')[:-1])


        #Points de la tête
        points_tete = self.Model_Tete(self.listeImages[InterfaceC.numImageActuelle])[0]
        print(points_tete)
        points_tete_copy = points_tete
        print(points_tete_copy)
        #Oeil du poisson
        HeadFishC.oeilXY = [0.5*(points_tete_copy[1][0]+points_tete_copy[2][0]),0.5*(points_tete_copy[1][1]+points_tete_copy[2][1])]

        #Points de l'échelle calculés par le modèle 2
        points_echelle = self.Model_Echelle(self.listeImages[InterfaceC.numImageActuelle])[0]
        points_echelle_copy = points_echelle
        ScaleFishC.left = points_echelle[0]

        #Placement des points de l'echelle au bon endroit
        # points_echelle = XY_tools.Externes.centerPoints2([points_echelle[0],points_echelle[1]],ScaleFish.left)
        points_echelle = XY_tools.Externes.centerPoints(points_echelle[0:2],ScaleFishC.left,25,50)

        self.labelNomImage.config(text=self.listeImages[InterfaceC.numImageActuelle])
        self.labelNumImage.config(text=str(InterfaceC.numImageActuelle+1)+"/"+str(len(self.listeImages)))

        #Image de la tête
        self.ImagePIL = Image.open(self.listeImages[InterfaceC.numImageActuelle])
        HeadFishC(self.canvasTete,self.ImagePIL,cv2.imread(self.listeImages[InterfaceC.numImageActuelle]),(1920,1440))

        #Image entière
        self.ImagePIL2 = Image.open(self.listeImages[InterfaceC.numImageActuelle])
        BodyFishC(InterfaceC.canvasCorps,self.ImagePIL2,(640,480))

        #Calcul des points du corps
        listePoints3 = self.Model_Longueur(self.listeImages[InterfaceC.numImageActuelle])[0]
        listePoints3 = [[listePoints3[0][0]/3,listePoints3[0][1]/3],[listePoints3[1][0]/3,listePoints3[1][1]/3]]
        corpsStandard = listePoints3

        #Ajout de l'echelle
        corpsStandard.extend([[points_echelle_copy[0][0]/3,points_echelle_copy[0][1]/3],[points_echelle_copy[1][0]/3,points_echelle_copy[1][1]/3]])

        #Affichage des points sur l'image entière
        BodyClass(InterfaceC.canvasCorps,corpsStandard,'cyan')
        InterfaceC.canvasCorps.update()

        #Affichage des points sur la tête
        pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19,pt21 = points_tete_copy
        points_tete_copy = XY_tools.Externes.centerPoints([pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19,pt21],HeadFishC.oeilXY,200,200)
        HeadClass.pointsEchelle = points_echelle
        HeadClass(self.canvasTete, points_tete_copy,'#ff00f2')
        self.canvasTete.update()

        #Image de l'échelle
        self.ImagePIL3 = Image.open(self.listeImages[InterfaceC.numImageActuelle])
        tete2 = points_tete
        ScaleFishC(InterfaceC.canvasEchelle,self.ImagePIL3,(1920,1440))
        ScaleFishC.left = points_tete[0]

        InterfaceC.PolygoneB = ScaleClassC(InterfaceC.canvasEchelle,points_echelle,'#ffffff')
        points_echelle = XY_tools.Externes.centerPoints(points_echelle,ScaleFishC.left,25,50)
        print(points_echelle)

        # Calcul des points  du corps Bis
        points_longueur = self.Model_Longueur('/'.join(self.listeImages[0].split('/')[:-1]))[0]
        pt1,pt2 = [points_longueur[0][0],points_longueur[0][1]],[points_longueur[1][0],points_longueur[1][1]]
        ScaleFishBodyC.left = [points_longueur[0][0],points_longueur[0][1]]
        points_longueur = XY_tools.Externes.centerPoints([pt1,pt2],ScaleFishBodyC.left,25,50)
        print(points_longueur)
        # Image du corps
        self.ImagePIL4 = Image.open(self.listeImages[InterfaceC.numImageActuelle])
        ScaleFishBodyC(InterfaceC.canvasEchelle2,self.ImagePIL4,(1920,1440))
        InterfaceC.PolygoneC = ScaleClassBodyC(InterfaceC.canvasEchelle2,points_longueur,'#ffffff')

    def Model_Tete(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        print("points tête")

        #modify the following line to update head landmark model
        name_predictor = 'predictor_head2.dat'

        try:
            pathPredictor = os.path.join(sys._MEIPASS, name_predictor)
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),name_predictor)
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = pathPython+'models\\'+name_predictor
            a = ModelPoints(pathPython+'models\\',"")
            a.predict(pathimage,pathPython+"\models\\",name_predictor)
            listepoints = ML.ML_pointage.xmltolistY(pathPython+"\models\\"+"output.xml",0)

        self.verbose_points(listepoints)
        return listepoints

    def Model_Echelle(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        print("points echelle")
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_scale3.dat')
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_scale3.dat")
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = pathPython+'models\\predictor_scale3.dat'
            a = ModelPoints(pathPython+'models\\',"")
            a.predict(pathimage,pathPython+"\models\\","predictor_scale3.dat")
            listepoints = ML.ML_pointage.xmltolistY(pathPython+"\models\\"+"output.xml",0)

        return listepoints


    def Model_Longueur(self,pathimage):
        print("points longueur")
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_LS3.dat')
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_LS3.dat")
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        except:
            pathPredictor = pathPython+'models\\predictor_LS3.dat'
            a = ModelPoints(pathPython+"\models\\","")
            a.predict(pathimage,pathPython+"\models\\","predictor_LS3.dat")
            listepoints = ML.ML_pointage.xmltolistY(pathPython+"\models\\"+"output.xml",0)

        return listepoints


    def Model_Sexage(self):
        print("classification")
        # try:
        InterfaceC.lenBody = XY_tools.Externes.euclide(InterfaceC.canvasEchelle2.coords(3+6*InterfaceC.numImageActuelle),InterfaceC.canvasEchelle2.coords(5+6*InterfaceC.numImageActuelle))
        print("\n\n Longueur standard \n\n")
        print(InterfaceC.lenBody)
        # except:
        #     pass
        InterfaceC.allDist(InterfaceC.lenBody)
        from joblib import dump, load
        import pandas as pd

        predictorGB = "GBClassifierFinal3.joblib"
        predictorSVC = "SVCClassifierFinal3.joblib"
        predictorXGB = "XGBClassifierFinal3.joblib"

        try:
            clf = load(os.path.join(sys._MEIPASS,predictorGB))
            clf1 = load(os.path.join(sys._MEIPASS,predictorSVC))
            clf2 = load(os.path.join(sys._MEIPASS,predictorXGB))
        except:
            clf = load(pathPython+'models'+'\\'+predictorGB)
            clf1 = load(pathPython+'models'+'\\'+predictorSVC)
            clf2 = load(pathPython+'models'+'\\'+predictorXGB)

        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', None)
        ae = pd.DataFrame(InterfaceC.modeleDistances).T
        print("\n\n All distances \n\n")
        print(ae)
        # print(ae)
        prediction = clf.predict(ae)
        prediction1 = clf1.predict(ae)
        prediction2 = clf2.predict(ae)


        # Consensus
        if(prediction==prediction1==prediction2):
            y_consensus = prediction
        else:
            y_consensus = 0.5

        proba = max(clf.predict_proba(ae)[0])
        listePredictionInt = [clf.predict(ae)[0], clf1.predict(ae)[0], clf2.predict(ae)[0]]
        listeProba = [list(np.round(clf.predict_proba(ae),4).flatten()), list(np.round(clf1.predict_proba(ae),4).flatten()),list(np.round(clf2.predict_proba(ae),4).flatten())]

        listePredictionStr = ["F" if x==0 else "M" for x in listePredictionInt]
        if y_consensus==0:
            consensusStr = "F"
        if y_consensus==1:
            consensusStr = "M"
        if y_consensus==0.5:
            consensusStr = "Undetermined"

        text = ""
        for i in range(3):
            text += listePredictionStr[i]+" "+str(listeProba[i][listePredictionInt[i]])+";"
        text+="\n\n Sex classification : "+consensusStr
        self.labelSex.config(text = text)

        self.verbose_distances(ae)
        self.verbose_sexe(text,proba)

        nomImage = "".join(self.listeImages[InterfaceC.numImageActuelle].split("/")[-1])
        self.NomImages.append(nomImage)
        self.NumImages.append(InterfaceC.numImageActuelle+1)
        self.LS.append(list(ae.values[0])[0])
        self.sexe.append(text.split(">")[-1])

        if(InterfaceC.numImageActuelle==len(self.listeImages)-1):

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



    def affichePrediction():
        """!
        Méthode permettant d'afficher la prédiction du sexe
        """
        choix,couleur,p = IA_sexage.Prediction.predict(None,"","")
        self.labelSex.config(text="")
        self.labelSex.config(text=choix+" avec p="+str(round(p,2)),font=("Purisa",16),fg=couleur)

    def nextImage(self):
        """!
        Méthode permettant de passer à l'image d'après
        """
        if(InterfaceC.numImageActuelle<len(self.listeImages)):
            self.blockButton(+1)

    def previousImage(self):
        """!
        Méthode permettant de revenir a l'image précédente
        """
        if(InterfaceC.numImageActuelle>0):
            self.blockButton(-1)

    def blockButton(self,param):
        """!
        Méthode permettant de désactiver temporairement les boutons pour éviter une superposition d'images
        @param param : +1 pour passer à l'image suivante, -1 pour la précédente
        """
        import time
        self.unbind_all("<Control-Return>")
        self.unbind_all("<Control-BackSpace>")
        InterfaceC.numImageActuelle+=param
        nbPointNonDetectes = 0
        time.sleep(0.3)
        self.boutonPrevious.configure(state=tk.DISABLED)
        self.boutonNext.configure(state=tk.DISABLED)
        self.calculPoints2()
        time.sleep(0.3)
        self.boutonPrevious.configure(state=tk.ACTIVE)
        self.boutonNext.configure(state=tk.ACTIVE)
        self.bind_all("<Control-Return>",lambda e : self.nextImage())
        self.bind_all("<Control-BackSpace>",lambda e : self.previousImage())

    def help(self):
        """!
        Méthode permettant d'afficher des informations
        """
        message = "PROCEDURE DE SEXAGE DE L'EPINOCHE v2.0"
        message += "\n\n- Modèle de placement de points par traitement d'image et par Machine Learning (learning : 385 individus)"
        message += "\n\n- Modèle de classification Male/Femelle par Machine Learning (learning : 336 individus)"
        message += "\n\n\n Interface développée par R. Masson pour l'INERIS"
        tk.messagebox.showinfo(title="Informations",message=message)

## Lancement global de l'interface
app = MainApp()
app.mainloop()