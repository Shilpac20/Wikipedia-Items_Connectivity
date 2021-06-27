import csv
import pandas as pd
tsv_file=f"Required Data/articles.tsv"
data_file = open('article-ids.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['Article_Name','Article_ID']
csv_writer.writerow([header[0],header[1]])
counter='A000'
count=1
with open(tsv_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        try:
            if '#' in row[0]:
                continue
            else:
                if count>=10 and count<100:
                    counter='A00'
                elif count>=100 and count<1000:
                    counter='A0'
                elif count>=1000:
                    counter='A'
                csv_writer.writerow([row[0],counter+str(count)])
                count+=1

        except:
            continue
data_file.close()
article_file=pd.DataFrame(pd.read_csv("article-ids.csv"))
group_data = article_file.sort_values(['Article_Name'], ascending=[True])
group_data.to_csv('article-ids.csv',index=False)
