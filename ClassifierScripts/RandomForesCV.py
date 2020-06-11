import loader
from sklearn import preprocessing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpl_toolkits
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn.preprocessing import MinMaxScaler
import math

def transform_values(csv_data):
    max_dict = dict()
    min_dict = dict()
    columns = csv_data.columns
    csv_data = csv_data.values
    i = 0
    for row in csv_data:
        for col in row:
            if columns[i] not in max_dict:
                max_dict[columns[i]] = col
            else:
                if col>max_dict[columns[i]]:
                    max_dict[columns[i]] = col
            if columns[i] not in min_dict:
                min_dict[columns[i]] = col
            else:
                if col<min_dict[columns[i]]:
                    min_dict[columns[i]] = col
            i+=1
        i = 0
    return max_dict,min_dict,columns

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

#get first column of every row X[0:,1]
#get first column of first row X[0,0]
####################################################################Examining Data
#read in data
#musicIrisLowLevelFeaturesAll(best result so far)
#music_IrisAmbroseCustom(second set of best results)
data = pd.read_csv("data/abrsm_all_1.csv")
N = 500
data = data.sample(frac=1).reset_index(drop=True)
data = data.groupby('Grade')\
    .apply(lambda x: x[:N])
# data = data[data.Grade <10 ]
#describe data(mean,avg,std,etc)
print(data.describe())
dict = {}
for elem in data.Grade:
    if elem not in dict:
        dict[elem] = 0
    print("el: ", elem)
    dict[elem] = dict[elem] + 1

print(dict)


###################################################Linear Regression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn import ensemble
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression

estimators = 1000

labels = data['Grade']
train1 = data.drop(['Grade'],axis = 1)
# transform_values(train1)
train1 = train1.to_numpy()
labels = labels.to_numpy()

#scale data
# scaler = MinMaxScaler()
# minMaxScale = scaler.fit(train1)
# train1 = minMaxScale.transform(train1)
#feature selection
# sel = VarianceThreshold(threshold=(.02*(1-.02)))
# train1 = sel.fit_transform(train1)
#train1 = SelectKBest(chi2, k=100).fit_transform(train1,labels)
print(train1.shape)

#clf = ensemble.GradientBoostingRegressor(n_estimators=estimators,learning_rate=.01)
clf = RandomForestRegressor(n_estimators=estimators,min_samples_split=2,min_samples_leaf=1,bootstrap=False)
clf.fit(train1,labels)
scores = cross_val_score(clf,train1,labels,cv=2)
print("scores: ",scores,"\n\n")
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))






#####################################################Graph data points and draw line between datapoints
# clf.fit(train1,labels)
# y_pred = cross_val_predict(clf,train1,labels,cv=6)
# print(y_pred)
# fig, ax = plt.subplots()
# ax.scatter(labels, y_pred, edgecolors=(0, 0, 0))
# ax.plot([labels.min(), labels.max()], [labels.min(), labels.max()], 'k--', lw=4)
# ax.set_xlabel('Measured')
# ax.set_ylabel('Predicted')
# plt.show()
#################################################

# #.2 and random_state = 0 best result,test_size.1
# #best result = .1, 2
# random_state = 0
# highest_accuracy = 0
# highest_accuracy_state = 0
# #while(random_state<1):
# #print("random state: ",random_state)
# x_train,x_test,y_train,y_test = train_test_split(train1,labels,test_size=.2,random_state=4)
# reg.fit(x_train,y_train)
# print(reg.score(x_test,y_test))
#
# ###################################################Gradient Boosting Regression
# from sklearn import ensemble
# #n_estimators=420,max_depth=5,min_samples_split=2,learning_rate=.1(best result so far)
# #best result: n_estimators=500,max_depth=5,min_samples_split=2,learning_rate=.1: accuracy .74 music_IriseAmbroseCustom
# #best result: n_estimators=1000,max_depth=5,min_samples_split=2,learning_rate=.1: accuracy .80 music_IrisCustomFeatures15LL(didn't have classical music)
# #best result: n_estimators=1000,max_depth=5,min_samples_split=2,learning_rate=.05: accuracy .86 music_IrisCustomFeatures15LL
# learning_rates = [.01,0.05, 0.1, 0.25, 0.5, 0.75, 1]
# estimators = 1000
# # for learning_rate in learning_rates:
# current_accuracy = 0
# clf = ensemble.GradientBoostingRegressor(n_estimators=estimators,max_depth=5,min_samples_split=4,learning_rate=.01)
# clf.fit(x_train,y_train)
# y_pred = clf.predict(x_test)
# current_accuracy = clf.score(x_test,y_test)
# # if current_accuracy>=highest_accuracy:
# #     highest_accuracy = current_accuracy
# #     highest_accuracy_state = random_state
# print("training score: ",clf.score(x_train,y_train),end=" ")
# print(current_accuracy)
#
# mse = mean_squared_error(y_test, clf.predict(x_test))
# print("MSE: %.4f" % mse)
#











    #random_state+=1

filename = './ClassificationModels/NoTotal2SomeLLFeaturesModel.sav'
joblib.dump(clf, filename)


# plt.figure(figsize=(10, 5))
# plt.title('Gradient Boosting model (1 estimators, Single tree split)')
# print(x_train)
# print("\n\n\n\n")
# print(y_train)
# plt.scatter(x_test, y_test)
# plt.plot(x_test, gradient_boosting_regressor.predict(x_test), color='r')
# plt.show()


# from pandas.tools.plotting import parallel_coordinates

# Take the iris dataset
import seaborn as sns
#data = sns.load_dataset('iris')
