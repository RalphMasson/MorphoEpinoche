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


    def load_models(modeleDistances):
        from joblib import dump, load
        import pandas as pd
        import numpy as np
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
        ae = pd.DataFrame(modeleDistances).T
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
        return text,ae,proba