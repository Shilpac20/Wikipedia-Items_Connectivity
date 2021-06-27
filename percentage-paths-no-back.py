import csv
import pandas as pd
import math
path_no_backedge=pd.DataFrame(pd.read_csv('finished-paths-no-back.csv'))

data_file = open('percentage-paths-no-back.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['Equal_Length','Larger_by_1','Larger_by_2','Larger_by_3','Larger_by_4','Larger_by_5','Larger_by_6'
    ,'Larger_by_7','Larger_by_8','Larger_by_9','Larger_by_10','Larger_by_more_than_10']
csv_writer.writerow([header[0],header[1],header[2],header[3],header[4],header[5],header[6],header[7],header[8],header[9],header[10],header[11]])

total_count=0
count_same=0
count_remaining=[0,0,0,0,0,0,0,0,0,0,0]
#print(path_no_backedge.iloc[0]['human path length'])

for i in range(len(path_no_backedge)):
    if path_no_backedge.iloc[i]['Shortest_Path_Length']=='NA':
        continue
    diff=int(path_no_backedge.iloc[i]['Human_Path_Length'])-int(path_no_backedge.iloc[i]['Shortest_Path_Length'])
    #diff=int(path_no_backedge.iloc[i][1])-int(path_no_backedge.iloc[i][2])
    total_count+=1
    if diff==0:
        count_same+=1
    elif diff >=1 and diff <=10:
        count_remaining[diff-1]+=1
    else:
        count_remaining[10]+=1
csv_writer.writerow([round((count_same/total_count)*100,2),round((count_remaining[0]/total_count)*100,2),round((count_remaining[1]/total_count)*100,2),
                     round((count_remaining[2] / total_count) * 100, 2),round((count_remaining[3]/total_count)*100,2),round((count_remaining[4]/total_count)*100,2),
                     round((count_remaining[5]/total_count)*100,2),round((count_remaining[6]/total_count)*100,2),round((count_remaining[7]/total_count)*100,2),
                     round((count_remaining[8]/total_count)*100,2),round((count_remaining[9]/total_count)*100,2),round((count_remaining[10]/total_count)*100,2)
                     ])





