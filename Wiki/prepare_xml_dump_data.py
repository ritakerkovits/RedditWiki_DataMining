import xml.etree.ElementTree as ET
import pandas as pd
import re
from difflib import unified_diff
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import warnings

# --------------------------------
# FUNCTIONS
# --------------------------------

def get_title_from_text(string_of_text):
    '''
    :param string_of_text: Text property of the current Wikipedia dump XML as string
    :return: Returns the subject title of the specific XML text property.
    '''
    if string_of_text is not None:
        title = ''
        string_of_text = str(string_of_text)
        list_of_textline = string_of_text.splitlines()
        list_of_textline = list(map(str.strip, list_of_textline))
        for i in reversed(range(0, len(list_of_textline))):
            element = list_of_textline[i]
            if element.startswith("==") and not element.startswith("==="):
                first_equals = element.find('==')
                second_equals = element.find('==', first_equals + 1)
                title = element[first_equals + 2 : second_equals]
                break
    else:
        title = ''
    return title

def remove_html_tags(text):
    '''
    :param text: Text input to perform HTML parsing on as type string
    :return: Returns a string without HTML tags
    '''
    if text is None:
        return text
    else:
        text = str(text)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
            soup = BeautifulSoup(text, features='lxml')
            return soup.get_text()
        
def compare(dataframe):
    '''
    :param dataframe: Pandas Dataframe to perform the diff on (type pd.Dataframe)
    :return: The results of the Diff as a list 
    '''
    diff_all = []
    for i in range(len(dataframe) - 1):
        if dataframe.iloc[i]['text'] is not None and dataframe.iloc[i + 1]['text'] is not None:
            if dataframe.iloc[i]['page_id'] == dataframe.iloc[i + 1]['page_id']:
                text1 = dataframe.iloc[i]['text'].splitlines()
                text2 = dataframe.iloc[i + 1]['text'].splitlines()
                diff = list(unified_diff(text1, text2, lineterm=''))
                diff_all.append('\n'.join(diff))
            else:             
                diff_all.append('')
        else:             
            diff_all.append('')
    
    diff_all = [get_differences(item) for item in diff_all]
    diff_all.insert(0, dataframe.loc[0]['text'])
    
    return diff_all

def get_differences(string):
    '''
    :param string: String type input to perform function on
    :return: Unified_diff method returns a string where the line starting with 
             a '+' character is the difference of the two input strings. The function
             returns the line which starts with a single '+' character.
    '''
    string_list = []
    string_list = string.splitlines()
    for item in string_list: 
        if item.startswith('+') and not item.startswith('+++'):
            string = item[1:]
        else:
            string = ''
    return string

def remove_spec_char(text):
    '''
    :param: text: Text to execute regex methods on as type string.
    :return: Returs the text with not needed characters removed.
    '''
    text = re.sub(r'<[^>]*>.*?<\/[^>]*>', '', text)
    text = re.sub(r'\[\[[^\]]*\|', '', text)  # Removes wiki link alias
    text = re.sub(r'\{\{[^\}]*\}\}', '', text)  # Removes templates
    text = re.sub(r'\'\'\'|\'\'', '', text)
    text = re.sub(r'\{\|[^\}]*\|\}', '', text)  # Removes tables
    text = re.sub(r'\|\s*style=".*?""', '', text)
    text = re.sub(r'\|.*?\|', '', text) #removes the content within | 
    text = re.sub(r'\[\[|\]\]', '', text)  # Removes wiki links
    text = re.sub('\t', '', text)
    return text    
    
# --------------------------------
# MAIN PROCESS
# --------------------------------

df_wiki_data = pd.read_csv(r'C:\\Users\\Ritus\\OneDrive\\Dokumentumok\\7.félév\\komplex\\python\\enwiki_huge.csv')


df_wiki_data = df_wiki_data.rename(columns={'Unnamed: 0': 'iteration'})

df_wiki_data['timestamp'] = pd.to_datetime(df_wiki_data['timestamp'])
df_wiki_data['timestamp'] = df_wiki_data['timestamp'].dt.strftime("%Y/%m/%d %H:%M")

df_wiki_data['subject_title'] = df_wiki_data['text'].apply(func=get_title_from_text)

df_wiki_data['user2'] = df_wiki_data['page_title'].str.split(':').str[1]

df_wiki_data['text'] = df_wiki_data['text'].apply(remove_html_tags)
df_wiki_data['text'] = df_wiki_data['text'].apply(remove_spec_char)

df_wiki_data['differences'] = compare(dataframe = df_wiki_data)
df_wiki_data.loc[df_wiki_data['iteration'] == 0, 'differences'] = df_wiki_data['text']

print(df_wiki_data.sample(5))

df_wiki_data.to_csv("enwiki_huge.csv")