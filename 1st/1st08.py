# 爬取贴吧图片

from urllib import request, parse
from lxml import etree

# 下载铁汁的链接
def loadPage(url):
    # 发送请求
    req = request.Request(url)
    # 响应信息
    response = request.urlopen(req)
    # 读取数据
    html = response.read().decode('utf8')
    content = etree.HTML(html)
    link_list = content.xpath('//li/div[@class="t_con cleafix"]/div/div/div/a/@href')
    for link in link_list:
        fullurl = 'https://tieba.baidu.com/' + link
        print(fullurl)
        loadImage(fullurl)


# 下载图片的链接
def loadImage(url):
    # 发送请求
    req = request.Request(url)
    # 响应信息
    response = request.urlopen(req)
    # 读取数据
    html = response.read().decode('utf8')
    content = etree.HTML(html)
    link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    for link in link_list:
        print(link)
        writeImage(link)


def writeImage(url):
    req = request.Request(url)
    response = request.urlopen(req)
    image = response.read()
    filename = url[-12]
    with open(filename, 'wb') as f:
        f.write(image)


def tiebaSpider(url, beginPage, endPage):
    for page in range(beginPage, endPage):
        pn = (page - 1) * 50
        fullurl = url + "&pn=" + str(pn)
        print(fullurl)
        loadPage(fullurl)


if __name__ == '__main__':
    kw = input("请输入需要爬取的贴吧名称:")
    beginPage = int(input("请输入起始页:"))
    endPage = int(input("请输入终止页:"))
    url = "http://www.tieba.baidu.com/?"
    key = parse.urlencode({"kw": kw})
    fullurl = url + key
    tiebaSpider(fullurl, beginPage, endPage)