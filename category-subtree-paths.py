import csv
import pandas as pd
from _datetime import datetime as dt
from collections import defaultdict
import networkx as nx
#print(dt.now())
data_file_article=pd.DataFrame(pd.read_csv('article-ids.csv'))
edges_file=pd.DataFrame(pd.read_csv('edges.csv'))
article_list=[]
article_list_name=[]
dict_article={}
list_of_list=[]
for i in range(0,len(data_file_article)):
    article_list.append(data_file_article.loc[i]['Article_ID'])
    article_list_name.append(data_file_article.loc[i]['Article_Name'])
DG = nx.DiGraph()
for i in range(len(edges_file)):
    list1=[]
    source = edges_file.loc[i][0]
    dest = edges_file.loc[i][1]
    DG.add_edge(source,dest)
    list_of_list.append((source,dest))


#DG.add_weighted_edges_from(list_of_list)
#short_path = nx.shortest_path(DG)

categories=pd.DataFrame(pd.read_csv('category-ids.csv'))
finished_path_no_backedge=pd.DataFrame(pd.read_csv('own_ref.csv'))
data_file=open('category-subtree-paths.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['Category_ID','Number_of_human_paths_traversed','Number_of_times_traversed_in_human_path','Number_of_shortest_paths_traversed','Number_of_times_traversed_in_shortest_path']
csv_writer.writerow([header[0],header[1],header[2],header[3],header[4]])
tsv_file=f"Required Data/categories.tsv"
dict_article_category={}
with open(tsv_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        list_category=[]
        try:
            if '#' in row[0]:
                continue
            else:
                if row[0] not in dict_article_category:
                        dict_article_category[row[0]]=[row[1]]
                else:
                    dict_article_category[row[0]].append(row[1])
        except:
            continue

#print(dict_article_category)
category_dict={}
category_path_final={}
category_dict_shortest={}
category_path_final_shortest={}
for i in finished_path_no_backedge['Interpreted_path']:
    if ';' not in i:
        continue
    else:
        category_path = {}
        category_path_shortest={}
        path_temp=i.split(';')
        source=path_temp[0]
        dest=path_temp[-1]

        source_index=article_list[article_list_name.index(source)]
        dest_index=article_list[article_list_name.index(dest)]
        shortest_path=nx.shortest_path(DG,source_index,dest_index)#short_path[source_index][dest_index]#BFS_SP(graph,source_index,dest_index)
        list_sht_path=[]
        for article in shortest_path:
            article_index=article_list.index(article)
            article_name=article_list_name[article_index]
            list_sht_path.append(article_name)
        for j in list_sht_path:
            try:
                if j not in dict_article_category:
                    dict_article_category[j] = ['subject']
                list_path_temp=dict_article_category[j]
                #print(list_path)
                #need to consider paths having the category as well
                list_path=[]
                for item in list_path_temp:
                    new_str = item.split('.')
                    temp=''
                    for item_sub in new_str:
                        if temp!='':
                            temp=temp+'.'+item_sub
                        else:
                            temp=item_sub
                        if temp not in list_path:
                            list_path.append(temp)

                #print(list_path)
                for k in list_path:
                    if k in category_dict_shortest:
                        category_dict_shortest[k]+=1
                    else:
                        category_dict_shortest[k]=1
                    if k not in category_path_shortest:
                        category_path_shortest[k]=1
            except:
                continue

        for j in path_temp:
            try:
                if j not in dict_article_category:
                    dict_article_category[j]=['subject']
                list_path_temp=dict_article_category[j]
                #print(list_path)
                #need to consider paths having the category as well
                list_path = []
                for item in list_path_temp:
                    new_str = item.split('.')
                    temp = ''
                    for item_sub in new_str:
                        if temp != '':
                            temp = temp + '.' + item_sub
                        else:
                            temp = item_sub
                        if temp not in list_path:
                            list_path.append(temp)

                for k in list_path:
                    if k in category_dict:
                        category_dict[k]+=1
                    else:
                        category_dict[k]=1
                    if k not in category_path:
                        category_path[k]=1
            except:
                continue
        temp=category_path.copy()
        #print(temp)
        temp_shortest=category_path_shortest.copy()
        for item in temp:
            if item in category_path_final:
                category_path_final[item]+=temp[item]
            else:
                category_path_final[item]=temp[item]
        for item in temp_shortest:
            if item in category_path_final_shortest:
                    category_path_final_shortest[item] += temp_shortest[item]
            else:
                    category_path_final_shortest[item] = temp_shortest[item]
#print(category_dict)
for i in range(len(categories)):
    category_id=categories.iloc[i]['Category_ID']
    category_name=categories.iloc[i]['Category_Name']
    category_count=0
    path_count=0
    if category_name in category_dict:
        category_count=category_dict[category_name]
        path_count=category_path_final[category_name]
        category_count_shrt=category_dict_shortest[category_name]
        path_count_shrt=category_path_final_shortest[category_name]
        csv_writer.writerow([category_id,path_count,category_count,path_count_shrt,category_count_shrt])
    else:
        csv_writer.writerow([category_id,path_count, category_count,  path_count, category_count])

data_file.close()
#print(dt.now())





