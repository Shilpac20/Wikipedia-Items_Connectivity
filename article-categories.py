import csv
import pandas as pd
catagories=pd.DataFrame(pd.read_csv('category-ids.csv'))
articles=pd.DataFrame(pd.read_csv('article-ids.csv'))
data_file = open('article-categories.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['Article_ID','Category_ID']
csv_writer.writerow([header[0],header[1]])
tsv_file=f"Required Data/categories.tsv"
dict_article_category={}
article_list=[]
for i in range(0,len(articles)):
    article_list.append(articles.loc[i][1])


with open(tsv_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        list_category=[]
        try:
            if '#' in row[0]:
                continue
            else:
                #print(row[0]," ")
                #print('hi',articles.loc[articles[1]==row[0],0].iloc[0])
                #district_id.loc[district_id['districtname'] == neighbor, 'districtid'].iloc[0]
                article_id=articles.loc[articles['Article_Name']==row[0],'Article_ID'].iloc[0]
                #print(article_id)
                if article_id not in dict_article_category:
                    dict_article_category[article_id]=[]
                #list_category_temp = list(row[1].split('.'))
                #list_category = []
                list_category=[row[1]]
                #print(list_category)
                if catagories.loc[catagories['Category_Name'] == list_category[0], 'Category_ID'].iloc[0] not in dict_article_category[article_id]:
                    dict_article_category[article_id].append(
                        catagories.loc[catagories['Category_Name'] == list_category[0], 'Category_ID'].iloc[0])

        except:
            continue
#print(catagories.loc[catagories['Category_Name']=='subject','Category_ID'].iloc[0])
for item in article_list:
    if item not in dict_article_category:
        dict_article_category[item]=[catagories.loc[catagories['Category_Name']=='subject','Category_ID'].iloc[0]]
for article_id in dict_article_category.keys():
    list_category1=dict_article_category[article_id]
    list_category1.sort()
    #print(list_category1)
    category=(','.join(list_category1))
    csv_writer.writerow([article_id,category])
data_file.close()

article_category=pd.DataFrame(pd.read_csv('article-categories.csv'))
#article_category.columns = ['article_id','category_list']
group_data = article_category.sort_values(['Article_ID'], ascending=[True])
group_data.to_csv('article-categories.csv',index=False)