# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def main():
    base_url = "https://ja.wikipedia.org"

    url = base_url + "/wiki/首都の一覧"

    # requestsを利用して一覧ページのURLを取得
    r = requests.get(url)
    html = r.content

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html, 'html.parser')

    # classを指定してtable情報の取得
    country_table = soup.find_all(class_="wikitable")[0]

    for country_raw in country_table.find_all("tr"):

        country_columns = country_raw.find_all("td")

        if len(country_columns) != 0:
            print(country_columns[1].text)


main()