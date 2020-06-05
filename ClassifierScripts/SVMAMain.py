import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv("IrisTextFiles/PianoMarvelNoTotal.csv")
data = data[data.Grade <11]
dict = {}
for elem in data.Grade:
    if elem not in dict:
        dict[elem] = 0
    dict[elem] = dict[elem] + 1

print(dict)
N = 500
data = data.sample(frac=1).reset_index(drop=True)
data = data.groupby('Grade')\
    .apply(lambda x: x[:N])

print("data: ",data)

dict = {}
for elem in data.Grade:
    if elem not in dict:
        dict[elem] = 0
    dict[elem] = dict[elem] + 1

print(dict)

labels = data.Grade
train1 = data.drop(['Grade'],axis = 1)

#scale dataset
# scaler = StandardScaler()
# std_scale = scaler.fit(train1)
# train1 = std_scale.transform(train1)
scaler = MinMaxScaler()
minMaxScale = scaler.fit(train1)
train1 = minMaxScale.transform(train1)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train1, labels, test_size = 0.20)

from sklearn.svm import SVC
svclassifier = SVC(kernel='sigmoid', degree=8)
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
