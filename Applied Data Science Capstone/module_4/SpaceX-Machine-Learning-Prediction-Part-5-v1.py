# Databricks notebook source
# MAGIC %md
# MAGIC <p style="text-align:center">
# MAGIC     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01" target="_blank">
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
# MAGIC     </a>
# MAGIC </p>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # **Space X  Falcon 9 First Stage Landing Prediction**
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hands on Lab: Complete the Machine Learning Prediction lab
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Estimated time needed: **60** minutes
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Space X advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against space X for a rocket launch.   In this lab, you will create a machine learning pipeline  to predict if the first stage will land given the data from the preceding labs.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing_1.gif)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Several examples of an unsuccessful landing are shown here:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Most unsuccessful landings are planed. Space X; performs a controlled landing in the oceans.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Objectives
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Perform exploratory  Data Analysis and determine Training Labels
# MAGIC
# MAGIC *   create a column for the class
# MAGIC *   Standardize the data
# MAGIC *   Split into training data and test data
# MAGIC
# MAGIC \-Find best Hyperparameter for SVM, Classification Trees and Logistic Regression
# MAGIC
# MAGIC *   Find the method performs best using test data
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Libraries and Define Auxiliary Functions
# MAGIC

# COMMAND ----------

!pip install numpy
!pip install pandas
!pip install seaborn
!pip install scikit-learn

# COMMAND ----------

# MAGIC %md
# MAGIC We will import the following libraries for the lab
# MAGIC

# COMMAND ----------

# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier

# COMMAND ----------

# MAGIC %md
# MAGIC This function is to plot the confusion matrix.
# MAGIC

# COMMAND ----------

def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed']) 
    plt.show() 

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load the dataframe
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Load the data
# MAGIC

# COMMAND ----------

data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")


# COMMAND ----------

data.head()

# COMMAND ----------


X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')

# COMMAND ----------

X.head(100)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  1
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Create a NumPy array from the column <code>Class</code> in <code>data</code>, by applying the method <code>to_numpy()</code>  then
# MAGIC assign it  to the variable <code>Y</code>,make sure the output is a  Pandas series (only one bracket df\['name of  column']).
# MAGIC

# COMMAND ----------

Y = data['Class'].to_numpy()
Y

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  2
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Standardize the data in <code>X</code> then reassign it to the variable  <code>X</code> using the transform provided below.
# MAGIC

# COMMAND ----------

# students get this 
X = preprocessing.StandardScaler().fit_transform(X)
#X = transform.fit_transform(X)

# COMMAND ----------

# MAGIC %md
# MAGIC We split the data into training and testing data using the  function  <code>train_test_split</code>.   The training data is divided into validation data, a second set used for training  data; then the models are trained and hyperparameters are selected using the function <code>GridSearchCV</code>.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  3
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Use the function train_test_split to split the data X and Y into training and test data. Set the parameter test_size to  0.2 and random_state to 2. The training data and test data should be assigned to the following labels.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <code>X_train, X_test, Y_train, Y_test</code>
# MAGIC

# COMMAND ----------

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 2)

# COMMAND ----------

# MAGIC %md
# MAGIC we can see we only have 18 test samples.
# MAGIC

# COMMAND ----------

Y_test.shape

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  4
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Create a logistic regression object  then create a  GridSearchCV object  <code>logreg_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# MAGIC

# COMMAND ----------

parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'],
             'solver':['lbfgs']}

# COMMAND ----------

parameters ={"C":[0.01,0.1,1],'penalty':['l2'], 'solver':['lbfgs']}# l1 lasso l2 ridge
lr=LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters, cv = 10)
logreg_cv.fit(X_train,Y_train)

# COMMAND ----------

# MAGIC %md
# MAGIC We output the <code>GridSearchCV</code> object for logistic regression. We display the best parameters using the data attribute <code>best_params\_</code> and the accuracy on the validation data using the data attribute <code>best_score\_</code>.
# MAGIC

# COMMAND ----------

print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  5
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Calculate the accuracy on the test data using the method <code>score</code>:
# MAGIC

# COMMAND ----------

# Calculate accuracy on test data
accuracy = logreg_cv.score(X_test, Y_test)
print("Test accuracy:", accuracy)

# COMMAND ----------

# MAGIC %md
# MAGIC Lets look at the confusion matrix:
# MAGIC

# COMMAND ----------

yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# COMMAND ----------

# MAGIC %md
# MAGIC Examining the confusion matrix, we see that logistic regression can distinguish between the different classes.  We see that the problem is false positives.
# MAGIC
# MAGIC Overview:
# MAGIC
# MAGIC True Postive - 12 (True label is landed, Predicted label is also landed)
# MAGIC
# MAGIC False Postive - 3 (True label is not landed, Predicted label is landed)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  6
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Create a support vector machine object then  create a  <code>GridSearchCV</code> object  <code>svm_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# MAGIC

# COMMAND ----------

parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = SVC()

# COMMAND ----------

svm_cv = GridSearchCV(svm, param_grid = parameters, cv = 10)
svm_cv.fit(X_train, Y_train) 

# COMMAND ----------

print("tuned hpyerparameters :(best parameters) ",svm_cv.best_params_)
print("accuracy :",svm_cv.best_score_)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  7
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Calculate the accuracy on the test data using the method <code>score</code>:
# MAGIC

# COMMAND ----------

acurracy_svm = svm_cv.score(X_test,Y_test)
print(f"Accuracy SVM: {acurracy_svm}")

# COMMAND ----------

# MAGIC %md
# MAGIC We can plot the confusion matrix
# MAGIC

# COMMAND ----------

yhat=svm_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  8
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Create a decision tree classifier object then  create a  <code>GridSearchCV</code> object  <code>tree_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# MAGIC

# COMMAND ----------

parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

tree = DecisionTreeClassifier()

# COMMAND ----------

tree_cv = GridSearchCV(tree, parameters, cv = 10)
tree_cv.fit(X_train, Y_train)

# COMMAND ----------

print("tuned hpyerparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  9
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:
# MAGIC

# COMMAND ----------

accuracy_tree = tree_cv.score(X_test,Y_test)
print(f"Accuracy Tree: {accuracy_tree}")

# COMMAND ----------

# MAGIC %md
# MAGIC We can plot the confusion matrix
# MAGIC

# COMMAND ----------

yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  10
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Create a k nearest neighbors object then  create a  <code>GridSearchCV</code> object  <code>knn_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# MAGIC

# COMMAND ----------

parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}

KNN = KNeighborsClassifier()

# COMMAND ----------

knn_cv = GridSearchCV(KNN, parameters, cv = 10)
knn_cv.fit(X_train, Y_train)

# COMMAND ----------

print("tuned hpyerparameters :(best parameters) ",knn_cv.best_params_)
print("accuracy :",knn_cv.best_score_)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  11
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Calculate the accuracy of knn_cv on the test data using the method <code>score</code>:
# MAGIC

# COMMAND ----------

acuracy_knn = knn_cv.score(X_test,Y_test)
print(f"Accuracy KNN: {acuracy_knn}")

# COMMAND ----------

# MAGIC %md
# MAGIC We can plot the confusion matrix
# MAGIC

# COMMAND ----------

yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK  12
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Find the method performs best:
# MAGIC

# COMMAND ----------

# Compare all model accuracies
import pandas as pd

models = {
    'Logistic Regression': accuracy,
    'SVM': acurracy_svm,
    'Decision Tree': accuracy_tree,
    'KNN': acuracy_knn
}

# Create DataFrame for comparison
results_df = pd.DataFrame(list(models.items()), columns=['Model', 'Test Accuracy'])
results_df = results_df.sort_values('Test Accuracy', ascending=False).reset_index(drop=True)

print("\n=== Model Performance Comparison ===")
print(results_df.to_string(index=False))

# Find best model
best_model = results_df.iloc[0]['Model']
best_accuracy = results_df.iloc[0]['Test Accuracy']

print(f"\n🏆 Best Model: {best_model} with accuracy of {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")

# Visualize comparison
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(results_df['Model'], results_df['Test Accuracy'], color=['green', 'blue', 'orange', 'red'])
plt.xlabel('Model', fontsize=12)
plt.ylabel('Test Accuracy', fontsize=12)
plt.title('Model Performance Comparison', fontsize=14, fontweight='bold')
plt.ylim([0, 1.0])
plt.xticks(rotation=45, ha='right')

# Add value labels on bars
for i, v in enumerate(results_df['Test Accuracy']):
    plt.text(i, v + 0.02, f'{v:.4f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()

results_df

# COMMAND ----------

# MAGIC %md
# MAGIC ## Authors
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC [Pratiksha Verma](https://www.linkedin.com/in/pratiksha-verma-6487561b1/)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <!--## Change Log--!>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <!--| Date (YYYY-MM-DD) | Version | Changed By      | Change Description      |
# MAGIC | ----------------- | ------- | -------------   | ----------------------- |
# MAGIC | 2022-11-09        | 1.0     | Pratiksha Verma | Converted initial version to Jupyterlite|--!>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### <h3 align="center"> IBM Corporation 2022. All rights reserved. <h3/>
# MAGIC