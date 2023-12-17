import pandas as pd
import datetime
df_s = pd.read_csv('C:/Users/Public/RS_Filtered.csv')
df_c = pd.read_csv('C:/Users/Public/RC_Filtered.csv')
df_c2 = pd.read_csv('C:/Users/Public/RC_Filtered.csv')
print(df_c.columns)

#Creating common structure for both tables 
#Submissions 
df_s.rename(columns= {'title' : 'body'} , inplace=True )
df_s['parent_id']='None'
df_s['link_id']='None'

df_s=df_s.reindex(columns=['id', 'author', 'created_utc', 'body', 'parent_id', 'link_id', 'score', 'isSarcasm'])
#Filling up the conversation with posts, so that filling up the parnet with empty values
df_c['subreddit_id']='None'
#Renaming columns to match the other table
df_s=df_s.reindex(columns=['id', 'author', 'created_utc', 'body', 'parent_id', 'link_id' , 'score', 'isSarcasm' ])
df_c=df_c.reindex(columns=['id', 'author', 'created_utc', 'body', 'parent_id', 'link_id', 'score', 'isSarcasm'])

print(df_c.columns)
print(df_s.columns)

#Concatenating the two tables
search =pd.concat([df_c, df_s], ignore_index=True)


#Merging the two tables so that the parents can be matched with there children
merged_df = pd.merge(search, df_c2, left_on='id', right_on='parent_id', how='inner')

print(merged_df.columns)

#Renaming columns to match the requriements of the desired output, only keeping the necessary columns under the correct names
df_s.rename(columns={'id' : 'id_y', 'author' : 'author_y', 'created_utc' : 'created_utc_y', 'body' : 'body_y' , 'parent_id' : 'parent_id_y', 'link_id' : 'link_id_y' , 'score':'score_y', 'isSarcasm' : 'isSarcasm_y' }, inplace=True)
df_s['id_x'] = df_s['author_x']  = df_s['body_x'] = df_s['parent_id_x'] = df_s['link_id_x'] = df_s['score_x']= df_s['isSarcasm_x']= 'None'
df_s['created_utc_x'] = '0'
df_s['link_id_y'] = df_s['id_y']

paired =pd.concat([merged_df, df_s], ignore_index=True)

print(df_s)
#Renaming columns to match the requriements of the desired output, only keeping the necessary columns under the correct names
columns_to_keep = ['id_y','created_utc_y', 'author_y', 'author_x', 'body_y', 'link_id_y', 'parent_id_y', 'id_x', 'score_y', 'isSarcasm_y']
new_column_names = ['id','created_utc', 'user1', 'user2', 'raw_content' , 'topic', 'parent_id', 'id_of_parent', 'score', 'isSarcasm']

df_conversation = paired[columns_to_keep].rename(columns=dict(zip(columns_to_keep, new_column_names)))


#Converting the time to datetime format
df_conversation['created_utc'] = pd.to_datetime(df_conversation['created_utc'], unit='s')
#exporting the output
df_conversation.to_csv('Conversation.csv')

