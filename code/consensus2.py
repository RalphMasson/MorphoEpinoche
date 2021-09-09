from joblib import dump, load
from sklearn.model_selection import train_test_split
import pandas as pd
csv = r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\bdd_v0.csv"
bdd = pd.read_csv(csv,encoding="latin-1",delimiter=";")

y = bdd['Sexe']
X = bdd.drop(bdd.columns[0],axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8,stratify=y)
chemin = r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\models'

# load modele SVC
clf_svc = load(chemin+"\\SVCClassifierFinal2.joblib")
clf_gb = load(chemin+"\\GBClassifierFinal2.joblib")
clf_xgb = load(chemin+"\\XGBClassifierFinal2.joblib")

print(clf_svc.score(X_test,y_test))
print(clf_gb.score(X_test,y_test))
print(clf_xgb.score(X_test,y_test))


def oneConsensusModel(y_pred):
    y_consensus = []
    for i in range(len(y_pred)):
        y_consensus.append(y_pred[i])

    return y_consensus

def twoConsensusModel(y_pred,y_pred1):
    y_consensus = []
    for i in range(len(y_pred)):
        if (y_pred[i]==y_pred1[i]):
            y_consensus.append(y_pred[i])
        else:
            y_consensus.append(0.5)
    return y_consensus

def consensusModel(y_pred,y_pred1,y_pred2):
    y_consensus = []
    for i in range(len(y_pred)):
        if (y_pred[i]==y_pred1[i]==y_pred2[i]):
            y_consensus.append(y_pred[i])
        else:
            y_consensus.append(0.5)
    return y_consensus

def consensusModel2_1(y_pred,y_pred1,y_pred2):
    y_consensus = []
    for i in range(len(y_pred)):
        consensus3 = [y_pred[i],y_pred1[i],y_pred2[i]]
        checksum = np.sum(consensus3)
        if ((checksum == 2) or (checksum == 3)):
            y_consensus.append(1)

        else:
            if ((checksum==0) or (checksum == 1)):
                y_consensus.append(0)
            else:
                print(consensus3)
                y_consensus.append(0.5)

    return y_consensus

def consensusModel2_1_pondere(y_pred,y_pred1,y_pred2,y_predProba,y_pred1Proba,y_pred2Proba):
    y_consensus = []
    for i in range(len(y_pred)):
        consensus3 = [y_pred[i],y_pred1[i],y_pred2[i]]
        checksum = np.sum(consensus3)
        sumProba1 = np.sum([y_predProba[i][1],y_pred1Proba[i][1],y_pred2Proba[i][1]])
        sumProba0 = np.sum([y_predProba[i][0],y_pred1Proba[i][0],y_pred2Proba[i][0]])
        if ((checksum == 2) or (checksum == 3)):
            if sumProba1>1.7*sumProba0:
                y_consensus.append(1)
            else:
                y_consensus.append(0.5)

        else:
            if ((checksum==0) or (checksum == 1)):
                if sumProba0>1.7*sumProba1:
                    y_consensus.append(0)
                else:
                    y_consensus.append(0.5)
            else:
                print(consensus3)
                y_consensus.append(0.5)

    return y_consensus

def consensusModelPondere(y_pred,y_pred1,y_pred2,y_predProba,y_pred1Proba,y_pred2Proba):
    y_consensus = []
    for i in range(len(y_pred)):
        if (y_pred[i]==y_pred1[i]==y_pred2[i]):
            if (y_predProba[i][y_pred[i]]>0.9 and y_pred1Proba[i][y_pred[i]]>0.9 and y_pred2Proba[i][y_pred[i]]>0.9):
                y_consensus.append(y_pred[i])
            else:
                y_consensus.append(0.5)
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
for i in range(2000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,stratify=y)
    y_pred = clf_gb.predict(X_test)
    y_predProba = clf_gb.predict_proba(X_test)
    y_pred1 = clf_svc.predict(X_test)
    y_pred1Proba = clf_gb.predict_proba(X_test)
    y_pred2 = clf_xgb.predict(X_test)
    y_pred2Proba = clf_gb.predict_proba(X_test)

    # y_consensus = oneConsensusModel(y_pred)
    # y_consensus = twoConsensusModel(y_pred,y_pred1)
    # y_consensus = consensusModel(y_pred,y_pred1,y_pred2)
    # y_consensus = consensusModelPondere(y_pred,y_pred1,y_pred2,y_predProba,y_pred1Proba,y_pred2Proba)
    # y_consensus = consensusModel2_1(y_pred,y_pred1,y_pred2)
    y_consensus = consensusModel2_1_pondere(y_pred,y_pred1,y_pred2,y_predProba,y_pred1Proba,y_pred2Proba)

    # if ((100-print_misclassified(y_consensus,y_test))>0):
        # print(clf_gb.predict_proba(X_test),clf_svc.predict_proba(X_test),clf_xgb.predict_proba(X_test))
    missed.append(100-print_misclassified(y_consensus,y_test))
    undetermined.append(print_undetermined(y_consensus))



df = pd.DataFrame({'% of correctly classified individuals':missed})
df['% of undetermined individuals']=undetermined
import matplotlib.pyplot as plt
import seaborn as sns
sns.boxplot(data=df)
plt.title("Results of 2:1 pondéré")
plt.ylim([0,102])
plt.show()


