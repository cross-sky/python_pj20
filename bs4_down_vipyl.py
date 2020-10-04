import requests
import bs_headers
import os,sys
from bs4 import BeautifulSoup
from bs_myprint import MyPrint
import chardet
#from fake_useragent import UserAgent
#import brotli
import random
import time

DEBUG = 1
my_print = MyPrint(DEBUG)
RESULT_DIR = os.path.dirname(os.path.realpath(__file__)) + r'/result/vipyl/'

'''
get total page
each page using one threading
using 5 threading
get article list
get article
save article
'''
class DownArticle:
    def __init__(self, url):
        pass
    
    def get_headers(self):
        #ua = UserAgent(use_cache_server=False)
        #ua = UserAgent()
        headers = {
        'User-Agent': bs_headers.random_ua(),
        'DNT': "1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'br,gzip, deflate', #, br
        'Host': 'www.vipyl.com',
        'TE': 'Trailers'
        }
        return headers

    def get_page(self, url):
        i = 5
        while i:
            headers = self.get_headers() #bs_headers.get_headers(url)
            try:
                r = requests.get(url, headers=headers, timeout=5)
                if r.status_code == 200:
                    d = r.content
                    charset1 = chardet.detect(d)
                    encoding = charset1['encoding']
                    if encoding is 'GB2312':
                        encoding = 'gb18030'
                    #my_print.my_print(charset1)
                    #my_print.my_print(d.decode(charset1['encoding'])[300:400])  # str.encode(r.text)
                    """my_print.my_print(r.headers)
                    key = 'Content-Encoding'
                    if (key in r.headers and r.headers[key] == 'br' ):
                        data = brotli.decompress(r.content)
                        my_print.my_print(data[:300]) #r.content
                    else:
                        #r.encoding = 'gbk'
                        data = r.content
                    return data"""
                    #my_print.my_print(d[:400])
                    #my_print.my_print(d.decode(encoding)[300:400])
                    return d.decode(encoding)
                elif r.status_code == 403:
                    my_print.my_print(r.headers)
                    #my_print.my_print(headers['User-Agent'])
                    my_print.my_print('access forbidden')
                i = i-1
            except Exception as e:
                print(e)
                return None
        return None

    def get_total_page(self, url):
        data = self.get_page(url)
        if data is not None:
            soup = BeautifulSoup(data, 'lxml')
            total = soup.find('div', class_='pagecss')
            #my_print.my_print(total)
            p = total.find('strong').text.split('/')[1]
            my_print.my_print(p)
            return int(p)

    def check_path_exits(self, path):
        if os.path.exists(path):
            return True
        else:
            return False
    
    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def save_jkes(self, path, content):
        with open(path, 'a', encoding='utf-8') as f:
            try:
                for arts in content:
                    if arts is not None:
                        f.write('\n'.join(arts))
                    f.write('\n')
            except Exception as e:
                print(e)
        

    def get_article(self, url):
        data = self.get_page(url)
        my_print.my_print('download.article...' + url)
        if data is not None:
            soup = BeautifulSoup(data, 'lxml')#from_encoding='gbk',charset1['encoding']
            h1 = soup.find('h1').string +'*****'
            body = soup.find('div', class_='Article_body')
            p = body.find_all('p')
            articles = [h1]
            for i in p:
                joke = i.text.strip()
                if joke is not "":
                    articles.append(joke)
            return articles
        my_print.my_print('download.article... none')    
        return None

    def get_article_list(self, url, page_number):
        '''
        https://www.youtube.com/watch?v=W3jQmX1NHhY
        https://www.youtube.com/watch?v=0OS8FGIOFw0
        get header
        get page
        get list
        get article save to one txt, thitle = '经典搞笑语录_page.txt'
        '''
        data = self.get_page(url)
        my_print.my_print('download.page list...' + url)
        if data is not None:
            soup = BeautifulSoup(data, 'lxml')#from_encoding='gbk',charset1['encoding']
            art = soup.find('ul', attrs={'id': 'artadd'})
            art_list = art.find_all('div', attrs={'class': 'rightnr'})

            articles = []
            for i in art_list:
                href = 'https://www.vipyl.com' + i.find('a')['href']
                contents = self.get_article(href)
                articles.append(contents)
                time.sleep(random.randint(3,6))
            self.save_jkes(RESULT_DIR + '经典搞笑语录_{}.txt'.format(page_number), articles)
                #my_print.my_print(href)

if __name__ == "__main__":
    # get total page
    # check file exits 
    # get page list
    # get article, and save artiles in one file
    url = 'https://www.vipyl.com/article/143/list_1.html'
    #url = 'https://www.vipyl.com/article/143/418218.html'
    u = 'https://www.vipyl.com/article/143/410747.html' #410747

    article = DownArticle(url)
    article.create_dir(RESULT_DIR)
    total = article.get_total_page(url)
    # total = 2

    # a = article.get_article(u)
    #print(total+1)

    for i in range(1, total+1):
        u = 'https://www.vipyl.com/article/143/list_{}.html'.format(i)
        if not article.check_path_exits(RESULT_DIR + '经典搞笑语录_{}.txt'.format(i)):
            article.get_article_list(u, i)


    # ur = 'https://www.vipyl.com/article/143/68400.html'
    # content = article.get_article(ur)
    # my_print.my_print(content)
    #article.get_article_list(url)





