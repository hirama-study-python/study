# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from time import sleep



def main():
    base_url = "https://ja.wikipedia.org"
    url = base_url + "/wiki/首都の一覧"


    # requestsを利用して一覧ページのURLを取得
    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html, 'html.parser')

    # classを指定してtable情報の取得
    country_table = soup.find_all('table', class_='wikitable')[0]

    for country_raw in country_table.find_all("tr"):

        country_columns = country_raw.find_all("td")
        country_links = country_raw.find_all("a")

        for country_link in country_links:

            if len(country_columns) != 0:
                print(f" 国名 :{country_columns[2].text}")
                print(f" 首都名　:{country_columns[1].text}")
                print(f" URL : {base_url + country_link.get('href')}")

                # 詳細ページの取得
                country_detail( country_link.string , base_url + country_link.get( 'href' ) )

                sleep( 2 )

                break


def country_detail(name, url):

    # 引数で指定されたURLからHTMLを取得
    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html, 'html.parser')

    # table要素を取得
    info_table = soup.find_all('table', class_='infobox')

    if len(info_table):
        english_name = info_table[0].find_all('small')
        overviews = soup.find_all('p')

        # 該当テキスト要素の取得
        if len(english_name):
            e_name = english_name[0].text
        else:
            e_name = ""

        if len(overviews):
            overview = overviews[1].text
        else:
            overview = ""

    else:
        e_name = ""
        overview = ""

    print(f" 英名　: {e_name}")
    print(f' 概要 : {overview}')


main()