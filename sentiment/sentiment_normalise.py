import pandas as pd

# Load your file
file_path = '/Users/toroklili/Corvinus/7.felev/Szentiment/Reddit/RedditManualScore350.csv'  # Replace with your file path
df = pd.read_csv(file_path, sep=';')  # Replace ',' with the appropriate deli

# Function to normalize L_sentiment and S_sentiment
def score_to_rating(value):
    if value > 0.2:
        return 1
    elif value <= 0.2 and value >= -0.2:
        return 0
    else:
        return -1

# Normalize L_sentiment and S_sentiment
df['L_Sentiment_n'] = df['L_Sentiment'].apply(lambda x:score_to_rating(x))
df['S_Sentiment_n'] = df['S_Sentiment'].apply(lambda x:score_to_rating(x))

# Function to normalize the manual score
def score_to_Target(value):
    if value > 4:
        return 1
    elif value in [3, 4]:
        return 0
    else:
        return -1

# Normalize the manual score
df['Manual_score_n'] = df['Manual_score'].apply(lambda x:score_to_Target(x))  # Replace 'manual_score' with the actual column name for manual score

# Save the modified DataFrame
df.to_csv('RedditManualScore350_normalised.csv', index=False)
print('File saved')