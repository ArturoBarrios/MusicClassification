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

# training a DescisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
dtree_model = DecisionTreeClassifier(max_depth = 1)

# dividing X, y into train and test data
cross_val_predictions = cross_val_predict(dtree_model,X,y,cv=10)


# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)
#
#
#
# # creating a confusion matrix
# cm = confusion_matrix(y_test, dtree_predictions)
# print(dtree_predictions)
# print(y_test)
#
# #new prediction calculation
key_list = list(type2id.keys())
i = 0
range_values = {0:0,1:0,2:1,3:1,4:1,5:2,5:2,6:3,7:3,8:3}
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
