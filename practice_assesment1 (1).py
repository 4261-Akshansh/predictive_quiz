# -*- coding: utf-8 -*-
"""practice_assesment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MBLf-aMAj2oeUAmy1_bxIWpO4nTX64X0
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import numpy as np

df = pd.read_csv('/content/DSAI-LVA-DATASET for Quiz (1).csv')
df

print("Unique values in 'Pass' column before mapping:", df['Pass'].unique())

target_mapping = {'fail': 0, 'passed with low grade': 1, 'passed with high grade': 2}

df['Pass'] = df['Pass'].map(target_mapping)


encoder = OneHotEncoder(sparse=False, drop='first')
parent_education_encoded = encoder.fit_transform(df[['ParentEducation']])
df_encoded = pd.concat([df.drop(['ParentEducation', 'Pass'], axis=1),
                        pd.DataFrame(parent_education_encoded, columns=encoder.get_feature_names_out()),
                        df['Pass']], axis=1)


X = df_encoded.drop('Pass', axis=1)
X.columns = X.columns.astype(str)
y = df_encoded['Pass']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


inv_target_mapping = {v: k for k, v in target_mapping.items()}
y_test_inv = np.vectorize(inv_target_mapping.get)(y_test)
y_pred_inv = np.vectorize(inv_target_mapping.get)(y_pred)

print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(f"Classification Report:\n{classification_report(y_test_inv, y_pred_inv)}")

cm = confusion_matrix(y_test_inv, y_pred_inv, labels=list(inv_target_mapping.values()))
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=inv_target_mapping.values(), yticklabels=inv_target_mapping.values())
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.title('Confusion Matrix with Original Labels')
plt.show()

