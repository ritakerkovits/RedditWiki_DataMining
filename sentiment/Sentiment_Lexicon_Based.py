import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer, PorterStemmer
import string
nltk.download('wordnethow ')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('vader_lexicon')


#Read CSV file
df = pd.read_csv('usertalk_enwiki_history10_v3.csv')

analyzer = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

#-------------------
#FUNCTIONS
#-------------------

# Part of speech tagging
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = { 
                "J" : wordnet.ADJ,
                "N" : wordnet.NOUN,
                "V" : wordnet.VERB,
                "R" : wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

# Lemmatizing Function
def lemmatize(text):
    text = str(text)
    if text is not None:
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokenized_content = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokenized_content if not word in stop_words]
        lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in filtered_tokens]
        processed_token = ' '.join(lemmatized_tokens)
    
    else:
        processed_token = ' '
    
    return processed_token

# Stemming Function
def stem(text):
    text = str(text)
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

# Get the compound sentiment score
def getCompound(text):
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    return compound_score

#-------------------
#MAIN PROCESS
#-------------------

df['lemmatized'] = df['differences'].apply(lemmatize)
df['stemming'] = df['differences'].apply(stem)
df['sentiment_score_lem'] = df['lemmatized'].apply(getCompound)
df['sentiment_score_stem'] = df['stemming'].apply(getCompound)

# Normalizing the sentiment scores to  [-1, 0, 1]
def score_to_rating(value):
    if value > 0.2:
        return 1
    if value <= 0.2 and value >= -0.2:
        return 0
    else:
        return -1
    
df['lemmatized_norm'] = df['sentiment_score_lem'].apply(lambda x:score_to_rating(x))
df['stem_norm'] = df['sentiment_score_stem'].apply(lambda x:score_to_rating(x))

save_file = r'sentiment_usertalk_enwiki_history3_v3.csv'
df.to_csv(save_file, encoding='utf-8')



