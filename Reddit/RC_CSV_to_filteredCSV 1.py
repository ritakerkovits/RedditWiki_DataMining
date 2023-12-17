import pandas as pd

#Path to input file
original_file_path = 'C:/Users/Public/RC_politics_extracted.csv'

# Reading the input file
df = pd.read_csv(original_file_path)

#Flagging sarcastic content (/s) but not links (http) or other words that contain '/s' eg '/sports'
df['isSarcasm'] = df['body'].str.contains(r'(?<!\S)/s(?!http)')
# Select only the specified columns
selected_columns = ['id', 'author',  'created_utc', 'body', 'parent_id', 'link_id', 'score', 'isSarcasm']  
#Removing prefiexs 
df_selected = df[selected_columns]
df_selected['link_id'] = df_selected['link_id'].str[3:]
df_selected['parent_id'] = df_selected['parent_id'].str[3:]
new_file_path = 'RC_Filtered.csv'
# Export the selected columns to a new CSV file
df_selected.to_csv(new_file_path, index=False)

print(f'Új fájl létrehozva {new_file_path}')