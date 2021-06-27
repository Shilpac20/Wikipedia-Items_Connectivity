import pandas as pd
import csv
import numpy as np
finished_no_back_edge=pd.DataFrame(pd.read_csv('own_ref.csv'))
article_list=[]
article_list_name=[]
data_file_article=pd.DataFrame(pd.read_csv('article-ids.csv'))
article_category=pd.DataFrame(pd.read_csv('article-categories.csv'))
category=pd.DataFrame(pd.read_csv('category-ids.csv'))
data_file=open('category-ratios.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['From_Category','To_Category','Ratio_of_human_to_shortest']
csv_writer.writerow([header[0],header[1],header[2]])
for i in range(0,len(data_file_article)):
    article_list.append(data_file_article.loc[i]['Article_ID'])
    article_list_name.append(data_file_article.loc[i]['Article_Name'])

dict_article_category={}
for i in range(len(article_category)):
    article_id=article_category.loc[i]['Article_ID']
    category_list = article_category.loc[i]['Category_ID']
    for item in category_list.split(','):
        category_id_name = category.loc[category['Category_ID'] == item, 'Category_Name'].iloc[0]
        if article_id in dict_article_category:
            dict_article_category[article_id].append(category_id_name)
        else:
            dict_article_category[article_id] = [category_id_name]
dict_category_pair={}
for i in range(len(finished_no_back_edge)):
    path_str=finished_no_back_edge.iloc[i]['Interpreted_path']
    if ';' not in path_str:
        continue
    else:

        path=path_str.split(';')
        source=path[0]
        dest=path[-1]
        source_id=article_list[article_list_name.index(source)]
        dest_id=article_list[article_list_name.index(dest)]
        path_length=finished_no_back_edge.iloc[i]['Human_Path_Length']
        path_length_shrt=finished_no_back_edge.iloc[i]['Shortest_Path_Length']
        source_category_list_temp=dict_article_category[source_id]
        dest_category_list_temp=dict_article_category[dest_id]
        source_category_list=[]
        dest_category_list=[]

        for item in source_category_list_temp:
            newstr=''
            category_str=item.split('.')
            #print(category_str)
            for category_sub in category_str:
                if newstr!='':
                    newstr=newstr+'.'+category_sub
                else:
                    newstr=category_sub
                source_category_list.append(newstr)
        for item in dest_category_list_temp:
            newstr=''
            category_str=item.split('.')
            for category_sub in category_str:
                if newstr!='':
                    newstr=newstr+'.'+category_sub
                else:
                    newstr=category_sub
                dest_category_list.append(newstr)
        list_of_pairs_visited = []
        for item_source in source_category_list:
            for item_dest in dest_category_list:
                if (item_source, item_dest) not in list_of_pairs_visited:
                    list_of_pairs_visited.append((item_source, item_dest))
                    if (item_source, item_dest) not in dict_category_pair:
                        dict_category_pair[(item_source, item_dest)] = {}
                        dict_category_pair[(item_source, item_dest)]['human_path'] = [path_length]
                        dict_category_pair[(item_source, item_dest)]['shortest_path'] = [path_length_shrt]
                    else:
                        dict_category_pair[(item_source, item_dest)]['human_path'].append(path_length)
                        dict_category_pair[(item_source, item_dest)]['shortest_path'].append(path_length_shrt)

for item in dict_category_pair.keys():
    (source,dest)=item
    source_id = category.loc[category['Category_Name'] == source, 'Category_ID'].iloc[0]
    dest_id = category.loc[category['Category_Name'] == dest, 'Category_ID'].iloc[0]
    path_length=np.mean(dict_category_pair[item]['human_path'])
    path_length_shrt=np.mean(dict_category_pair[item]['shortest_path'])
    ratio_human_shrt=round((path_length/path_length_shrt),2)
    csv_writer.writerow([source_id,dest_id,ratio_human_shrt])
data_file.close()
category_pair=pd.DataFrame(pd.read_csv("category-ratios.csv"))
group_data = category_pair.sort_values(['From_Category','To_Category'], ascending=[True,True])
group_data.to_csv('category-ratios.csv',index=False)
