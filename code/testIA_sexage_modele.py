
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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,stratify=y)
X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y, test_size=0.3,stratify=y)


###### Gradient Boosting Classifier
            ## GridSearch ##
""" Best params for Gradient Boosting
    Training Score : 1.0
    Testing Score : 0.92
{'criterion': 'friedman_mse', 'learning_rate': 0.075, 'loss': 'deviance', 'max_depth': 5, 'max_features': 'sqrt', 'n_estimators': 1000, 'subsample': 0.618}
"""

# # # print("Gradient Boosting Classifier")
# # # parameters = {
# # #     "loss":["deviance"],
# # #     "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1],
# # #     "max_depth":[3,5,8],
# # #     "max_features":["log2","sqrt"],
# # #     "criterion": ["friedman_mse",  "mae"],
# # #     "subsample":[0.5, 0.618, 0.95, 1.0],
# # #     "n_estimators":[200,500,1000]
# # #     }
# # #
# # # clf0 = GridSearchCV(GradientBoostingClassifier(), parameters, cv=10, n_jobs=-1,verbose=2).fit(X_train,y_train)
# # # print(clf0.score(X_train,y_train))
# # # print(clf0.score(X_test,y_test))



# listeGradientBoosting = []

# # for i in range(100):
# #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,stratify=y)
# #     clf = GradientBoostingClassifier(criterion = "friedman_mse",learning_rate = 0.075,n_estimators=1000,max_depth=5,max_features="sqrt",subsample=0.618,loss="deviance")
# #     clf.fit(X_train,y_train)
# #     # print(clf.score(X_test,y_test))
# #     listeGradientBoosting.append(clf.score(X_test,y_test))
# #
# # plt.figure()
# # plt.boxplot(listeGradientBoosting)
# # plt.title("Moyenne du testing score pour le Gradient Boosting")
# # plt.ylim([0,1])
# # plt.show()
# #
# #
# # #plot learning curve
# clf = GradientBoostingClassifier(criterion = "friedman_mse",learning_rate = 0.075,n_estimators=1000,max_depth=5,max_features="sqrt",subsample=0.618,loss="deviance")
# # fig, axes = plt.subplots(3, 1, figsize=(10, 15))
# # cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
# # plot_learning_curve(clf, "Learning curves", X, y, axes=axes[:, 0], ylim=(0.7, 1.01),cv=cv, n_jobs=4)

#
# clf = GradientBoostingClassifier(criterion = "friedman_mse",learning_rate = 0.075,n_estimators=1000,max_depth=5,max_features="sqrt",subsample=0.618,loss="deviance")
# clf.fit(X_train,y_train)
#
from joblib import dump, load
# dump(clf, r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\GBClassifierFinal.joblib')
# #
#
#
# clf = load(r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\GBClassifierFinal.joblib')
#
# y_pred = clf.predict(X_test)
# #
# print(pd.DataFrame(classification_report(y_test , y_pred, target_names=["femelle","male"],output_dict=True)).transpose()['recall'])
# # # #
# # # # titles_options = [("Normalized confusion matrix", 'true')]
# # # # for title, normalize in titles_options:
# # # #     disp = plot_confusion_matrix(clf, X_test, y_test,
# # # #                                  display_labels=[0,1],
# # # #                                  cmap=plt.cm.Blues,
# # # #                                  normalize=normalize)
# # # #     disp.ax_.set_title(title)
# # # # plt.show()


# clf = GradientBoostingClassifier()
#
# parameters = {
#     "loss":["deviance"],
#     "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1],
#     "max_depth":[3,5,8],
#     "max_features":["log2","sqrt"],
#     "criterion": ["friedman_mse",  "mae"],
#     "subsample":[0.5, 0.618, 0.95, 1.0],
#     "n_estimators":[200,500,1000]
#     }
#
# grid_search_clf = testIA_sexage.Model.grid_search_wrapper(X_train2,y_train2,clf,parameters,refit_score='recall_score')
#
#
#
# clf_svc = SVC(C=100,gamma=0.01,kernel="poly",probability=True)
# clf_svc.fit(X_train,y_train)
#
# titles_options = [("Normalized confusion matrix", 'true')]
# for title, normalize in titles_options:
#     disp = plot_confusion_matrix(clf_svc, X_test, y_test,
#                                  display_labels=[0,1],
#                                  cmap=plt.cm.Blues,
#                                  normalize=normalize)
#     disp.ax_.set_title(title)
# plt.show()
#
# dump(clf_svc, r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\SVCClassifierFinal.joblib')
# import xgboost as xgb
#
# xgb_model = xgb.XGBClassifier(objective="binary:logistic", random_state=42, eval_metric="auc",nthread=4)
# xgb_model.fit(X_train, y_train, early_stopping_rounds=5, eval_set=[(X_test, y_test)])
# titles_options = [("Normalized confusion matrix", 'true')]
# for title, normalize in titles_options:
#     disp = plot_confusion_matrix(xgb_model, X_test, y_test,
#                                  display_labels=[0,1],
#                                  cmap=plt.cm.Blues,
#                                  normalize=normalize)
#     disp.ax_.set_title(title)
# plt.show()
#
# dump(xgb_model, r'C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\XGBClassifierFinal.joblib')
