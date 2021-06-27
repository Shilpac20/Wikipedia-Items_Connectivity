import csv
import pandas as pd
tsv_file=f"Required Data/paths_finished.tsv"
dict_paths={}
dict_shortest_path={}
shortestpath_file=f"Required Data/shortest-path-distance-matrix.txt"
#file1 = open("myfile.txt","w")
articles=pd.DataFrame(pd.read_csv('article-ids.csv'))
articles_idlist=articles['Article_ID'].values.tolist()
data_file = open('finished-paths-back.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['Human_Path_Length','Shortest_Path_Length','Ratio']
csv_writer.writerow([header[0],header[1],header[2]])
def remove_backspace(path_str):
    temp=path_str.split(';')
    new_str=[]
    ret_str=''
    for i in range(len(temp)):
        if temp[i]=='<':
            ele_before_backspace=temp[i-1]
            ind_temp = 1
            cur_index=i-1
            count_backspace=0
            #print('ele ', ele_before_backspace)
            while ele_before_backspace == '<':
                if (ele_before_backspace == '<'):
                    count_backspace += 1
                ele_before_backspace = temp[i - 1 - ind_temp]
                cur_index=i-ind_temp-1
                #print('ele ', ele_before_backspace,' cur index is ',cur_index)

                ind_temp += 1
            element_to_append = temp[cur_index-1-count_backspace]
            #print('element to append',element_to_append)
            new_str.append(element_to_append)
            new_str.append(';')
        else:
            new_str.append(temp[i])
            new_str.append(';')
    len_new_str = len(new_str)
    if new_str[len_new_str - 1] == ';':
        new_str.pop()
    #print(new_str)
    for i in new_str:
        ret_str += i
        # print(ret_str)
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
                if '<;' not in path_temp:
                    path_length = path_temp.count(';') #+ 1
                    shortest_path = path_temp.split(';')
                    article_id_source = articles.loc[articles['Article_Name'] == shortest_path[0], 'Article_ID'].iloc[0]
                    shortest_path_length = 0
                    article_id_dest = articles.loc[articles['Article_Name'] == shortest_path[-1], 'Article_ID'].iloc[0]
                    article_id_index = articles_idlist.index(article_id_dest)
                    shortest_path_length += int(dict_shortest_path[article_id_source][article_id_index])
                    if shortest_path_length == 99999:
                        '''
                        shortest_path_length_str='NA'
                        csv_writer.writerow(
                            [path_temp, path_length, shortest_path_length_str,
                             'NA'])
                        '''
                        continue
                    else:
                        csv_writer.writerow(
                            [path_length, shortest_path_length,
                             round(path_length / shortest_path_length, 2)])
                else:
                    #print("Original path is : ",path_temp)
                    path_temp1=remove_backspace(path_temp)
                    #print(path_temp)
                    #path_temp = path_temp.replace('<;', '')
                    path_length = path_temp1.count(';') #+ 1
                    shortest_path=path_temp1.split(';')
                    article_id_source = articles.loc[articles['Article_Name'] == shortest_path[0], 'Article_ID'].iloc[0]
                    #print(path_temp," ",path_length," ",article_id_source)
                    shortest_path_length=0
                    article_id_dest = articles.loc[articles['Article_Name'] == shortest_path[-1], 'Article_ID'].iloc[0]
                    article_id_index = articles_idlist.index(article_id_dest)
                    shortest_path_length += int(dict_shortest_path[article_id_source][article_id_index])
                    if shortest_path_length == 99999:
                        continue
                    else:
                        csv_writer.writerow(
                            [path_length, shortest_path_length,
                             round(path_length / shortest_path_length, 2)])
                    
        except:
            continue
data_file.close()

