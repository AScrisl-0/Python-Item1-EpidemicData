# 正则表达式获取贴吧标题

import re
from urllib import request, parse


class TieBaSpider(object):
    def __init__(self, kw):
        # 初始化要爬取的页数
        self.page = 1
        # 贴吧的名称
        self.kw = kw
        self.url = 'https://tieba.baidu.com/f?'

    # 下载页面方法
    def loadPage(self):
        kw = {"kw": self.kw}
        param = parse.urlencode(kw)
        url = self.url + param
        pn = (self.page - 1) * 50
        url += "&pn=" + str(pn)
        print(url)
        # 发送请求、响应信息
        req = request.Request(url)
        response = request.urlopen(req)
        # 读取信息
        html = response.read().decode('utf8')
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