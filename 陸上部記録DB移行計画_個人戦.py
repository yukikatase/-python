
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import re
import math
import copy


# In[2]:

html = 'schedule/s2014/private.php'
fetched_dataframes = pd.io.html.read_html(html)
p_name = html.split('/')[1] + '_' + html.split('/')[2].split('.')[0]


# In[10]:

lst = []
for i in range(len(fetched_dataframes)):
    if fetched_dataframes[i][0][0] == '種目':
        lst.append(i)


# In[11]:

j = lst[0]
fetched_dataframes[j]


# In[12]:

k = lst[-1]
fetched_dataframes[k]


# In[13]:

dfs = pd.concat([fetched_dataframes[i].iloc[1:, :] for i in lst])
dfs


# In[14]:

dfs.columns=['種目', '氏名', '記録', '風', '備考']
dfs = dfs.reset_index(drop=True)

dfs


# In[15]:

new_dfs = pd.DataFrame(columns=['種目', '氏名', '記録', '風', '備考'])

for i in range(len(dfs)):
    line = dfs.iloc[i]['種目']
    temp_df = pd.DataFrame(dfs.iloc[i])
    if re.search('\d', line) or re.search('跳', line) or re.search('投', line) or re.search('マラソン', line):
        temp_df = temp_df.T
    else:
        temp_df = temp_df.shift(1).T
    
    new_dfs = new_dfs.append(temp_df)
    
new_dfs


# In[16]:

new_dfs2 = copy.deepcopy(new_dfs)
track = pd.DataFrame(columns=['種目', '氏名', '記録', '風', '備考'])
field = pd.DataFrame(columns=['種目', '氏名', '記録', '風', '備考'])

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


# In[17]:

track['時間'] = [np.nan for i in range(len(track))]
track['分'] = [np.nan for i in range(len(track))]
track['秒']  = [np.nan for i in range(len(track))]
track['秒以下'] = [np.nan for i in range(len(track))]


# In[18]:

track = track.reset_index(drop=True)
field = field.reset_index(drop=True)


# In[20]:

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
        
track2


# In[21]:

track3 = copy.deepcopy(track2)

for i in range(len(track3)):
    discipline = track3.iloc[i]['種目']
    if isinstance(discipline, str):
        temp_dis = discipline
    
    else:
        track3['種目'][i] = temp_dis

track3['区分'] = [np.nan for i in range(len(track3))]


# In[22]:

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


# In[23]:

track4


# In[24]:

track5 = copy.deepcopy(track4)

for i in range(len(track5)):
    wind = track5.iloc[i]['風']
    if isinstance(wind, float) and math.isnan(wind):
        continue
    else:
        if re.search(r'PB', wind) or re.search(r'位', wind) or re.search(r'Q', wind) or re.search(r'q', wind):
            track5['備考'][i] = wind
            track5['風'][i] = np.nan
            
track5


# In[25]:

track6 = copy.deepcopy(track5)

for i in range(len(track6)):
    record = track6.iloc[i]['記録']
    name = track6.iloc[i]['氏名']
    if record == 'DNS' or record == 'DNF' or record == 'DQ' or record == 'DSQ':
        track6['備考'][i] = record
    if re.search('　', name) or re.search(' ', name):
        track6['氏名'][i] = name.replace('　', '').replace(' ', '')
        
track6


# In[30]:

track6.to_csv(p_name + '_track.csv', encoding='shift_jis', sep=',')


# In[ ]:




# In[44]:

field2 = copy.deepcopy(field)

for i in range(len(field2)):
    line = field.iloc[i]['記録']

    if re.search('m', line):
        field2['記録'][i] = line.replace('m', '.')


# In[45]:

field3 = copy.deepcopy(field2)

for i in range(len(field3)):
    discipline = field3.iloc[i]['種目']
    if isinstance(discipline, str):
        temp_dis = discipline
    
    else:
        field3['種目'][i] = temp_dis

field3['区分'] = [np.nan for i in range(len(field3))]


# In[46]:

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


# In[47]:

field5 = copy.deepcopy(field4)

for i in range(len(field5)):
    wind = field5.iloc[i]['風']
    if isinstance(wind, float) and math.isnan(wind):
        continue
    else:
        if re.search(r'PB', wind) or re.search(r'位', wind) or re.search(r'Q', wind) or re.search(r'q', wind):
            field5['備考'][i] = wind
            field5['風'][i] = np.nan


# In[48]:

field6 = copy.deepcopy(field5)

for i in range(len(field6)):
    record = field6.iloc[i]['記録']
    name = field6.iloc[i]['氏名']
    if record == 'DNS' or record == 'DNF' or record == 'DQ' or record == 'DSQ' or record == 'NM':
        field6['備考'][i] = record
    if re.search('　', name) or re.search(' ', name):
        field6['氏名'][i] = name.replace('　', '').replace(' ', '')
        
field6


# In[ ]:




# In[49]:

field6.to_csv(p_name + '_field.csv', encoding='shift_jis')


# In[ ]:




# In[ ]:



