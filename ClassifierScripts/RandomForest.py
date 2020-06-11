import loader
from sklearn import preprocessing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpl_toolkits
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
import math
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import r2_score

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

#get first column of every row X[0:,1]
#get first column of first row X[0,0]
####################################################################Examining Data
#read in data
#musicIrisLowLevelFeaturesAll(best result so far)
#music_IrisAmbroseCustom(second set of best results)
#read in data
#musicIrisLowLevelFeaturesAll(best result so far)
#music_IrisAmbroseCustom(second set of best results)
data = pd.read_csv("data/abrsm_all_1.csv")#
# data = data[data.Grade < 10]
# data2 = data[data.Grade == 8]
# frames = [data1,data2]
# data = pd.concat(frames)

N = 500
data = data.sample(frac=1).reset_index(drop=True)
data = data.groupby('Grade')\
    .apply(lambda x: x[:N])

dict = {}
for elem in data.Grade:
    if elem not in dict:
        dict[elem] = 0
    dict[elem] = dict[elem] + 1

print(dict)
###################################################Linear Regression

#linear regression
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
labels = data['Grade']
train1 = data.drop(['Grade'],axis = 1)


#.2 and random_state = 0 best result,test_size.1
#best result = .1, 2
random_state = 0
highest_accuracy = 0
highest_accuracy_state = 0
#while(random_state<1):
#print("random state: ",random_state)
x_train,x_test,y_train,y_test = train_test_split(train1,labels,test_size=.2,random_state=0,stratify=labels)
from sklearn import ensemble

estimators = 500
current_accuracy = 0

clf = RandomForestRegressor(n_estimators=estimators,min_samples_split=2,min_samples_leaf=1,random_state=0)
clf.fit(x_train, y_train)
#currently .01 should be the threashold
sfm = SelectFromModel(clf,threshold=.3).fit(x_train,y_train)
x_important_train = sfm.transform(x_train)
x_important_test = sfm.transform(x_test)
clf_important = RandomForestRegressor(n_estimators=estimators,min_samples_split=2,min_samples_leaf=1,random_state=0, warm_start=True)
clf_important.fit(x_important_train, y_train)

#compare estimators
y_test_pred = clf.predict(x_test)
y_train_pred = clf.predict(x_train)
print("no feature selection train score: ",r2_score(y_train,y_train_pred))
print("no feature selection test score: ",r2_score(y_test,y_test_pred))


y_important_test_pred = clf_important.predict(x_important_test)
y_important_train_pred = clf_important.predict(x_important_train)
print("feature selection train score: ",r2_score(y_train, y_important_train_pred))
print("feature selection test score: ",r2_score(y_test, y_important_test_pred))


    #random_state+=1
#
filename = './ClassificationModels/PianoMarvelNoTotal1.sav'
joblib.dump(clf, filename)





#######################################################Plot multidimensional data
# from pandas.tools.plotting import parallel_coordinates
#
# # Take the iris dataset
# import seaborn as sns
# data = sns.load_dataset('iris')
#
# Make the multidimensional plot
# parallel_coordinates(data, 'Grade', colormap=plt.get_cmap("Set2"))
# plt.show()







#######################################################plot deviance of two models
# I think deviance is just how good the model is compared to the perfect model
# ie how well this model explains the data, it seems like the score is the deviance
# calculation used for deviance: (dev_max-dev_model)/dev_max

# test_score = np.zeros((estimators,), dtype=np.float64)
# for i, y_pred in enumerate(clf.staged_predict(x_test)):
#     test_score[i] = clf.loss_(y_test, y_pred)
#
#
# plt.figure(figsize=(10, 7))
# plt.subplot(1, 2, 1)
# plt.title('Deviance')
# plt.plot(np.arange(estimators) + 1, clf.train_score_, 'b-',
#          label='Training Set Deviance')
# plt.plot(np.arange(estimators) + 1, test_score, 'r-',
#          label='Test Set Deviance')
# plt.legend(loc='upper right')
# plt.xlabel('Boosting Iterations')
# plt.ylabel('Deviance')
#
# # Plot feature importance
# feature_importance = clf.feature_importances_
# # make importances relative to max importance
# feature_importance = 100.0 * (feature_importance / feature_importance.max())
# sorted_idx = np.argsort(feature_importance)
# print(sorted_idx)
#
# pos = np.arange(sorted_idx.shape[0]) + .5
# ## plt.subplot(1, 2, 2)
# ## plt.barh(pos, feature_importance[sorted_idx], align='center')
# ## plt.yticks(pos, data.columns[sorted_idx])
# ## plt.xlabel('Relative Importance')
# ## plt.title('Variable Importance')
# plt.show()


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Only use the labels that appear in the data
    # classes = classes[unique_labels(y_true, y_pred)]
    classes = unique_labels(pd.Series(y_true))

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')




    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)

    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


# np.set_printoptions(precision=2)

# y_pred_new = []
# for y in y_pred:
#     y_new = round_half_up(y,0)
#     y_pred_new.append(y_new)

# # Plot non-normalized confusion matrix
# plot_confusion_matrix(y_test, y_pred_new, classes=labels,
#                       title='Confusion matrix, without normalization')

# # Plot normalized confusion matrix
# plot_confusion_matrix(y_test, y_pred_new, classes=labels, normalize=True,
#                       title='Normalized confusion matrix')

# plt.show()

