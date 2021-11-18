from random import randint
from token import NAME
import requests
import requests
from requests.exceptions import Timeout
import bs_headers
import os,sys
from bs4 import BeautifulSoup
from bs_myprint import MyPrint
import chardet
#from fake_useragent import UserAgent
#import brotli
import random
import time
import threading
from queue import Queue
from urllib.parse import urlparse, unquote

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
LOGGER.setLevel(logging.WARNING)

# file path
import platform
if platform.system().lower() == 'windows':
    EXECUTE_PATH = "C:\\Users\\apple\\anaconda3\\Scripts\\geckodriver.exe"
    RESULT_DIR = os.path.dirname(os.path.realpath(__file__)) + r'\esult\video'
elif platform.system().lower() == 'linux':
    EXECUTE_PATH = "/usr/bin/geckodriver"
    RESULT_DIR = os.path.dirname(os.path.realpath(__file__)) + r'/video/'


DEBUG = 1
my_print = MyPrint(DEBUG)



from os import rename
import youtube_dl
import youtube_dl.utils


class Myheaders:
    def __init__(self, url) -> None:
        self.url = url

    def createHost(self) -> None:
        parsed_uri = urlparse(self.url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        self.host = domain

    def get_headers(self) -> dict:
        self.createHost()

        headers = {
        'User-Agent': bs_headers.random_ua(),
        'DNT': "1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'br,gzip, deflate', #, br
        'Host': self.host,
        }
        return headers

class MyDriver:
    def __init__(self) -> None:
        option = Options()
        option.add_argument('-headless')
        option.add_argument('user-agent={}'.format(bs_headers.random_ua()))
        option.set_preference('permissions.default.stylesheet', 2)
        option.set_preference('permissions.default.image', 2)
        #option
        self.driver = webdriver.Firefox(options=option, executable_path=EXECUTE_PATH)

    
class ResultLists:
    def __init__(self, urls, names) -> None:
        self.video_urls = urls
        self.names = names

class YDL(object):

    def rename_hook(self,d):
        # 重命名下载的视频名称的钩子
        if d['status'] == 'finished':
            #file_name = 'video_{}.mp4'.format(int(time.time()))
            file_name = self.video_name
            rename(d['filename'], file_name)
            print('下载完成{}'.format(file_name))

    def download(self,youtube_url, name):
        self.video_name = name
        youtube_dl.utils.std_headers['User-Agent'] = bs_headers.random_ua()
        # 定义某些下载参数
        ydl_opts = {
            'progress_hooks': [self.rename_hook],
            # 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': '%(id)s%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            result = ydl.download([youtube_url])

class GetVideo:
    def __init__(self, driver:MyDriver=None, youdl:YDL=None, html_url=None) -> None:
        self.html_url = html_url
        self.geckodriver = driver
        self.youdl = youdl

    #use geckodriver to download player page
    def get_page_data(self, url) -> str:
        # try 5 times
        i = 5
        while i:
            h = Myheaders(url).get_headers()
            try:
                r = requests.get(url, headers=h, timeout=5)
                if r.status_code == 200:
                    d = r.content
                    charset1 = chardet.detect(d)
                    encoding = charset1['encoding']
                    return d.decode(encoding)

                elif r.status_code == 403:
                    my_print.my_print(r.headers)
                    my_print.my_print("access forbidden")
                i = i - 1
            except Exception as e:
                my_print.my_print("error")
                my_print.my_print(e)
                return None
        return None

    def page_video_url(self, data):
        my_print.my_print('get video url...')
        if data is not None:
            soup = BeautifulSoup(data, 'lxml')
            frame = soup.find('div', class_='content')
            frame_url = frame.find('iframe')['src'] # str

            mp4_url = unquote(frame_url.split("url=")[1]).split('&')[0]
            
            #my_print.my_print(frame)
            my_print.my_print(frame_url)
            my_print.my_print(mp4_url)
            #video_name = soup.find('')
            return mp4_url

    def page_video_name(self, data):
        if data is not None:
            soup = BeautifulSoup(data, 'lxml')
            video_name = soup.select('h4 > a')[0].text
            return video_name

    def check_path_exits(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    # not use
    def get_page_video_url(self, url):
        data = self.get_page_data( url)
        self.page_video_url(data)
        """my_print.my_print('get video url...')
        if data is not None:
            soup = BeautifulSoup(data, 'lxml')
            frame = soup.find('div', class_='content')
            my_print.my_print(frame)"""
        
    def geckodrive_download_video(self, url, name=None):
        self.geckodriver.get(url)
        page_data = self.geckodriver.page_source
        mp4url = self.page_video_url(page_data)
        if name is None:
            name = self.page_video_name(page_data) + url.split('playid=')[1] #+ mp4url.split('.')[-1]
        name = RESULT_DIR + name
        my_print.my_print('{},{}'.format(name, mp4url))

        # check file exits before download
        if self.check_path_exits(name):
            my_print.my_print('file exits, skip download.')
            return


        self.youdl.download(mp4url, name)

        """driver.close()
        driver.quit()"""
    
    def get_page_urllists(self, url):
        #download agefan.net urls
        #[name , url]
        data = self.get_page_data(url)
        my_print.my_print('download page list....')
        if data is not None:
            soup = BeautifulSoup(data, 'lxml')
            video_name = soup.find('h4', class_='detail_imform_name').string
            #url_li = soup.find('div', class_='main0').find('div', attrs={'style': 'display: block'}).find('ul')
            url_li1 = soup.find('div', class_='main0')
            #my_print.my_print(url_li1)
            url_li = url_li1.find('div', attrs={'style': 'display:block'}).find_all('li')
            #my_print.my_print(url_li)
            urls = []
            for i in url_li:
                href = 'https://www.agefans.net' + i.find('a')['href']
                name = video_name + i.find('a')['title']
                urls.append([name, href])

            return urls
        my_print.my_print('page lists is none')
        return None

    def run(self, url):
        #get page urls
        #check file is exis
        #if not exits, then download.
        #sleep randon(20s,30s)
        try:
            if 'play' in url:
                #download single video 
                self.geckodrive_download_video(url)
            else:
                urls = self.get_page_urllists(url)
                if urls is not None:
                    for name, url in urls:
                        self.geckodrive_download_video(url, name)
                        time.sleep(randint(20, 30))
                    
        finally:
            self.geckodriver.quit()


if __name__ == "__main__":
    """t_u = 'https://www.agefans.net/play/20210036?playid=3_1'
    getPage = GetPages(t_u)
    getPage.get_page_video_url(t_u)
    getItem =  GetItem()
    getItem.download('https://www.youtube.com/watch?v=VUOAszEiR8I')
    
    """
    #t_u1 = 'https://www.baidu.com'


    """t_u1 = 'https://www.agefans.net/play/20210005?playid=3_4'
    page = GetPages(t_u1)
    driver = MyDriver().driver
    driver.get(t_u1)
    #print(driver.page_source)
    page_data = driver.page_source
    mp4url = page.page_video_process(page_data)
    getItem =  GetItem()
    getItem.download(mp4url)
    driver.close()
    driver.quit()"""

    """t_u1 = 'https://www.agefans.net/detail/20140129'
    page = GetPages(html_url=t_u1)
    urls = page.get_page_lists(t_u1)
    print(urls)"""

    #t_u1 = 'https://www.agefans.net/play/20200004?playid=3_1'
    t_u1  = 'https://www.agefans.net/detail/20200014'
    driver = MyDriver().driver
    ydl = YDL()
    d = GetVideo(driver=driver, youdl=ydl, html_url=t_u1)
    d.run(t_u1)






