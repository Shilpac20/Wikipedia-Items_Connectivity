I have used Python 3.6.1 and the following packages-- csv, pandas,sys,networkx,fuzzywuzzy,python-Levenshtein,numpy
To install networkx use the command sudo pip3 install networkx.
To install fuzzywuzzy and Levenshtein use the following commands:
sudo apt-get install -y python3-fuzzywuzzy
sudo apt-get install -y python3-levenshtein

Please do not delete any of the csv files created in any of the questions as I have used those csv files to solve some of the subsequent questions.

For making the scripts executable please run the command chmod u+x scriptname.sh.

1. For question 1, please run the file article-ids.sh file . Inorder to run please execute the command chmod u+x article-ids.sh to make it executable and to run the script type ./article-ids.sh in the terminal. This will create the article-ids.csv file containing the article id and its corresponding name.The file is sorted according to the article names.

2. For question 2 , please run the file category-ids.sh file . Inorder to run please execute the command chmod u+x category-ids.sh to make it executable and to run the script type ./category-ids.sh in the terminal. This will create the category-ids.csv file containing the category id and its corresponding name.Here all the categories are sorted levelwise alphabetically(i.e. Breadth First Ordering for the categories has been done). The file is sorted according to category names.

3.For question 3, please run the file article-categories.sh file . Inorder to run please execute the command chmod u+x article-categories.sh to make it executable and to run the script type ./article-categories.sh in the terminal. This will create the article-categories.csv file containing the article id and its corresponding category ids(some articles have multiple categories) {Here for categories only the lowest level of category of category tree is considered i.e.if an article has catergory as subject.a.b then in the csv its category is mentioned as the category id of subject.a.b (subject and subject.a are not included in the category list of the article)} 
In articles.tsv there were 6 articles namely Directdebit,Donation,Friend_Directdebit,Pikachu,Sponsorship_Directdebit,Wowpurchase which do not have any categories so, these articles have been assigned category id C0001 which is category 'subject'.


4.For Question 4,please run the file edges.sh file . Inorder to run please execute the command chmod u+x edges.sh to make it executable and to run the script type ./edges.sh in the terminal.This will create a file named edges.csv which contains directed edges between articles.


5.For Question 5,please run the file graph-components.sh file . Inorder to run please execute the command chmod u+x graph-components.sh to make it executable and to run the script type ./graph-components.sh in the terminal. This will create graph-components.csv which contains components, number of nodes, its nodes(i.e. article ids), number of edges, diameter of the component. For the components I have considered the graph as undirected graph.


6.For Question 6,please run the file paths_finished.sh file . Inorder to run please execute the command chmod u+x paths_finished.sh to make it executable and to run the script type ./paths_finished.sh in the terminal. This will create two files namely finished-paths-no-back.csv and finished-paths-back.csv each file containing the actual path(in paths_finished.tsv), the iterpreted path,human path length, shortest path length,ratio of human path to shortest path. The ratio of human path to shortest path has been rounded upto 2 decimal places.

For finished-paths-no-back.csv the actual path with back edge is interpreted as follows:
If the path is a;b;<;c where < is the backspace , then it is interpreted as a;c

For finished-paths-back.csv the actual path with back edge is interpreted as follows:
If the path is a;b;<;c where < is the backspace , then it is interpreted as a;b;a;c

7. For Question 7,please run the file percentage-paths.sh file . Inorder to run please execute the command chmod u+x percentage-paths.sh to make it executable and to run the script type ./percentage-paths.sh in the terminal.This will create two files namely percentage-paths-no-back.csv and percentage-paths-back.csv each file containing the percentage of human paths having same path length,path length difference 1,path length difference 2,path length difference 3,path length difference 4,path length difference 5,path length difference 6,path length difference 7,path length difference 8,path length difference 10,path length difference 11 or more with respect to the corresponding shortest path. The percentages has been rounded upto 2 decimal places.

8. For Question 8, please run the file category-paths.sh file . Inorder to run please execute the command chmod u+x category-paths.sh to make it executable and to run the script type ./category-paths.sh in the terminal.This will create a csv file named category-paths.csv which contains category_id, number of times a human path touched the category, Number of times this category was traversed in human path(counted multiple times if a category is visited multiple times in a path),number of times a shortest path touched the category, Number of times this category was traversed in shortest path.Here only the leaf categories have been considered.

9.For Question 9, please run the file category-subtree-paths.sh file . Inorder to run please execute the command chmod u+x category-subtree-paths.sh to make it executable and to run the script type ./category-subtree-paths.sh in the terminal.This will create a csv file named category-subtree-paths.csv which contains category_id, number of times a human path touched the category, Number of times this category was traversed in human path(counted multiple times if a category is visited multiple times in a path),number of times a shortest path touched the category, Number of times this category was traversed in shortest path.Here whenever a leaf category is touched all its parent categories also get updated.

10.For Question 10, please run the file category-pairs.sh file . Inorder to run please execute the command chmod u+x category-pairs.sh to make it executable and to run the script type ./category-pairs.sh in the terminal.This will create category-pairs.csv containing the source category,destination category,finished_path_percentage,unfinished_path_percentage. All the percentages are rounded of upto 2 decimal points. There are certain articles in paths_unfinished.tsv which are absent in paths_finished.tsv namely (test','c++','the','usa','rss','black_ops_2','fats','bogota','georgia','rat','charlottes_web','western_australia','the_rock','great','georgia','english','mustard','kashmir','netbook','podcast','christmas','sportacus','macedonia'
) and for all these articles i have given them a category of subject. I have used fuzzywuzzy for mapping articles of paths_unfinished.tsv to articles of paths_finished.tsv and the mapping is present in unfinshed_finished_mapping.csv. There were some spelling mistakes in articles like 'Long_peper','Adolph_Hitler' which the fuzzywuzzy code(written in temp.py file) has correctly mapped.
For the source destination category pair if the source article belongs to category subject.a and the destination article belongs to subject.b , then the source-destination category pairs will be as follows:
(subject,subject) ,(subject,subject.b), (subject.a,subject), (subject.a,subject.b)

11.For Question 11, please run the file category-ratios.sh file . Inorder to run please execute the command chmod u+x category-ratios.sh to make it executable and to run the script type ./category-ratios.sh in the terminal.This will create a csv file named category-ratios.csv which contains the source and destination category pairs visited in finished paths with no backegde and their human to shortest path length ratio. The ratio is rounded upto 2 decimal places.

12.For executing the entire assignment please execute the command chmod u+x assign2.sh and to run the script type ./assign2.sh. This will create all the csv files. It will take 11-12mins to run the entire assignment.


13. The report.tex is present in the folder named as Report and all the required files for its succesfull compilation is present there.




