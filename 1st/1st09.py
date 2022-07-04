import  re
from urllib import request,parse

class TieBaSpider(object):
    def __init__(self,kw):
        self.page = 1
        self.kw = kw
        self.url='https://tieba/baidu.com/f?'
    # 下载页面方法
    def loadpage(self):
        kw = {"kw:",self.kw}
        param = parse.urlencode(kw)
        url = self.url + param
        pn = (self.page - 1) * 50
        url +="&pn=" + str(pn)
        print(url)
        # 发送请求，响应信息
        req = request.Request(url)
        response = request.urlopen(req)
        # 读取信息
        html = response.read().decode('utf-8')
        self.dealpage(html)

    def dealpage(self,html):
        # 正则式
        pattern = re.complie('<a .* class="j_th_tit ">(.*)</a>')
        titlelist = pattern.findall(html)
        for title in titlelist:
            print(title)
            self.writepage(title)

    # 标题写入文本
    def writepage(self,title):
        with open('tieba.txt',"a",encoding="utf-8") as f:
            f.write(title + "\n")

    # 控制爬虫
    def startwork(self):
        while True:
            self.loadpage()
            command = input("是否继续爬取(y/n):")
            if command.startswith('y'):
                self.page+=1
            else:
                break

if __name__ == '__main__':
    name = input("请输入需要爬取的贴吧名称：")
    spider = TieBaSpider(name)
    spider.startwork()