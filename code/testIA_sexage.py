import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold,learning_curve,ShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,LabelBinarizer
from sklearn.svm import SVC
from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, recall_score, accuracy_score, precision_score, confusion_matrix
from sklearn.feature_selection import SelectFromModel,RFE,SelectKBest, chi2
import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix

from sklearn.ensemble import GradientBoostingClassifier

lb = LabelBinarizer()



#### Plot learning curve

class Model():

    def plot_learning_curve(estimator, title, X, y, axes=None, ylim=None, cv=None,
                            n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):


        if axes is None:
            _, axes = plt.subplots(1, 3, figsize=(20, 5))

        axes[0].set_title(title)
        if ylim is not None:
            axes[0].set_ylim(*ylim)
        axes[0].set_xlabel("Training examples")
        axes[0].set_ylabel("Score")

        train_sizes, train_scores, test_scores, fit_times, _ = \
            learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs,
                        train_sizes=train_sizes,
                        return_times=True,verbose=2)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        fit_times_mean = np.mean(fit_times, axis=1)
        fit_times_std = np.std(fit_times, axis=1)

        # Plot learning curve
        axes[0].grid()
        axes[0].fill_between(train_sizes, train_scores_mean - train_scores_std,
                            train_scores_mean + train_scores_std, alpha=0.1,
                            color="r")
        axes[0].fill_between(train_sizes, test_scores_mean - test_scores_std,
                            test_scores_mean + test_scores_std, alpha=0.1,
                            color="g")
        axes[0].plot(train_sizes, train_scores_mean, 'o-', color="r",
                    label="Training score")
        axes[0].plot(train_sizes, test_scores_mean, 'o-', color="g",
                    label="Cross-validation score")
        axes[0].legend(loc="best")

        # Plot n_samples vs fit_times
        axes[1].grid()
        axes[1].plot(train_sizes, fit_times_mean, 'o-')
        axes[1].fill_between(train_sizes, fit_times_mean - fit_times_std,
                            fit_times_mean + fit_times_std, alpha=0.1)
        axes[1].set_xlabel("Training examples")
        axes[1].set_ylabel("fit_times")
        axes[1].set_title("Scalability of the model")

        # Plot fit_time vs score
        axes[2].grid()
        axes[2].plot(fit_times_mean, test_scores_mean, 'o-')
        axes[2].fill_between(fit_times_mean, test_scores_mean - test_scores_std,
                            test_scores_mean + test_scores_std, alpha=0.1)
        axes[2].set_xlabel("fit_times")
        axes[2].set_ylabel("Score")
        axes[2].set_title("Performance of the model")

        return plt

    def grid_search_wrapper(X_train,y_train,clf,param_grid,refit_score='precision_score'):
        """
        fits a GridSearchCV classifier using refit_score for optimization
        prints classifier performance metrics
        """
        skf = StratifiedKFold(n_splits=10)
        scorers = {
            'precision_score': make_scorer(precision_score),
            'recall_score': make_scorer(recall_score),
            'accuracy_score': make_scorer(accuracy_score)
        }
        grid_search = GridSearchCV(clf, param_grid, scoring=scorers, refit=refit_score,
                            cv=skf, return_train_score=True, n_jobs=-1,verbose=2)
        grid_search.fit(X_train.values, y_train.values)

        # make the predictions
        y_pred = grid_search.predict(X_test.values)

        print('Best params for {}'.format(refit_score))
        print(grid_search.best_params_)

        # confusion matrix on the test data.
        print('\nConfusion matrix of Random Forest optimized for {} on the test data:'.format(refit_score))
        print(pd.DataFrame(confusion_matrix(y_test, y_pred),
                    columns=['pred_femelle', 'pred_male'], index=['femelle', 'male']))
        return grid_search

    def adjusted_classes(y_scores, t):
        """
        This function adjusts class predictions based on the prediction threshold (t).
        Will only work for binary classification problems.
        """
        return [1 if y >= t else 0 for y in y_scores]

    def precision_recall_threshold(t=0.5):
        """
        plots the precision recall curve and shows the current value for each
        by identifying the classifier's threshold (t).
        """

        # generate new class predictions based on the adjusted_classes
        # function above and view the resulting confusion matrix.
        y_pred_adj = adjusted_classes(y_scores, t)
        print(pd.DataFrame(confusion_matrix(y_test, y_pred_adj),
                        columns=['pred_femelle', 'pred_male'],
                        index=['femelle', 'male']))

        # plot the curve
        plt.figure(figsize=(8,8))
        plt.title("Precision and Recall curve ^ = current threshold")
        plt.step(r, p, color='b', alpha=0.2,
                where='post')
        plt.fill_between(r, p, step='post', alpha=0.2,
                        color='b')
        plt.ylim([0.5, 1.01]);
        plt.xlim([0.5, 1.01]);
        plt.xlabel('Recall');
        plt.ylabel('Precision');

        # plot the current threshold on the line
        close_default_clf = np.argmin(np.abs(thresholds - t))
        plt.plot(r[close_default_clf], p[close_default_clf], '^', c='k',
                markersize=15)
        plt.show()


    def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
        """
        Modified from:
        Hands-On Machine learning with Scikit-Learn
        and TensorFlow; p.89
        """
        plt.figure(figsize=(8, 8))
        plt.title("Precision and Recall Scores as a function of the decision threshold")
        plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
        plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
        plt.ylabel("Score")
        plt.xlabel("Decision Threshold")
        plt.legend(loc='best')
        plt.show()

    def plot_roc_curve(fpr, tpr, label=None):
        """
        The ROC curve, modified from
        Hands-On Machine learning with Scikit-Learn and TensorFlow; p.91
        """
        plt.figure(figsize=(8,8))
        plt.title('ROC Curve')
        plt.plot(fpr, tpr, linewidth=2, label=label)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([-0.005, 1, 0, 1.005])
        plt.xticks(np.arange(0,1, 0.05), rotation=90)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate (Recall)")
        plt.legend(loc='best')
        plt.show()

