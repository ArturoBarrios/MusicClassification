import loader
from sklearn.model_selection import train_test_split

#loading example data
x_labels = []
f = open("./data/musicIrisLowLevelFeaturesAll.txt","r")
line = f.read()
#put labels in x_labels

for label in line.split(","):
    x_labels.append(label)

X, y, type2id = loader.load_data('./data/musicIrisLowLevelFeaturesAll.csv', y_label="Grade", x_labels=x_labels)

# Create the train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.linear_model import Ridge
from yellowbrick.regressor import ResidualsPlot

# Instantiate the linear model and visualizer
ridge = Ridge()
visualizer = ResidualsPlot(ridge)

visualizer.fit(X_train, y_train)  # Fit the training data to the model
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.poof()                 # Draw/show/poof the data
