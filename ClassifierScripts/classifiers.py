#!/usr/bin/python

from maxheap import Maxheap
import numpy as np
import sys
import math
import operator

"""
Task 3: record the results of your experiments here.

Changing random seed:
    3521: --
    1: --
    1700 --
    There was no change in the test and validation accuracy of the Perceptron classification algorithm when changing the random seeds

Changing distance metric:
    L2: --
    Euclidean: -- There was no change in the test and validation accuracy of the KNN classification algorithm when
    using Euclidean distance.
    Manhattan Distance:  -- When the Manhattan distance was applied instead of L2, there was a difference for the validation
    accuracy for K = 1 and K = 5. For the Manhattan Distance the validation accuracy was lower by .12 for K = 1 and .26 lower for
    K = 5. The test set accuracy remained the same.
"""


class Perceptron:
    """ Implementation of the perceptron classification algorithm """

    def __init__(self, X, Y, params):
        np.random.seed(100)
        self.W = np.random.rand(len(X[0]))
        self.Bias = 0
        self.N = params[0] #Number of Iterations
        self.train(X,Y)


    def train(self, X, Y):
        """
        Train the Perceptron given the training data using Gradient Descent.

        Step 1: Predict Yhat for training inputs
        Step 2: Update Each Parameter (including bias) as per the Gradient:
                wi = wi + (Y - Yhat) . Xi
        Step 3: Repeat above steps N times

        Tips:
        A. It is faster to use a matrix operation to compute the gradient
        B. Inputs and Parameters are provided as 'Numpy' Arrays.
        C. Numpy provides a dot product operation, and other matrix operations.
        D. You can print the parameters to see what's going on: self.W, self.Bias, etc.
        """
        i = 0
        while i<self.N:
            j = 0
            while j<len(X):
                YH =  self.W.dot(X[j])

                self.W = self.W +(Y-YH).dot(X)

                self.W = self.W.dot(Y[j])
                j+=1

            i+=1

    def predict(self, input_x):
        """ Predict the output of a single input """
        weighted_sum = input_x.dot(self.W) + self.Bias

        return (weighted_sum > 0).astype(int)

    def predict_batch(self, X_test):
        """ Predict the outputs of a set of inputs """
        return [self.predict(point) for point in X_test]

class KNN:
    """ Implementation of the kNN classification algorithm """

    def __init__(self, X, Y, params):
        self.X=X
        self.Y=Y
        self.k=params[0]
        self.train(X,Y)

    def train(self,X,Y):
        """ No training step needed. """
        pass

    def predict(self, input_x):
        """
        Predict labels using k-nearest neigbors for a given point.
        self.X : training inputs to use for reference
        self.Y : training outputs to use for reference
        self.k : number of neighbors to use
        input_x : point to predict the label for

        Implement KNN with the below algorithm:
        Step 1: Find the nearest K neighbors to input_x
            A. Initialize a MaxHeap with any K points (and K distances)
            B. Go through all the remaining reference points
            C. If any point is a nearer neighbor than existing ones
            D. Remove the farthest neighbor from the heap (Max distance value)
            E. Add the new point in it's place

        Step 2: Find the majority class amongst the nearest neighbors in the heap
            (You may find the maxheap.counts() method helpful for this). In case
            of a tie, returning any of the tied classes is fine (this won't matter
            for the values of k that we are testing, since they are all odd).

        Step 3: Return the majority class (in the binary case, 0 or 1)

        Use self.distance to measure the distance between two points. Try:
        a=[0,1]; b=[1,1]; print(self.distance(a,b))

        You can try the below operations and print them:

        myheap=Maxheap(['e','d','f'],[5,4,6])
        myheap.peekMaxValue()
        myheap.pop()
        myheap.push('e', 0)
        myheap.counts()
        """
        heap = Maxheap([],[])
        i = 0

        while i<len(self.X):
            #find distance from input_x to point in X
            point = self.X[i]
            #print("point: ",point," Y: ",self.Y[i])
            dist = self.distance(input_x,point)
            
            #print self.k, '     ' ,point, '    ', dist, len(heap)
            #check if dis is less than max value in heap
            if(len(heap)==self.k and self.k>0):
                #check to see if dist is less than max value
                if dist<heap.peekMaxValue():
                    heap.pop()
                    heap.push(self.Y[i],dist)
            #keep pushing items with distances to heap
            else:
                heap.push(self.Y[i],dist)
            i+=1
        class_counts = heap.counts()

        class_count_dict = dict()
        for k in class_counts:
            class_count_dict[k[1]] = k[0]

        #print(min(class_count_dict.iteritems(), key=operator.itemgetter(1))[0])
        return max(class_count_dict.iteritems(), key=operator.itemgetter(1))[0]




    def predict_batch(self, X_test):
        """
        Predict labels using k-nearest neigbors for a batch.
        X_test : batch of inputs to predict
        """
        return [self.predict(point) for point in X_test]

    def distance(self,x1,x2):
        """ Calculate the distance between two points x1 and x2 """
        #return sum((x1 - x2) ** 2) # L2 distance
        #return math.sqrt(sum((x1 - x2) ** 2)) #Euclidean distance
        #cosine similarity
        return sum(abs(x1-x2)) #Manhattan distance
