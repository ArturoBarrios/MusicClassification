import csv
import numpy as np

def load_data(filename, y_label, x_labels):
    """
    Load the data from the file into an "inputs" list and a "labels" list


    filename: the string representing the location of the datafile
    y_label: the column label representing the "label" of the data
    x_labels: the column labels representing the "inputs"
    """

    # Read data into list
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            #if(row['Grade']=='2' or row['Grade']=='3'):
                #print(row)
            data.append(row)

    # Change labels into indexes
    labels = set(d[y_label] for d in data)

    # for d in data:
    #     print(d)
    label2id = { label: i for i, label in enumerate(labels) }


    # Shuffle data (with random seed for replicability)
    np.random.seed(0)
    np.random.shuffle(data)

    # Parse x and y
    y = np.array([label2id[d[y_label]] for d in data], dtype=np.int)
    x = np.array([[d[label] for label in d if label in x_labels] for d in data], dtype=np.float)
    return x, y, label2id


def split_data(x, y, ratio, fold = 0):
    """
    Split the data into two sets, train and test

    x: inputs
    y: labels
    ratio: fraction of total to put in the test set
    fold: which part of the data to assign to test (nth fraction of the data)
    """

    # Define the boundaries of the test data
    test_start = int(len(x) * ratio * fold)
    test_stop = int(len(x) * ratio * (fold+1))

    # Split the data
    train_x = np.concatenate((x[:test_start], x[test_stop:]))
    train_y = np.concatenate((y[:test_start], y[test_stop:]))
    test_x = x[test_start:test_stop]
    test_y = y[test_start:test_stop]

    return train_x, train_y, test_x, test_y
