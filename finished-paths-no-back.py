import csv
import pandas as pd
from _datetime import datetime as dt
#print(dt.now())
tsv_file=f"Required Data/paths_finished.tsv"
dict_paths={}
dict_shortest_path={}
shortestpath_file=f"Required Data/shortest-path-distance-matrix.txt"
#file1 = open("myfile.txt","w")
articles=pd.DataFrame(pd.read_csv('article-ids.csv'))
articles_idlist=articles['Article_ID'].values.tolist()
data_file = open('finished-paths-no-back.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['Human_Path_Length','Shortest_Path_Length','Ratio']
csv_writer.writerow([header[0],header[1],header[2]])
data_file1 = open('own_ref.csv', 'w+',newline='',encoding='utf-8')
csv_writer1 = csv.writer(data_file1)
header=['Actual_path','Interpreted_path','Human_Path_Length','Shortest_Path_Length','Ratio']
csv_writer1.writerow([header[0],header[1],header[2],header[3],header[4]])
def remove_backspace(path_str):
    temp=path_str.split(';')
    new_str=[]
    ret_str=''
    for i in temp:
        if i=='<':
            new_str.pop()
            new_str.pop()
        else:
            new_str.append(i)
            new_str.append(';')
    len_new_str=len(new_str)
    if new_str[len_new_str-1]==';':
        new_str.pop()
    for i in new_str:
        ret_str+=i
    #print(ret_str)
    return ret_str


with open(shortestpath_file) as sf:
    i=0
    for line in sf:
        #dict_shortest_path[articles_idlist[i]]=[]
        if '#' in line[0]:
            #print('Hi')
            continue
        elif line=='\n':
            continue
        else:
            sentence=line
            for j in range(len(sentence)-1):
                if sentence[j]=='_':
                    if articles_idlist[i] in dict_shortest_path:
                        dict_shortest_path[articles_idlist[i]].append('99999')
                    else:
                        dict_shortest_path[articles_idlist[i]]=['99999']

                else:
                    if articles_idlist[i] in dict_shortest_path:
                        dict_shortest_path[articles_idlist[i]].append(sentence[j])
                    else:
                        dict_shortest_path[articles_idlist[i]]=[sentence[j]]
                    #print(i,j)
                    #dict_shortest_path[articles_idlist[i]].append(sentence[j])
            i+=1

#print(dict_shortest_path['A0001'][13])
with open(tsv_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        #print(row)
        try:
            if '#' in row[0] or row=='\n':
               # print(row)
                continue
            else:
                path_temp=row[3]
                #print(row[1]," ",row[2]," ",row[3])
                #print(path_temp)

                if '<;' in path_temp:
                    path_temp1 = remove_backspace(path_temp)
                    # path_temp = path_temp.replace('<;', '')
                    path_length = path_temp1.count(';') #+ 1
                    shortest_path = path_temp1.split(';')
                    article_id_source = articles.loc[articles['Article_Name'] == shortest_path[0], 'Article_ID'].iloc[0]
                    # print(path_temp," ",path_length," ",article_id_source)
                    shortest_path_length = 0
                    article_id_dest = articles.loc[articles['Article_Name'] == shortest_path[-1], 'Article_ID'].iloc[0]
                    article_id_index = articles_idlist.index(article_id_dest)
                    shortest_path_length += int(dict_shortest_path[article_id_source][article_id_index])
                    if shortest_path_length == 99999:
                        continue
                    else:
                        csv_writer.writerow(
                            [ path_length, shortest_path_length,
                             round(path_length / shortest_path_length, 2)])
                        csv_writer1.writerow([path_temp, path_temp1,path_length, shortest_path_length,
                             round(path_length / shortest_path_length, 2)])
                    continue
                elif ';' not in path_temp:
                    continue
                else:
                #path_temp = path_temp.replace('<;', '')
                    path_length = path_temp.count(';') #+ 1
                    shortest_path=path_temp.split(';')
                    article_id_source = articles.loc[articles['Article_Name'] == shortest_path[0], 'Article_ID'].iloc[0]
                    shortest_path_length=0
                    article_id_dest=articles.loc[articles['Article_Name'] == shortest_path[-1], 'Article_ID'].iloc[0]
                    article_id_index = articles_idlist.index(article_id_dest)
                    shortest_path_length += int(dict_shortest_path[article_id_source][article_id_index])
                    if shortest_path_length==99999:
                        continue
                    else:
                        csv_writer.writerow(
                        [ path_length, shortest_path_length, round(path_length / shortest_path_length, 2)])
                        csv_writer1.writerow([path_temp, path_temp, path_length, shortest_path_length,
                                              round(path_length / shortest_path_length, 2)])



        except:
            continue
data_file.close()


