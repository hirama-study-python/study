# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import json
from elasticsearch import Elasticsearch


def main():
    base_url = "https://ja.wikipedia.org"
    url = base_url + "/wiki/Portal:最近の出来事"

    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html, 'html.parser')

    # ページ内のテーブルを取ってくる
    date_headlines_table = soup.find('table')

    #テーブルの中のテーブルを取ってくる
    summary_table = date_headlines_table.find_all('table')

    for year_list in summary_table:

        year_summaries = year_list.find_all('ul')

    for year_summary in year_summaries:

        #<ul>タグの次の<dl>タグを取ってくる
        month_summary = year_summary.next_sibling.string.next_sibling

        for month_link_tag in month_summary.find_all("a"):

            month_link = base_url + month_link_tag.get('href')


            detail(month_link)

            sleep(2)



def detail(url):

    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup( html , 'html.parser' )

    # ページ内のテーブルを取ってくる
    date_headlines_table = soup.find('div' ,class_ = "mw-parser-output")

    # 見出しの日付を取得する
    date_headlines = date_headlines_table.find_all( 'h3' )

    for date_headline in date_headlines:

        date_detail = date_headline.find('span',class_ = "mw-headline")
        # 日付見出しの次は必ず<ui>タグが設定されている
        newses = date_headline.next_sibling.string.next_sibling

        # <ui>タグ内の<li>タグを探す
        for i , news in enumerate( newses.find_all( 'li' ) ):
            category = news.find( "i" )
            re_news = re.sub( '（[^）]*）' , '' , news.text )

            news_obj = {
                "date": date_detail.text ,
                "category": category.text ,
                "news": re_news
            }



            id = re.sub( '[年月日]' , '-' , date_headline.text ) + str( i )

            save_news( id , news_obj )
            print( json.dumps( news_obj , ensure_ascii=False ) )
            

            sleep(2)

            break
        break


def save_news(id, obj):

    es = Elasticsearch()

    es.index('wiki-portal', 'news', id=id, body=obj)


main()

