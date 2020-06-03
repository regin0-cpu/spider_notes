from urllib import parse

import requests
import json
from threading import Thread, Lock
import time
import random
from queue import Queue
from useragents import ua_list
import ssl

class TencentSpider(object):
    def __init__(self):
        self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?tim' \
                       'estamp=1563912271089&countryId=&city' \
                       'Id=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSiz' \
                       'e=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1563912374645&postId={}&language=zh-cn'
        self.one_q = Queue()
        self.two_q = Queue()
        self.lock = Lock()
        self.i = 0

    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        html = requests.get(url=url, headers=headers).text
        return html

    def url_in(self):
        keyword = input('关键字：')
        keyword = parse.quote(keyword)
        total = self.get_total(keyword)
        for index in range(1, total + 1):
            url = self.one_url.format(keyword, index)
            self.one_q.put(url)

    def get_total(self, keyword):
        url = self.one_url.format(keyword, 1)
        html = json.loads(self.get_html(url))
        count = int(html['Data']['Count'])
        if count % 10 == 0:
            total = count // 10
        else:
            total = count // 10 + 1
        return total

    # 一级页面
    def parse_one_page(self):
        while True:
            if not self.one_q.empty():
                one_url = self.one_q.get()
                html = json.loads(self.get_html(one_url))
                for job in html['Data']['Posts']:
                    post_id = job['PostId']
                    two_url = self.two_url.format(post_id)
                    self.two_q.put(two_url)
            else:
                break

    # 二级页面
    def parse_two_page(self):
        while True:
            try:
                two_url = self.two_q.get(block=True, timeout=3)
                html = json.loads(self.get_html(two_url))
                item = {}
                item['name'] = html['Data']['ProductName']
                item['city'] = html['Data']['LocationName']
                item['duty'] = html['Data']['Responsibility']
                item['requ'] = html['Data']['RecruitPostName']
                item['time'] = html['Data']['LastUpdateTime']
                print(item)
                # 存数据

                self.lock.acquire()
                self.i += 1
                self.lock.release()

            except Exception as e:
                break

    def run(self):
        self.url_in()
        one_list = []
        two_list = []
        for i in range(3):
            t = Thread(target=self.parse_one_page)
            one_list.append(t)
            t.start()
        for i in range(5):
            t = Thread(target=self.parse_two_page())
            two_list.append(t)
            t.start()
        for one in one_list:
            one.join()
        for two in two_list:
            two.join()
        print(self.i)


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    t = TencentSpider()
    t.run()
