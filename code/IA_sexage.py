from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.datasets import make_classification
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
from joblib import dump, load
import xgboost
import sys,inspect,os
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)

pathPython = r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\DEPLOIEMENT_INERIS_2021\\"

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
        self.bdd = pd.read_csv(bdd,encoding="latin-1",delimiter=";")



    def preprocess(self):
        """!
            Récupère la base de données complète avec les distances, angles et sexe
            @param df dataframe
            @return Xtrain Xtest,yTrain yTest
        """
        print(self.bdd)
        self.X = self.bdd.drop('Sexe',axis=1)
        self.y = self.bdd[self.bdd.columns[0]]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2,stratify = self.y)

    def parameters(self):

        self.clf = SVC(C= 10, break_ties= False, cache_size= 200, class_weight= None, coef0= 0.0, decision_function_shape= 'ovr', degree= 3, gamma=0.001, kernel= 'poly', max_iter= -1, probability= True, random_state= None, shrinking= True, tol= 0.001, verbose=False)


        self.clf1 = GradientBoostingClassifier(ccp_alpha= 0.0, criterion= 'friedman_mse', init= None, learning_rate= 0.03, loss= 'deviance', max_depth= 4, max_features= None, max_leaf_nodes= None, min_impurity_decrease= 0.0, min_impurity_split= None, min_samples_leaf= 1, min_samples_split=2, min_weight_fraction_leaf= 0.0, n_estimators= 500, n_iter_no_change= None, random_state= None, subsample=0.618, tol= 0.0001, validation_fraction=0.1, verbose= 0, warm_start= False)

        self.clf2 = xgboost.XGBClassifier(use_label_encoder=False,objective="binary:logistic",eval_metric='mlogloss', random_state=42,nthread=4,colsample_bytree = 0.6,gamma = 1.5,max_depth = 5,min_child_weight = 1,n_estimators = 500,subsample = 0.6)

    def train(self):
        """!
            Train & exports models in path
            @param None
            @return None

        """

        self.clf.fit(self.X_train,self.y_train)

        self.clf1.fit(self.X_train,self.y_train)

        self.clf2.fit(self.X_train,self.y_train)

        dump(self.clf, self.path+"SVCClassifierFinalx.joblib")

        dump(self.clf1, self.path+"GBClassifierFinalx.joblib")

        dump(self.clf2, self.path+"XGBClassifierFinalx.joblib")



    def load_models(modeleDistances):
        from joblib import dump, load
        import pandas as pd
        import numpy as np
        predictorGB = "GBClassifierFinal3.joblib"
        predictorSVC = "SVCClassifierFinal3.joblib"
        predictorXGB = "XGBClassifierFinal3.joblib"
        try:
            clf = load(os.path.join(sys._MEIPASS,predictorGB))
            clf1 = load(os.path.join(sys._MEIPASS,predictorSVC))
            clf2 = load(os.path.join(sys._MEIPASS,predictorXGB))
        except:
            clf = load(pathPython+'models'+'\\'+predictorGB)
            clf1 = load(pathPython+'models'+'\\'+predictorSVC)
            clf2 = load(pathPython+'models'+'\\'+predictorXGB)

        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', None)
        ae = pd.DataFrame(modeleDistances).T
        # print(ae)
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

            #get minority vote
            majorityVote = max(set(listePredictionInt), key = listePredictionInt.count)
            if majorityVote==0:
                majorityVoteStr = "F"
            if majorityVote==1:
                majorityVoteStr = "M"

            minorityVote = min(set(listePredictionInt), key = listePredictionInt.count)
            indexMinorityVote = listePredictionInt.index(min(set(listePredictionInt), key = listePredictionInt.count))

            if minorityVote==0:
                minorityVoteStr = "F"
            if minorityVote==1:
                minorityVoteStr = "M"

            probaMinMajority = []
            for i in range(len(listePredictionInt)):
                if (listePredictionInt[i]==majorityVote):
                    probaMinMajority.append(listeProba[i][majorityVote])
            probaMinMajority = min(probaMinMajority)>0.8


            if majorityVote==0:
                consensusStr = "F"
            else:
                if (listeProba[indexMinorityVote][minorityVote]<0.67):
                    if probaMinMajority:
                        consensusStr = "Undetermined (possibly "+majorityVoteStr+" )"
                else:
                    consensusStr = "Undetermined"





        text = ""
        for i in range(3):
            text += listePredictionStr[i]+" "+str(listeProba[i][listePredictionInt[i]])+";"
        text+="--> "+consensusStr
        return text,ae,proba