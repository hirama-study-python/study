# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from time import sleep
import re



def main():
    url = "https://ja.wikipedia.org/wiki/Portal:最近の出来事"

    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html, 'html.parser')

    # ページ内のテーブルを取ってくる
    date_headlines_table = soup.find('table')

    # 見出しの日付を取得する
    date_headlines = date_headlines_table.find_all('h3')

    for date_headline in date_headlines:

        print(date_headline.text)

        # 日付見出しの次は必ず<ui>タグが設定されている
        newses = date_headline.next_sibling.string.next_sibling

        # <ui>タグ内の<li>タグを探す
        for news in newses.find_all('li'):
            #<li>タグの内の<i>タグを探す
            for category in news.find_all("i"):
                #正規表現で（＊＊）というカテゴリ部分を削除
                re_news = re.sub('（[^）]*）', '', news.text)
                #カテゴリとニュース内容を出力
                print(category.text)
                print(re_news)

            sleep( 2 )
main()
