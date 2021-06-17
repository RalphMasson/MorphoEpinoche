from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import pandas as pd
from joblib import dump, load

import sys,inspect,os
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)

import XY_tools

class Prediction():
    """!
        Classe de prediction du sexe du poisson par Machine Learning
        Nécessite d'avoir un modèle de prédiction des points et du sexe avec un image

        Adapted from :
            Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," doi: 10.1109/CVPR.2014.241.       2014
            Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" doi: 10.1016/j.imavis.2020.103976   2020
            Porto, Voje "ML-morph: [...] automated [...] landmarking of biological structures in images" 10.1111/2041-210X.13373      2020
            Irani, Allada.. "Highly versatile facial landmarks detection models using ensemble of regression trees with application"  2019
    """


    def __init__(self,bdd):
        """!
            Constructeur du prédicteur de sexe
            @param bdd chemin du fichier csv (default = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\rapports\\"
        """
        self.path = XY_tools.Externes.cheminAvant2(bdd)
        # print(bdd)
        self.bdd = pd.read_csv(bdd,delimiter=";")


    def preprocess(self):
        """!
            Récupère la base de données complète avec les distances, angles et sexe
            @param df dataframe
            @return Xtrain Xtest,yTrain yTest
        """

        self.X = self.bdd.drop('Sexe (0:F, 1:M)',axis=1)
        self.y = self.bdd[self.bdd.columns[0]]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3)


    def parameters(self):
        self.clf=RandomForestClassifier(n_estimators=2000)
        self.clf1 = make_pipeline(StandardScaler(), SVC(C=100,gamma=0.01,kernel='poly'))

    def train(self):
        """!
            Train with RF & SVC and exports models in path
            @param None
            @return None

        """

        self.clf.fit(self.X_train,self.y_train)
        print(self.path)
        print(self.clf.score(self.X_train,self.y_train))
        print(self.clf.score(self.X_test,self.y_test))
        dump(self.clf, self.path+"modelRF.joblib")


        self.clf1.fit(self.X_train,self.y_train)
        print(self.clf1.score(self.X_train,self.y_train))
        print(self.clf1.score(self.X_test,self.y_test))
        dump(self.clf1, self.path+"modelSVC.joblib")



    def predict(xPredict,modelRF,modelSVC):
        """!
            Load the 2 models of classification and makes the prediction
            @param distances of unknown fish
            @param modelRF : random forest classifier
            @param modelSVC : support vector machine classifier
            @return sex, color, probability
        """

        if(len(modelRF)!=0):
            clfRF = load(modelRF)
            clfSVC = load(modelSVC)
        from random import randrange,uniform
        labels = ('Male','Female')
        # choice = randrange(2)
        p = uniform(0,1)
        if(p>0.5):
            fg='blue'
            choice = 0
            p = p
        if(p<0.5):
            fg='red'
            choice = 1
            p = 1 - p
        return labels[choice],fg,p