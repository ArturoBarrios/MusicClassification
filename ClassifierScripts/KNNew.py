#!/usr/bin/python

# Library imports
import numpy as np

# Local imports
import loader
from classifiers import KNN, Perceptron
# importing necessary libraries
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score


# # loading the iris dataset
# iris = datasets.load_iris()
#
# # X -> features, y -> label
# X = iris.data
# y = iris.target

x_labels = []
f = open("./data/music_IrisNCAmbroseClassical.txt","r")
line = f.read()
#put labels in x_labels

for label in line.split(","):
    x_labels.append(label)

#x_labels=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
X, y, type2id = loader.load_data('./data/music_IrisNCAmbroseClassical.csv', y_label="Grade", x_labels=x_labels)

#feature selection(L1 based feature selection)
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
# print(X.shape)
# lsvc = LinearSVC(C=0.001, penalty="l1", dual=False).fit(X, y)
# model = SelectFromModel(lsvc, prefit=True)
# X = model.transform(X)
# print(X.shape)
#feature selection(univariate feature selection(selectKBest))
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import VarianceThreshold
print(X.shape)
# sel = VarianceThreshold(threshold=(.9* (1 - .9)))
# X = sel.fit_transform(X)
# X = SelectKBest(chi2, k=5).fit_transform(X, y)
# print(X.shape)


# training a K-nearest neighbors classifier
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 10)

cv = 10
cross_val_scores = cross_val_score(knn,X,y,cv=cv)
cross_val_predictions = cross_val_predict(knn,X,y,cv=cv)
print(cross_val_scores)
#calculate average score
total_score = 0
average_score = 0
for score in cross_val_scores:
    total_score+=score
average_score = total_score/len(cross_val_scores)
print("average scores: ",average_score)
# creating a confusion matrix


#new prediction calculation
key_list = list(type2id.keys())
i = 0
range_values = {0:0,1:1,2:1,3:1,4:1,5:2,6:2,7:2,8:3}
actualCorrectPredictions = 0
altCorrectPredictions = 0
for prediction in cross_val_predictions:
    val = int(y[i])
    prediction = int(prediction)
    if range_values[val]==range_values[prediction]:
        altCorrectPredictions+=1

    # if abs(val-prediction)<2:
    #     altCorrectPredictions += 1
    if(val==prediction):
        actualCorrectPredictions +=1
    i+=1
print("accuracy: ",actualCorrectPredictions/len(cross_val_predictions))
print("Alternative Accuracy: ",altCorrectPredictions/len(cross_val_predictions))
