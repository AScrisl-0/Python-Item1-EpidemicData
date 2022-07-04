import re
from urllib import request, parse
import requests
# 添加IP代理的代码

class TieBaSpider(object):

    def __init__(self, kw):
        # 初始化要爬取的页数
        self.page = 1
        # 贴吧的名称
        self.kw = kw
        self.url = 'https://tieba.baidu.com/f?'
        # 代理服务器
        self.proxy = "121.41.8.23:16818"

        # 用户名和密码
        self.username = "469041623"
        self.password = "fv1cq0kl"

        self.proxies = {
            'http': 'http://%(user)s:%(pwd)s@%(ip)s/' % {'user': self.username, 'pwd': self.password, 'ip': self.proxy},
            'https': 'http://%(user)s:%(pwd)s@%(ip)s/' % {'user': self.username, 'pwd': self.password, 'ip': self.proxy}
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}

    # 下载页面方法
    def loadPage(self):
        kw = {"kw": self.kw}
        param = parse.urlencode(kw)
        url = self.url + param
        pn = (self.page - 1) * 50
        url += "&pn=" + str(pn)
        print(url)
        # 发送请求、响应信息
        req = requests.get(url, headers=self.headers, proxies=self.proxies)
        # response = request.urlopen(req)
        # 读取信息
        html = req.content.decode('utf8')
        self.dealPage(html)

    def dealPage(self, html):
        # 正则模板
        pattern = re.compile('<a .* class="j_th_tit ">(.*)</a>')
        titleList = pattern.findall(html)
        for title in titleList:
            print(title)
            self.writePage(title)

    # 把标题写入文本
    def writePage(self, title):
        with open("tieba.txt", "a", encoding="utf8") as f:
            f.write(title + "\n")

    # 控制爬虫
    def startWork(self):
        while True:
            self.loadPage()
            command = input("是否继续爬取(y/n):")
            if command.startswith('y'):
                self.page += 1
            else:
                break


if __name__ == '__main__':
    name = input("请输入需要爬取的贴吧名称:")
    spider = TieBaSpider(name)
    spider.startWork()