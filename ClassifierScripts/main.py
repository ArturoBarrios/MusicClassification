#!/usr/bin/python

# Library imports
import numpy as np

# Local imports
import loader
from classifiers import KNN, Perceptron


def main():
    """
    Perform n-fold cross-validation to evaluate knn and perceptron algorithms
    for classification of a dataset of Iris species.
    """

    # Load the data

    x_labels = []
    f = open("./data/music_IrisNCAmbroseClassical.txt","r")
    line = f.read()
    #put labels in x_labels

    for label in line.split(","):
        x_labels.append(label)

    #x_labels=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
    x, y, type2id = loader.load_data('./data/music_IrisNCAmbroseClassical.csv', y_label="Grade", x_labels=x_labels)

    # summation_X = []
    # summation_Y = []
    # for vector in x:
    #     index = 1
    #     result = 0
    #     for v in vector:
    #         if(v>0):
    #             result+=(index*v)
    #
    #     index+=1
    #     temp = []
    #     temp.append(result)
    #     summation_X.append(temp)
    #     summation_Y.append(1)
    #
    # x = np.array([np.array(xi)for xi in summation_X])

    # Split into 75% train & 25% test
    train_x, train_y, test_x, test_y = loader.split_data(x, y, ratio=.2)

    # print("RUNNING Perceptron: ")
    # run_classifier(train_x, train_y, test_x, test_y, Classifier=Perceptron, Param='N')
    print("RUNNING KNN: ")
    run_classifier(train_x, train_y, test_x, test_y, Classifier=KNN, Param='K')


def run_classifier(train_x,train_y,test_x,test_y, Classifier, Param):
    """
    Find the average accuracy for this classifier across all folds

    train_x: training inputs
    train_y: training labels
    test_x: testing inputs
    test_y: testing labels
    Classifier: Algorithm to use for classification
    param: The name of the parameter used in this algorithm
    """
    # Check every 10th value of Parameter P from 1 to 100
    best_acc = 0
    best_P = 0
    if Param == 'K':
        parameters = [i for i in range(1, 81, 4)]
    else:
        parameters = [i for i in range(1, 201, 10)]
    for P in parameters:
        # 4-fold cross validation
        accuracy = cross_validate(Classifier,train_x, train_y, folds=4, params=(P,))
        print("Validation Accuracy for {0} = {1}: {2:1.3f}".format(Param, P, accuracy))
        if accuracy > best_acc:
            best_acc = accuracy
            best_P = P

    # Use the best parameter
    print("Checking accuracy on the test set using {0} = {1} ...".format(Param, best_P))
    classifier = Classifier(train_x,train_y,(best_P,))
    y_hat = classifier.predict_batch(test_x)
    accuracy = find_accuracy(test_y, y_hat)
    print("TEST SET ACCURACY: {0:1.3f}\n".format(accuracy))


def cross_validate(Classifier, train_x, train_y, folds=4, params=(1,)):
    """
    Find the average accuracy for this classifier across all folds.

    Classifier: The classifier we're testing now
    train_x: training set inputs
    train_y: training set labels
    folds: the number of folds to use for cross-validation
    params: parameters to the classifier algorithm
    """
    accuracies = []
    for fold in range(folds):
        subset_x, subset_y, val_x, val_y = loader.split_data(train_x, train_y, ratio=1./folds, fold=fold)
        classifier=Classifier(subset_x, subset_y, params)
        y_hat=classifier.predict_batch(val_x)
        accuracies.append(find_accuracy(val_y, y_hat))
    return np.mean(accuracies)

def find_accuracy(y, y_hat):
    """
    Compute the accuracy of the predictions made based on the labels.

    y: the labels
    y_hat: the predictions
    """
    return np.sum(np.equal(y, y_hat), dtype=float) / len(y)

if __name__ == '__main__':
    main()
