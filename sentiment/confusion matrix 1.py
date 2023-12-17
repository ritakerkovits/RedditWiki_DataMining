import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools

# Load your file
file_path = '/Users/toroklili/Corvinus/7.felev/Szentiment/Reddit/RedditManualScore_350_normalised_vader.csv'  # Replace with your file path
df = pd.read_csv(file_path, sep=';')  # Replace ',' with the appropriate deli



rating_classes = list(df['Manual_score_n'])
sentiment_values1  = list(df['L_Sentiment_n'])
sentiment_values2  = list(df['S_Sentiment_n'])

from sklearn.metrics import classification_report
target_names = ["negative", "neutral", "positive"]
print('L_Sentiment confusion matrix')
print(classification_report(rating_classes, sentiment_values1, target_names=target_names))
print('S_Sentiment confusion matrix')
print(classification_report(rating_classes, sentiment_values2, target_names=target_names))

# Function to plot confusion matrix
def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=None, normalize=True):
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()

# Generate confusion matrices
cm_l_sentiment = confusion_matrix(df['Manual_score_n'], df['L_Sentiment_n'])
cm_s_sentiment = confusion_matrix(df['Manual_score_n'], df['S_Sentiment_n'])

# Plot the confusion matrices
target_names = ["negative", "neutral", "positive"]



print('S_Sentiment Confusion Matrix')
plot_confusion_matrix(cm_s_sentiment, target_names, title='Stemming Confusion Matrix' )

print('L_Sentiment Confusion Matrix')
plot_confusion_matrix(cm_l_sentiment, target_names, title='Lemmatized Confusion Matrix')