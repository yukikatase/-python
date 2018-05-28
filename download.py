# coding: utf-8

'''
コマンド例
python download.py 2015_shinjin http://photozou.jp/photo/list/550732/8711111 2
'''

import sys
import os
import requests
from bs4 import BeautifulSoup
import re
import time


DIR_HOZON = sys.argv[1] # 画像保存先のフォルダ名
URL_ORG = sys.argv[2] # フォト蔵のアルバムのURL
N_PAGES = sys.argv[3] # フォト蔵のアルバムのページ数


# スクレイピングする関数
def scraping():

    soups=[] # BeautifulSoupを貯めておくリスト

    for i in range(int(N_PAGES)):
        url = URL_ORG + '?page=' + str(i + 1)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        soups.append(soup)

    # 画像リンクを取得する
    img_list=[]
    for soup in soups:
        for x in soup.find_all('img'):
            if re.search('src="http', str(x)) and re.search('.jpg', str(x)):
                img_list.append(x)

    # 画像の名前のリスト
    names = [x['title'] for x in img_list]

    # サムネイル画像のリンクのリスト
    thumb_links = [x['src'] for x in img_list]

    # 原寸画像のリンクのリスト
    org_links = [x.replace('thumbnail', 'org') for x in thumb_links]

    return (names, thumb_links, org_links)


# ファイルをダウンロードする関数
def download(mode, names, thumb_links, org_links):

    # mode=Trueのときオリジナルの画像をダウンロードする
    # mode=Falseのときサムネイル画像をダウンロードする
    if mode:
        download_urls = org_links
    else:
        download_urls = thumb_links

    for i in range(len(names)):

        r = requests.get(download_urls[i])

        # ファイルの保存
        if r.status_code == 200:
            if mode:
                f = open(DIR_HOZON +  '/' + names[i] + '.jpg', 'bw')
            else:
                f = open(DIR_HOZON +  '/thumbnail_' + names[i] + '.jpg', 'bw')
            f.write(r.content)
            f.close()
        else:
            print('error - ' + names[i])

        # 0.5秒スリープ
        time.sleep(0.5)


# main関数
def main():
    # 画像保存先のフォルダを作る
    if not os.path.exists(DIR_HOZON):
        os.mkdir(DIR_HOZON)

    names, thumb_links, org_links =  scraping()

    download(True, names, thumb_links, org_links)
    download(False, names, thumb_links, org_links)


if __name__ == '__main__':
    main()
