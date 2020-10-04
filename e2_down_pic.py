
import requests
import os
import time
import threading
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter
import string

from bs_headers import get_headers
from bs_myprint import my_print


DEBUG = 1

"""
1.get page 0-n
2.at page n, get list4-box
3.for each list-box page,request its url,
4.get pic list.
"""

RESULT_DIR = os.path.dirname(os.path.realpath(__file__)) + r'/result/ex2/'


def download_page(url):
    headers = get_headers(url)
    r = requests.get(url, headers=headers)
    r.encoding
    return r.text

def get_url_ref(url):
    referer = lambda url: re.search(
        "^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)", url
        ).group()  
    return referer(url)


def get_pic_list(url):
    html = download_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    box_list = soup.find_all('div', class_='list4-box')
    ref = get_url_ref(url)[:-1]
    for box in box_list:
        a_tag = box.find('li', class_='title').find('a')
        link = a_tag.get('href')
        my_print(ref + link)
        #html = download_page(ref + link)
        get_pic(ref + link)
        time.sleep(1)

def get_pic(link):
    html = download_page(link)
    soup = BeautifulSoup(html, 'html.parser')
    pic_box = soup.find('div', class_='pic-box')

    title = soup.find('h1').string.strip()

    remove = string.punctuation
    table = str.maketrans('', '', remove)
    title = title.translate(table)

    create_dir(RESULT_DIR + '{}'.format(title))
    my_print(RESULT_DIR + '{}'.format(title))

    pic_list = pic_box.find_all('img')
    i = 0

    headers = get_headers(link)

    for pic in pic_list:
        link = pic.get('src')

        if os.path.exists(RESULT_DIR + '{}/'.format(title)+ str(i) + '.jpg'):
            i = i+1
            continue
        
        my_print(link, DEBUG)

        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=3))

        try:
            r = session.get(link, headers=headers, timeout=5)
            with open(RESULT_DIR + '{}/'.format(title) +str(i)+ '.jpg', 'wb') as f:
                i = i+1
                f.write(r.content)
                time.sleep(1)
        except requests.exceptions.ConnectionError as e:
            print('url failed')
        #r = requests.get(link, headers=headers)
        


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def main():
    queue = [i for i in range(1, 2)]
    threads  = []
    while len(queue) > 0 or len(threads) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < 1 and len(queue) > 0:
            cur_page = queue.pop(0)
            url = 'https://www.51tietu.net/xiezhen/{}'.format(cur_page)
            thread = threading.Thread(target=get_pic_list, args=(url,))
            thread.setDaemon(True)
            thread.start()
            my_print('down load page {}'.format(cur_page))
            threads.append(thread)
            

if __name__ == "__main__":
    DEBUG = 1
    main()
"""    page_l = 'https://www.51tietu.net/xiezhen/0'
    box_l = 'https://www.51tietu.net/xiezhen/211926.html'
    #p = download_page(box_l)
    get_pic_list(page_l)"""