import json
from urllib import parse

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import csv


# url = "https://mobile.baidu.com/cateDetail?cateBoardid=board_101_0311&boardid=board_101_0311&f0=cate_soft%400_cateContent%400_cateContentItem%400"
# driver = webdriver.Firefox() #创建driver实例
# driver.get(url)
# for i in range(1, 16):
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#
# html = requests.get(url)
# soup = BeautifulSoup(html.text,'html.parser')
#
#
#
# liebiao = soup.find_all('li', attrs={"class": "app-base-normal boardl-app base-normal--normal"})
#
# for item in liebiao:
#     print(item)
appnum = 0
docnum = 0
accnum = 0
# up_url = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
f = open('母婴育儿.csv', 'w')
writer = csv.writer(f, lineterminator='\n')
writer.writerow(["name", "link"])

headers = {'Accept': 'application/json'}
# for k in range(15):
#     type= k+10
#     up_url[k] = "https://mobile.baidu.com/api/board?boardid=board_101_03"+str(type)+"&pn="
up_url = "https://mobile.baidu.com/api/board?boardid=board_101_0324&pn="
# for j in range(16):
for i in range(20):
    url = up_url+str(i)
    # print(url)
    html=requests.get(url,headers=headers)
    if html.status_code == 200:
        html_bytes = html.content
        html_str = html_bytes.decode()
        # print(html_str)
        write_content = []
        # data = json.loads(html_str)
        data = json.loads(html_bytes)
        all_items=data['data']['data']
        for item in all_items:
             appnum = appnum + 1
             name = item['sname']
             if 'privacyUrl' in item:
                doc = item['privacyUrl']
                print(doc)
                if len(doc) != 0:
                    docnum = docnum + 1
                    acc = requests.get(url, headers=headers)
                    if acc.status_code == 200:
                        accnum = accnum + 1
             else:
                doc = 'none'

             writer.writerow([name, doc])

             # write_content.append({doc})
        # print(write_content)

print("appnum:", appnum)
print("docnum:", docnum)
#