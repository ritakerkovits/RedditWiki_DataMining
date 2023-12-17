import pandas as pd

# Assuming your original CSV file is named 'original.csv'
original_file_path = 'C:/Users/Public/RS_politics_extracted.csv'

# Read the original CSV file
df = pd.read_csv(original_file_path)
#Flagging sarcastic content (/s) but not links (http) or other words that contain '/s' eg '/sports'
df['isSarcasm'] = df['title'].str.contains(r'(?<!\S)/s(?!http)')
# Select only the specified columns
selected_columns = ['id', 'author',  'created_utc', 'title', 'subreddit_id', 'score' , 'isSarcasm']
df_selected = df[selected_columns]
#df_selected['id'] = df_selected['id'].str[3:]

#Removing prefiexs from subreddit_id
df_selected['subreddit_id'] = df_selected['subreddit_id'].str[3:]

# Specify the path for the new CSV file
new_file_path = 'RS_Filtered.csv'

# Export the selected columns to a new CSV file
df_selected.to_csv(new_file_path, index=False)

print(f'Exported selected columns to {new_file_path}')
