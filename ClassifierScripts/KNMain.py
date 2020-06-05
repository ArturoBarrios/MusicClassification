#!/usr/bin/python

# Library imports
import numpy as np

# Local imports
import loader
from classifiers import KNN, Perceptron
# importing necessary libraries
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

# # loading the iris dataset
# iris = datasets.load_iris()
#
# # X -> features, y -> label
# X = iris.data
# y = iris.target

x_labels = []
f = open("./IrisTextFiles/music_IrisNCAmbroseClassical.txt","r")
line = f.read()
#put labels in x_labels

for label in line.split(","):
    x_labels.append(label)

#x_labels=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
X, y, type2id = loader.load_data('./IrisTextFiles/music_IrisNCAmbroseClassical.csv', y_label="Grade", x_labels=x_labels)

#feature selection
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import VarianceThreshold
print(X.shape)
# sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
# X = sel.fit_transform(X)
#X = SelectKBest(mutual_info_classif, k=5).fit_transform(X, y)
print(X.shape)



# dividing X, y into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)



# training a KNN classifier
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 10).fit(X_train, y_train)

# accuracy on X_test
accuracy = knn.score(X_test, y_test)
print(accuracy)



# creating a confusion matrix
# from sklearn.metrics import classification_report
# knn_predictions = knn.predict(X_test)
# target_names = ['0','1','2','3','4','5','6','7','8']
# print(classification_report(y_test,knn_predictions,target_names=target_names))
# cm = confusion_matrix(y_test, knn_predictions).ravel()
# print(type2id)
