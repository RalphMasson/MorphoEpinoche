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
from datetime import timedelta,datetime,date
import XY_tools,IA_sexage
import IA_morph as ML
import io,os,time,dlib,easygui
from contextlib import redirect_stdout

# Classe pour les points de la tête

class Temp():
    chemin = ""

class ModelPoints():
    """!
        Classe de préparation du modèle Regression Trees pour la détection des
        points par Machine Learning
    """

    def __init__(self):
        """!
            Constructeur de la classe
                Example : a = ModelPoints()
        """
        self.pointsML = [[0,0]]*10

    def instantiate(self):
        """!
            Créer le modèle
        """
        ModelPoints.pointsML = ML.ML_pointage(InterfacePoint.modele_path,"")

    def split(self):
        """!
            Sépare les données en train / test
        """
        ModelPoints.pointsML.preprocess_folder(InterfacePoint.imagefolder_path,InterfacePoint.tpsfile_path)

    def options(self):
        """!
            Règle les paramètres d'entrainement
            @return a : liste des options choisies
        """
        #1e
        a = ModelPoints.pointsML.parameter_model([500,3],0.08,1,20,700,20,200)

        #2e
        # a = ModelPoints.pointsML.parameter_model([500,4],0.08,1,20,800,20,300)

        # # # #3e
        # a = ModelPoints.pointsML.parameter_model([500,4],0.08,1,20,1000,20,300)

        #4e
        # a = ModelPoints.pointsML.parameter_model([500,4],0.08,1,20,1200,20,300)


        return a

    def train(self):
        """!
            Entraine le modèle
        """
        ModelPoints.pointsML.train_model(InterfacePoint.trainfolder_path)

class ModelSexage():
    """!
        Classe de préparation du modèle Regression Trees pour la classification des
        poissons par Machine Learning
    """

    def __init__(self):
        """!
            Constructeur de la classe
                Example : a = ModelSexage()
        """

        self.pointsML = [[0,0]]*10

    def instantiate(self):
        """!
            Créer le modèle
        """
        ModelSexage.sexage = IA_sexage.Prediction(InterfaceGender.csv_path)


    def split(self):
        """!
            Sépare les données en train / test
        """
        ModelSexage.sexage.preprocess()

    def options(self):
        """!
            Règle les paramètres d'entrainement
        """
        ModelSexage.sexage.parameters()
        ModelSexage.list1 = list(ModelSexage.sexage.clf.get_params().keys())
        ModelSexage.list2 = list(ModelSexage.sexage.clf.get_params().values())
        ModelSexage.list3 = list(ModelSexage.sexage.clf1.get_params().keys())
        ModelSexage.list4 = list(ModelSexage.sexage.clf1.get_params().values())
        ModelSexage.list5 = list(ModelSexage.sexage.clf2.get_params().keys())
        ModelSexage.list6 = list(ModelSexage.sexage.clf2.get_params().values())
    def train(self):
        """!
            Entraine le modèle
        """
        ModelSexage.sexage.train()

    def accuracyTrain(self):
        """!
            Calcule le score d'entrainement des modèles
            @return acc1 : float (0<acc1<1)
            @return acc2 : float (0<acc2<2)
        """
        acc1 = ModelSexage.sexage.clf.score(ModelSexage.sexage.X_train,ModelSexage.sexage.y_train)
        acc2 = ModelSexage.sexage.clf1.score(ModelSexage.sexage.X_train,ModelSexage.sexage.y_train)
        return acc1,acc2

    def accuracyTest(self):
        """!
            Calcule le score de test des modèles
            @return acc1 : float (0<acc1<1)
            @return acc2 : float (0<acc2<2)
        """
        acc1 = ModelSexage.sexage.clf.score(ModelSexage.sexage.X_test,ModelSexage.sexage.y_test)
        acc2 = ModelSexage.sexage.clf1.score(ModelSexage.sexage.X_test,ModelSexage.sexage.y_test)
        return acc1,acc2

class InterfacePoint(tk.Tk):

    def __init__(self, **kwargs):
        """!
        Constructeur de l'interface
        """
        rr = easygui.passwordbox(msg='Code',title="Landmarking Verification Code")
        while rr!="Pointage2021":
            rr = easygui.passwordbox(msg='Code',title="Landmarking Verification Code")
        super().__init__()
        self.state('zoomed')
        self.title("Sex Determination for Three Spined Stickleback")
        self.add_labels()
        self.add_buttons()
        self.add_entrys()


    def add_labels(self):
        tk.Label(self,text="Mise à jour du modèle Pointage (Regression Trees) \n",font=("Andalus",16,"bold")).pack(padx=5,pady=5)
        message = "RESPECTER L'ARCHITECTURE SUIVANTE : "
        message += "\n\n  📁 ModelePointage"
        message += "\n\t 📁version1"
        message += "\n\t 📁version2"
        message += "\n\t\t ➜v2.tps (fichier de pointage obtenu par tpsDig)"
        message += "\n\t\t 📁 all"
        message += "\n\t\t\t ➜IMG1.JPG"
        message += "\n\t\t\t ➜IMG2.JPG"

        tk.Label(self,text=message,justify=tk.LEFT).place(relx = 0.35,rely = 0.1)
        self.labelpathall = tk.Label(self,text="")
        self.labelpathall.place(relx = 0.3,rely = 0.12)
        self.labelpathmodel = tk.Label(self,text="")
        self.labelpathmodel.place(relx= 0.3,rely= 0.17)

        self.labelpathtps = tk.Label(self,text="")
        self.labelpathtps.place(relx=0.3,rely=0.22)

        message = "Pour ajouter des données au modèle v1 de placement de points :"
        message += "\n\n1) Avec tpsDig, pointez les nouvelles images sur tpsDig"
        message += "\n2) Avec tpsUtils, faites un append dans un nouveau fichier .tps"
        message += "\n3) Déplacer les images nouvelles dans le même dossier que les anciennes"
        tk.Label(self,text=message,justify=tk.LEFT,borderwidth=2,highlightthickness=1,bd=0,highlightbackground="black", highlightcolor="black").place(relx = 0.05,rely = 0.1)
        # tk.Label(self,text="cascade_depth (6-18)").place(relx=0.001,rely = 0.4)
        # tk.Label(self,text="tree_depth (2-8)").place(relx=0.001,rely = 0.44)
        # tk.Label(self,text="tree per cascade (500)").place(relx=0.001,rely = 0.48)
        # tk.Label(self,text="nu (0-1)").place(relx=0.001,rely = 0.52)
        # tk.Label(self,text="oversampling amout (0-50)").place(relx=0.001,rely = 0.56)
        # tk.Label(self,text="feature pool size (300-700)").place(relx=0.001,rely = 0.6)
        # tk.Label(self,text="split tests (10-30)").place(relx=0.001,rely = 0.64)


    def add_entrys(self):
        # self.EntryCascade = tk.StringVar(self)
        # self.CascadeDepth = tk.Entry(self,textvariable = self.EntryCascade).place(relx=0.12,rely=0.4,width = 60)
        # self.EntryTree= tk.StringVar(self)
        # self.TreeDepth = tk.Entry(self,textvariable = self.EntryTree).place(relx=0.12,rely=0.44,width = 60)
        # self.EntryTreeCascade = tk.StringVar(self)
        # self.TreeCascade = tk.Entry(self,textvariable = self.EntryTreeCascade).place(relx=0.12,rely=0.48,width = 60)
        # self.EntryNu = tk.StringVar(self)
        # self.Nu = tk.Entry(self,textvariable = self.EntryNu).place(relx=0.12,rely=0.52,width = 60)
        # self.EntryOS = tk.StringVar(self)
        # self.Oversampling = tk.Entry(self,textvariable = self.EntryOS).place(relx=0.12,rely=0.56,width = 60)
        # self.EntryFeaturePoolSize = tk.StringVar(self)
        # self.FeaturePoolSize = tk.Entry(self,textvariable = self.EntryFeaturePoolSize).place(relx=0.12,rely=0.6,width = 60)
        # self.EntrySplitTests = tk.StringVar(self)
        # self.SplitTests = tk.Entry(self,textvariable = self.EntrySplitTests).place(relx=0.12,rely=0.64,width = 60)
        print("toto")

    def add_buttons(self):
        self.boutonImageAll = tk.Button(self,text="1) Selectionner le dossier version2",command=self.getDirectoryModel).place(relx=0.05,rely=0.22)
        self.buttonTrain = tk.Button(self,text="2) Mettre à jour le modele",command=self.prepareModel).place(relx=0.05,rely=0.26)
        self.text = tk.Text(self,height=35, width=150)
        self.text.place(relx=0.18,rely=0.3)
        self.text.configure(state='disabled')
        # self.buttonOptions = tk.Button(self,text="Modifier options (leave blank to default)").place(relx = 0.02,rely = 0.35)

    def getDirectoryModel(self):
        InterfacePoint.modele_path = XY_tools.Externes.openfolder()+"/"
        InterfacePoint.imagefolder_path = InterfacePoint.modele_path + "all/"
        InterfacePoint.trainfolder_path = InterfacePoint.modele_path + "train.xml"
        InterfacePoint.tpsfile_path = InterfacePoint.modele_path + "v2.tps"
        print(InterfacePoint.modele_path)
        self.text.configure(state='normal')
        self.text.insert(1.0,"Vérification du path : "+str(InterfacePoint.modele_path)+"\n")
        self.text.update()
        self.text.configure(state='disabled')

    def prepareModel(self):

        a = ModelPoints()
        a.instantiate()
        self.text.configure(state='normal')
        self.text.insert("insert","\n#########################################")
        self.text.insert("insert","#########################################")
        self.text.insert("insert","\n\t\t\tModèle initialisé : "+str(date.today())+" "+str(datetime.now().time()))
        self.text.insert("insert","\n\n--> Nombre d'images : ")
        self.text.insert("insert",str(len(os.listdir(InterfacePoint.imagefolder_path))))
        self.text.update()
        a.split()
        self.text.insert("insert","\n\n--> Dossiers train / test crées : ")
        self.text.insert("insert",str(len(os.listdir(InterfacePoint.modele_path+"train")))+" images Train + ")
        self.text.insert("insert",str(len(os.listdir(InterfacePoint.modele_path+"test")))+" images Test")
        self.text.update()
        c = str(a.options())
        self.text.insert("insert","\n\n--> Options set :")
        for x in c[c.find("(")+1:c.find(")")].split(','):
            self.text.insert("insert","\t"+x+"\n")
        message = "\n\n--> Fitting trees..."
        self.text.insert("insert",message)
        message = "\n\n\t\t\tPLEASE WAIT UNTIL FINISHED !"
        self.text.insert("insert",message)
        self.text.update()
        start = time.time()
        a.train()
        end = time.time()
        self.text.insert("insert","\n\n--> Time elapsed : "+str(timedelta(seconds=round(end-start)))+" s")
        self.text.update()
        self.text.insert("insert","\n--> Apprentissage terminé\n--> Modèle mis à jour : ")
        self.text.update()
        self.text.insert("insert",str(round(int(os.path.getsize(InterfacePoint.modele_path+"predictor.dat"))/1048000))+" Mo")
        self.text.insert("insert","\n--> Training error: {}".format(round(dlib.test_shape_predictor(InterfacePoint.trainfolder_path,InterfacePoint.modele_path+"predictor.dat"),2)))
        self.text.insert("insert"," pixels")
        self.text.insert("insert","\n\t\t\tModèle finalisé : "+str(date.today())+" "+str(datetime.now().time()))
        self.text.insert("insert","\n#########################################")
        self.text.insert("insert","#########################################")
        self.text.update()
        self.text.configure(state='disabled')


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




class InterfaceGender(tk.Tk):

    def __init__(self, **kwargs):
        """!
        Constructeur de l'interface
        """
        rr = easygui.passwordbox(msg='Code',title="Sexing Verification Code")
        while rr!="Sexage2021":
            rr = easygui.passwordbox(msg='Code',title="Sexing Verification Code")
        super().__init__()
        self.state('zoomed')
        self.title("Sex Determination for Three Spined Stickleback")
        self.add_labels()
        self.add_buttons()

    def add_labels(self):
        """!
            Fonction pour ajouter les textes de l'interface
        """
        tk.Label(self,text="Mise à jour du modèle Sexage (Random Forest & SVM) \n",font=("Andalus",16,"bold")).pack(padx=5,pady=5)

    def add_buttons(self):
        """!
            Fonction pour ajouter les bouttons de l'interface
        """
        self.boutonImageAll = tk.Button(self,text="1) Import le fichier csv",command=self.getDirectoryModel).place(relx=0.05,rely=0.22)
        self.buttonTrain = tk.Button(self,text="2) Mettre à jour le modele",command=self.prepareModel).place(relx=0.05,rely=0.26)
        self.text = tk.Text(self,height=40, width=150)
        self.text.place(relx=0.18,rely=0.2)
        self.text.configure(state='disabled')
        # self.buttonOptions = tk.Button(self,text="Modifier options (leave blank to default)").place(relx = 0.02,rely = 0.35)

    def getDirectoryModel(self):
        """!
            Fonction pour avoir le chemin du dossier contenant le fichier csv
        """
        InterfaceGender.csv_path = XY_tools.Externes.opencsv()
        InterfaceGender.csv_folder = XY_tools.Externes.cheminAvant2(InterfaceGender.csv_path)
        self.text.configure(state='normal')
        self.text.insert("1.0","Vérification du path : "+str(InterfaceGender.csv_path)+"\n")
        self.text.update()
        self.text.configure(state='disabled')

    def prepareModel(self):
        """!
            Fonction pour preparer le modele
        """

        a = ModelSexage()
        a.instantiate()

        self.text.configure(state='normal')
        self.text.insert("insert","\n#########################################")
        self.text.insert("insert","#########################################")
        self.text.insert("insert","\n\t\t\tModèle initialisé : "+str(date.today())+" "+str(datetime.now().time()))

        a.split()
        a.options()

        list1 = list(ModelSexage.list1)
        list2 = list(ModelSexage.list2)
        list3 = list(ModelSexage.list3)
        list4 = list(ModelSexage.list4)
        list5 = list(ModelSexage.list5)
        list6 = list(ModelSexage.list6)

        self.text.insert("insert","\n\n--> Training with following parameters :\n\n")
        for i in range(len(list1)):
            self.text.insert("insert","\t"+str(list1[i]) + " : "+str(list2[i]))
            self.text.update()
        self.text.insert("insert","\n\n")
        for i in range(len(list3)):
            self.text.insert("insert","\t"+str(list3[i]) + " : "+str(list4[i]))
            self.text.update()
        self.text.insert("insert","\n\n")

        for i in range(len(list5)):
            self.text.insert("insert","\t"+str(list5[i]) + " : "+str(list6[i]))
            self.text.update()
        self.text.insert("insert","\n\n")


        start = time.time()
        a.train()
        end = time.time()

        self.text.insert("insert","\n\n--> Time elapsed : "+str(timedelta(seconds=round(end-start)))+" s")
        self.text.update()
        self.text.insert("insert","\n--> Apprentissage terminé")

        b = a.accuracyTrain()

        self.text.insert("insert","\n--> Modèle SVC mis à jour : "+XY_tools.Externes.sizeKoParent(InterfaceGender.csv_folder+"SVCClassifierFinalx.joblib"))
        self.text.insert("insert","\n--> Modèle GB mis à jour : "+XY_tools.Externes.sizeKoParent(InterfaceGender.csv_folder+"GBClassifierFinalx.joblib"))
        self.text.insert("insert","\n--> Modèle XGB mis à jour : "+XY_tools.Externes.sizeKoParent(InterfaceGender.csv_folder+"XGBClassifierFinalx.joblib"))

        # self.text.insert("insert","\n--> Training score: {}".format(a.accuracyTrain()))
        # self.text.insert("insert","\n--> Testing score: {}".format(a.accuracyTest()))

        self.text.insert("insert","\n\n\t\t\tModèle finalisé : "+str(date.today())+" "+str(datetime.now().time()))
        self.text.insert("insert","\n#########################################")
        self.text.insert("insert","#########################################")
        self.text.update()
        self.text.configure(state='disabled')


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


#
# app = Interface()
# app.mainloop()