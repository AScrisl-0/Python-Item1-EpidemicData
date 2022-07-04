from urllib import parse, request
import requests


def loadPage(url):
    # 发送请求
    req = request.Request(url)
    # 响应事件
    response = request.urlopen(req)
    # 读取数据
    html = response.read()
    # 对内容进行解码
    content = html.decode('utf8')
    return content


def writePage(data, filename):
    print("正在保存:" + filename)
    f = open(filename, 'w', encoding='utf8')
    f.write(data)
    f.close()


def tiebaSpider(url, beginPage, endPage):
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        fullurl = url + "&pn=" + str(pn)
        html = loadPage(fullurl)
        filename = "第" + str(page) + "页.html"
        writePage(html, filename)


if __name__ == '__main__':
    kw = input('请输入需要爬取的贴吧名称:')
    beginPage = int(input('请输入起始页:'))
    endPage = int(input('请输入终止页:'))
    url = 'https://tieba.baidu.com/f?'
    key = parse.urlencode({"kw": kw})
    fullurl = url + key
    tiebaSpider(fullurl, beginPage, endPage)