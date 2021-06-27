import networkx as nx
import csv
from networkx.algorithms.components.connected import connected_components
import networkx.algorithms.distance_measures as ndt
from _datetime import datetime as dt
import pandas as pd
#G=nx.Graph()

#print(dt.now())
edges_file=pd.DataFrame(pd.read_csv('edges.csv'))
data_file_article=pd.DataFrame(pd.read_csv('article-ids.csv'))
article_list=[]
dict_article={}

for i in range(0,len(data_file_article)):
    article_list.append(data_file_article.loc[i]['Article_ID'])
    dict_article[data_file_article.loc[i]['Article_ID']]={'index':i}


shortestpath_file=f"Required Data/shortest-path-distance-matrix.txt"
dict_shortest_path={}
data_file=open('graph-components.csv', 'w+',newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
header=['Nodes','Edges','Diameter']
csv_writer.writerow([header[0],header[1],header[2]])
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
                    if article_list[i] in dict_shortest_path:
                        dict_shortest_path[article_list[i]].append('99999')
                    else:
                        dict_shortest_path[article_list[i]]=['99999']

                else:
                    if article_list[i] in dict_shortest_path:
                        dict_shortest_path[article_list[i]].append(sentence[j])
                    else:
                        dict_shortest_path[article_list[i]]=[sentence[j]]
                    #print(i,j)
                    #dict_shortest_path[articles_idlist[i]].append(sentence[j])
            i+=1

list_of_list=[]
def to_graph(l):
    G = nx.Graph()
    for part in l:
        G.add_nodes_from(part)
        G.add_edges_from(to_edges(part))
    return G

def to_edges(l):
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current
for i in range(len(edges_file)):
    list1=[]
    source = edges_file.loc[i][0]
    dest = edges_file.loc[i][1]
    list1.append(source)
    list1.append(dest)
    #G.add_edge(source,dest)
    #G.add_edge(dest,source)
    list_of_list.append(list1)
    #list1 = []
    #list1.append(dest)
    #list1.append(source)
    #list_of_list.append(list1)
#print(G.nodes())
#print(G.edges())
#print(len(list_of_list))
dict_list={}
G = to_graph(list_of_list)
component=1
list_components=[]
diameter_edge_dict={}
for c in (connected_components(G)):
    dict_list[component]=list(sorted(c))
    component+=1
    #print(sorted(c))
    list_components.extend(dict_list[component-1])
    #list_components.append(i for i in dict_list[component-1])
    sub_components = (G.subgraph(c).copy())
    egde_count=len(list(sub_components.edges))
    diameter_edge_dict[egde_count]=nx.diameter(sub_components)

list_components.sort()

#print(list_components)
isolated_articles=list(set(article_list).difference(set(list_components)))
#print(isolated_articles)
for i in isolated_articles:
    dict_list[component]=[i]
    component+=1
#print(type(dict_list[1]))
#edge_list=list_of_list
#edge_list=list(nx.edges(G))
#print(len(list(nx.edges(G))))
#dict_final={}
#print(dict_article)

for item in dict_list.keys():
    edge_count=0
    diameter=0
    node_count=len(dict_list[item])
    if node_count>1:
        subgraph_component=G.subgraph(dict_list[item])
        edge_count=len(list(subgraph_component.edges))
        diameter=diameter_edge_dict[edge_count]
        '''
        for (s,e) in edge_list:
            if (s in dict_list[item]) &(e in dict_list[item]) &(s!=e):
                #print(G.adj[s])
                #print((s,e))
                edge_count+=1
                #if s in dict_shortest_path:
        v = dict_list[item]
        pairs = [(v[i], v[j]) for i in range(len(v) - 1) for j in range(i + 1, len(v))]
        for (s, e) in pairs:
            if s in dict_shortest_path:
                dest_index=dict_article[e]['index']
                source_index = dict_article[s]['index']
                #dest_index = article_list.index(e)
                #source_index = article_list.index(s)
                #print(source_index," ",dest_index)
                distance = dict_shortest_path[s][dest_index]
                distance1 = dict_shortest_path[e][source_index]
                if distance != '99999':
                    diameter = max(diameter, int(distance))
                if distance1 != '99999':
                    diameter = max(diameter, int(distance1))
        '''
    csv_writer.writerow([node_count,edge_count,diameter])
#print(dict_final)
data_file.close()
graph_component=pd.DataFrame(pd.read_csv("graph-components.csv"))
group_data = graph_component.sort_values(['Nodes'], ascending=[True])
group_data.to_csv('graph-components.csv',index=False)
#print(dt.now())
