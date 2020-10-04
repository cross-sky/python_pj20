import requests
import json
import time
import random

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
}

def get_cookie():
    url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
    s = requests.Session()
    s.get(url, headers=headers, timeout=3)
    cookie = s.cookies
    return cookie

def get_page(url, param):
    html = requests.post(url, data=param, headers=headers,
        cookies=get_cookie(), timeout=5)
    json_data = json.loads(html.text)

    page = 2
    get_info(url, page)

def get_info(url, page):
    for pn in range(1, page+1):
        params = {
            "first": "true",
            "pn": str(pn),
            "kd": "python"
            }

        try:
            html = requests.post(url, data=params, headers=headers,
                    cookies=get_cookie(), timeout=5)

            print(url, html.status_code)
            json_data = json.loads(html.text)

            results = json_data['content']['positionResult']['result']
            for result  in results:
                infos = {
                    "positionName": result["positionName"],

                        "companyFullName": result["companyFullName"],
                        "companySize": result["companySize"],
                        "industryField": result["industryField"],
                        "financeStage": result["financeStage"],

                        "firstType": result["firstType"],
                        "secondType": result["secondType"],
                        "thirdType": result["thirdType"],

                        "positionLables": result["positionLables"],

                        "createTime": result["createTime"],

                        "city": result["city"],
                        "district": result["district"],
                        "businessZones": result["businessZones"],

                        "salary": result["salary"],
                        "workYear": result["workYear"],
                        "jobNature": result["jobNature"],
                        "education": result["education"],

                        "positionAdvantage": result["positionAdvantage"]
                    }
                print(infos)
    
        except requests.exceptions.ConnectionError:
                print("requests.exceptions.ConnectionError")
                pass
        
        time.sleep(random.randint(10,20))


if __name__ == '__main__':
    url = "https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false".format('广州')
    # post请求参数
    params = {
        "first": "true",
        "pn": 1,
        "kd": "python"
    }
    get_page(url, params)