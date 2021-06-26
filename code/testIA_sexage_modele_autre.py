



##### Random Forest Classifier

# # # # # print("\nRF Classifier")
# # # # # clf = RandomForestClassifier(n_estimators=200,max_depth=6,max_features="auto")
# # # # # clf.fit(X_train,y_train)
# # # # # print(clf.score(X_train,y_train))
# # # # # print(clf.score(X_test,y_test))


# # # # # #
# # # # # #
# # # # # # clf.get_support()
# # # # # # selected_feat= X_train.columns[(clf.get_support())]
# # # # # # print(len(selected_feat))
# # # # # # print(X_train.shape[1])
# # # # # # print(selected_feat)
# # # # # # importances = clf.estimator_.feature_importances_
# # # # # # indices = np.argsort(importances)[::-1]
# # # # # # # X is the train data used to fit the model
# # # # # # plt.figure()
# # # # # # plt.title("Feature importances")
# # # # # # plt.bar(range(X.shape[1]), importances[indices],
# # # # # #        color="r", align="center")
# # # # # # plt.xticks(range(X.shape[1]), indices)
# # # # # # plt.xlim([-1, X.shape[1]])
# # # # # # plt.show()



# print("Random Forest")
# clf=RandomForestClassifier()
# param_grid = {
#     'n_estimators': [200,250,300],
#     'max_features': ['auto','sqrt'],
#     'max_depth' : [7,8,9]
# }
#
# scorers = {
#     'precision_score': make_scorer(precision_score),
#     'recall_score': make_scorer(recall_score),
#     'accuracy_score': make_scorer(accuracy_score)
# }
#
#
#
#

#
# grid_search_clf = grid_search_wrapper(refit_score='precision_score')
#
#
# results = pd.DataFrame(grid_search_clf.cv_results_)
# results = results.sort_values(by='mean_test_precision_score', ascending=False)
# results[['mean_test_precision_score', 'mean_test_recall_score', 'mean_test_accuracy_score',
#          'param_max_depth', 'param_max_features',
#          'param_n_estimators']].head()
#
#
# # this gives the probability [0,1] that each sample belongs to class 1
# y_scores = grid_search_clf.predict_proba(X_test)[:, 1]
#
#
#
#
# p, r, thresholds = precision_recall_curve(y_test, y_scores)
#
# import matplotlib.pyplot as plt
#
#
#
#
# precision_recall_threshold(0.48)
#
#
#
#
# plot_precision_recall_vs_threshold(p, r, thresholds)
#
#

#
#
# fpr, tpr, auc_thresholds = roc_curve(y_test, y_scores)
# print(auc(fpr, tpr)) # AUC of ROC
# plot_roc_curve(fpr, tpr, 'recall_optimized')





#
# CV_clf = GridSearchCV(estimator=clf, param_grid=param_grid, cv= 5,verbose=2)
#
# CV_clf.fit(X_train,y_train)
# print("\tTraining score : "+str(CV_clf.score(X_train,y_train)))
# print("\tTesting score : "+str(CV_clf.score(X_test,y_test)))
# print("\n")
#
#
# for x in CV_clf.cv_results_['mean_test_score']:
#     print(x)
#
# for x in CV_clf.cv_results_['params']:
#     print(x)





#
###### SVM
# # # #
# # # #
# # # # print("SVM")
# # # # clf1 = make_pipeline(StandardScaler(), SVC(C=100,gamma=0.01,kernel='poly'))
# # # # clf1.fit(X_train,y_train)
# # # # print("\tTraining score : "+str(clf1.score(X_train,y_train)))
# # # # print("\tTesting score : "+str(clf1.score(X_test,y_test)))
# # # #
# # clf = SVC(C=100,gamma=0.01,kernel="poly")
# # # # fig, axes = plt.subplots(3, 1, figsize=(10, 15))
# # # # cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
# # # # plot_learning_curve(clf, "Learning curves", X, y, axes=axes[:], ylim=(0.7, 1.01),cv=cv, n_jobs=4)
# # # # plt.show()

clf = SVC(C=100,gamma=0.01,kernel="poly")
clf.fit(X_train,y_train)

titles_options = [("Normalized confusion matrix", 'true')]
for title, normalize in titles_options:
    disp = plot_confusion_matrix(clf, X_test, y_test,
                                 display_labels=[0,1],
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
    disp.ax_.set_title(title)
plt.show()




##### xgb

import xgboost as xgb

xgb_model = xgb.XGBClassifier(objective="binary:logistic", random_state=42, eval_metric="auc",nthread=4)
xgb_model.fit(X_train, y_train, early_stopping_rounds=5, eval_set=[(X_test, y_test)])
# # print(xgb_model.score(X_train,y_train))
# # print(xgb_model.score(X_test,y_test))
# # print("best score: {0}, best iteration: {1}, best ntree limit {2}".format(xgb_model.best_score, xgb_model.best_iteration, xgb_model.best_ntree_limit))


parameters = {
    'max_depth': range (2, 10, 1),
    'n_estimators': range(60, 220, 40),
    'learning_rate': [0.1, 0.01, 0.05]
}


grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=parameters,
    scoring = 'roc_auc',
    n_jobs = 10,
    cv = 10,
    verbose=True
)
grid_search.fit(X2, y)


clf2 = xgb.XGBClassifier(objective="binary:logistic", random_state=42, eval_metric="auc",nthread=4,max_depth=3,n_estimators=180,learning_rate=0.05)

clf2 = xgb.XGBClassifier(objective="binary:logistic", random_state=42, eval_metric="auc",nthread=4,max_depth=2,n_estimators=60,learning_rate=0.1)


clf2.fit(X_train2,y_train2)
print(clf2.score(X_train2,y_train2))
print(clf2.score(X_test2,y_test2))

xgb.plot_importance(clf2)
plt.show()

fig, axes = plt.subplots(3, 1, figsize=(10, 15))
cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
plot_learning_curve(clf2, "Learning curves", X, y, axes=axes[:], ylim=(0.7, 1.01),cv=cv, n_jobs=4)
plt.show()


from sklearn.metrics import classification_report

y_pred = clf2.predict(X_test2)

print(classification_report(y_test2 , y_pred, target_names=["femelle","male"]))