# Pour assurer le bon fonctionnement
import sys
sys.path.insert(0, 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho')

# Import des bibliothèques (s'assurer qu'elles soient installées)
import tkinter as tk
from PIL import Image, ImageTk
import os,cv2,Placement,Fonctions
import numpy as np
import math,functools,itertools

# Classe pour les points de la tête
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
    distances_check = [0 for _ in range(20)]
    distances_all = []

    def __init__(self, canvas, points,color):
        """!
        Constructeur du polygone de la tête
        @param canvas tk.Canvas : cadre de l'image
        @param points list : liste des points du polygone
        @param color String : couleur du polygone
        """
        self.previous_x = None
        self.previous_y = None
        self.selected = None
        self.points = points
        self.x = None
        if points!=None:
            if color=='red':outline='red'
            else: outline=''
            self.polygon = canvas.create_polygon(self.points,fill='',outline=outline,smooth=0,width=2,dash=())
            HeadClass.id_polygons.append(self.polygon)
            canvas.tag_bind(self.polygon, '<ButtonPress-1>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas.tag_bind(self.polygon, '<ButtonRelease-1>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag))
            canvas.tag_bind(self.polygon, '<B1-Motion>', self.on_move_polygon)

            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                label = canvas.create_text((x+15, y+6),text=str(node%25),font=("Purisa", 1),fill='red')
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas.tag_bind(node, '<ButtonPress-1>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas.tag_bind(node, '<ButtonRelease-1>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag))
                canvas.tag_bind(node, '<B1-Motion>', lambda event, number=number: self.on_move_node(event, number))

        HeadClass.update_points()

        if(len(HeadClass.pointsEchelle)>0):
             afficheLongueur()

    def update_points():
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

    def on_release_tag(self, event, number, tag):
        self.selected = None
        self.previous_x = None
        self.previous_y = None
        HeadClass.update_points()

    def on_move_node(self, event, number):
        '''move single node in polygon'''
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

        HeadClass.update_points()
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
        HeadClass.update_points()

    def genererAllDistancesHead():

        listeCombinaisonsDistance,listeCombinaisonsAngle = Fonctions.Externes.allPointsAngles()
        pt22 = HeadClass.pointsEchelle[0]
        pt24 = HeadClass.pointsEchelle[1]
        echelle3mm_px = Fonctions.Externes.euclideDist(pt22,pt24)
        for x in listeCombinaisonsDistance:
            distpx = Fonctions.Externes.euclideDist(HeadClass.pointsFish[x[0]],HeadClass.pointsFish[x[1]])
            distmm = round(3*distpx/echelle3mm_px,4)
            HeadClass.distances_all.append(distmm)
        for x in listeCombinaisonsAngle:
            thetas = Fonctions.Externes.calculAngle(HeadClass.pointsFish[x[0]],HeadClass.pointsFish[x[1]],HeadClass.pointsFish[x[2]])
            thetas = np.around(thetas[0],4)
            HeadClass.distances_all.append(thetas)

        f = open("C:/Users/MASSON/Desktop/STAGE_EPINOCHE/DistancesPourModele.csv", "a")
        header = listeCombinaisonsDistance+listeCombinaisonsAngle
        header = "; ".join(str(i) for i in header)
        HeadClass.distances_all = "; ".join(str(i) for i in HeadClass.distances_all)
        f.write(str(header)+"\n")
        f.write(str(HeadClass.distances_all))
        f.close()

    def calculDistances():
        pt3 = HeadClass.pointsFish[0]
        pt5 = HeadClass.pointsFish[1]
        pt7 = HeadClass.pointsFish[2]
        pt9 = HeadClass.pointsFish[3]
        pt11 = HeadClass.pointsFish[4]
        pt13 = HeadClass.pointsFish[5]
        pt15 = HeadClass.pointsFish[6]
        pt17 = HeadClass.pointsFish[7]
        pt19 = HeadClass.pointsFish[8]
        pt22 = HeadClass.pointsEchelle[0]
        pt24 = HeadClass.pointsEchelle[1]
        echelle3mm_px = Fonctions.Externes.euclideDist(pt22,pt24)

        snout_eye_px = Fonctions.Externes.euclideDist(pt3,pt5)
        snout_eye_mm = round(3*snout_eye_px/echelle3mm_px,4)
        HeadClass.distances_check[0]=snout_eye_mm

        snout_length_px = Fonctions.Externes.euclideDist(pt5,pt7)
        snout_length_mm = round(3*snout_length_px/echelle3mm_px,4)
        HeadClass.distances_check[1]=snout_length_mm

        eye_diameter_px = Fonctions.Externes.euclideDist(pt3,pt19)
        eye_diameter_mm = round(3*eye_diameter_px/echelle3mm_px,4)
        HeadClass.distances_check[2]=eye_diameter_mm

        head_length_px = Fonctions.Externes.euclideDist(pt5,pt17)
        head_length_mm = round(3*head_length_px/echelle3mm_px,4)
        HeadClass.distances_check[3]=head_length_mm

        head_depth_px = Fonctions.Externes.euclideDist(pt11,pt17)
        head_depth_mm = round(3*head_depth_px/echelle3mm_px,4)
        HeadClass.distances_check[4]=head_depth_mm

        jaw_length_px = Fonctions.Externes.euclideDist(pt7,pt9)
        jaw_length_mm = round(3*jaw_length_px/echelle3mm_px,4)
        HeadClass.distances_check[5]=jaw_length_mm

        jaw_length2_px = Fonctions.Externes.euclideDist(pt5,pt9)
        jaw_length2_mm = round(3*jaw_length2_px/echelle3mm_px,4)
        HeadClass.distances_check[6]=jaw_length2_mm

        return HeadClass.distances_check





class BodyClass():
    """Variables globales pour export
    id_polygons : liste des id des polygons (le corps et l'echelle)
    pointsTete : liste des points du corps [(x1,y1),(x2,y2)...]
    pointsEchelle3mm : liste des points de l'echelle [(x1,y1),(x2,y2)]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    """

    id_polygons = []
    pointsFish = []
    pointsEchelle = []
    distances_check = [0 for _ in range(2)]
    distances_all = []

    def __init__(self, canvas1, points,color):

        self.previous_x = None
        self.previous_y = None
        self.selected = None
        self.points = points
        self.x = None

        if points!=None:
            if color=='red':outline='red'
            else: outline=''
            self.polygon = canvas1.create_polygon(self.points,fill='',outline=outline,smooth=0,width=3,dash=())
            BodyClass.id_polygons.append(self.polygon)
            canvas1.tag_bind(self.polygon, '<ButtonPress-3>',   lambda event, tag=self.polygon: self.on_press_tag(event, 0, tag))
            canvas1.tag_bind(self.polygon, '<ButtonRelease-3>', lambda event, tag=self.polygon: self.on_release_tag(event, 0, tag))
            canvas1.tag_bind(self.polygon, '<B3-Motion>', self.on_move_polygon)
            self.nodes = []
            self.nonodes = []
            for number, point in enumerate(self.points):
                x, y = point
                node = canvas1.create_rectangle((x-3, y-3, x+3, y+3), fill=color)
                label = canvas1.create_text((x+15, y+6),text=str(node%15),font=("Purisa", 1),fill='green')
                self.nodes.append(node)
                self.nonodes.append(label)
                canvas1.tag_bind(node, '<ButtonPress-3>',   lambda event, number=number, tag=node: self.on_press_tag(event, number, tag))
                canvas1.tag_bind(node, '<ButtonRelease-3>', lambda event, number=number, tag=node: self.on_release_tag(event, number, tag))
                canvas1.tag_bind(node, '<B3-Motion>', lambda event, number=number: self.on_move_node(event, number))

        BodyClass.update_points()

        if(len(BodyClass.pointsFish)>0):
            afficheLongueurBody()

    def update_points():
        for id in BodyClass.id_polygons:
            liste = canvas1.coords(id)
            if(len(canvas1.coords(id))==8):BodyClass.pointsFish=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas1.coords(id))==4):BodyClass.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

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
        print('press:', event,tag)

        BodyClass.update_points()
        afficheLongueurBody()

    def on_release_tag(self, event, number, tag):
        self.selected = None
        self.previous_x = None
        self.previous_y = None
        print('release:', tag)

        BodyClass.update_points()
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

        BodyClass.update_points()
        afficheLongueurBody()

    def on_move_polygon(self, event):
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

        BodyClass.update_points()
        afficheLongueurBody()

    def calculDistances():
        pt3 = BodyClass.pointsEchelle[0]
        pt5 = BodyClass.pointsEchelle[1]
        pt8 = BodyClass.pointsFish[0]
        pt10 = BodyClass.pointsFish[1]
        pt12 = BodyClass.pointsFish[2]
        pt14 = BodyClass.pointsFish[3]
        echelle10mm_px = Fonctions.Externes.euclideDist(pt3,pt5)
        body_size_px = Fonctions.Externes.euclideDist(pt8,pt12)
        body_size_mm = round(10*body_size_px/echelle10mm_px,4)
        body_depth_px = Fonctions.Externes.euclideDist(pt10,pt14)
        body_depth_mm = round(10*body_depth_px/echelle10mm_px,4)
        BodyClass.distances_check[0]=body_size_mm
        BodyClass.distances_check[1]=body_depth_mm
        return BodyClass.distances_check

class HeadFish():
    """Variables globales pour export
    id_polygons : liste des id des polygons (la tete et l'echelle)
    pointsTete : liste des points de la tête [(x1,y1),(x2,y2)...]
    pointsEchelle3mm : liste des points de l'echelle [(x1,y1),(x2,y2)]
    distances_check : liste des distances caractéristiques affichées
    distances_all : liste de toutes les distances sauvegardés pour le modèle
    """
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
    def detect_eye(self,img):
        img_couleur = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray,21)
        circles1 = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=70,param2=65, minDist=100, minRadius=25,maxRadius=45)
        circles = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=100,param2=30, minDist=120, minRadius=80,maxRadius=95)
        circles = np.round(circles[0, :]).astype("int32")
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


def afficheLongueur():
    distance = HeadClass.calculDistances()
    texte = ""
    texte += "5 <-> 3 : distance nez oeil : "+str(distance[0])+" mm \n"
    texte += "5 <-> 7 : longueur museau : "+str(distance[1])+" mm \n"
    texte += "3 <-> 19 : diametre oeil : "+str(distance[2])+" mm \n"
    texte += "5 <-> 17 : longueur tête : "+str(distance[3])+" mm \n"
    texte += "11 <-> 17 : largeur tête : "+str(distance[4])+" mm \n"
    texte += "7 <-> 9 : bas bouche - menton : "+str(distance[5])+" mm \n"
    texte += "5 <-> 9 : haut bouche - menton : "+str(distance[6])+" mm \n"
    Longueur.config(text=texte)

def afficheLongueurBody():
    distance = BodyClass.calculDistances()
    texte = ""
    texte += "8 <-> 10 : Longueur Corps : "+str(distance[0])+" mm \n"
    texte += " 13 <-> 15 : Largeur corps : "+str(distance[1])+" mm \n"
    LongueurBody.config(text=texte)

def openfn():
    import tkinter.filedialog
    filepath = tk.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('jpeg files','.jpeg')])
    return filepath
def clearAllCanvas():
    HeadClass.id_polygons=[]
    HeadClass.pointsFish=[]
    HeadClass.pointsEchelle=[]
    HeadClass.distances_check=[0 for _ in range(20)]
    Longueur.config(text="")
    BodyClass.id_polygons=[]
    BodyClass.pointsFish=[]
    BodyClass.pointsEchelle=[]
    BodyClass.distances_check=[0 for _ in range(20)]
    LongueurBody.config(text="")
    canvas.delete('all')
    canvas1.delete('all')


def importImage():
    print("### Initialisation ###")
    corps,echelle10mm,echelle3mm = Placement.Points.randomPointsBis()
    pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19 = corps
    clearAllCanvas()
    pathok = openfn()
    PIL_image = Image.open(pathok)

    ''' Resize pour le corps '''
    print("\n### Traitement du corps 1/3 ###")
    PIL_image = PIL_image.resize((1300,975), Image.ANTIALIAS)
    CV2_image = np.array(Image.open(pathok))
    '''' Initialisation des points du corps par détection auto '''
    print("\n### Traitement du corps 2/3 ###")
    out,c = Placement.Points.contoursCorps(CV2_image)
    [left,right,top,bottom] = Placement.Points.pointExtremeContours(c)
    imagerot = Placement.Points.rotate_image(out,Placement.Points.angleRot(left,right)[0],Placement.Points.angleRot(left,right)[1])
    _,c = Placement.Points.contoursCorps(imagerot)
    [left,right,top,bottom] = Placement.Points.pointExtremeContours(c)
    corpsStandard = [[left[0],left[1]],[top[0],top[1]],[right[0],right[1]],[bottom[0],bottom[1]]]
    """Incrustation de l'image """
    print("\n### Traitement du corps 3/3 ###")
    newPIL_image = Image.fromarray(imagerot)
    newCV2_image = cv2.cvtColor(np.array(newPIL_image), cv2.COLOR_BGR2RGB)
    BodyFish(canvas1,newPIL_image,newCV2_image,(1300,975))
    # print(BodyFish.poisson)
    canvas1.move(BodyFish.poisson,-(left[0]-50),-(left[1]-280))
    canvas1.update()
    print("### OK ###")

    ''' Resize pour la tête '''
    print("\n### Traitement de la tête 1/3 ### ")
    PIL_image_big = Image.open(pathok)
    PIL_image_big = PIL_image_big.resize((3500,2625), Image.ANTIALIAS)
    PIL_image_big = np.flip(PIL_image_big,axis=2)
    CV2_image_big = np.array(PIL_image_big)
    CV2_image_big = CV2_image_big[:, :, ::-1].copy()
    out,c = Placement.Points.contoursCorpsBig(CV2_image_big)
    [left1,right1,top,bottom] = Placement.Points.pointExtremeContours(c)
    CV2_image_big = Placement.Points.rotate_image(out,Placement.Points.angleRot(left1,right1)[0],Placement.Points.angleRot(left1,right1)[1])

    print("\n### Chargement de l'image de la tête' ###")
    newPIL_image_big = Image.fromarray(CV2_image_big)
    newCV2_image_big = cv2.cvtColor(np.array(newPIL_image_big), cv2.COLOR_BGR2RGB)
    HeadFish(canvas,newPIL_image_big,newCV2_image_big,(3500,2625))
    canvas.update()
    print("### OK ###")

    print("\n### Alignement des points sur le corps'  ###")
    corpsStandard = [[x[0]-(left[0]-50),x[1]-(left[1]-280)] for x in corpsStandard]
    echelle10mm = [[x[0]-(left[0]-250),x[1]-(left[1]-350)] for x in echelle10mm]
    BodyClass(canvas1, echelle10mm,'red')
    BodyClass(canvas1,corpsStandard,'cyan')
    canvas1.update()
    print("### OK ###")
    ''' Initialisation des points 3 et 19 par détection auto '''
    print("\n### Calcul des points 3 et 19 ###")
    try:
        [pt3,pt19]=Placement.Points.points3_19(CV2_image_big)
        pt3 = [pt3[0],pt3[1]]
        pt19 = [pt19[0],pt19[1]]
    except:
        print("Impossible de déterminer les points 3 et 19")


    print("### OK ###")

    '''Initialisation du point 9 par détection auto '''
    print("\n### Calcul du point 9 ###")
    _,c = Placement.Points.contoursCorpsBig(CV2_image_big)
    try:
        pt9=Placement.Points.point9(c,pt19)
        pt9 = [pt9[0],pt9[1]]
        print(pt9)
    except:
        print("Impossible de déterminer le point 9")

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
    print("### OK ###")


    '''Initialisation des points 5 et 7 par détection auto '''
    print("\n### Calcul des points 5 et 7  ###")

    try:
        pt7,pt5 = Placement.Points.points5_7(CV2_image_big,pt9)
        pt5 = [pt5[0],pt5[1]]
        pt7 = [pt7[0],pt7[1]]
    except:
        print("Impossible de détecter les points 5 et 7")

    """Initialisation des points 11 et 17 par détection auto """
    try:
        pt17,pt11 = Placement.Points.points11_17(CV2_image_big,pt13,pt15)
    except:
        print("Impossible de détecter les points 11 et 17")

    corps = Placement.Points.centerPoints([pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19],HeadFish.centreOeil)

    print("\n### Placement des points de la tête ###")
#     ancienne  : #37ff00
#  nouvelle : #ffff00
    HeadClass(canvas, corps,'#ff00f2')
    HeadClass(canvas,echelle3mm,'red')
    print("### OK ###")


def affichePrediction():
    from random import randrange
    labels = ('Male','Female')
    choice = randrange(2)
    print(choice)
    if(choice==0):fg='blue'
    if(choice==1):fg='pink'
    sexPrediction.config(text="")
    sexPrediction.config(text=labels[choice],font=("Purisa",16,"bold"),fg=fg)



## Main

''' Fenetre et menu'''
root = tk.Tk()
# root.geometry("1000x800")
root.state('zoomed')
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
intro = tk.Label(root,text=" ",font=("Purisa",12,"bold"))
intro.grid(ipadx=2)
intro = tk.Label(root,text=" \t Sexing procedure of three-spined stickleback \n",font=("Purisa",12,"bold"))
intro.place(x=650,y=30,anchor=tk.CENTER)
''' Label explications '''
explanation = tk.Label(root,text="\n \n \n \n ")
explanation.grid(column=0,row=1)



''' Boutons '''


B = tk.Label(root, text = 'PREDICTION',font=("Purisa",12,"bold"),fg='blue')
B.place(x=460,y=50)
B = tk.Button(root,text = "Import image and autoplace",command = importImage,fg='blue')
B.place(x=400,y=80)
B = tk.Button(root,text = "Predict",command = affichePrediction,fg='blue')
B.place(x=570,y=80)
B = tk.Label(root, text = 'ADD THESE VALUES TO MODEL',font=("Purisa",12,"bold"),fg='green')
B.place(x=760,y=50)

B = tk.Button(root,text = "Model Update (developpers only)",command = HeadClass.genererAllDistancesHead,fg='green')
B.place(x=850,y=80)
B = tk.Label(root,text='Sex for model: ',fg='green')
B.place(x=725,y=85)
sexModel = tk.Entry(root,width=3)
sexModel.place(x=810,y=85)

sexPrediction = tk.Label(root,text="")
sexPrediction.place(x=650,y=145)

explanation = tk.Label(root,text="\n \n ")
explanation.grid(column=0,row=3)

''' Labels pour les longueurs de la tête '''
tk.Label(root,text="Longueurs caractéristiques de la tête : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=0,row=3)
Longueur = tk.Label(root,text="",justify=tk.LEFT)
Longueur.grid(column=0,row=4)


''' Labels pour les longueurs du corps '''
tk.Label(root,text="Longueurs caractéristiques du corps : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=1,row=3)
LongueurBody = tk.Label(root,text="",justify=tk.LEFT)
LongueurBody.grid(column=1,row=4)


''' Canvas pour la tête '''
canvas = tk.Canvas(root,bg='#f0f0f0',bd=0)
canvas.config(width=600, height=500)
canvas.grid(column=0,row=8)


''' Canvas pour le corps '''
canvas1 = tk.Canvas(root,bg='#f0f0f0')
canvas1.config(width=1000, height=500)
canvas1.grid(column=1,row=8)

root.mainloop()
#
# import inspect
# src_file_path = inspect.getfile(lambda: None)
# print(inspect.stack()[0][1])

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

