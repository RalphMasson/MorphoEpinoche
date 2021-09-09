"""" Schéma pour rapport """

## Bibliothèques

from joblib import dump, load
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import *
import matplotlib.pyplot as plt


## Base de données du rapport

X = [2,0.1,3,0.4]
X= pd.DataFrame({'D1':X})
X['D2'] = [4,3,5,2]
X['D3'] = [46,42,49,40]

y = [0.5,-0.5,0.5,-0.5]
y = pd.DataFrame({'r1':y})


## Calcul des arbres de regression

from sklearn.tree import DecisionTreeRegressor
dtr = DecisionTreeRegressor()
dtr.fit(X,y)

from dtreeviz.trees import dtreeviz
viz = dtreeviz(dtr, X.values, y.values,feature_names=X.columns)
viz.view()

import sklearn
sklearn.tree.plot_tree(dtr,filled=True, fontsize=6, rounded = True,class_names = True)
plt.show()

all = X.copy()
all['r1'] = y.copy()
all['r2'] = [0.83,-0.5,0.83,-0.5]

r2 = [0.17,-0.17,0.17,-0.17]
dtr2 = DecisionTreeRegressor()
dtr2.fit(X,r2)

sklearn.tree.plot_tree(dtr2,filled=True, fontsize=6, rounded = True,class_names = True)
plt.show()

r3 = [0.08,-0.07,0.08,-0.07]
dtr3 = DecisionTreeRegressor()
dtr3.fit(X,r3)
sklearn.tree.plot_tree(dtr3,filled=True, fontsize=6, rounded = True,class_names = True)
plt.show()

