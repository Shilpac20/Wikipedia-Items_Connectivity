import csv
import pandas as pd
from fuzzywuzzy import process,fuzz
from _datetime import  datetime as dt
#print(dt.now())
data_file_article=pd.DataFrame(pd.read_csv('article-ids.csv'))
data_file=open('unfinshed_finished_mapping.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
tsv_file_unfinished=f"Required Data/paths_unfinished.tsv"
header=['article_in_unfinished','nearest_mapping_in_finished']
csv_writer.writerow([header[0],header[1]])

def fuzz_score(str1,dataframe1):
    return process.extract(str1, dataframe1, scorer=fuzz.token_sort_ratio,limit=1)[0][0]

dict_fuzz={}

with open(tsv_file_unfinished, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        try:
            if '#' in row[0]:
                continue
            else:
                source=row[3].split(';')[0]
                dest=row[4]

                if source not in dict_fuzz:
                    source_temp = fuzz_score(source, data_file_article['Article_Name'])
                    dict_fuzz[source]=source_temp
                    csv_writer.writerow([source,str(dict_fuzz[source])])

                if dest not in dict_fuzz:
                    dest_temp = fuzz_score(dest, data_file_article['Article_Name'])
                    dict_fuzz[dest]=dest_temp
                    csv_writer.writerow([dest, str(dict_fuzz[dest])])




        except:
            continue

data_file.close()
#print(dt.now())
