import requests
from threading import Thread
from queue import Queue
from bs4 import BeautifulSoup
import csv

class Xmshoop_spider(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
        self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId=14&pageSize=30'   # 需要爬取的url,通过改变page的值从而获取所有需要发送请求的url
        self.url_list = Queue()    # 创建先进先出队列
        self.count = 0
        # self.f = open('医疗健康.csv', 'w')
        # self.writer = csv.writer(self.f, lineterminator='\n')
        # self.writer.writerow(["name", "link"])

    def send_request(self):
        while not self.url_list.empty():
            response = requests.get(self.url_list.get(),headers=self.headers).json()   # 通过get方法取出第一个放进去的url，然后将获取到的json数据转为python中的字典类型数据
            self.parse_json(response)


    def parse_json(self,res):
        for data in res['data']:
            name = data['displayName']
            package = data['packageName']
            print(name, package)
            self.get_Privacy(name, package)
            self.count += 1

    def get_Privacy(self, name, package):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
        url = 'http://app.mi.com/details?id=' + package  # 需要爬取的url,通过改变page的值从而获取所有需要发送请求的url
        # url = 'https://app.mi.com/catTopList/0?page=1'
        data = requests.get(url).text
        soup = BeautifulSoup(data,'lxml')
        privacy = soup.find_all(style='float:right;')[5]
        if privacy.find_all(class_ ='privacyNotFoundBtn'):
            link= "none"
        else:
            link = privacy.a['href']

        self.writer.writerow([name, link])


    def main(self):
        t_list = []
        for i in range(0,67):
            self.url_list.put(self.url.format(i))   # 将要爬取的url通过put方法加入到队列中

        for x in range(5):   # for循环5次，总共创建了5个线程去爬取
            t1 = Thread(target=self.send_request)  # 创建线程
            t1.start()        # 启动线程
            t_list.append(t1)

        for t in t_list:
            t.join()   # 主线程会一直阻塞等待子线程结束




if __name__ == '__main__':
    spider = Xmshoop_spider()
    spider.main()
    print(spider.count)  # 显示总共爬取了多少个数据
