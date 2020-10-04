#https://mp.weixin.qq.com/s/ApnEy6NWS2f-DqIIrhHzGw

import requests
from bs4 import BeautifulSoup

from bs_headers import get_headers
from bs_myprint import my_print

import os, sys


def download_page(url):
    headers = get_headers(url)
    r = requests.get(url, headers=headers)
    return r.text

def get_content(htmml, page):
    output="""page {}, author: {}, sex: {}, age: {}, thumb: {}, comment: {}\n{}\n-----\n"""  #output format
    soup = BeautifulSoup(htmml, 'html.parser')
    con = soup.find(name='div', attrs={'class':'col1 old-style-col1'})
    #my_print(con)

    con_list = con.find_all('div', class_='article')

    for i in con_list:
        my_print(i)
        author = i.find('h2').string
        content = i.find('div', class_='content').find('span').get_text()
        stats = i.find('div', class_='stats')
        vote = stats.find('span', class_='stats-vote').find('i', class_='number').string
        comment = stats.find('span', class_= 'stats-comments').find('i', class_='number').string
        author_info = i.find('div', class_='articleGender')
        if author_info is not None:
            class_list = author_info['class']
            if 'womenIcon' in class_list:
                gender = 'women'
            elif 'manIcon' in class_list:
                gender = 'man'
            else:
                gender = ''
            age = author_info.string
        else:
            gender = ''
            age = ''

        save_txt(output.format(page, author, gender, age, vote, comment, content))

def save_txt(*args):
    for i in args:
        with open(r_path, 'a', encoding='utf-8') as f:    #wins
            f.write(i)

r_path = os.path.dirname(os.path.realpath(__file__)) + r'\result\qiubai.txt'



if __name__ == "__main__":
    url = 'https://www.qiushibaike.com/text/'
    html = download_page(url)
    get_content(html, 0)