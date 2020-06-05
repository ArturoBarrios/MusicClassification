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
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
import math

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

#get first column of every row X[0:,1]
#get first column of first row X[0,0]
####################################################################Examining Data
#read in data
data = pd.read_csv("IrisTextFiles/PianoMarvelNoTotal.csv")#
data = data[data.Grade < 10]
# data2 = data[data.Grade == 8]
# frames = [data1,data2]
# data = pd.concat(frames)

N = 1000
data = data.sample(frac=1).reset_index(drop=True)
data = data.groupby('Grade')\
    .apply(lambda x: x[:N])

dict = {}
for elem in data.Grade:
    if elem not in dict:
        dict[elem] = 0
    dict[elem] = dict[elem] + 1

print(dict)





###################################################Linear Regression

#linear regression
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
labels = data['Grade']
train1 = data.drop(['Grade'],axis = 1)
#scale data
scaler = MinMaxScaler()
minMaxScale = scaler.fit(train1)
train1 = minMaxScale.transform(train1)

#.2 and random_state = 0 best result,test_size.1
#best result = .1, 2
random_state = 0
highest_accuracy = 0
highest_accuracy_state = 0
#while(random_state<1):
#print("random state: ",random_state)
x_train,x_test,y_train,y_test = train_test_split(train1,labels,test_size=.2,random_state=1)


###################################################Gradient Boosting Regression
from sklearn import ensemble
#n_estimators=420,max_depth=5,min_samples_split=2,learning_rate=.1(best result so far)
#best result: n_estimators=500,max_depth=5,min_samples_split=2,learning_rate=.1: accuracy .74 music_IriseAmbroseCustom
#best result: n_estimators=1000,max_depth=5,min_samples_split=2,learning_rate=.1: accuracy .80 music_IrisCustomFeatures15LL(didn't have classical music)
#best result: n_estimators=1000,max_depth=5,min_samples_split=2,learning_rate=.05: accuracy .86 music_IrisCustomFeatures15LL
learning_rates = [.01,0.05, 0.1, 0.25, 0.5, 0.75, 1]
estimators = 10000
# for learning_rate in learning_rates:
current_accuracy = 0

clf = ensemble.GradientBoostingRegressor(n_estimators=estimators, learning_rate=.01,min_samples_split=2,min_samples_leaf=1, max_features=10)
clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)
current_accuracy = clf.score(x_test,y_test)
# if current_accuracy>=highest_accuracy:
#     highest_accuracy = current_accuracy
#     highest_accuracy_state = random_state
print("training score: ",clf.score(x_train,y_train))
print(current_accuracy)

mse = mean_squared_error(y_test, clf.predict(x_test))
print("MSE: %.4f" % mse)










    #random_state+=1
#
# filename = './ClassificationModels/NoTotalGBR1.sav'
# joblib.dump(clf, filename)





#######################################################Plot multidimensional data
# from pandas.tools.plotting import parallel_coordinates
#
# # Take the iris dataset
# import seaborn as sns
# data = sns.load_dataset('iris')
#
# Make the multidimensional plot
# parallel_coordinates(data, 'Grade', colormap=plt.get_cmap("Set2"))
# plt.show()







#######################################################plot deviance of two models
# I think deviance is just how good the model is compared to the perfect model
# ie how well this model explains the data, it seems like the score is the deviance
# calculation used for deviance: (dev_max-dev_model)/dev_max

# test_score = np.zeros((estimators,), dtype=np.float64)
# for i, y_pred in enumerate(clf.staged_predict(x_test)):
#     test_score[i] = clf.loss_(y_test, y_pred)
#
#
# plt.figure(figsize=(10, 7))
# plt.subplot(1, 2, 1)
# plt.title('Deviance')
# plt.plot(np.arange(estimators) + 1, clf.train_score_, 'b-',
#          label='Training Set Deviance')
# plt.plot(np.arange(estimators) + 1, test_score, 'r-',
#          label='Test Set Deviance')
# plt.legend(loc='upper right')
# plt.xlabel('Boosting Iterations')
# plt.ylabel('Deviance')
#
# # Plot feature importance
# feature_importance = clf.feature_importances_
# # make importances relative to max importance
# feature_importance = 100.0 * (feature_importance / feature_importance.max())
# sorted_idx = np.argsort(feature_importance)
# print(sorted_idx)
#
# pos = np.arange(sorted_idx.shape[0]) + .5
# ## plt.subplot(1, 2, 2)
# ## plt.barh(pos, feature_importance[sorted_idx], align='center')
# ## plt.yticks(pos, data.columns[sorted_idx])
# ## plt.xlabel('Relative Importance')
# ## plt.title('Variable Importance')
# plt.show()


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Only use the labels that appear in the data
    # classes = classes[unique_labels(y_true, y_pred)]
    classes = unique_labels(pd.Series(y_true))

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')




    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)

    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


np.set_printoptions(precision=2)

y_pred_new = []
for y in y_pred:
    y_new = round_half_up(y,0)
    y_pred_new.append(y_new)

# Plot non-normalized confusion matrix
plot_confusion_matrix(y_test, y_pred_new, classes=labels,
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plot_confusion_matrix(y_test, y_pred_new, classes=labels, normalize=True,
                      title='Normalized confusion matrix')

plt.show()




# from sklearn.linear_model import Ridge
# from yellowbrick.regressor import ResidualsPlot
#
# # Instantiate the linear model and visualizer
# ridge = Ridge()
# visualizer = ResidualsPlot(ridge)
#
# visualizer.fit(x_train, y_train)  # Fit the training data to the model
# visualizer.score(x_test, y_test)  # Evaluate the model on the test data
# visualizer.poof()
