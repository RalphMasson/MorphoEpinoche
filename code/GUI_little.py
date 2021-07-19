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
import IA_morph as ML
from tkinter import messagebox
from PIL import Image, ImageTk
import math,functools,itertools,os,cv2,webbrowser
import XY_tools,IA_sexage
import numpy as np
from datetime import datetime

# Classe pour les points de la tête

class Temp():
    chemin = ""

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
                label = canvas.create_text((x+15, y+6),text=str(node%25),font=("Purisa", 1),fill='red')
                HeadClass.nodes.append(node)
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
        Interface.afficheLongueur()
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
        Interface.afficheLongueurBody()

    def on_release_tag(self, event, number, tag,canvas1):
        """!
        Methode pour determiner l'item selectionné
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
        self.selected = self.previous_x = self.previous_y = None
        BodyClass.update_points(canvas1)
        Interface.afficheLongueurBody()

    def on_move_node(self, event, number,canvas1):
        """!
        Methode pour deplacer un noeud du graphe
        @param event event : coordonnees de l'item
        @param number int : numero de l'id
        @param tag int : numero de l'id
        """
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
        Interface.afficheLongueurBody()

    def calculDistances():
        """!
        Methode pour calculer certaines distances caractéristiques
        """
        BodyClass.distances_check = XY_tools.Externes.calculDistances2(BodyClass.pointsFish[2:4],BodyClass.pointsFish[0:2])
        return BodyClass.distances_check

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
        ScaleClass.update_points(canvas2)



    def update_points(canvas2):
        """!
        Methode de mise à jour de la position des points
        @param canvas2 tk.Canvas : cadre de l'image
        """
        for id in HeadClass.id_polygons:
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
        # print(self.selected,event,tag)

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
            px50mm = XY_tools.Externes.euclide(Interface.canvasEchelle.coords(3),Interface.canvasEchelle.coords(5))

            if self.selected==5:
                Interface.canvasCorps.move(9,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(BodyClass.nonodes[BodyClass.nodes.index(9)],dx/3,dy/3)
                Interface.canvasCorps.update()
                BodyClass.points[3][0] += dx
                BodyClass.points[3][1] += dy
                coordes = sum(BodyClass.points, [])
                Interface.canvasCorps.coords(BodyClass.polygon, coordes)
                Interface.canvasCorps.update()
                BodyClass.previous_x = event.x
                BodyClass.previous_y = event.y
                BodyClass.update_points(Interface.canvasCorps)
                Interface.afficheLongueur()
                app.labelLongueurBody.config(text="Longueur = "+str(round(Interface.lenBody*50/px50mm,3)))
                Interface.allDist(Interface.lenBody)

            if self.selected==3:
                Interface.canvasCorps.move(7,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(BodyClass.nonodes[BodyClass.nodes.index(7)],dx/3,dy/3)
                Interface.canvasCorps.update()
                BodyClass.points[2][0] += dx
                BodyClass.points[2][1] += dy
                coordes = sum(BodyClass.points, [])
                Interface.canvasCorps.coords(BodyClass.polygon, coordes)
                Interface.canvasCorps.update()
                BodyClass.previous_x = event.x
                BodyClass.previous_y = event.y
                BodyClass.update_points(Interface.canvasCorps)
                Interface.afficheLongueur()
                Interface.allDist(Interface.lenBody)

            app.labelLongueurBody.config(text="Longueur = "+str(round(Interface.lenBody*50/px50mm,3)))
            Interface.allDist(Interface.lenBody)



        ScaleClass.update_points(canvas2)
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

        ScaleClassBody.update_points(canvas3)



    def update_points(canvas3):
        """!
        Methode de mise à jour de la position des points
        @param canvas2 tk.Canvas : cadre de l'image
        """
        for id in HeadClass.id_polygons:
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
                Interface.canvasCorps.move(BodyClass.nonodes[BodyClass.nodes.index(5)],dx/3,dy/3)
                Interface.canvasCorps.update()
                BodyClass.points[1][0] += dx
                BodyClass.points[1][1] += dy
                coordes = sum(BodyClass.points, [])
                Interface.canvasCorps.coords(BodyClass.polygon, coordes)
                Interface.canvasCorps.update()
                BodyClass.previous_x = event.x
                BodyClass.previous_y = event.y
                BodyClass.update_points(Interface.canvasCorps)
                Interface.afficheLongueurBody()

            if self.selected==3:
                Interface.canvasCorps.move(3,dx/3,dy/3)
                Interface.canvasCorps.update()
                Interface.canvasCorps.move(BodyClass.nonodes[BodyClass.nodes.index(3)],dx/3,dy/3)
                Interface.canvasCorps.update()
                BodyClass.points[0][0] += dx
                BodyClass.points[0][1] += dy
                coordes = sum(BodyClass.points, [])
                Interface.canvasCorps.coords(BodyClass.polygon, coordes)
                Interface.canvasCorps.update()
                BodyClass.previous_x = event.x
                BodyClass.previous_y = event.y
                BodyClass.update_points(Interface.canvasCorps)
                Interface.afficheLongueurBody()



        ScaleClassBody.update_points(canvas3)
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
        ScaleClassBody.update_points(canvas3)

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

class ScaleFish():
    poisson = None
    img = None
    def __init__(self, canvas2,PIL_image,size):
        ScaleFish.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        # ScaleFish.poisson = canvas2.create_image(0, 0, anchor=tk.NW, image=ScaleFish.img)
        # Interface.canvasEchelle.itemconfig(ScaleFish.poisson,state='normal')
        # canvas2.move(ScaleFish.poisson,-(ScaleFish.left[0]-25),-(ScaleFish.left[1]-50))

class ScaleFishBody():
    poisson = None
    img = None
    def __init__(self, canvas3,PIL_image,size):
        ScaleFishBody.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        # ScaleFishBody.poisson = canvas3.create_image(0, 0, anchor=tk.NW, image=ScaleFishBody.img)
        # Interface.canvasEchelle2.itemconfig(ScaleFishBody.poisson,state='hidden')
        # Interface.canvasEchelle2.move(ScaleFishBody.poisson,-(ScaleFishBody.left[0]-25),-(ScaleFishBody.left[1]-125))

class Interface(tk.Frame):
    sexModele = None
    app = None
    chemin = ""
    version = 1.6
    def __init__(self, master, **kwargs):
        """!
        Constructeur de l'interface
        """
        tk.Frame.__init__(self)
        self.root = master
        self.add_menu()
        self.canvasGeneral = tk.Canvas(self,width=600,height=700,highlightthickness=0, highlightbackground="black")
        self.frame = tk.Frame(self.canvasGeneral)
        self.frame.pack(fill=tk.BOTH,expand=True)
        self.add_scrollbar()
        self.populate()
        self.createlog()


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
    def populate(self):

        self.listeImages = []
        """Canvas pour logo"""

        pathLogo = Interface.resource_path("logo2.png")
        self.canvasLogo = tk.Canvas(self.frame,bg='#f0f0f0')
        self.canvasLogo.config(width=157,height=84)
        self.imgLogo = ImageTk.PhotoImage(Image.open(pathLogo).resize((157,84)))
        self.canvasLogo.create_image(0, 0, anchor=tk.NW,image=self.imgLogo)

        tk.Label(self.frame,text=" Sexing procedure of three-spined stickleback (mini) \n",font=("Andalus",16,"bold")).pack(padx=5,pady=5)

        ''' Canvas pour le schema '''
        pathSchema = Interface.resource_path("schema.png")
        self.canvasSchema = tk.Canvas(self.frame,bg='#f0f0f0')
        self.canvasSchema.config(width = 288,height=192)

        self.imgSchema = ImageTk.PhotoImage(Image.open(pathSchema).resize((288,192)))
        self.canvasSchema.create_image(0,0,anchor=tk.NW,image=self.imgSchema)

        ''' Boutons '''
        tk.Label(self.frame, text = 'PREDICTION',font=("Purisa",12,"bold"),fg='purple').pack(padx=5,pady=0,anchor=tk.W,fill='x')
        self.boutonImport = tk.Button(self.frame,text = "Import image and autoplace",command = self.importImage,fg='purple')

        self.boutonImport.pack(anchor=tk.W,padx=5,pady=5,ipady=15,expand=True,fill='x')

        self.boutonImport.bind('<Control-o>',self.importImage)
        tk.Button(self.frame,text = "Predict",command = self.Model_Sexage,fg='purple').pack(anchor=tk.W,padx=5,ipady=8,fill='x')
        # tk.Label(self.frame, text = 'ADD THESE VALUES TO MODEL',font=("Purisa",12,"bold"),fg='green').pack(padx=0,pady=0)
        Interface.sexModele = tk.StringVar(self.frame)

        # self.sexModel = tk.Entry(self.frame,width=3,textvariable=Interface.sexModele)
        # self.sexModel.pack(padx=5,pady=5,anchor=tk.N)
        # tk.Button(self.frame,text = "Model Update (close Excel before)",command = HeadClass.genererAllDistancesHead,fg='green').pack(padx=0,pady=0,fill='x')
        self.boutonPrevious = tk.Button(self.frame,text='←',font=("Purisa",13,"bold"),command = self.previousImage)
        self.boutonPrevious.pack(fill='x',ipady=8)
        self.boutonNext = tk.Button(self.frame,text='→',font=("Purisa",13,"bold"),command = self.nextImage)
        self.boutonNext.pack(fill='x',ipady=8)

        self.labelSex = tk.Label(self.frame,text="")
        self.labelSex.pack()

        self.labelInfoPoints = tk.Label(self.frame,text="")


        ''' Canvas pour la tête '''
        self.labelLongueur = tk.Label(self.frame,text="",justify=tk.LEFT)
        Interface.canvasTete = tk.Canvas(self.frame,bg='#f0f0f0',bd=0,highlightthickness=1, highlightbackground="black")
        Interface.canvasTete.config(width=600, height=500)
        Interface.canvasTete.pack()
        self.labelLongueurBody = tk.Label(self.frame,justify=tk.LEFT)

        ''' Canvas pour le corps '''
        Interface.canvasCorps = tk.Canvas(self.frame,bg='#f0f0f0',highlightthickness=1, highlightbackground="black")
        Interface.canvasCorps.config(width=630, height=500)
        Interface.canvasCorps.pack(padx=6)
        self.labelNumImage = tk.Label(self.frame,text="Image :",font=("Purisa",11),fg='gray')
        self.labelNumImage.pack()
        self.labelNomImage = tk.Label(self.frame,text="",font=("Purisa",11),fg='gray')
        self.labelNomImage.pack()


        Interface.canvasEchelle2 = tk.Canvas(self,bg='#f0f0f0')
        Interface.canvasEchelle = tk.Canvas(self,bg='#f0f0f0')


    def allDist(lenBody):
        listepoints = []
        for i in HeadClass.nodes:
            listepoints.append([Interface.canvasTete.coords(i)[0]+3,Interface.canvasTete.coords(i)[1]+3])
        px50mm = XY_tools.Externes.euclide(Interface.canvasEchelle.coords(3),Interface.canvasEchelle.coords(5))

        listedistances2 = []
        print(lenBody)
        print(px50mm)
        listedistances2.append(round(lenBody*50/px50mm,5))
        print(HeadClass.distances_all)

        for x in HeadClass.distances_all:
            listedistances2.append(x)
        Interface.modeleDistances = listedistances2

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvasGeneral.configure(scrollregion=self.canvasGeneral.bbox("all"))
    def add_menu(self):
        self.root.state('zoomed')
        self.root.title("Sex Determination for Three Spined Stickleback")
        menubar = tk.Menu(self.root)
        menuFichier = tk.Menu(menubar,tearoff=0)
        menuFichier.add_command(label="Importer", command=self.importImage,accelerator="(Ctrl+O)")
        self.bind_all("<Control-o>",lambda e : self.importImage())
        menuFichier.add_separator()
        menuFichier.add_command(label="Quitter", command=self.root.destroy,accelerator="(Ctrl+Q)")
        self.bind_all("<Control-q>",lambda e : self.root.destroy())
        menubar.add_cascade(label="Fichier", menu=menuFichier)

        menuOutils = tk.Menu(menubar,tearoff=0)
        menuOutils.add_command(label="Prédire le sexe",command=Interface.affichePrediction,accelerator="(Ctrl+P)")
        self.bind_all("<Control-p>",lambda e : self.Model_Sexage())
        menuOutils.add_command(label="Image suivante",command=self.nextImage,accelerator="(Ctrl+Entrée)")
        self.bind_all("<Control-Return>",lambda e : self.nextImage())
        menuOutils.add_command(label="Image précédente",command=self.previousImage,accelerator="(Ctrl+Backspace)")
        self.bind_all("<Control-BackSpace>",lambda e : self.previousImage())

        menuOutils.add_separator()
        menuOutils.add_command(label="Ouvrir base de données",command=self.openDataBase,accelerator="(Ctrl+H)")
        self.bind_all("<Control-h>",lambda e : self.openDataBase())
        menubar.add_cascade(label="Outils",menu=menuOutils)

        menuAide = tk.Menu(menubar, tearoff=0)
        menuAide.add_command(label="A propos", command=self.help,accelerator="(Ctrl+I)")
        self.bind_all("<Control-i>",lambda e : self.help())
        menuAide.add_command(label="Version",command=Interface.getVersion)
        menubar.add_cascade(label="Aide", menu=menuAide)

        self.root.config(menu=menubar)

    def createlog(self):
        if not os.path.exists(os.getcwd()+"/log"):
            os.mkdir(os.getcwd()+"/log")
            pathname = os.getcwd()+"/log/"
            date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = "rapport" + "_" + date
            f = open(pathname+filename+".txt","w+")
        if os.path.exists(os.getcwd()+"/log"):
            pathname = os.getcwd()+"/log/"
            date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = "rapport" + "_" + date
            self.finalname = pathname+filename+".txt"
            f = open(self.finalname,"w+")
            f.close()

    def verbose_intro(self):
        message = "Rapport généré le "+datetime.now().strftime("%d/%m/%Y")+" à "+datetime.now().strftime("%H:%M:%S")+"\n"
        message += "# Morphométrie Ineris v"+str(Interface.version)+"\n\n"
        message += "# ML_morph version\n"
        message += "\t - Algorithme utilisé : Regression trees (gradient boosting) \n"
        message += "\t - Performances : erreur de placement moyenne de 4 pixels (0.25% de la longueur standard) \n\n"
        message += "# ML_gender version\n"
        message += "\t - Algorithmes utilisés : Gradient Boosting, SVM, Random Forest (consensus) \n"
        message += "\t - Performances : 0.9% \n"

        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_photo(self):
        message = "\n# Photos importées pour la prédiction :\n"
        for x in self.listeImages:
            message += "\t"+x+"\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_points(self,listepoints):
        message = "\n# Coordonnées des points détectés :\n"
        listepoints = listepoints[0]
        for i in range(1,10):
            message += "\t -"
            for j in range(1,len(self.listeImages)+1):
                message += "point n°"+str(i)+": "+"X = "+str(listepoints[i][0])+" Y = " +str(listepoints[i][1])+"\t"
            message += "\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_distances(self,df_distance):
        message = "\n# Distances utilisées pour la prédiction du sexe :\n"
        for j in range(1,len(self.listeImages)+1):
            # message += "distance n°"+str(i)+"= \t\t\t"
            message += df_distance
        message += "\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_sexe(self,text,proba):
        message = "\n# Sexe finalement prédit :\n"
        for i in range(1,len(self.listeImages)+1):
            message += "\t - image n°"+str(i)+": "+text+"  (p="+str(proba)+"....)\n"
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
        message += "\nVersion actuelle : "+"v"+str(Interface.version)
        message += "\nCliquez sur OK pour télécharger"

        reponse = tk.messagebox.askyesnocancel(title="Informations",message=message)
        if(reponse):
            Interface.updateVersion()

    def resource_path(relative_path):
        """!
        Méthode permettant d'avoir le chemin absolu temporaire (pour l'exe) ou normal
        @param relative_path String : chemin du fichier dans le pc
        @return resource_path : chemin temporaire
        """
        try:
            base_path = sys._MEIPASS
            # print(base_path)
        except Exception:
            base_path = pypath2+"/images/"
            base_path = '/'.join(pypath1.split("/")[:-1])+"/images"
            # print(base_path)
            print('/'.join(pypath1.split("/")[:-1])+"/images")
            # print(pypath2)
            # print(pypath3)

        return os.path.join(base_path, relative_path)

    def afficheLongueur():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs dans l'interface
        """
        # app.labelLongueur.config(text=XY_tools.Externes.Longueur(HeadClass.calculDistances()))
        HeadClass.calculDistances()

    def afficheLongueurBody():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs du corps dans l'interface
        """
        # app.labelLongueurBody.config(text=XY_tools.Externes.LongueurBody(BodyClass.calculDistances()))
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
        self.numImageActuelle = 0

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
        self.calculPoints()
        # print("chemin temp")
        # print(Temp.chemin)


    def calculPoints(self):
        """!
        Méthode permettant de calculer les points et de les disposer sur l'image
        """
        # print("\n liste images selectionnées")
        # print(self.listeImages)
        # print("\n image actuelle")
        # print(self.listeImages[self.numImageActuelle])
        # print("\n")
        path_global = '/'.join(self.listeImages[self.numImageActuelle].split('/')[:-1])

        #Points de la tête
        points_tete = self.Model_Tete(self.listeImages[self.numImageActuelle])[0]
        points_tete_copy = points_tete

        #Oeil du poisson
        HeadFish.oeilXY = [0.5*(points_tete_copy[1][0]+points_tete_copy[2][0]),0.5*(points_tete_copy[1][1]+points_tete_copy[2][1])]

        #Points de l'échelle calculés par le modèle 2
        points_echelle = self.Model_Echelle(self.listeImages[self.numImageActuelle])[0]
        points_echelle_copy = points_echelle
        ScaleFish.left = points_echelle[0]

        #Placement des points de l'echelle au bon endroit
        points_echelle = XY_tools.Externes.centerPoints2([points_echelle[0],points_echelle[1]],ScaleFish.left)
        app.labelNomImage.config(text=self.listeImages[self.numImageActuelle])
        app.labelNumImage.config(text=str(self.numImageActuelle+1)+"/"+str(len(self.listeImages)))

        #Image de la tête
        self.ImagePIL = Image.open(self.listeImages[self.numImageActuelle])
        HeadFish(self.canvasTete,self.ImagePIL,cv2.imread(self.listeImages[self.numImageActuelle]),(1920,1440))

        #Image entière
        self.ImagePIL2 = Image.open(self.listeImages[self.numImageActuelle])
        BodyFish(Interface.canvasCorps,self.ImagePIL2,(640,480))

        #Calcul des points du corps
        listePoints3 = self.Model_Longueur(self.listeImages[self.numImageActuelle])[0]
        listePoints3 = [[listePoints3[0][0]/3,listePoints3[0][1]/3],[listePoints3[1][0]/3,listePoints3[1][1]/3]]
        corpsStandard = listePoints3

        #Ajout de l'echelle
        corpsStandard.extend([[points_echelle_copy[0][0]/3,points_echelle_copy[0][1]/3],[points_echelle_copy[1][0]/3,points_echelle_copy[1][1]/3]])

        #Affichage des points sur l'image entière
        BodyClass(Interface.canvasCorps,corpsStandard,'cyan')
        Interface.canvasCorps.update()

        #Affichage des points sur la tête
        pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19,pt21 = points_tete_copy
        points_tete_copy = XY_tools.Externes.centerPoints([pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19,pt21],HeadFish.oeilXY)
        HeadClass.pointsEchelle = points_echelle
        HeadClass(self.canvasTete, points_tete_copy,'#ff00f2')
        self.canvasTete.update()

        #Image de l'échelle
        ImagePIL = Image.open(self.listeImages[self.numImageActuelle])
        tete2 = points_tete
        ScaleFish(Interface.canvasEchelle,ImagePIL,(1920,1440))
        ScaleClass(Interface.canvasEchelle,points_echelle,'#ffffff')

        # Calcul des points  du corps Bis
        points_longueur = self.Model_Longueur('/'.join(self.listeImages[0].split('/')[:-1]))[0]
        pt1,pt2 = [points_longueur[0][0],points_longueur[0][1]],[points_longueur[1][0],points_longueur[1][1]]
        ScaleFishBody.left = [points_longueur[0][0],points_longueur[0][1]]
        points_longueur = XY_tools.Externes.centerPoints3([pt1,pt2],ScaleFishBody.left)

        # Image du corps
        ImagePIL = Image.open(self.listeImages[self.numImageActuelle])
        ScaleFishBody(Interface.canvasEchelle2,ImagePIL,(1920,1440))
        ScaleClassBody(Interface.canvasEchelle2,points_longueur,'#ffffff')

    def Model_Tete(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        print("points tête")
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_head.dat')
        except:
            pathPredictor = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\predictor_head.dat'
        try:
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
        except:
            a = ModelPoints(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\',"")
        # print("load ok")
        try:
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_head.dat")
        except:
            a.predict(pathimage,Temp.ppath2+"\models\\","predictor_head.dat")

        # print("predict ok")
        # print(Temp.chemin)
        try:
            listepoints = ML.ML_pointage.xmltolistY(Temp.ppath2+"\models\\"+"output.xml",0)
        except:
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)
        self.verbose_points(listepoints)
        return listepoints

    def Model_Echelle(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        print("points echelle")
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_scale2.dat')
        except:
            pathPredictor = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\predictor_scale2.dat'

        try:
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
        except:
            a = ModelPoints(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\',"")

        try:
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_scale2.dat")
        except:
            a.predict(pathimage,Temp.ppath2+"\models\\","predictor_scale2.dat")

        try:
            listepoints = ML.ML_pointage.xmltolistY(Temp.ppath2+"\models\\"+"output.xml",0)
        except:
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)

        return listepoints


    def Model_Longueur(self,pathimage):
        print("points longueur")
        try:
            pathPredictor = os.path.join(sys._MEIPASS, 'predictor_LS.dat')
        except:
            pathPredictor = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\predictor_LS.dat'
        try:
            a = ModelPoints(os.path.join(sys._MEIPASS,''),"")
        except:
            a = ModelPoints(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\\',"")
        try:
            a.predict(pathimage,os.path.join(sys._MEIPASS,''),"predictor_LS.dat")
        except:
            a.predict(pathimage,Temp.ppath2+"\models\\","predictor_LS.dat")

        try:
            listepoints = ML.ML_pointage.xmltolistY(Temp.ppath2+"\models\\"+"output.xml",0)
        except:
            listepoints = ML.ML_pointage.xmltolistY(os.path.join(sys._MEIPASS,"output.xml"),0)
        return listepoints


    def Model_Sexage(self):
        print("classification")
        Interface.lenBody = XY_tools.Externes.euclide(Interface.canvasEchelle2.coords(3),Interface.canvasEchelle2.coords(5))
        Interface.allDist(Interface.lenBody)
        from joblib import dump, load
        import pandas as pd
        try:
            clf = load(os.path.join(sys._MEIPASS,"GBClassifierFinal.joblib"))
            clf1 = load(os.path.join(sys._MEIPASS,"SVCClassifierFinal.joblib"))
            clf2 = load(os.path.join(sys._MEIPASS,"XGBClassifierFinal.joblib"))
        except:
            clf = load(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\GBClassifierFinal.joblib')
            clf1 = load(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\SVCClassifierFinal.joblib')
            clf2 = load(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\XGBClassifierFinal.joblib')

        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', None)
        ae = pd.DataFrame(Interface.modeleDistances).T

        # print(ae)
        prediction = clf.predict(ae)
        prediction1 = clf1.predict(ae)
        prediction2 = clf2.predict(ae)


        ## Consensus
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
        app.labelSex.config(text = text)

        self.verbose_distances(str(ae))
        self.verbose_sexe(text,proba)
        self.verbose_conclusion()


    def affichePrediction():
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
        print("toto")
        print('/'.join(inspect.getfile(lambda: None).split('\\')[:-2])+"/executable/DistancesPourModele.csv")
        print(pypath3+"\DistancesPourModele.csv")
        print(Temp.chemin+"/DistancesPourModele.csv")
        if(os.path.exists('/'.join(inspect.getfile(lambda: None).split('\\')[:-2])+"/executable/DistancesPourModele.csv")):
            try:
                subprocess.Popen('/'.join(inspect.getfile(lambda: None).split('\\')[:-2])+"/executable/DistancesPourModele.csv",shell=True)
            except:
                commande = "start notepad.EXE "
                commande += pypath3+"/DistancesPourModele.csv"
                os.system(commande)

        elif(os.path.exists(Temp.chemin+"/DistancesPourModele.csv")):
            try:
                subprocess.Popen(Temp.chemin+"/DistancesPourModele.csv",shell=True)
            except:
                commande = "start notepad.EXE "
                commande += os.getcwd()+"\DistancesPourModele.csv"
                os.system(commande)

        elif(os.path.exists(os.getcwd()+"\DistancesPourModele.csv")):
            try:
                subprocess.Popen(os.getcwd()+"\DistancesPourModele.csv",shell=True)
            except:
                None

        else:
            message = "La base de données n'a pas été trouvée"
            message += "\n\n1) Vérifier qu'elle est située ici : "
            message += "\n"+pypath3+"/DistancesPourModele.csv"
            test = os.getcwd()
            test2 = inspect.getfile(lambda: None)
            message += "\n"+test
            message += "\n"+'/'.join(test2.split('\\')[:-2])+"executable/DistancesPourModele.csv"
            message += "\n\n2) Commencer par créer une base de données"
            # message += "\n"+str(len(test))
            # message += "\n"+str(len('/'.join(test2.split('\\')[:-1])))
            tk.messagebox.showwarning(title="Attention", message=message)

    def help(self):
        """!
        Méthode permettant d'afficher des informations
        """
        message = "PROCEDURE DE SEXAGE DE L'EPINOCHE v1.6"
        message += "\n\n- Modèle de placement de points par traitement d'image et par Machine Learning (learning : 150 individus)"
        message += "\n\n- Modèle de classification Male/Femelle par Machine Learning (learning : 300 individus)"
        message += "\n\n\n Interface développée par R. Masson pour l'INERIS"
        tk.messagebox.showinfo(title="Informations",message=message)


# root = tk.Tk()
# app = Interface(root)
# app.pack(side="top", fill="both", expand=True)
# app.mainloop()