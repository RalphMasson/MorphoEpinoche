from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import pandas as pd

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


    def train(self):
        """!
            Train with RF & SVC
        """

        self.clf=RandomForestClassifier(n_estimators=200)
        self.clf.fit(self.X_train,self.y_train)
        print(self.clf.score(self.X_train,self.y_train))
        print(self.clf.score(self.X_test,self.y_test))

        self.clf1 = make_pipeline(StandardScaler(), SVC(gamma='auto'))
        self.clf1.fit(self.X_train,self.y_train)
        print(self.clf1.score(self.X_train,self.y_train))
        print(self.clf1.score(self.X_test,self.y_test))



    def predict():
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