import tkinter as tk
from PIL import Image, ImageTk
import os,glob,cv2
import numpy as np
# path = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATABASE_rotation\\"
# pathFinal = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATABASE_schema\\"
#
# listImg = glob.glob(path+"**\\*.JPG",recursive=True)
import sys
sys.path.insert(0, 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho')
import ArchitectureFondBlanc
# import MorphoPolygon,MorphoImage
# from MorphoPolygon import HeadClass,BodyClass
# from MorphoImage import HeadFish,BodyFish

class HeadClass():
    ''' class Item pour la tete du poisson'''
    ''' Variables globales pour export '''
    ''' nodes1 : noeuds du polygone convexe de la tête et de l'echelle '''
    ''' poly1 : liste de tous les points '''
    ''' pointsTete : liste des points de la tête [(x1,y1),(x2,y2)...]'''
    ''' pointsEchelle3mm : liste des points de l'echelle [(x1,y1),(x2,y2)]'''
    ''' distance : liste des distances calculées entre les points'''
    ''' angles : liste des angles calculées entre les points'''

    nodes1 = []
    poly1 = []
    pointsTete = []
    pointsEchelle3mm = []
    distance = [0 for _ in range(20)]
    alldistancesHead=[]
    angles = [0 for _ in range(20)]
    points=None

    def __init__(self, canvas, points,color):
        self.previous_x = None
        self.previous_y = None
        self.selected = None
        self.listPoly = [2,21]
        self.NomsPoly = ["tete","echelle",]
        self.points = points
        self.x = None
        if points!=None:
            self.polygon = canvas.create_polygon(self.points,fill='',outline=color,smooth=0,width=6,dash=(1,5))

            # print(self.polygon)
            # print("test")
            HeadClass.poly1.append(self.polygon)
            # print(HeadClass.poly1)
            # print("test")
            canvas.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag))
            canvas.tag_bind(self.polygon, '<B1-Motion>', self.on_move_polygon)

            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                # print(node)
                label = canvas.create_text((x+15, y+6),text=str(node%25),font=("Purisa", 12),fill='yellow')
                self.nodes.append(node)
                self.nonodes.append(label)
                HeadClass.nodes1.append(node)
                canvas.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag))
                canvas.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number))

        print(self.nodes)
        for x,y in zip(HeadClass.poly1,self.NomsPoly):
            # print(y)
            # print(canvas.coords(x))
            # print("\n")
            liste = canvas.coords(x)
            # print("longueur"+str(len(canvas.coords(x))))
            if(len(canvas.coords(x))==18):HeadClass.pointsTete=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas.coords(x))==4):HeadClass.pointsEchelle3mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
        # print(HeadClass.pointsEchelle3mm)
        # print(HeadClass.pointsTete)
        if(len(HeadClass.pointsEchelle3mm)>0):
             afficheLongueur()

    def on_press_tag(self, event, number, tag):
        self.selected = tag
        self.previous_x = event.x
        self.previous_y = event.y
        print(self.selected,event,tag)
    def on_release_tag(self, event, number, tag):
        self.selected = None
        self.previous_x = None
        self.previous_y = None

        for x,y in zip(HeadClass.poly1,self.NomsPoly):
            # print(canvas.coords(x))
            liste = canvas.coords(x)
            if(len(canvas.coords(x))==18):HeadClass.pointsTete=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas.coords(x))==4):HeadClass.pointsEchelle3mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

    def on_move_node(self, event, number):
        '''move single node in polygon'''
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            # print(number)
            canvas.move(self.selected, dx, dy)
            canvas.move(self.nonodes[self.nodes.index(self.selected)],dx,dy)
            self.points[number][0] += dx
            self.points[number][1] += dy
            coords = sum(self.points, [])
            canvas.coords(self.polygon, coords)
            self.previous_x = event.x
            self.previous_y = event.y

        for x,y in zip(HeadClass.poly1,self.NomsPoly):
            liste = canvas.coords(x)
            if(len(canvas.coords(x))==18):HeadClass.pointsTete=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas.coords(x))==4):HeadClass.pointsEchelle3mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
        afficheLongueur()
    def on_move_polygon(self, event):
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
        for x,y in zip(HeadClass.poly1,self.NomsPoly):
            # print(list(zip(self.listPoly,self.NomsPoly)))
            liste = canvas.coords(x)
            if(len(canvas.coords(x))==18):HeadClass.pointsTete=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas.coords(x))==4):HeadClass.pointsEchelle3mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
    def hide_nodes():
        for node in HeadClass.nodes1:
            canvas.itemconfig(node,fill="",outline='')
        for poly in HeadClass.poly1:
            canvas.itemconfig(poly,dash=())
    def euclideDist(a,b):
        import numpy as np
        x1 = a[0]
        y1 = a[1]
        x2 = b[0]
        y2 = b[1]
        norme = np.sqrt((x2-x1)**2+(y2-y1)**2)
        return norme

    def calculAngle(pt1,pt2,pt3):
        #calcul par alkashi des angles en degres du triangle reliant les 3 points
        #        pt2
        #     b /     \ a
        #  pt1 ----- pt3
        #         c
        #angle au niveau du pt1

        b = HeadClass.euclideDist(pt1,pt2)
        a = HeadClass.euclideDist(pt2,pt3)
        c = HeadClass.euclideDist(pt1,pt3)

        from math import acos,pi

        Apt1 = acos((b**2+c**2-a**2)/(2*b*c))*180/pi
        Apt2 = acos((b**2+a**2-c**2)/(2*b*a))*180/pi
        Apt3 = acos((a**2+c**2-b**2)/(2*a*c))*180/pi

        listeAngle = [Apt1,Apt2,Apt3]
        return listeAngle





    def genererAllDistancesHead():
        from itertools import combinations,permutations,combinations_with_replacement
        atest = list(combinations([i for i in range(9)],3))
        from functools import partial
        listeCombinaisonsAngle = []
        def reorder_from_idx(idx, a):
            return a[idx:] + a[:idx]
        def cyclic_perm(a):
            return [partial(reorder_from_idx, i) for i in range(len(a))]
        for a in atest:
            result = cyclic_perm(a)
            # print("toto"+str(a))
            for x in range(len(a)):
                listeCombinaisonsAngle.append(result[x](a))



        from itertools import combinations
        pt22 = HeadClass.pointsEchelle3mm[0]
        pt24 = HeadClass.pointsEchelle3mm[1]
        echelle3mm_px = HeadClass.euclideDist(pt22,pt24)
        listeCombinaisonsDistance = list(combinations([i for i in range(9)],2))
        # listeCombinaisonsAngle = list(combinations([i for i in range(9)],3))

        for x in listeCombinaisonsDistance:
            distpx = HeadClass.euclideDist(HeadClass.pointsTete[x[0]],HeadClass.pointsTete[x[1]])
            distmm = round(3*distpx/echelle3mm_px,4)
            HeadClass.alldistancesHead.append(distmm)
        print(len(HeadClass.alldistancesHead))
        for x in listeCombinaisonsAngle:
            thetas = HeadClass.calculAngle(HeadClass.pointsTete[x[0]],HeadClass.pointsTete[x[1]],HeadClass.pointsTete[x[2]])
            thetas = np.around(thetas[0],4)
            HeadClass.alldistancesHead.append(thetas)
        print(len(HeadClass.alldistancesHead))


        # for i in range(len(HeadClass.alldistancesHead)):

        f = open("C:/Users/MASSON/Desktop/STAGE_EPINOCHE/DistancesPourModele.csv", "a")
        header = listeCombinaisonsDistance+listeCombinaisonsAngle
        header = "; ".join(str(i) for i in header)
        HeadClass.alldistancesHead = "; ".join(str(i) for i in HeadClass.alldistancesHead)
        f.write(str(header)+"\n")
        f.write(str(HeadClass.alldistancesHead))
        f.close()

    def calculDistances():
        pt3 = HeadClass.pointsTete[0]
        pt5 = HeadClass.pointsTete[1]
        pt7 = HeadClass.pointsTete[2]
        pt9 = HeadClass.pointsTete[3]
        pt11 = HeadClass.pointsTete[4]
        pt13 = HeadClass.pointsTete[5]
        pt15 = HeadClass.pointsTete[6]
        pt17 = HeadClass.pointsTete[7]
        pt19 = HeadClass.pointsTete[8]
        pt22 = HeadClass.pointsEchelle3mm[0]
        pt24 = HeadClass.pointsEchelle3mm[1]
        echelle3mm_px = HeadClass.euclideDist(pt22,pt24)

        snout_eye_px = HeadClass.euclideDist(pt3,pt5)
        snout_eye_mm = round(3*snout_eye_px/echelle3mm_px,4)
        HeadClass.distance[0]=snout_eye_mm

        snout_length_px = HeadClass.euclideDist(pt5,pt7)
        snout_length_mm = round(3*snout_length_px/echelle3mm_px,4)
        HeadClass.distance[1]=snout_length_mm

        eye_diameter_px = HeadClass.euclideDist(pt3,pt19)
        eye_diameter_mm = round(3*eye_diameter_px/echelle3mm_px,4)
        HeadClass.distance[2]=eye_diameter_mm

        head_length_px = HeadClass.euclideDist(pt5,pt17)
        head_length_mm = round(3*head_length_px/echelle3mm_px,4)
        HeadClass.distance[3]=head_length_mm

        head_depth_px = HeadClass.euclideDist(pt11,pt17)
        head_depth_mm = round(3*head_depth_px/echelle3mm_px,4)
        HeadClass.distance[4]=head_depth_mm

        # print(HeadClass.calculAngle(pt9,pt11,pt13))
        # print("nez-oeil "+str(snout_eye_mm)+" mm")
        # print("museau "+str(snout_length_mm)+" mm")
        # print("diametre eye "+str(eye_diameter_mm)+" mm")
        # print("longueur tête "+str(head_length_mm)+" mm")
        return HeadClass.distance





class BodyClass():
    ''' Class item2 pour le corps du poisson'''
    ''' Variables globales pour export '''
    ''' nodes1 : noeuds du polygone convexe de la tête et de l'echelle '''
    ''' poly1 : liste de tous les points '''
    ''' pointsTete : liste des points de la tête [(x1,y1),(x2,y2)...]'''
    ''' pointsEchelle3mm : liste des points de l'echelle [(x1,y1),(x2,y2)]'''
    ''' distance : liste des distances calculées entre les points'''
    nodes1 = []
    poly1 = []
    # pointsLongueur = []
    # pointsLargeur = []
    pointsStandard = []
    pointsEchelle10mm = []
    distance = [0 for _ in range(2)]

    def __init__(self, canvas1, points,color):

        self.previous_x = None
        self.previous_y = None
        self.selected = None
        self.listPoly = [2,7,12]
        self.NomsPoly = ["echelle","longueur","largeur"]
        self.points = points
        self.x = None
        self.pointsCardinauxFish = BodyFish.pointsCardinaux()
        # print(self.pointsCardinauxFish)

        if points!=None:
            self.polygon = canvas1.create_polygon(self.points,fill='',outline=color,smooth=0,width=6,dash=(1,5))
            BodyClass.poly1.append(self.polygon)
            canvas1.tag_bind(self.polygon, '<ButtonPress-3>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas1.tag_bind(self.polygon, '<ButtonRelease-3>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag))
            canvas1.tag_bind(self.polygon, '<B3-Motion>', self.on_move_polygon)
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas1.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                label = canvas1.create_text((x+15, y+6),text=str(node%14),font=("Purisa", 12),fill='green')
                self.nodes.append(node)
                self.nonodes.append(label)
                BodyClass.nodes1.append(node)
                canvas1.tag_bind(node, '<ButtonPress-3>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas1.tag_bind(node, '<ButtonRelease-3>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag))
                canvas1.tag_bind(node, '<B3-Motion>', lambda event, number=number: self.on_move_node(event, number))
        # canvas1.coords(7,self.pointsCardinauxFish[0][0],self.pointsCardinauxFish[0][1],self.pointsCardinauxFish[1][0],self.pointsCardinauxFish[1][1])

        # listeLongueur = canvas1.coords(7)
        # listeLargeur = canvas1.coords(12)
        # listeEchelle = canvas1.coords(2)
        # print(listeLargeur)
        # BodyClass.pointsLongueur=[(listeLongueur[i],listeLongueur[i+1]) for i in range(0,len(listeLongueur),2)]
        # BodyClass.pointsLargeur=[(listeLargeur[i],listeLargeur[i+1]) for i in range(0,len(listeLargeur),2)]
        # BodyClass.pointsEchelle10mm=[(listeEchelle[i],listeEchelle[i+1]) for i in range(0,len(listeEchelle),2)]

        for x in BodyClass.poly1:
            liste = canvas1.coords(x)
            if(len(canvas1.coords(x))==8):BodyClass.pointsStandard=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas1.coords(x))==4):BodyClass.pointsEchelle10mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

        if(len(BodyClass.pointsStandard)>0):
            afficheLongueurBody()

    def on_press_tag(self, event, number, tag):
        self.selected = tag
        self.previous_x = event.x
        self.previous_y = event.y
        print('press:', event,tag)
        # listeLongueur = canvas1.coords(7)
        # listeLargeur = canvas1.coords(12)
        # listeEchelle = canvas1.coords(2)
        # print(listeLargeur)

        # BodyClass.pointsLongueur=[(listeLongueur[i],listeLongueur[i+1]) for i in range(0,len(listeLongueur),2)]
        # BodyClass.pointsLargeur=[(listeLargeur[i],listeLargeur[i+1]) for i in range(0,len(listeLargeur),2)]
        # BodyClass.pointsEchelle10mm=[(listeEchelle[i],listeEchelle[i+1]) for i in range(0,len(listeEchelle),2)]
        #

        for x in BodyClass.poly1:
            liste = canvas1.coords(x)
            if(len(canvas1.coords(x))==8):BodyClass.pointsStandard=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas1.coords(x))==4):BodyClass.pointsEchelle10mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

        afficheLongueurBody()

    def on_release_tag(self, event, number, tag):
        self.selected = None
        self.previous_x = None
        self.previous_y = None
        # for x,y in zip(self.listPoly,self.NomsPoly):
            # print(y)
            # print(canvas1.coords(x))
            # print("\n")
        print('release:', tag)
        # listeLongueur = canvas1.coords(7)
        # listeLargeur = canvas1.coords(12)
        # listeEchelle = canvas1.coords(2)
        # # print(listeLargeur)
        #
        # BodyClass.pointsLongueur=[(listeLongueur[i],listeLongueur[i+1]) for i in range(0,len(listeLongueur),2)]
        # BodyClass.pointsLargeur=[(listeLargeur[i],listeLargeur[i+1]) for i in range(0,len(listeLargeur),2)]
        # BodyClass.pointsEchelle10mm=[(listeEchelle[i],listeEchelle[i+1]) for i in range(0,len(listeEchelle),2)]
        for x in BodyClass.poly1:
            liste = canvas1.coords(x)
            if(len(canvas1.coords(x))==8):BodyClass.pointsStandard=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas1.coords(x))==4):BodyClass.pointsEchelle10mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

        afficheLongueurBody()

    def on_move_node(self, event, number):
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
        # listeLongueur = canvas1.coords(7)
        # listeLargeur = canvas1.coords(12)
        # listeEchelle = canvas1.coords(2)
        # # print(listeLargeur)
        #
        # BodyClass.pointsLongueur=[(listeLongueur[i],listeLongueur[i+1]) for i in range(0,len(listeLongueur),2)]
        # BodyClass.pointsLargeur=[(listeLargeur[i],listeLargeur[i+1]) for i in range(0,len(listeLargeur),2)]
        # BodyClass.pointsEchelle10mm=[(listeEchelle[i],listeEchelle[i+1]) for i in range(0,len(listeEchelle),2)]
        for x in BodyClass.poly1:
            liste = canvas1.coords(x)
            if(len(canvas1.coords(x))==8):BodyClass.pointsStandard=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas1.coords(x))==4):BodyClass.pointsEchelle10mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
        afficheLongueurBody()

    def on_move_polygon(self, event):
        '''move polygon and red rectangles in nodes'''
        if self.selected:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
            # move polygon
            canvas1.move(self.selected, dx, dy)
            print(self.selected)
            # move red nodes
            for item,item1 in zip(self.nodes,self.nonodes):
                print("move")
                print(item)
                print(item1)
                canvas1.move(item, dx, dy)
                canvas1.move(item1,dx,dy)
            # recalculate values in self.points
            for item in self.points:
                print("calculate)")
                print(item)

                item[0] += dx
                item[1] += dy
            self.previous_x = event.x
            self.previous_y = event.y
        # listeLongueur = canvas1.coords(7)
        # listeLargeur = canvas1.coords(12)
        # listeEchelle = canvas1.coords(2)
        # BodyClass.pointsLongueur=[(listeLongueur[i],listeLongueur[i+1]) for i in range(0,len(listeLongueur),2)]
        # BodyClass.pointsLargeur=[(listeLargeur[i],listeLargeur[i+1]) for i in range(0,len(listeLargeur),2)]
        # BodyClass.pointsEchelle10mm=[(listeEchelle[i],listeEchelle[i+1]) for i in range(0,len(listeEchelle),2)]
        for x in BodyClass.poly1:
            liste = canvas1.coords(x)
            if(len(canvas1.coords(x))==8):BodyClass.pointsStandard=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas1.coords(x))==4):BodyClass.pointsEchelle10mm=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
        afficheLongueurBody()

    def hide_nodes():
        for node in Item.nodes1:
            canvas1.itemconfig(node,fill="",outline='')
        for poly in Item.poly1:
            canvas1.itemconfig(poly,dash=())
    def euclideDist(a,b):
        import numpy as np
        x1 = a[0]
        y1 = a[1]
        x2 = b[0]
        y2 = b[1]
        norme = np.sqrt((x2-x1)**2+(y2-y1)**2)
        return norme
    def calculDistances():
        pt3 = BodyClass.pointsEchelle10mm[0]
        pt5 = BodyClass.pointsEchelle10mm[1]
        # pt8 = BodyClass.pointsLongueur[0]
        # pt10 = BodyClass.pointsLongueur[1]
        # pt13 = BodyClass.pointsLargeur[0]
        # pt15 = BodyClass.pointsLargeur[1]
        pt8 = BodyClass.pointsStandard[0]
        pt10 = BodyClass.pointsStandard[1]
        pt12 = BodyClass.pointsStandard[2]
        pt14 = BodyClass.pointsStandard[3]
        echelle10mm_px = BodyClass.euclideDist(pt3,pt5)
        body_size_px = BodyClass.euclideDist(pt8,pt12)
        body_size_mm = round(10*body_size_px/echelle10mm_px,4)
        body_depth_px = BodyClass.euclideDist(pt10,pt14)
        body_depth_mm = round(10*body_depth_px/echelle10mm_px,4)
        BodyClass.distance[0]=body_size_mm
        BodyClass.distance[1]=body_depth_mm
        return BodyClass.distance

class HeadFish():
    img1 = None
    pathImg = ""
    poisson = None
    centreOeil=None
    def __init__(self, canvas,PIL_image,CV2_image,size):
        # HeadFish.pathImg = path
        self.img = PIL_image
        self.img = self.img.resize(size, Image.ANTIALIAS)
        print(self.img.size)
        # self.img.putalpha(200)
        self.tatras = ImageTk.PhotoImage(self.img)
        toto = CV2_image
        self.circle = self.detect_eye(cv2.resize(toto,size,Image.ANTIALIAS))
        HeadFish.centreOeil = [self.circle[0],self.circle[1]]
        # print(self.circle)
        # canvas.delete()
        HeadFish.poisson = canvas.create_image(0, 0, anchor=tk.NW,image=self.tatras)
        canvas.move(HeadFish.poisson,-(self.circle[0]-300),-(self.circle[1]-250))
        HeadFish.img1 = HeadFish.poisson
        root.bind("<Left>",self.moveLeft)
        root.bind("<Right>",self.moveRight)
        root.bind("<Up>",self.moveUp)
        root.bind("<Down>",self.moveDown)
    def moveLeft(self,event):
        canvas.move(self.poisson,-10,0)
    def moveRight(self,event):
        canvas.move(self.poisson,10,0)
    def moveUp(self,event):
        canvas.move(self.poisson,0,-10)
    def moveDown(self,event):
        canvas.move(self.poisson,0,10)
    def hideImage():
        canvas.move(HeadFish.img1,0,1000)
    def saveImage():
        ps = canvas.postscript(colormode='color')
        import io
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(pathFinal+HeadFish.pathImg[-13:])
    def detect_eye(self,img):
        import matplotlib.pyplot as plt
        img_couleur = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # img_gray = cv2.resize(img_gray,(3500,2625),Image.ANTIALIAS)
        # print(type(img_gray))
        img_gray = cv2.medianBlur(img_gray,21)
        # plt.figure()
        # plt.imshow(img_gray)
        # plt.show()
        # print(type(img_gray))
        circles1 = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=70,param2=65, minDist=100, minRadius=25,maxRadius=45)
        circles = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=100,param2=30, minDist=120, minRadius=80,maxRadius=95)
        circles = np.round(circles[0, :]).astype("int32")
        # print(circles)
        # print(circles1[0])
        copy=img_gray.copy()
        # for (x, y, r) in circles:
        #     cv2.circle(copy, (x, y), r, (255, 255, 266), 4)
        # for (x, y, r) in circles1[0]:
            # cv2.circle(copy, (int(x), int(y)), int(r), (255, 255, 255), 3)
        #
        # #
        # plt.figure()
        # plt.imshow(copy,cmap="gray")
        # plt.show()

        return circles1[0][0]


class BodyFish():
    img1 = None
    imgcv2 = None
    pathImg = ""
    pointsEchelle10mm = []
    poisson = None
    def __init__(self, canvas1,PIL_image,CV2_image,size):
        self.img = PIL_image
        self.img = self.img.resize(size, Image.ANTIALIAS)
        print(self.img.size)
        self.tatras = ImageTk.PhotoImage(self.img)
        BodyFish.poisson = canvas1.create_image(0, 0, anchor=tk.NW, image=self.tatras)
        BodyFish.img1 = BodyFish.poisson
        BodyFish.imgcv2 = CV2_image
        root.bind("<Key>",self.move)
        root.bind("<Key>",self.move)
        root.bind("<Key>",self.move)
        root.bind("<Key>",self.move)
    def move(self,event):
        if event.char=='q':
            canvas1.move(BodyFish.poisson,-10,0)

        if event.char=='s':
            canvas1.move(BodyFish.poisson,10,0)
        if event.char =='z':
            canvas1.move(BodyFish.poisson,0,-10)

    def hideImage():
        canvas1.move(Fish.img1,0,1000)
    def saveImage():
        ps = canvas1.postscript(colormode='color')
        import io
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(pathFinal+Fish.pathImg[-13:])
    def pointsCardinaux():
        import cv2
        import matplotlib.pyplot as plt
        import numpy as np
        pointsCardinauxFish = []
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
        img = cv2.cvtColor(BodyFish.imgcv2,cv2.COLOR_RGB2BGR)
        #1500x1125
        img = cv2.resize(img,(1300,975))
        # print(img)
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, diamond,iterations=5)
        dilated = cv2.dilate(closing,diamond,iterations=1)
        blured = cv2.medianBlur(dilated,ksize=21)
        binarized = cv2.adaptiveThreshold(cv2.cvtColor(blured,cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,51,6)


        # plt.imshow(binarized)
        # plt.show()
        contours, hierarchy = cv2.findContours(binarized,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        list_area = [cv2.contourArea(c) for c in contours]
        for c in contours:
            area = cv2.contourArea(c)
            if area < 100:
                cv2.fillPoly(binarized, pts=[c], color=0)
                continue
        binarized = cv2.morphologyEx(binarized, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4)));
        contours2, hierarchy2 = cv2.findContours(binarized,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        list_area2 = [cv2.contourArea(c) for c in contours2]
        drawing = np.ones((img.shape[0], img.shape[1], 3), np.uint8)*255
        cv2.fillPoly(drawing,pts=contours2,color=(0,0,0))
        drawing = cv2.dilate(drawing,diamond,iterations=7)
        drawing = cv2.morphologyEx(drawing, cv2.MORPH_CLOSE, diamond,iterations=5)
        # plt.imshow(drawing)
        # plt.show()
        contours3, hierarchy3 = cv2.findContours(cv2.cvtColor(drawing,cv2.COLOR_BGR2GRAY),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        out_mask = np.zeros_like(img)
        contours3 = sorted(contours3, key=cv2.contourArea)
        out=img.copy()
        cv2.drawContours(out, [contours3[-1]], -1, (255,0,0), 3)
        c=max(contours3, key=cv2.contourArea)
        left = tuple(c[c[:, :, 0].argmin()][0])
        right = tuple(c[c[:, :, 0].argmax()][0])
        top = tuple(c[c[:, :, 1].argmin()][0])
        bottom = tuple(c[c[:, :, 1].argmax()][0])
        # plt.imshow(out)
        # plt.show()
        print(left)
        print(right)
        pointsCardinauxFish.append(left)
        pointsCardinauxFish.append(right)
        pointsCardinauxFish.append(top)
        pointsCardinauxFish.append(bottom)
        # print(pointsCardinauxFish)
        return pointsCardinauxFish


def afficheLongueur():
    distance = HeadClass.calculDistances()
    # print(distance)
    texte = ""
    texte += "5 <-> 3 : nez oeil : "+str(distance[0])+" mm \n"
    texte += "5 <-> 7 : museau : "+str(distance[1])+" mm \n"
    texte += "3 <-> 19 : diametre oeil : "+str(distance[2])+" mm \n"
    texte += "5 <-> 17 : longueur tête : "+str(distance[3])+" mm \n"
    texte += "11 <-> 17 : largeur tête : "+str(distance[4])+" mm \n"
    Longueur.config(text=texte)

def afficheLongueurBody():
    distance = BodyClass.calculDistances()
    # print(distance)
    texte = ""
    texte += "8 <-> 10 : Longueur Corps : "+str(distance[0])+" mm \n"
    texte += " 13 <-> 15 : Largeur corps : "+str(distance[1])+" mm \n"
    LongueurBody.config(text=texte)

def alignPoints():
    ptsCardinaux = BodyFish.pointsCardinaux()
def openfn():
    import tkinter.filedialog
    filepath = tk.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('jpeg files','.jpeg')])
    return filepath
def clearAllCanvas():
    HeadClass.nodes1=[]
    HeadClass.poly1=[]
    HeadClass.pointsTete=[]
    HeadClass.pointsEchelle3mm=[]
    HeadClass.distance=[0 for _ in range(20)]
    HeadClass.angles= [0 for _ in range(20)]
    HeadClass.points=None
    Longueur.config(text="")
    BodyClass.nodes1=[]
    BodyClass.poly1=[]
    BodyClass.pointsTete=[]
    BodyClass.pointsEchelle3mm=[]
    BodyClass.distance=[0 for _ in range(20)]
    BodyClass.points=None
    LongueurBody.config(text="")
    canvas.delete('all')
    canvas1.delete('all')
def importImage():

    ''' Placement manuel des points'''
    pt3 = [249.0, 250.0]
    pt5 = [122.0, 259.0]
    pt7 = [105.0, 312.0]
    pt9 = [207.0, 393.0]
    pt11 = [396.0, 415.0]
    pt13 = [414.0, 343.0]
    pt15 = [438.0, 239.0]
    pt17 = [473.0, 119.0]
    pt19 = [379.0, 248.0]
    corps= [pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19]
    echelle10mm = [[112,181],[300,186]]
    echelle3mm = [[67,74],[199,74]]

    ''' Réinitialisation pour import '''
    print("\n### Reset ###")
    clearAllCanvas()

    ''' Import de l'image 4000x3000 '''
    print("\n### Import de l'image ###")
    pathok = openfn()
    PIL_image = Image.open(pathok)

    ''' Resize pour le corps '''
    print("\n### Resize de l'image pour le corps")
    PIL_image = PIL_image.resize((1300,975), Image.ANTIALIAS)
    CV2_image = np.array(Image.open(pathok))

    '''' Initialisation des points du corps par détection auto '''
    print("\n### Calcul des points pour la longueur et la largeur ###")
    out,c = ArchitectureFondBlanc.contoursCorps(CV2_image)
    [left,right,top,bottom] = ArchitectureFondBlanc.pointExtremeContours(c)
    imagerot = ArchitectureFondBlanc.rotate_image(out,ArchitectureFondBlanc.angleRot(left,right)[0],ArchitectureFondBlanc.angleRot(left,right)[1])
    _,c = ArchitectureFondBlanc.contoursCorps(imagerot)
    [left,right,top,bottom] = ArchitectureFondBlanc.pointExtremeContours(c)
    corpsStandard = [[left[0],left[1]],[top[0],top[1]],[right[0],right[1]],[bottom[0],bottom[1]]]
    print("### OK ###")

    print("\n### Rotation et conversion de l'image ###")
    newPIL_image = Image.fromarray(imagerot)
    newCV2_image = cv2.cvtColor(np.array(newPIL_image), cv2.COLOR_BGR2RGB)
    print("### OK ###")

    print("\n### Chargement de l'image du corps et repositionnement' ###")
    BodyFish(canvas1,newPIL_image,newCV2_image,(1300,975))
    print(BodyFish.poisson)
    canvas1.move(BodyFish.poisson,-(left[0]-50),-(left[1]-280))
    print("### OK ###")

    print("\n### Alignement des points sur le corps'  ###")
    corpsStandard = [[x[0]-(left[0]-50),x[1]-(left[1]-280)] for x in corpsStandard]
    echelle10mm = [[x[0]-(left[0]-250),x[1]-(left[1]-350)] for x in echelle10mm]
    BodyClass(canvas1, echelle10mm,'red')
    BodyClass(canvas1,corpsStandard,'cyan')
    print("### OK ###")

    ''' Resize pour la tête '''
    print("\n### Resize de l'image pour la tête")
    PIL_image_big = PIL_image.resize((3500,2625), Image.ANTIALIAS)
    CV2_image_big = np.array(Image.open(pathok))

    print("\n### Chargement de l'image de la tête' ###")
    newPIL_image_big = Image.fromarray(CV2_image_big)
    newCV2_image_big = cv2.cvtColor(np.array(newPIL_image_big), cv2.COLOR_BGR2RGB)
    HeadFish(canvas,newPIL_image_big,newCV2_image_big,(3500,2625))
    print("### OK ###")

    ''' Initialisation des points 3 et 19 par détection auto '''
    print("\n### Calcul des points 3 et 19 ###")
    [pt3,pt19]=ArchitectureFondBlanc.points3_19(CV2_image_big)
    pt3 = [pt3[0],pt3[1]]
    pt19 = [pt19[0],pt19[1]]


    print("### OK ###")

    '''Initialisation du point 9 par détection auto '''
    print("\n### Calcul du point 9 ###")
    _,c = ArchitectureFondBlanc.contoursCorpsBig(CV2_image_big)

    pt9=ArchitectureFondBlanc.point9(c,pt19)
    pt9 = [pt9[0],pt9[1]]
    print(pt9)
    pt9 = [pt9[0]-(HeadFish.centreOeil[0]-300),pt9[1]-(HeadFish.centreOeil[1]-250)]

    print("### OK ###")
    #
    # '''Initialisation du point 15 et 13 par détection auto '''
    # print("\n### Calcul des points 9 ###")
    # pt15,pt13=ArchitectureFondBlanc.points15_13(imagerot)
    # pt15 = [pt15[0],pt15[1]]
    # pt13 = [pt13[0],pt13[1]]
    # print("### OK ###")


    '''Initialisation des points 5 et 7 par détection auto '''
    # pt5,pt7 = ArchitectureFondBlanc.points5_7(img)

    pt3 = [pt3[0]-(HeadFish.centreOeil[0]-300),pt3[1]-(HeadFish.centreOeil[1]-250)]
    pt19 = [pt19[0]-(HeadFish.centreOeil[0]-300),pt19[1]-(HeadFish.centreOeil[1]-250)]
    print(pt3)
    print(pt19)
    corps= [pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19]
    print("\n### Placement des points de la tête ###")
    HeadClass(canvas, corps,'cyan')
    HeadClass(canvas,echelle3mm,'red')
    print("### OK ###")



def resetCanvas(canvas,canvas1):
    canvas1.destroy()
    canvas.destroy()
    ''' Canvas pour la tête '''
    canvas = tk.Canvas(root,bg='#f0f0f0',bd=0)
    canvas.config(width=600, height=500)
    # canvas.pack(side='left')
    canvas.grid(column=0,row=8)


    ''' Canvas pour le corps '''
    canvas1 = tk.Canvas(root,bg='#f0f0f0')
    canvas1.config(width=1000, height=500)
    # canvas1.pack(side='left')
    canvas1.grid(column=1,row=8)

## Main

''' Fenetre et menu'''
root = tk.Tk()
root.geometry("1000x800")
root.title("Sex Determination for Three Spined Stickleback")
menubar = tk.Menu(root)
menuFichier = tk.Menu(menubar,tearoff=0)
menuFichier.add_command(label="Créer", command=None)
menuFichier.add_command(label="Importer", command=None)
menuFichier.add_command(label="Editer", command=None)
menuFichier.add_separator()
menuFichier.add_command(label="Quitter", command=root.destroy)
menubar.add_cascade(label="Fichier", menu=menuFichier)
menuEditer = tk.Menu(menubar, tearoff=0)
menuEditer.add_command(label="Couper", command=None)
menuEditer.add_command(label="Copier", command=None)
menuEditer.add_command(label="Coller", command=None)
menubar.add_cascade(label="Editer", menu=menuEditer)
menuAide = tk.Menu(menubar, tearoff=0)
menuAide.add_command(label="A propos", command=None)
menubar.add_cascade(label="Aide", menu=menuAide)
root.config(menu=menubar)

''' Label Intro de presentation'''
intro = tk.Label(root,text="Sexing procedure of three-spined stickleback -- Proof of concept \n")
# intro.place(x=500,y=0)
intro.grid(ipadx=2)

''' Label explications '''
explanation = tk.Label(root,text="Le positionnement des points est fait automatiquement -- Ajuster si nécessaire \n ")
# explanation.place(x=10,y=120)
explanation.grid(column=0,row=1)




''' Boutons '''
B = tk.Button(root,text = "Import image and autoplace",command = importImage)
B.place(x=625,y=105)
B = tk.Button(root,text = "Predict",command = None)
B.place(x=790,y=105)
B = tk.Button(root,text = "Export (developpers only)",command = HeadClass.genererAllDistancesHead)
B.place(x=625,y=135)
# B = tk.Button(root,text="Next image",command = None)
# B.place(x=775,y=135)
# B.()

# B.pack()

# B.pack()
#
#
''' Labels pour les longueurs de la tête '''
tk.Label(root,text="Longueurs caractéristiques de la tête : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=0,row=2)
Longueur = tk.Label(root,text="",justify=tk.LEFT)
# Longueur.place(x=200,y=45)
Longueur.grid(column=0,row=4)


''' Labels pour les longueurs du corps '''
tk.Label(root,text="Longueurs caractéristiques du corps : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=1,row=2)
LongueurBody = tk.Label(root,text="",justify=tk.LEFT)
# LongueurBody.place(x=700,y=45)
LongueurBody.grid(column=1,row=4)


''' Canvas pour la tête '''
canvas = tk.Canvas(root,bg='#f0f0f0',bd=0)
canvas.config(width=600, height=500)
# canvas.pack(side='left')
canvas.grid(column=0,row=8)


''' Canvas pour le corps '''
canvas1 = tk.Canvas(root,bg='#f0f0f0')
canvas1.config(width=1000, height=500)
# canvas1.pack(side='left')
canvas1.grid(column=1,row=8)

#
#
#
# ''' Placement manuel des points'''
# corps= [[249.0, 250.0], [122.0, 259.0], [105.0, 312.0], [207.0, 393.0], [396.0, 415.0], [414.0, 343.0], [438.0, 239.0], [473.0, 119.0], [379.0, 248.0]]
# echelle10mm = [[112,181],[300,186]]
# echelle3mm = [[67,74],[199,74]]
# longueurStandard = [[178,331],[878,361]]
# largeurStandard = [[500,420],[475,280]]
#
# ''' Import de l'image '''
# pathok = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATABASE\\FEMALE\\IMGP1093F.jpg"
# pathok = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\gimp_cut\\male\\IMGP1074M.JPG"
# # listImg[190]
#
#
#
# '''' Initialisation des points du corps par détection auto '''
# print("### Calcul des points du corps ###")
# pointsCardx = BodyFish.pointsCardinaux()
# # print("liste")
# # print(pointsCardx)
# longueurStandard = [[pointsCardx[0][0],pointsCardx[0][1]],[pointsCardx[1][0],pointsCardx[1][1]]]
# print("### OK ###")
#
# print("### Placement des points de la tête ###")
# HeadClass(canvas, corps,'cyan')
# HeadClass(canvas,echelle3mm,'red')
# print("### OK ###")
# print("### Placement des points du corps ###")
# BodyClass(canvas1, echelle10mm,'red')
# BodyClass(canvas1,longueurStandard,'cyan')
# BodyClass(canvas1,largeurStandard,'cyan')
# print("### OK ###")

# canvas.pack()

root.mainloop()



''' Documentation

generate diagramm class

in powershell : Pyreverse -o dot placementCorps.py
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

