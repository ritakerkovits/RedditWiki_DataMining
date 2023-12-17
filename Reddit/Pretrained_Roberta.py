from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

# Check if GPU is available
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Running on device: {device}")

# Load tokenizer and model on GPU
tokenizer = AutoTokenizer.from_pretrained('mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis')
model = AutoModelForSequenceClassification.from_pretrained('mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis')
model.to(device)

# Example with tokens
tokens = tokenizer.encode('I love you', return_tensors='pt').to(device)
print(tokens[0])
print(tokenizer.decode(tokens[0]))

result = model(tokens)
sent = int(torch.argmax(result.logits)) + 1
print(sent)

# Read CSV file
df = pd.read_csv("RedditManualScore.csv", header=0, names=["id", "text", "label"], delimiter=';')
df.head()
print(df['text'].iloc[0])

# Define SentimentAnalysis function to run on GPU
def SentimentAnalysis(text):
    # Truncate or pad the input to a maximum length of 512 tokens
    tokens = tokenizer.encode(text, max_length=512, truncation=True, return_tensors='pt').to(device)
    result = model(tokens)
    sent = int(torch.argmax(result.logits)) + 1
    return sent
print('writing to df')

# Apply SentimentAnalysis function to the DataFrame
df['text'].to_string()
df['sentiment'] = df['text'].astype(str).apply(lambda x: SentimentAnalysis(x[:512]))
print('saving')

# Save the DataFrame to a new CSV file
df.to_csv('all.csv', index=False)
