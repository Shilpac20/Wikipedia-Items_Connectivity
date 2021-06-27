import pandas as pd
import csv
from _datetime import datetime as dt
#print(dt.now())
unfinished_finished_map=pd.DataFrame(pd.read_csv("unfinshed_finished_mapping.csv"))
articles_with_no_mapping=['test','c++','the','usa','black_ops_2','fats','rat',
                        'western_australia','the_rock','great','mustard','kashmir','netbook',
                          'christmas','sportacus','macedonia'
                           ]
category=pd.DataFrame(pd.read_csv('category-ids.csv'))
article_category=pd.DataFrame(pd.read_csv('article-categories.csv'))
data_file_article=pd.DataFrame(pd.read_csv('article-ids.csv'))
tsv_file_unfinished=f"Required Data/paths_unfinished.tsv"
tsv_file_finished=f"Required Data/paths_finished.tsv"

data_file=open('category-pairs.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['From_Category','To_Category','Percentage_of_finished_paths','Percentage_of_unfinished_paths']
csv_writer.writerow([header[0],header[1],header[2],header[3]])
article_list=[]
article_list_name=[]
for i in range(0,len(data_file_article)):
    article_list.append(data_file_article.loc[i]['Article_ID'])
    article_list_name.append(data_file_article.loc[i]['Article_Name'])
dict_unfinished_category_pairs={}
dict_article_category={}
for i in range(len(article_category)):
    article_id=article_category.loc[i]['Article_ID']
    category_list=article_category.loc[i]['Category_ID']
    for item in category_list.split(','):
        category_id_name = category.loc[category['Category_ID'] == item, 'Category_Name'].iloc[0]
        if article_id in dict_article_category:
            dict_article_category[article_id].append(category_id_name)
        else:
            dict_article_category[article_id] = [category_id_name]


#print(dict_article_category)
for i in range(0,len(unfinished_finished_map)):
    unfinished_article=unfinished_finished_map.loc[i]['article_in_unfinished']
    mapped_article=unfinished_finished_map.loc[i]['nearest_mapping_in_finished']
    unfinished_article_category=[]
    if str(unfinished_article).lower() in articles_with_no_mapping:
        continue
    else:
        unfinished_article_id=article_list[article_list_name.index(mapped_article)]
        #print(unfinished_article_id," ",mapped_article)
        for i in dict_article_category[unfinished_article_id]:
            category_str=i.split('.')
            if unfinished_article_id not in dict_unfinished_category_pairs:
                dict_unfinished_category_pairs[unfinished_article_id]=[]
            new_str=''
            for item in category_str:
                if new_str!='':
                    new_str=new_str+'.'+item
                else:
                    new_str=item
                dict_unfinished_category_pairs[unfinished_article_id].append(new_str)
#print(dict_unfinished_category_pairs)
dict_unfinished_path={}
with open(tsv_file_unfinished, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        try:
            if '#' in row[0]:
                continue
            else:
                source_temp=row[3].split(';')[0]
                dest_temp=row[4]
                if str(source_temp).lower() in articles_with_no_mapping:
                    unfinishedSource_category_list=['subject']
                else:
                    mapped_article=unfinished_finished_map.loc[unfinished_finished_map['article_in_unfinished']==source_temp,'nearest_mapping_in_finished'].iloc[0]
                    unfinishedSource_article_id = article_list[article_list_name.index(mapped_article)]
                    unfinishedSource_category_list=dict_unfinished_category_pairs[unfinishedSource_article_id]

                if str(dest_temp).lower() in articles_with_no_mapping:
                    unfinishedDest_category_list=['subject']
                else:
                    mapped_article = unfinished_finished_map.loc[unfinished_finished_map['article_in_unfinished'] == dest_temp, 'nearest_mapping_in_finished'].iloc[0]
                    unfinishedDest_article_id = article_list[article_list_name.index(mapped_article)]
                    unfinishedDest_category_list = dict_unfinished_category_pairs[unfinishedDest_article_id]
                list_of_pairs_visited = []
                for sourceitem in unfinishedSource_category_list:
                    for destitem in unfinishedDest_category_list:
                        if (sourceitem, destitem) not in list_of_pairs_visited:
                            list_of_pairs_visited.append((sourceitem, destitem))
                            if (sourceitem, destitem) in dict_unfinished_path:
                                dict_unfinished_path[(sourceitem, destitem)] += 1
                            else:
                                dict_unfinished_path[(sourceitem, destitem)] = 1

        except:
            continue

#print(dict_unfinished_path)
dict_finished_path={}
with open(tsv_file_finished, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        try:
            if '#' in row[0]:
                continue
            else:
                source_temp=row[3].split(';')[0]
                dest_temp=row[3].split(';')[-1]

                finishedSource_article_id = article_list[article_list_name.index(source_temp)]
                finishedSource_category_list=[]
                for item in dict_article_category[finishedSource_article_id]:
                        category_str=item.split('.')
                        new_str=''
                        for element in category_str:
                            if new_str!='':
                                new_str=new_str+'.'+element
                            else:
                                new_str=element
                            finishedSource_category_list.append(new_str)

                finishedDest_article_id = article_list[article_list_name.index(dest_temp)]
                finishedDest_category_list = []
                for item in dict_article_category[finishedDest_article_id]:
                    category_str = item.split('.')
                    new_str = ''
                    for element in category_str:
                        if new_str != '':
                            new_str = new_str + '.' + element
                        else:
                            new_str = element
                        finishedDest_category_list.append(new_str)

                list_of_pairs_visited = []
                for sourceitem in finishedSource_category_list:
                    for destitem in finishedDest_category_list:
                        if (sourceitem, destitem) not in list_of_pairs_visited:
                            list_of_pairs_visited.append((sourceitem, destitem))
                            if (sourceitem, destitem) in dict_finished_path:
                                dict_finished_path[(sourceitem, destitem)] += 1
                            else:
                                dict_finished_path[(sourceitem, destitem)] = 1
        except:
            continue
dict_final={}

for item in dict_unfinished_path.keys():
    #print(item)
    (source,dest)=item
    source_id=category.loc[category['Category_Name']==source,'Category_ID'].iloc[0]
    dest_id=category.loc[category['Category_Name']==dest,'Category_ID'].iloc[0]
    count=dict_unfinished_path[item]
    if (source_id,dest_id) not in dict_final:
        dict_final[(source_id,dest_id)]={'finished':0,'unfinished':count}
for item in dict_finished_path.keys():
    (source, dest) = item
    source_id = category.loc[category['Category_Name'] == source, 'Category_ID'].iloc[0]
    dest_id = category.loc[category['Category_Name'] == dest, 'Category_ID'].iloc[0]
    count = dict_finished_path[item]
    if (source_id, dest_id) not in dict_final:
       # print(source_id,dest_id)
        dict_final[(source_id, dest_id)] = {'finished': count, 'unfinished': 0}
    else:
        dict_final[(source_id,dest_id)]['finished']=count

for item in dict_final.keys():
    (source,dest)=item
    finished_path_count=dict_final[item]['finished']
    unfinished_path_count=dict_final[item]['unfinished']
    totalpath_count=finished_path_count+unfinished_path_count
    csv_writer.writerow([source,dest,round((finished_path_count/totalpath_count)*100,2),round((unfinished_path_count/totalpath_count)*100,2)])
data_file.close()
category_pair=pd.DataFrame(pd.read_csv("category-pairs.csv"))
group_data = category_pair.sort_values(['From_Category','To_Category'], ascending=[True,True])
group_data.to_csv('category-pairs.csv',index=False)
#print(dt.now())
