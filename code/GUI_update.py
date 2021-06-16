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
import XY_tools
import IA_morph as ML
import io,os,time,dlib
from contextlib import redirect_stdout

# Classe pour les points de la tête

class Temp():
    chemin = ""

class ModelPoints():

    def __init__(self):
        self.pointsML = [[0,0]]*10

    def instantiate(self):
        """!
        Récupère les coordonnées par machine learning
        @param path_model dossier où se trouve le modele regression trees
            (default = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\img\\")
        @param path_image dossier où se trouve le dossier de l'image à pointer
            (default = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\img\\test\\")
        The list is expected to be ordered
        """
        ModelPoints.pointsML = ML.ML_pointage(InterfacePoint.modele_path,"")

    def split(self):
        ModelPoints.pointsML.preprocess_folder(InterfacePoint.imagefolder_path,InterfacePoint.tpsfile_path)

    def options(self):
        a = ModelPoints.pointsML.parameter_model([500,3],1,2,6,700,20,500)
        return a

    def train(self):
        print(InterfacePoint.trainfolder_path)


        with io.StringIO() as buf, redirect_stdout(buf):

            ModelPoints.pointsML.train_model(InterfacePoint.trainfolder_path)
            output = buf.getvalue()
            return output

class InterfacePoint(tk.Tk):
    sexModele = None
    app = None
    chemin = ""
    version = 1.6
    modele_path = ""
    imagefolder_path = ""
    tpsfile_path = ""

    def __init__(self, **kwargs):
        """!
        Constructeur de l'interface
        """
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
        tk.Label(self,text="cascade_depth (6-18)").place(relx=0.001,rely = 0.4)
        tk.Label(self,text="tree_depth (2-8)").place(relx=0.001,rely = 0.44)
        tk.Label(self,text="tree per cascade (500)").place(relx=0.001,rely = 0.48)
        tk.Label(self,text="nu (0-1)").place(relx=0.001,rely = 0.52)
        tk.Label(self,text="oversampling amout (0-50)").place(relx=0.001,rely = 0.56)
        tk.Label(self,text="feature pool size (300-700)").place(relx=0.001,rely = 0.6)
        tk.Label(self,text="split tests (10-30)").place(relx=0.001,rely = 0.64)


    def add_entrys(self):
        self.EntryCascade = tk.StringVar(self)
        self.CascadeDepth = tk.Entry(self,textvariable = self.EntryCascade).place(relx=0.12,rely=0.4,width = 60)
        self.EntryTree= tk.StringVar(self)
        self.TreeDepth = tk.Entry(self,textvariable = self.EntryTree).place(relx=0.12,rely=0.44,width = 60)
        self.EntryTreeCascade = tk.StringVar(self)
        self.TreeCascade = tk.Entry(self,textvariable = self.EntryTreeCascade).place(relx=0.12,rely=0.48,width = 60)
        self.EntryNu = tk.StringVar(self)
        self.Nu = tk.Entry(self,textvariable = self.EntryNu).place(relx=0.12,rely=0.52,width = 60)
        self.EntryOS = tk.StringVar(self)
        self.Oversampling = tk.Entry(self,textvariable = self.EntryOS).place(relx=0.12,rely=0.56,width = 60)
        self.EntryFeaturePoolSize = tk.StringVar(self)
        self.FeaturePoolSize = tk.Entry(self,textvariable = self.EntryFeaturePoolSize).place(relx=0.12,rely=0.6,width = 60)
        self.EntrySplitTests = tk.StringVar(self)
        self.SplitTests = tk.Entry(self,textvariable = self.EntrySplitTests).place(relx=0.12,rely=0.64,width = 60)


    def add_buttons(self):
        self.boutonImageAll = tk.Button(self,text="1) Selectionner le dossier version2",command=self.getDirectoryModel).place(relx=0.05,rely=0.22)
        self.buttonTrain = tk.Button(self,text="2) Mettre à jour le modele",command=self.prepareModel).place(relx=0.05,rely=0.26)
        self.text = tk.Text(self,height=35, width=150)
        self.text.place(relx=0.18,rely=0.3)
        self.text.configure(state='disabled')
        self.buttonOptions = tk.Button(self,text="Modifier options (leave blank to default)").place(relx = 0.02,rely = 0.35)

    def getDirectoryModel(self):
        InterfacePoint.modele_path = XY_tools.Externes.openfolder()+"/"
        InterfacePoint.imagefolder_path = InterfacePoint.modele_path + "all/"
        InterfacePoint.trainfolder_path = InterfacePoint.modele_path + "train.xml"
        InterfacePoint.tpsfile_path = InterfacePoint.modele_path + "v2.tps"
        print(InterfacePoint.modele_path)

    def prepareModel(self):

        a = ModelPoints()
        a.instantiate()
        self.text.configure(state='normal')
        self.text.insert(1.0,"\t\t\tModèle initialisé : "+str(date.today())+" "+str(datetime.now().time()))
        self.text.insert("insert","\nNombre d'images : ")
        self.text.insert("insert",str(len(os.listdir(InterfacePoint.imagefolder_path))))
        self.text.insert("insert","\nVérification du path : "+str(InterfacePoint.modele_path))
        self.text.update()
        a.split()
        self.text.insert("insert","\n\nDossiers train / test crées")
        self.text.insert("insert","\n\t"+str(len(os.listdir(InterfacePoint.modele_path+"train")))+" images Train")
        self.text.insert("insert","\n\t"+str(len(os.listdir(InterfacePoint.modele_path+"test")))+" images Test")
        self.text.update()
        optionSet = a.options()
        self.text.insert("insert","\n\nOptions set :")
        message = "\n\tTraining with cascade depth : "+str(optionSet.cascade_depth)
        message = "\n\tTraining with tree depth :"+str(optionSet.tree_depth)
        message = "\n\tTraining with "+str(optionSet.num_trees_per_cascade_level)+" trees per cascade level."
        message = "\n\tTraining with nu : "+str(optionSet.nu)
        message = "\n\tTraining with oversampling amount : "+str(optionSet.oversampling_amount)
        message = "\n\tTraining with oversampling translation jitter : "+str(optionSet.oversampling_translation_jitter)
        message = "\n\tTraining with feature pool size : "+str(optionSet.feature_pool_size)
        message = "\n\tTraining with "+str(optionSet.num_threads)+" threads"
        message = "\n\tTraining with lambda_param: "+str(optionSet.lambda_param)
        message = "\n\tTraining with "+str(optionSet.num_test_splits)+" split tests."
        message = "\nFitting trees..."
        message = "\n\n\t\t\tPLEASE WAIT UNTIL FINISHED !"
        self.text.insert("insert",message)
        self.text.update()
        start = time.time()
        a.train()
        end = time.time()
        self.text.insert("insert"," Time elapsed : "+str(timedelta(seconds=round(end-start)))+" s")
        self.text.update()
        self.text.insert("insert","\n\nApprentissage terminé")
        self.text.insert("insert","\nModèle mis à jour : ")
        self.text.update()
        self.text.insert("insert",str(round(int(os.path.getsize(InterfacePoint.modele_path+"predictor.dat"))/1048000))+" Mo")
        self.text.insert("insert","\nTraining error: {}".format(round(dlib.test_shape_predictor(InterfacePoint.trainfolder_path, "predictor.dat"),2)))
        self.text.insert("insert"," pixels")
        self.text.insert("insert","\n\n\t\t\tModèle finalisé : "+str(date.today())+" "+str(datetime.now().time()))
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
    sexModele = None
    app = None
    chemin = ""
    version = 1.6
    modele_path = ""
    imagefolder_path = ""
    tpsfile_path = ""

    def __init__(self, **kwargs):
        """!
        Constructeur de l'interface
        """
        super().__init__()
        self.state('zoomed')
        self.title("Sex Determination for Three Spined Stickleback")
        self.add_labels()
        self.add_buttons()
        self.add_entrys()

    def add_labels(self):
        tk.Label(self,text="Mise à jour du modèle Sexage (Random Forest & SVM) \n",font=("Andalus",16,"bold")).pack(padx=5,pady=5)
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
        tk.Label(self,text="cascade_depth (6-18)").place(relx=0.001,rely = 0.4)
        tk.Label(self,text="tree_depth (2-8)").place(relx=0.001,rely = 0.44)
        tk.Label(self,text="tree per cascade (500)").place(relx=0.001,rely = 0.48)
        tk.Label(self,text="nu (0-1)").place(relx=0.001,rely = 0.52)
        tk.Label(self,text="oversampling amout (0-50)").place(relx=0.001,rely = 0.56)
        tk.Label(self,text="feature pool size (300-700)").place(relx=0.001,rely = 0.6)
        tk.Label(self,text="split tests (10-30)").place(relx=0.001,rely = 0.64)


    def add_entrys(self):
        self.EntryCascade = tk.StringVar(self)
        self.CascadeDepth = tk.Entry(self,textvariable = self.EntryCascade).place(relx=0.12,rely=0.4,width = 60)
        self.EntryTree= tk.StringVar(self)
        self.TreeDepth = tk.Entry(self,textvariable = self.EntryTree).place(relx=0.12,rely=0.44,width = 60)
        self.EntryTreeCascade = tk.StringVar(self)
        self.TreeCascade = tk.Entry(self,textvariable = self.EntryTreeCascade).place(relx=0.12,rely=0.48,width = 60)
        self.EntryNu = tk.StringVar(self)
        self.Nu = tk.Entry(self,textvariable = self.EntryNu).place(relx=0.12,rely=0.52,width = 60)
        self.EntryOS = tk.StringVar(self)
        self.Oversampling = tk.Entry(self,textvariable = self.EntryOS).place(relx=0.12,rely=0.56,width = 60)
        self.EntryFeaturePoolSize = tk.StringVar(self)
        self.FeaturePoolSize = tk.Entry(self,textvariable = self.EntryFeaturePoolSize).place(relx=0.12,rely=0.6,width = 60)
        self.EntrySplitTests = tk.StringVar(self)
        self.SplitTests = tk.Entry(self,textvariable = self.EntrySplitTests).place(relx=0.12,rely=0.64,width = 60)


    def add_buttons(self):
        self.boutonImageAll = tk.Button(self,text="1) Selectionner le dossier version2",command=self.getDirectoryModel).place(relx=0.05,rely=0.22)
        self.buttonTrain = tk.Button(self,text="2) Mettre à jour le modele",command=self.prepareModel).place(relx=0.05,rely=0.26)
        self.text = tk.Text(self,height=35, width=150)
        self.text.place(relx=0.18,rely=0.3)
        self.text.configure(state='disabled')
        self.buttonOptions = tk.Button(self,text="Modifier options (leave blank to default)").place(relx = 0.02,rely = 0.35)

    def getDirectoryModel(self):
        InterfaceGender.modele_path = XY_tools.Externes.openfolder()+"/"
        InterfaceGender.imagefolder_path = InterfaceGender.modele_path + "all/"
        InterfaceGender.trainfolder_path = InterfaceGender.modele_path + "train.xml"
        InterfaceGender.tpsfile_path = InterfaceGender.modele_path + "v2.tps"
        print(InterfaceGender.modele_path)
    def getFileTps(self):
        InterfaceGender.tpsfile_path = XY_tools.Externes.opentps()
        # self.labelpathtps.config(text=InterfaceGender.tpsfile_path)

        print(InterfaceGender.tpsfile_path)


    def prepareModel(self):

        a = ModelPoints()
        a.instantiate()
        self.text.configure(state='normal')
        self.text.insert(1.0,"\t\t\tModèle initialisé : "+str(date.today())+" "+str(datetime.now().time()))
        self.text.insert("insert","\nNombre d'images : ")
        self.text.insert("insert",str(len(os.listdir(InterfaceGender.imagefolder_path))))
        self.text.insert("insert","\nVérification du path : "+str(InterfaceGender.modele_path))
        self.text.update()
        a.split()
        self.text.insert("insert","\n\nDossiers train / test crées")
        self.text.insert("insert","\n\t"+str(len(os.listdir(InterfaceGender.modele_path+"train")))+" images Train")
        self.text.insert("insert","\n\t"+str(len(os.listdir(InterfaceGender.modele_path+"test")))+" images Test")
        self.text.update()
        optionSet = a.options()
        self.text.insert("insert","\n\nOptions set :")
        message = "\n\tTraining with cascade depth : "+str(optionSet.cascade_depth)
        message = "\n\tTraining with tree depth :"+str(optionSet.tree_depth)
        message = "\n\tTraining with "+str(optionSet.num_trees_per_cascade_level)+" trees per cascade level."
        message = "\n\tTraining with nu : "+str(optionSet.nu)
        message = "\n\tTraining with oversampling amount : "+str(optionSet.oversampling_amount)
        message = "\n\tTraining with oversampling translation jitter : "+str(optionSet.oversampling_translation_jitter)
        message = "\n\tTraining with feature pool size : "+str(optionSet.feature_pool_size)
        message = "\n\tTraining with "+str(optionSet.num_threads)+" threads"
        message = "\n\tTraining with lambda_param: "+str(optionSet.lambda_param)
        message = "\n\tTraining with "+str(optionSet.num_test_splits)+" split tests."
        message = "\nFitting trees..."
        message = "\n\n\t\t\tPLEASE WAIT UNTIL FINISHED !"
        self.text.insert("insert",message)
        self.text.update()
        start = time.time()
        a.train()
        end = time.time()
        self.text.insert("insert"," Time elapsed : "+str(timedelta(seconds=round(end-start)))+" s")
        self.text.update()
        self.text.insert("insert","\n\nApprentissage terminé")
        self.text.insert("insert","\nModèle mis à jour : ")
        self.text.update()
        self.text.insert("insert",str(round(int(os.path.getsize(InterfaceGender.modele_path+"predictor.dat"))/1048000))+" Mo")
        self.text.insert("insert","\nTraining error: {}".format(round(dlib.test_shape_predictor(InterfaceGender.trainfolder_path, "predictor.dat"),2)))
        self.text.insert("insert"," pixels")
        self.text.insert("insert","\n\n\t\t\tModèle finalisé : "+str(date.today())+" "+str(datetime.now().time()))
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