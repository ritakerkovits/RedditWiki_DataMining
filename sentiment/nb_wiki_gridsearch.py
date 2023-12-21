from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
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
                             max_df=0.4,
                             sublinear_tf=True,
                             use_idf=True)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

param_grid = {'alpha': [0.1, 1, 3, 5.7, 8, 10]}

# Create a Multinomial Naive Bayes classifier
nb_classifier = MultinomialNB()

grid_search = GridSearchCV(nb_classifier, param_grid, cv=5, scoring='accuracy')

grid_search.fit(X_train_tfidf, y_train)
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

nb_classifier = MultinomialNB(alpha=best_params['alpha'])
nb_classifier.fit(X_train_tfidf, y_train)

# Predict sentiment on the test set using the Naive Bayes model
y_pred_nb = nb_classifier.predict(X_test_tfidf)

# Calculate accuracy using the Naive Bayes model
accuracy_nb = accuracy_score(y_test, y_pred_nb)
print("Naive Bayes Model Accuracy:", accuracy_nb)

# Predict sentiment on the original, larger dataset using Naive Bayes
X_original = df_labeled['differences'].to_list()
X_original_tfidf = vectorizer.transform(X_original)
y_original_pred_nb = nb_classifier.predict(X_original_tfidf)

# Create a DataFrame with the Naive Bayes predictions
df_pred_nb = pd.DataFrame(y_original_pred_nb, columns=['Pred_sent_nb'])

# Concatenate the results with the original data and Naive Bayes predictions
df_results_nb = pd.concat([df_labeled, df_pred_nb], axis='columns')

# Print the correlation between actual and Naive Bayes predicted sentiments
correlation_nb = df_results_nb['Sentiment'].corr(df_results_nb['Pred_sent_nb'])

actual_sentiments = df_results_nb['Sentiment']
predicted_sentiments = df_results_nb['Pred_sent_nb']

# Create a confusion matrix for Naive Bayes
conf_matrix_nb = confusion_matrix(actual_sentiments, predicted_sentiments)
print("Correlation between Actual and Predicted Sentiments (Naive Bayes):", correlation_nb)

# Display the confusion matrix using a heatmap for Naive Bayes
sns.heatmap(conf_matrix_nb, annot=True, fmt='d', cmap='Blues', xticklabels=df_results_nb['Sentiment'].unique(), yticklabels=df_results_nb['Sentiment'].unique())
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Naive Bayes)')
plt.show()