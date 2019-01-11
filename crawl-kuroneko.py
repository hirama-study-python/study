# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from time import sleep



def main():
    base_url = "https://www.wikipedia.org/"

    url = base_url + "wiki/%E9%A6%96%E9%83%BD%E3%81%AE%E4%B8%80%E8%A6%A7"


    # requestsを利用して一覧ページのURLを取得
    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html, 'html.parser')

    # classを指定してtable情報の取得
    country_table = soup.find_all('table', class_='wikitable sortable jquery-tsblesorter')

    for country_raw in country_table:

        # table情報からアンカータグ(link)を取得
        country_links = country_raw.find_all('a')

        for country_link in country_links:
            print(f"{country_link.string}: {base_url + country_link.get('href')}")

            # 詳細ページの取得
            country_detail(country_link.string, base_url + country_link.get('href'))

            # 必ずsleepを入れる
            sleep(2)

            break

        break


def country_detail(name, url):

    # 引数で指定されたURLからHTMLを取得
    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html, 'html.parser')

    # table要素を取得
    info_table = soup.find_all('table', class_='infobox')

    # th, tdタグ要素を取得
    english_name = info_table[0].find_all('tr')


    # 該当テキスト要素の取得
    e_name = english_name[0].text


    print(f"{name}: {e_name}")

main()