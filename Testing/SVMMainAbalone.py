#!/usr/bin/python

# Library imports
import numpy as np

# Local imports
import loader

# importing necessary libraries
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
# # loading the iris dataset
# iris = datasets.load_iris()
#
# # X -> features, y -> label
# X = iris.data
# y = iris.target
x_labels = []
f = open("Testing/abalone.txt","r")
line = f.read()
#put labels in x_labels

for label in line.split(","):
    x_labels.append(label)

#x_labels=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
X, y, type2id = loader.load_data('Testing/abalone.csv', y_label="Rings", x_labels=x_labels)
print("yyyyyy: ",y)
i = 0

# dividing X, y into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state = 2)
# training a linear SVM classifier
from sklearn.svm import SVC
svm_model_linear = SVC(kernel = 'poly',degree= 5).fit(X_train, y_train)
svm_predictions = svm_model_linear.predict(X_test)
print("type2id: ",type2id)

# model accuracy for X_test
accuracy = svm_model_linear.score(X_test, y_test)

# creating a confusion matrix
cm = confusion_matrix(y_test, svm_predictions)
# print("Accuracy: ",accuracy)


# new prediction calculation
key_list = list(type2id.keys())
i = 0
correctPredictions = 0
for prediction in svm_predictions:
    val = int(key_list[prediction])

    if val<=8 and int(y_test[i]) <= 8 :
        correctPredictions+=1
    elif val <= 10 and int(y_test[i]) <= 10:
        correctPredictions+=1
    elif val>=11 and int(y_test[i])>=11:
        correctPredictions+=1

    # if abs(val-int(y_test[i])<2):
    #     correctPredictions += 1
    i+=1
print("Alternative Accuracy: ",correctPredictions/len(svm_predictions))
# save the model to disk
# filename = 'finalized_music_model.sav'
# joblib.dump(svm_model_linear, filename)
