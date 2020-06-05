import matplotlib.pyplot as plt
from mlxtend.plotting import scatterplotmatrix
import pandas as pd
from multiprocessing import Process
from collections import Counter

#scale x [min,max] to [a,b]
def scale(x,min_x,max_x,a,b):
    res = (((float(b)-float(a))*(float(x)-float(min_x)))/(float(max_x)-float(min_x)))+float(a)
    return res



df = pd.read_csv("IrisTextFiles/abrsm_all_1.csv")

#describe data(mean,avg,std,etc)
dict = {}
for elem in df.Grade:
    if elem not in dict:
        dict[elem] = 0
    dict[elem] = dict[elem] + 1

print(dict)

number_of_columns = len(df.columns)
print("number of columns: ", number_of_columns)
#histogram showing frequency of features
# for(columnName, columnData) in df.iteritems():
#     title = columnName
#     plt.style.use('ggplot')
#     df[title].plot(kind='hist', color='purple', edgecolor='black', figsize=(10,7))
#     plt.title(title, size=24)
#     plt.xlabel(title, size=18)
#     plt.ylabel('Frequency', size=18)
#     plt.show()

#scatter plot showing relationship between features and Grade
#even distribution of data
# df = df[df.Grade<10]
# N = 158
# df = df.sample(frac=1, random_state = 1).reset_index(drop=True)
# df = df.groupby('Grade')\
#     .apply(lambda x: x[:N])



#scale data based on frequency
for(columnName, columnData) in df.iteritems():
    c = Counter(zip(df[columnName],df['Grade']))
    print(c)
    s = [c[(xx,yy)] for xx,yy in zip(df[columnName],df['Grade'])]
    min_x = min(s)
    max_x = max(s)
    i = 0
    for s_val in s:
        s[i] = scale(s_val, min_x, max_x, 1,200)
        i+=1
    title = "Relationship between " + columnName + " and "+columnName
    df.plot(kind='scatter', s=s, x=columnName, y='Grade', color='magenta', alpha=1, figsize=(10, 7))
   
    plt.legend(labels=['Grade'])
    plt.title(title, size=20)
    plt.xlabel(columnName, size=18)
    plt.ylabel('Grade', size=18)
    plt.show()






#analyze linear relationship between features


#analyze linear correlation matrix
# from mlxtend.plotting import heatmap
# import numpy as np
# cols = ['music_key', 'average_LRH_accidentals', 'average_RH_accidentals', 'average_LH_accidentals','average_next_LH_range','Grade']
# cm = np.corrcoef(df[df.columns].values.T)
# hm = heatmap(cm,
#             cell_font_size=4,
#             figsize=(40,10))
# plt.show()





 