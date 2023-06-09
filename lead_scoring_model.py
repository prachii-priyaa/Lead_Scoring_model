# -*- coding: utf-8 -*-
"""UniAcco Assgn:Lead Scoring Model.ipynb

"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression

# Load the data
data = pd.read_csv('dataset.csv', header= 0,
                        encoding= 'unicode_escape')

# Data Cleaning and Feature Selection
data = data[data['status'].isin(['WON', 'LOST'])]  # Drop leads with status other than WON or LOST
selected_features = ['Agent_id', 'source_city', 'lost_reason', 'lead_id']  # Select important features
data = data[selected_features + ['status']]  # Create a new dataframe with selected features and status

# Data Preprocessing
data = data.replace('9b2d5b4678781e53038e91ea5324530a03f27dc1d0e5f6c9bc9d493a23be9de0', np.nan)  # Replace NaN values with np.nan
data = data.fillna('Unknown')  # Replace NaN values with a unique identifier
le = LabelEncoder()  # Create an instance of LabelEncoder
for col in data.columns:  # Convert all columns to categorical columns
    data[col] = le.fit_transform(data[col])

# Model Training and Testing
X = data.iloc[:, :-1]
y = data.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split the data into training and testing sets
model = LogisticRegression()  # Create an instance of Logistic Regression model
model.fit(X_train, y_train)  # Train the model on the training set
y_pred = model.predict(X_test)  # Predict the lead scores on the testing set

# Performance Evaluation
accuracy = accuracy_score(y_test, y_pred)  # Calculate the accuracy
precision = precision_score(y_test, y_pred, pos_label=0)  # Calculate the precision for WON leads
recall = recall_score(y_test, y_pred, pos_label=0)  # Calculate the recall for WON leads
f1 = f1_score(y_test, y_pred, pos_label=0)  # Calculate the F1-score for WON leads
print('Accuracy: {:.2f}'.format(accuracy))
print('Precision: {:.2f}'.format(precision))
print('Recall: {:.2f}'.format(recall))
print('F1-Score: {:.2f}'.format(f1))
