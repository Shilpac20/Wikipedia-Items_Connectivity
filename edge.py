import pandas as pd
import csv
articles=pd.DataFrame(pd.read_csv('article-ids.csv'))
articles_idlist=articles['Article_ID'].values.tolist()
#print(articles_idlist," ",len(articles_idlist))
shortestpath_file=f"Required Data/shortest-path-distance-matrix.txt"
data_file = open('edges.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['From_ArticleID','To_ArticleID']
csv_writer.writerow([header[0],header[1]])
with open(shortestpath_file) as sf:
    i=0
    for line in sf:
        if '#' in line[0]:
            #print('Hi')
            continue
        elif line=='\n':
            continue
        else:
            sentence=line
            for j in range(len(sentence)-1):
                if sentence[j]!='1':
                    continue
                else:
                    #print(i,j)
                    csv_writer.writerow([articles_idlist[i],articles_idlist[j]])
            i+=1


data_file.close()
#print(count," ",hash)


