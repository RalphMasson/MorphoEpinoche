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
from tkinter import messagebox
from PIL import Image, ImageTk
import math,functools,itertools,os,cv2,webbrowser,random,string
import XY_compute,XY_tools,IA_sexage,GUI_little,GUI_update
import IA_morph as ML
from datetime import datetime
import numpy as np

# Classe pour les points de la tête
class HeadClass():
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
    def __init__(self, canvas, points,color):
        """!
        Constructeur du polygone de la tête
        @param canvas tk.Canvas : cadre de l'image
        @param points list : liste des points du polygone
        @param color String : couleur du polygone
        """
        self.previous_x = self.previous_y = self.selected = self.x = None
        self.points = points
        listenode = [i for i in range(1,13)]
        num = 0
        if points!=None:
            if color=='red':outline='red'
            else: outline=''
            # print(points)

            self.polygon = canvas.create_polygon(self.points,fill='',outline=outline,smooth=0,width=2,dash=(1,))
            HeadClass.id_polygons.append(self.polygon)
            # print(self.polygon)
            canvas.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag,canvas))
            canvas.tag_bind(self.polygon, '<B1-Motion>', lambda event = self.polygon : self.on_move_polygon(event,canvas))
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

        # print(HeadClass.id_polygons)
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
            # print(liste)
            # print(len(liste))
            if(len(canvas.coords(id))==20):HeadClass.pointsFish=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            # if(len(canvas.coords(id))==4):HeadClass.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

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
                    pt13_calcul = XY_tools.Externes.decenterPoint(pt13_image,HeadFish.centreOeil)
                    pt15_calcul = XY_tools.Externes.decenterPoint(pt15_image,HeadFish.centreOeil)
                    pt17,pt11 = XY_compute.Points.points11_17(HeadFish.CV2_image_big,pt13_calcul,pt15_calcul)
                    pt11_old = [canvas.coords(id11)[0]+3,canvas.coords(id11)[1]+3]
                    pt17_old = [canvas.coords(id17)[0]+3,canvas.coords(id17)[1]+3]
                    pt11,pt17 = XY_tools.Externes.centerPoints([pt11,pt17],HeadFish.centreOeil)
                    canvas.move(id11,pt11[0]-pt11_old[0],pt11[1]-pt11_old[1])
                    canvas.move(id17,pt17[0]-pt17_old[0],pt17[1]-pt17_old[1])
                    canvas.update()
            except:
                None


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
        """!
        Methode pour calculer toutes les distances de la tete
        """
        XY_tools.Externes.genererAllDistancesHead(HeadClass.pointsEchelle,HeadClass.pointsFish,Interface.sexModele.get(),pypath3)

    def calculDistances():
        """!
        Methode pour calculer certaines distances caractéristiques
        """
        # print("points echelle")
        # print(HeadClass.pointsEchelle)
        # print(HeadClass.pointsFish)
        HeadClass.distances_check = XY_tools.Externes.calculDistances(HeadClass.pointsEchelle,HeadClass.pointsFish)
        return HeadClass.distances_check


class BodyClass():
    """Variables globales pour export
    id_polygons : liste des id des polygons (le corps et l'echelle)
    pointsFish : liste des points du corps [(x1,y1),(x2,y2)...]
    pointsEchelle : liste des points de l'echelle [(x1,y1),(x2,y2)]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    """

    id_polygons = []
    pointsFish = []
    pointsEchelle = []
    distances_all = []
    distances_check = []

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
        @param canvas1 tk.Canvas : cadre de l'image
        """
        for id in BodyClass.id_polygons:
            liste = canvas1.coords(id)
            if(len(canvas1.coords(id))==8):BodyClass.pointsFish=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            # if(len(canvas1.coords(id))==4):BodyClass.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]


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
        print(number)
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
        # print("test test")
        # print(BodyClass.pointsEchelle)
        # print(BodyClass.pointsFish)
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
            # print(points)

            self.polygon = canvas2.create_polygon(self.points,fill='',outline=outline,smooth=0,width=2,dash=(1,))
            HeadClass.id_polygons.append(self.polygon)
            # print(self.polygon)
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

        # print(HeadClass.id_polygons)
        ScaleClass.update_points(canvas2)



    def update_points(canvas2):
        """!
        Methode de mise à jour de la position des points
        @param canvas2 tk.Canvas : cadre de l'image
        """
        for id in HeadClass.id_polygons:
            liste = canvas2.coords(id)
            print(liste)
            # print(len(liste))
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
            # print(self.selected)
            canvas2.move(self.nonodes[self.nodes.index(self.selected)],dx,dy)
            self.points[number][0] += dx
            self.points[number][1] += dy
            coords = sum(self.points, [])
            canvas2.coords(self.polygon, coords)
            # print(canvas2.coords(self.selected))
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
                    pt13_image = [canvas2.coords(id13)[0]+3,canvas2.coords(id13)[1]+3]
                    pt15_image = [canvas2.coords(id15)[0]+3,canvas2.coords(id15)[1]+3]
                    pt13_calcul = XY_tools.Externes.decenterPoint(pt13_image,HeadFish.centreOeil)
                    pt15_calcul = XY_tools.Externes.decenterPoint(pt15_image,HeadFish.centreOeil)
                    pt17,pt11 = XY_compute.Points.points11_17(HeadFish.CV2_image_big,pt13_calcul,pt15_calcul)
                    pt11_old = [canvas2.coords(id11)[0]+3,canvas2.coords(id11)[1]+3]
                    pt17_old = [canvas2.coords(id17)[0]+3,canvas2.coords(id17)[1]+3]
                    pt11,pt17 = XY_tools.Externes.centerPoints([pt11,pt17],HeadFish.centreOeil)
                    canvas2.move(id11,pt11[0]-pt11_old[0],pt11[1]-pt11_old[1])
                    canvas2.move(id17,pt17[0]-pt17_old[0],pt17[1]-pt17_old[1])
                    canvas2.update()
            except:
                None


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
        """!
        Constructeur de l'image de la tete
        @param canvas tk.Canvas : cadre de l'image
        @param PIL_image list : matrice de l'image format PIL
        @param cv2_image list : matrice de l'image format cv2
        @param size list : dimension souhaitée de l'image
        """
        self.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        # self.circle = XY_compute.Points.detect_eye(cv2.resize(CV2_image,size,Image.ANTIALIAS))
        # HeadFish.centreOeil = [self.circle[0],self.circle[1]]
        HeadFish.poisson = canvas.create_image(0, 0, anchor=tk.NW,image=self.img)
        HeadFish.CV2_image_big = CV2_image
        canvas.move(HeadFish.poisson,-(HeadFish.oeilXY[0]-200),-(HeadFish.oeilXY[1]-200))
        app.bind("<Left>",self.moveLeft)
        app.bind("<Right>",self.moveRight)
        app.bind("<Up>",self.moveUp)
        app.bind("<Down>",self.moveDown)
    def moveLeft(self,event):
        """!
        Méthode pour déplacer l'image à gauche
        @param event : event
        """
        Interface.canvasTete.move(HeadFish.poisson,10,0)
    def moveRight(self,event):
        """!
        Méthode pour déplacer l'image à droite
        @param event : event
        """
        Interface.canvasTete.move(HeadFish.poisson,-10,0)
    def moveUp(self,event):
        """!
        Méthode pour déplacer l'image en haut
        @param event : event
        """
        Interface.canvasTete.move(HeadFish.poisson,0,-10)
    def moveDown(self,event):
        """!
        Méthode pour déplacer l'image en bas
        @param event : event
        """
        Interface.canvasTete.move(HeadFish.poisson,0,10)

class BodyFish():
    poisson = None
    def __init__(self, canvas1,PIL_image,size):
        """!
        Constructeur de l'image du corps
        @param canvas tk.Canvas : cadre de l'image
        @param PIL_image list : matrice de l'image format PIL
        @param cv2_image list : matrice de l'image format cv2
        @param size list : dimension souhaitée de l'image
        """
        self.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        BodyFish.poisson = canvas1.create_image(0, 0, anchor=tk.NW, image=self.img)
        # canvas1.move(BodyFish.poisson,-(HeadFish.oeilXY[0]-150),-(HeadFish.oeilXY[1]-250))
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
    def move(self,event):
        """!
        Méthode pour déplacer l'image
        @param event : touche pressée
        """
        if event.char=='q':
            canvas1.move(BodyFish.poisson,-10,0)
        if event.char=='s':
            canvas1.move(BodyFish.poisson,10,0)
        if event.char =='z':
            canvas1.move(BodyFish.poisson,0,-10)

class ScaleFish():
    poisson = None
    def __init__(self, canvas2,PIL_image,size):
        """!
        Constructeur de l'image du corps
        @param canvas tk.Canvas : cadre de l'image
        @param PIL_image list : matrice de l'image format PIL
        @param cv2_image list : matrice de l'image format cv2
        @param size list : dimension souhaitée de l'image
        """
        self.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        ScaleFish.poisson = canvas2.create_image(0, 0, anchor=tk.NW, image=self.img)
        Interface.canvasEchelle.itemconfig(ScaleFish.poisson,state='hidden')
        canvas2.move(ScaleFish.poisson,-(ScaleFish.left[0]-25),-(ScaleFish.left[1]-50))
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
        app.bind("<Key>",self.move)
    def move(self,event):
        """!
        Méthode pour déplacer l'image
        @param event : touche pressée
        """
        if event.char=='q':
            canvas1.move(BodyFish.poisson,-10,0)
        if event.char=='s':
            canvas1.move(BodyFish.poisson,10,0)
        if event.char =='z':
            canvas1.move(BodyFish.poisson,0,-10)

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
        self.pointsML = [[0,0]]*10
        ModelPoints.pointsML = ML.ML_pointage(aa,bb)

    def instantiate(self):
        """!
            Créer le modèle
        """

        ModelPoints.path_xml = r"C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho/test_pointage_ML/v2/train.xml"
        # try:
        #     ModelPoints.path_xml = os.path.join(sys._MEIPASS,ModelPoints.path_xml)
        # except Exception:
        #     ModelPoints.path_xml = r"C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho/test_pointage_ML/v2/train.xml"
        #
        # ModelPoints.liste = ML.ML_pointage.xmltolist(ModelPoints.path_xml,0)
        # print(ModelPoints.liste)

    def predict(self,aa,bb):
        ModelPoints.pointsML.predict(aa,bb)



class Interface(tk.Tk):
    sexModele = None
    version = 1.6
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
        self.add_entrys()

        self.createlog()
        self.verbose_intro()

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
        message += "\t - Algorithme utilisé : \n"
        message += "\t - Performances : \n\n"
        message += "# ML_gender version\n"
        message += "\t - Algorithmes utilisés : \n"
        message += "\t - Performances : \n"

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

    def verbose_points(self):
        message = "\n# Coordonnées des points détectés :\n"
        for i in range(1,10):
            message += "\t -"
            for j in range(1,len(self.listeImages)+1):
                message += "point n°"+str(i)+": X = ... Y = ... \t"
            message += "\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_distances(self):
        message = "\n# Distances utilisées pour la prédiction du sexe :\n"
        for i in range(1,10):
            message += "\t -"
            for j in range(1,len(self.listeImages)+1):
                message += "distance n°"+str(i)+"= \t\t\t"
            message += "\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_sexe(self):
        message = "\n# Sexe finalement prédit :\n"
        for i in range(1,len(self.listeImages)+1):
            message += "\t - image n°"+str(i)+" :  (p=....)\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def verbose_conclusion(self):
        message = "\nFIN \n"
        message += datetime.now().strftime("%d/%m/%Y")+" à "+datetime.now().strftime("%H:%M:%S")+"\n"
        f = open(self.finalname,"a")
        f.write(message)
        f.close()

    def loadModel(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        a = ModelPoints(r"C:\Users\MASSON\Desktop\POINTAGe\\","")
        a.predict(pathimage,r"C:\Users\MASSON\Desktop\POINTAGe\predictor.dat")
        listepoints = ML.ML_pointage.xmltolistY(r"C:\Users\MASSON\Desktop\POINTAGe\output.xml",1)
        return listepoints

    def loadModel2(self,pathimage):
        """!
            @param pathimage dossier de l'image
        """
        a = ModelPoints(r"C:\Users\MASSON\Desktop\pointageEchelle\\","")
        a.predict(pathimage,r"C:\Users\MASSON\Desktop\pointageEchelle\predictor.dat")
        listepoints = ML.ML_pointage.xmltolistY(r"C:\Users\MASSON\Desktop\pointageEchelle\output.xml",1)
        return listepoints

        print(listepoints)

    def add_entrys(self):

        Interface.sexModele = tk.StringVar(self)
        self.sexModel = tk.Entry(self,width=3,textvariable=Interface.sexModele)
        self.sexModel.place(relx=0.52,rely=0.125)


    def add_canvas(self):
        ''' Canvas pour la tête '''
        Interface.canvasTete = tk.Canvas(self,bg='#f0f0f0',bd=0,highlightthickness=1, highlightbackground="black")
        Interface.canvasTete.config(width=450, height=400)
        Interface.canvasTete.grid(column=0,row=8)

        ''' Canvas pour le corps '''
        self.canvasCorps = tk.Canvas(self,bg='#f0f0f0',highlightthickness=1, highlightbackground="black")
        self.canvasCorps.config(width=630, height=400)
        self.canvasCorps.grid(column=1,row=8)

        Interface.canvasEchelle = tk.Canvas(self,bg='#f0f0f0')
        Interface.canvasEchelle.config(width=1590, height=160)
        Interface.canvasEchelle.place(relx=0,rely=0.80)

        """Canvas pour logo"""
        pathLogo = XY_tools.Externes.resource_path("logo2.png")
        self.canvasLogo = tk.Canvas(self,bg='#f0f0f0')
        self.canvasLogo.config(width=157,height=84)
        self.canvasLogo.place(x=0,y=0)
        self.imgLogo = ImageTk.PhotoImage(Image.open(pathLogo).resize((157,84)))
        self.canvasLogo.create_image(0, 0, anchor=tk.NW,image=self.imgLogo)

        ''' Canvas pour le schema '''
        pathSchema = XY_tools.Externes.resource_path("schema.png")
        self.canvasSchema = tk.Canvas(self,bg='#f0f0f0')
        self.canvasSchema.config(width = 288,height=192)
        self.canvasSchema.place(x=1250,y=0)
        self.imgSchema = ImageTk.PhotoImage(Image.open(pathSchema).resize((288,192)))
        self.canvasSchema.create_image(0,0,anchor=tk.NW,image=self.imgSchema)


    def add_buttons(self):
        self.boutonImport = tk.Button(self,text = "Import images",command = self.importImage,fg='purple')
        self.boutonImport.place(relx=0.25,rely=0.12)
        self.boutonImport.bind('<Control-o>',self.importImage)
        tk.Button(self,text = "Predict",command = self.affichePrediction,fg='purple').place(relx=0.25,rely=0.155)
        tk.Button(self,text = "Model Update (close Excel before)",command = HeadClass.genererAllDistancesHead,fg='green').place(relx=0.46,rely=0.158)
        self.boutonPrevious = tk.Button(self,text='<--',fg='red',command = self.previousImage)
        self.boutonPrevious.place(relx=0.38,rely=0.3)
        self.boutonNext = tk.Button(self,text='-->',fg='red',command = self.nextImage)
        self.boutonNext.place(relx=0.40,rely=0.3)

        self.buttonScale = tk.Button(self,text="Affiche scale",command = self.afficheScale).place(relx = 0.7,rely=0.6)
        self.buttonScale = tk.Button(self,text="Hide scale",command = self.hideScale).place(relx = 0.76,rely=0.6)

    def afficheScale(self):
        Interface.canvasEchelle.itemconfig(ScaleFish.poisson,state='normal')

    def hideScale(self):
        Interface.canvasEchelle.itemconfig(ScaleFish.poisson,state='hidden')



    def add_labels(self):
        ''' Label Intro de presentation'''
        tk.Label(self, text = 'PREDICTION',font=("Purisa",12,"bold"),fg='purple').place(relx=0.25,rely=0.08)
        tk.Label(self,text=" ",font=("Purisa",12,"bold")).grid(ipadx=2)
        tk.Label(self,text=" Sexing procedure of three-spined stickleback \n",font=("Andalus",16,"bold")).place(relx=0.35,rely=0.01)
        tk.Label(self,text="\n \n \n \n ").grid(column=0,row=1)
        tk.Label(self, text = 'ADD THESE VALUES TO MODEL',font=("Purisa",12,"bold"),fg='green').place(relx=0.46,rely=0.08)
        tk.Label(self,text='Sex for model:',fg='green').place(relx=0.46,rely=0.125)
        self.labelSex = tk.Label(self,text="")
        self.labelSex.place(x=650,y=190)


        self.labelInfoPoints = tk.Label(self,text="",font=("Purisa",11),fg='gray')
        self.labelInfoPoints.place(relx=0.1,rely=0.975)

        self.labelVide = tk.Label(self,text="\n\n ")
        self.labelVide.grid(column=0,row=3)

        self.labelNumImage = tk.Label(self,text="",font=("Purisa",11),fg='gray')
        self.labelNumImage.place(relx=0.35,rely=0.975)
        self.labelNomImage = tk.Label(self,text="",font=("Purisa",11),fg='gray')
        self.labelNomImage.place(relx=0.4,rely=0.975)

        ''' Labels pour les longueurs de la tête '''
        # tk.Label(self,text="Longueurs caractéristiques de la tête : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=2,row=4)
        tk.Label(self,text="Longueurs caractéristiques de la tête : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).place(relx=.7,rely=.38)
        tk.Label(self,text="\n\n\n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=2,row=4)

        self.labelLongueur = tk.Label(self,text="",justify=tk.LEFT)
        # self.labelLongueur.grid(column=2,row=5)
        self.labelLongueur.place(relx=0.7,rely=0.42)

        ''' Labels pour les longueurs du corps '''
        # tk.Label(self,text="Longueurs caractéristiques du corps : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=2,row=6)
        tk.Label(self,text="Longueurs caractéristiques du corps : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).place(relx=.7,rely=.25)

        self.labelLongueurBody = tk.Label(self,text="",justify=tk.LEFT)
        # self.labelLongueurBody.grid(column=2,row=7)
        self.labelLongueurBody.place(relx = .7,rely=.3)


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
        menuOutils.add_command(label="Prédire le sexe",command=Interface.affichePrediction,accelerator="(Ctrl+P)")
        self.bind_all("<Control-p>",lambda e : Interface.affichePrediction())
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
        self.destroy()
        # self.withdraw()
        root = tk.Tk()

        GUI_little.app = GUI_little.Interface(root)
        GUI_little.app.pack(side="top", fill="both", expand=True)
        GUI_little.app.mainloop()

        # self.deiconify()

    def updatePointModel(self):
        # self.destroy()
        # self.withdraw()
        GUI_update.InterfacePoint()
        # self.deiconify()

    def updatePointModel1(self):
        # self.destroy()
        # self.withdraw()
        GUI_update.InterfaceGender()
        # self.deiconify()

    def afficheLongueur():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs dans l'interface
        """
        app.labelLongueur.config(text=XY_tools.Externes.Longueur(HeadClass.calculDistances()))

    def afficheLongueurBody():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs du corps dans l'interface
        """
        app.labelLongueurBody.config(text=XY_tools.Externes.LongueurBody(BodyClass.calculDistances()))

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


    def importImage(self,event=' '):
        """!
        Méthode permettant de charger 1 ou plusieurs images
        """
        self.choice = 0
        self.resetListeImages()
        self.listeImages = XY_tools.Externes.openfn()
        self.verbose_photo()
        self.verbose_points()
        self.verbose_distances()
        self.verbose_sexe()
        self.verbose_conclusion()
        self.calculPoints()

    def calculPoints(self):
        """!
        Méthode permettant de calculer les points et de les disposer sur l'image
        """

        print(self.listeImages)
        listePoints = self.loadModel('/'.join(self.listeImages[0].split('/')[:-1]))[0]
        print(listePoints)

        tete = listePoints
        HeadFish.oeilXY = [0.5*(tete[1][0]+tete[2][0]),0.5*(tete[1][1]+tete[2][1])]

        listePoints2 = self.loadModel2('/'.join(self.listeImages[0].split('/')[:-1]))[0]
        listePoints22 = listePoints2
        ScaleFish.left = listePoints2[0]
        print(ScaleFish.left)
        print("Echelle")
        print(listePoints2)
        pt1,pt2 = listePoints2
        listePoints2 = XY_tools.Externes.centerPoints2([pt1,pt2],ScaleFish.left)




        ImagePIL = Image.open(self.listeImages[self.numImageActuelle])
        app.labelNomImage.config(text=self.listeImages[self.numImageActuelle])
        app.labelNumImage.config(text=str(self.numImageActuelle+1)+"/"+str(len(self.listeImages)))
        # 605,487
        BodyFish(self.canvasCorps,ImagePIL,(640,480))
        self.canvasTete.update()

        # echelle3mm = [[80,80],[90,90]]
        HeadFish(self.canvasTete,ImagePIL,cv2.imread(self.listeImages[self.numImageActuelle]),(1920,1440))

        corpsStandard = [[80,80],[81,81]]
        echelle10mm = [[20,30],[30,50]]
        # BodyClass(self.canvasCorps, echelle10mm,'red')
        # BodyClass.pointsEchelle = [[listePoints2[0][0]/2,listePoints2[0][1]/2],[listePoints2[1][0]/2,listePoints2[1][1]/2]]
        corpsStandard.extend([[listePoints22[0][0]/3,listePoints22[0][1]/3],[listePoints22[1][0]/3,listePoints22[1][1]/3]])
        BodyClass(self.canvasCorps,corpsStandard,'cyan')
        print("echelle body")
        print(BodyClass.pointsEchelle)
        print("point body")
        print(BodyClass.pointsFish)
        self.canvasCorps.update()
        pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19,pt21 = tete


        tete = XY_tools.Externes.centerPoints([pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19,pt21],HeadFish.oeilXY)
        HeadClass.pointsEchelle = listePoints2
        HeadClass(self.canvasTete, tete,'#ff00f2')


        # HeadClass(self.canvasTete,echelle3mm,'red')
        self.canvasTete.update()
        ImagePIL = Image.open(self.listeImages[self.numImageActuelle])
        tete2 = listePoints



        ScaleFish(Interface.canvasEchelle,ImagePIL,(1920,1440))
        ScaleClass(Interface.canvasEchelle,listePoints2,'#ffffff')
        # ScaleClass(self.canvasEchelle,echelle3mm2,'#ff00f2')


    def affichePrediction(self):
        """!
        Méthode permettant d'afficher la prédiction du sexe
        """
        choix,couleur,p = IA_sexage.Prediction.predict(None,"","")
        app.labelSex.config(text="")
        app.labelSex.config(text=choix+" avec p="+str(round(p,2)),font=("Purisa",16),fg=couleur)
        print("toto")
        print(Interface.canvasEchelle.itemcget(ScaleFish.poisson,'state'))


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
        message = "PROCEDURE DE SEXAGE DE L'EPINOCHE v1.6"
        message += "\n\n- Modèle de placement de points par traitement d'image et par Machine Learning (learning : 150 individus)"
        message += "\n\n- Modèle de classification Male/Femelle par Machine Learning (learning : 300 individus)"
        message += "\n\n\n Interface développée par R. Masson pour l'INERIS"
        tk.messagebox.showinfo(title="Informations",message=message)




app = Interface()
app.mainloop()



