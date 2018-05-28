
# coding: utf-8

# In[12]:

import pandas as pd
import numpy as np
import re
import math
import copy


# In[36]:

html = 'schedule/s2016/index.php'
fetched_dataframes = pd.io.html.read_html(html)
name = html.split('/')[1] + '_' + html.split('/')[2].split('.')[0]


# In[49]:

j = 5
fetched_dataframes[j]


# In[50]:

k = 12
fetched_dataframes[k]


# In[51]:

dfs = pd.concat([fetched_dataframes[i].iloc[1:, :] for i in range(j, k+1)])
dfs


# In[53]:

dfs.columns=['種目', '組', '選手', '記録', '着順', '風・備考']
dfs = dfs.reset_index(drop=True)

dfs


# In[54]:

new_dfs = pd.DataFrame(columns=['種目', '組', '選手', '記録', '着順', '風・備考'])

for i in range(len(dfs)):
    line = dfs.iloc[i]['種目']
    temp_df = pd.DataFrame(dfs.iloc[i])
    if re.search('\d', line) or re.search('跳', line) or re.search('投', line) or re.search('マラソン', line):
        temp_df = temp_df.T
    else:
        temp_df = temp_df.shift(1).T
    
    new_dfs = new_dfs.append(temp_df)
    
new_dfs


# In[55]:

new_dfs2 = copy.deepcopy(new_dfs)
track = pd.DataFrame(columns=['種目', '組', '選手', '記録', '着順', '風・備考'])
field = pd.DataFrame(columns=['種目', '組', '選手', '記録', '着順', '風・備考'])

status = False
for i in range(len(new_dfs2)):
    discipline = new_dfs2.iloc[i]['種目']
    if isinstance(discipline, str):
        if re.search('投', discipline) or re.search('跳', discipline):
            field = field.append(pd.DataFrame(new_dfs2.iloc[i]).T)
            status = True
            
        else:
            track = track.append(pd.DataFrame(new_dfs2.iloc[i]).T)
            status = False
    
    else:
        if math.isnan(discipline) and status:
            field = field.append(pd.DataFrame(new_dfs2.iloc[i]).T)
            status = True
        
        else:
            track = track.append(pd.DataFrame(new_dfs2.iloc[i]).T)
            status = False


# In[56]:

track['時間'] = [np.nan for i in range(len(track))]
track['分'] = [np.nan for i in range(len(track))]
track['秒']  = [np.nan for i in range(len(track))]
track['秒以下'] = [np.nan for i in range(len(track))]


# In[57]:

track = track.reset_index(drop=True)
field = field.reset_index(drop=True)


# In[58]:

track2 = copy.deepcopy(track)

for i in range(len(track2)):
    line = track2.iloc[i]['記録']

    if re.search(':', line):
        track2['時間'][i] = line.split(':')[0]
        track2['分'][i] = line.split(':')[1].split('\'')[0]
        track2['秒'][i] = line.split(':')[1].split('\'')[1].split('\"')[0]
        
    elif re.search('\'', line):
        track2['分'][i] = line.split('\'')[0]
        track2['秒'][i] = line.split('\'')[1].split('\"')[0]
        if re.search('\"', line):
            track2['秒以下'][i] = line.split('\'')[1].split('\"')[1]
    
    elif re.search('\"', line):
        track2['秒'][i] = line.split('\"')[0]
        track2['秒以下'][i] = line.split('\"')[1]


# In[60]:

track3 = copy.deepcopy(track2)

for i in range(len(track3)):
    discipline = track3.iloc[i]['種目']
    if isinstance(discipline, str):
        temp_dis = discipline
    
    else:
        track3['種目'][i] = temp_dis

track3['区分'] = [np.nan for i in range(len(track3))]


# In[61]:

track4 = copy.deepcopy(track3)

for i in range(len(track4)):
    discipline = track4.iloc[i]['種目']
    
    if re.search(r'H', discipline):
        if len(discipline.split('H')) > 1 and discipline.split('H')[1] != '':
                track4['区分'][i] = discipline.split('H')[1].replace(' ', '')
                track4['種目'][i] = discipline.replace(discipline.split('H')[1], '')
    
    elif re.search(r'C', discipline):
        if len(discipline.split('C')) > 1 and discipline.split('C')[1] != '':
                track4['区分'][i] = discipline.split('C')[1].replace(' ', '')
                track4['種目'][i] = discipline.replace(discipline.split('C')[1], '')

    elif re.search(r'TR', discipline):
        if len(discipline.split('R')) > 1 and discipline.split('m')[1] != '':
                track4['区分'][i] = discipline.split('m')[1].replace(' ', '')
                track4['種目'][i] = discipline.replace(discipline.split('m')[1], '')

    elif re.search(r'mR', discipline):
        if len(discipline.split('R')) > 1 and discipline.split('R')[1] != '':
                track4['区分'][i] = discipline.split('R')[1].replace(' ', '')
                track4['種目'][i] = discipline.replace(discipline.split('R')[1], '')

                
    elif len(discipline.split('m')) > 1 and discipline.split('m')[1] != '':
        track4['区分'][i] = discipline.split('m')[1].replace(' ', '')
        track4['種目'][i] = discipline.replace(discipline.split('m')[1], '')


# In[62]:

track4


# In[28]:

track4.to_csv(name + '_track.csv', encoding='shift_jis')


# In[ ]:




# In[29]:

field2 = copy.deepcopy(field)

for i in range(len(field2)):
    line = field.iloc[i]['記録']

    if re.search('m', line):
        field2['記録'][i] = line.replace('m', '.')


# In[30]:

field3 = copy.deepcopy(field2)

for i in range(len(field3)):
    discipline = field3.iloc[i]['種目']
    if isinstance(discipline, str):
        temp_dis = discipline
    
    else:
        field3['種目'][i] = temp_dis

field3['区分'] = [np.nan for i in range(len(field3))]


# In[32]:

field4 = copy.deepcopy(field3)

for i in range(len(field4)):
    discipline = field4.iloc[i]['種目']
    
    if re.search(r'跳', discipline):
        if len(discipline.split('跳')) > 1 and discipline.split('跳')[1] != '':
                field4['区分'][i] = discipline.split('跳')[1].replace(' ', '')
                field4['種目'][i] = discipline.replace(discipline.split('跳')[1], '')
    
    elif re.search(r'投', discipline):
        if len(discipline.split('投')) > 1 and discipline.split('投')[1] != '':
                field4['区分'][i] = discipline.split('投')[1].replace(' ', '')
                field4['種目'][i] = discipline.replace(discipline.split('投')[1], '')


# In[31]:

field4.to_csv(name + '_field.csv', encoding='shift_jis')


# In[ ]:



