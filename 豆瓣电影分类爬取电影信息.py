import requests
import time
import random, re
from useragents import ua_list
import json
import ssl


class Db(object):
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'

    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        html = requests.get(url=url, headers=headers).text
        return html

    def parse_html(self, url):
        html = self.get_html(url)
        html = json.loads(html)
        item = {}
        for film in html:
            item['name'] = film['title']
            item['score'] = film['score']
            item['time'] = film['release_date']
            print(item)

    def run(self):
        type_dict = self.get_types_dict()
        menu = ''
        for key in type_dict:
            menu = menu + key + '|'
        print(menu)

        type_name = input('请输入电影类型：')
        if not type_dict:
            print('无结果')
            return
        types = type_dict[type_name]
        total = self.get_total(types)
        # total = int(total)
        for start in range(0, total, 20):
            url = self.url.format(types, start)
            self.parse_html(url)
            time.sleep(random.uniform(0, 1))

    def get_types_dict(self):
        url = 'https://movie.douban.com/chart'
        html = self.get_html(url)
        p = re.compile('<span><a href=".*?type_name=(.*?)&type=(.*?)&interval_id=100:90&action=">.*?</a></span>', re.S)
        r_list = p.findall(html)
        types_dict = {}
        for r in r_list:
            types_dict[r[0]] = r[1]
        return types_dict

    def get_total(self, types):
        url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(types)

        html = json.loads(self.get_html(url))
        total = html['total']
        return total


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    spider = Db()
    spider.run()
