import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer, PorterStemmer
import string

#Download necessary NLTK packages
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('wordnet')

# Read CSV file
df = pd.read_csv('PConversation.csv')

# Initialize Sentiment Analyzer, Lemmatizer and Stemmer
analyzer = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Lemmatizing Function
def lemmatize(text):
    text = str(text)
    # Remove punctuation, tokenize, remove stopwords, lemmatize
    if text is not None:
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokenized_content = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokenized_content if word not in stop_words]
        lemmatized_tokens = [lemmatizer.lemmatize(token, pos="a") for token in filtered_tokens]
        lemmatized_tokens = [lemmatizer.lemmatize(token, pos="n") for token in lemmatized_tokens]
        lemmatized_tokens = [lemmatizer.lemmatize(token, pos="r") for token in lemmatized_tokens]
        lemmatized_tokens = [lemmatizer.lemmatize(token, pos="v") for token in lemmatized_tokens]
        processed_token = ' '.join(lemmatized_tokens)
    else:
        processed_token = ' '
    return processed_token

# Stemming Function
def stem(text):
    text = str(text)
    # Remove punctuation, tokenize, remove stopwords, stem
    if text is not None:
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokenized_content = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokenized_content if word not in stop_words]
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
        processed_token = ' '.join(stemmed_tokens)
    else:
        processed_token = ' '
    return processed_token

# Apply lemmatizing to 'raw_content' column
df['lemmatized'] = df['raw_content'].apply(lemmatize)

# Apply stemming to 'raw_content' column
df['stemmed'] = df['raw_content'].apply(stem)

# Sentiment Analysis
def getCompound(text):
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    return compound_score

# Apply sentiment analysis to 'raw_content', 'lemmatized' and 'stemmed' columns
df['L_Sentiment'] = df['lemmatized'].apply(getCompound)
df['S_Sentiment'] = df['stemmed'].apply(getCompound)

# Save to CSV
df.to_csv(r'sentiment_lemmatized_stemmed.csv', encoding='utf-8-sig')
    
