# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from time import sleep


def main():
    base_url = "http://date.kuronekoyamato.co.jp"

    url = base_url + "/date/KokusaiTakkyubin?ACTID=J_RKWTJS0010&SEARCH_ID=02"

    # requestsを利用して一覧ページのURLを取得
    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html, 'html.parser')

    # classを指定してtable情報の取得
    country_table = soup.find_all('table', class_='tableStyle01 linkIcon')

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
    price_table = soup.find_all('table', class_='tableStyle02 elm-s')

    # th, tdタグ要素を取得
    headers = price_table[0].find_all('th')
    prices = price_table[0].find_all('td')

    # 該当テキスト要素の取得
    header = headers[2].text
    price = prices[1].string

    print(f"{name}: {header}: {price}")

main()