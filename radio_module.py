from bs4 import BeautifulSoup
from requests import get
import urllib.request
import urllib.parse
from PyQt5.QtWidgets import *
import time
import webbrowser
import os


def last_page_module(search):

    last_page_num_list = []

    url = f'https://radibrary.tistory.com/search/{search}?page=1'

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')


    last_page_num = soup.select('.inner_paging > .link_page')

    if last_page_num is None or last_page_num == '' or not last_page_num:
        return 0

    else:

        for i in last_page_num:

            last_page_num_list.append(i.get_text())


        print(f'\n{last_page_num_list[-1]} 페이지의 결과가 탐색됨....')
        return last_page_num_list[-1] #마지막 페이지





def url_list_module(post_list, url_list, search, page_num):  # 검색어 입력,검색해서 포스트 제목,url 표시 + [url리스트 에 저장]

    url = f'https://radibrary.tistory.com/search/{search}?page={page_num}'

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select('.list_content > .link_post > .tit_post')
    title_url = soup.select('.list_content > .link_post')

    for title, title_url in zip(title, title_url):
        print(title.get_text())
        print('https://radibrary.tistory.com' + title_url.attrs['href'])
        print('\n----------------------------------------------------------------------------------\n')

        post_list.append(title.get_text())
        url_list.append('https://radibrary.tistory.com' + title_url.attrs['href'])
