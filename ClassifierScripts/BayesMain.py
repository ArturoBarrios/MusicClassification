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
from sklearn.naive_bayes import GaussianNB


x_labels = []
f = open("./data/music_IrisNCAmbroseClassical.txt","r")
line = f.read()
#put labels in x_labels

for label in line.split(","):
    x_labels.append(label)

#x_labels=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
X, y, type2id = loader.load_data('./data/music_IrisNCAmbroseClassical.csv', y_label="Grade", x_labels=x_labels)

# training a DescisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
gnb = GaussianNB()

# dividing X, y into train and test data
cross_val_predictions = cross_val_predict(gnb,X,y,cv=10)

key_list = list(type2id.keys())
i = 0
correctPredictions = 0
for prediction in cross_val_predictions:
    val = int(y[i])
    if abs(val-prediction)<3:
        correctPredictions += 1
    i+=1
print("Alternative Accuracy: ",correctPredictions/len(cross_val_predictions))
