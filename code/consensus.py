
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, recall_score, accuracy_score, precision_score, confusion_matrix

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold,learning_curve,ShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,LabelBinarizer
from sklearn.svm import SVC
from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, recall_score, accuracy_score, precision_score, confusion_matrix
from sklearn.feature_selection import SelectFromModel,RFE,SelectKBest, chi2
import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
from sklearn.ensemble import GradientBoostingClassifier
import sys,inspect
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)

import testIA_sexage

csv = r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\bdd_v0.csv"
bdd = pd.read_csv(csv,encoding="latin-1",delimiter=";")

y = bdd['Sexe']
X = bdd.drop(bdd.columns[0],axis=1)
X2 = bdd.drop(bdd.columns[0],axis=1)
X2[X2.columns[1:]] = X2[X2.columns[1:]].div(X2['LS'].values,axis=0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5,stratify=y)

from joblib import dump, load

clf = load(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\GBClassifierFinal.joblib')
clf1 = load(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\SVCClassifierFinal.joblib')
clf2 = load(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models\XGBClassifierFinal.joblib')



def consensusModel(y_pred,y_pred1,y_pred2):
    y_consensus = []
    for i in range(len(y_pred)):
        if (y_pred[i]==y_pred1[i]==y_pred2[i]):
            y_consensus.append(y_pred[i])
        else:
            y_consensus.append(0.5)
    return y_consensus

def print_undetermined(y_consensus):
    print("Undetermined : "+str(round(100*y_consensus.count(0.5)/len(y_consensus),2))+"%")
    return round(100*y_consensus.count(0.5)/len(y_consensus),2)

def print_misclassified(y_consensus,y_test):
    err = 0
    for i in range(len(y_consensus)):
        if y_consensus[i]==0.5:
            None
        else:
            if y_consensus[i]!=list(y_test)[i]:
                err+=1
            else:
                None
    print("Misclassified : "+str(100*err/len(y_consensus))+"%")
    return 100*err/len(y_consensus)

missed = []
undetermined = []
for i in range(1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,stratify=y)
    y_pred = clf.predict(X_test)
    y_pred1 = clf1.predict(X_test)
    y_pred2 = clf2.predict(X_test)
    y_consensus = consensusModel(y_pred,y_pred1,y_pred2)
    missed.append(100-print_misclassified(y_consensus,y_test))
    undetermined.append(print_undetermined(y_consensus))



df = pd.DataFrame({'% of correctly classified individuals':missed})
df['% of undetermined individuals']=undetermined

import seaborn as sns
sns.boxplot(data=df)
plt.title("Results of consensus model (1000 runs)")
plt.ylim([0,102])
plt.show()
