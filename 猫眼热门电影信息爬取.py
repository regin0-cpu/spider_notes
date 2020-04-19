from urllib import request, parse
from useragents import ua_list
import time, random, re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class My(object):
    def __init__(self):
        self.url = 'https://maoyan.com/board'
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }

    def get_html(self):
        req = request.Request(url=self.url, headers=self.HEADERS)
        resp = request.urlopen(req)
        html = resp.read().decode()
        return html

    def get_data(self, html):
        r1 = re.compile('.*?<p class="name"><a href=".*?" title=".*?" data-act=".*?" '
                        'data-val="{.*?}">(.*?)</a></p>.*?<p class="star">(.*?)</p>.*?<p '
                        'class="releasetime">(.*?)</p>.*?', re.S)
        data_list = r1.findall(html)
        return data_list

    def run(self):
        html = self.get_html()
        data_list = self.get_data(html)
        for data in data_list:
            with open('file.text', 'a') as f:
                f.write(data[0].strip()+' '*30+data[1].strip()+' '*20+data[2]+'\n')


if __name__ == '__main__':
    m = My()
    m.run()
