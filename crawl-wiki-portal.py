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

    #日付とカテゴリを取得
    news_date = soup.find_all( 'span' , class_='mw-headline' )
    news_categories = soup.find_all("i")

    news_articles = soup.find_all("ul")
    #news_article = news_articles.find_all("li")

    for n in range(30):

        date = news_date[n].text
        #artice = news_articles[n].text
        category = news_categories[n].text

        print(date +":"+ category)

        sleep(2)




main()


