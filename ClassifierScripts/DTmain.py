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
f = open("./data/music_IrisNCAmbroseClassical.txt","r")
line = f.read()
#put labels in x_labels

for label in line.split(","):
    x_labels.append(label)

#x_labels=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
X, y, type2id = loader.load_data('./data/music_IrisNCAmbroseClassical.csv', y_label="Grade", x_labels=x_labels)

# dividing X, y into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)

# training a DescisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
dtree_model = DecisionTreeClassifier(max_depth = 100).fit(X_train, y_train)
dtree_predictions = dtree_model.predict(X_test)

# creating a confusion matrix
cm = confusion_matrix(y_test, dtree_predictions)
print(dtree_predictions)
print(y_test)

#new prediction calculation
key_list = list(type2id.keys())
i = 0
correctPredictions = 0
for prediction in dtree_predictions:
    val = int(key_list[prediction])
    if abs(val-int(y_test[i]))<2:
        correctPredictions += 1
    i+=1
print("Alternative Accuracy: ",correctPredictions/len(dtree_predictions))
