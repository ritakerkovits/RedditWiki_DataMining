from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the labeled data
df_labeled = pd.read_csv(r'C:\Users\Zeke Gábor\Desktop\123\TextMining\data\labeled_data3.csv', delimiter=';')

# Example data
X = df_labeled['differences']
y = df_labeled['Sentiment']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to TF-IDF features
vectorizer = TfidfVectorizer(stop_words='english',
                             min_df=2,
                             max_df=0.3,
                             sublinear_tf=True,
                             use_idf=True)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Define the parameter grid to search
param_grid = {'C': [0.1, 1, 3, 5.7, 8, 10],
              'kernel': ['linear', 'rbf', 'poly'],
              'gamma': ['scale', 'auto', 0.1, 0.01, 0.001]}

# Create an SVM classifier
svm_classifier = svm.SVC(decision_function_shape='ovr')

# Create a GridSearchCV object
grid_search = GridSearchCV(svm_classifier, param_grid, cv=5, scoring='accuracy')

# Fit the GridSearchCV object to the training data
grid_search.fit(X_train_tfidf, y_train)

# Get the best parameters from the grid search
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

# Use the best parameters to train the SVM model
best_classifier = svm.SVC(**best_params, decision_function_shape='ovr')
best_classifier.fit(X_train_tfidf, y_train)

# Predict sentiment on the test set using the best model
y_pred_best = best_classifier.predict(X_test_tfidf)

# Calculate accuracy using the best model
accuracy_best = accuracy_score(y_test, y_pred_best)
print("Best Model Accuracy:", accuracy_best)

# Predict sentiment on the original, larger dataset
X_original = df_labeled['differences'].to_list()
X_original_tfidf = vectorizer.transform(X_original)
y_original_pred_best = best_classifier.predict(X_original_tfidf)

# Create a DataFrame with the predictions
df_pred_best = pd.DataFrame(y_original_pred_best, columns=['Pred_sent_best'])

# Concatenate the results with the original data and predictions
df_results_best = pd.concat([df_labeled, df_pred_best], axis='columns')

# Print the correlation between actual and predicted sentiments
correlation_best = df_results_best['Sentiment'].corr(df_results_best['Pred_sent_best'])

actual_sentiments = df_results_best['Sentiment']
predicted_sentiments = df_results_best['Pred_sent_best']

# Create a confusion matrix
conf_matrix = confusion_matrix(actual_sentiments, predicted_sentiments)

print("Correlation between Actual and Predicted Sentiments (Best Model):", correlation_best)

# Display the confusion matrix using a heatmap
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=df_results_best['Sentiment'].unique(), yticklabels=df_results_best['Sentiment'].unique())
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()