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
from sklearn.neural_network import MLPClassifier


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

# training a Neural Network

#
clf = MLPClassifier(activation='relu', alpha=1e-05, batch_size='auto',
              beta_1=0.9, beta_2=0.999, early_stopping=False,
              epsilon=1e-08, hidden_layer_sizes=(5, 2),
              learning_rate='constant', learning_rate_init=0.001,
              max_iter=200, momentum=0.9, n_iter_no_change=10,
              nesterovs_momentum=True, power_t=0.5, random_state=1,
              shuffle=True, solver='lbfgs', tol=0.0001,
              validation_fraction=0.1, verbose=False, warm_start=False)

# dividing X, y into train and test data
cross_val_predictions = cross_val_predict(clf,X,y,cv=10)


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
correctPredictions = 0
for prediction in cross_val_predictions:
    val = int(y[i])
    if abs(val-prediction)<1:
        correctPredictions += 1
    i+=1
print("Alternative Accuracy: ",correctPredictions/len(cross_val_predictions))
