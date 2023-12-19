from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

file_path = r"C:\\Users\\Ritus\\OneDrive\\Dokumentumok\\7.félév\\komplex\\labeled_to_confusion.csv"
df_sentiment = pd.read_csv(file_path)

print(df_sentiment.head())


target = df_sentiment['label']
lemmatized = df_sentiment['lemmatized_norm']
stem = df_sentiment['stem_norm']

corr_lemm_target = target.corr(lemmatized)
corr_stem_target = target.corr(stem)
print(corr_lemm_target)
print(corr_stem_target)

'''
#Confsuin matrix for lemmatized
cm_lem = confusion_matrix(target, lemmatized)

plt.figure(figsize=(8, 6))
sns.heatmap(cm_lem, annot=True, fmt="d", cmap='Blues', xticklabels=target.unique(), yticklabels=target.unique())
plt.ylabel('Manual score')
plt.xlabel('Lemmatized score')
plt.title('Confusion Matrix for Lemmatized and Target scores')
plt.show()
'''


#Confsuin matrix for stemming
cm_stem = confusion_matrix(target, lemmatized)

plt.figure(figsize=(8, 6))
sns.heatmap(cm_stem, annot=True, fmt="d", cmap='Blues', xticklabels=[-1,0,1], yticklabels=[-1,0,1])
plt.ylabel('Target score')
plt.xlabel('Predicted score')
plt.title('Confusion Matrix for Stemming and Target scores')
plt.show()
