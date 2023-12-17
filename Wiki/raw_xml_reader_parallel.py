import xml.etree.ElementTree as ET
import pandas as pd
import time
import psutil
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

start_time = time.time()

# --------------------------------
# FUNCTIONS
# --------------------------------

def get_data_for_namespace(page, page_id, page_title, xlmns_string, ns, bot_list): 
    '''
    Extracts data from a specific namespace in an XML Wikipedia dump page object.
    
    :param page: XML Wikipedia dump page object to run function on
    :param page_id: XML Wikipedia dump page object's ID
    :param page_title: Title of the page
    :param xlmns_string: XLMS property of XML file as string
    :param ns: Namespace of the page
    :param bot_list: List of bot IDs
    :return: Returns a formatted dataframe of the page data required.
    '''
    data = []
    df = pd.DataFrame()
    namespaces = ['1', '3', '5', '7', '9', '11', '13', '101', '829']
    if ns in namespaces:
        for revision in page.findall(xlmns_string + 'revision'): # cycles through each revision
            rev_id = revision.find(xlmns_string + 'id').text
            timestamp = revision.find(xlmns_string + 'timestamp').text
            text = revision.find(xlmns_string + 'text').text 
            for contributor in revision.findall(xlmns_string + 'contributor'): # cycles through each contributor of the revision
                if contributor.find(xlmns_string + 'username') is not None:
                    user_id = contributor.find(xlmns_string + 'id').text
                    if user_id in bot_list:
                        continue                
                    else:
                        username = contributor.find(xlmns_string + 'username').text
                        df_temp = pd.DataFrame({'page_title': [page_title], 'ns': [ns], 'page_id': [page_id],
                                        'rev_id':[rev_id], 'timestamp':[timestamp], 'username':[username],
                                        'user_id':[user_id], 'subject_title':None, 'text':[text]})   
                        data.append(df_temp)
                        
                        del df_temp, user_id, username                               
                else:
                    continue

        del revision
            
        if len(data)==0:
            return df       
                        
        df = pd.concat(data, ignore_index=True) 
        
        del data
        
        return df

def processing_page_instance(elem, xlmns, bot_list):
    '''
    Processes a single page instance in parallel.
    
    :param elem: XML element representing a page instance
    :param xlmns: XLMS property of XML file as string
    :param bot_list: List of bot IDs
    :return: Returns the formatted dataframe for the page instance.
    '''
    ns = elem.find(xlmns + 'ns').text
    namespaces = ['1', '3', '5', '7', '9', '11', '13', '101', '829']
    if ns in namespaces:
        p_title = elem.find(xlmns + 'title').text
        page_id = elem.find(xlmns + 'id').text

        df_data_on_iter = get_data_for_namespace(page=elem, page_id=page_id, page_title=p_title, xlmns_string=xlmns, ns=ns, bot_list=bot_list)
        print(f"Page {page_id} completed with {psutil.virtual_memory().available / (1024 ** 2)} available RAM, current CPU: {psutil.cpu_percent()}%.")
        
        elem.clear()
        
        del page_id, p_title
        
        return df_data_on_iter
    
# --------------------------------
# MAIN PROCESS
# --------------------------------
        
# Replace the path to your local XMl file path
main_dir = r'C:\\Users\\Ritus\\OneDrive\\Dokumentumok\\7.félév\\komplex\\python'
#C:\Users\Ritus\OneDrive\Dokumentumok\7.félév\komplex\python\enwiki-20231001-pages-meta-history9.xml
file = r'C:\\Users\\Ritus\\OneDrive\\Dokumentumok\\7.félév\\komplex\\python\\enwiki-20231001-pages-meta-history9.xml'


if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    # XLMNS string in the XML file stored as a tring for better readability of parameters
    xlmns = '{http://www.mediawiki.org/xml/export-0.10/}'
    
    bot = r'C:\\Users\\Ritus\\OneDrive\\Dokumentumok\\7.félév\\komplex\\enwiki\\bots_en_all.csv'
    df_bot = pd.read_csv(bot, delimiter=';')
    
    # Creates list of bots, completes sufficient type modifications
    bot_list = df_bot['userid'].values.tolist()
    bot_list = [int(element) for element in bot_list]
    bot_list = [str(element) for element in bot_list]
    
    fileread_time = time.time()

    xmlstartread_time = time.time()
    context = ET.iterparse(file, events=('end',))
    xmlendread_time = time.time()

    # Dataframe used for output
    df_user_talk = pd.DataFrame(columns=['page_title', 'ns', 'page_id',
                                        'rev_id', 'timestamp',  'username',
                                        'user_id', 'subject_title', 'text'])

    parallel_start_time = time.time()
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(processing_page_instance, elem[1], xlmns, bot_list) for elem in context if elem[1].tag == xlmns + 'page'] 
        for future in futures:
            df_data_on_iter = future.result()
            if df_data_on_iter is not None:
                df_user_talk = pd.concat([df_user_talk, df_data_on_iter])
    parallel_end_time = time.time()

    #Print data to csv
    df_user_talk.to_csv(main_dir + '\\enwiki_huge.csv', encoding='utf-8-sig')

    #Runtime diagnosis
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Run diagnostics:")
    print(f"File and botlist read in {fileread_time - start_time} s.")
    print(f"Iterparse complete in {xmlendread_time - xmlstartread_time} s.")
    print(f"Parallel XML manipulation done in {parallel_end_time - parallel_start_time} s.")
    print(f"Process completed in {elapsed_time} s.")
