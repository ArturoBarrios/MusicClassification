from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import datasets, cluster
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
import math
 
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier + 0.5) / multiplier


def showFeatureImportance(clf, X): 
    importances = clf.feature_importances_
    std = np.std([clf.feature_importances_ for tree in clf.estimators_],
                axis=0)
    indices = np.argsort(importances)[::-1]
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
    # Plot the impurity-based feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.show()
    
def TrainPredictRandomForestRegressor(X, labels, estimators ):
    x_train,x_test,y_train,y_test = train_test_split(X,labels,test_size=.25,random_state=2,stratify=labels)
    clf = RandomForestRegressor(n_estimators=estimators,min_samples_split=2,min_samples_leaf=1,random_state=0)
    clf.fit(x_train,y_train)
    y_test_pred = clf.predict(x_test)
    y_train_pred = clf.predict(x_train)
    print("no feature selection train score: ",r2_score(y_train,y_train_pred))
    print("no feature selection test score: ",r2_score(y_test,y_test_pred))
    return (clf,x_train,y_test_pred,y_test)

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=True,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    y_pred_new = []
    for y in y_pred:
        y_new = round_half_up(y,0)
        y_pred_new.append(y_new)
    y_pred = y_pred_new

    y_true_new = []
    for y in y_true:
        y_new = round_half_up(y,0)
        y_true_new.append(y_new)
    y_true = y_true_new

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
    print("classess: ", classes)

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
    plt.show()
  






N = 500
data = pd.read_csv("IrisTextFiles/music_marvel_GE_80.csv")
data = data.sample(frac=1).reset_index(drop=True)
data = data[data.Grade<10]
data = data.groupby('Grade')\
    .apply(lambda x: x[:N])
labels = data['Grade']
X = data.drop(['Grade'],axis = 1)
print(labels)

scaler = StandardScaler()
scaler.fit(X)
scaledX = scaler.transform(X)

#FeatureAgglomeration reduction
agglo = cluster.FeatureAgglomeration(n_clusters=128)
agglo.fit(scaledX)
X_reduced = agglo.transform(scaledX)
#Principal component analysis
pca = PCA(n_components=2, svd_solver='full')
pca.fit(X)
X_reducedPCA = pca.transform(X)
#Kernel principal component analysis
kpca = KernelPCA(n_components=20, kernel='cosine')
kpca.fit(X)
X_reducedKPCA = kpca.transform(X)
N=500
print("no feature reduction: ")
res = TrainPredictRandomForestRegressor(scaledX,labels, N)
print("Agglomerative Feature Reduction: ")
res2 = TrainPredictRandomForestRegressor(X_reduced,labels, N)
# print("Principal Component Analysis Feature Reduction ")
# res3 = TrainPredictRandomForestRegressor(X_reducedPCA,labels, N)
# print("Kernel Principal Component Analysis Feature Reduction ")
# res4 = TrainPredictRandomForestRegressor(X_reducedKPCA,labels, N)



plot_confusion_matrix(res[2], res[3], classes=labels, normalize=True,
                      title='Normalized confusion matrix')
plot_confusion_matrix(res2[2], res2[3], classes=labels, normalize=True,
                        title='Normalized confusion matrix')


# showFeatureImportance(res[0],res[1])
# showFeatureImportance(res2[0],res2[1])


