# http://image.baidu.com/search/index?tn=baiduimage&word=%E8%B5%B5%E4%B8%BD%E9%A2%96

import requests
from urllib import parse

import time
import random, re, os


class BaiduImage(object):
    def __init__(self):
        self.url = 'https://image.baidu.com/search/index?tn=baiduimage&word={}'
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def get_image(self, url, word):
        html = requests.get(url=url, headers=self.headers).text
        p = re.compile('"thumbURL":"(.*?)"', re.S)
        link_list = p.findall(html)
        self.save_image(link_list, word)

    def save_image(self, link_list, word):
        directory = '/Users/regin1/spider_study/image/{}/'.format(word)
        if not os.path.exists(directory):
            os.makedirs(directory)
        for link in link_list:
            time.sleep(1)
            if not link:
                continue
            html = requests.get(url=link, headers=self.headers).content
            filename = directory + link[-30:]
            with open(filename, 'wb') as f:
                f.write(html)

    def run(self):
        word = input('请输入你想要谁的图片：')
        params = parse.quote(word)
        url = self.url.format(params)
        self.get_image(url, word)


if __name__ == '__main__':
    spider = BaiduImage()
    spider.run()
