"""url download
Usage:
    gecko <url>

Example:
    gecko www.apple.com
"""

from selenium import webdriver

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
LOGGER.setLevel(logging.WARNING)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


import bs_headers
import os,sys,time
import bs_headers

import platform
if platform.system().lower() == 'windows':
    EXECUTE_PATH = "C:\\Users\\apple\\anaconda3\\Scripts\\geckodriver.exe"
    RESULT_DIR = os.path.dirname(os.path.realpath(__file__)) + r'\result\video'
elif platform.system().lower() == 'linux':
    EXECUTE_PATH = "/usr/bin/geckodriver"
    RESULT_DIR = os.path.dirname(os.path.realpath(__file__)) + r'/video/'

from docopt import docopt

def cli() -> dict:
    return docopt(__doc__)

import argparse
parser = argparse.ArgumentParser(description='video url')
parser.add_argument('url', type=str, help='video url')
args = parser.parse_args()

class MyDriver:
    def __init__(self) -> None:
        option = Options()
        option.add_argument('-headless')
        #option.add_argument('user-agent={}'.format(bs_headers.random_ua()))
        option.set_preference('general.useragent.override', bs_headers.random_ua())
        option.set_preference('permissions.default.stylesheet', 2)
        option.set_preference('permissions.default.image', 2)

        option.set_preference("browser.download.folderList",2)
        option.set_preference('browser.download.dir', RESULT_DIR)
        option.set_preference("browser.download.manager.showWhenStarting", False)
        option.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4")
        option.set_preference("browser.helperApps.neverAsk.openFile","video/mp4")
        option.set_preference("browser.helperApps.alwaysAsk.force", False)
        option.set_preference("browser.download.manager.useWindow", False)
        option.set_preference("browser.download.manager.focusWhenStarting", False)
        option.set_preference("browser.download.manager.showAlertOnComplete", False)
        option.set_preference("browser.download.manager.closeWhenDone", True)

        print(RESULT_DIR)

        self.option = option
        self.driver = webdriver.Firefox(options=self.option, executable_path=EXECUTE_PATH)

        #option

    def download(self, url, name=None):
        try:
            self.driver.get(url)

            # waiting server for finishing inner task
            def download_begin(driver):
                if len(os.listdir()) == 0:
                    time.sleep(5)
                    return False
                else:
                    return True
            WebDriverWait(self.driver, 120).until(download_begin) # the max wating time is 120s

            # waiting server for finishing sending.
            # if size of directory is changing,wait
            def download_complete(driver):
                sum_before=-1
                sum_after=sum([os.stat(file).st_size for file in os.listdir()])
                while sum_before != sum_after:
                    time.sleep(5)
                    sum_before = sum_after
                    sum_after = sum([os.stat(file).st_size for file in os.listdir()])
                return True
            WebDriverWait(self.driver, 120).until(download_complete)  # the max wating time is 120s

            self.driver.get('www.baidu.com')
            print('download finish.')
        except Exception as e:
            print('error')
            print(e)
        finally:
            print('exit..')
            self.driver.close()
            self.driver.quit()

def get_file_url(filename):
    with open(filename, 'r') as f:
        urls = f.readlines()
    return urls

if __name__ == "__main__":
    dr = MyDriver()
    #url = 'https://cloud189-sichuan-person.oos-sccd.ctyunapi.cn/5763882e-a7f9-4bd2-8771-c04fddde6755.mp4?response-content-disposition=attachment%3Bfilename%3D%22%C3%A5%C2%92%C2%B1%C3%A4%C2%BB%C2%AC%C3%A8%C2%A3%C2%B8%C3%A7%C2%86%C2%8AS04E40.mp4%22&x-amz-CLIENTNETWORK=UNKNOWN&x-amz-CLOUDTYPEIN=CORP&x-amz-CLIENTTYPEIN=UNKNOWN&Signature=mtnGOsSrqOBUsZsBvrDwJMfb3/c%3D&AWSAccessKeyId=caf5e6901807aca55a45&Expires=1612114678&x-amz-limitrate=102400&response-content-type=video/mp4&x-amz-FSIZE=124343921&x-amz-UID=758808201&x-amz-UFID=91368310543255119'
    #url = 'https://cloud189-sichuan-person.oos-sccd.ctyunapi.cn/5e6e8869-e76f-471c-b275-9d5828be516a.mp4?response-content-disposition=attachment%3Bfilename%3D%22%C3%A5%C2%92%C2%B1%C3%A4%C2%BB%C2%AC%C3%A8%C2%A3%C2%B8%C3%A7%C2%86%C2%8AS04E39.mp4%22&x-amz-CLIENTNETWORK=UNKNOWN&x-amz-CLOUDTYPEIN=CORP&x-amz-CLIENTTYPEIN=UNKNOWN&Signature=Sg251f2lcBlOW0qm71e%2BKslEPhE%3D&AWSAccessKeyId=caf5e6901807aca55a45&Expires=1612115360&x-amz-limitrate=102400&response-content-type=video/mp4&x-amz-FSIZE=113269731&x-amz-UID=758808201&x-amz-UFID=91368310543255110'
    #url = 'https://cloud189-shh2-person.oos-sh2.ctyunapi.cn/PERSONCLOUD/167603a5-f47a-4786-b106-56d4131febf3.mp4?response-content-disposition=attachment%3Bfilename%3D%22%C3%A6%C2%97%C2%BA%C3%A8%C2%BE%C2%BE%C3%A5%C2%B9%C2%BB%C3%A8%C2%A7%C2%86S01E04.mp4%22&x-amz-CLIENTNETWORK=UNKNOWN&x-amz-CLOUDTYPEIN=CORP&x-amz-CLIENTTYPEIN=UNKNOWN&Signature=5vvPoS9bP4S7I3fzTHUECsEvVw0%3D&AWSAccessKeyId=e975956edda0be55c086&Expires=1612108749&x-amz-limitrate=102400&response-content-type=video/mp4&x-amz-FSIZE=472043924&x-amz-UID=172982920492925&x-amz-UFID=31303312490064760'
    #args = cli()
    #url =  args['<url>']

    url = args.url
    #print(len(url))
    #print(url)
    file_urls = get_file_url(url)
    print(file_urls)
    for u in file_urls:
        print('download: ' + u)
        dr.download(u)
    #file_url = cli()
    #dr.download(url)

