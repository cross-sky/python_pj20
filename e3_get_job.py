import requests
import random
import time
from openpyxl import Workbook
import os
import bs_myprint
import json


RESULT_DIR = os.path.dirname(os.path.realpath(__file__)) + r'/result/ex3/'

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
}


headers1 = {
        'Host': 'www.lagou.com',
        'Connection': 'keep-alive',
 #       'Content-Length': '23',
        'Origin': 'https://www.lagou.com',
        'X-Anit-Forge-Code': '0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/79.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Anit-Forge-Token': 'None',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

def get_cookie():
    url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
    s = requests.Session()
    s.get(url, headers=headers, timeout=3)
    cookie = s.cookies
    
    return cookie

def get_json(url, page, lang_name):   
    data = {'first':'true', 'pn':str(page), 'kd':lang_name}

    #session_data = requests.Session()
    #session_data.get(url, headers=headers, timeout=3)
    #cookie_data = get_cookie()
    #time.sleep(3)
    html = requests.post(url, data=data, headers=headers, 
            cookies=get_cookie(), timeout=5
    )
    #result_json = session_data.post(url, data, headers=headers).json()
    #result_json = requests.post(url, data, headers=headers).json()
    result_json = json.loads(html.text)

    if result_json['msg'] is not None:
        bs_myprint.my_print(result_json)
        return None
    
    list_con = result_json['content']['positionResult']['result']
    list_hr = result_json['content']['hrInfoMap']  # dic
    info_list = []

    info_hr = []

    for k in list_con:
        info = []
        info.append(k.get('companyShortName', '无'))
        info.append(k.get('companyFullName', '无'))
        info.append(k.get('industryField', '无'))
        info.append(k.get('financeStage', '无'))
        info.append(k.get('companySize', '无'))
        info.append(k.get('salary', '无'))
        info.append(k.get('city', '无'))
        info.append(k.get('education', '无'))
        info_list.append(info)
        bs_myprint.my_print(info)

    for k in list_hr.keys():
        value = list_hr[k]
        hr = []
        hr.append(value.get('realName', '无'))
        hr.append(value.get('userId', '无'))
        if value.get('portrait', '无') is not None:
            hr.append('https://www.lgstatic.com/'+ value.get('portrait', '无'))
        info_hr.append(hr)
        bs_myprint.my_print(hr)
        
    return info_list, info_hr

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def main():
    lang_name = 'python'
    wb = Workbook()
    create_dir(RESULT_DIR)

    cities = ['北京', '上海', '广州', '深圳', '杭州']
    #cities = ['上海',  '广州']

    ws1 = wb.active
    ws1.title = lang_name

    for i in cities:
        page = 1
        #ws1 = wb.active
        #ws1.title = lang_name
        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(i)
        while page < 7:
            result_data = get_json(url, page, lang_name)
            if result_data is None:
                return
            info, hr = result_data
            page += 1
            time.sleep(random.randint(10,20))
            for i, h in zip(info, hr):
                ws1.append(i + h)
    wb.save(RESULT_DIR + '{}职位信息{}.xlsx'.format(lang_name, time.strftime("%Y-%m-%d %H %M %S")))

if __name__ == "__main__":
    main()
    
