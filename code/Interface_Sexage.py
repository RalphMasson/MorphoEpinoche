''' Module pour l'interface GUI '''

# Pour assurer le bon fonctionnement
import sys,inspect
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)

# Documentation

"""generate diagramm class : script.ps1"""
"""use ml-morph : ..."""
"""articles :
* file:///C:/Users/MASSON/Downloads/Admixture_mapping_of_male_nuptial_color_and_body_s.pdf
* https://condor.depaul.edu/~waguirre/Aguirre_et_al_08_RS.pdf
* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3183875/
* file:///C:/Users/MASSON/Downloads/KitanoetalCopeia.pdf
* https://jeb.biologists.org/content/216/5/835
* file:///C:/Users/MASSON/Downloads/Environ.Biol.Fish.2005.pdf
* file:///C:/Users/MASSON/Downloads/_journals_njz_28_3-4_article-p524_5-preview.pdf
* https://www.researchgate.net/figure/Morphological-characters-measured-from-the-left-side-of-each-fish-1-fork-length-2-jaw_fig2_233726301
* https://www.researchgate.net/figure/Morphometric-analysis-of-body-shape-and-its-association-with-colour-a-The-20-numbered_fig3_225288970
* https://journals.plos.org/plosone/article/figure?id=10.1371/journal.pone.0021060.g001
* https://docs.google.com/presentation/d/1HZcpJerbqx9Z-llRNlb6E30YXBvOnMuJ/edit#slide=id.p12
"""


# Import des bibliothèques (s'assurer qu'elles soient installées)
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import math,functools,itertools,os,cv2,webbrowser
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
        @param canvas tk.Canvas : cadre de l'image
        """
        for id in HeadClass.id_polygons:
            liste = canvas.coords(id)
            if(len(canvas.coords(id))==18):HeadClass.pointsFish=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]
            if(len(canvas.coords(id))==4):HeadClass.pointsEchelle=[(liste[i],liste[i+1]) for i in range(0,len(liste),2)]

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
        # HeadClass.distances_all = Fonctions.Externes.genererAllDistancesHead(HeadClass.pointsEchelle,HeadClass.pointsFish,Interface.sexModele.get(),pypath)
        Fonctions.Externes.genererAllDistancesHead(HeadClass.pointsEchelle,HeadClass.pointsFish,Interface.sexModele.get(),pypath3)

        Fonctions.Externes.nbClic +=1

    def calculDistances():
        """!
        Methode pour calculer certaines distances caractéristiques
        """
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
        """!
        Constructeur de l'image de la tete
        @param canvas tk.Canvas : cadre de l'image
        @param PIL_image list : matrice de l'image format PIL
        @param cv2_image list : matrice de l'image format cv2
        @param size list : dimension souhaitée de l'image
        """
        self.img = ImageTk.PhotoImage(PIL_image.resize(size, Image.ANTIALIAS))
        self.circle = Placement.Points.detect_eye(cv2.resize(CV2_image,size,Image.ANTIALIAS))
        HeadFish.centreOeil = [self.circle[0],self.circle[1]]
        HeadFish.poisson = canvas.create_image(0, 0, anchor=tk.NW,image=self.img)
        HeadFish.CV2_image_big = CV2_image
        canvas.move(HeadFish.poisson,-(self.circle[0]-300),-(self.circle[1]-250))
        app.bind("<Left>",self.moveLeft)
        app.bind("<Right>",self.moveRight)
        app.bind("<Up>",self.moveUp)
        app.bind("<Down>",self.moveDown)
    def moveLeft(self,event):
        """!
        Méthode pour déplacer l'image à gauche
        @param event : event
        """
        canvas.move(HeadFish.poisson,-10,0)
    def moveRight(self,event):
        """!
        Méthode pour déplacer l'image à droite
        @param event : event
        """
        canvas.move(HeadFish.poisson,10,0)
    def moveUp(self,event):
        """!
        Méthode pour déplacer l'image en haut
        @param event : event
        """
        canvas.move(HeadFish.poisson,0,-10)
    def moveDown(self,event):
        """!
        Méthode pour déplacer l'image en bas
        @param event : event
        """
        canvas.move(HeadFish.poisson,0,10)

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


class Interface(tk.Tk):
    sexModele = None

    def __init__(self):
        """!
        Constructeur de l'interface
        """

        super().__init__()

        ''' Fenetre et menu'''
        # root = tk.Tk()
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


        menuAide = tk.Menu(menubar, tearoff=0)
        menuAide.add_command(label="A propos", command=self.help,accelerator="(Ctrl+I)")
        self.bind_all("<Control-i>",lambda e : self.help())
        menuAide.add_command(label="Télécharger la dernière version",command=Interface.updateVersion)
        menubar.add_cascade(label="Aide", menu=menuAide)


        self.config(menu=menubar)
        self.listeImages = []
        CV2_image_big = None
        ''' Label Intro de presentation'''
        tk.Label(self,text=" ",font=("Purisa",12,"bold")).grid(ipadx=2)
        tk.Label(self,text=" Sexing procedure of three-spined stickleback \n",font=("Andalus",16,"bold")).place(x=750,y=40,anchor=tk.CENTER)
        tk.Label(self,text="\n \n \n \n ").grid(column=0,row=1)

        ''' Boutons '''
        tk.Label(self, text = 'PREDICTION',font=("Purisa",12,"bold"),fg='purple').place(x=460,y=70)
        self.boutonImport = tk.Button(self,text = "Import image and autoplace",command = self.importImage,fg='purple')
        self.boutonImport.place(x=400,y=100)
        self.boutonImport.bind('<Control-o>',self.importImage)
        tk.Button(self,text = "Predict",command = Interface.affichePrediction,fg='purple').place(x=570,y=100)
        tk.Label(self, text = 'ADD THESE VALUES TO MODEL',font=("Purisa",12,"bold"),fg='green').place(x=760,y=70)
        Interface.sexModele = tk.StringVar(self)
        self.sexModel = tk.Entry(self,width=3,textvariable=Interface.sexModele)
        self.sexModel.place(x=810,y=105)
        tk.Button(self,text = "Model Update (close Excel before)",command = HeadClass.genererAllDistancesHead,fg='green').place(x=850,y=100)
        tk.Label(self,text='Sex for model: ',fg='green').place(x=725,y=105)
        self.boutonPrevious = tk.Button(self,text='<--',command = self.previousImage)
        self.boutonPrevious.place(x=570,y=780)
        self.boutonNext = tk.Button(self,text='-->',command = self.nextImage)
        self.boutonNext.place(x=610,y=780)




        self.labelSex = tk.Label(self,text="")
        self.labelSex.place(x=650,y=190)

        self.labelInfoPoints = tk.Label(self,text="")
        self.labelInfoPoints.place(x=650,y=160)

        self.labelVide = tk.Label(self,text="\n ")
        self.labelVide.grid(column=0,row=3)

        self.labelNumImage = tk.Label(self,text="Image :",font=("Purisa",11),fg='gray')
        self.labelNumImage.place(x=650,y=780)
        self.labelNomImage = tk.Label(self,text="",font=("Purisa",11),fg='gray')
        self.labelNomImage.place(x=760,y=780)

        ''' Labels pour les longueurs de la tête '''
        tk.Label(self,text="Longueurs caractéristiques de la tête : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=0,row=4)
        self.labelLongueur = tk.Label(self,text="",justify=tk.LEFT)
        self.labelLongueur.grid(column=0,row=5)
        self.numImageActuelle = 0

        ''' Labels pour les longueurs du corps '''
        tk.Label(self,text="Longueurs caractéristiques du corps : \n",justify=tk.LEFT,font=("Purisa",8,"bold","underline")).grid(column=1,row=4)
        self.labelLongueurBody = tk.Label(self,text="",justify=tk.LEFT)
        self.labelLongueurBody.grid(column=1,row=5)

        ''' Canvas pour la tête '''
        self.canvasTete = tk.Canvas(self,bg='#f0f0f0',bd=0,highlightthickness=1, highlightbackground="black")
        self.canvasTete.config(width=600, height=500)
        self.canvasTete.grid(column=0,row=8)

        ''' Canvas pour le corps '''
        self.canvasCorps = tk.Canvas(self,bg='#f0f0f0',highlightthickness=1, highlightbackground="black")
        self.canvasCorps.config(width=960, height=500)
        self.canvasCorps.grid(column=1,row=8)

        """Canvas pour logo"""
        pathLogo = Interface.resource_path("logo2.png")
        self.canvasLogo = tk.Canvas(self,bg='#f0f0f0')
        self.canvasLogo.config(width=157,height=84)
        self.canvasLogo.place(x=0,y=0)
        self.imgLogo = ImageTk.PhotoImage(Image.open(pathLogo).resize((157,84)))
        self.canvasLogo.create_image(0, 0, anchor=tk.NW,image=self.imgLogo)

        ''' Canvas pour le schema '''
        pathSchema = Interface.resource_path("schema.png")
        self.canvasSchema = tk.Canvas(self,bg='#f0f0f0')
        self.canvasSchema.config(width = 288,height=192)
        self.canvasSchema.place(x=1250,y=0)
        self.imgSchema = ImageTk.PhotoImage(Image.open(pathSchema).resize((288,192)))
        self.canvasSchema.create_image(0,0,anchor=tk.NW,image=self.imgSchema)

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

        return os.path.join(base_path, relative_path)

    def afficheLongueur():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs dans l'interface
        """
        app.labelLongueur.config(text=Fonctions.Externes.Longueur(HeadClass.calculDistances()))

    def afficheLongueurBody():
        """!
        Méthode permettant de mettre à jour l'affichage des longueurs du corps dans l'interface
        """
        app.labelLongueurBody.config(text=Fonctions.Externes.LongueurBody(BodyClass.calculDistances()))

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
        self.listeImages = Fonctions.Externes.openfn()
        self.calculPoints()


    def calculPoints(self):
        """!
        Méthode permettant de calculer les points et de les disposer sur l'image
        """
        nbPointNonDetectes = 0
        print("### Initialisation ###")
        tete,echelle10mm,echelle3mm = Placement.Points.randomPointsBis()
        pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19 = tete
        self.clearAllCanvas()

        print(self.numImageActuelle)

        ImagePIL = Image.open(self.listeImages[self.numImageActuelle])
        app.labelNomImage.config(text=self.listeImages[self.numImageActuelle])
        app.labelNumImage.config(text=str(self.numImageActuelle+1)+"/"+str(len(self.listeImages)))

        ''' Resize pour le corps '''
        print("\n### Traitement du corps ###")
        corpsStandard,newPIL_image,left = Placement.Points.ImageCorps(ImagePIL)
        BodyFish(self.canvasCorps,newPIL_image,(1300,975))
        self.canvasCorps.move(BodyFish.poisson,-(left[0]-50),-(left[1]-280))
        self.canvasCorps.update()
        print("### OK ###")

        ''' Resize pour la tête '''
        print("\n### Traitement de la tête 1/3 ### ")
        PIL_image_big,CV2_image_big,left1,right1 = Placement.Points.ImageTete(self.listeImages,self.numImageActuelle)
        HeadFish(self.canvasTete,PIL_image_big,CV2_image_big,(3500,2625))
        self.canvasTete.update()
        print("### OK ###")

        print("\n### Alignement des points sur le corps'  ###")
        corpsStandard = [[x[0]-(left[0]-50),x[1]-(left[1]-280)] for x in corpsStandard]
        echelle10mm = [[x[0]-(left[0]-250),x[1]-(left[1]-350)] for x in echelle10mm]
        BodyClass(self.canvasCorps, echelle10mm,'red')
        BodyClass(self.canvasCorps,corpsStandard,'cyan')
        self.canvasCorps.update()
        print("### OK ###")

        ''' Initialisation des points 3 et 19 par détection auto '''
        print("\n### Calcul des points 3 et 19 ###")
        try:
            [pt3,pt19]=Placement.Points.points3_19(CV2_image_big)
            pt3 = [pt3[0],pt3[1]]
            pt19 = [pt19[0],pt19[1]]
        except:
            print("Impossible de déterminer les points 3 et 19")
            nbPointNonDetectes+=2
        # [pt3,pt19]=Placement.Points.points3_19(CV2_image_big)
        # pt3 = [pt3[0],pt3[1]]
        # pt19 = [pt19[0],pt19[1]]
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
        print("\n### Calcul des points 15 et 13 ###")
        # pt15,pt13=Placement.Points.points15_13(CV2_image_big,pt19,left1,right1)
        try:
            pt15,pt13=Placement.Points.points15_13(CV2_image_big,pt19,left1,right1)
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

        tete = Fonctions.Externes.centerPoints([pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19],HeadFish.centreOeil)

        print("\n### Placement des points de la tête ###")
        HeadClass(self.canvasTete, tete,'#ff00f2')
        HeadClass(self.canvasTete,echelle3mm,'red')
        print("### OK ###")
        app.labelInfoPoints.config(text=str(13-nbPointNonDetectes)+" points détectés / 13 ")

    def affichePrediction():
        """!
        Méthode permettant d'afficher la prédiction du sexe
        """
        choix,couleur,p = Classification.Prediction.predict()
        app.labelSex.config(text="")
        app.labelSex.config(text=choix+" avec p="+str(round(p,2)),font=("Purisa",16),fg=couleur)

    def nextImage(self):
        """!
        Méthode permettant de passer à l'image d'après
        """
        import time
        if(self.numImageActuelle<len(self.listeImages)):
            self.unbind_all("<Control-Return>")
            self.unbind_all("<Control-BackSpace>")
            self.numImageActuelle+=1
            nbPointNonDetectes = 0
            time.sleep(0.3)
            self.boutonNext.configure(state=tk.DISABLED)
            self.boutonPrevious.configure(state=tk.DISABLED)
            self.calculPoints()
            time.sleep(0.3)
            self.boutonNext.configure(state=tk.ACTIVE)
            self.boutonPrevious.configure(state=tk.ACTIVE)
            self.bind_all("<Control-Return>",lambda e : self.nextImage())
            self.bind_all("<Control-BackSpace>",lambda e : self.previousImage())


    def previousImage(self):
        """!
        Méthode permettant de revenir a l'image précédente
        """
        import time
        if(self.numImageActuelle>0):
            self.unbind_all("<Control-Return>")
            self.unbind_all("<Control-BackSpace>")
            self.numImageActuelle-=1
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
        message = "PROCEDURE DE SEXAGE DE L'EPINOCHE v1.2"
        message += "\n\n- Modèle de placement de points par traitement d'image et par Machine Learning (learning : 150 individus)"
        message += "\n\n- Modèle de classification Male/Femelle par Machine Learning (learning : 300 individus)"
        message += "\n\n\n Interface développée par R. Masson pour l'INERIS"
        tk.messagebox.showinfo(title="Informations",message=message)

app = Interface()
# app.iconphoto(False,tk.PhotoImage(file=Interface.resource_path("icon.png")))
app.mainloop()


