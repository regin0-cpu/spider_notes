import requests
import json
from threading import Thread, Lock
from queue import Queue
import time
import random

from lxml import etree

from useragents import ua_list


class XiaoMi(object):
    def __init__(self):
        self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
        self.q = Queue()
        self.i = 0
        self.lock = Lock()

    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        html = requests.get(url=url, headers=headers).text
        return html

    def get_id(self):
        url = 'http://app.mi.com/'
        html = self.get_html(url)
        p = etree.HTML(html)
        li_list = p.xpath('//div[@class="sidebar"]/div[2]/ul[1]/li')
        for li in li_list:
            url_id = li.xpath('./a/@href')[0].split('/')[-1]
            type_name = li.xpath('./a/text()')[0]
            self.url_in(url_id)

    # url 入队列
    def url_in(self, url_id):
        total = self.get_total(url_id)
        for page in range(0, total):
            url = self.url.format(page, url_id)
            self.q.put(url)

    def get_total(self, url_id):
        url = self.url.format(0, url_id)
        html = json.loads(self.get_html(url))
        count = html['count']
        if count % 30:
            return count // 30 + 1
        else:
            return count // 30

    def parse_html(self):
        while True:
            if not self.q.empty():
                time.sleep(1)
                url = self.q.get()
                data = self.get_html(url)
                try:
                    html = json.loads(data)
                    item = {}
                    app_list = []
                    for app in html['data']:
                        item['name'] = app['displayName']
                        item['type'] = app['level1CategoryName']
                        item['link'] = app['packageName']
                        app_list.append((
                            item['name'],
                            item['type'],
                            item['link']
                        ))
                        print(item)

                        self.lock.acquire()
                        self.lock.release()

                        self.lock.acquire()
                        self.i += 1
                        self.lock.release()
                except:
                    print(data)
                    continue
            else:
                break

    def run(self):
        self.get_id()
        t_list = []
        for i in range(3):
            t = Thread(target=self.parse_html)
            t_list.append(t)
            t.start()
        for j in t_list:
            j.join()


if __name__ == '__main__':
    b = time.time()
    s = XiaoMi()
    s.run()
    e = time.time()
    print('数量：', s.i)
    print('执行时间：', e - b)
