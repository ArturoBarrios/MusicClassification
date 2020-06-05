import matplotlib.pyplot as plt
from mlxtend.plotting import scatterplotmatrix
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import numpy as np


df = pd.read_csv("IrisTextFiles/PianoMarvelNoTotal.csv")
X = df[['average_large_10jumps_LH']]
y = df['Grade'].values


#show residuals
data = df[df.Grade < 10]
labels = data['Grade']
train1 = data.drop(['Grade'],axis = 1)

X_train,X_test,y_train,y_test = train_test_split(train1,labels,test_size=.4,random_state=1)

from sklearn.ensemble import RandomForestRegressor
forest = RandomForestRegressor(n_estimators=1000,criterion='mse',random_state=1,n_jobs=-1)
from sklearn.linear_model import RANSACRegressor
from sklearn.linear_model import LinearRegression
from sklearn import ensemble

ransac = RANSACRegressor(ensemble.RandomForestRegressor(), max_trials=100, min_samples=50, loss='absolute_loss',residual_threshold=5.0,random_state=0).fit(X,y)
inlier_mask = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)

line_X = np.arange(3, 10, 1)
line_y_ransac = ransac.predict(line_X[:, np.newaxis])
plt.scatter(X[inlier_mask], y[inlier_mask],
             c='steelblue', edgecolor='white',
            marker='o', label='Inliers')
plt.scatter(X[outlier_mask], y[outlier_mask],
            c='limegreen', edgecolor='white',
             marker='s', label='Outliers')
plt.plot(line_X, line_y_ransac, color='black', lw=2)
plt.xlabel('Average number of rooms [RM]')
plt.ylabel('Price in $1000s [MEDV]')
plt.legend(loc='upper left')
plt.show()


# forest.fit(X_train,y_train)
# y_train_pred = forest.predict(X_train)
# y_test_pred = forest.predict(X_test)
# print('MSE train: %.3f, test: %.3f' % (mean_squared_error(y_train, y_train_pred),mean_squared_error(y_test, y_test_pred)))
# print('R^2 train: %.3f, test: %.3f' % (r2_score(y_train, y_train_pred),r2_score(y_test, y_test_pred)))

