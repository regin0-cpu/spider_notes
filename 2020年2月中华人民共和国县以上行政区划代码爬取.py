import requests, re
from lxml import etree
import ssl


class Zp(object):
    def __init__(self):
        self.herders = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}

        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'


    def get_false_link(self):
        html = requests.get(url=self.url, headers=self.herders).text
        p = etree.HTML(html)
        link = 'http://www.mca.gov.cn' + p.xpath('//table/tr[2]//a/@href')[0]
        self.get_real_link(link)

    def get_real_link(self, link):
        html = requests.get(url=link, headers=self.herders).text
        p = re.compile('window.location.href="(.*?)"', re.S)
        real_link = p.findall(html)[0]
        self.get_data(real_link)

        # with open('gov.html', 'w') as f:
        #     f.write(html)

    def get_data(self, real_link):
        html = requests.get(url=real_link, headers=self.herders).text
        p = etree.HTML(html)
        tr_list = p.xpath('//tr[@height="19"]')
        for tr in tr_list:
            name = tr.xpath('./td[3]/text()')[0].strip()
            try:
                code = tr.xpath('./td[2]/text()')[0].strip()
            except:
                code = tr.xpath('./td[2]/span/text()')[0].strip()
            print(name, code)

    def run(self):
        self.get_false_link()


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    z = Zp()
    z.run()
