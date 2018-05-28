
# coding: utf-8

# ## スクレイピング
# **必要なライブラリ**
# - BeautifulSoup
# - requests
# - re
# - time

# In[23]:



import requests
from bs4 import BeautifulSoup
import math

# 画像保存先のフォルダ名
DIR_HOZON = 'test'

# フォト蔵のアルバムのURL
URL_ORG = 'http://photozou.jp/photo/list/550732/2275613'


soups = [] # BeautifulSoupを貯めておくリスト

# 1ページ目
url = URL_ORG + '?page=1'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
soups.append(soup)

# フォト蔵のアルバムの画像の枚数
n_pic = int(str(soup('dd')[0]).split('>')[1].split('枚')[0])

# フォト蔵のアルバムのページ数
n_pages = math.ceil(n_pic / 20)

# 2ページ目以降
if n_pages > 1:
    for i in range(n_pages):
        if i != 0:
            url = URL_ORG + '?page=' + str(i + 1)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            soups.append(soup)


# In[24]:

# 画像リンクを取得する
import re
img_list=[]
for soup in soups:
    for x in soup.find_all('img'):
        if re.search('src="http', str(x)) and re.search('.jpg', str(x)):
            img_list.append(x)

# 画像枚数が合っているか確認
print(len(img_list))

# サムネイル画像のリンクのリスト
thumb_links = [x['src'] for x in img_list]

# 原寸画像のリンクのリスト
org_links = [x.replace('thumbnail', 'org') for x in thumb_links]

# 画像の名前のリスト
names = [x['title'] for x in img_list]


# In[25]:

# 名前重複確認
chofuku=[]
for x in sorted(names):
    if x not in chofuku:
        chofuku.append(x)
    else:
        print(x)
print(len(chofuku))


# In[89]:

import time

# サムネイルか原寸画像か選ぶ(原寸のときselect=True, サムネselect=Falseで)
select = True

if select:
    download_urls = org_links
else:
    download_urls = thumb_links

# ファイルのダウンロード（for文を回す間隔を設定してから実行!!!!!!!）
for i in range(len(names)):    
    
    r = requests.get(download_urls[i])
    
    # ファイルの保存
    if r.status_code == 200:
        if select:
            f = open(DIR_HOZON +  '/' + names[i] + '.jpg', 'bw')
        else:
            f = open(DIR_HOZON +  '/thumbnail_' + names[i] + '.jpg', 'bw')
        f.write(r.content)
        f.close()
    else:
        print('error - ' + names[i])
    
    # 0.5秒スリープ
    time.sleep(0.5)


# In[ ]:




# ## HTML生成
# **必要なライブラリ**
# - glob
# - re

# In[102]:



import glob

# 画像が入っているフォルダ
DIR_HOZON = '2017_26univ'

# 生成するhtml
htm1 = DIR_HOZON + '.html'

# htmlのタイトル
TITLE = r'2017年26大学対校戦'

# フォルダ内の画像のパスを取得
files = glob.glob(DIR_HOZON + '/*.jpg')

# フォルダ内の画像の名前のリスト
file_names = [x.replace(DIR_HOZON + '/', '').replace('.jpg', '') for x in files]


# In[107]:

import re

f = open(htm1, 'a')

f.write('<!DOCTYPE html>' + '\n')
f.write('<html>' + '\n')
f.write('  <head>' + '\n')
f.write('    <meta charset="UTF-8" />' + '\n')
f.write('    <title>' + TITLE + '</title>' + '\n')
f.write('  </head>' + '\n')
f.write('  <body>' + '\n')

for name in file_names:
    if not re.search('thumbnail', name):
        f.write('    <a href="' + DIR_HOZON + '/' + name + '.jpg' + '"><img src="' + DIR_HOZON + '/thumbnail_' + name + '.jpg' + '" alt="image" width="120" border="0" /></a>\n')

f.write('  </body>' + '\n')
f.write('</html>' + '\n')

f.close()


# In[ ]:




# In[ ]:




# In[1]:

with open('event_list.txt', 'r') as f:
    event_list = f.readlines()


# In[7]:

a = [event.split(' ')[0] for event in event_list]


# In[8]:

a


# In[ ]:



