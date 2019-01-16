# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from time import sleep
import re


def main():
    url = "https://ja.wikipedia.org/wiki/Portal:最近の出来事"

    r = requests.get(url)
    html = r.content

    soup = BeautifulSoup(html, 'html.parser')

    news_head = soup.find_all("h3")
    news_categories = soup.find_all("i")
    news_articles = soup.find_all("ul")

    for n in range(30):
        article = news_articles[n].find_all("li")

        if article.find("<i>") > -1:
            print("OK")

    # for n in range(30):
    #
    #     news_date = news_head[n].find_all('span' , class_='mw-headline')
    #
    #
    #     for n in news_date :
    #         date = n.text
    #
    #         print(date)
    #
    #         sleep(2)

main()


