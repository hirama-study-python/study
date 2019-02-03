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

    soup = html_parse(url)

    detail(url)

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

    soup = html_parse(url)

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
            #カテゴリがない場合のエラー処理を実装
            try:
                category = news.find( "i" ).text
            except AttributeError:
                category = "-"

            re_news = re.sub( '（[^）]*）' , '' , news.text )

            news_obj = {
                "date": date_detail.text ,
                "category": category ,
                "news": re_news
            }



            id = re.sub( '[年月日]' , '-' , date_detail.text ) + str( i )

            save_news( id , news_obj )
            print(id)
            print( json.dumps( news_obj , ensure_ascii=False ) )
            

            sleep(2)



def html_parse(url) :
    r = requests.get( url )
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup_value = BeautifulSoup( html , 'html.parser' )

    return soup_value



def save_news(id, obj):
    #更新分のニュースを変数に代入
    update_news = obj["news"]
    es = Elasticsearch()
    #docker_volume上の要素を参照
    res_news = es.search(index="wiki-portal",doc_type= "news" ,body={"query": {"match_all":{}}})

    if id not in res_news:
        #対象のニュースデータがない場合DBに対象ニュースを追加
        es.index( index='wiki-portal' , doc_type='news' , id=id , body=obj )

    elif update_news.text != res_news.text:
        #対象のニュースがあるが、データの変更があった場合要素を更新
        es.update(index= 'wiki-portal', doc_type = 'news', id=id, body=obj)

    else:
        #対象のニュースがあり、データの変更がない場合なにも行わない
        pass




def query_news_id():
    input_id = input("IDを入力してください：")
    es = Elasticsearch()
    res = es.search(index="wiki-portal",doc_type= "news" ,body={"query": {"match": {"_id":input_id}}})
    result = json.dumps(res,ensure_ascii=False, indent = 4)

    print(result)

main()

#query_news_id()

